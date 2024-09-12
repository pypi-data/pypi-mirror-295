import gzip
import json
import re
from collections import defaultdict
from itertools import groupby
from pathlib import Path
from tempfile import TemporaryDirectory

import frictionless
import minify_html
import pandas as pd
import unidecode
from jinja2 import Environment, PackageLoader
from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from paralex import to_markdown
from tqdm import tqdm

env = Environment(loader=PackageLoader("mkdocs_paralex_plugin"))


class ParalexConfig(Config):
    paralex_package_path = c.Optional(c.File(exists=True))
    paradigm_pages = c.Type(bool, default=True)
    layout_rows = c.ListOfItems(c.Type(str), default=[])
    layout_columns = c.ListOfItems(c.Type(str), default=[])
    layout_tables = c.ListOfItems(c.Type(str), default=[])
    frequency_sample = c.Type(bool, default=True)
    sample_size = c.Type(int, default=-1)
    compress = c.Type(bool, default=False)


class ParalexSite(BasePlugin[ParalexConfig]):

    def on_config(self, config):
        """
        Note:
            the config argument contains mkdocs global config
            self.config contains the config for this plugin

        """
        self.dir = Path(config.get("config_file_path")).parent
        try:
            self.package_path = self.config.get("paralex_package_path") or next(Path(self.dir).glob("*.package.json"))
        except StopIteration:
            raise ValueError("Can not find your .package.json file."
                             "Please either put it in the same  directory as the config file, "
                             "or specify a path with the config option paralex_package_path.")
        self.layout_rows = self.config.get("layout_rows")
        self.layout_columns = self.config.get("layout_columns")
        self.layout_tables = self.config.get("layout_tables")
        self.frequency_sample = self.config.get("frequency_sample")
        self.sample_size = self.config.get("sample_size")

        assert (self.layout_rows or not self.layout_columns) and \
               (self.layout_rows or not self.layout_tables)
        self.paradigm_pages = self.config.get("paradigm_pages")
        self.cleaners = []
        self.do_compress = self.config.get("compress")

        with open(self.package_path, 'r', encoding="utf-8") as f:
            self.package = json.load(f)

        self.tmp_dir = TemporaryDirectory("data_tmp_")
        self.cleaners.append(self.tmp_dir.cleanup)

        # Add any css / js / etc.
        config["extra_css"].insert(0,
                                   "https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css")  # So that it has lower priority than user files.
        config["extra_css"].insert(0, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css")
        config["extra_css"].insert(0, "css/paralex_styles.css")  # So that it has lower priority than user files.

        if not config.get("copyright", None):
            footer = ""
            if "contributors" in self.package:
                footer += "by " + ", ".join([auth['title'] for auth in self.package["contributors"]]) + "."
            if "licenses" in self.package:
                footer += f" licenses: " + ", ".join(
                    [f"<a href='{ls['path']}'>{ls['name']}</a>" for ls in self.package["licenses"]]) + ". "
            config["copyright"] = footer
        config[
            "copyright"] += "This lexicon follows the <a href='https://www.paralex-standard.org/'>paralex</a> standard."
        if "theme" in config and "logo" not in config["theme"]:
            config["theme"]["logo"] = "paralex.png"
            self.add_paralex_logo = True

    def on_pre_build(self, *args, config):
        # Simlink readme to index if there is no index in the docs directory
        doc_dir = Path(config.get("docs_dir"))
        readmes = list((self.dir.glob("[Rr][eE][aA][dD][mM][eE].md")))
        readme = readmes[0] if readmes else None
        index = (doc_dir / "index.md")
        if not index.exists() and readme is not None:
            index.symlink_to(readme)
            self.cleaners.append(index.unlink)

    def on_files(self, files, *, config):
        here = Path(__file__).parent
        files.append(File("paralex_styles.css", str(here / "css"), config['site_dir'] + "/css/", False))
        tables = {"forms": None,
                  "lexemes": None,
                  "features-values": None}

        if self.add_paralex_logo:
            dest = Path(self.tmp_dir.name) / "paralex.png"
            src = Path(__file__).parent / "paralex.png"
            dest.write_bytes(src.read_bytes())
            files.append(File(dest.name, self.tmp_dir.name, config['site_dir'], False))

        for resource in self.package["resources"]:
            new_files = csv_to_html_table(resource, self.tmp_dir.name,
                                          with_paradigms=self.paradigm_pages,
                                          compressed=self.do_compress)
            name = resource["name"]
            if name in tables:
                tables[name] = resource
            for filename in new_files:
                files.append(File(filename, self.tmp_dir.name, config['site_dir'], False))

        package_out = Path(self.tmp_dir.name) / "metadata.md"
        to_markdown(frictionless.Package(self.package_path), package_out, title="Metadata")
        files.append(File("metadata.md", self.tmp_dir.name, config['site_dir'], False))

        if self.paradigm_pages:
            if tables["features-values"] is None:
                raise ValueError("Can not generate paradigms tables if there is no features table.")

            if tables["lexemes"] is None:
                raise ValueError("Can not generate paradigm tables if there is no lexemes table.")

            (Path(self.tmp_dir.name) / "details").mkdir(exist_ok=True)

            forms_df = read_pandas(tables["forms"]["path"])
            features = read_pandas(tables["features-values"]["path"], index_col=0)
            lexemes = read_pandas(tables["lexemes"]["path"])

            # Restrict to a sample of lexemes
            if self.sample_size > 0:  # Using -1 as a sentinel value, as None isn't a valid default for mkdocs
                if self.frequency_sample and "frequency" in lexemes.columns:
                    lexemes = lexemes.sort_values("frequency", ascending=False)[:self.sample_size]
                else:
                    lexemes = lexemes.sample(self.sample_size)
                sampled = set(lexemes.lexeme_id)
                forms_df = forms_df[forms_df.lexeme.isin(sampled)]

            # Separate cells features according to layout
            if not self.layout_rows:
                self.layout_rows = features.index.tolist()

            dim_to_f = defaultdict(list)
            for i, f in features.feature.items():
                dim_to_f[f].append(i)
            feature_grouper = dict(**{v: "tables" for f in self.layout_tables for v in dim_to_f[f]},
                                   **{v: "rows" for f in self.layout_rows for v in dim_to_f[f]},
                                   **{v: "cols" for f in self.layout_columns for v in dim_to_f[f]},
                                   )

            used_dimensions = set(dim_to_f)
            known_dimensions = set(self.layout_rows + self.layout_tables + self.layout_columns)
            undef_dimensions = used_dimensions - known_dimensions
            if undef_dimensions:
                raise ValueError("Undefined features found. "
                                 "Edit your config file to add "
                                 "these to tables, rows or cols: {}".format(", ".join(undef_dimensions)))

            cells = {cell: parse_cell(cell, feature_grouper) for cell in forms_df.cell.unique()}
            forms_df.loc[:, ["tables", "rows", "cols"]] = forms_df.cell.apply(lambda x: cells[x])

            if "canonical_order" in features.columns:
                cell_sorter = {elt: cell_order(elt, features.canonical_order)
                               for c in cells for _, elt in cells[c].fillna("").items()}
            else:
                # TODO: default to something sensible here...
                cell_sorter = {elt: 0 for c in cells for _, elt in cells[c].fillna("").items()}

            with tqdm(total=lexemes.shape[0]) as pbar:
                p_files = forms_df.groupby("lexeme") \
                    .apply(paradigm_to_html,
                           self.tmp_dir.name,
                           cell_sorter,
                           lexemes.set_index("lexeme_id"),
                           pbar)
                for f in p_files:
                    files.append(File(f, self.tmp_dir.name, config['site_dir'], False))

        return files

    def on_post_build(self, *, config):
        for clean_action in self.cleaners:
            clean_action()


def paradigm_to_html(paradigm, out_dir, sorter, lexemes, pbar):
    table_dict = paradigm_to_json(paradigm, sorter)
    lexeme = paradigm.name
    # Load jinja template
    template = env.get_template("paradigm.md")

    table = template.render(tables=table_dict,
                            lexeme=lexeme,
                            lexeme_info=lexemes.loc[lexeme, :].to_dict()
                            )
    table = minify_html.minify(table)

    filename = f"details/{slug(lexeme)}.txt"
    table_out = Path(out_dir) / filename
    with table_out.open("w", encoding="utf-8") as f:
        f.write(table)
    pbar.update(1)
    return filename


def paradigm_to_json(paradigm, sorter):
    """Go from long form to a json dict

    tables: [ # list of tables (dict)
                { # A table
                    headers: [] # list of headers (str)
                    indexes:  [] # list of indexes (str)
                    rows: [ # list of content rows
                            [ # one row is a list
                                { # One original form entry, multiple can be at the same coordinates
                                    phon_form: xyz # col/vals from original df
                                }
                        ]
                    ]
                },

                {} # another table...
            ]
    """

    def one_paradigm_to_json(table):
        table_data = {"headers": table.cols.unique().tolist(),
                      "indexes": [],
                      "rows": [],
                      "name": table.name
                      }
        col_to_i = {c: i for i, c in enumerate(table_data["headers"])}
        row_list = []
        for idx, data in table.groupby("rows"):  # groupby doesn't respect row order !
            idx_hr = []
            if idx:
                idx_hr.append(idx)
            r = [None for _ in col_to_i]
            for col, entries in data.groupby("cols"):
                r[col_to_i[col]] = entries.to_dict('records')
            row_list.append((idx, ".".join(idx_hr), r))

        # Sort the row order
        row_list = sorted(row_list, key=lambda x: sorter[x[0]])
        table_data["indexes"] = [x[1] for x in row_list]
        table_data["rows"] = [x[2] for x in row_list]
        return table_data

    ts = paradigm.sort_values(by=["tables", "rows", "cols"],
                              key=lambda x: x.map(sorter)) \
        .fillna("") \
        .groupby("tables").apply(one_paradigm_to_json).to_list()
    ts = sorted(ts, key=lambda t: sorter[t["name"]])
    return ts


def cell_order(cell, order):
    return tuple(order.get(f, default=0) for f in cell.split("."))


def parse_cell(cell, feature_sorter):
    def sort_func(val):
        r = feature_sorter.get(val)
        if r is None:
            print("Err at:", val)
            print("sorter is:", feature_sorter)
            return float("inf")
        return r

    features = sorted(cell.split("."), key=sort_func)
    groups = groupby(features, sort_func)
    return pd.Series({k: ".".join(g) for k, g in groups}, index=["tables", "rows", "cols"])


def slug(string):
    slug = unidecode.unidecode(str(string))
    return re.sub(r'[\W]+', '-', slug)


def read_pandas(path, **kwargs):
    data = pd.read_csv(path,
                       na_values=['', 'NaN'],
                       keep_default_na=False,
                       **kwargs).fillna("")
    return data


def get_id(name):
    return "id_" + slug(name)


def table_to_json(resource, infos=None, with_paradigms=False):
    ## If paradigm tables, add links to tables from lexeme...
    df = read_pandas(resource["path"])
    table_dict = {}
    fields = {f["name"]: f for f in resource["schema"]["fields"]}
    pkey = set(resource["schema"].get("primaryKey", {})).pop()

    # Add styling classes
    for f in fields:
        name = fields[f]["name"]
        fields[f]["classes"] = [slug(name)]
        if name == pkey:
            fields[f]["classes"].append("table_id")

    # prepare foreign key url
    rels = {}
    for relation in resource["schema"].get("foreignKeys", []):
        fs = relation["fields"][0]
        table = relation["reference"]["resource"]
        id_col = relation["reference"]["fields"][0]
        if id_col.endswith("_id"):
            rels[fs] = f"{table}.html#" + "{}"

    table_dict["columns"] = [fields.get(col, {"name": col}) for col in df.columns]

    # Prepare rows
    table_dict["rows"] = []
    for id, row in df.iterrows():
        row_data = {col: cell for col, cell in zip(df.columns, row)}
        table_dict["rows"].append(row_data)
        if pkey:
            row_data["DT_RowId"] = get_id(row_data[pkey])
        for col, url in rels.items():
            row_data[col] = f"<a href={url.format(get_id(row_data[col]))}>{row_data[col]}</a>"

    table_dict["infos"] = infos

    if resource["name"] == "lexemes":
        for row in table_dict["rows"]:
            row["details"] = "details/" + slug(row["lexeme_id"]) + ".txt"
    return table_dict


def write_compressed(path, content):
    # Touch (tricks gitlab into serving gziped file)
    with path.open("w", encoding="utf-8") as f:
        pass

    # Write gziped file
    gziped = path.with_suffix(path.suffix + ".gz")
    with gzip.open(gziped, mode="wt", encoding="utf-8") as f:
        f.write(content)

    return gziped


def csv_to_html_table(resource, out_dir, with_paradigms, compressed=False):
    files = []
    template = env.get_template("table.md")

    table_data = table_to_json(resource, with_paradigms=with_paradigms)

    json_content = json.dumps({"data": table_data["rows"]},
                              indent=None,
                              separators=(',', ':'))
    json_out = Path(out_dir) / (resource["name"] + ".json")
    files.append(json_out.name)
    if compressed:
        compressed_path = write_compressed(json_out, json_content)
        files.append(compressed_path.name)
    else:
        with json_out.open("w", encoding="utf-8") as f:
            f.write(json_content)

    table = template.render(columns=table_data["columns"],
                            current_page=resource["name"],
                            json_src=json_out.name
                            )
    limit = table.find('<')
    header = table[0:limit]
    table = header + minify_html.minify(table[limit:])
    table_out = Path(out_dir) / (resource["name"] + ".md")
    with table_out.open("w", encoding="utf-8") as f:
        f.write(table)
    files.append(table_out.name)

    return files

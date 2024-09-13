---
hide:
    - navigation
    - toc
    - path
---

<table id="{{current_page}}" class='dataTable table table-hover display {{current_page}}'>
<thead>
<tr>
{% for column in columns %}
  <th class='table-col-header'><div title="{{ column["description"] }}"> {{ column["name"] }} </div></th>
{% endfor %}
</thead>
</table>

{% block datatables %}
<script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.js" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
<script type="text/javascript" src="https://cdn.datatables.net/plug-ins/1.13.4/api/row().show().js"></script>
<script>

var details = details ? JSON.parse(details) : {};

function select_row(table) {
    var id = "#" + location.hash.slice(1);
    if (id != "#"){
        let row = table.row(id);
        row.show().draw(false);
        $(id).toggleClass('selected');
        row.scrollTo();
    }
};

$(document).ready(function() {
    var table = $('#{{current_page}}').DataTable({
        ajax: "{{json_src}}",
        paging: true,
        deferRender: true,
        language: {
            search: ""
        },
        pageLength: 10,
        search: {
            "regex": false,
        },
        orderCellsTop: true,
        columns: [
            {% for c in columns %}
                { "defaultContent": "",
                  "data":"{{c["name"]}}",
                "className":"{{ c['classes']|join(' ') }}",
                    {% if ('url' in c) and c['url'] is not none %}
                        "render": function ( data, type, row, meta ) {return '<a href="{{c['url']}}' + data + '">' + data + '</a>';}
                    {% elif c["name"].endswith('_tag') %}
                        "render": function ( data, type, row, meta ) {
                            if (data === '') {
                                return data;
                            }
                              else {
                                return data.split("|").map(tag => '<span class="paralex_tag"><a href="tags.html#id_' + tag + '">' + tag + '</a></span>').join(" ");
                            }
                        }
                    {% elif "form" in c["name"] %}
                        "render": function ( data, type, row, meta ) {
                            if (data === '#DEF#') {
                                return '<span class="defective">defective</span>' ;
                            } else {
                                return '<span class="form">'+data+'</span>'
                            }
                            }
                    {% endif %}
                },
        {% endfor %}
        ],
    initComplete: function() { select_row(this.api())}
    });

    $('#lexemes tbody').on('click', 'td.lexeme_id', function (event) {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    row.child(this.responseText, "detail-child").show();
                    tr.addClass('shown');
                }
            };
            xhttp.open("GET", row.data()["details"], true);
            xhttp.send();
            }
        });
    $('[type=search]').each(function () {
        $(this).attr("placeholder", "Search...");
        $(this).before('<span class="fa fa-search"></span>');
    });
});
</script>
{% endblock %}
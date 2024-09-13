{% for table in tables %}
<table class="paradigm_table">
    <thead>
    <caption >
            {{  table["name"] }}
    </caption>
    <tr>
        <th></th>
        {% for col in table["headers"] %}
            <th>{{ col }}</th>
        {% endfor %}
    </tr>
    </thead>
    <tbody>
    {% for row in table["rows"] %}
        <tr>
            <th>{{ table["indexes"][loop.index-1] }}</th>
            {% for data in row %}
                <td>
                    {% if data is not none %}
                        <ul class='form_sets list-unstyled'>
                            {% for form_group in data %}
                                <li class="form_set">
                                    {% if "orth_form" in form_group %}
                                        {% if form_group["orth_form"] == "#DEF#" %}
                                        <span class="formtype orth_form defective">defective</span>
                                        {% else %}
                                        <span class="formtype orth_form">{{ form_group["orth_form"] }}</span>
                                        {% endif %}
                                    {% endif %}
                                    {% if "segmented_orth_form" in form_group %}
                                        {% if form_group["segmented_orth_form"] == "#DEF#" %}
                                        <span class="formtype segmented_orth_form defective">defective</span>
                                        {% else %}
                                        <span class="formtype segmented_orth_form">{{ form_group["segmented_orth_form"] }}</span>
                                        {% endif %}
                                    {% endif %}
                                    {% if "phon_form" in form_group %}
                                        {% if form_group["phon_form"] == "#DEF#" %}
                                        <span class="formtype phon_form defective">defective</span>
                                        {% else %}
                                        <span class="formtype phon_form">/{{ form_group["phon_form"] | replace(" ","") }}/</span>
                                        {% endif %}
                                    {% endif %}
                                    {% if "segmented_phon_form" in form_group %}
                                        {% if form_group["segmented_phon_form"] == "#DEF#" %}
                                        <span class="formtype segmented_phon_form defective">defective</span>
                                        {% else %}
                                        <span class="formtype segmented_phon_form">/{{ form_group["segmented_phon_form"] | replace(" ","") }}/</span>
                                        {% endif %}
                                    {% endif %}
                                </li>
                            {% endfor %}
                        </ul>
                    {% endif %}
                </td>
            {% endfor %}
        </tr>

    {% endfor %}
    </tbody>
</table>
{% endfor %}
from bs4 import BeautifulSoup
import json

def generate_filled_html(json_path, template_path, output_path):
    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Load HTML template
    with open(template_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Field mappings for direct text fields
    field_mapping = {
        "project-name": "project-name",
        "target-release": "release-target",
        "project-contacts": "contacts",
        "form-completed-by": "completed-by",
        "date": "date",
        "why": "why-content",
        "technical-changes": "technical-details",
        "dependencies": "dependencies-content",
        "code-refactoring": "refactoring-content",
        "mobile-impact": "mobile-impact-details",
        "future-regression-testing": "future-regression-details",
        "environment": "environment-details",
        "additional-notes": "additional-notes-content"
    }

    # Field mappings for list fields
    list_mapping = {
        "in-scope": "in-scope",
        "out-of-scope": "out-scope",
        "testing-requirements": "testing-details",  # special handling below
        "regression-functionality-areas": "regression-areas"
    }

    # Fill single-value fields
    for json_key, html_id in field_mapping.items():
        value = json_data.get(json_key, "")
        tag = soup.find(id=html_id)
        if tag:
            tag.string = value

    # Fill list fields
    for json_key, html_id in list_mapping.items():
        list_items = json_data.get(json_key, [])
        tag = soup.find(id=html_id)
        if tag and tag.name == "ul":
            tag.clear()
            for item in list_items:
                li = soup.new_tag("li")
                li.string = item
                tag.append(li)
        elif html_id == "testing-details" and isinstance(list_items, list):  # testing-requirements is <p>
            tag = soup.find(id=html_id)
            if tag:
                tag.string = ", ".join(list_items)

    # Write the filled HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

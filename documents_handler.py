import os
from datetime import datetime
from documents_processor import process_document
from merge_documents_gpt import get_gpt_response
from generate_filled_html import generate_filled_html


import json
# Set your folder path here
folder_path = r'docs'
# List of accepted document extensions
document_extensions = ['.docx', '.pdf']
# Get list of (filename, full_path, last_modified_time)
documents = []
for filename in os.listdir(folder_path):
    full_path = os.path.join(folder_path, filename)
    if(
        os.path.isfile(full_path)
        and any(filename.lower().endswith(ext) for ext in document_extensions)
    ):
         modified_time = os.path.getmtime(full_path)
         documents.append((filename, full_path, modified_time))


# Sort by last modified time (most recent first)
documents.sort(key=lambda x: x[2])
#Template to be defined
document_json_final = response_format = {
    "project-name": "",
    "target-release": "",
    "project-contacts": "",
    "form-completed-by": "",
    "date": "",
    "why": "",
    "in-scope": [],
    "out-of-scope": [],
    "technical-changes": "",
    "dependencies": "",
    "code-refactoring": "",
    "testing-requirements": [],
    "mobile-impact": "",
    "future-regression-testing": "",
    "environment": "",
    "additional-notes": "",
    "regression-functionality-areas": []
}


# Print the results
for filename, path, mod_time in documents:
    readable_time = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{filename} - Last Modified: {readable_time} - Full Path: {path}")
    # Calling the method to extract the contents of document into JSON
    document_json = process_document(path)
    # Transform the JSON and merge the revisions into One 
    document_json_transformed = get_gpt_response(document_json, document_json_final)
    document_json_final = document_json_transformed
   

# generate a html based on the JSON
print(json.dumps(json.loads(document_json_final)))
#Below code logic is temporary and can be removed
#---------
json_filename = "Final_Merged_Doc_V1" + ".json"
with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(json.loads(document_json_final), json_file, indent=2)
#Converting the stringified JSON into JSON object
# -------- 
finalJsonObj = json.loads(document_json_final)
#Place holder for calling appropriate method to generate HTML         
generate_filled_html(
    json_path="Final_Merged_Doc_V1.json",
    template_path="Template.html",
    output_path="Generated_Doc.html"
)
    
import os
import fitz  # PyMuPDF for PDFs
import docx  # for .docx files
import json
from datetime import datetime

# Function to extract text from PDF file
def extract_text_from_pdf(filepath):
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from DOCX file
def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to create JSON from document
def process_document(filepath):
    filename = os.path.basename(filepath)
    modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract content based on file type
    if filename.endswith(".pdf"):
        content = extract_text_from_pdf(filepath)
    elif filename.endswith(".docx"):
        content = extract_text_from_docx(filepath)
    else:
        raise ValueError("Unsupported file type. Please use .docx or .pdf")

    # Build the JSON object
    json_obj = {
        "Document_name": filename,
        "modified_date": modified_date,
        "content": content
    }

    return json_obj

# List to hold all processed document JSONs
all_documents = []

# Main loop to process documents one by one
while True:
    print("\n📂 Upload a document (PDF or DOCX). Type 'exit' to finish.")
    filepath = input("Enter full file path: ").strip()

    if filepath.lower() == "exit":
        break

    if not os.path.isfile(filepath):
        print("❌ File does not exist. Try again.")
        continue

    try:
        # Process the document and get the JSON
        document_json = process_document(filepath)

        # Add to the list
        all_documents.append(document_json)

        # Save to a JSON file (e.g., sample.docx → sample.docx.json)
        json_filename = filepath + ".json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(document_json, json_file, indent=2)

        print(f"✅ JSON saved as: {json_filename}")

    except Exception as e:
        print(f"⚠️ Error processing file: {e}")

# Optionally, print or use the final list of all document JSONs
print("\nAll processed documents:")
for doc in all_documents:
    print(f"- {doc['Document_name']}")

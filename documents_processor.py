import os
import fitz  # PyMuPDF for PDFs
import docx  # for .docx files
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

import os
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import tempfile

def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("PyPDF2 failed, trying OCR fallback:", e)

    if text.strip():
        return text

    # OCR Fallback
    text = ""
    images = convert_from_path(file_path)
    for image in images:
        text += pytesseract.image_to_string(image)

    return text

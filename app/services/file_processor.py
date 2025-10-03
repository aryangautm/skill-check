import io
from typing import Tuple
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    pdf_file = io.BytesIO(file_content)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file."""
    docx_file = io.BytesIO(file_content)
    doc = Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text.strip()


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file."""
    return file_content.decode('utf-8').strip()


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extract text from file based on extension."""
    extension = filename.lower().split('.')[-1]
    
    if extension == 'pdf':
        return extract_text_from_pdf(file_content)
    elif extension in ['doc', 'docx']:
        return extract_text_from_docx(file_content)
    elif extension == 'txt':
        return extract_text_from_txt(file_content)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

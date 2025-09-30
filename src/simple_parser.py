import re
import PyPDF2
import docx
import pandas as pd
import os

def safe_text_read(file_path):
    """Safely read text files with multiple encoding fallbacks"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'windows-1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, use replace strategy
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        print(f"All encoding attempts failed for {file_path}: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Basic PDF text extraction"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """Basic DOCX text extraction"""
    try:
        doc = docx.Document(docx_path)
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
        return ""

def extract_basic_fields(text):
    """Extract email and phone using simple regex"""
    if not text:
        return {'email': '', 'phone': '', 'text': ''}
    
    email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    
    return {
        'email': email[0] if email else '',
        'phone': phone[0] if phone else '',
        'text': text
    }

# For backward compatibility
def extract_text_from_txt(txt_path):
    """Extract text from TXT files with encoding fallback"""
    return safe_text_read(txt_path)

if __name__ == "__main__":
    # Test with encoding robustness
    print("Testing simple parser with robust encoding...")

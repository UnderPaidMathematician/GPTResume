import os
from docx import Document
import pdfplumber
import win32com.client as win32
import re


class TextExtractor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.resume_text = self.extract_text()
        self.resume_text = self.clean_text(self.resume_text)

    def extract_text(self):
        """Extract text based on the format of the resume text."""
        if self.filepath.endswith('.docx'):
            return self.extract_text_from_docx()
        elif self.filepath.endswith('.doc'):
            converted_docx_path = self.convert_doc_to_docx()
            self.filepath = converted_docx_path  # Update the file path to the converted .docx file
            return self.extract_text_from_docx()
        elif self.filepath.endswith('.pdf'):
            return self.extract_text_from_pdf()
        else:
            raise ValueError("Unsupported file format")

    def extract_text_from_docx(self):
        """Extract text from docx."""
        doc = Document(self.filepath)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text_from_pdf(self):
        """Helper function to extract text from pdf file"""
        text = ''
        with pdfplumber.open(self.filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def convert_doc_to_docx(self):
        """Helper function for converting doc to docx format"""
        # Check if the file exists
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file {self.filepath} does not exist")

        word = win32.gencache.EnsureDispatch('Word.Application')
        try:
            doc = word.Documents.Open(self.filepath)
            doc_path_new = self.filepath + 'x'
            doc.SaveAs2(doc_path_new, FileFormat=16)  # FileFormat=16 for DOCX
            doc.Close()
        except Exception as e:
            print(f"Error occurred while converting .doc to .docx: {e}")
            raise
        finally:
            word.Quit()
        return doc_path_new

    def clean_text(self, text):
        """Clean resume text."""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Replace various bullet point symbols with a standard symbol
        text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]', '-', text)

        # Fix hyphenated words
        text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)

        # Trim leading and trailing spaces
        text = text.strip()

        return text

    def get_text(self):
        """Get resume text."""
        return self.resume_text

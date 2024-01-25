import os
import time
from docx import Document
import pdfplumber
import win32com.client as win32
import re


class TextExtractor:
    """Extracts text from all files in a directory with .doc, .docx, and pdf extensions.
    Then cleans up the text. Currently, throws a value error if the file is not one of the expected formats."""
    def __init__(self, filepath):
        self.filepath = filepath
        self.extracted_text = self.extract_text()
        self.cleaned_text = self.clean_text(self.extracted_text)

    def extract_text(self):
        """Extract text based on the format of the resume text."""
        if self.filepath.endswith('.docx'):
            return self.extract_text_from_docx()
        elif self.filepath.endswith('.doc'):
            return self.convert_doc_to_docx()
        elif self.filepath.endswith('.pdf'):
            return self.extract_text_from_pdf()
        else:
            raise ValueError("Unsupported file format")

    def extract_text_from_docx(self):
        """Extract text from docx."""
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f"No file found at {self.filepath}")
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
        """Converts a .doc file to .docx format and returns the text."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"The file {self.filepath} does not exist")

        word = win32.gencache.EnsureDispatch('Word.Application')
        word.Visible = False  # Run Word in the background
        doc = None
        try:
            doc = word.Documents.Open(self.filepath)
            text = []
            for para in doc.Paragraphs:
                text.append(para.Range.Text.strip())
            text = "\n".join(text)
        except Exception as e:
            print(f"Error occurred while converting .doc to .docx: {e}")
            raise
        finally:
            if doc is not None:
                doc.Close(False)  # Close the document without saving
            word.Quit()
            # Next time will consider a more elegant approach. Currently, giving system time to close word document.
            time.sleep(1)
        return text

    @staticmethod
    def clean_text(text):
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
        """Get cleaned text."""
        return self.cleaned_text

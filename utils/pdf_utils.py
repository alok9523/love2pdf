# utils/pdf_utils.py

from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs(pdf_list, output_path):
    """Merge multiple PDFs into one."""
    pdf_writer = PdfWriter()
    for pdf in pdf_list:
        pdf_reader = PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
    with open(output_path, "wb") as out_pdf:
        pdf_writer.write(out_pdf)

def split_pdf(input_pdf, output_dir):
    """Split a PDF into separate pages."""
    pdf_reader = PdfReader(input_pdf)
    for i in range(len(pdf_reader.pages)):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[i])
        with open(os.path.join(output_dir, f"page_{i+1}.pdf"), "wb") as out_pdf:
            pdf_writer.write(out_pdf)

def encrypt_pdf(input_pdf, output_pdf, password):
    """Encrypt a PDF with a password."""
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()
    for page in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page])
    pdf_writer.encrypt(password)
    with open(output_pdf, "wb") as out_pdf:
        pdf_writer.write(out_pdf)
# handlers/convert.py

import os
from pdf2image import convert_from_path
from docx import Document
from fpdf import FPDF
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

def pdf_to_images(update: Update, context: CallbackContext) -> None:
    """Converts a PDF to images (PNG format)."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    images = convert_from_path(file_path)

    for i, img in enumerate(images):
        image_path = os.path.join(FILE_STORAGE, f"page_{i+1}.png")
        img.save(image_path, "PNG")
        update.message.reply_photo(photo=open(image_path, "rb"))

    update.message.reply_text("✅ PDF converted to images!")

def docx_to_pdf(update: Update, context: CallbackContext) -> None:
    """Converts a DOCX file to PDF."""
    if not context.user_data.get("docx_file"):
        update.message.reply_text("Please send a DOCX file first.")
        return

    file_path = context.user_data["docx_file"]
    pdf_path = os.path.join(FILE_STORAGE, "converted.pdf")

    doc = Document(file_path)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for para in doc.paragraphs:
        pdf.multi_cell(0, 10, para.text)

    pdf.output(pdf_path)

    update.message.reply_document(document=open(pdf_path, "rb"), filename="converted.pdf")
    update.message.reply_text("✅ DOCX converted to PDF!")

def txt_to_pdf(update: Update, context: CallbackContext) -> None:
    """Converts a TXT file to PDF."""
    if not context.user_data.get("txt_file"):
        update.message.reply_text("Please send a TXT file first.")
        return

    file_path = context.user_data["txt_file"]
    pdf_path = os.path.join(FILE_STORAGE, "converted.pdf")

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.readlines()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text:
        pdf.multi_cell(0, 10, line)

    pdf.output(pdf_path)

    update.message.reply_document(document=open(pdf_path, "rb"), filename="converted.pdf")
    update.message.reply_text("✅ TXT converted to PDF!")
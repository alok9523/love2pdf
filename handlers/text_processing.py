# handlers/text_processing.py

import os
from PyPDF2 import PdfReader
from docx import Document
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

def extract_text_from_pdf(update: Update, context: CallbackContext) -> None:
    """Extracts text from a PDF file."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    pdf_reader = PdfReader(file_path)
    extracted_text = ""

    for page in pdf_reader.pages:
        extracted_text += page.extract_text() + "\n"

    if not extracted_text.strip():
        update.message.reply_text("❌ No text found in this PDF.")
        return

    text_file_path = os.path.join(FILE_STORAGE, "extracted_text.txt")
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    update.message.reply_document(document=open(text_file_path, "rb"), filename="extracted_text.txt")
    update.message.reply_text("✅ Extracted text from PDF!")

def txt_to_docx(update: Update, context: CallbackContext) -> None:
    """Converts a TXT file to a DOCX file."""
    if not context.user_data.get("txt_file"):
        update.message.reply_text("Please send a TXT file first.")
        return

    file_path = context.user_data["txt_file"]
    docx_path = os.path.join(FILE_STORAGE, "converted.docx")

    doc = Document()
    with open(file_path, "r", encoding="utf-8") as text_file:
        for line in text_file:
            doc.add_paragraph(line)

    doc.save(docx_path)

    update.message.reply_document(document=open(docx_path, "rb"), filename="converted.docx")
    update.message.reply_text("✅ TXT converted to DOCX!")
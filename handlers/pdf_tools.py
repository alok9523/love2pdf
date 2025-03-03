# handlers/pdf_tools.py

import os
from PyPDF2 import PdfReader, PdfWriter
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

def merge_pdfs(update: Update, context: CallbackContext) -> None:
    """Merges multiple PDFs into one."""
    files = context.user_data.get("pdf_files", [])
    if len(files) < 2:
        update.message.reply_text("Please send at least two PDFs to merge.")
        return
    
    output_path = os.path.join(FILE_STORAGE, "merged.pdf")
    pdf_writer = PdfWriter()

    for file_path in files:
        pdf_reader = PdfReader(file_path)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)

    update.message.reply_document(document=open(output_path, "rb"), filename="merged.pdf")
    update.message.reply_text("✅ Merged PDF is ready!")

def split_pdf(update: Update, context: CallbackContext) -> None:
    """Splits a PDF into separate pages."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    pdf_reader = PdfReader(file_path)
    
    for i, page in enumerate(pdf_reader.pages):
        pdf_writer = PdfWriter()
        pdf_writer.add_page(page)
        output_path = os.path.join(FILE_STORAGE, f"page_{i+1}.pdf")
        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)
        
        update.message.reply_document(document=open(output_path, "rb"), filename=f"page_{i+1}.pdf")

    update.message.reply_text("✅ PDF has been split into individual pages!")

def compress_pdf(update: Update, context: CallbackContext) -> None:
    """Compresses a PDF (simple implementation)."""
    update.message.reply_text("⚠️ Compression feature will be improved in future versions!")

def protect_pdf(update: Update, context: CallbackContext) -> None:
    """Adds a password to a PDF."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a PDF first.")
        return

    password = context.args[0] if context.args else "1234"  # Default password if not provided
    file_path = context.user_data["pdf_file"]
    output_path = os.path.join(FILE_STORAGE, "protected.pdf")

    pdf_reader = PdfReader(file_path)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(password)

    with open(output_path, "wb") as output_file:
        pdf_writer.write(output_file)

    update.message.reply_document(document=open(output_path, "rb"), filename="protected.pdf")
    update.message.reply_text(f"✅ PDF protected with password: `{password}`")
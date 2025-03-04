import os
from telegram import Update
from telegram.ext import CallbackContext
from docx import Document
from fpdf import FPDF
from config import FILE_STORAGE

async def docx_to_pdf(update: Update, context: CallbackContext) -> None:
    """Converts a DOCX file to PDF."""
    document = update.message.document

    if document.mime_type != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        await update.message.reply_text("❌ Please send a valid DOCX file.")
        return

    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(FILE_STORAGE, document.file_name)
    await file.download_to_drive(file_path)
    
    docx_file = file_path
    pdf_file = os.path.splitext(docx_file)[0] + ".pdf"

    convert_docx_to_pdf(docx_file, pdf_file)

    with open(pdf_file, "rb") as pdf:
        await update.message.reply_document(pdf)

    await update.message.reply_text(f"✅ DOCX converted to PDF: {os.path.basename(pdf_file)}")

def convert_docx_to_pdf(docx_file, pdf_file):
    doc = Document(docx_file)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for paragraph in doc.paragraphs:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, paragraph.text)

    pdf.output(pdf_file)

# Add this function to the handlers/convert.py file
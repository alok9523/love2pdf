import os
from pdf2image import convert_from_path
from docx import Document
from fpdf import FPDF
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

### 📌 Handle Receiving PDF ###
async def receive_pdf(update: Update, context: CallbackContext):
    """Handles PDF file uploads and converts them to images."""
    document = update.message.document

    if document.mime_type != "application/pdf":
        await update.message.reply_text("❌ Please send a valid PDF file.")
        return

    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(FILE_STORAGE, document.file_name)

    await file.download_to_drive(file_path)
    context.user_data["pdf_file"] = file_path

    await update.message.reply_text(f"✅ File received: {document.file_name}\nSaved successfully!")

    # Convert PDF to images after saving
    await pdf_to_images(update, context)

### 📌 Convert PDF to Images ###
async def pdf_to_images(update: Update, context: CallbackContext):
    """Converts a PDF to images (PNG format)."""
    if "pdf_file" not in context.user_data:
        await update.message.reply_text("❌ No PDF found. Please send a PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    
    try:
        images = convert_from_path(file_path)

        for i, img in enumerate(images):
            image_path = os.path.join(FILE_STORAGE, f"page_{i+1}.png")
            img.save(image_path, "PNG")
            with open(image_path, "rb") as image_file:
                await update.message.reply_photo(photo=image_file)

        await update.message.reply_text("✅ PDF converted to images!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error converting PDF: {str(e)}")

### 📌 Handle Receiving DOCX ###
async def receive_docx(update: Update, context: CallbackContext):
    """Handles DOCX file uploads and converts them to PDF."""
    document = update.message.document

    if document.mime_type not in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        await update.message.reply_text("❌ Please send a valid DOCX file.")
        return

    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(FILE_STORAGE, document.file_name)

    await file.download_to_drive(file_path)
    context.user_data["docx_file"] = file_path

    await update.message.reply_text(f"✅ File received: {document.file_name}\nSaved successfully!")

    # Convert DOCX to PDF after saving
    await docx_to_pdf(update, context)

### 📌 Convert DOCX to PDF ###
async def docx_to_pdf(update: Update, context: CallbackContext):
    """Converts a DOCX file to PDF."""
    if "docx_file" not in context.user_data:
        await update.message.reply_text("❌ No DOCX found. Please send a DOCX file first.")
        return

    file_path = context.user_data["docx_file"]
    pdf_path = os.path.join(FILE_STORAGE, "converted.pdf")

    try:
        doc = Document(file_path)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, para.text)

        pdf.output(pdf_path)

        with open(pdf_path, "rb") as pdf_file:
            await update.message.reply_document(document=pdf_file, filename="converted.pdf")

        await update.message.reply_text("✅ DOCX converted to PDF!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error converting DOCX: {str(e)}")

### 📌 Handle Receiving TXT ###
async def receive_txt(update: Update, context: CallbackContext):
    """Handles TXT file uploads and converts them to PDF."""
    document = update.message.document

    if document.mime_type not in ["text/plain"]:
        await update.message.reply_text("❌ Please send a valid TXT file.")
        return

    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(FILE_STORAGE, document.file_name)

    await file.download_to_drive(file_path)
    context.user_data["txt_file"] = file_path

    await update.message.reply_text(f"✅ File received: {document.file_name}\nSaved successfully!")

    # Convert TXT to PDF after saving
    await txt_to_pdf(update, context)

### 📌 Convert TXT to PDF ###
async def txt_to_pdf(update: Update, context: CallbackContext):
    """Converts a TXT file to PDF."""
    if "txt_file" not in context.user_data:
        await update.message.reply_text("❌ No TXT found. Please send a TXT file first.")
        return

    file_path = context.user_data["txt_file"]
    pdf_path = os.path.join(FILE_STORAGE, "converted.pdf")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.readlines()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in text:
            pdf.multi_cell(0, 10, line)

        pdf.output(pdf_path)

        with open(pdf_path, "rb") as pdf_file:
            await update.message.reply_document(document=pdf_file, filename="converted.pdf")

        await update.message.reply_text("✅ TXT converted to PDF!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error converting TXT: {str(e)}")
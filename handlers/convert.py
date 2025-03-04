import os
from pdf2image import convert_from_path
from docx import Document
from fpdf import FPDF
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

### 📌 Handle Receiving PDF ###
async def receive_pdf(update: Update, context: CallbackContext):
    """Handles PDF file uploads and processes based on the caption command."""
    document = update.message.document
    caption = update.message.caption  # Extract caption

    if document.mime_type != "application/pdf":
        await update.message.reply_text("❌ Please send a valid PDF file.")
        return

    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(FILE_STORAGE, document.file_name)

    await file.download_to_drive(file_path)
    context.user_data["pdf_file"] = file_path

    await update.message.reply_text(f"✅ File received: {document.file_name}\nSaved successfully!")

    # 📌 Check if caption contains "/pdf_to_images"
    if caption and caption.strip() == "/pdf_to_images":
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
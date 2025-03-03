# handlers/image_processing.py

import os
from PIL import Image
from fpdf import FPDF
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

def images_to_pdf(update: Update, context: CallbackContext) -> None:
    """Converts multiple images into a single PDF."""
    if not context.user_data.get("image_files"):
        update.message.reply_text("Please send images first.")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)

    for img_path in context.user_data["image_files"]:
        image = Image.open(img_path)
        pdf.add_page()
        pdf.image(img_path, x=10, y=10, w=190)  

    pdf_path = os.path.join(FILE_STORAGE, "images_to_pdf.pdf")
    pdf.output(pdf_path)

    update.message.reply_document(document=open(pdf_path, "rb"), filename="converted.pdf")
    update.message.reply_text("✅ Images converted to PDF!")

def compress_image(update: Update, context: CallbackContext) -> None:
    """Compresses an image to reduce its size."""
    if not context.user_data.get("image_file"):
        update.message.reply_text("Please send an image first.")
        return

    file_path = context.user_data["image_file"]
    output_path = os.path.join(FILE_STORAGE, "compressed.jpg")

    image = Image.open(file_path)
    image.save(output_path, "JPEG", quality=40)  

    update.message.reply_document(document=open(output_path, "rb"), filename="compressed.jpg")
    update.message.reply_text("✅ Image compressed successfully!")
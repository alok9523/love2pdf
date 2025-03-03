# handlers/file_handler.py

import os
from telegram import Update, Document
from telegram.ext import CallbackContext
from config import FILE_STORAGE
from telegram import Update, PhotoSize

# Ensure the file storage directory exists
os.makedirs(FILE_STORAGE, exist_ok=True)

def handle_file(update: Update, context: CallbackContext) -> None:
    document: Document = update.message.document
    file_id = document.file_id
    file_name = document.file_name

    # Get the file from Telegram servers
    file = context.bot.get_file(file_id)
    
    # Save file to local storage
    file_path = os.path.join(FILE_STORAGE, file_name)
    file.download(file_path)

    update.message.reply_text(f"✅ File received: {file_name}\nSaved successfully!")


def handle_image(update: Update, context: CallbackContext) -> None:
    """Handles incoming images and stores them."""
    photo: PhotoSize = update.message.photo[-1]  # Get highest resolution
    file = context.bot.get_file(photo.file_id)
    
    file_path = os.path.join(FILE_STORAGE, f"{photo.file_id}.jpg")
    file.download(file_path)

    if "image_files" not in context.user_data:
        context.user_data["image_files"] = []
    context.user_data["image_files"].append(file_path)

    update.message.reply_text("✅ Image received and saved!")
# handlers/file_handler.py

import os
from telegram import Update, Document
from telegram.ext import CallbackContext
from config import FILE_STORAGE

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
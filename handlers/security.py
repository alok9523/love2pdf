# handlers/security.py

import os
from PyPDF2 import PdfReader, PdfWriter
from cryptography.fernet import Fernet
from telegram import Update
from telegram.ext import CallbackContext
from config import FILE_STORAGE

# Generate a key for encryption (should be stored securely)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def add_password_to_pdf(update: Update, context: CallbackContext) -> None:
    """Adds a password to a PDF file."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    output_path = os.path.join(FILE_STORAGE, "protected.pdf")
    password = "1234"  # You can allow users to set a password

    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(file_path)

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.encrypt(password)
    with open(output_path, "wb") as f:
        pdf_writer.write(f)

    update.message.reply_document(document=open(output_path, "rb"), filename="protected.pdf")
    update.message.reply_text("✅ PDF password protected!")

def remove_password_from_pdf(update: Update, context: CallbackContext) -> None:
    """Removes a password from a PDF file."""
    if not context.user_data.get("pdf_file"):
        update.message.reply_text("Please send a password-protected PDF first.")
        return

    file_path = context.user_data["pdf_file"]
    output_path = os.path.join(FILE_STORAGE, "unprotected.pdf")
    password = "1234"  # Ask users for the correct password

    pdf_reader = PdfReader(file_path)
    if pdf_reader.decrypt(password):
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        with open(output_path, "wb") as f:
            pdf_writer.write(f)

        update.message.reply_document(document=open(output_path, "rb"), filename="unprotected.pdf")
        update.message.reply_text("✅ PDF password removed!")
    else:
        update.message.reply_text("❌ Incorrect password!")

def encrypt_file(update: Update, context: CallbackContext) -> None:
    """Encrypts a file using Fernet encryption."""
    if not context.user_data.get("file"):
        update.message.reply_text("Please send a file first.")
        return

    file_path = context.user_data["file"]
    output_path = os.path.join(FILE_STORAGE, "encrypted_file.enc")

    with open(file_path, "rb") as f:
        encrypted_data = cipher_suite.encrypt(f.read())

    with open(output_path, "wb") as f:
        f.write(encrypted_data)

    update.message.reply_document(document=open(output_path, "rb"), filename="encrypted_file.enc")
    update.message.reply_text("✅ File encrypted successfully!")

def decrypt_file(update: Update, context: CallbackContext) -> None:
    """Decrypts a file using Fernet encryption."""
    if not context.user_data.get("file"):
        update.message.reply_text("Please send an encrypted file first.")
        return

    file_path = context.user_data["file"]
    output_path = os.path.join(FILE_STORAGE, "decrypted_file")

    with open(file_path, "rb") as f:
        decrypted_data = cipher_suite.decrypt(f.read())

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    update.message.reply_document(document=open(output_path, "rb"), filename="decrypted_file")
    update.message.reply_text("✅ File decrypted successfully!")
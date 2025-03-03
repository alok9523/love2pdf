# utils/keyboard.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    """Returns the main menu inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("📂 Upload File", callback_data="upload_file")],
        [InlineKeyboardButton("📄 PDF Tools", callback_data="pdf_tools"),
         InlineKeyboardButton("🖼 Image Tools", callback_data="image_tools")],
        [InlineKeyboardButton("🔒 Security", callback_data="security_tools")],
    ]
    return InlineKeyboardMarkup(keyboard)

def pdf_tools_keyboard():
    """Returns the PDF tools menu."""
    keyboard = [
        [InlineKeyboardButton("📑 Merge PDFs", callback_data="merge_pdf"),
         InlineKeyboardButton("✂ Split PDF", callback_data="split_pdf")],
        [InlineKeyboardButton("🔐 Encrypt PDF", callback_data="encrypt_pdf")],
        [InlineKeyboardButton("⬅ Back", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)
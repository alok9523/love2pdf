import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
)
from config import BOT_TOKEN
from handlers import start, file_handler, pdf_tools, convert, image_processing, text_processing, security, admin
from database.db_manager import init_db 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database tables
init_db()

def main():
    """Main function to run the Telegram bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start.start_command))
    dp.add_handler(CommandHandler("help", start.handle_help))
    dp.add_handler(CommandHandler("admin", admin.handle_admin))

    # File handling
    dp.add_handler(MessageHandler(Filters.document, file_handler.handle_file))
    dp.add_handler(MessageHandler(Filters.photo, file_handler.handle_image))

    # PDF tools
    dp.add_handler(CommandHandler("merge_pdf", pdf_tools.merge_pdfs))
    dp.add_handler(CommandHandler("split_pdf", pdf_tools.split_pdf))
    dp.add_handler(CommandHandler("compress_pdf", pdf_tools.compress_pdf))
    dp.add_handler(CommandHandler("protect_pdf", pdf_tools.protect_pdf))

    # File conversion
    dp.add_handler(CommandHandler("convert", convert.handle_conversion))

# Image processing

    dp.add_handler(CommandHandler("image_to_pdf", image_processing.images_to_pdf))  # Correct function name

    dp.add_handler(CommandHandler("compress_image", image_processing.compress_image))

# Text processing
    dp.add_handler(CommandHandler("extract_text", text_processing.extract_text_from_pdf))
    dp.add_handler(CommandHandler("txt_to_docx", text_processing.convert_txt_to_docx))

# Security features
    dp.add_handler(CommandHandler("encrypt", security.encrypt_file))
    dp.add_handler(CommandHandler("decrypt", security.decrypt_file))  # Ensure it's properly aligned


        # Error handling (Properly defined before usage)
    dp.add_error_handler(error_handler)

    # Start the bot
updater.start_polling()
updater.idle()

if __name__ == "__main__":
    main()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
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

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a message to the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text("An error occurred, please try again later.")

def main():
    """Main function to run the Telegram bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start.start_command))
    application.add_handler(CommandHandler("help", start.handle_help))
    application.add_handler(CommandHandler("admin", admin.handle_admin))

    # File handling
    application.add_handler(MessageHandler(filters.Document.ALL, file_handler.handle_file))
    application.add_handler(MessageHandler(filters.PHOTO, file_handler.handle_image))

    # PDF tools
    application.add_handler(CommandHandler("merge_pdf", pdf_tools.merge_pdfs))
    application.add_handler(CommandHandler("split_pdf", pdf_tools.split_pdf))
    application.add_handler(CommandHandler("compress_pdf", pdf_tools.compress_pdf))
    application.add_handler(CommandHandler("protect_pdf", pdf_tools.protect_pdf))

    # File conversion
    application.add_handler(CommandHandler("pdf_to_images", convert.pdf_to_images))
    application.add_handler(CommandHandler("docx_to_pdf", convert.docx_to_pdf))
    application.add_handler(CommandHandler("txt_to_pdf", convert.txt_to_pdf))

    # Image processing
    application.add_handler(CommandHandler("image_to_pdf", image_processing.images_to_pdf))  
    application.add_handler(CommandHandler("compress_image", image_processing.compress_image))

    # Text processing
    application.add_handler(CommandHandler("extract_text", text_processing.extract_text_from_pdf))
    application.add_handler(CommandHandler("txt_to_docx", text_processing.txt_to_docx))

    # Security features
    application.add_handler(CommandHandler("encrypt", security.encrypt_file))
    application.add_handler(CommandHandler("decrypt", security.decrypt_file))

    # Error handling
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
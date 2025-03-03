# bot.py

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from config import TOKEN
from handlers import start, file_handler

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register handlers
    dp.add_handler(CommandHandler("start", start.start_command))
    dp.add_handler(MessageHandler(Filters.document, file_handler.handle_file))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
# handlers/start.py

from telegram import Update
from telegram.ext import CallbackContext

def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_text = f"Hello, {user.first_name}! 👋\n\n"
    welcome_text += "I am an advanced file bot. Send me a file, and I'll process it for you!"
    
    update.message.reply_text(welcome_text)
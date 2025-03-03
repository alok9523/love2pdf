from telegram import Update
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_text = f"Hello, {user.first_name}! 👋\n\n"
    welcome_text += "I am an advanced file bot. Send me a file, and I'll process it for you!"
    
    await update.message.reply_text(welcome_text)

async def handle_help(update: Update, context: CallbackContext) -> None:
    """Send a help message."""
    help_text = "📌 Available commands:\n"
    help_text += "/start - Start the bot\n"
    help_text += "/help - Get help information\n"
    help_text += "/admin - Admin commands\n"
    await update.message.reply_text(help_text)
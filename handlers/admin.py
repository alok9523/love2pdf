import os
import time
from telegram import Update
from telegram.ext import CallbackContext
from config import ADMIN_ID, FILE_STORAGE, LOG_FILE

def handle_admin(update: Update, context: CallbackContext) -> None:
    """Admin panel command handler."""
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized to access the admin panel.")
        return

    admin_text = (
        "🔧 **Admin Panel** 🔧\n\n"
        "/status - Check bot status\n"
        "/list_users - List registered users\n"
        "/clear_logs - Clear log files\n"
        "/delete_old_files - Delete old stored files\n"
    )
    update.message.reply_text(admin_text)

def check_bot_status(update: Update, context: CallbackContext) -> None:
    """Check if the bot is running properly."""
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized to use this command.")
        return

    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - context.bot_data.get("start_time", 0)))
    update.message.reply_text(f"✅ Bot is running!\n⏳ Uptime: {uptime}")

def list_users(update: Update, context: CallbackContext) -> None:
    """List all registered users (stored in users.db)."""
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized to use this command.")
        return

    from database.db_manager import get_all_users
    users = get_all_users()
    
    if users:
        user_list = "\n".join([f"{user[0]} - {user[1]}" for user in users])  # Assuming (user_id, username)
        update.message.reply_text(f"📜 Registered Users:\n{user_list}")
    else:
        update.message.reply_text("📜 No users registered yet.")

def clear_logs(update: Update, context: CallbackContext) -> None:
    """Clear log files to free up space."""
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized to use this command.")
        return

    try:
        open(LOG_FILE, "w").close()
        update.message.reply_text("✅ Logs cleared successfully.")
    except Exception as e:
        update.message.reply_text(f"❌ Failed to clear logs: {e}")

def delete_old_files(update: Update, context: CallbackContext) -> None:
    """Delete old files from storage to free up space."""
    if update.message.from_user.id != ADMIN_ID:
        update.message.reply_text("❌ You are not authorized to use this command.")
        return

    deleted_count = 0
    for root, _, files in os.walk(FILE_STORAGE):
        for file in files:
            file_path = os.path.join(root, file)
            if time.time() - os.path.getctime(file_path) > 7 * 24 * 3600:  # Files older than 7 days
                os.remove(file_path)
                deleted_count += 1

    update.message.reply_text(f"🗑️ Deleted {deleted_count} old files.")
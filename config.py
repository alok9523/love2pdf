import os  # Ensure os is imported

BOT_TOKEN = "7889602638:AAFtqbV5K_4uCEJcCL4DmdnkdJ0QCzVjrtg"  # Replace with your actual bot token
ADMIN_ID = int(os.getenv("ADMIN_ID", 6195379665))  # Replace with your actual admin ID
FILE_STORAGE = os.getenv("FILE_STORAGE", "/app/files/")  # Default file storage path
LOG_FILE = os.getenv("LOG_FILE", "/app/logs/bot.log")  # Default log file path
DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/database/users.db")  # Default database path
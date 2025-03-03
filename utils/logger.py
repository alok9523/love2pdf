# utils/logger.py

import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging settings
logging.basicConfig(
    filename=os.path.join("logs", "bot_activity.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_activity(activity):
    """Log general bot activities."""
    logging.info(activity)

def log_error(error):
    """Log errors and exceptions."""
    logging.error(error, exc_info=True)

def log_file_activity(user_id, file_name, action):
    """Log file operations (upload, convert, delete, etc.)."""
    log_message = f"User {user_id}: {action} - {file_name}"
    logging.info(log_message)
# database/db_manager.py

import sqlite3
from config import DATABASE_PATH

# Initialize the database
def init_db():
    """Create necessary tables if they don't exist."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # File records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_id TEXT PRIMARY KEY,
                user_id INTEGER,
                file_name TEXT,
                file_type TEXT,
                file_size INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        conn.commit()

# Add a new user
def add_user(user_id, username, first_name, last_name):
    """Insert a new user into the database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, last_name))
        conn.commit()

# Get all users
def get_all_users():
    """Retrieve all registered users."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users")
        return cursor.fetchall()

# Add a file record
def add_file(file_id, user_id, file_name, file_type, file_size):
    """Insert a new file record into the database."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO files (file_id, user_id, file_name, file_type, file_size)
            VALUES (?, ?, ?, ?, ?)
        """, (file_id, user_id, file_name, file_type, file_size))
        conn.commit()

# Get files by user
def get_files_by_user(user_id):
    """Retrieve all files uploaded by a specific user."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_name, file_type, file_size, uploaded_at FROM files WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

# Clear old files from the database
def delete_old_files(days=7):
    """Delete file records older than a specified number of days."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM files WHERE uploaded_at < datetime('now', ? || ' days')
        """, (-days,))
        conn.commit()
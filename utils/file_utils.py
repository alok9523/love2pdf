# utils/file_utils.py

import os

def ensure_directory_exists(directory):
    """Ensure that the specified directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_extension(filename):
    """Extract file extension from a filename."""
    return os.path.splitext(filename)[1].lower()

def is_valid_file_type(filename, allowed_extensions):
    """Check if a file has a valid extension."""
    return get_file_extension(filename) in allowed_extensions

def delete_file(filepath):
    """Delete a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
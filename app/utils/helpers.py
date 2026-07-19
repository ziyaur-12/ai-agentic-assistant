import os
import uuid
from datetime import datetime

def generate_session_id() -> str:
    """Har user session ke liye unique ID banata hai"""
    return str(uuid.uuid4())

def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_directory_exists(path: str):
    """Agar folder exist nahi karta to bana deta hai"""
    os.makedirs(path, exist_ok=True)

def is_valid_pdf(filename: str) -> bool:
    return filename.lower().endswith(".pdf")

def clean_text(text: str) -> str:
    """Extra whitespace aur newlines clean karta hai"""
    return " ".join(text.split())

def truncate_text(text: str, max_length: int = 500) -> str:
    """Lambi text ko limit tak trim karta hai (logging/display ke liye)"""
    return text[:max_length] + "..." if len(text) > max_length else text
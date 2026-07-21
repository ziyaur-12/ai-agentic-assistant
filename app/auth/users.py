import json
import os
import bcrypt
from datetime import datetime

USERS_FILE = "data/users.json"

def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_users(data):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def signup(username: str, password: str):
    users = _load_users()
    username = username.strip().lower()

    if not username or not password:
        return {"success": False, "message": "Username and password are required."}

    if username in users:
        return {"success": False, "message": "Username already exists."}

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users[username] = {
        "password_hash": hashed.decode("utf-8"),
        "created_at": datetime.now().isoformat()
    }
    _save_users(users)
    return {"success": True, "message": "Account created successfully."}

def login(username: str, password: str):
    users = _load_users()
    username = username.strip().lower()

    if username not in users:
        return {"success": False, "message": "Invalid username or password."}

    stored_hash = users[username]["password_hash"].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        return {"success": True, "message": "Login successful."}
    else:
        return {"success": False, "message": "Invalid username or password."}
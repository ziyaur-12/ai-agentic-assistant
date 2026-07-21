import json
import os
from typing import List, Dict
from datetime import datetime

MEMORY_FILE = "data/chat_sessions.json"

def _load_all_sessions() -> Dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def _save_all_sessions(data: Dict):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ConversationMemory:
    def __init__(self, session_id: str, max_history: int = 50):
        self.session_id = session_id
        self.max_history = max_history
        all_sessions = _load_all_sessions()
        session_data = all_sessions.get(session_id, {})
        self.history: List[Dict[str, str]] = session_data.get("history", [])
        self.title: str = session_data.get("title", "New Chat")
        self.created_at: str = session_data.get("created_at", datetime.now().isoformat())

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        if self.title == "New Chat" and role == "user":
            self.title = content[:40]

        self._persist()

    def _persist(self):
        all_sessions = _load_all_sessions()
        all_sessions[self.session_id] = {
            "title": self.title,
            "history": self.history,
            "created_at": self.created_at
        }
        _save_all_sessions(all_sessions)

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def clear(self):
        self.history = []
        all_sessions = _load_all_sessions()
        if self.session_id in all_sessions:
            del all_sessions[self.session_id]
            _save_all_sessions(all_sessions)


def get_session_memory(session_id: str) -> ConversationMemory:
    return ConversationMemory(session_id)

def list_all_sessions() -> List[Dict]:
    """Sabhi saved chats ki list deta hai, sabse naya pehle"""
    all_sessions = _load_all_sessions()
    result = [
        {"session_id": sid, "title": data.get("title", "New Chat"), "created_at": data.get("created_at", "")}
        for sid, data in all_sessions.items()
    ]
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return result
from typing import List, Dict

class ConversationMemory:
    """Simple in-memory conversation history tracker.
    Production me isse database (PostgreSQL/MongoDB) se replace karna."""

    def __init__(self, max_history: int = 10):
        self.history: List[Dict[str, str]] = []
        self.max_history = max_history

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # Purani history trim karo agar limit cross ho jaye
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def get_formatted_history(self) -> str:
        """LLM ko context ke liye readable string format me history do"""
        formatted = ""
        for msg in self.history:
            formatted += f"{msg['role'].upper()}: {msg['content']}\n"
        return formatted

    def clear(self):
        self.history = []


# Global memory store — har user/session ka apna memory object
user_sessions: Dict[str, ConversationMemory] = {}

def get_session_memory(session_id: str) -> ConversationMemory:
    if session_id not in user_sessions:
        user_sessions[session_id] = ConversationMemory()
    return user_sessions[session_id]
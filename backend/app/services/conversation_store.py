# app/services/conversation_store.py
import time
from collections import deque
from typing import Dict, List
from uuid import uuid4


class ConversationStore:
    """
    Historial en memoria con TTL.
    No sustituye BD, solo ayuda al contexto del prompt.
    """

    def __init__(self, ttl_seconds: int = 1800):
        self.ttl = ttl_seconds
        self.sessions: Dict[str, Dict] = {}

    def _cleanup(self):
        """Elimina sesiones expiradas."""
        now = time.time()
        expired = [
            sid for sid, data in self.sessions.items()
            if now - data.get("updated_at", now) > self.ttl
        ]
        for sid in expired:
            self.sessions.pop(sid, None)

    def new_session(self) -> str:
        """Crea nueva sesión de conversación."""
        self._cleanup()
        sid = uuid4().hex
        self.sessions[sid] = {
            "messages": deque(maxlen=10),
            "updated_at": time.time(),
        }
        return sid

    def append(self, session_id: str, role: str, text: str):
        """Agrega mensaje al historial de la sesión."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "messages": deque(maxlen=10),
                "updated_at": time.time(),
            }
        self.sessions[session_id]["messages"].append(
            {"role": role, "text": text}
        )
        self.sessions[session_id]["updated_at"] = time.time()
        self._cleanup()

    def history(self, session_id: str) -> List[Dict[str, str]]:
        """Obtiene historial de la sesión."""
        self._cleanup()
        return list(self.sessions.get(session_id, {}).get("messages", []))

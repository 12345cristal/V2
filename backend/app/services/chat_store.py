"""
Almacenamiento de sesiones de chat y historial en BD
"""
import os
from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage
from datetime import datetime, timedelta

class ChatStore:
    """Almacena y recupera sesiones y mensajes de chat desde BD"""
    
    def new_session(self, db: Session, nino_id: int | None = None) -> str:
        """
        Crea una nueva sesión de chat
        """
        sid = os.urandom(16).hex()
        try:
            session = ChatSession(session_id=sid, nino_id=nino_id)
            db.add(session)
            db.commit()
        except Exception:
            db.rollback()
            raise
        print(f"[ChatStore] Nueva sesión: {sid}")
        return sid

    def ensure_session(self, db: Session, session_id: str, nino_id: int | None = None) -> str:
        """
        Asegura que la sesión existe; si no, la crea
        """
        s = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if s:
            return session_id
        
        try:
            db.add(ChatSession(session_id=session_id, nino_id=nino_id))
            db.commit()
        except Exception:
            db.rollback()
            raise
        print(f"[ChatStore] Sesión creada (ensure): {session_id}")
        return session_id

    def append(self, db: Session, session_id: str, role: str, content: str):
        """
        Agrega un mensaje a la sesión
        """
        if role not in ("usuario", "asistente"):
            raise ValueError("Rol inválido en chat: debe ser 'usuario' o 'asistente'")

        try:
            msg = ChatMessage(session_id=session_id, role=role, content=content)
            db.add(msg)
            
            # Actualizar last_seen_at
            session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
            if session:
                session.last_seen_at = datetime.utcnow()
            
            db.commit()
        except Exception:
            db.rollback()
            raise

    def history(self, db: Session, session_id: str, limit: int = 8):
        """
        Recupera historial de una sesión (últimos N mensajes)
        """
        rows = (db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.asc())
                .all())
        
        # Retorna los últimos 'limit' mensajes
        rows = rows[-limit:] if rows else []
        return [{"role": r.role, "text": r.content} for r in rows]
    
    def cleanup_old_sessions(self, db: Session, days: int = 7):
        """
        Limpia sesiones inactivas más viejas que N días
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        old_sessions = db.query(ChatSession).filter(
            ChatSession.last_seen_at < cutoff
        ).all()
        
        try:
            for session in old_sessions:
                # Eliminar mensajes asociados
                db.query(ChatMessage).filter(
                    ChatMessage.session_id == session.session_id
                ).delete()
                db.delete(session)
            
            db.commit()
        except Exception:
            db.rollback()
            raise
        print(f"[ChatStore] Limpieza: eliminadas {len(old_sessions)} sesiones antiguas")

# Instancia global
chat_store = ChatStore()

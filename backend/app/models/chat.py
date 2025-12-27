"""
Modelos para Chat - Persistencia de conversaciones
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class ChatSession(Base):
    """Sesión de chat del usuario"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(32), unique=True, index=True, nullable=False)
    nino_id = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    active = Column(Boolean, default=True)

class ChatMessage(Base):
    """Mensaje individual en una sesión"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(32), ForeignKey("chat_sessions.session_id", ondelete="CASCADE", onupdate="CASCADE"), index=True, nullable=False)
    role = Column(String(16), nullable=False)  # "usuario" | "asistente"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

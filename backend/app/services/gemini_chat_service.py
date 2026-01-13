# app/services/gemini_chat_service.py
from __future__ import annotations

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import google.generativeai as genai
from pydantic import BaseModel, Field

from app.core.config import settings


class ChatMessage(BaseModel):
    role: str = Field(..., description="Rol: 'user' o 'assistant'")
    content: str = Field(..., description="Contenido del mensaje")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True


class ChatSession(BaseModel):
    session_id: str
    nino_id: int
    usuario_id: int
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True


class GeminiChatService:
    """Servicio de chat integrado con Google Gemini AI"""
    
    def __init__(self):
        """Inicializa el servicio de chat con Gemini"""
        self.is_configured = False
        
        # Validar que la API key esté configurada
        if not settings.GEMINI_API_KEY:
            print("⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada.")
            return
        
        try:
            # Configurar la API de Google Generative AI
            genai.configure(api_key=settings.GEMINI_API_KEY)
            
            # Usar GEMINI_MODEL (no GEMINI_MODEL_ID)
            self.model_name = settings.GEMINI_MODEL
            self.model = genai.GenerativeModel(self.model_name)
            
            self.is_configured = True
            print(f"✓ Servicio Gemini inicializado con modelo: {self.model_name}")
        except Exception as e:
            print(f"⚠ Error al inicializar Gemini: {str(e)}")
            return
        
        # Almacenar sesiones de chat en memoria (usar Redis en producción)
        self.chat_sessions: Dict[str, ChatSession] = {}
        
        # Sistema de prompt para el asistente
        self.system_prompt = """Eres un asistente especializado en apoyo educativo y emocional para niños con autismo.

Tu rol es:
1. Proporcionar información clara y accesible sobre temas educativos
2. Ofrecer apoyo emocional y motivación
3. Ser paciente, empático y comprensivo
4. Utilizar lenguaje simple y directo
5. Respetar los ritmos de aprendizaje individuales
6. Fomentar la autoestima y confianza
7. Sugerir estrategias de afrontamiento cuando sea necesario

Considera siempre:
- La edad del niño
- Sus intereses específicos
- Sus necesidades de comunicación
- El contexto de su educación

Responde siempre de manera amigable, positiva y motivadora."""

    def create_chat_session(self, session_id: str, nino_id: int, usuario_id: int) -> ChatSession:
        """Crea una nueva sesión de chat"""
        if not self.is_configured:
            raise ValueError("Servicio Gemini no configurado")
            
        session = ChatSession(
            session_id=session_id,
            nino_id=nino_id,
            usuario_id=usuario_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.chat_sessions[session_id] = session
        return session

    def add_message_to_session(self, session_id: str, role: str, content: str) -> Optional[ChatMessage]:
        """Añade un mensaje a una sesión existente"""
        if session_id not in self.chat_sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.utcnow()
        )
        self.chat_sessions[session_id].messages.append(message)
        self.chat_sessions[session_id].updated_at = datetime.utcnow()
        return message

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Obtiene una sesión existente"""
        return self.chat_sessions.get(session_id)

    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Obtiene el historial de chat formateado para Gemini"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        history = []
        for msg in session.messages:
            history.append({
                "role": msg.role,
                "parts": [{"text": msg.content}]
            })
        return history

    def get_response(self, session_id: str, user_message: str) -> str:
        """Obtiene una respuesta de Gemini basada en el historial de chat"""
        if not self.is_configured:
            raise ValueError("Servicio Gemini no configurado")
            
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        try:
            # Obtener historial de chat
            history = self.get_chat_history(session_id)
            
            # Crear contexto con el sistema prompt
            context_message = {
                "role": "user",
                "parts": [{"text": self.system_prompt}]
            }
            system_response = {
                "role": "model",
                "parts": [{"text": "Entendido. Seré un asistente especializado en apoyo para niños con autismo."}]
            }
            
            # Combinar historial completo
            full_history = [context_message, system_response] + history
            
            # Iniciar chat con Gemini
            chat = self.model.start_chat(history=full_history)
            response = chat.send_message(user_message)
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error al obtener respuesta de Gemini: {str(e)}")

    def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión de chat"""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
            return True
        return False

    def list_sessions(self, usuario_id: int) -> List[ChatSession]:
        """Lista todas las sesiones de un usuario"""
        return [
            session for session in self.chat_sessions.values()
            if session.usuario_id == usuario_id
        ]

    def clear_all_sessions(self):
        """Limpia todas las sesiones (usar con cuidado)"""
        self.chat_sessions.clear()


# Inicializar el servicio de forma segura
gemini_chat_service = GeminiChatService()

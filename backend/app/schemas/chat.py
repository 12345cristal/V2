"""
Esquemas Pydantic para Chat
"""
from pydantic import BaseModel, Field
from typing import Optional

class ChatbotRequest(BaseModel):
    """Request para el chatbot"""
    mensaje: str = Field(..., min_length=1, max_length=2000, description="Pregunta del usuario")
    nino_id: Optional[int] = Field(None, description="ID del niño para contextualizar (opcional)")
    incluir_contexto: bool = Field(True, description="Incluir contexto del niño")
    session_id: Optional[str] = Field(None, description="ID de sesión existente (opcional)")

class ChatbotResponse(BaseModel):
    """Response del chatbot"""
    respuesta: str
    contexto_usado: bool
    configurado: bool
    session_id: str

class ChatSessionStartResponse(BaseModel):
    """Response al iniciar sesión"""
    session_id: str

class EstadoResponse(BaseModel):
    """Response del estado de IA"""
    configurado: bool
    model: Optional[str] = None

"""
Endpoints de Chat - Seguro, con persistencia y rate limiting
ACCESO PÚBLICO - No requiere autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import traceback

from app.db.session import get_db
from app.schemas.chat import (
    ChatbotRequest,
    ChatbotResponse,
    ChatSessionStartResponse,
    EstadoResponse
)
from app.services.chat_store import chat_store
from app.services.chat_service import ask_gemini
from app.services.safety import sanitize_user_text, looks_malicious
from app.services.gemini_service import gemini_chat_service
from app.core.rate_limit import chatbot_limiter
from app.models.nino import Nino

router = APIRouter()

# ============================================================
# ENDPOINT PÚBLICO: Iniciar sesión de chat
# ============================================================
@router.post("/chat/sesion", response_model=ChatSessionStartResponse)
def iniciar_sesion(request: Request, db: Session = Depends(get_db)):
    try:
        chatbot_limiter.check_rate_limit(request)

        sid = chat_store.new_session(db)
        return ChatSessionStartResponse(session_id=sid)

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno creando sesión de chat"}
        )


# ============================================================
# ENDPOINT PÚBLICO: Estado de Gemini
# ============================================================
@router.get("/estado", response_model=EstadoResponse)
def estado():
    try:
        return EstadoResponse(
            configurado=gemini_chat_service.configured,
            model=getattr(gemini_chat_service, "model_id", None)
        )
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Error verificando estado de Gemini"}
        )


# ============================================================
# ENDPOINT PÚBLICO: Chatbot principal
# ============================================================
@router.post("/chatbot", response_model=ChatbotResponse)
def chatbot(req: ChatbotRequest, request: Request, db: Session = Depends(get_db)):
    try:
        chatbot_limiter.check_rate_limit(request)

        # 1️⃣ Sanitizar mensaje
        mensaje = sanitize_user_text(req.mensaje)
        if not mensaje:
            raise HTTPException(status_code=400, detail="Mensaje vacío")

        # 2️⃣ Prompt injection
        if looks_malicious(mensaje):
            sid = req.session_id or chat_store.new_session(db)
            return ChatbotResponse(
                respuesta=(
                    "No puedo ayudar con solicitudes para evadir reglas o revelar "
                    "instrucciones internas. Puedo ayudarte con terapias y orientación."
                ),
                contexto_usado=False,
                configurado=gemini_chat_service.configured,
                session_id=sid
            )

        # 3️⃣ Sesión
        session_id = req.session_id or chat_store.new_session(db, nino_id=req.nino_id)
        chat_store.ensure_session(db, session_id, nino_id=req.nino_id)

        # 4️⃣ Contexto del niño (opcional)
        contexto = None
        contexto_usado = False
        if req.nino_id and req.incluir_contexto:
            nino = db.query(Nino).filter(Nino.id == req.nino_id).first()
            if nino:
                contexto = {
                    "nombre": f"{nino.nombre} {nino.apellido_paterno}",
                    "edad": getattr(nino, "edad", "No especificada"),
                    "diagnostico": (
                        nino.diagnostico.diagnostico_principal
                        if nino.diagnostico else "No especificado"
                    ),
                    "nivel_autismo": (
                        nino.diagnostico.nivel_autismo
                        if nino.diagnostico else "No especificado"
                    )
                }
                contexto_usado = True

        # 5️⃣ Historial
        historial = chat_store.history(db, session_id, limit=8) or []
        chat_store.append(db, session_id, "usuario", mensaje)

        # 6️⃣ Gemini (PROTEGIDO) con soporte para rol del usuario
        try:
            respuesta = ask_gemini(
                mensaje, 
                contexto, 
                historial,
                rol_usuario=req.rol_usuario  # Pasar el rol del usuario
            )
        except Exception:
            traceback.print_exc()
            respuesta = (
                "El asistente IA no está disponible en este momento. "
                "Puedes intentarlo más tarde."
            )

        # 7️⃣ Guardar respuesta
        chat_store.append(db, session_id, "asistente", respuesta)

        return ChatbotResponse(
            respuesta=respuesta,
            contexto_usado=contexto_usado,
            configurado=gemini_chat_service.configured,
            session_id=session_id
        )

    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del chatbot"}
        )

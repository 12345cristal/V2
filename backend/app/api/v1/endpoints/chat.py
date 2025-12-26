"""
Endpoints de Chat - Seguro, con rate-limit y persistencia
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat import ChatbotRequest, ChatbotResponse, ChatSessionStartResponse, EstadoResponse
from app.services.chat_store import chat_store
from app.services.chat_service import ask_gemini
from app.services.safety import sanitize_user_text, looks_malicious, medical_disclaimer
from app.services.gemini_client import gemini_client
from app.core.rate_limit import limiter
from app.models.nino import Nino

router = APIRouter()

@router.post("/chat/sesion", response_model=ChatSessionStartResponse)
@limiter.limit("30/minute")
def iniciar_sesion(request, db: Session = Depends(get_db)):
    """
    Inicia una nueva sesión de chat
    """
    try:
        print("[SESION] 🔵 Creando nueva sesión...")
        sid = chat_store.new_session(db)
        print(f"[SESION] ✅ Sesión creada: {sid}")
        return ChatSessionStartResponse(session_id=sid)
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[SESION] 🔥 ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Error creando sesión: {error_msg}")

@router.get("/estado", response_model=EstadoResponse)
def estado():
    """
    Verifica el estado de configuración de Gemini AI
    """
    try:
        print("[ESTADO] 🔵 Verificando estado...")
        estado = EstadoResponse(
            configurado=gemini_client.configured,
            model=getattr(gemini_client, "model_name", None)
        )
        print(f"[ESTADO] ✅ Configurado: {estado.configurado}")
        return estado
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[ESTADO] 🔥 ERROR: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Error verificando estado: {error_msg}")

@router.post("/chatbot", response_model=ChatbotResponse)
@limiter.limit("20/minute")
def chatbot(req: ChatbotRequest, request, db: Session = Depends(get_db)):
    """
    Endpoint principal del chatbot
    
    Flujo:
    1. Sanitizar y validar entrada
    2. Detectar prompt injection
    3. Inicializar o recuperar sesión
    4. Cargar contexto del niño (si aplica)
    5. Recuperar historial
    6. Consultar a Gemini
    7. Guardar en BD
    """
    try:
        print(f"[CHATBOT] 🔵 Iniciando consulta: {req.mensaje[:50]}...")
        
        # 1️⃣ SANITIZAR
        msg = sanitize_user_text(req.mensaje)
        print(f"[CHATBOT] ✅ Mensaje sanitizado: {msg[:50]}...")
        
        # 2️⃣ DETECTAR INYECCIÓN
        if looks_malicious(msg):
            print("[CHATBOT] ⚠️ Posible prompt injection detectado")
            return ChatbotResponse(
                respuesta="No puedo ayudar con solicitudes para revelar instrucciones internas o evadir reglas. "
                          "Puedo ayudarte con dudas sobre terapias, rutinas, actividades y estrategias de comunicación.",
                contexto_usado=False,
                configurado=gemini_client.configured,
                session_id=req.session_id or chat_store.new_session(db)
            )
        
        # 3️⃣ SESIÓN
        print(f"[CHATBOT] 🔵 Manejando sesión...")
        session_id = req.session_id or chat_store.new_session(db, nino_id=req.nino_id)
        chat_store.ensure_session(db, session_id, nino_id=req.nino_id)
        print(f"[CHATBOT] ✅ Session ID: {session_id}")
        
        # 4️⃣ CONTEXTO
        contexto = None
        contexto_usado = False
        if req.nino_id and req.incluir_contexto:
            try:
                nino = db.query(Nino).filter(Nino.id == req.nino_id).first()
                if nino:
                    contexto = {
                        "nombre": f"{nino.nombre} {nino.apellido_paterno}",
                        "edad": getattr(nino, "edad", "No especificada"),
                        "diagnostico": nino.diagnostico.diagnostico_principal if hasattr(nino, 'diagnostico') and nino.diagnostico else "No especificado",
                        "nivel_autismo": nino.diagnostico.nivel_autismo if hasattr(nino, 'diagnostico') and nino.diagnostico else "No especificado"
                    }
                    contexto_usado = True
                    print(f"[CHATBOT] ✅ Contexto cargado: {contexto['nombre']}")
            except Exception as ctx_err:
                print(f"[CHATBOT] ⚠️ Error cargando contexto: {ctx_err}")
                contexto = None
        
        # 5️⃣ HISTORIAL
        print(f"[CHATBOT] 🔵 Recuperando historial...")
        historial = chat_store.history(db, session_id, limit=8) or []
        chat_store.append(db, session_id, "usuario", msg)
        print(f"[CHATBOT] ✅ Historial: {len(historial)} mensajes")
        
        # 6️⃣ GEMINI
        print(f"[CHATBOT] 🔵 Consultando Gemini...")
        respuesta = ask_gemini(msg, contexto, historial)
        print(f"[CHATBOT] ✅ Respuesta generada: {respuesta[:100]}...")
        
        # 7️⃣ GUARDAR
        chat_store.append(db, session_id, "asistente", respuesta)
        print(f"[CHATBOT] ✅ Conversación guardada")
        
        resultado = ChatbotResponse(
            respuesta=respuesta,
            contexto_usado=contexto_usado,
            configurado=gemini_client.configured,
            session_id=session_id
        )
        print(f"[CHATBOT] ✅ Response construido correctamente")
        return resultado
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[CHATBOT] 🔥 ERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en chatbot: {error_msg}")

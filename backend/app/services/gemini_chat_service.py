# app/services/gemini_chat_service.py
from __future__ import annotations

import json
from typing import Optional, Dict, List

# Importaciones del SDK de Gemini con fallback si no está instalado
try:
    from google import genai  # paquete oficial: google-genai
    from google.genai import types
except Exception:
    genai = None
    types = None

from app.core.config import settings
from app.services.conversation_store import ConversationStore


SYSTEM_PROMPT = """
Eres un asistente virtual especializado en Trastorno del Espectro Autista (TEA).

Rol:
- Apoyar a padres, terapeutas y personal educativo.
- Responder de forma empática, clara y profesional.
- Brindar orientación basada en buenas prácticas clínicas.
- NO realizas diagnósticos médicos.
- NO sustituyes a un profesional de la salud.

Reglas CRÍTICAS (para Gemini 2.0):
- Responde SIEMPRE en español.
- Usa lenguaje respetuoso, sencillo y humano.
- Máximo 180 palabras por respuesta.
- Si la información es insuficiente, da recomendaciones generales.
- Si detectas crisis severa, recomienda acudir a profesional INMEDIATAMENTE.
- NO hagas afirmaciones categóricas sobre el niño sin evidencia.
- Valida emociones del adulto (es importante en TEA).
"""


class GeminiChatService:
    """
    Chatbot terapéutico TEA usando el SDK OFICIAL de Gemini.
    """

    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        self.store = ConversationStore()

        # Si el SDK no está disponible o no hay API key, usar fallback
        if genai is None or not api_key:
            self.client = None
            self.model_id = None
            self.configured = False
            if genai is None:
                print("[WARN] SDK google-genai no instalado. Usando fallback clínico.")
            else:
                print("[WARN] Gemini no configurado, usando fallback clínico.")
            return

        self.client = genai.Client(api_key=api_key)
        # Usar GEMINI_MODEL_ID si está configurado, si no usar GEMINI_MODEL
        self.model_id = (
            settings.GEMINI_MODEL_ID 
            or getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        )
        self.configured = True
        print(f"[OK] Gemini Chat (Gemini 2.5 Flash) listo con modelo {self.model_id}")

    def chat(
        self,
        mensaje: str,
        *,
        session_id: Optional[str] = None,
        contexto_nino: Optional[Dict] = None,
        rol_usuario: str = "padre",
    ) -> Dict:
        """
        Respuesta terapéutica segura optimizada para Gemini 2.0 Flash.
        
        Args:
            mensaje: Pregunta del usuario
            session_id: ID de sesión (se crea si no existe)
            contexto_nino: Dict con datos del niño para contexto
            rol_usuario: "padre", "terapeuta" o "educador" (personaliza respuesta)
            
        Returns:
            Dict con respuesta, session_id y estado de configuración
        """
        if not self.configured:
            return self._fallback(mensaje)

        session_id = session_id or self.store.new_session()
        history = self.store.history(session_id)

        # Instrucciones específicas por rol
        rol_instrucciones = self._get_rol_instructions(rol_usuario)

        contexto_txt = ""
        if contexto_nino:
            contexto_txt = (
                "\n\nPerfil del niño:\n"
                + json.dumps(contexto_nino, ensure_ascii=False, indent=2)
            )

        history_txt = ""
        if history:
            history_txt = "\n\nConversación previa (últimos 6 mensajes):\n"
            for h in history[-6:]:
                label = "Usuario" if h["role"] == "user" else "Asistente"
                history_txt += f"{label}: {h['text']}\n"

        prompt = f"""
{SYSTEM_PROMPT}

{rol_instrucciones}

Pregunta del usuario:
{mensaje}
{contexto_txt}
{history_txt}

Responde con orientación práctica y empática.
LÍMITE: Máximo 180 palabras.
"""

        try:
            resp = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)],
                    )
                ],
            )

            text = self._extract_text(resp)

            # Guardar en historial
            self.store.append(session_id, "user", mensaje)
            self.store.append(session_id, "assistant", text)

            return {
                "respuesta": text,
                "session_id": session_id,
                "configurado": True,
                "modelo": self.model_id,
            }

        except Exception as e:
            print(f"❌ Error Gemini Chat: {e}")
            return self._fallback(mensaje, session_id)

    # ---------- Helpers ----------

    @staticmethod
    def _get_rol_instructions(rol: str) -> str:
        """Instrucciones específicas por tipo de usuario."""
        instrucciones = {
            "padre": (
                "Contexto: El usuario es un PADRE o CUIDADOR.\n"
                "• Enfatiza estrategias prácticas para casa.\n"
                "• Valida sus emociones y preocupaciones.\n"
                "• Sugiere actividades simples y recursos.\n"
                "• Recomienda que consulte con un terapeuta si es complejo."
            ),
            "terapeuta": (
                "Contexto: El usuario es un TERAPEUTA o PSICÓLOGO.\n"
                "• Proporciona orientación clínica basada en evidencia.\n"
                "• Sugiere técnicas específicas (ABA, TEA, etc).\n"
                "• Ofrece referencias a literatura clínica.\n"
                "• Discute estrategias de intervención avanzadas."
            ),
            "educador": (
                "Contexto: El usuario es EDUCADOR o PERSONAL ESCOLAR.\n"
                "• Enfatiza adaptaciones en el aula.\n"
                "• Sugiere estrategias inclusivas.\n"
                "• Proporciona apoyos visuales y estructurados.\n"
                "• Coordina con terapeutas y familia."
            ),
        }
        return instrucciones.get(rol.lower(), instrucciones["padre"])

    @staticmethod
    def _extract_text(resp) -> str:
        """Extrae texto de la respuesta de Gemini."""
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()

        if hasattr(resp, "candidates"):
            parts = resp.candidates[0].content.parts
            return "".join(
                p.text for p in parts if getattr(p, "text", None)
            ).strip()

        return "No se pudo generar una respuesta."

    @staticmethod
    def _fallback(mensaje: str, session_id: Optional[str] = None) -> Dict:
        """Respuesta clínica segura cuando Gemini no está disponible."""
        return {
            "respuesta": (
                "Puedo darte orientación general basada en buenas prácticas:\n\n"
                "• Mantén rutinas predecibles.\n"
                "• Usa apoyos visuales y lenguaje claro.\n"
                "• Refuerza conductas positivas.\n"
                "• Divide tareas en pasos pequeños.\n"
                "• Ante rabietas: calma, validación y espacio seguro.\n\n"
                "Para recomendaciones más específicas, indica edad y objetivo terapéutico."
            ),
            "session_id": session_id,
            "configurado": False,
        }


# Singleton
gemini_chat_service = GeminiChatService()

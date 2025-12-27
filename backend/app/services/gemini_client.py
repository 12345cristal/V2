"""
Compatibilidad: Redirige a `gemini_chat_service` (cliente oficial google-genai).
Conservar importaciones antiguas sin romper el código.
"""
from app.services.gemini_service import gemini_chat_service

class GeminiClientCompat:
    def __init__(self):
        self.configured = gemini_chat_service.configured
        self.model_name = getattr(gemini_chat_service, "model_id", None)

    def generate(self, prompt: str) -> str:
        # Envía el prompt como mensaje directo
        return gemini_chat_service.chat(prompt)

# Instancia global compatible
gemini_client = GeminiClientCompat()

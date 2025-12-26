"""
Cliente de Gemini API
"""
from app.core.config import settings
import google.generativeai as genai

class GeminiClient:
    def __init__(self):
        self.configured = bool(settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL

        if self.configured:
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✅ Gemini AI configurado con {self.model_name}")
            except Exception as e:
                print(f"⚠️ Error configurando Gemini: {e}")
                self.model = None
                self.configured = False
        else:
            self.model = None

    def generate(self, prompt: str) -> str:
        """
        Genera respuesta usando Gemini
        """
        if not self.configured or not self.model:
            return ("El asistente IA no está configurado en este momento. "
                    "Por favor, configura GEMINI_API_KEY en el backend.")
        
        try:
            resp = self.model.generate_content(prompt)
            return (resp.text or "").strip()
        except Exception as e:
            print(f"❌ Error en Gemini: {e}")
            return ("Hubo un error procesando tu solicitud. Por favor intenta de nuevo.")

# Instancia global
gemini_client = GeminiClient()

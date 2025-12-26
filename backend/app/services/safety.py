"""
Seguridad y validación de entrada
"""
import re

DISALLOWED = [
    "dame tu api key", "muéstrame tu clave", "system prompt", "prompt del sistema",
    "ignora instrucciones", "override", "bypass", "jailbreak", "vulnerabilidad",
    "hack", "comando sql", "inyección", "exploit", "backdoor"
]

def sanitize_user_text(text: str) -> str:
    """
    Sanitiza texto del usuario:
    - Recorta excesos
    - Limpia caracteres raros
    - Limita a 2000 caracteres
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text[:2000]

def looks_malicious(text: str) -> bool:
    """
    Detecta intentos de prompt injection básicos
    """
    t = text.lower()
    return any(x in t for x in DISALLOWED)

def medical_disclaimer() -> str:
    """
    Disclaimer de responsabilidad médica
    """
    return ("⚠️ Nota: Soy un asistente informativo. No sustituyo a un profesional de salud. "
            "Si hay riesgo de autolesión o crisis, busca ayuda profesional inmediata o contacta a un especialista.")

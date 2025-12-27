#!/usr/bin/env python3
"""
Script de prueba para Gemini 2.0 Flash
Demuestra el funcionamiento con los 3 roles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.gemini_chat_service import gemini_chat_service
from app.core.config import settings

def test_gemini_chat():
    """Prueba el servicio de chat con los 3 roles"""
    
    print("=" * 70)
    print("🧠 PRUEBA GEMINI 2.0 FLASH - CHATBOT TERAPÉUTICO TEA")
    print("=" * 70)
    
    # Verificar configuración
    print(f"\n✅ API configurada: {gemini_chat_service.configured}")
    print(f"✅ Modelo: {gemini_chat_service.model_id}")
    print(f"✅ API Key presente: {bool(settings.GEMINI_API_KEY)}")
    
    if not gemini_chat_service.configured:
        print("\n⚠️ Gemini no está configurado. Usando fallback clínico.")
        return
    
    # Datos de prueba
    nino_contexto = {
        "nombre": "Juan",
        "edad": 6,
        "diagnosticos": ["TEA Moderado"],
        "dificultades": ["Comunicación", "Interacción social"],
        "fortalezas": ["Memoria visual", "Interés en colores"],
        "sensibilidades": ["Ruido fuerte", "Texturas ásperas"],
    }
    
    preguntas = [
        "¿Cómo puedo mejorar la comunicación con mi hijo?",
        "¿Qué técnicas ABA puedo usar para reducir estereotipias?",
        "¿Cómo adapto el aula para un niño con TEA?",
    ]
    
    roles = ["padre", "terapeuta", "educador"]
    
    for idx, (rol, pregunta) in enumerate(zip(roles, preguntas), 1):
        print(f"\n{'=' * 70}")
        print(f"TEST {idx}: ROL = {rol.upper()}")
        print(f"{'=' * 70}")
        print(f"❓ Pregunta: {pregunta}\n")
        
        try:
            resultado = gemini_chat_service.chat(
                pregunta,
                contexto_nino=nino_contexto,
                rol_usuario=rol
            )
            
            print(f"✅ Estado: {resultado['configurado']}")
            print(f"📧 Session ID: {resultado['session_id']}\n")
            print("📝 RESPUESTA:")
            print("-" * 70)
            print(resultado['respuesta'])
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'=' * 70}")
    print("✅ PRUEBA COMPLETADA")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    test_gemini_chat()

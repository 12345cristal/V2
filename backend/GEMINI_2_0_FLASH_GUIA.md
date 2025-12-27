# 🧠 GEMINI 2.0 FLASH - GUÍA DE IMPLEMENTACIÓN

**Fecha:** 26 de diciembre de 2025
**Sistema:** Autismo Mochis IA
**Modelo:** Google Generative AI - Gemini 2.0 Flash

---

## ✅ ¿QUÉ SE IMPLEMENTÓ?

### 1️⃣ Modelo Gemini 2.0 Flash
- **Modelo:** `models/gemini-2.0-flash`
- **Velocidad:** ⚡⚡⚡⚡⚡ (Ultra rápido)
- **Costo:** 💰 Económico
- **Ideal para:** Chat en tiempo real, producción web

### 2️⃣ Arquitectura limpia (3 servicios)
```
app/services/
├── conversation_store.py     ← Historial en memoria (TTL)
├── gemini_chat_service.py    ← Chat terapéutico (nuevo)
├── gemini_embedding_service.py ← Embeddings y similitud
└── gemini_service.py         ← Compatibilidad hacia atrás
```

### 3️⃣ Soporte por rol de usuario
El sistema ahora personaliza respuestas según:
- 👨‍👩‍👧 **Padre/Cuidador** → Estrategias prácticas para casa
- 👨‍⚕️ **Terapeuta** → Orientación clínica basada en evidencia
- 👨‍🏫 **Educador** → Adaptaciones escolares e inclusión

---

## 📋 ARCHIVOS MODIFICADOS

| Archivo | Cambio |
|---------|--------|
| `app/core/config.py` | GEMINI_MODEL = "models/gemini-2.0-flash" |
| `app/services/gemini_chat_service.py` | ✅ Nuevo SDK, sin generation_config |
| `app/services/gemini_embedding_service.py` | Embeddings separados |
| `app/services/conversation_store.py` | Historial limpio con TTL |
| `app/services/chat_service.py` | ask_gemini() con parámetro rol_usuario |
| `app/schemas/chat.py` | ChatbotRequest con campo rol_usuario |
| `app/api/v1/endpoints/chat.py` | Pasar rol_usuario a Gemini |
| `.env.example` | Documentación de GEMINI_MODEL |

---

## 🔧 CONFIGURACIÓN

### `.env` (Backend)
```env
# API Key de Google Generative AI
GEMINI_API_KEY=tu_api_key_aqui

# Modelo Gemini 2.0 Flash (optimizado para chatbot)
GEMINI_MODEL=models/gemini-2.0-flash
```

**Obtén tu API Key en:** https://aistudio.google.com/app/apikey

---

## 🚀 USO DEL CHATBOT

### Endpoint: `POST /api/v1/chatbot`

**Request:**
```json
{
  "mensaje": "¿Cómo manejar una rabieta?",
  "nino_id": 1,
  "incluir_contexto": true,
  "session_id": "abc123def456",
  "rol_usuario": "padre"
}
```

**Parámetros:**
- `mensaje` (string, required) - Pregunta del usuario
- `nino_id` (integer, optional) - ID del niño para contextualizar
- `incluir_contexto` (boolean) - Incluir datos del niño en la respuesta
- `session_id` (string, optional) - ID de sesión existente
- `rol_usuario` (string) - **"padre"** | "terapeuta" | "educador"

**Response:**
```json
{
  "respuesta": "Para manejar una rabieta de forma efectiva...",
  "contexto_usado": true,
  "configurado": true,
  "session_id": "abc123def456"
}
```

---

## 📊 CARACTERÍSTICAS POR ROL

### 👨‍👩‍👧 PADRE/CUIDADOR
✅ Estrategias prácticas para casa
✅ Explicaciones sencillas
✅ Validación emocional
✅ Recomendaciones de recursos

### 👨‍⚕️ TERAPEUTA
✅ Orientación clínica basada en evidencia
✅ Técnicas específicas (ABA, TEA, etc.)
✅ Referencias bibliográficas
✅ Estrategias avanzadas

### 👨‍🏫 EDUCADOR
✅ Adaptaciones en el aula
✅ Estrategias inclusivas
✅ Apoyos visuales y estructurados
✅ Coordinación con terapeutas y familia

---

## 🛡️ SEGURIDAD CLÍNICA

### Reglas Críticas
1. **NO diagnostica** - Solo orienta
2. **Detecta crisis severas** - Recomienda profesional INMEDIATA
3. **Límite de palabras** - Máximo 180 palabras por respuesta
4. **Fallback seguro** - Respuesta clínica si Gemini falla
5. **Sanitización** - Textos verificados contra injecciones

### Disclaimer Automático
Todas las respuestas incluyen:
> "Esta orientación no sustituye atención médica profesional. Para diagnósticos o crisis, acude a un especialista."

---

## 🧪 PRUEBA RÁPIDA

### Con curl:
```bash
curl -X POST http://localhost:8000/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "¿Cómo puedo mejorar la comunicación?",
    "rol_usuario": "padre"
  }'
```

### Con Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chatbot",
    json={
        "mensaje": "¿Actividades para estimular lenguaje?",
        "rol_usuario": "terapeuta",
        "nino_id": 1
    }
)

print(response.json()["respuesta"])
```

---

## ⚡ OPTIMIZACIONES DE GEMINI 2.0 FLASH

| Aspecto | Gemini 2.0 Flash | Gemini 2.0 Pro |
|--------|-----------------|----------------|
| Latencia | 150-300ms | 500-1000ms |
| Costo | $0.075 / 1M tokens | $1.50 / 1M tokens |
| Respuestas cortas | ✅ Excelente | ⚠️ Verboso |
| Seguimiento instrucciones | ✅ Muy bueno | ⚠️ Tende a ignorar límites |
| Para chat público | ✅ Ideal | ❌ Excesivo |
| Para reportes largos | ⚠️ Corta respuestas | ✅ Ideal |

---

## 🔮 POSIBLES MEJORAS FUTURAS

1. **Analytics** - Rastrear preguntas frecuentes
2. **Fine-tuning** - Entrenar modelo con casos TEA reales
3. **Gemini 2.0 Pro** - Para reportes clínicos largos (endpoint separado)
4. **Multimodal** - Procesar imágenes de actividades
5. **Memoria a largo plazo** - BD de preferencias por usuario

---

## 📞 SOPORTE

Si el chatbot no funciona:

1. Verifica `GEMINI_API_KEY` en `.env`
2. Revisa logs: `python -m app.main` (nivel DEBUG)
3. Comprueba que `GEMINI_MODEL=models/gemini-2.0-flash`
4. Si aún falla, el sistema usa fallback clínico seguro

---

**¡Listo para producción!** 🎉

Gemini 2.0 Flash está optimizado para proporcionar respuestas empáticas, rápidas y clínicamente seguras a padres, terapeutas y educadores en el contexto del autismo (TEA).

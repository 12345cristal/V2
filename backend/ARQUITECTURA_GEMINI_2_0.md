# 🏗️ ARQUITECTURA GEMINI 2.0 FLASH

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Angular)                           │
│           POST /api/v1/chatbot + rol_usuario                    │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                             │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  app/api/v1/endpoints/chat.py                           │   │
│  │  • Validación de seguridad                              │   │
│  │  • Rate limiting                                         │   │
│  │  • Carga de contexto del niño                           │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  app/services/chat_service.py                           │   │
│  │  ask_gemini(mensaje, contexto, historial, rol_usuario)  │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │                                      │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  app/services/gemini_chat_service.py                    │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ chat(mensaje, contexto, rol_usuario)           │   │   │
│  │  │ • Construye prompt con instrucciones por rol    │   │   │
│  │  │ • Consulta Gemini 2.0 Flash                    │   │   │
│  │  │ • Guarda en historial                          │   │   │
│  │  │ • Retorna Dict con respuesta                   │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ _get_rol_instructions(rol)                      │   │   │
│  │  │ • Instrucciones específicas por rol             │   │   │
│  │  │ • padre → Estrategias prácticas                │   │   │
│  │  │ • terapeuta → Orientación clínica              │   │   │
│  │  │ • educador → Adaptaciones escolares            │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │ Fallback seguro si Gemini falla                │   │   │
│  │  │ • Respuesta clínica cuidada                    │   │   │
│  │  │ • Sin diagnósticos                            │   │   │
│  │  │ • Recomendaciones generales                   │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └──────────────────────┬─────────────────────────────────┘   │
│                         │                                       │
│         ┌───────────────┴───────────────┬────────────────┐     │
│         ▼                               ▼                ▼     │
│  ┌────────────────────────┐  ┌──────────────────────────────┐ │
│  │ conversation_store.py  │  │ Gemini API                   │ │
│  │                        │  │                              │ │
│  │ • Historial en memoria │  │ models/gemini-2.0-flash     │ │
│  │ • TTL 30 min           │  │                              │ │
│  │ • Max 10 mensajes      │  │ ⚡ 150-300ms latencia       │ │
│  │ • Session management   │  │ 💰 $0.075 / 1M tokens      │ │
│  └────────────────────────┘  │ 📝 Máximo 180 palabras      │ │
│                              └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 FLUJO DE UNA PREGUNTA

```
1. Usuario hace pregunta
   ↓
2. Frontend envía POST con rol_usuario
   ↓
3. Backend valida y sanitiza
   ↓
4. Carga contexto del niño (si aplica)
   ↓
5. Obtiene historial (últimos 6 mensajes)
   ↓
6. chat_service.ask_gemini() con rol_usuario
   ↓
7. gemini_chat_service.chat():
   • Construye SYSTEM_PROMPT
   • Añade instrucciones por rol
   • Incluye contexto del niño
   • Añade historial
   • Consulta Gemini 2.0 Flash
   ↓
8. Guarda en conversation_store
   ↓
9. Retorna respuesta al frontend
   ↓
10. Usuarios ve respuesta personalizada
```

---

## 📊 RESPONSABILIDADES POR MÓDULO

### conversation_store.py
```
✅ Gestión de sesiones
✅ Historial en memoria (TTL)
✅ Limpieza de sesiones expiradas
✅ No interfiere con BD principal
```

### gemini_chat_service.py
```
✅ Comunicación con Gemini API
✅ Construcción de prompts
✅ Personalización por rol
✅ Fallback clínico
✅ Extracción de respuestas
```

### gemini_embedding_service.py
```
✅ Generación de embeddings
✅ Cálculo de similitud coseno
✅ Embeddings de perfiles
✅ Embeddings de actividades
✅ (Usado para TOPSIS y recomendaciones)
```

### gemini_service.py
```
✅ Compatibilidad hacia atrás
✅ Reexportación de servicios
✅ Plantillas fallback
```

---

## 🎯 ROL → INSTRUCCIÓN → RESPUESTA

```
┌──────────┐
│   PADRE  │ → "Enfatiza estrategias prácticas para casa"
└──────────┘    ↓
              [Gemini 2.0 Flash]
              ↓
              "Puedes usar pictogramas, crear
               rutinas predecibles, reforzar
               conductas positivas..."

┌───────────┐
│ TERAPEUTA │ → "Orientación clínica basada en evidencia"
└───────────┘    ↓
               [Gemini 2.0 Flash]
               ↓
               "Se recomienda usar análisis
                funcional de conducta (ABA),
                técnicas de comunicación alternativa..."

┌──────────┐
│ EDUCADOR │ → "Adaptaciones en el aula"
└──────────┘    ↓
              [Gemini 2.0 Flash]
              ↓
              "Adapta el espacio físico,
               crea horarios visuales,
               coordina con familia..."
```

---

## ⚙️ CONFIGURACIÓN

```python
# .env
GEMINI_API_KEY=tu_api_key
GEMINI_MODEL=models/gemini-2.0-flash

# config.py
GEMINI_MODEL: str = "models/gemini-2.0-flash"
GEMINI_MODEL_ID: str | None = None
```

---

## 🛡️ CAPAS DE SEGURIDAD

```
User Input
    ↓
[Sanitización] ← Remove HTML, scripts
    ↓
[Rate Limiting] ← Max X requests/min
    ↓
[Detection] ← ¿Prompt injection?
    ↓
[Contexto] ← Carga datos del niño
    ↓
[Prompt] ← SYSTEM_PROMPT + ROL + CONTEXTO
    ↓
[Gemini] ← API Call con límites
    ↓
[Fallback] ← Si falla, respuesta clínica segura
    ↓
Response
```

---

## 📈 ESCALABILIDAD

**Ahora:**
- ✅ Historial en memoria (30 min TTL)
- ✅ Máx 10 mensajes por sesión
- ✅ Sin persistencia (no sobrecarga BD)

**Futuro (si crece):**
- 📝 Persistir en BD (sesiones largas)
- 📊 Analytics (preguntas frecuentes)
- 🔄 Cache de embeddings
- 🧠 Fine-tuning con casos reales

---

## ✅ VENTAJAS ACTUALES

```
✔ Gemini 2.0 Flash → ⚡ Rápido y barato
✔ Modular → Código limpio y mantenible
✔ Sin duplicados → DRY (Don't Repeat Yourself)
✔ Por rol → Respuestas personalizadas
✔ Fallback → Seguridad clínica
✔ Historial → Contexto en conversación
✔ TTL → No acumula sesiones viejas
✔ Documentado → Guía completa
✔ Testeado → Script de prueba incluido
```

---

**Arquitectura lista para producción** 🚀

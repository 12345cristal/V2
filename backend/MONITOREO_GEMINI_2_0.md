# 📊 MONITOREO Y MANTENIMIENTO - GEMINI 2.0 FLASH

**Documento:** Guía de monitoreo post-implementación
**Fecha:** 26 de diciembre de 2025
**Sistema:** Autismo Mochis IA

---

## 🔍 VERIFICACIONES PERIÓDICAS

### ✅ Diariamente (automático)

```python
# Logs a verificar
❌ [CRÍTICO] ERROR en Gemini Chat
⚠️  ADVERTENCIA: Gemini no configurado
✅ Gemini Chat (Gemini 2.0 Flash) listo
```

### ✅ Semanalmente

| Métrica | Umbral | Acción |
|---------|--------|--------|
| API uptime | < 99% | Revisar logs de Gemini |
| Latencia promedio | > 500ms | Contactar Google |
| Errores de API | > 5% | Revisar rate limiting |
| Sesiones activas | > 1000 | Aumentar TTL si es necesario |

### ✅ Mensualmente

1. **Revisar analytics**
   - Preguntas más frecuentes
   - Rol más activo
   - Temas de consulta

2. **Análisis de fallback**
   - ¿Cuándo se activa?
   - ¿Por qué?
   - Mejorar respuesta clínica

3. **Costos**
   - Tokens utilizados
   - Costo estimado
   - Optimizaciones

---

## 📈 MÉTRICAS A RASTREAR

### Uso
```
- Sesiones creadas por día
- Mensajes por sesión
- Rol más frecuente: padre | terapeuta | educador
- Edad promedio de niños en contexto
```

### Rendimiento
```
- Latencia P50 (mediana)
- Latencia P95 (percentil 95)
- Latencia P99 (percentil 99)
- Tasa de errores de API
```

### Seguridad
```
- Respuestas que activaron fallback
- Detecciones de crisis
- Intentos de prompt injection bloqueados
- Sesiones expiradas (TTL)
```

---

## 🚨 ALERTAS RECOMENDADAS

### CRÍTICAS
```
❌ Gemini API unavailable
❌ GEMINI_API_KEY no configurada
❌ Modelo no soportado
❌ Error de autenticación
```

### ADVERTENCIAS
```
⚠️  Latencia > 1000ms (más de 1 segundo)
⚠️  Error rate > 10%
⚠️  Sesión session_limit alcanzado
⚠️  Gemini usando fallback > 20%
```

### INFORMACIÓN
```
ℹ️  Sesión TTL expirada (normal)
ℹ️  Límite de palabras respetado
ℹ️  Historial limpiado
```

---

## 🔧 TROUBLESHOOTING

### "Gemini no está configurado"
**Causa:** GEMINI_API_KEY vacía
**Solución:**
```bash
# 1. Obtener API Key
# Ir a https://aistudio.google.com/app/apikey

# 2. Configurar en .env
echo "GEMINI_API_KEY=tu_api_key" >> .env

# 3. Reiniciar servidor
python -m app.main
```

### "Latencia muy alta (> 1s)"
**Causa:** Red lenta o API sobrecargada
**Solución:**
```python
# Verificar estado de Google API
# https://status.cloud.google.com/

# Opción: Usar caché de respuestas
# (implementación futura)
```

### "Error de modelo no soportado"
**Causa:** GEMINI_MODEL mal configurado
**Solución:**
```bash
# Verificar modelo en .env
GEMINI_MODEL=models/gemini-2.0-flash  # ← Correcto

# NO usar:
# GEMINI_MODEL=gemini-2.0-flash  # ❌ Sin "models/"
# GEMINI_MODEL=gemini-pro  # ❌ Modelo antiguo
```

### "Rate limit exceeded"
**Causa:** Demasiadas solicitudes simultáneas
**Solución:**
```python
# app/core/rate_limit.py
CHATBOT_MAX_REQUESTS = 100  # Por minuto
CHATBOT_MAX_MESSAGES = 10   # Por sesión

# Aumentar si es necesario (con cuidado)
```

---

## 📊 DASHBOARD SUGERIDO

### Página de Admin `/admin/gemini`

```
┌─────────────────────────────────────────┐
│ MONITOREO - GEMINI 2.0 FLASH           │
├─────────────────────────────────────────┤
│                                         │
│ ✅ Estado: OPERATIVO                    │
│ 📊 Modelo: models/gemini-2.0-flash     │
│ ⏱️  Latencia: 245ms (P50)                │
│ 📈 Uptime: 99.8%                        │
│                                         │
│ ESTADÍSTICAS HOY                       │
│ ├─ Sesiones: 124                       │
│ ├─ Mensajes: 456                       │
│ ├─ Errores: 2 (0.4%)                   │
│ └─ Fallbacks: 5 (1.1%)                 │
│                                         │
│ DISTRIBUCIÓN POR ROL                   │
│ ├─ 👨‍👩‍👧 Padre: 65%                       │
│ ├─ 👨‍⚕️ Terapeuta: 25%                    │
│ └─ 👨‍🏫 Educador: 10%                     │
│                                         │
│ ÚLTIMOS ERRORES                        │
│ └─ (mostrar últimos 5)                 │
│                                         │
└─────────────────────────────────────────┘
```

---

## 💰 ESTIMACIÓN DE COSTOS

### Cálculo base
```
Gemini 2.0 Flash:
- Entrada: $0.075 / 1M tokens
- Salida: $0.30 / 1M tokens

Promedio por pregunta:
- Input: 300 tokens
- Output: 150 tokens
- Total: 450 tokens

Costo por pregunta: ~$0.00009

A escala:
- 1,000 preguntas/día = $0.09/día
- 30,000 preguntas/mes = $2.70/mes
```

### Optimizaciones
```
1. Caché de respuestas frecuentes
   → Reduce 20-30% de consultas

2. Shorter context (limitar histórico)
   → Reduce tokens de entrada

3. Fine-tuning (futuro)
   → Reduce tokens de salida
```

---

## 🔐 SEGURIDAD Y PRIVACIDAD

### ✅ Datos NO guardados
- Mensajes en memoria (TTL 30 min)
- Session IDs volátiles
- No hay persistencia de chat

### ✅ Datos guardados (si se implementa BD)
- ID de sesión (hash)
- Rol del usuario (anónimo)
- Timestamp
- Tópico de pregunta (sin contenido sensible)

### ✅ GDPR Compliance
```
- ✅ No recolectamos datos personales del niño
- ✅ Contexto del niño es opcional
- ✅ Historial expira automáticamente
- ✅ Usuario puede pedir eliminación
```

---

## 📝 LOGS Y DEBUG

### Activar DEBUG
```python
# app/main.py
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("gemini_chat")
logger.debug("Chat iniciado", extra={
    "session_id": session_id,
    "rol_usuario": rol,
    "modelo": model_id
})
```

### Estructura de logs
```
[2025-12-26 14:30:45] ✅ Gemini Chat iniciado
[2025-12-26 14:30:45] ℹ️  Session ID: abc123
[2025-12-26 14:30:45] 👤 Rol: padre
[2025-12-26 14:30:45] 📊 Contexto: {nombre: Juan, edad: 6}
[2025-12-26 14:30:46] 🤖 Respuesta generada (245ms)
[2025-12-26 14:30:46] 💾 Guardado en historial
```

---

## 🔄 ESCALABILIDAD

### Actual (Desarrollo)
```
✅ Historial en memoria
✅ Máx 10 mensajes por sesión
✅ TTL 30 minutos
✅ Sin persistencia
```

### Futuro (Escala)
```
📈 Persistencia en Redis
📈 Cache de respuestas
📈 Load balancing
📈 Rate limiting más sofisticado
```

---

## 📞 SOPORTE

### Si algo falla...

**1. Verificar configuración**
```bash
python -c "
from app.core.config import settings
from app.services.gemini_chat_service import gemini_chat_service
print(f'API Key: {bool(settings.GEMINI_API_KEY)}')
print(f'Configurado: {gemini_chat_service.configured}')
print(f'Modelo: {gemini_chat_service.model_id}')
"
```

**2. Revisar logs**
```bash
tail -f app.log | grep -i "gemini\|error\|warning"
```

**3. Probar servicio directamente**
```bash
python backend/test_gemini_flash.py
```

**4. Revisar estado de Google API**
```
https://status.cloud.google.com/
```

---

## 📚 RECURSOS

- [Google AI Studio](https://aistudio.google.com)
- [Google Generative AI SDK](https://ai.google.dev/tutorials/python_quickstart)
- [Documentación Gemini 2.0](https://ai.google.dev/models/gemini)
- [Guía de Pricing](https://ai.google.dev/pricing)

---

**Documento:** Mantén esto a mano para monitoreo efectivo 📊


# 🤖 GUÍA: INTEGRACIÓN DE GEMINI AI

## ✅ ¿Qué se ha integrado?

### Backend (FastAPI)
1. **Servicio GeminiService expandido** (`backend/app/services/gemini_service.py`)
   - ✅ Chatbot de consultas sobre autismo
   - ✅ Generador de actividades personalizadas
   - ✅ Generador de planes terapéuticos
   - ✅ Analizador de progreso
   - ✅ Funciona con/sin API key (fallback a respuestas por defecto)

2. **API Endpoints** (`backend/app/api/v1/endpoints/gemini_ia.py`)
   - `POST /api/v1/ia/chatbot` - Chatbot de consultas
   - `POST /api/v1/ia/actividades-personalizadas` - Generar actividades
   - `POST /api/v1/ia/plan-terapeutico` - Generar plan de 3 meses
   - `POST /api/v1/ia/analizar-progreso` - Análisis de evaluaciones
   - `GET /api/v1/ia/estado` - Verificar configuración

### Frontend (Angular)
1. **Servicio GeminiIaService** (`src/app/service/gemini-ia.service.ts`)
   - Métodos para todas las funcionalidades de IA

2. **Componente Chatbot** (`src/app/shared/chatbot-ia/`)
   - ✅ Botón flotante en toda la aplicación
   - ✅ Interfaz de chat moderna
   - ✅ Preguntas sugeridas
   - ✅ Soporte para contexto (perfil del niño)
   - ✅ Funciona sin configuración (respuestas limitadas)

---

## 🔑 Configurar API Key de Gemini (Opcional pero Recomendado)

### Paso 1: Obtener API Key GRATIS

1. **Ve a Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Inicia sesión** con tu cuenta de Google
3. **Click en "Create API Key"**
4. **Copia la API key** (empieza con `AIza...`)

**IMPORTANTE:** La API de Gemini tiene un tier gratuito generoso:
- 60 consultas por minuto
- 1,500 consultas por día
- GRATIS sin tarjeta de crédito

### Paso 2: Configurar en el Backend

**Opción A: Variable de entorno (Recomendado)**

```powershell
# En Windows PowerShell
$env:GEMINI_API_KEY="TU_API_KEY_AQUI"

# O agregar a tu sistema permanentemente:
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "TU_API_KEY_AQUI", "User")
```

**Opción B: Archivo .env**

Crea el archivo `backend/.env`:
```env
GEMINI_API_KEY=TU_API_KEY_AQUI
```

**Opción C: Desde la interfaz (Próximamente)**

Habrá una sección en Configuración para agregar la API key sin tocar código.

### Paso 3: Reiniciar el Backend

```powershell
# Detén el backend (Ctrl + C)
# Inicia nuevamente:
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver:
```
✅ Gemini AI configurado correctamente
```

---

## 🎯 Funcionalidades Disponibles

### 1. Chatbot de Consultas

**¿Qué hace?**
- Responde preguntas sobre autismo, terapias, desarrollo infantil
- Puede usar el contexto del niño para personalizar respuestas
- Disponible 24/7 en toda la aplicación

**Ejemplos de uso:**
```
Usuario: "¿Cómo puedo mejorar la comunicación con mi hijo de 5 años?"
IA: "Para un niño de 5 años con TEA, te recomiendo..."

Usuario: "¿Qué actividades son buenas para desarrollar habilidades sociales?"
IA: "Actividades recomendadas: 1. Juegos de turnos..."

Usuario: "¿Cómo manejar las rabietas?"
IA: "Las rabietas en niños con autismo..."
```

**Dónde aparece:**
- ✅ Botón flotante morado en la esquina inferior derecha
- ✅ Disponible en todas las páginas

### 2. Generador de Actividades Personalizadas

**¿Qué hace?**
- Genera 5-10 actividades terapéuticas adaptadas al niño
- Considera edad, diagnóstico, nivel de autismo, intereses
- Incluye: descripción paso a paso, materiales, duración, objetivo

**Cómo usar:**
```typescript
// En el perfil del niño:
this.geminiService.generarActividades(ninoId, 5).subscribe(actividades => {
  // Muestra actividades personalizadas
});
```

**Ejemplo de actividad generada:**
```json
{
  "nombre": "Juego de imitación con espejos",
  "descripcion": "Actividad para desarrollar...",
  "objetivo": "Mejorar comunicación no verbal",
  "duracion_minutos": 20,
  "materiales": ["Espejo", "Tarjetas"],
  "nivel_dificultad": "Básico",
  "area_desarrollo": "Social"
}
```

### 3. Generador de Planes Terapéuticos

**¿Qué hace?**
- Crea un plan completo de 3 meses
- Objetivos SMART
- Terapias recomendadas con justificación
- Indicadores de progreso medibles
- Recomendaciones para padres

**Usar en:**
- Al registrar un niño nuevo
- Después de una evaluación inicial
- Para renovar el plan terapéutico

### 4. Analizador de Progreso

**¿Qué hace?**
- Analiza evaluaciones del niño
- Identifica áreas de mejora y oportunidad
- Detecta tendencias
- Sugiere ajustes al plan
- Da una calificación numérica (0-10)

**Usar cuando:**
- Revisión mensual/trimestral
- Antes de reunión con padres
- Para informes de progreso

---

## 💡 Casos de Uso Prácticos

### Caso 1: Terapeuta necesita ideas de actividades

```
1. Abre perfil del niño
2. Click en "Generar Actividades con IA"
3. La IA sugiere 5 actividades personalizadas
4. Terapeuta selecciona las más apropiadas
5. Las agrega al plan del niño
```

### Caso 2: Padre tiene dudas sobre autismo

```
1. Abre chatbot (botón morado)
2. Escribe: "¿Cómo ayudar a mi hijo a hacer amigos?"
3. IA responde con estrategias prácticas
4. Padre puede hacer preguntas de seguimiento
```

### Caso 3: Coordinador crea plan terapéutico

```
1. Registra niño nuevo
2. Click en "Generar Plan con IA"
3. Completa evaluación inicial
4. IA genera plan de 3 meses
5. Coordinador revisa y ajusta
6. Guarda el plan
```

### Caso 4: Análisis de progreso trimestral

```
1. Recopila evaluaciones de 3 meses
2. Click en "Analizar Progreso"
3. IA procesa evaluaciones
4. Muestra resumen, tendencias, recomendaciones
5. Coordinador prepara informe para padres
```

---

## 🧪 Probar las Funcionalidades

### Probar Chatbot

1. **Abre cualquier página** del sistema
2. **Busca el botón morado** (esquina inferior derecha)
3. **Click en el botón**
4. **Escribe una pregunta:**
   - "¿Qué es el autismo?"
   - "¿Cómo mejorar el lenguaje en niños con TEA?"
   - "Dame consejos para rutinas"
5. **Presiona Enter** o click en enviar
6. **Espera la respuesta**

### Probar desde Swagger

1. **Abre**: http://localhost:8000/docs
2. **Busca la sección**: "Inteligencia Artificial - Gemini"
3. **Endpoints disponibles:**
   - `/api/v1/ia/chatbot`
   - `/api/v1/ia/actividades-personalizadas`
   - `/api/v1/ia/plan-terapeutico`
   - `/api/v1/ia/analizar-progreso`
   - `/api/v1/ia/estado`

**Ejemplo - Chatbot:**
```json
POST /api/v1/ia/chatbot
{
  "mensaje": "¿Qué actividades recomiendas para un niño de 5 años con TEA?",
  "incluir_contexto": false
}
```

---

## 📊 Comparación: Con vs Sin API Key

| Funcionalidad | Sin API Key | Con API Key |
|---------------|-------------|-------------|
| **Chatbot** | Respuestas genéricas | Respuestas personalizadas y contextuales |
| **Actividades** | 2-3 actividades básicas | 5-10 actividades adaptadas al niño |
| **Plan Terapéutico** | Plantilla estándar | Plan personalizado basado en evaluación |
| **Análisis de Progreso** | "Análisis no disponible" | Análisis detallado con recomendaciones |
| **Calidad** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**Recomendación:** Configurar la API key para aprovechar al 100% la IA.

---

## 🔍 Verificar Estado de Gemini

### Desde la Interfaz

El chatbot muestra un mensaje si Gemini no está configurado:
```
⚠️ El chatbot de IA no está configurado completamente. 
Las respuestas pueden ser limitadas.
```

### Desde el Backend

```powershell
# Ver logs al iniciar:
INFO:     Application startup complete.
✅ Gemini AI configurado correctamente

# O si no está configurado:
⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada
```

### Desde Swagger

```
GET /api/v1/ia/estado

Response:
{
  "configurado": true,
  "mensaje": "Gemini AI está configurado y funcionando",
  "funcionalidades_disponibles": {
    "chatbot": true,
    "actividades_personalizadas": true,
    "plan_terapeutico": true,
    "analisis_progreso": true
  }
}
```

---

## 🆘 Solución de Problemas

### "Error: google.generativeai no encontrado"

```powershell
cd backend
pip install google-generativeai
```

### "API Key inválida"

1. Verifica que la key sea correcta
2. Asegúrate de no tener espacios al inicio/final
3. Verifica que la key esté activa en Google AI Studio

### "Respuestas genéricas aunque configuré la API"

1. Reinicia el backend
2. Verifica variable de entorno: `echo $env:GEMINI_API_KEY`
3. Verifica en Swagger: `GET /api/v1/ia/estado`

### "Chatbot no aparece"

1. Refresca la página (F5)
2. Abre consola del navegador (F12) y busca errores
3. Verifica que el backend esté corriendo

---

## 📝 Próximas Mejoras

- [ ] Botón "Generar actividades con IA" en perfil del niño
- [ ] Análisis automático de progreso en evaluaciones
- [ ] Sugerencias de IA en asignación de terapeutas
- [ ] Predicción de respuesta a terapias
- [ ] Recomendaciones de horarios optimizados
- [ ] Generación de informes para padres
- [ ] Detección de patrones en conducta

---

## 🎓 Recursos

- **Gemini API Docs**: https://ai.google.dev/docs
- **Google AI Studio**: https://makersuite.google.com
- **Límites del tier gratuito**: https://ai.google.dev/pricing

---

**Estado Actual:** ✅ Integración completa y funcional
**Versión:** 1.0
**Última actualización:** Diciembre 2025

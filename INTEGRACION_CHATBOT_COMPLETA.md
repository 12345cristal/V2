# 🤖 Integración Completa del Chatbot IA (Gemini)

## Estado Actual ✅

El chatbot **Gemini 1.5 Flash** está completamente integrado en tu aplicación Autismo Mochis con dos modos de funcionamiento:

### 1. **Chatbot Público** (sin autenticación)
Visible en TODAS las páginas públicas para que cualquier visitante pueda hacer preguntas sobre:
- Comunicación con niños autistas
- Actividades recomendadas para TEA
- Manejo de rabietas y emociones
- Rutinas y estructura
- Información sobre terapias
- **Sugerencia automática**: Si preguntan sobre costos/terapias, el chatbot sugiere acceder al sistema para agendar

**Páginas públicas activas:**
- ✅ Página de Inicio (`landing`)
- ✅ Servicios (`servicios`)
- ✅ Tienda (`ventas`)
- ✅ Contacto (`contacto`)
- ✅ Donaciones (`donar`)
- ✅ Equipo (`equipo`)

### 2. **Chatbot Privado** (dentro de perfiles de usuario)
Disponible para usuarios autenticados (Padres, Terapeutas, Coordinadores) con contexto personalizado:
- Recibe `nino_id` como parámetro
- Las respuestas incluyen contexto específico del niño
- Puede proporcionar recomendaciones adaptadas al perfil

---

## 🏗️ Arquitectura Técnica

### Backend (FastAPI)
**Ubicación:** `backend/app/api/v1/endpoints/chat.py`

```
FastAPI (Puerto 8000)
    ↓
/api/v1/ia/ (Router)
    ├── GET  /estado             → Retorna estado de Gemini
    ├── POST /chat/sesion        → Crea sesión de chat (sin autenticación)
    └── POST /chatbot            → Procesa mensajes y genera respuestas
```

**Características de seguridad:**
- Rate limiting: 20 requests/minuto por IP
- Sanitización de entrada
- Detección de inyección de prompts
- Sin exposición de API keys de Gemini
- Respuestas con disclaimer médico cuando corresponde

### Base de Datos (MySQL)
**Tablas automáticas:**
- `chat_sessions`: Almacena sesiones (CHAR(32) session_id, nino_id opcional, timestamps)
- `chat_messages`: Historial de mensajes con roles (usuario/asistente)

**Se crean automáticamente** al iniciar el servidor (ver `backend/app/main.py`)

### Frontend (Angular)
**Ubicación:** `src/app/shared/chatbot-ia/`

**Componente reutilizable:**
```typescript
<app-chatbot-ia 
  [ninoId]="userId"                    // Opcional: ID del niño
  [incluirContexto]="true">            // Opcional: incluir contexto
</app-chatbot-ia>
```

**Servicio HTTP:**
- `src/app/service/gemini-ia.service.ts`
- Base URL: `http://localhost:8000/api/v1/ia`
- Métodos: `verificarEstado()`, `iniciarSesion()`, `chatbot()`
- Manejo de errores con `catchError` pipe

---

## 🚀 Cómo Usar

### Para Visitantes (Página Pública)
1. Ve a cualquier página pública (inicio, servicios, etc.)
2. Haz clic en el botón flotante del chatbot en la esquina inferior derecha
3. Escribe tu pregunta, ejemplo:
   - "¿Cómo comunicarme mejor con mi hijo autista?"
   - "¿Qué actividades recomiendan para niños con TEA?"
   - "¿Cuáles son los costos de las terapias?"

### Para Usuarios Autenticados (Perfil Privado)
1. Inicia sesión en el sistema
2. Ve a tu perfil o lista de niños
3. El chatbot aparecerá con contexto personalizado
4. Tus preguntas pueden incluir referencias al niño específico

### Para Desarrolladores

#### Iniciar Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

#### Iniciar Frontend
```bash
npm start
# o
ng serve --port 4200
```

#### Verificar Endpoints
```bash
# Comprobar estado
curl http://localhost:8000/api/v1/ia/estado

# Crear sesión
curl -X POST http://localhost:8000/api/v1/ia/chat/sesion

# Enviar mensaje
curl -X POST http://localhost:8000/api/v1/ia/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "tu_session_id_aqui",
    "mensaje": "¿Cómo manejar rabietas?",
    "nino_id": null
  }'
```

---

## 📝 Preguntas Sugeridas (Pre-cargadas)

El componente muestra 5 preguntas sugeridas para ayudar a visitantes:

1. "¿Cómo comunicarme mejor con mi hijo autista?"
2. "¿Qué actividades son recomendadas para niños con TEA?"
3. "¿Cómo manejar las rabietas y cambios de humor?"
4. "¿Cómo establecer rutinas efectivas?"
5. "¿Cuáles son los beneficios de la terapia?"

Los usuarios pueden hacer clic en cualquier sugerencia o escribir su propia pregunta.

---

## 🔄 Sistema de Prompts

### Gemini System Prompt
El sistema está configurado con instrucciones específicas:

```
Eres un asistente experto en Trastorno del Espectro Autista (TEA) 
y desarrollo infantil. Debes ser:
- Empático y comprensivo
- Informativo pero no prescriptivo (no reemplaces a profesionales)
- Incluir advertencia: "Este es un chatbot IA, no reemplaza 
  atención profesional"
```

### Variables Dinámicas
- `nino_id`: Si es null → respuestas generales
- `nino_id`: Si existe → incluye contexto personalizado

---

## 📊 Base de Datos

### Tabla: chat_sessions
```sql
CREATE TABLE chat_sessions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id CHAR(32) UNIQUE NOT NULL,
  nino_id INT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE
);
```

### Tabla: chat_messages
```sql
CREATE TABLE chat_messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  session_id CHAR(32) NOT NULL,
  role ENUM('usuario','asistente') NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
);
```

---

## 🛡️ Características de Seguridad

✅ **Rate Limiting:** 20 requests/minuto por IP (previene abuso)
✅ **Sanitización:** Limpia caracteres peligrosos de entrada
✅ **Inyección de Prompts:** Detección de intentos de manipulación
✅ **Sin API Keys Expuestas:** Las claves de Gemini solo en backend
✅ **CORS Configurado:** Comunic. segura entre frontend y backend
✅ **Respuestas Estructuradas:** JSON response con manejo de errores

---

## 🔍 Depuración

### Backend
**Logs en consola:**
```
✅ Tablas de chat verificadas/creadas
✅ [IA] Chat iniciado - Session: 0b011bf6...
✅ [IA] Mensaje procesado y guardado
```

### Frontend
**Abrir consola del navegador (F12):**
```javascript
// Ver errores HTTP
// Ver respuestas del chatbot
// Verificar sesión_id creado
```

---

## 📱 Componentes Integrados

| Página | Ruta | Estado |
|--------|------|--------|
| Landing | `/` | ✅ Activo |
| Servicios | `/servicios` | ✅ Activo |
| Ventas | `/ventas` | ✅ Activo |
| Contacto | `/contacto` | ✅ Activo |
| Donar | `/donar` | ✅ Activo |
| Equipo | `/equipo` | ✅ Activo |

---

## 🎯 Casos de Uso Cubiertos

### Visitantes Públicos
✅ Información general sobre TEA
✅ Estrategias de comunicación
✅ Actividades recomendadas
✅ Manejo de conductas desafiantes
✅ Consultas sobre servicios/costos → Sugerencia de contacto

### Usuarios Autenticados
✅ Recomendaciones personalizadas por niño
✅ Seguimiento de progreso
✅ Estrategias adaptadas al perfil específico
✅ Preguntas sobre terapias agendadas

---

## 🚨 Errores Comunes

| Error | Solución |
|-------|----------|
| "No se puede conectar a API" | Verifica que backend esté en `localhost:8000` |
| "Session not found" | Crea una nueva sesión con POST /chat/sesion |
| "Rate limit exceeded" | Espera 1 minuto antes de enviar más mensajes |
| "MySQL table not found" | Reinicia el backend para crear tablas automáticamente |

---

## 📞 Soporte

- **Servicio:** `src/app/service/gemini-ia.service.ts`
- **Componente:** `src/app/shared/chatbot-ia/chatbot-ia.component.ts`
- **Backend:** `backend/app/api/v1/endpoints/chat.py`
- **Documentación API:** Ver `backend/TESTING_API.md`

---

## ✨ Próximas Mejoras Sugeridas

1. **Analytics:** Registrar preguntas frecuentes
2. **Multi-idioma:** Traducir respuestas a otros idiomas
3. **Offline Mode:** Respuestas pre-cached cuando no hay conexión
4. **Mejores preguntas sugeridas:** Dinámicas según la página
5. **Integración con calendario:** Sugerir citas directamente

---

**Última actualización:** 2024-12-26
**Estado:** ✅ Producción-lista

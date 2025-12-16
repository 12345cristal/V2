# 📅 MÓDULO DE GESTIÓN DE TERAPIAS CON GOOGLE CALENDAR

## 🎯 Descripción General

Sistema completo de gestión de citas terapéuticas con sincronización automática a Google Calendar, exclusivo para el rol **COORDINADOR**.

---

## 🏗️ Arquitectura Implementada

### 1. Base de Datos (MySQL)
**Tabla extendida:** `citas`

```sql
-- Nuevos campos agregados:
- google_event_id VARCHAR(255)        # ID único del evento en Google Calendar
- google_calendar_link VARCHAR(500)   # URL directa al evento
- sincronizado_calendar BOOLEAN       # Estado de sincronización
- fecha_sincronizacion DATETIME       # Última sync
- confirmada BOOLEAN                  # Confirmación por padre/tutor
- fecha_confirmacion DATETIME
- cancelado_por INT                   # Usuario que canceló
- fecha_cancelacion DATETIME
- motivo_cancelacion TEXT
- creado_por INT                      # Auditoría
- actualizado_por INT
```

**Índices creados para optimización:**
- `idx_citas_google_event` en `google_event_id`
- `idx_citas_sincronizado` en `sincronizado_calendar`
- `idx_citas_confirmada` en `confirmada`

### 2. Modelos (SQLAlchemy)

**Archivo:** `backend/app/models/cita.py`

```python
class Cita(Base):
    """Modelo extendido con Google Calendar"""
    __tablename__ = "citas"
    
    # Campos originales + nuevos campos de sincronización
    google_event_id = Column(String(255), unique=True)
    sincronizado_calendar = Column(Boolean, default=False)
    # ... etc
```

### 3. Schemas (Pydantic v2)

**Archivo:** `backend/app/schemas/cita.py`

```python
class CitaCreate(CitaBase):
    sincronizar_google_calendar: bool = True
    
class CitaReprogramar(BaseModel):
    nueva_fecha: date
    nueva_hora_inicio: time
    nueva_hora_fin: time
    actualizar_google_calendar: bool = True
    
class CitaCancelar(BaseModel):
    motivo_cancelacion: str
    eliminar_de_google_calendar: bool = True
```

### 4. Servicio Google Calendar

**Archivo:** `backend/app/services/google_calendar_service.py`

**Características:**
- ✅ Autenticación con **Service Account**
- ✅ Manejo robusto de errores
- ✅ Logging detallado
- ✅ Funciona sin credenciales (modo degradado)
- ✅ Métodos: `crear_evento()`, `actualizar_evento()`, `eliminar_evento()`

```python
from app.services.google_calendar_service import google_calendar_service

# Crear evento
resultado = google_calendar_service.crear_evento(
    titulo="Terapia de Lenguaje - Juan Pérez",
    descripcion="Sesión regular de terapia",
    fecha=date(2025, 12, 20),
    hora_inicio=time(10, 0),
    hora_fin=time(11, 0),
    ubicacion="Centro de Terapias"
)
# Retorna: {'google_event_id': '...', 'google_calendar_link': '...'}
```

### 5. Endpoints REST

**Archivo:** `backend/app/api/v1/endpoints/citas_calendario.py`

**Rutas implementadas:**

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/citas-calendario/` | Crear cita + sincronizar Google Calendar |
| PUT | `/api/v1/citas-calendario/{id}/reprogramar` | Reprogramar cita existente |
| PUT | `/api/v1/citas-calendario/{id}/cancelar` | Cancelar cita |
| GET | `/api/v1/citas-calendario/calendario` | Obtener calendario con filtros |
| GET | `/api/v1/citas-calendario/{id}` | Detalles de una cita |

**Todos los endpoints requieren:**
- 🔐 Autenticación JWT
- 👔 Rol COORDINADOR (o ADMIN)

---

## 🔧 Configuración de Google Calendar

### Paso 1: Google Cloud Console

1. Ir a [https://console.cloud.google.com](https://console.cloud.google.com)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar **Google Calendar API**:
   - Ir a "APIs y servicios" → "Biblioteca"
   - Buscar "Google Calendar API"
   - Clic en "Habilitar"

### Paso 2: Crear Service Account

1. Ir a "IAM y administración" → "Cuentas de servicio"
2. Clic en "Crear cuenta de servicio"
3. Configurar:
   - **Nombre:** `autismo-calendar-service`
   - **ID:** `autismo-calendar-service`
   - **Descripción:** Servicio para sincronizar citas con Google Calendar
4. Clic en "Crear y continuar"
5. **Rol:** Editor de calendarios (Calendar Editor)
6. Clic en "Listo"

### Paso 3: Generar Credenciales JSON

1. Clic en la cuenta de servicio creada
2. Pestaña "Claves"
3. "Agregar clave" → "Crear nueva clave"
4. Tipo: **JSON**
5. Clic en "Crear" → Se descarga archivo `.json`

### Paso 4: Configurar en el Proyecto

```bash
# Crear carpeta de credenciales
mkdir -p backend/credentials

# Copiar archivo JSON descargado
cp ~/Downloads/autismo-calendar-service-xxxxx.json \
   backend/credentials/google-calendar-service-account.json
```

### Paso 5: Compartir Calendario

1. Abrir Google Calendar
2. Clic derecho en tu calendario → "Configuración y compartir"
3. En "Compartir con personas específicas":
   - Agregar el **email del Service Account**
   - Email formato: `autismo-calendar-service@tu-proyecto.iam.gserviceaccount.com`
   - Permisos: **Realizar cambios en los eventos**
4. Guardar

### Paso 6: Variables de Entorno (Opcional)

```env
# backend/.env
GOOGLE_CALENDAR_CREDENTIALS=credentials/google-calendar-service-account.json
GOOGLE_CALENDAR_ID=primary  # O ID específico del calendario
```

---

## 📡 Uso de los Endpoints

### 1. Crear Cita con Sincronización

```http
POST /api/v1/citas-calendario/
Authorization: Bearer <token_coordinador>
Content-Type: application/json

{
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2025-12-20",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "estado_id": 1,
  "motivo": "Sesión regular de lenguaje",
  "sincronizar_google_calendar": true
}
```

**Respuesta:**
```json
{
  "id_cita": 42,
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2025-12-20",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "estado_id": 1,
  "google_event_id": "abc123xyz789",
  "google_calendar_link": "https://www.google.com/calendar/event?eid=...",
  "sincronizado_calendar": true,
  "fecha_sincronizacion": "2025-12-16T14:30:00",
  "confirmada": false
}
```

### 2. Reprogramar Cita

```http
PUT /api/v1/citas-calendario/42/reprogramar
Authorization: Bearer <token_coordinador>
Content-Type: application/json

{
  "nueva_fecha": "2025-12-21",
  "nueva_hora_inicio": "14:00:00",
  "nueva_hora_fin": "15:00:00",
  "motivo": "Cambio por solicitud del padre",
  "actualizar_google_calendar": true
}
```

### 3. Cancelar Cita

```http
PUT /api/v1/citas-calendario/42/cancelar
Authorization: Bearer <token_coordinador>
Content-Type: application/json

{
  "motivo_cancelacion": "Niño enfermo, requiere reposo",
  "eliminar_de_google_calendar": true,
  "crear_reposicion": false
}
```

### 4. Obtener Calendario

```http
GET /api/v1/citas-calendario/calendario?fecha_inicio=2025-12-01&fecha_fin=2025-12-31&terapeuta_id=3
Authorization: Bearer <token_coordinador>
```

**Respuesta:**
```json
[
  {
    "id_cita": 42,
    "nino_id": 5,
    "terapeuta_id": 3,
    "fecha": "2025-12-20",
    "hora_inicio": "10:00:00",
    "hora_fin": "11:00:00",
    "google_calendar_link": "https://...",
    "confirmada": true
  },
  // ... más citas
]
```

---

## 🔒 Seguridad Implementada

### 1. Control de Acceso por Rol

```python
# Solo COORDINADOR puede gestionar citas
@router.post("/")
def crear_cita(
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    # Solo ejecuta si rol_id in [1, 2]
```

### 2. Validación de Datos

```python
from pydantic import Field, field_validator

class CitaCreate(BaseModel):
    fecha: date = Field(...)
    hora_inicio: time = Field(...)
    
    @field_validator('hora_fin')
    def validar_horas(cls, v, info):
        # Valida que hora_fin > hora_inicio
```

### 3. Transacciones Seguras

```python
try:
    # Crear en BD
    nueva_cita = Cita(...)
    db.add(nueva_cita)
    db.flush()
    
    # Sincronizar Google Calendar
    google_calendar_service.crear_evento(...)
    
    db.commit()
except Exception as e:
    db.rollback()
    raise HTTPException(500, str(e))
```

### 4. Manejo de Errores Robusto

- ✅ Si Google Calendar falla, la cita se crea en BD sin sincronizar
- ✅ Logs detallados de cada operación
- ✅ Mensajes de error descriptivos al frontend

---

## 📊 Manejo de Estados

### Estados de Cita (tabla `estado_cita`)

```sql
INSERT INTO estado_cita (codigo, nombre) VALUES
('PROGRAMADA', 'Programada'),
('CONFIRMADA', 'Confirmada'),
('EN_CURSO', 'En Curso'),
('COMPLETADA', 'Completada'),
('CANCELADA', 'Cancelada'),
('REPROGRAMADA', 'Reprogramada'),
('NO_ASISTIO', 'No Asistió');
```

### Flujo de Estados

```
PROGRAMADA → CONFIRMADA → EN_CURSO → COMPLETADA
    ↓            ↓           ↓
CANCELADA ← ─ ─ ─ ─ ─ ─ ─ ─ ┘
    ↓
REPROGRAMADA → PROGRAMADA (nueva cita)
```

---

## 🧪 Testing

### Ejemplo con `curl`

```bash
# 1. Login como coordinador
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"coordinador@test.com","password":"123456"}' \
  | jq -r '.token.access_token')

# 2. Crear cita
curl -X POST http://localhost:8000/api/v1/citas-calendario/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nino_id": 1,
    "terapeuta_id": 2,
    "terapia_id": 1,
    "fecha": "2025-12-25",
    "hora_inicio": "09:00:00",
    "hora_fin": "10:00:00",
    "sincronizar_google_calendar": true
  }'

# 3. Ver calendario
curl -X GET "http://localhost:8000/api/v1/citas-calendario/calendario?fecha_inicio=2025-12-01" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚀 Integración en el Sistema

### Registrar endpoints en `main.py`

```python
# backend/app/main.py
from app.api.v1.endpoints import citas_calendario

app.include_router(
    citas_calendario.router,
    prefix=f"{settings.API_V1_PREFIX}/citas-calendario",
    tags=["Citas y Calendario"]
)
```

---

## 📝 Consideraciones Importantes

### 1. **Google Calendar es Opcional**
- El sistema funciona **sin credenciales de Google**
- Si no están configuradas, muestra advertencia en logs
- Las citas se crean normalmente en BD, solo sin sincronizar

### 2. **Zona Horaria**
- Actualmente configurada: `America/Hermosillo` (GMT-7)
- Ajustar en `google_calendar_service.py` según ubicación

### 3. **Límites de Google Calendar API**
- Cuota diaria: 1,000,000 requests
- Suficiente para operación normal de un centro terapéutico

### 4. **Reposiciones**
- La lógica de crear citas de reposición está preparada (`crear_reposicion` en schemas)
- Implementación completa pendiente según reglas de negocio

### 5. **Notificaciones**
- Google Calendar envía notificaciones automáticas a los emails agregados
- Configurable en el evento (recordatorios por email/popup)

---

## 🐛 Troubleshooting

### Error: "Credenciales no encontradas"
```
⚠️  Archivo de credenciales no encontrado: credentials/google-calendar-service-account.json
```
**Solución:** Descargar JSON de Service Account y colocar en `backend/credentials/`

### Error: 403 Forbidden en Google Calendar
```
❌ Error HTTP al crear evento: <HttpError 403 ...>
```
**Solución:** Verificar que el calendario esté compartido con el email del Service Account

### Error: "Service Account email inválido"
**Solución:** En Google Calendar, agregar el email exacto del Service Account (formato: `nombre@proyecto.iam.gserviceaccount.com`)

### Citas se crean pero no sincronizan
**Verificar:**
1. Logs del backend: `logger.warning("⚠️  Cita X creada pero NO sincronizada")`
2. Estado de `esta_configurado`: `google_calendar_service.esta_configurado`
3. Archivo de credenciales existe y es válido

---

## 📚 Archivos del Sistema

```
backend/
├── app/
│   ├── models/
│   │   └── cita.py                    # Modelo extendido
│   ├── schemas/
│   │   └── cita.py                    # Schemas Pydantic
│   ├── services/
│   │   └── google_calendar_service.py # Servicio de Google Calendar
│   └── api/
│       └── v1/
│           └── endpoints/
│               └── citas_calendario.py # Endpoints REST
├── credentials/
│   └── google-calendar-service-account.json  # Credenciales (NO SUBIR A GIT)
└── scripts/
    └── migrar_citas_google_calendar.sql     # Script de migración SQL
```

---

## ✅ Checklist de Implementación

- [✅] Modelo `Cita` extendido con campos de Google Calendar
- [✅] Schemas Pydantic para CRUD completo
- [✅] Servicio `GoogleCalendarService` con manejo robusto de errores
- [✅] Endpoints REST para crear, reprogramar, cancelar citas
- [✅] Endpoint de calendario con filtros
- [✅] Control de acceso solo para COORDINADOR
- [✅] Transacciones seguras con rollback
- [✅] Script SQL de migración
- [✅] Documentación completa
- [⏳] Registrar router en `main.py` (pendiente)
- [⏳] Configurar credenciales de Google (manual)
- [⏳] Testing con datos reales

---

## 🎉 Funcionalidades Listas

✅ **Crear cita** → Se guarda en BD + Google Calendar  
✅ **Reprogramar cita** → Actualiza BD + Google Calendar  
✅ **Cancelar cita** → Cambia estado + Elimina de Google Calendar  
✅ **Ver calendario** → Filtros por fecha, terapeuta, niño  
✅ **Solo COORDINADOR** → Seguridad por roles  
✅ **Transacciones** → Rollback automático en errores  
✅ **Logs detallados** → Rastreo de cada operación  

---

**Desarrollado por:** Backend Senior Developer  
**Fecha:** 16 de diciembre de 2025  
**Versión:** 1.0.0

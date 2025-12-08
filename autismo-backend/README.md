# 🧩 Backend Autismo Mochis IA

Sistema de gestión integral para centro de terapias de autismo con algoritmos de IA (TOPSIS y Google Gemini) para priorización y recomendaciones.

## 🚀 Stack Tecnológico

- **Python 3.12+**
- **FastAPI 0.115.0** - Framework web moderno y rápido
- **SQLAlchemy 2.0.36** - ORM con soporte MySQL
- **Pydantic 2.10.3** - Validación de datos
- **JWT** - Autenticación con tokens (python-jose)
- **Bcrypt** - Hash de contraseñas (passlib)
- **Google Gemini AI** - Análisis y recomendaciones con IA
- **NumPy** - Algoritmo TOPSIS para toma de decisiones

## 📁 Estructura del Proyecto

```
autismo-backend/
├── app/
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── core/
│   │   ├── config.py          # Configuración con Pydantic Settings
│   │   └── security.py        # JWT, bcrypt, auth dependencies
│   ├── db/
│   │   ├── base_class.py      # DeclarativeBase SQLAlchemy 2.x
│   │   └── session.py         # Engine y SessionLocal
│   ├── models/                 # SQLAlchemy ORM (30+ tablas)
│   │   ├── usuario.py
│   │   ├── rol.py
│   │   ├── permiso.py
│   │   ├── role_permiso.py
│   │   ├── personal.py
│   │   ├── tutor.py
│   │   ├── nino.py
│   │   ├── terapia.py
│   │   ├── cita.py
│   │   ├── recurso.py
│   │   ├── notificacion.py
│   │   ├── decision_log.py
│   │   ├── auditoria.py
│   │   └── catalogos.py
│   ├── schemas/                # Pydantic v2 schemas
│   │   ├── auth.py
│   │   ├── usuario.py
│   │   ├── rol.py
│   │   ├── personal.py
│   │   ├── tutor.py
│   │   ├── nino.py
│   │   ├── terapia.py
│   │   ├── cita.py
│   │   ├── recurso.py
│   │   └── notificacion.py
│   ├── services/              # Business logic (TODO)
│   │   ├── usuario_service.py
│   │   ├── topsis_service.py
│   │   └── ia_service.py
│   └── api/
│       └── v1/
│           ├── __init__.py
│           └── endpoints/
│               ├── auth.py         # ✅ Implementado
│               ├── usuarios.py     # TODO
│               ├── roles.py        # TODO
│               ├── personal.py     # TODO
│               ├── tutores.py      # TODO
│               ├── ninos.py        # TODO
│               ├── terapias.py     # TODO
│               ├── citas.py        # TODO
│               ├── sesiones.py     # TODO
│               ├── recursos.py     # TODO
│               ├── notificaciones.py # TODO
│               ├── priorizacion.py # TODO (TOPSIS)
│               └── ia.py           # TODO (Gemini)
├── scripts/
│   ├── init_database.py       # Script maestro de inicialización
│   ├── init_catalogos.py      # Poblar tablas de catálogos
│   ├── init_roles_permisos.py # Crear roles y permisos
│   └── crear_usuarios_demo.py # Usuarios de prueba
├── requirements.txt
├── .env.example
└── README.md
```

## ⚙️ Instalación y Configuración

### 1. Clonar e Instalar Dependencias

```bash
cd autismo-backend
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```env
# Base de datos MySQL
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/autismo_mochis

# JWT
JWT_SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Gemini AI
GEMINI_API_KEY=tu_api_key_de_google

# App
PROJECT_NAME="Autismo Mochis IA"
API_V1_PREFIX=/api/v1
DEBUG=True
```

### 3. Crear Base de Datos

```sql
CREATE DATABASE autismo_mochis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Ejecutar Migraciones (Manual)

Ejecutar el esquema SQL completo proporcionado en tu motor MySQL.

### 5. Inicializar Datos

```bash
cd scripts
python init_database.py
```

Este script ejecuta en orden:
1. **init_catalogos.py** - Puebla 9 tablas de catálogos
2. **init_roles_permisos.py** - Crea 4 roles con 40+ permisos
3. **crear_usuarios_demo.py** - Crea 4 usuarios de prueba

### 6. Iniciar Servidor

```bash
# Desarrollo con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

El servidor estará disponible en:
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## 🔐 Autenticación y Autorización

### Sistema de Roles

| Rol | Descripción | Permisos |
|-----|-------------|----------|
| **ADMIN** | Administrador del sistema | Todos los permisos |
| **COORDINADOR** | Coordinador del centro | Gestión de personal, niños, terapias, priorización |
| **TERAPEUTA** | Terapeuta | Ver/editar sesiones propias, recursos, IA |
| **PADRE** | Padre/tutor del niño | Ver información de sus hijos, citas, recursos |

### Usuarios Demo

Después de ejecutar `init_database.py`:

```
Email: admin@demo.com
Contraseña: 12345678

Email: coordinador@demo.com
Contraseña: 12345678

Email: terapeuta@demo.com
Contraseña: 12345678

Email: padre@demo.com
Contraseña: 12345678
```

### Flujo de Autenticación

1. **Login**: `POST /api/v1/auth/login`
   ```json
   {
     "email": "admin@demo.com",
     "password": "12345678"
   }
   ```
   
2. **Respuesta**: JWT token + datos de usuario con permisos
   ```json
   {
     "token": {
       "access_token": "eyJhbGc...",
       "token_type": "bearer"
     },
     "user": {
       "id": 1,
       "nombres": "Ana",
       "email": "admin@demo.com",
       "rol_id": 1,
       "rol_nombre": "ADMIN",
       "permisos": ["usuarios:ver", "usuarios:crear", ...]
     }
   }
   ```

3. **Usar Token**: Agregar header en todas las peticiones
   ```
   Authorization: Bearer eyJhbGc...
   ```

### Protección de Endpoints

```python
from app.core.security import get_current_active_user, require_role, require_permissions

# Solo usuarios autenticados
@router.get("/")
async def get_items(current_user: Usuario = Depends(get_current_active_user)):
    pass

# Solo roles específicos
@router.post("/", dependencies=[Depends(require_role("ADMIN", "COORDINADOR"))])
async def create_item():
    pass

# Permisos específicos
@router.delete("/{id}", dependencies=[Depends(require_permissions("usuarios:eliminar"))])
async def delete_item(id: int):
    pass
```

## 📊 Base de Datos

### Tablas Principales (30+)

**Usuarios y Roles:**
- `usuarios` - Usuarios del sistema
- `roles` - Roles (ADMIN, COORDINADOR, TERAPEUTA, PADRE)
- `permisos` - Permisos granulares
- `role_permisos` - Relación roles-permisos

**Personal:**
- `personal` - Terapeutas y personal del centro
- `personal_perfil` - Información detallada
- `personal_horarios` - Horarios de disponibilidad

**Tutores:**
- `tutores` - Padres/tutores
- `tutor_direccion` - Dirección del tutor

**Niños:**
- `ninos` - Niños en el sistema
- `nino_direccion` - Dirección del niño
- `nino_diagnostico` - Diagnóstico médico
- `nino_info_emocional` - Perfil emocional
- `nino_archivos` - Documentos adjuntos

**Terapias:**
- `terapias` - Tipos de terapia
- `terapia_personal` - Asignación terapeuta-terapia
- `terapia_nino` - Terapias asignadas a niños
- `sesiones` - Sesiones de terapia realizadas
- `reposiciones` - Reposiciones de sesiones

**Citas:**
- `citas` - Citas programadas

**Recursos:**
- `recursos` - Recursos educativos/terapéuticos
- `tareas_recursos` - Tareas asignadas a niños
- `valoraciones` - Calificaciones de recursos
- `recomendaciones` - Recomendaciones de recursos (IA)

**Sistema:**
- `notificaciones` - Notificaciones a usuarios
- `decision_logs` - Logs de decisiones IA/TOPSIS
- `auditoria` - Auditoría de acciones

**Catálogos (9):**
- `grado_academico`
- `estado_laboral`
- `tipo_terapia`
- `prioridad`
- `estado_cita`
- `nivel_dificultad`
- `tipo_recurso`
- `categoria_recurso`
- `nivel_recurso`

## 🤖 Inteligencia Artificial

### TOPSIS (TODO - Implementar)

Algoritmo de toma de decisiones multi-criterio para:
- **Priorización de niños**: Determinar qué niños requieren atención urgente
- **Asignación de terapeutas**: Seleccionar terapeuta óptimo según carga, experiencia, especialidad

Endpoint: `POST /api/v1/priorizacion/topsis`

### Google Gemini AI (TODO - Implementar)

Funcionalidades de IA generativa:
- **Resumen de progreso**: Analizar sesiones y generar resumen del avance del niño
- **Sugerencias de actividades**: Recomendar recursos y actividades personalizadas
- **Dashboard insights**: Análisis general del centro

Endpoints:
- `GET /api/v1/ia/ninos/{id}/resumen`
- `GET /api/v1/ia/ninos/{id}/sugerencias`
- `POST /api/v1/ia/dashboard-resumen`

## 🛣️ Endpoints API

### ✅ Implementados

#### Autenticación
- `POST /api/v1/auth/login` - Login con email/password
- `POST /api/v1/auth/change-password` - Cambiar contraseña
- `GET /api/v1/auth/me` - Obtener usuario actual

### 📋 TODO - Por Implementar

#### Usuarios
- `GET /api/v1/usuarios` - Listar usuarios
- `POST /api/v1/usuarios` - Crear usuario
- `GET /api/v1/usuarios/{id}` - Obtener usuario
- `PUT /api/v1/usuarios/{id}` - Actualizar usuario
- `DELETE /api/v1/usuarios/{id}` - Eliminar usuario

#### Roles y Permisos
- `GET /api/v1/roles` - Listar roles
- `POST /api/v1/roles` - Crear rol
- `GET /api/v1/roles/{id}` - Obtener rol con permisos
- `PUT /api/v1/roles/{id}` - Actualizar rol
- `POST /api/v1/roles/{id}/permisos` - Asignar permisos a rol

[... más endpoints por documentar según se implementen]

## 🧪 Testing

```bash
# TODO: Agregar tests unitarios
pytest

# TODO: Coverage
pytest --cov=app tests/
```

## 📝 Convenciones de Código

- **Modelos**: SQLAlchemy 2.x con `relationship(..., back_populates=...)`
- **Schemas**: Pydantic v2 con `ConfigDict(from_attributes=True)`
- **Endpoints**: Async cuando sea posible
- **Errores**: HTTPException con status codes apropiados
- **Logging**: Decision_logs para IA, Auditoria para acciones críticas

## 🚀 Roadmap

### Fase 1: Core (✅ Completado ~40%)
- [x] Configuración proyecto
- [x] Base de datos y modelos
- [x] Autenticación JWT
- [x] Sistema de roles y permisos
- [x] Schemas Pydantic
- [ ] Service layer
- [ ] CRUD básico (Usuarios, Roles, Personal)

### Fase 2: Funcionalidades Principales
- [ ] Módulo Niños completo
- [ ] Módulo Terapias y Sesiones
- [ ] Módulo Citas
- [ ] Módulo Recursos
- [ ] Sistema de Notificaciones

### Fase 3: Inteligencia Artificial
- [ ] Servicio TOPSIS
- [ ] Integración Google Gemini
- [ ] Recomendaciones automáticas

### Fase 4: Optimización
- [ ] WebSockets para notificaciones en tiempo real
- [ ] Middleware de auditoría automática
- [ ] Tests unitarios y de integración
- [ ] Documentación API completa
- [ ] Deploy con Docker

## 🤝 Contribución

Proyecto en desarrollo activo. Contactar al equipo para contribuir.

## 📄 Licencia

Privado - Autismo Mochis IA © 2024

# Backend - Autismo Mochis IA

Sistema de autenticación basado en FastAPI con JWT para el centro de atención de autismo.

## 📋 Requisitos

- Python 3.9 o superior
- MySQL 8.0 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno virtual

**Windows (CMD):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus datos:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=autismo_mochis_ia
```

### 5. Crear la base de datos

Ejecuta el script SQL proporcionado en MySQL para crear la base de datos y las tablas.

## 🏃 Ejecución

### Opción 1: Script automático (Windows)

```bash
.\start.bat
```

o con PowerShell:

```bash
.\start.ps1
```

### Opción 2: Comando directo

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Opción 3: Ejecutar con Python

```bash
python -m uvicorn app.main:app --reload
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

## 📚 Estructura del proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── api/
│   │   ├── deps.py            # Dependencias (auth, permisos)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── auth.py        # Endpoints de autenticación
│   ├── core/
│   │   ├── config.py          # Configuración
│   │   └── security.py        # JWT y hashing
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base_class.py      # Clase base SQLAlchemy
│   │   └── session.py         # Sesión de BD
│   ├── models/                # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── rol.py
│   │   ├── permiso.py
│   │   └── role_permiso.py
│   └── schemas/               # Schemas Pydantic
│       ├── __init__.py
│       ├── auth.py
│       └── usuario.py
├── .env                       # Variables de entorno (no en git)
├── .env.example              # Ejemplo de variables
├── .gitignore
├── requirements.txt
├── start.bat                 # Script de inicio Windows CMD
├── start.ps1                 # Script de inicio PowerShell
└── README.md
```

## 🔐 Autenticación

El sistema utiliza JWT (JSON Web Tokens) para la autenticación.

### Login

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña"
}
```

**Response:**
```json
{
  "token": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
  },
  "user": {
    "id": 1,
    "nombres": "Juan",
    "apellido_paterno": "Pérez",
    "email": "juan@ejemplo.com",
    "rol_id": 2,
    "rol_nombre": "Coordinador",
    "permisos": ["ver_ninos", "editar_citas", ...]
  }
}
```

### Uso del token

Incluye el token en el header `Authorization` de las peticiones:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 👥 Roles del sistema

1. **Admin** (rol_id: 1) - Acceso total al sistema
2. **Coordinador** (rol_id: 2) - Gestión de personal y niños
3. **Terapeuta** (rol_id: 3) - Gestión de sesiones y terapias
4. **Padre** (rol_id: 4) - Consulta de información de sus hijos

## 🔒 Protección de endpoints

### Requiere autenticación

```python
from app.api.deps import get_current_active_user

@router.get("/protegido")
def endpoint_protegido(current_user: Usuario = Depends(get_current_active_user)):
    return {"user": current_user.email}
```

### Requiere rol específico

```python
from app.api.deps import require_admin

@router.post("/admin-only")
def solo_admin(current_user: Usuario = Depends(require_admin)):
    return {"message": "Acceso de administrador"}
```

### Requiere permisos

```python
from app.api.deps import require_permissions

@router.get("/recursos")
def ver_recursos(
    current_user: Usuario = Depends(require_permissions(["ver_recursos"]))
):
    return {"recursos": []}
```

## 🛠️ Desarrollo

### Generar nueva clave secreta JWT

```bash
openssl rand -hex 64
```

### Ver logs del servidor

El servidor con `--reload` muestra logs en tiempo real en la consola.

## 📖 Documentación API

Una vez iniciado el servidor, visita:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## ⚠️ Notas importantes

1. Cambia el `JWT_SECRET_KEY` en producción
2. No compartas el archivo `.env`
3. El entorno virtual (`venv/`) no debe subirse a git
4. Asegúrate de que MySQL esté corriendo antes de iniciar el backend
5. La primera vez puede tardar en instalar las dependencias

## 🐛 Solución de problemas

### Error de conexión a MySQL

Verifica que MySQL esté corriendo y las credenciales en `.env` sean correctas.

### Error al activar entorno virtual en PowerShell

Ejecuta como administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error de módulos no encontrados

Asegúrate de estar en el entorno virtual y ejecuta:
```bash
pip install -r requirements.txt
```

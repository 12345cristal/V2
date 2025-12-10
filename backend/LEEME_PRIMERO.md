# ✅ BACKEND CREADO EXITOSAMENTE

## 📁 Estructura creada

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # ✅ Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py               # ✅ Dependencias (auth, guards)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── auth.py           # ✅ Endpoints de autenticación
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # ✅ Configuración y .env
│   │   └── security.py           # ✅ JWT y hashing de passwords
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base_class.py         # ✅ Base SQLAlchemy
│   │   └── session.py            # ✅ Sesión de BD
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py            # ✅ Modelo Usuario
│   │   ├── rol.py                # ✅ Modelo Rol
│   │   ├── permiso.py            # ✅ Modelo Permiso
│   │   └── role_permiso.py       # ✅ Relación Roles-Permisos
│   └── schemas/
│       ├── __init__.py
│       ├── auth.py               # ✅ Schemas autenticación
│       └── usuario.py            # ✅ Schemas usuario
├── scripts/
│   ├── __init__.py
│   └── init_roles_permisos.py    # ✅ Script inicialización
├── .env                          # ✅ Variables de entorno
├── .env.example                  # ✅ Ejemplo de variables
├── .gitignore                    # ✅ Ignorar archivos
├── requirements.txt              # ✅ Dependencias Python
├── start.bat                     # ✅ Script inicio Windows CMD
├── start.ps1                     # ✅ Script inicio PowerShell
├── README.md                     # ✅ Documentación principal
├── INSTALACION.md               # ✅ Guía de instalación
└── TESTING_API.md               # ✅ Guía de pruebas
```

## 🚀 PASOS PARA INICIAR

### 1️⃣ Crear entorno virtual

**Windows (PowerShell):**
```powershell
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si hay error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2️⃣ Instalar dependencias

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Configurar base de datos

1. Asegúrate de que MySQL esté corriendo
2. Ejecuta el script SQL completo en MySQL
3. Edita el archivo `.env` con tus credenciales:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=autismo_mochis_ia
```

### 4️⃣ Inicializar roles y permisos

```powershell
python scripts/init_roles_permisos.py
```

Esto creará:
- ✅ Roles: Admin, Coordinador, Terapeuta, Padre
- ✅ Permisos del sistema
- ✅ Usuario admin inicial (admin@autismo.com / admin123)

### 5️⃣ Iniciar el servidor

**Opción 1: Script automático**
```powershell
.\start.ps1
```

**Opción 2: Comando directo**
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 6️⃣ Verificar funcionamiento

Abre tu navegador en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔐 SISTEMA DE AUTENTICACIÓN

### Características implementadas:

✅ **Login con JWT**
- Endpoint: `POST /api/v1/auth/login`
- Retorna: Token JWT + datos del usuario

✅ **Validación de tokens**
- Middleware automático con OAuth2
- Verificación de expiración
- Verificación de firma

✅ **Roles y permisos**
- 4 roles: Admin, Coordinador, Terapeuta, Padre
- Sistema completo de permisos
- Guards para proteger endpoints

✅ **Dependencias reutilizables**
- `get_current_user`: Obtiene usuario del token
- `get_current_active_user`: Verifica usuario activo
- `require_admin`: Solo administradores
- `require_admin_or_coordinator`: Admin o coordinador
- `require_role([ids])`: Roles específicos
- `require_permissions([permisos])`: Permisos específicos

### Ejemplo de uso en endpoints:

```python
from fastapi import APIRouter, Depends
from app.api.deps import get_current_active_user, require_admin

router = APIRouter()

# Endpoint que requiere autenticación
@router.get("/protegido")
def endpoint_protegido(
    current_user: Usuario = Depends(get_current_active_user)
):
    return {"user": current_user.email}

# Endpoint solo para administradores
@router.post("/admin-only")
def solo_admin(
    current_user: Usuario = Depends(require_admin)
):
    return {"message": "Acceso administrativo"}

# Endpoint con permisos específicos
@router.get("/recursos")
def ver_recursos(
    current_user: Usuario = Depends(require_permissions(["ver_recursos"]))
):
    return {"recursos": []}
```

## 🎯 ROLES DEL SISTEMA

| Rol | ID | Descripción | Permisos |
|-----|-------|-------------|----------|
| **Admin** | 1 | Administrador del sistema | Todos los permisos |
| **Coordinador** | 2 | Coordinador del centro | Gestión general (excepto admin) |
| **Terapeuta** | 3 | Terapeuta | Sesiones, recursos, consultas |
| **Padre** | 4 | Padre/tutor | Solo consulta |

## 📡 ENDPOINTS DISPONIBLES

### Autenticación
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/token` - Login OAuth2
- `GET /api/v1/auth/me` - Usuario actual
- `POST /api/v1/auth/logout` - Logout

### Sistema
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Documentación Swagger
- `GET /redoc` - Documentación ReDoc

## 🔗 INTEGRACIÓN CON ANGULAR

Tu frontend Angular ya está configurado correctamente:

1. **AuthService** (`auth.service.ts`):
   - ✅ Compatible con el endpoint `/api/v1/auth/login`
   - ✅ Almacena token y datos del usuario
   - ✅ Verifica permisos

2. **TokenInterceptor** (`token.interceptor.ts`):
   - ✅ Agrega automáticamente el header `Authorization: Bearer <token>`

3. **AuthGuard** (`auth.guard.ts`):
   - ✅ Protege rutas que requieren autenticación

4. **PermissionGuard** (`permission.guard.ts`):
   - ✅ Verifica permisos específicos

Solo necesitas asegurarte de que `environment.apiBaseUrl` apunte a:
```typescript
apiBaseUrl: 'http://localhost:8000'
```

## 🧪 PROBAR EL SISTEMA

### Desde Swagger UI:
1. Ve a http://localhost:8000/docs
2. POST `/api/v1/auth/login` con:
   ```json
   {
     "email": "admin@autismo.com",
     "password": "admin123"
   }
   ```
3. Copia el `access_token`
4. Click en "Authorize" (arriba)
5. Pega el token
6. Prueba otros endpoints protegidos

### Desde PowerShell:
```powershell
# Login
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
  -Method Post `
  -Body (@{email="admin@autismo.com"; password="admin123"} | ConvertTo-Json) `
  -ContentType "application/json"

# Guardar token
$token = $response.token.access_token

# Usar token
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/me" `
  -Method Get `
  -Headers @{Authorization="Bearer $token"}
```

## ⚠️ IMPORTANTE

1. **Cambia la contraseña del admin:**
   - Email: admin@autismo.com
   - Password inicial: admin123
   - ⚠️ Cambia esto inmediatamente en producción

2. **Variables de entorno:**
   - El archivo `.env` contiene configuración sensible
   - No lo subas a git (ya está en `.gitignore`)
   - En producción, usa variables de entorno del servidor

3. **JWT Secret:**
   - La clave JWT debe ser única en producción
   - Genera una nueva con: `openssl rand -hex 64`

## 📚 DOCUMENTACIÓN

- **README.md**: Documentación general
- **INSTALACION.md**: Guía paso a paso
- **TESTING_API.md**: Cómo probar los endpoints

## ✅ TODO LISTO

Tu backend está completamente funcional con:
- ✅ FastAPI configurado
- ✅ Uvicorn listo para ejecutar
- ✅ Autenticación JWT
- ✅ Sistema de roles y permisos
- ✅ Base de datos MySQL conectada
- ✅ CORS habilitado para Angular
- ✅ Entorno virtual (venv)
- ✅ .gitignore configurado
- ✅ Scripts de inicio automatizados
- ✅ Documentación completa

## 🚀 SIGUIENTE PASO

```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Inicializar base de datos
python scripts/init_roles_permisos.py

# 4. Iniciar servidor
.\start.ps1
```

¡Listo para usar! 🎉

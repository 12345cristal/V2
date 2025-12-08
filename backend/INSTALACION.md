# INSTALACIÓN Y CONFIGURACIÓN DEL BACKEND

Guía completa para configurar el backend desde cero.

## 📋 Paso 1: Verificar requisitos

```bash
# Verificar Python
python --version
# Debe ser 3.9 o superior

# Verificar MySQL
mysql --version
# Debe ser 8.0 o superior
```

## 📦 Paso 2: Crear y activar entorno virtual

### Windows (CMD):
```bash
python -m venv venv
venv\Scripts\activate.bat
```

### Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si hay error de permisos en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

## 📥 Paso 3: Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🗄️ Paso 4: Configurar base de datos

1. **Crear la base de datos en MySQL:**

```sql
-- Conectarse a MySQL
mysql -u root -p

-- Ejecutar el script SQL completo proporcionado
source ruta/al/script.sql
```

O copia y pega el contenido del script SQL completo en MySQL Workbench.

2. **Configurar credenciales:**

Copia `.env.example` a `.env`:
```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de MySQL:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_aqui
DB_NAME=autismo_mochis_ia
```

## 🔐 Paso 5: Inicializar roles y permisos

```bash
python scripts/init_roles_permisos.py
```

Este script creará:
- ✓ Roles: Admin, Coordinador, Terapeuta, Padre
- ✓ Permisos del sistema
- ✓ Asignación de permisos a roles
- ✓ Usuario administrador por defecto:
  - Email: `admin@autismo.com`
  - Password: `admin123`

**⚠️ IMPORTANTE:** Cambia la contraseña del administrador inmediatamente después del primer login.

## 🚀 Paso 6: Iniciar el servidor

### Opción 1: Script automático (Windows)
```bash
.\start.bat
```

### Opción 2: PowerShell
```bash
.\start.ps1
```

### Opción 3: Comando directo
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## ✅ Paso 7: Verificar instalación

Abre tu navegador en:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

Deberías ver la documentación interactiva de la API.

## 🧪 Paso 8: Probar autenticación

1. Ve a http://localhost:8000/docs
2. Busca el endpoint `POST /api/v1/auth/login`
3. Click en "Try it out"
4. Usa las credenciales:
```json
{
  "email": "admin@autismo.com",
  "password": "admin123"
}
```
5. Click en "Execute"
6. Deberías recibir un token JWT

## 🔧 Solución de problemas

### Error: "Module not found"
```bash
# Asegúrate de estar en el entorno virtual
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL"
- Verifica que MySQL esté corriendo
- Verifica credenciales en `.env`
- Verifica que la base de datos exista

### Error: "Access denied for user"
- Verifica usuario y contraseña en `.env`
- Verifica que el usuario tenga permisos en MySQL

### Error al activar venv en PowerShell
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Estructura de archivos

```
backend/
├── app/
│   ├── api/              # Endpoints
│   ├── core/             # Configuración
│   ├── db/               # Base de datos
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Schemas Pydantic
│   └── main.py           # App principal
├── scripts/
│   └── init_roles_permisos.py
├── venv/                 # Entorno virtual (no en git)
├── .env                  # Variables (no en git)
├── .env.example
├── requirements.txt
├── start.bat
├── start.ps1
└── README.md
```

## 🎯 Próximos pasos

1. Cambia la contraseña del administrador
2. Crea usuarios de prueba para cada rol
3. Conecta el frontend Angular al backend
4. Prueba los endpoints protegidos

## 🔑 Roles del sistema

1. **Admin (ID: 1)**: Acceso total
2. **Coordinador (ID: 2)**: Gestión general
3. **Terapeuta (ID: 3)**: Sesiones y recursos
4. **Padre (ID: 4)**: Solo consulta

## 📞 Soporte

Si encuentras problemas, verifica:
- Logs del servidor
- Variables de entorno en `.env`
- Conexión a MySQL
- Versión de Python y dependencias

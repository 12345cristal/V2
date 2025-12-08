# ⚡ Comandos Rápidos - Módulo Terapias

## 🚀 Iniciar Todo

```powershell
# 1. Inicializar catálogos
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python scripts/init_catalogos_terapias.py

# 2. Iniciar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Abrir Swagger (en navegador)
start http://localhost:8000/docs

# 4. Iniciar frontend (nueva terminal)
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo
npm start
```

## 🔍 Verificar Base de Datos

```sql
-- Ver tipos de terapia
SELECT * FROM tipo_terapia;

-- Ver prioridades
SELECT * FROM prioridad;

-- Ver terapias
SELECT t.*, tt.nombre as tipo 
FROM terapias t 
JOIN tipo_terapia tt ON t.tipo_id = tt.id;

-- Ver asignaciones de personal
SELECT 
    p.nombres, 
    p.apellido_paterno, 
    t.nombre as terapia,
    tp.activo
FROM terapias_personal tp
JOIN personal p ON tp.personal_id = p.id
JOIN terapias t ON tp.terapia_id = t.id;

-- Ver personal sin terapia
SELECT p.id, p.nombres, p.apellido_paterno, p.especialidad_principal
FROM personal p
WHERE p.id NOT IN (
    SELECT personal_id 
    FROM terapias_personal 
    WHERE activo = 1
)
AND p.estado_laboral = 'ACTIVO';
```

## 🧪 Pruebas con cURL

### Obtener Token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"coordinador@test.com","password":"password123"}'
```

### Listar Terapias
```bash
curl -X GET "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Crear Terapia
```bash
curl -X POST "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Terapia Test",
    "descripcion": "Descripción de prueba",
    "tipo_id": 1,
    "duracion_minutos": 45,
    "objetivo_general": "Objetivo de prueba"
  }'
```

### Personal Sin Terapia
```bash
curl -X GET "http://localhost:8000/api/v1/personal/sin-terapia" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Asignar Personal a Terapia
```bash
curl -X POST "http://localhost:8000/api/v1/terapias/asignar" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id_personal": 5,
    "id_terapia": 2
  }'
```

### Personal Asignado
```bash
curl -X GET "http://localhost:8000/api/v1/terapias/personal-asignado" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Cambiar Estado
```bash
curl -X PATCH "http://localhost:8000/api/v1/terapias/1/estado" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐍 Pruebas con Python

### Script de Prueba Completo
```powershell
# Configurar token en el archivo
notepad backend/scripts/test_terapias.py

# Ejecutar pruebas
python backend/scripts/test_terapias.py
```

### Prueba Manual Rápida
```python
import requests

TOKEN = "tu_token_aqui"
BASE = "http://localhost:8000/api/v1"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Listar terapias
r = requests.get(f"{BASE}/terapias", headers=headers)
print(r.json())

# Crear terapia
data = {
    "nombre": "Terapia Python",
    "descripcion": "Creada desde Python",
    "tipo_id": 1,
    "duracion_minutos": 45
}
r = requests.post(f"{BASE}/terapias", headers=headers, json=data)
print(r.json())
```

## 📊 Endpoints Disponibles

```
GET    /api/v1/terapias                      # Lista todas
GET    /api/v1/terapias/{id}                 # Obtiene una
POST   /api/v1/terapias                      # Crea nueva
PUT    /api/v1/terapias/{id}                 # Actualiza
PATCH  /api/v1/terapias/{id}/estado          # Cambia estado
DELETE /api/v1/terapias/{id}                 # Elimina (soft)
POST   /api/v1/terapias/asignar              # Asigna personal
GET    /api/v1/terapias/personal-asignado    # Lista asignados
GET    /api/v1/terapias/catalogos/tipos      # Tipos de terapia
GET    /api/v1/personal/sin-terapia          # Personal disponible
```

## 🔥 Atajos de Desarrollo

### Ver logs del servidor
```powershell
# Backend ya muestra logs en consola con --reload
```

### Reiniciar servidor rápido
```powershell
# Ctrl + C en la terminal del backend
# Luego ejecutar de nuevo:
uvicorn app.main:app --reload
```

### Ver base de datos en tiempo real
```sql
-- Monitorear cambios
SELECT * FROM terapias ORDER BY id DESC LIMIT 5;
SELECT * FROM terapias_personal ORDER BY id DESC LIMIT 5;
```

## 🎯 Verificación Rápida

### ✅ Checklist de Funcionamiento

```powershell
# 1. Backend corriendo
curl http://localhost:8000/health

# 2. Catálogos inicializados
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/terapias/catalogos/tipos

# 3. Terapias listadas
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/terapias

# 4. Frontend conectado
start http://localhost:4200/coordinador/terapias
```

## 🐛 Debug Rápido

### Si no aparecen terapias
```sql
-- Verificar datos
SELECT COUNT(*) FROM terapias;
SELECT COUNT(*) FROM tipo_terapia;

-- Re-inicializar si necesario
DELETE FROM terapias;
DELETE FROM tipo_terapia;
-- Luego ejecutar: python scripts/init_catalogos_terapias.py
```

### Si falla autenticación
```sql
-- Verificar usuario existe
SELECT * FROM usuarios WHERE email = 'coordinador@test.com';

-- Resetear password (si necesario)
UPDATE usuarios 
SET hashed_password = '$2b$12$...'  -- usar bcrypt
WHERE email = 'coordinador@test.com';
```

### Si no encuentra personal
```sql
-- Verificar personal activo
SELECT * FROM personal WHERE estado_laboral = 'ACTIVO';

-- Activar personal si necesario
UPDATE personal SET estado_laboral = 'ACTIVO' WHERE id = 5;
```

## 📖 Documentación Rápida

```powershell
# Swagger UI
start http://localhost:8000/docs

# ReDoc
start http://localhost:8000/redoc

# Documentación completa
notepad backend/MODULO_TERAPIAS_COMPLETADO.md

# Guía rápida
notepad backend/TERAPIAS_README.md
```

## ⚡ Super Rápido (Todo en uno)

```powershell
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python scripts/init_catalogos_terapias.py; uvicorn app.main:app --reload
```

---

**Listo! 🚀** Todos los comandos necesarios para trabajar con el módulo de terapias.

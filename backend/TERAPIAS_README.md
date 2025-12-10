# 🚀 Guía Rápida - Módulo de Terapias

## ✅ Archivos Creados

```
backend/
├── app/
│   ├── models/
│   │   └── terapia.py                    ✅ NUEVO
│   ├── schemas/
│   │   └── terapia.py                    ✅ NUEVO
│   └── api/
│       └── v1/
│           └── endpoints/
│               └── terapias.py           ✅ NUEVO
├── scripts/
│   ├── init_catalogos_terapias.py        ✅ NUEVO
│   └── init_catalogos_terapias.sql       ✅ NUEVO
└── MODULO_TERAPIAS_COMPLETADO.md         ✅ NUEVO
```

## 📦 Instalación

### 1. Inicializar Catálogos

**Opción A - Python (Recomendado):**
```powershell
cd backend
python scripts/init_catalogos_terapias.py
```

**Opción B - SQL:**
```powershell
# Si usas MySQL desde línea de comandos
mysql -u root -p autismo_mochis_ia < backend/scripts/init_catalogos_terapias.sql
```

### 2. Iniciar el Servidor

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Verificar Instalación

Abre en tu navegador:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔌 Endpoints Disponibles

### Terapias (Base: `/api/v1/terapias`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Lista todas las terapias |
| GET | `/{id}` | Obtiene una terapia |
| POST | `/` | Crea una terapia |
| PUT | `/{id}` | Actualiza una terapia |
| PATCH | `/{id}/estado` | Cambia estado activo/inactivo |
| POST | `/asignar` | Asigna personal a terapia |
| GET | `/personal-asignado` | Lista personal con terapias |
| GET | `/catalogos/tipos` | Catálogo de tipos de terapia |

### Personal (Base: `/api/v1/personal`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/sin-terapia` | Personal disponible sin terapia |

## 🧪 Pruebas Rápidas

### 1. Listar Terapias
```bash
curl -X GET "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2. Crear Terapia
```bash
curl -X POST "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Terapia de Lenguaje",
    "descripcion": "Para niños con TEA",
    "tipo_id": 1,
    "duracion_minutos": 45
  }'
```

### 3. Personal Sin Terapia
```bash
curl -X GET "http://localhost:8000/api/v1/personal/sin-terapia" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Asignar Personal
```bash
curl -X POST "http://localhost:8000/api/v1/terapias/asignar" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id_personal": 5,
    "id_terapia": 2
  }'
```

## 📊 Catálogos Inicializados

### Tipos de Terapia
- `LENGUAJE` - Terapia de Lenguaje
- `CONDUCTUAL` - Terapia Conductual
- `OCUPACIONAL` - Terapia Ocupacional
- `FISICA` - Terapia Física
- `ABA` - Análisis Conductual Aplicado
- `SENSORIAL` - Integración Sensorial
- `COGNITIVA` - Terapia Cognitiva
- `SOCIAL` - Habilidades Sociales
- `PSICOLOGICA` - Apoyo Psicológico
- `ACADEMICA` - Apoyo Académico

### Prioridades
- `URGENTE` - Urgente
- `ALTA` - Alta
- `MEDIA` - Media
- `BAJA` - Baja

## 🔥 Frontend Integrado

El frontend Angular ya tiene el componente listo:
- **Componente:** `src/app/coordinador/terapias/terapias.ts`
- **Servicio:** `src/app/service/terapias.service.ts`
- **Ruta:** `/coordinador/terapias`

## ✨ Características

✅ CRUD completo de terapias
✅ Asignación de terapeutas
✅ Gestión de estado (activo/inactivo)
✅ Personal disponible/asignado
✅ Catálogos precargados
✅ Validaciones de negocio
✅ Documentación completa

## 📚 Documentación Completa

Ver: `MODULO_TERAPIAS_COMPLETADO.md` para documentación detallada.

---

**¡Listo para usar!** 🎉

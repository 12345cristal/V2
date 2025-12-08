# 📋 MÓDULO DE TERAPIAS - BACKEND COMPLETADO

## 📌 Descripción General

Este módulo gestiona todas las operaciones relacionadas con terapias, incluyendo:
- CRUD de terapias
- Asignación de personal (terapeutas) a terapias
- Catálogos de tipos de terapia y prioridades
- Gestión de sesiones
- Control de reposiciones

---

## 🗄️ Base de Datos

### Tablas Principales

#### `terapias`
Almacena las terapias disponibles en el centro.

```sql
- id (PK)
- nombre
- descripcion
- tipo_id (FK -> tipo_terapia)
- duracion_minutos
- objetivo_general
- activo (1=activa, 0=inactiva)
```

#### `terapias_personal`
Relación many-to-many entre terapias y personal (terapeutas).

```sql
- id (PK)
- terapia_id (FK -> terapias)
- personal_id (FK -> personal)
- activo
```

#### `terapias_nino`
Asignación de terapias a niños con su terapeuta y prioridad.

```sql
- id (PK)
- nino_id (FK -> ninos)
- terapia_id (FK -> terapias)
- terapeuta_id (FK -> personal)
- prioridad_id (FK -> prioridad)
- frecuencia_semana
- fecha_asignacion
- activo
```

#### `sesiones`
Registro de sesiones de terapia realizadas.

```sql
- id (PK)
- terapia_nino_id (FK -> terapias_nino)
- fecha
- asistio
- progreso
- colaboracion
- observaciones
- creado_por (FK -> personal)
```

#### `reposiciones`
Gestión de reposiciones de sesiones.

```sql
- id (PK)
- nino_id (FK -> ninos)
- terapia_id (FK -> terapias)
- fecha_original
- fecha_nueva
- motivo
- estado (PENDIENTE, APROBADA, RECHAZADA)
```

### Catálogos

#### `tipo_terapia`
- LENGUAJE - Terapia de Lenguaje
- CONDUCTUAL - Terapia Conductual
- OCUPACIONAL - Terapia Ocupacional
- FISICA - Terapia Física
- ABA - Análisis Conductual Aplicado
- SENSORIAL - Integración Sensorial
- COGNITIVA - Terapia Cognitiva
- SOCIAL - Habilidades Sociales
- PSICOLOGICA - Apoyo Psicológico
- ACADEMICA - Apoyo Académico

#### `prioridad`
- URGENTE - Urgente
- ALTA - Alta
- MEDIA - Media
- BAJA - Baja

---

## 🔌 API Endpoints

### Base URL: `/api/v1/terapias`

### 1️⃣ **CRUD de Terapias**

#### `GET /`
Lista todas las terapias registradas.

**Response:**
```json
[
  {
    "id_terapia": 1,
    "nombre": "Terapia de Lenguaje Inicial",
    "descripcion": "Desarrollo de habilidades comunicativas básicas",
    "tipo_id": 1,
    "duracion_minutos": 45,
    "objetivo_general": "Mejorar la comunicación verbal y no verbal",
    "estado": "ACTIVA"
  }
]
```

#### `GET /{terapia_id}`
Obtiene una terapia específica por ID.

#### `POST /`
Crea una nueva terapia.

**Request Body:**
```json
{
  "nombre": "Terapia de Lenguaje Inicial",
  "descripcion": "Desarrollo de habilidades comunicativas básicas",
  "tipo_id": 1,
  "duracion_minutos": 45,
  "objetivo_general": "Mejorar la comunicación verbal y no verbal"
}
```

#### `PUT /{terapia_id}`
Actualiza una terapia existente.

**Request Body:**
```json
{
  "nombre": "Terapia de Lenguaje Avanzado",
  "descripcion": "Nueva descripción",
  "duracion_minutos": 60
}
```

#### `PATCH /{terapia_id}/estado`
Cambia el estado de una terapia (activo/inactivo).

**Response:**
```json
{
  "id_terapia": 1,
  "nombre": "Terapia de Lenguaje Inicial",
  "estado": "INACTIVA"
}
```

#### `DELETE /{terapia_id}`
Elimina (inactiva) una terapia.

---

### 2️⃣ **Asignación de Personal**

#### `POST /asignar`
Asigna un terapeuta a una terapia.

**Request Body:**
```json
{
  "id_personal": 5,
  "id_terapia": 2
}
```

**Response:**
```json
{
  "id_asignacion": 10,
  "id_personal": 5,
  "id_terapia": 2,
  "activo": 1
}
```

#### `GET /personal-asignado`
Lista todo el personal con sus terapias asignadas.

**Response:**
```json
[
  {
    "id_personal": 5,
    "nombre_completo": "María González López",
    "terapia": "Terapia de Lenguaje Inicial",
    "id_terapia": 2
  }
]
```

---

### 3️⃣ **Catálogos**

#### `GET /catalogos/tipos`
Obtiene el catálogo de tipos de terapia.

**Response:**
```json
[
  {
    "id": 1,
    "codigo": "LENGUAJE",
    "nombre": "Terapia de Lenguaje"
  }
]
```

---

### 4️⃣ **Personal Disponible**

#### `GET /personal/sin-terapia`
Lista personal que no tiene terapia asignada.

**Base URL:** `/api/v1/personal/sin-terapia`

**Response:**
```json
[
  {
    "id_personal": 8,
    "nombre_completo": "Juan Pérez Martínez",
    "especialidad": "Terapia Conductual"
  }
]
```

---

## 📦 Modelos (SQLAlchemy)

### `Terapia`
```python
class Terapia(Base):
    __tablename__ = "terapias"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    tipo_id = Column(SmallInteger, ForeignKey("tipo_terapia.id"))
    duracion_minutos = Column(Integer, default=60)
    objetivo_general = Column(Text)
    activo = Column(SmallInteger, default=1)
    
    # Relaciones
    tipo_terapia = relationship("TipoTerapia")
    personal_asignado = relationship("TerapiaPersonal")
    terapias_nino = relationship("TerapiaNino")
```

### `TerapiaPersonal`
```python
class TerapiaPersonal(Base):
    __tablename__ = "terapias_personal"
    
    id = Column(Integer, primary_key=True)
    terapia_id = Column(Integer, ForeignKey("terapias.id"))
    personal_id = Column(Integer, ForeignKey("personal.id"))
    activo = Column(SmallInteger, default=1)
    
    terapia = relationship("Terapia")
    personal = relationship("Personal")
```

---

## 📝 Schemas (Pydantic)

### `TerapiaCreate`
```python
class TerapiaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo_id: int = 1
    duracion_minutos: int = 60
    objetivo_general: Optional[str] = None
```

### `TerapiaRead`
```python
class TerapiaRead(BaseModel):
    id_terapia: int
    nombre: str
    descripcion: Optional[str]
    tipo_id: int
    duracion_minutos: int
    objetivo_general: Optional[str]
    estado: str  # ACTIVA o INACTIVA
```

### `TerapiaPersonalCreate`
```python
class TerapiaPersonalCreate(BaseModel):
    id_personal: int
    id_terapia: int
```

---

## 🚀 Instalación y Configuración

### 1. Inicializar Catálogos

**Opción A: Usando SQL**
```bash
mysql -u root -p autismo_mochis_ia < backend/scripts/init_catalogos_terapias.sql
```

**Opción B: Usando Python**
```bash
cd backend
python scripts/init_catalogos_terapias.py
```

### 2. Verificar Instalación

```bash
# Iniciar servidor
cd backend
uvicorn app.main:app --reload

# Verificar endpoints
# Abrir: http://localhost:8000/docs
```

---

## 🧪 Pruebas con cURL

### Crear una terapia
```bash
curl -X POST "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Terapia de Lenguaje Inicial",
    "descripcion": "Para niños con TEA",
    "tipo_id": 1,
    "duracion_minutos": 45,
    "objetivo_general": "Mejorar comunicación"
  }'
```

### Listar terapias
```bash
curl -X GET "http://localhost:8000/api/v1/terapias" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Asignar terapeuta
```bash
curl -X POST "http://localhost:8000/api/v1/terapias/asignar" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id_personal": 5,
    "id_terapia": 2
  }'
```

### Personal sin terapia
```bash
curl -X GET "http://localhost:8000/api/v1/personal/sin-terapia" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 📊 Flujo de Trabajo

1. **Crear Terapia**
   - El coordinador crea una nueva terapia
   - Se asigna un tipo y duración

2. **Asignar Personal**
   - Se consulta personal disponible
   - Se asigna terapeuta a la terapia

3. **Asignar a Niño**
   - Se asigna terapia a un niño
   - Se define prioridad y frecuencia
   - Se asigna terapeuta específico

4. **Registrar Sesiones**
   - El terapeuta registra cada sesión
   - Se captura progreso y observaciones

5. **Gestionar Reposiciones**
   - Se solicitan reposiciones cuando necesario
   - Se aprueban o rechazan

---

## ✅ Características Implementadas

- ✅ CRUD completo de terapias
- ✅ Asignación de personal a terapias
- ✅ Catálogos de tipos de terapia
- ✅ Catálogos de prioridades
- ✅ Cambio de estado (activo/inactivo)
- ✅ Consulta de personal disponible
- ✅ Consulta de personal asignado
- ✅ Modelos de sesiones
- ✅ Modelos de reposiciones
- ✅ Validaciones de negocio
- ✅ Documentación completa
- ✅ Scripts de inicialización

---

## 🔐 Seguridad

Todos los endpoints requieren autenticación mediante Bearer Token:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## 📄 Archivos Creados

```
backend/
├── app/
│   ├── models/
│   │   └── terapia.py ✅ NUEVO
│   ├── schemas/
│   │   └── terapia.py ✅ NUEVO
│   └── api/
│       └── v1/
│           └── endpoints/
│               └── terapias.py ✅ NUEVO
└── scripts/
    ├── init_catalogos_terapias.py ✅ NUEVO
    └── init_catalogos_terapias.sql ✅ NUEVO
```

---

## 🎯 Integración con Frontend

El frontend en Angular ya está preparado para consumir estos endpoints:

- `TerapiasComponent` → `/coordinador/terapias`
- `TherapyService` → Servicio HTTP para terapias

**Endpoints utilizados por el frontend:**
- `GET /api/v1/terapias` → Lista terapias
- `POST /api/v1/terapias` → Crea terapia
- `PUT /api/v1/terapias/{id}` → Actualiza terapia
- `PATCH /api/v1/terapias/{id}/estado` → Cambia estado
- `POST /api/v1/terapias/asignar` → Asigna personal
- `GET /api/v1/personal/sin-terapia` → Personal disponible
- `GET /api/v1/terapias/personal-asignado` → Personal asignado

---

## 🐛 Troubleshooting

### Error: "Tipo de terapia no válido"
**Solución:** Ejecutar script de inicialización de catálogos

### Error: "Personal ya está asignado a esta terapia"
**Solución:** Verificar que no exista asignación activa previa

### Error: "Personal no encontrado"
**Solución:** Verificar que el ID de personal existe y está activo

---

## 📚 Próximos Pasos

1. Implementar endpoints de `TerapiaNino` (asignación de terapias a niños)
2. Implementar endpoints de `Sesiones`
3. Implementar endpoints de `Reposiciones`
4. Agregar filtros avanzados en listados
5. Implementar sistema de reportes
6. Agregar notificaciones automáticas

---

## 👨‍💻 Desarrollado por
Sistema de Gestión de Centro de Atención de Autismo
Versión 2.0

**Fecha:** Diciembre 2025

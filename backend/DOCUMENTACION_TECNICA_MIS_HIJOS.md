# 🏗️ DOCUMENTACIÓN TÉCNICA: BACKEND MIS HIJOS

## 📋 Índice

1. [Arquitectura General](#arquitectura-general)
2. [Modelos de Base de Datos](#modelos-de-base-de-datos)
3. [Servicios y Lógica de Negocio](#servicios-y-lógica-de-negocio)
4. [Esquemas (DTOs)](#esquemas-dtos)
5. [Endpoints API](#endpoints-api)
6. [Integración](#integración)
7. [Seguridad](#seguridad)

---

## 🏗️ Arquitectura General

### Estructura de Capas

```
┌─────────────────────────────────────────────────────┐
│         Frontend (Angular 17 - Standalone)          │
│              (mis-hijos.component)                  │
└────────────────────┬────────────────────────────────┘
                     │
                     ↓ HTTP Request (GET /api/v1/padres/mis-hijos)
                     │
┌─────────────────────────────────────────────────────┐
│            FastAPI Router (mis_hijos.py)            │
│  - GET /mis-hijos                                   │
│  - GET /mis-hijos/{nino_id}                         │
│  - PUT /mis-hijos/{nino_id}/medicamentos/.../visto  │
└─────────────┬──────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────┐
│       Service Layer (padres_mis_hijos_service)      │
│  - obtener_mis_hijos()                              │
│  - obtener_hijo_detalle()                           │
│  - obtener_medicamentos_hijo()                      │
│  - obtener_alergias_hijo()                          │
│  - marcar_medicamento_como_visto()                  │
└─────────────┬──────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────┐
│         Database Models (SQLAlchemy ORM)            │
│  - Nino                                             │
│  - Medicamento                                      │
│  - Alergia                                          │
│  - Tutor                                            │
└─────────────┬──────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────┐
│      MySQL Database (medicamentos, alergias)        │
└─────────────────────────────────────────────────────┘
```

---

## 💾 Modelos de Base de Datos

### 1. Modelo: Medicamento

**Archivo:** `app/models/medicamentos.py`

```python
class Medicamento(Base):
    __tablename__ = "medicamentos"

    id: int (PK)
    nino_id: int (FK → ninos.id)
    nombre: str (200)
    dosis: str (100)
    frecuencia: str (100)
    razon: str (255)
    fecha_inicio: date
    fecha_fin: date (nullable)
    activo: bool (default=True)
    novedadReciente: bool (default=False)
    fecha_actualizacion: datetime (auto-updated)
    actualizado_por: str (100, nullable)
    notas: text (nullable)
    fecha_creacion: datetime (auto)
```

**Relaciones:**

```
Medicamento.nino ← Nino.medicamentos (One-to-Many)
```

**Indices:**

```sql
INDEX idx_nino_id (nino_id)
INDEX idx_activo (activo)
INDEX idx_medicamentos_nino_activo (nino_id, activo)
```

### 2. Modelo: Alergia

**Archivo:** `app/models/medicamentos.py`

```python
class Alergia(Base):
    __tablename__ = "alergias"

    id: int (PK)
    nino_id: int (FK → ninos.id)
    nombre: str (200)
    severidad: enum ('leve', 'moderada', 'severa')
    reaccion: text
    tratamiento: text (nullable)
    fecha_registro: datetime (auto)
```

**Relaciones:**

```
Alergia.nino ← Nino.alergias (One-to-Many)
```

### 3. Actualización Modelo: Nino

El modelo `Nino` se actualizó para incluir:

```python
medicamentos = relationship("Medicamento",
                           back_populates="nino",
                           cascade="all, delete-orphan")
alergias = relationship("Alergia",
                       back_populates="nino",
                       cascade="all, delete-orphan")
```

---

## 🔧 Servicios y Lógica de Negocio

### Archivo: `app/services/padres_mis_hijos_service.py`

#### Función 1: `calcular_edad(fecha_nacimiento: date) → int`

```python
def calcular_edad(fecha_nacimiento: date) -> int:
    """
    Calcula la edad exacta en años.

    Args:
        fecha_nacimiento: fecha de nacimiento del niño

    Returns:
        edad en años (int)
    """
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year

    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad
```

#### Función 2: `obtener_alergias_hijo(nino_id: int, db: Session) → List[AlergiaResponse]`

```python
def obtener_alergias_hijo(nino_id: int, db: Session) -> List[AlergiaResponse]:
    """
    Obtiene todas las alergias de un niño.

    Query:
        SELECT * FROM alergias WHERE nino_id = {nino_id}

    Returns:
        Lista de AlergiaResponse con:
        - id, nombre, severidad, reaccion
    """
```

#### Función 3: `obtener_medicamentos_hijo(nino_id: int, db: Session) → List[MedicamentoResponse]`

```python
def obtener_medicamentos_hijo(nino_id: int, db: Session) -> List[MedicamentoResponse]:
    """
    Obtiene todos los medicamentos de un niño.

    Query:
        SELECT * FROM medicamentos
        WHERE nino_id = {nino_id}
        ORDER BY activo DESC, fecha_actualizacion DESC

    Returns:
        Lista de MedicamentoResponse ordenada por:
        1. Medicamentos activos primero
        2. Más recientes primero
    """
```

#### Función 4: `obtener_hijo_detalle(nino: Nino, db: Session) → HijoResponse`

```python
def obtener_hijo_detalle(nino: Nino, db: Session) -> HijoResponse:
    """
    Construye respuesta completa de un hijo.

    Calcula automáticamente:
    - edad: date.today() - fecha_nacimiento
    - cuatrimestre: (meses desde registro / 4) + 1
    - fecha_ingreso: nino.fecha_registro

    Obtiene:
    - alergias: llamada a obtener_alergias_hijo()
    - medicamentos: llamada a obtener_medicamentos_hijo()
    - foto: nino.archivos.foto_url

    Cuenta:
    - novedades: medicamentos con novedadReciente=True
    """
```

#### Función 5: `obtener_mis_hijos(tutor_id: int, db: Session) → MisHijosApiResponse`

```python
def obtener_mis_hijos(tutor_id: int, db: Session) -> MisHijosApiResponse:
    """
    Obtiene todos los hijos activos del tutor.

    Verificaciones:
    1. Busca Tutor por usuario_id
    2. Si no existe → error

    Query:
        SELECT * FROM ninos
        WHERE tutor_id = {tutor.id}
        AND estado = 'ACTIVO'
        ORDER BY nombre

    Respuesta:
        MisHijosApiResponse con:
        - exito: bool
        - datos: MisHijosPageResponse con lista de HijoResponse
        - mensaje: string descriptivo
    """
```

#### Función 6: `marcar_medicamento_como_visto(...) → MisHijosApiResponse`

```python
def marcar_medicamento_como_visto(
    tutor_id: int,
    nino_id: int,
    medicamento_id: int,
    db: Session
) -> MisHijosApiResponse:
    """
    Marca un medicamento como visto (quita novedadReciente).

    Verificaciones:
    1. Tutor existe
    2. Medicamento existe y pertenece al niño

    Update:
        UPDATE medicamentos
        SET novedadReciente = FALSE
        WHERE id = {medicamento_id}

    Commit: Automático
    """
```

---

## 📦 Esquemas (DTOs)

### Archivo: `app/schemas/padres_mis_hijos.py`

#### Schema 1: AlergiaResponse

```python
class AlergiaResponse(BaseModel):
    id: int
    nombre: str
    severidad: str  # 'leve', 'moderada', 'severa'
    reaccion: str
```

#### Schema 2: MedicamentoResponse

```python
class MedicamentoResponse(BaseModel):
    id: int
    nombre: str
    dosis: str
    frecuencia: str
    razon: str
    fechaInicio: date
    fechaFin: Optional[date]
    activo: bool
    novedadReciente: bool = False
    fechaActualizacion: Optional[datetime]
```

**Mapeos:**

- `fecha_inicio` → `fechaInicio` (snake_case → camelCase)
- `fecha_fin` → `fechaFin`
- `fecha_actualizacion` → `fechaActualizacion`

#### Schema 3: HijoResponse

```python
class HijoResponse(BaseModel):
    id: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: Optional[str]
    foto: Optional[str]
    fechaNacimiento: date
    edad: Optional[int]
    diagnostico: Optional[str]
    cuatrimestre: Optional[int]
    fechaIngreso: Optional[date]
    alergias: List[AlergiaResponse]
    medicamentos: List[MedicamentoResponse]
    visto: bool = False
    novedades: int = 0
```

#### Schema 4: MisHijosPageResponse

```python
class MisHijosPageResponse(BaseModel):
    hijos: List[HijoResponse] = []
```

#### Schema 5: MisHijosApiResponse

```python
class MisHijosApiResponse(BaseModel):
    exito: bool
    datos: Optional[MisHijosPageResponse]
    error: Optional[str]
    mensaje: Optional[str]
```

---

## 🔌 Endpoints API

### Endpoint 1: GET /padres/mis-hijos

**Ruta:** `app/api/v1/padres/mis_hijos.py`

```python
@router.get("/mis-hijos", response_model=MisHijosApiResponse)
def get_mis_hijos(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
```

**Parámetros:**

- `db`: Session (inyectado)
- `current_user`: Usuario actual padre (inyectado)

**Respuesta:**

```json
{
  "exito": true,
  "datos": {
    "hijos": [...]
  },
  "mensaje": "Se encontraron N hijo(s)"
}
```

**Códigos HTTP:**

- `200` - OK
- `401` - No autenticado
- `403` - No es padre
- `500` - Error interno

### Endpoint 2: GET /padres/mis-hijos/{nino_id}

**Ruta:** `app/api/v1/padres/mis_hijos.py`

```python
@router.get("/mis-hijos/{nino_id}", response_model=MisHijosApiResponse)
def get_hijo_detalle(
    nino_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
```

**Parámetros:**

- `nino_id`: int (path parameter)
- `db`: Session
- `current_user`: Usuario actual

**Respuesta:**

```json
{
  "exito": true,
  "datos": {
    "hijos": [
      {
        "id": 1,
        "nombre": "Juan",
        ...
      }
    ]
  }
}
```

### Endpoint 3: PUT /padres/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto

**Ruta:** `app/api/v1/padres/mis_hijos.py`

```python
@router.put("/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto")
def marcar_medicamento_visto(
    nino_id: int = Path(...),
    medicamento_id: int = Path(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_padre),
):
```

**Parámetros:**

- `nino_id`: int
- `medicamento_id`: int
- `db`: Session
- `current_user`: Usuario actual

**Respuesta:**

```json
{
  "exito": true,
  "mensaje": "Medicamento marcado como visto"
}
```

---

## 🔗 Integración

### 1. Incluir Modelos

**Archivo:** `app/models/__init__.py`

```python
from app.models.medicamentos import Medicamento, Alergia

__all__ = [
    "Medicamento",
    "Alergia",
    # ... otros modelos
]
```

### 2. Incluir Router

**Archivo:** `app/api/v1/api.py`

```python
from app.api.v1.padres import padres_router

api_router.include_router(padres_router, tags=["Padres"])
```

### 3. Base de Datos

**Migración:**

```bash
python migracion_mis_hijos.py
```

o

```sql
-- Ejecutar en phpMyAdmin
source backend/sql/migracion_medicamentos_alergias.sql;
```

---

## 🔐 Seguridad

### 1. Autenticación

```python
current_user = Depends(get_current_padre)
```

Verifica:

- Token JWT válido
- Usuario existe
- Usuario tiene rol de padre (role_id = 4)

### 2. Autorización

El servicio verifica:

```python
tutor = db.query(Tutor).filter(Tutor.usuario_id == tutor_id).first()
if not tutor:
    return error
```

### 3. Validación de Datos

Los esquemas Pydantic validan:

- Tipos de datos
- Valores requeridos
- Formatos correctos (date, datetime)

### 4. SQL Injection Prevention

```python
# ✅ SEGURO - Usa parámetros
nino = db.query(Nino).filter(Nino.id == nino_id).first()

# ❌ INSEGURO - Concatenación de strings
nino = db.query(Nino).filter(f"id = {nino_id}").first()
```

---

## 📊 Flujo de Datos Completo

### Request → Response

```
1. Frontend (Angular)
   GET /api/v1/padres/mis-hijos
   Header: Authorization: Bearer {token_jwt}

2. FastAPI Router
   @get_mis_hijos(db, current_user)
   → Verifica autenticación ✓

3. Service Layer
   obtener_mis_hijos(user_id, db)
   → Query: SELECT * FROM ninos WHERE tutor_id AND estado='ACTIVO'
   → Para cada nino: obtener_hijo_detalle()

4. Database
   → SELECT FROM ninos
   → SELECT FROM medicamentos WHERE nino_id
   → SELECT FROM alergias WHERE nino_id

5. Mapeo a DTOs
   → Nino → HijoResponse
   → Medicamento → MedicamentoResponse
   → Alergia → AlergiaResponse

6. Response
   {
     "exito": true,
     "datos": {
       "hijos": [HijoResponse, ...]
     }
   }

7. Frontend Renderiza
   - Listado de hijos
   - Información clínica
   - Medicamentos
   - Alergias
```

---

## 🎯 Validaciones

### En Request

- Token JWT válido
- Usuario es padre
- nino_id existe
- nino_id pertenece al padre

### En Response

- Todos los campos requeridos completos
- Tipos de datos correctos
- Fechas válidas

### En Base de Datos

- Foreign Keys correctas
- Cascadas delete configuradas
- Índices para rendimiento

---

**Versión:** 1.0
**Fecha:** 2026-01-12
**Estado:** ✅ COMPLETO

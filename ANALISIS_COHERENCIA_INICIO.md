# 🔍 ANÁLISIS DE COHERENCIA - INTERFACES INICIO vs BD

## Estado Actual de la BD (Backend)

### Modelo: `Nino` (app/models/nino.py)

```python
- id (Integer)
- nombre (String)
- apellido_paterno (String)
- apellido_materno (String)
- fecha_nacimiento (Date)
- sexo (Enum: M, F, O)
- curp (String)
- tutor_id (ForeignKey)
- estado (Enum: ACTIVO, INACTIVO)
- fecha_registro (DateTime)
- perfil_contenido (JSON)
- Relaciones: direccion, diagnostico, info_emocional, archivos, terapias
```

### Modelo: `TerapiaNino` (app/models/terapia.py)

```python
- id (Integer)
- nino_id (ForeignKey → Nino)
- terapia_id (ForeignKey → Terapia)
- terapeuta_id (ForeignKey → Personal)
- prioridad_id (ForeignKey → Prioridad)
- Estado, fechas, etc.
```

### Schema Backend: `InicioPadreResponse` (schemas/padres_inicio.py)

```python
✅ hijo_id (UUID)
✅ hijo_nombre (str)
✅ proxima_sesion (Optional[ProximaSesionSchema])
✅ ultimo_avance (Optional[UltimoAvanceSchema])
✅ pagos_pendientes (float)
✅ documento_nuevo (bool)
✅ ultima_observacion (Optional[ObservacionSchema])
```

---

## ❌ PROBLEMAS ENCONTRADOS

### 1. **ID del Hijo: Inconsistencia de Tipos**

- **BD**: `id` es `Integer`
- **Backend Schema**: `hijo_id` es `UUID`
- **Frontend Interface (worktree)**: `id: string`
- **Frontend Actual**: `hijo_id: string`

**SOLUCIÓN**: Usar `Integer` o `string` de forma consistente.

---

### 2. **Nombre del Hijo: Incompleto**

- **BD**: Tiene `nombre`, `apellido_paterno`, `apellido_materno`
- **Backend Schema**: Solo devuelve `hijo_nombre` (string)
- **Frontend**: Necesita nombre completo

**SOLUCIÓN**: Ajustar interface para incluir apellidos o nombre concatenado.

---

### 3. **Próxima Sesión: Falta de Información**

- **Backend Schema devuelve**: `fecha`, `hora`, `terapeuta`, `tipo`
- **Frontend interface (worktree) espera**: `id`, `fecha`, `hora`, `tipoTerapia`, `terapeuta`, `location`, `estado`

**SOLUCIÓN**: Agregar campos `id` y `estado` al schema backend.

---

### 4. **Último Avance: Diferencia de Estructura**

- **Backend Schema**: `descripcion`, `porcentaje`
- **Frontend (worktree)**: `titulo`, `descripcion`, `fechaRegistro`, `porcentajeProgreso`, `objetivo`

**SOLUCIÓN**: Expandir el response del backend para incluir más contexto.

---

### 5. **Pagos Pendientes: Tipo de Dato**

- **Backend Schema**: `float` (suma total)
- **Frontend (worktree)**: Array de objetos `PagosPendientes[]`

**SOLUCIÓN**: Cambiar response para devolver array con detalles de pagos.

---

### 6. **Documento Nuevo: Información Incompleta**

- **Backend Schema**: Boolean simple
- **Frontend (worktree)**: Array de `DocumentoNuevo` con detalles

**SOLUCIÓN**: Agregar array con información completa de documentos nuevos.

---

### 7. **Última Observación: Nombre del Campo**

- **Backend Schema**: `resumen` (string)
- **Frontend (worktree)**: `contenido` (string)

**SOLUCIÓN**: Unificar nombres de campos.

---

## 📊 MATRIZ DE COHERENCIA

| Campo              | BD      | Backend Schema | Frontend (Worktree) | Frontend Actual | ✅/❌ |
| ------------------ | ------- | -------------- | ------------------- | --------------- | ----- |
| hijo_id            | Integer | UUID           | string              | string          | ❌    |
| hijo_nombre        | string  | string         | string              | string          | ✅    |
| hijo_apellidos     | string  | ✗              | string              | ✗               | ❌    |
| proxima_sesion     | ✓       | ✓              | ✓                   | ✓               | ⚠️    |
| ultimo_avance      | ✓       | ✓              | ✓                   | ✓               | ⚠️    |
| pagos_pendientes   | ✓       | float          | array               | ?               | ❌    |
| documento_nuevo    | ✓       | bool           | array               | ?               | ❌    |
| ultima_observacion | ✓       | ✓              | ✓                   | ✓               | ⚠️    |

---

## 🔧 RECOMENDACIONES DE AJUSTE

### Opción 1: Ajustar Frontend (RECOMENDADO)

Adaptar las interfaces del worktree para que coincidan con lo que devuelve el backend.

### Opción 2: Ajustar Backend

Ampliar el schema del backend para devolver más campos.

### Opción 3: Ambos

Hacer cambios coordinados en frontend y backend.

---

## ✨ PROPUESTA DE SOLUCIÓN UNIFICADA

### Interface TypeScript Corregida:

```typescript
export interface ProxSesion {
  id: string;
  fecha: string; // O Date - revisar consistencia
  hora: string;
  tipoTerapia: string;
  terapeuta: string;
  location?: string;
  estado: 'confirmada' | 'pendiente' | 'cancelada';
}

export interface UltimoAvance {
  id: string;
  titulo: string;
  descripcion: string;
  fechaRegistro: string; // Coincide con backend
  porcentajeProgreso: number;
  objetivo: string;
}

export interface PagoPendiente {
  id: string;
  descripcion: string;
  monto: number;
  fechaVencimiento: string;
  estado: 'pagado' | 'pendiente' | 'vencido' | 'parcial';
}

export interface DocumentoNuevo {
  id: string;
  nombre: string;
  tipo: 'acuerdo' | 'reporte' | 'medico' | 'medicamento' | 'otro';
  fechaSubida: string;
  visto: boolean;
  urlPdf?: string;
}

export interface UltimaObservacion {
  id: string;
  contenido: string; // O "resumen" como en backend
  terapeuta: string;
  fecha: string;
  tipoTerapia: string;
}

export interface InicioPage {
  saludo: string;
  hora: string;
  hijoSeleccionado: {
    id: number | string;
    nombre: string;
    apellidoPaterno?: string;
    apellidoMaterno?: string;
  };
  hijosDisponibles: Array<{
    id: number | string;
    nombre: string;
  }>;
  tarjetas: {
    proxSesion: ProxSesion | null;
    ultimoAvance: UltimoAvance | null;
    pagosPendientes: PagoPendiente[];
    documentosNuevos: DocumentoNuevo[];
    ultimaObservacion: UltimaObservacion | null;
  };
  cargando: boolean;
}
```

### Schema Backend a Actualizar:

```python
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class ProximaSesionSchema(BaseModel):
    id: int  # AGREGAR
    fecha: date
    hora: str
    terapeuta: str
    tipo: str
    estado: str = "confirmada"  # AGREGAR

class UltimoAvanceSchema(BaseModel):
    id: int  # AGREGAR
    titulo: str  # RENOMBRAR de description si es necesario
    descripcion: str  # EXPANDIR
    fecha: date
    porcentaje: int

class ObservacionSchema(BaseModel):
    id: int  # AGREGAR
    fecha: datetime
    terapeuta: str
    resumen: str

class PagoPendienteSchema(BaseModel):  # NUEVO
    id: int
    descripcion: str
    monto: float
    fecha_vencimiento: date
    estado: str

class DocumentoNuevoSchema(BaseModel):  # NUEVO
    id: int
    nombre: str
    tipo: str
    fecha_subida: datetime
    visto: bool
    url_pdf: Optional[str] = None

class InicioPadreResponse(BaseModel):
    hijo_id: int  # CAMBIAR a int
    hijo_nombre: str
    apellido_paterno: Optional[str]  # AGREGAR
    apellido_materno: Optional[str]   # AGREGAR

    proxima_sesion: Optional[ProximaSesionSchema]
    ultimo_avance: Optional[UltimoAvanceSchema]
    pagos_pendientes: List[PagoPendienteSchema]  # CAMBIAR a list
    documentos_nuevos: List[DocumentoNuevoSchema]  # CAMBIAR a list
    ultima_observacion: Optional[ObservacionSchema]
```

---

## 🎯 PRÓXIMOS PASOS

1. **[ ] Revisar Backend** - Confirmar qué endpoints existen actualmente
2. **[ ] Actualizar Schema Backend** - Expandir respuesta con campos faltantes
3. **[ ] Actualizar Interfaces Frontend** - Usar las nuevas interfaces unificadas
4. **[ ] Actualizar Componente** - Asegurar compatibilidad
5. **[ ] Tests** - Validar que todo funciona correctamente

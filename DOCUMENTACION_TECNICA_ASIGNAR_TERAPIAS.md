# Documentación Técnica - Módulo Asignar Terapias

## Arquitectura General

```
Frontend (Angular)
├── AsignarTerapiasComponent
│   ├── TypeScript (Lógica)
│   ├── HTML (Interfaz)
│   └── SCSS (Estilos)
└── CitasCalendarioService (Integración API)
         ↓
Backend (FastAPI)
├── /api/v1/citas-calendario/
│   ├── POST / (Crear cita)
│   ├── GET /calendario (Obtener citas)
│   └── PUT /{id}/reprogramar (Actualizar)
└── google_calendar_service.py (Sincronización)
         ↓
Google Calendar API
└── Service Account
```

## Componente Frontend

### Ubicación
- Archivo TypeScript: `src/app/coordinador/asignar-terapias/asignar-terapias.component.ts`
- Template HTML: `src/app/coordinador/asignar-terapias/asignar-terapias.component.html`
- Estilos SCSS: `src/app/coordinador/asignar-terapias/asignar-terapias.component.scss`

### Interfaces TypeScript

```typescript
interface Nino {
  id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
}

interface Terapeuta {
  id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  especialidad?: string;
}

interface Terapia {
  id: number;
  nombre: string;
  duracion_minutos: number;
  descripcion?: string;
}

interface AsignacionTerapia {
  nino: Nino | null;
  terapeuta: Terapeuta | null;
  terapia: Terapia | null;
  fechaInicio: string;
  diasSemana: number[]; // 1=Lunes, 2=Martes, etc.
  horaInicio: string;
  horaFin: string;
  cantidadSemanas: number;
  sincronizarGoogle: boolean;
}
```

### Propiedades del Componente

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `ninos` | `Nino[]` | Catálogo de niños disponibles |
| `terapeutas` | `Terapeuta[]` | Catálogo de terapeutas |
| `terapias` | `Terapia[]` | Catálogo de terapias |
| `asignacion` | `AsignacionTerapia` | Formulario actual |
| `opcionesDias` | `any[]` | Opciones de días (Lunes-Sábado) |
| `horasPredefinidas` | `string[]` | Horas disponibles (7am-7pm) |
| `cargando` | `boolean` | Estado de carga general |
| `citasGeneradas` | `any[]` | Citas presualizadas |
| `mostrarPrevisualizacion` | `boolean` | Mostrar modal de preview |

### Métodos Principales

#### `cargarCatalogos()`
Carga los catálogos de niños, terapeutas y terapias desde el backend.

```typescript
cargarCatalogos(): void {
  this.cargarNinos();        // GET /ninos
  this.cargarTerapeutas();   // GET /personal
  this.cargarTerapias();     // GET /terapias
}
```

#### `previsualizarCitas()`
Genera lista de citas a crear sin guardarlas. Abre modal de previsualización.

```typescript
previsualizarCitas(): void {
  if (!this.validarAsignacion()) return;
  
  this.citasGeneradas = 
    this.citasCalendarioService.generarFechasRecurrentes(
      fechaInicio,
      cantidadSemanas,
      diasSemana,
      horaInicio,
      horaFin
    );
  
  this.mostrarPrevisualizacion = true;
}
```

#### `asignarTerapias()`
Crea todas las citas en la BD y sincroniza con Google Calendar.

```typescript
asignarTerapias(): void {
  if (!this.validarAsignacion()) return;
  
  // Generar citas
  const citas: CitaCalendarioCreate[] = [...];
  
  // Crear secuencialmente
  this.crearCitasSecuencial(citas, 0, 0, 0);
}
```

#### `crearCitasSecuencial(citas, indice, creadas, errores)`
Crea citas una por una para evitar problemas de concurrencia con Google Calendar.

```typescript
private crearCitasSecuencial(
  citas: CitaCalendarioCreate[],
  indice: number,
  creadas: number,
  errores: number
): void {
  if (indice >= citas.length) {
    // Terminó - mostrar resultado
    this.mostrarMensajeResultado(creadas, errores);
    return;
  }
  
  // Crear cita actual
  this.citasCalendarioService.crearCita(citas[indice])
    .subscribe({
      next: () => {
        this.crearCitasSecuencial(citas, indice + 1, creadas + 1, errores);
      },
      error: () => {
        this.crearCitasSecuencial(citas, indice + 1, creadas, errores + 1);
      }
    });
}
```

#### `validarAsignacion()`
Valida que todos los campos estén completos.

```typescript
validarAsignacion(): boolean {
  // Validaciones:
  // - Niño seleccionado
  // - Terapeuta seleccionado
  // - Terapia seleccionada
  // - Días seleccionados (mín 1)
  // - Fecha de inicio válida
  // - Hora inicio < Hora fin
}
```

#### `onDiaChange(dia)`
Alterna selección de un día de la semana.

```typescript
onDiaChange(dia: any): void {
  dia.seleccionado = !dia.seleccionado;
  this.asignacion.diasSemana = 
    this.opcionesDias
      .filter(d => d.seleccionado)
      .map(d => d.valor);
}
```

#### `ajustarHoraFin(duracionMinutos)`
Calcula automáticamente hora de fin según duración de terapia.

```typescript
ajustarHoraFin(duracionMinutos: number): void {
  const [horas, minutos] = this.asignacion.horaInicio
    .split(':')
    .map(Number);
  
  const totalMinutos = horas * 60 + minutos + duracionMinutos;
  const nuevasHoras = Math.floor(totalMinutos / 60);
  const nuevosMinutos = totalMinutos % 60;
  
  this.asignacion.horaFin = 
    `${String(nuevasHoras).padStart(2, '0')}:
     ${String(nuevosMinutos).padStart(2, '0')}`;
}
```

## Servicio - CitasCalendarioService

### Ubicación
`src/app/service/citas-calendario.service.ts`

### Métodos Principales

#### `crearCita(cita: CitaCalendarioCreate)`
Crea una cita individual y la sincroniza con Google Calendar.

```typescript
crearCita(cita: CitaCalendarioCreate): Observable<CitaCalendarioResponse> {
  return this.http.post(`${baseUrl}/`, {
    ...cita,
    sincronizar_google_calendar: cita.sincronizar_google_calendar ?? true
  });
}
```

#### `generarFechasRecurrentes(...)`
Genera array de fechas/horas para citas recurrentes.

```typescript
generarFechasRecurrentes(
  fechaInicio: Date,
  cantidadSemanas: number,
  diasSemana: number[],      // 1=Lunes, 2=Martes, etc.
  horaInicio: string,
  horaFin: string
): { fecha: string; hora_inicio: string; hora_fin: string }[]
```

**Algoritmo:**
```
Para cada semana (0 a cantidadSemanas-1):
  Para cada dia en diasSemana:
    Calcular fecha = fechaInicio + (semana * 7) + (offset del día)
    Si fecha >= fechaInicio:
      Agregar a resultado
Retornar fechas ordenadas
```

#### `verificarDisponibilidad(...)`
Verifica si el terapeuta está disponible en un horario específico.

```typescript
verificarDisponibilidad(
  terapeutaId: number,
  fecha: string,
  horaInicio: string,
  horaFin: string
): Observable<{ disponible: boolean; conflictos: Cita[] }>
```

## Interfaz de Usuario (HTML/SCSS)

### Estructura HTML

```
.asignar-terapias-container
├── .medical-header (Encabezado profesional)
├── .alerts-container (Mensajes de éxito/error)
├── .form-container
│   ├── .form-card (Sección 1: Datos)
│   ├── .form-card (Sección 2: Horarios)
│   ├── .form-card (Sección 3: Sincronización)
│   └── .form-actions (Botones)
└── .modal-overlay
    └── .modal-content (Previsualización)
```

### Clases CSS Principales

| Clase | Propósito |
|-------|-----------|
| `.medical-header` | Encabezado con gradiente azul |
| `.form-card` | Tarjeta de formulario con sombra |
| `.form-group` | Grupo de formulario (label + input) |
| `.days-grid` | Grid de 6 días |
| `.day-button` | Botón de día (toggle) |
| `.btn btn-primary` | Botón primario (azul) |
| `.btn btn-secondary` | Botón secundario (gris) |
| `.modal-overlay` | Overlay oscuro con modal |
| `.alert alert-success` | Mensaje de éxito (verde) |
| `.alert alert-error` | Mensaje de error (rojo) |

### Tema de Colores

```scss
$primary-color: #0066CC;      // Azul médico
$secondary-color: #F5F5F5;    // Gris claro
$success-color: #00A86B;      // Verde
$error-color: #DC143C;        // Rojo
$text-primary: #1A1A1A;       // Negro
$text-secondary: #666666;     // Gris oscuro
```

### Responsive Design

- **Desktop (1024px+):** Grid de 2 columnas en formularios
- **Tablet (768px-1023px):** Grid de 1 columna
- **Mobile (< 768px):** Stack vertical, menos padding

## Flujo de Datos

### 1. Carga Inicial (ngOnInit)
```
Component → cargarCatalogos() 
  ├→ http.get(/ninos) → ninos[]
  ├→ http.get(/personal) → terapeutas[]
  └→ http.get(/terapias) → terapias[]
```

### 2. Previsualización
```
previsualizarCitas()
  ├→ validarAsignacion()
  ├→ CitasCalendarioService.generarFechasRecurrentes()
  └→ Mostrar modal con citasGeneradas[]
```

### 3. Creación de Citas
```
asignarTerapias()
  ├→ validarAsignacion()
  ├→ generarFechasRecurrentes()
  └→ crearCitasSecuencial(citas, 0, 0, 0)
       ├→ POST /citas-calendario/ (cita 1)
       │   ├→ Backend: Crear registro
       │   ├→ Backend: Sincronizar Google Calendar
       │   └→ Response: CitaCalendarioResponse
       ├→ POST /citas-calendario/ (cita 2)
       ├→ ... (más citas)
       └→ Mostrar resumen de creación
```

## Backend Integration

### Endpoint: POST /citas-calendario/

**Request:**
```json
{
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2024-12-20",
  "hora_inicio": "09:00:00",
  "hora_fin": "10:00:00",
  "estado_id": 1,
  "motivo": "Sesión de Terapia Ocupacional",
  "sincronizar_google_calendar": true
}
```

**Response:**
```json
{
  "id_cita": 42,
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2024-12-20",
  "hora_inicio": "09:00:00",
  "hora_fin": "10:00:00",
  "google_event_id": "abcd1234efgh5678",
  "google_calendar_link": "https://calendar.google.com/...",
  "sincronizado_calendar": true,
  "fecha_sincronizacion": "2024-12-16T17:30:45"
}
```

## Seguridad y Validaciones

### Frontend
- ✅ Validación de campos requeridos
- ✅ Validación de rangos (horas, semanas)
- ✅ Prevención de rutas futuras

### Backend
- ✅ Verificación de JWT (usuario autenticado)
- ✅ Verificación de rol (COORDINADOR/ADMIN)
- ✅ Verificación de disponibilidad del terapeuta
- ✅ Validación de datos con Pydantic

### Google Calendar
- ✅ Service Account autenticada
- ✅ Permisos para crear eventos
- ✅ Manejo de errores de sincronización

## Testing

### Casos a Verificar

1. **Carga de Catálogos**
   - Verificar que /ninos, /personal, /terapias retornan datos
   - Verificar que los selects se populan correctamente

2. **Previsualización**
   - Seleccionar datos y hacer clic en "Previsualizar"
   - Verificar que se muestren todas las citas esperadas
   - Verificar fechas y horarios

3. **Creación de Citas**
   - Crear 4 semanas de citas (3 días/semana = 12 citas)
   - Verificar que todas se crean exitosamente
   - Verificar que aparecen en módulo de Citas

4. **Sincronización Google**
   - Con sincronización ACTIVA: verificar que eventos aparecen en Google Calendar
   - Con sincronización INACTIVA: verificar que solo se crean en BD

5. **Validaciones**
   - Intentar crear sin seleccionar niño: debe mostrar error
   - Intentar crear con hora_fin <= hora_inicio: debe mostrar error
   - Intentar crear sin seleccionar días: debe mostrar error

## Performance

### Optimizaciones Implementadas

1. **Carga Secuencial de Citas**
   - Crea citas una por una para evitar sobrecargar servidor
   - Permite sincronización correcta con Google Calendar

2. **Previsualización sin Guardado**
   - No crea datos en BD hasta confirmación
   - Permite verificar antes de hacer cambios permanentes

3. **Caché de Catálogos**
   - Se cargan una sola vez al iniciar componente
   - No se recargan con cada cambio de formulario

4. **Lazy Loading de Rutas**
   - Componente se carga solo cuando se navega a él
   - No afecta el tiempo de inicio de la aplicación

## Troubleshooting Técnico

### Error: "Unexpected closing tag 'div'"
**Causa:** HTML con etiquetas mal balanceadas  
**Solución:** Verificar que cada `<div>` abierto tenga su cierre correspondiente

### Error: "citasCalendarioService is not defined"
**Causa:** Servicio no inyectado en constructor  
**Solución:** Agregar `CitasCalendarioService` a las dependencias

### Error: "No Google Calendar link"
**Causa:** Sincronización deshabilitada o Google Calendar no configurado  
**Solución:** Verificar configuración de Google en backend

### Error: "403 Forbidden"
**Causa:** Usuario no tiene rol COORDINADOR  
**Solución:** Verificar que usuario tenga rol correcto en BD

## Versión y Historial

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 16-12-2024 | Versión inicial - Interfaz profesional con Google Calendar |

## Referencias

- [Documentación de Angular Forms](https://angular.io/guide/reactive-forms)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Google Calendar API](https://developers.google.com/calendar)
- [SCSS Best Practices](https://sass-lang.com/guide)

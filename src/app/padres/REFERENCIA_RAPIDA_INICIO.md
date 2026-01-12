# 🎯 REFERENCIA RÁPIDA - INTERFACES PADRES ACTUALIZADAS

## ✨ Cambios Clave Realizados

### 1️⃣ IDs y Tipos de Datos

```typescript
// ✅ CORRECTO (Nuevo)
id: number; // Integer en BD
fecha: string; // ISO 8601: "2026-01-12T14:30:00"
monto: number; // Float en BD → number en TS

// ❌ INCORRECTO (Anterior)
id: string;
fecha: Date;
```

### 2️⃣ Estructura de INICIO

```typescript
// Vista: padres/inicio

interface InicioPage {
  saludo: string; // "Buenos días/tardes/noches"
  hora: string; // Hora actual
  hijoSeleccionado: HijoResumen; // Hijo actualmente seleccionado
  hijosDisponibles: HijoResumen[]; // Lista de hijos del padre
  tarjetas: TarjetaResumen; // Las 5 tarjetas principales
  cargando: boolean;
}

interface HijoResumen {
  id: number;
  nombre: string;
  apellidoPaterno?: string;
  apellidoMaterno?: string;
  foto?: string;
}

interface TarjetaResumen {
  proxSesion: ProxSesion | null;
  ultimoAvance: UltimoAvance | null;
  pagosPendientes: PagoPendiente[]; // Array, no number
  documentosNuevos: DocumentoNuevo[]; // Array, no boolean
  ultimaObservacion: UltimaObservacion | null;
}
```

### 3️⃣ Tarjetas Principales

#### 📅 Próxima Sesión

```typescript
interface ProxSesion {
  id: number;
  fecha: string; // "2026-01-15"
  hora: string; // "14:30"
  tipoTerapia: string; // "Terapia del Lenguaje"
  terapeuta: string; // "Dr. Juan García"
  location?: string; // Lugar opcional
  estado: 'confirmada' | 'pendiente' | 'cancelada' | 'realizada' | 'reprogramada';
}
```

#### 📊 Último Avance

```typescript
interface UltimoAvance {
  id: number;
  titulo: string; // "Mejora en pronunciación"
  descripcion: string; // Descripción detallada
  fechaRegistro: string; // "2026-01-10T10:00:00"
  porcentajeProgreso: number; // 0-100
  objetivo: string; // Objetivo asociado
}
```

#### 💳 Pagos Pendientes

```typescript
interface PagoPendiente {
  id: number;
  descripcion: string; // "Sesión enero 2026"
  monto: number; // 150000 (moneda: COP)
  fechaVencimiento: string; // "2026-01-31"
  estado: 'pagado' | 'pendiente' | 'vencido' | 'parcial';
}
```

#### 📄 Documento Nuevo

```typescript
interface DocumentoNuevo {
  id: number;
  nombre: string; // "Reporte de Progreso"
  tipo: 'acuerdo' | 'reporte' | 'medico' | 'medicamento' | 'otro';
  fechaSubida: string; // "2026-01-12"
  visto: boolean;
  urlPdf?: string; // URL para descargar
}
```

#### 📝 Última Observación

```typescript
interface UltimaObservacion {
  id: number;
  contenido: string; // "El niño mostró mejora..."
  terapeuta: string; // Nombre del terapeuta
  fecha: string; // "2026-01-10"
  tipoTerapia: string; // Tipo de terapia
}
```

---

## 📊 Comparativa: Antes vs Ahora

| Campo             | Antes     | Ahora                                | Razón                 |
| ----------------- | --------- | ------------------------------------ | --------------------- |
| `id`              | `string`  | `number`                             | BD usa Integer        |
| `fecha`           | `Date`    | `string`                             | API devuelve ISO 8601 |
| `apellidos`       | `string`  | `apellidoPaterno`, `apellidoMaterno` | Estructura BD         |
| `pagosPendientes` | `number`  | `PagoPendiente[]`                    | Necesita detalles     |
| `documentoNuevo`  | `boolean` | `DocumentoNuevo[]`                   | Necesita información  |

---

## 🔧 Uso en Componentes

### Template HTML

```html
<div *ngIf="inicioData">
  <h1>{{ saludo }}, {{ inicioData.hijoSeleccionado.nombre }}</h1>

  <!-- Próxima Sesión -->
  <div *ngIf="inicioData.tarjetas.proxSesion">
    <p>{{ inicioData.tarjetas.proxSesion.fecha | date: 'fullDate' }}</p>
    <p>{{ inicioData.tarjetas.proxSesion.hora }}</p>
  </div>

  <!-- Pagos Pendientes -->
  <div *ngFor="let pago of inicioData.tarjetas.pagosPendientes">
    <span>{{ pago.descripcion }}</span>
    <span>{{ pago.monto | currency: 'COP' }}</span>
  </div>

  <!-- Documentos Nuevos -->
  <div *ngFor="let doc of inicioData.tarjetas.documentosNuevos">
    <span [class.nuevo]="!doc.visto">{{ doc.nombre }}</span>
  </div>
</div>
```

### Componente TypeScript

```typescript
export class InicioComponent implements OnInit {
  inicioData: InicioPage | null = null;
  cargando = true;

  constructor(private padresService: PadresService) {}

  ngOnInit(): void {
    this.padresService.getInicioData().subscribe(respuesta => {
      if (respuesta.exito && respuesta.datos) {
        this.inicioData = respuesta.datos;
        this.cargando = false;
      }
    });
  }

  cambiarHijo(hijoId: number): void {
    this.padresService.getInicioData().subscribe(...);
  }

  // Formateo de fechas
  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'long'
    });
  }
}
```

---

## 📱 Estructura de Respuesta API

```typescript
interface RespuestaApi<T> {
  exito: boolean;
  datos?: InicioPage;
  error?: string;
  mensaje?: string;
}

// Ejemplo de respuesta real
{
  exito: true,
  datos: {
    saludo: "Buenos días",
    hora: "09:30",
    hijoSeleccionado: {
      id: 1,
      nombre: "Carlos",
      apellidoPaterno: "García",
      apellidoMaterno: "López"
    },
    hijosDisponibles: [
      { id: 1, nombre: "Carlos" },
      { id: 2, nombre: "María" }
    ],
    tarjetas: {
      proxSesion: {
        id: 101,
        fecha: "2026-01-15",
        hora: "14:30",
        tipoTerapia: "Lenguaje",
        terapeuta: "Dr. Juan",
        estado: "confirmada"
      },
      ultimoAvance: { ... },
      pagosPendientes: [ ... ],
      documentosNuevos: [ ... ],
      ultimaObservacion: { ... }
    },
    cargando: false
  }
}
```

---

## 🎨 Elementos UI Esperados

### Tarjeta: Próxima Sesión

```
┌─────────────────────────┐
│ 📅 PRÓXIMA SESIÓN       │
├─────────────────────────┤
│ Miércoles, 15 de enero  │
│ 14:30 - Terapia Lenguaje│
│ Terapeuta: Dr. Juan     │
│ ✅ Confirmada           │
└─────────────────────────┘
```

### Tarjeta: Pagos Pendientes

```
┌─────────────────────────┐
│ 💳 PAGOS PENDIENTES     │
├─────────────────────────┤
│ Sesión enero 2026       │
│ $150.000 COP            │
│ Vence: 31-01-2026       │
│ ⚠️ Pendiente            │
└─────────────────────────┘
```

### Tarjeta: Documentos

```
┌─────────────────────────┐
│ 📄 DOCUMENTOS NUEVOS    │
├─────────────────────────┤
│ 🆕 Reporte de Progreso  │
│ 📥 Descargar PDF        │
└─────────────────────────┘
```

---

## ⚠️ Notas Importantes

1. **Formato de Fechas**

   - Backend devuelve: `"2026-01-12"` o `"2026-01-12T14:30:00"`
   - En templates: usar pipe `date`
   - En componentes: usar `new Date(string)`

2. **IDs Numéricos**

   - Todos los IDs ahora son `number` (no string)
   - Para URLs: convertir con `.toString()` si es necesario
   - Para comparaciones: usar `===` con números

3. **Listas Vacías**

   - `pagosPendientes: []` → No hay pagos
   - `documentosNuevos: []` → No hay documentos nuevos
   - `proxSesion: null` → No hay próxima sesión

4. **Estados**
   - Próxima sesión: `confirmada | pendiente | cancelada | realizada | reprogramada`
   - Pago: `pagado | pendiente | vencido | parcial`
   - Documento: tipo = `acuerdo | reporte | medico | medicamento | otro`

---

## 🔄 Flujo de Datos

```
Componente InicioComponent
    ↓
PadresService.getInicioData()
    ↓
GET /api/padres/inicio?hijo_id=1
    ↓
Backend Controller
    ↓
InicioPadreResponse (Schema Pydantic)
    ↓
RespuestaApi<InicioPage>
    ↓
Template HTML (con pipe date, currency, etc)
```

---

## 📋 Checklist para Implementadores

- [ ] Actualizar imports en componentes
- [ ] Verificar tipos en templates
- [ ] Convertir fechas con pipe `date`
- [ ] Usar currency para montos
- [ ] Manejar arrays con `*ngFor`
- [ ] Manejar null con `*ngIf`
- [ ] Agregar spinner mientras carga
- [ ] Manejar errores de API
- [ ] Responsive design
- [ ] Tests unitarios

---

## 🚀 Próximo Módulo

Una vez finalizado `inicio`, seguir con:

1. **Mis Hijos** - Similar, pero con lista de hijos
2. **Sesiones** - Tabla con filtros
3. **Pagos** - Resumen y historial
4. **Documentos** - Tabla con descargas

---

## 📞 Contacto

Para preguntas sobre las interfaces:

- Revisar: `GUIA_INTERFACES.md`
- Ejemplo: `EJEMPLO_COMPONENTE_INICIO.ts`
- Análisis: `ANALISIS_COHERENCIA_INICIO.md`

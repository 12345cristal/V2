# 2️⃣ Mis Hijos - Módulo de Información Clínica

## 📋 Descripción

Componente principal que centraliza toda la información clínica y administrativa de los hijos del padre.

## 🎯 Objetivo

Proporcionar una vista integral y organizada de:

- Información personal del niño
- Estado actual de salud
- Medicamentos vigentes
- Alergias documentadas
- Estados de visualización (nuevo/visto)

## 📁 Estructura de Archivos

```
mis-hijos/
├── mis-hijos.ts        # Componente TypeScript
├── mis-hijos.html      # Template HTML
├── mis-hijos.scss      # Estilos SCSS
└── README.md           # Este archivo
```

## 🔧 Componentes del Módulo

### 1. **mis-hijos.ts** (Componente)

- Gestión de estado de hijos
- Carga de datos desde PadresService
- Lógica de selección y navegación
- Cálculo de edad automático
- Manejo de ciclo de vida (OnInit, OnDestroy)

**Métodos principales:**

- `cargarHijos()` - Obtiene lista de hijos del backend
- `seleccionarHijo(hijo)` - Selecciona un hijo para ver detalles
- `marcarVisto(hijoId)` - Marca notificaciones como vistas
- `calcularEdad(fechaNacimiento)` - Calcula edad en años
- `obtenerSeveridadColor(severidad)` - Retorna clase CSS para severidad
- `obtenerMedicamentoNuevo(medicamento)` - Verifica si hay novedad reciente

### 2. **mis-hijos.html** (Template)

#### Estructura Principal:

```
Contenedor Principal
├── Encabezado (Título y subtítulo)
└── Contenido Principal
    ├── Listado de Hijos (Sidebar)
    │   ├── Header con gradiente
    │   ├── Tarjetas de hijos (con foto, nombre, edad, estado)
    │   └── Estados: Cargando, Sin datos
    └── Detalle del Hijo Seleccionado
        ├── Información General (Foto, datos básicos)
        ├── Alergias (Solo lectura)
        ├── Medicamentos Actuales (Con badges de novedad)
        └── Estados Visibles (Leyenda de iconos)
```

#### Secciones HTML:

**1. Listado de Hijos**

- Sidebar scrollable con lista de hijos
- Tarjeta interactiva por hijo
- Badge de novedades
- Indicadores visuales de estado (visto/no visto)

**2. Información General**

- Foto del niño (circular, con fallback)
- Nombre completo
- Datos básicos: edad, diagnóstico, cuatrimestre, fecha de ingreso

**3. Alergias**

- Lista de alergias (solo lectura)
- Severidad con color codificado (leve/moderada/severa)
- Descripción de reacción

**4. Medicamentos**

- Tarjetas de medicamentos activos/inactivos
- Badge 🆕 para medicamentos recientemente actualizados
- Información: dosis, frecuencia, razón, fechas
- Nota informativa sobre coordinador

**5. Estados Visibles**

- Referencia visual de badgesusados
- 🆕 Medicamento actualizado
- 👀 Visto por padre
- 📌 No visto por padre

### 3. **mis-hijos.scss** (Estilos)

#### Paleta de Colores:

- **Primario:** `#4a90e2` (Azul)
- **Secundario:** `#50c878` (Verde)
- **Advertencia:** `#ff9800` (Naranja)
- **Peligro:** `#e74c3c` (Rojo)
- **Fondo:** `#f8f9fa` (Gris claro)

#### Estilos Principales:

**1. Layout General**

- Contenedor flexible (sidebar + contenido)
- Responsive: de 2 columnas a 1 en mobile (< 768px)
- Animaciones suaves (fadeIn, slideDown)

**2. Listado de Hijos**

- Header con gradiente
- Tarjetas interactivas con hover effects
- Scrollbar personalizado
- Badge pulsante para notificaciones

**3. Secciones de Contenido**

- Tarjetas con sombra baja
- Espaciado consistente
- Colores diferenciados por tipo (alergias = rojo, medicamentos = azul)

**4. Animaciones**

- `fadeIn` - Entrada suave
- `fadeInDown` - Entrada desde arriba
- `fadeInRight` - Entrada desde la derecha
- `pulse` - Animación de escala
- `blink` - Parpadeo
- `slideDown` - Deslizamiento hacia abajo
- `spin` - Rotación (para spinner)

#### Breakpoints:

- **Tablet:** `768px`
- **Mobile:** `480px`

## 📊 Interface de Datos

Utiliza interfaces definidas en `padres.interfaces.ts`:

```typescript
interface Hijo {
  id: number;
  nombre: string;
  apellidoPaterno: string;
  apellidoMaterno?: string;
  foto?: string;
  fechaNacimiento: string;
  edad: number;
  diagnostico: string;
  cuatrimestre: number;
  fechaIngreso: string;
  alergias: Alergia[];
  medicamentos: Medicamento[];
  visto: boolean;
  novedades: number;
}

interface Medicamento {
  id: number;
  nombre: string;
  dosis: string;
  frecuencia: string;
  razon: string;
  fechaInicio: string;
  fechaFin?: string;
  activo: boolean;
  novedadReciente?: boolean;
  fechaActualizacion?: string;
}

interface Alergia {
  id: number;
  nombre: string;
  severidad: 'leve' | 'moderada' | 'severa';
  reaccion: string;
}
```

## 🔌 Integración con Servicios

### PadresService

```typescript
getMisHijos(): Observable<RespuestaApi<MisHijosPage>>
getHijoDetalle(hijoId: string): Observable<RespuestaApi<Hijo>>
```

## 🎨 Características Visuales

### Badges y Indicadores

- **🆕** - Medicamento recientemente actualizado
- **👀** - Visto por padre
- **📌** - No visto por padre
- **Rojo (leve/moderada/severa)** - Nivel de severidad de alergia

### Estados Interactivos

- **Hover:** Cambio de background y transformación
- **Activo:** Border izquierdo y shadow inset
- **Cargando:** Spinner animado
- **Novedades:** Badge rojo pulsante

## 📱 Responsividad

### Desktop (> 768px)

- Layout: 2 columnas (sidebar + contenido)
- Foto: 48px (listado), 120px (detalle)
- Grid medicamentos: 2 columnas

### Tablet (768px)

- Layout: Flexible, puede cambiar a 1 columna
- Foto: Mantiene tamaño
- Grid medicamentos: 2 columnas

### Mobile (< 480px)

- Layout: 1 columna
- Grid medicamentos: 1 columna
- Datos básicos: Stack vertical
- Alergias: Stack vertical

## 🔄 Ciclo de Vida

1. **ngOnInit**

   - Carga lista de hijos
   - Selecciona el primer hijo

2. **seleccionarHijo()**

   - Actualiza `hijoSeleccionado`
   - Marca como visto si hay novedades

3. **ngOnDestroy**
   - Completa observables
   - Limpia recursos

## 🚀 Mejoras Futuras

- [ ] Filtro de hijos por estado
- [ ] Edición de datos (coordinador)
- [ ] Histórico de cambios de medicamentos
- [ ] Exportar información a PDF
- [ ] Notificaciones en tiempo real
- [ ] Integración con calendario
- [ ] Comparativa de evolución (múltiples hijos)

## 📝 Notas de Desarrollo

- Utiliza RxJS `takeUntil` para gestión de memoria
- Componente standalone (sin módulos)
- CommonModule para directivas Angular
- Pipe `date` de Angular para formateo
- CSS Grid y Flexbox para layout responsive

## 🔐 Control de Acceso

- Solo accesible para padres autenticados
- Datos filtrados por padre (backend)
- Información sensible: alergias y medicamentos (solo lectura)

## 📞 Soporte

Para reportar problemas o sugerencias, contactar al equipo de desarrollo.

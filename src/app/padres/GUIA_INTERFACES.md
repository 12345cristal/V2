# 📘 Guía de Interfaces - Módulo Padres

## 🎯 Estructura de Interfaces por Módulo

### 1️⃣ INICIO (Dashboard Inicial)

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`ProxSesion`**: Próxima sesión programada
- **`UltimoAvance`**: Últimos avances terapéuticos
- **`PagosPendientes`**: Pagos vencidos/pendientes
- **`DocumentoNuevo`**: Documentos recién subidos
- **`UltimaObservacion`**: Última observación del terapeuta
- **`TarjetaResumen`**: Agrupa todas las tarjetas
- **`InicioPage`**: Vista completa del inicio

#### Ejemplo de uso:

```typescript
import { InicioPage, ProxSesion } from '@app/padres';

export class InicioComponent {
  inicioData: InicioPage;

  proximaSesion: ProxSesion | null;
}
```

---

### 2️⃣ MIS HIJOS

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Hijo`**: Información completa del niño
  - Datos personales (nombre, edad calculada)
  - Información clínica (diagnóstico, cuatrimestre)
  - Alergias (solo lectura)
  - Medicamentos actuales
- **`Medicamento`**: Datos de medicamentos con estado "novedad"
- **`Alergia`**: Alergias registradas
- **`MisHijosPage`**: Lista de hijos del padre

#### Ejemplo de uso:

```typescript
import { Hijo, Medicamento } from '@app/padres';

export class MisHijosComponent {
  hijos: Hijo[];
  medicamentosActualizados: Medicamento[];
}
```

---

### 3️⃣ SESIONES

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Sesion`**: Información de una sesión
  - Fecha, hora, tipo de terapia
  - Estado (programada, realizada, cancelada, reprogramada)
  - Observaciones del terapeuta
  - Grabación de voz (opcional)
  - URL para descargar bitácora
- **`SesionesPage`**: Agrupador para vista actual
- **`EstadoSesion`**: Tipo para estados válidos

#### Ejemplo de uso:

```typescript
import { Sesion, EstadoSesion } from '@app/padres';

export class SesionesComponent {
  sesiones: Sesion[];
  sesionesHoy = this.sesiones.filter(s => /* hoy */);

  estado: EstadoSesion = 'programada';
}
```

---

### 4️⃣ HISTORIAL TERAPÉUTICO

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`AsistenciaData`**: Datos de asistencia por mes
- **`ObjetivoEvolucion`**: Progreso de objetivos (escala 0-100)
- **`FrecuenciaTerapia`**: Frecuencia por tipo de terapia
- **`HistorialTerapeuticoPage`**: Conjunto de datos para gráficas

#### Ejemplo de uso:

```typescript
import { HistorialTerapeuticoPage, AsistenciaData } from '@app/padres';

export class HistorialComponent {
  historial: HistorialTerapeuticoPage;
  asistencia: AsistenciaData[];
  porcentajePromedio = this.calcularPromedio();
}
```

---

### 5️⃣ TAREAS

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Tarea`**: Tarea asignada por terapeuta
  - Título, descripción, objetivo
  - Instrucciones claras
  - Recursos asociados (URLs)
  - Fechas (asignación, vencimiento, completada)
  - Estado (pendiente, realizada, vencida)
- **`TareasPage`**: Agrupador con filtros
- **`EstadoTarea`**: Tipo para estados válidos

#### Ejemplo de uso:

```typescript
import { Tarea, EstadoTarea } from '@app/padres';

export class TareasComponent {
  tareas: Tarea[];
  pendientes = this.tareas.filter((t) => t.estado === 'pendiente');
  vencidas = this.tareas.filter((t) => t.estado === 'vencida');
}
```

---

### 6️⃣ PAGOS

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Pago`**: Registro individual de pago
  - Fecha, monto, método (tarjeta, transferencia, etc)
  - Estado (pagado, pendiente, vencido, parcial)
  - Referencia y comprobante
- **`PlanPagos`**: Resumen del plan financiero
  - Total del plan
  - Monto pagado
  - Saldo pendiente
  - Próxima fecha de pago
- **`PagosPage`**: Vista completa con historial
- **`MetodoPago`** y **`EstadoPago`**: Tipos de estados

#### Ejemplo de uso:

```typescript
import { PagosPage, Pago } from '@app/padres';

export class PagosComponent {
  pagos: PagosPage;
  proxima = this.pagos.plan.proximaFechaPago;
  saldo = this.pagos.plan.saldoPendiente;
}
```

---

### 7️⃣ DOCUMENTOS

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Documento`**: Documento oficial
  - Tipo (acuerdo, reporte, médico, medicamento, otro)
  - PDF URL
  - Visto/no visto
  - Marcador de novedad reciente
- **`DocumentosPage`**: Agrupador con filtros
- **`TipoDocumento`**: Tipo con opciones válidas

#### Ejemplo de uso:

```typescript
import { Documento, TipoDocumento } from '@app/padres';

export class DocumentosComponent {
  documentos: Documento[];
  reportes = this.documentos.filter((d) => d.tipo === 'reporte');
  nuevos = this.documentos.filter((d) => d.novedadReciente);
}
```

---

### 8️⃣ RECURSOS RECOMENDADOS

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Recurso`**: Recurso de apoyo
  - Tipo (PDF, video, enlace)
  - Título, descripción
  - URL o archivo
  - Relacionado con terapeuta u objetivo
  - Marcador de visto
- **`RecursosPage`**: Agrupador con filtros
- **`TipoRecurso`** y **`OrganizacionRecurso`**: Tipos de estados

#### Ejemplo de uso:

```typescript
import { Recurso, TipoRecurso } from '@app/padres';

export class RecursosComponent {
  recursos: Recurso[];
  videos = this.recursos.filter((r) => r.tipo === 'video');
  porTerapeuta = this.agruparPorTerapeuta();
}
```

---

### 9️⃣ MENSAJES

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Mensaje`**: Mensaje individual
  - Contenido, tipo (texto, audio, archivo)
  - Remitente y tipo de contacto
  - Marca de leído
  - Archivo URL (opcional)
  - Respuesta a otro mensaje (opcional)
- **`Chat`**: Conversación completa
  - Contacto (terapeuta, coordinador, etc)
  - Último mensaje
  - Historial completo
  - Contador de no leídos
- **`MensajesPage`**: Agrupador de chats
- **`TipoContacto`** y **`TipoMensaje`**: Tipos de estados

#### Ejemplo de uso:

```typescript
import { Chat, Mensaje, TipoContacto } from '@app/padres';

export class MensajesComponent {
  chats: Chat[];
  noLeidos = this.chats.reduce((sum, c) => sum + c.noLeidosCount, 0);

  enviarMensaje(texto: string) {
    // Usar PadresService.enviarMensaje()
  }
}
```

---

### 🔔 10️⃣ NOTIFICACIONES

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`Notificacion`**: Notificación individual
  - Tipo (nueva-sesion, reprogramación, documento-nuevo, etc)
  - Título y contenido
  - Estado (leída/no leída)
  - Enlace relacionado
- **`NotificacionesPage`**: Agrupador con filtro
- **`TipoNotificacion`**: Tipo con opciones válidas

#### Ejemplo de uso:

```typescript
import { Notificacion, TipoNotificacion } from '@app/padres';

export class NotificacionesComponent {
  notificaciones: Notificacion[];
  noLeidas = this.notificaciones.filter((n) => !n.leida);
}
```

---

### ⚙️ 11️⃣ PERFIL Y ACCESIBILIDAD

**Archivo**: `padres.interfaces.ts`

#### Interfaces principales:

- **`PreferenciasAccesibilidad`**: Preferencias de acceso
  - Tamaño de texto (normal, grande, muy-grande)
  - Tema (claro, suave, oscuro, alto-contraste)
  - Modo lectura (normal, lectura, dislexia)
  - Contraste alto
  - Reducir animaciones
  - Sonidos activados
- **`UsuarioPadre`**: Datos del usuario padre
- **`PerfilPage`**: Vista completa del perfil
- **`TamanoTexto`**, **`TemaColor`**, **`ModoLectura`**: Tipos de estados

#### Ejemplo de uso:

```typescript
import { UsuarioPadre, PreferenciasAccesibilidad } from '@app/padres';

export class PerfilComponent {
  usuario: UsuarioPadre;
  prefs: PreferenciasAccesibilidad = usuario.preferenciasAccesibilidad;

  aplicarTema() {
    // Cambiar clase CSS según tema
  }
}
```

---

## 📦 Servicio Principal - `PadresService`

### Métodos disponibles:

```typescript
import { PadresService } from '@app/padres';

export class MiComponente {
  constructor(private padresService: PadresService) {}

  // INICIO
  getInicioData() {
    this.padresService.getInicioData().subscribe(respuesta => {
      if (respuesta.exito) {
        console.log(respuesta.datos);
      }
    });
  }

  // MIS HIJOS
  getMisHijos() {
    this.padresService.getMisHijos().subscribe(...);
  }

  // SESIONES
  getSesiones() {
    this.padresService.getSesiones('hoy').subscribe(...);
    // Opciones: 'hoy' | 'programadas' | 'semana'
  }

  // TAREAS
  completarTarea(tareaId: string) {
    this.padresService.completarTarea(tareaId).subscribe(...);
  }

  // MENSAJES
  enviarMensaje() {
    this.padresService.enviarMensaje(
      contactoId,
      'Mi mensaje',
      'texto'
    ).subscribe(...);
  }

  // DESCARGAS
  descargarBitacora(sesionId: string) {
    this.padresService.descargarBitacora(sesionId).subscribe(blob => {
      // Manejar descarga
    });
  }

  // ACTUALIZAR DATOS
  guardarPreferencias() {
    this.padresService.actualizarPreferenciasAccesibilidad({
      tamanoTexto: 'grande',
      tema: 'suave'
    }).subscribe(...);
  }
}
```

---

## 🔄 Estructura de Respuesta API

Todas las llamadas retornan un tipo genérico:

```typescript
interface RespuestaApi<T> {
  exito: boolean;
  datos?: T;
  error?: string;
  mensaje?: string;
}
```

### Ejemplo:

```typescript
this.padresService.getInicioData().subscribe((respuesta) => {
  if (respuesta.exito) {
    const inicioData: InicioPage = respuesta.datos;
  } else {
    console.error(respuesta.error);
  }
});
```

---

## 📝 Paginación

Para listados paginados:

```typescript
interface ListadoPaginado<T> {
  items: T[];
  paginacion: {
    pagina: number;
    porPagina: number;
    total: number;
    totalPaginas: number;
  };
}
```

---

## ✅ Checklist de Implementación

- [ ] Servicios creados para cada módulo
- [ ] Estados compartidos (NgRx/Signals/BehaviorSubject)
- [ ] Componentes usando las interfaces
- [ ] Manejo de errores
- [ ] Spinner de carga
- [ ] Mensajes de éxito/error
- [ ] Responsive design
- [ ] Accesibilidad (WCAG)
- [ ] Tests unitarios

---

## 🎨 Recomendaciones UX

1. **Siempre mostrar estado de carga** con spinner
2. **Indicadores visuales claros** de nuevas notificaciones
3. **Confirmación antes de acciones importantes** (completar tarea, pagar, etc)
4. **Tooltips explicativos** en gráficas del historial
5. **Colores suaves** en toda la interfaz (nunca rojo puro)
6. **Accesibilidad first** - textos alternativos, contraste suficiente

---

## 🚀 Próximos pasos

1. Crear componentes para cada sección
2. Implementar servicios reales (Backend)
3. Agregar gestión de estado
4. Diseño visual (Figma → CSS/Tailwind)
5. Tests unitarios
6. Integración de notificaciones en tiempo real (WebSocket)

# 📋 MÓDULO PADRES - GUÍA COMPLETA

## 🚀 PRIMEROS PASOS

### 1. Crear la estructura de carpetas

**Ejecuta este script batch:**

```bash
crear-estructura-padres.bat
```

Esto creará todas las carpetas necesarias en:

```
src/app/padres/pages/
├── inicio/
├── mis-hijos/
│   └── detalle-hijo/
├── sesiones/
│   └── detalle-sesion/
├── historial-terapeutico/
├── tareas/
│   └── detalle-tarea/
├── pagos/
│   └── historial-pagos/
├── documentos/
│   └── detalle-documento/
├── recursos/
├── mensajes/
│   └── chat/
└── notificaciones/
```

---

## 📄 COMPONENTES A CREAR

### 1️⃣ INICIO (Dashboard)

**Archivo:** `src/app/padres/pages/inicio/inicio.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { signal } from '@angular/core';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `...`,
  styles: [`...`],
})
export class InicioComponent implements OnInit {
  // Saludo dinámico
  // Selector de hijo
  // Tarjetas resumen
  // Quick links
}
```

**Características:**

- ✅ Saludo dinámico (Buenos días/tardes/noches)
- ✅ Selector de hijo
- ✅ 5 Tarjetas resumen (sesión, avance, pagos, documento, observación)
- ✅ Quick links a todas las secciones

---

### 2️⃣ MIS HIJOS

**Archivo:** `src/app/padres/pages/mis-hijos/mis-hijos.ts`

```typescript
@Component({
  selector: 'app-mis-hijos',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `...`,
})
export class MisHijosComponent {
  // Lista de hijos con:
  // - Foto
  // - Nombre completo
  // - Edad (calculada)
  // - Diagnóstico
  // - Cuatrimestre
  // - Fecha ingreso
  // - Alergias
  // - Medicamentos (con indicador nuevo)
  // - Estado visto/no visto
}
```

**Detalle Hijo:** `src/app/padres/pages/mis-hijos/detalle-hijo/detalle-hijo.ts`

```typescript
@Component({
  selector: 'app-detalle-hijo',
  standalone: true,
})
export class DetalleHijoComponent {
  // Vista completa de información del niño
  // Editable solo para coordinador
}
```

---

### 3️⃣ SESIONES

**Archivo:** `src/app/padres/pages/sesiones/sesiones.ts`

```typescript
@Component({
  selector: 'app-sesiones',
  standalone: true,
})
export class SesionesComponent {
  // 3 Vistas:
  // - Hoy
  // - Programadas
  // - Semana completa
  // Cada sesión muestra:
  // - Fecha, Hora
  // - Tipo de terapia
  // - Terapeuta
  // - Estado (Programada, Realizada, Cancelada, Reprogramada)
}
```

**Detalle Sesión:** `src/app/padres/pages/sesiones/detalle-sesion/detalle-sesion.ts`

```typescript
@Component({
  selector: 'app-detalle-sesion',
  standalone: true,
})
export class DetalleSessionComponent {
  // - Comentarios del terapeuta
  // - Grabación de voz (opcional)
  // - Descargar bitácora diaria (PDF)
}
```

---

### 4️⃣ HISTORIAL TERAPÉUTICO VISUAL

**Archivo:** `src/app/padres/pages/historial-terapeutico/historial-terapeutico.ts`

```typescript
@Component({
  selector: 'app-historial-terapeutico',
  standalone: true,
  imports: [CommonModule, NgCharts], // Necesita ng-chartjs o similar
})
export class HistorialTerapeuticoComponent {
  // Gráficas:
  // 1. Asistencia por mes (barras)
  // 2. Sesiones realizadas vs canceladas (pie)
  // 3. Evolución de objetivos (línea)
  // 4. Frecuencia de terapias (barras)
  // Botones:
  // - Descargar reporte PDF
  // - Descargar resumen mensual
}
```

---

### 5️⃣ TAREAS

**Archivo:** `src/app/padres/pages/tareas/tareas.ts`

```typescript
@Component({
  selector: 'app-tareas',
  standalone: true,
})
export class TareasComponent {
  // Lista de tareas asignadas por terapeuta
  // Campos: Fecha, Objetivo, Instrucciones, Recursos
  // Estados: Pendiente, Realizada, Vencida
  // Filtros por estado
}
```

**Detalle Tarea:** `src/app/padres/pages/tareas/detalle-tarea/detalle-tarea.ts`

```typescript
@Component({
  selector: 'app-detalle-tarea',
  standalone: true,
})
export class DetalleTaskComponent {
  // Vista completa con recursos asociados
  // Marcar como realizada
}
```

---

### 6️⃣ PAGOS

**Archivo:** `src/app/padres/pages/pagos/pagos.ts`

```typescript
@Component({
  selector: 'app-pagos',
  standalone: true,
})
export class PagosComponent {
  // Resumen:
  // - Total del plan
  // - Monto pagado
  // - Saldo pendiente
  // - Próxima fecha de pago
  // - Último pago realizado
  // Link a historial detallado
}
```

**Historial Pagos:** `src/app/padres/pages/pagos/historial-pagos/historial-pagos.ts`

```typescript
@Component({
  selector: 'app-historial-pagos',
  standalone: true,
})
export class HistorialPagosComponent {
  // Tabla con:
  // - Fecha
  // - Monto
  // - Método
  // - Referencia
  // - Botones descargar comprobante
  // Descargar reporte completo (PDF)
}
```

---

### 7️⃣ DOCUMENTOS

**Archivo:** `src/app/padres/pages/documentos/documentos.ts`

```typescript
@Component({
  selector: 'app-documentos',
  standalone: true,
})
export class DocumentosComponent {
  // Tipos de documentos:
  // - Acuerdo de servicios
  // - Reportes terapéuticos
  // - Documentos médicos
  // - Actualización de medicamentos
  // - Otros
  // Funciones:
  // - Ver PDF
  // - Descargar
  // - Marcar visto
  // - Indicador nuevo
}
```

**Detalle Documento:** `src/app/padres/pages/documentos/detalle-documento/detalle-documento.ts`

```typescript
@Component({
  selector: 'app-detalle-documento',
  standalone: true,
})
export class DetalleDocumentoComponent {
  // Visor PDF integrado
  // Información del documento
  // Botones de acción
}
```

---

### 8️⃣ RECURSOS RECOMENDADOS

**Archivo:** `src/app/padres/pages/recursos/recursos.ts`

```typescript
@Component({
  selector: 'app-recursos',
  standalone: true,
})
export class RecursosComponent {
  // Tipos:
  // - PDFs
  // - Videos
  // - Enlaces externos
  // Organización:
  // - Por terapeuta
  // - Por objetivo terapéutico
  // Estados: Visto/No visto
  // Descripción y recomendación
}
```

---

### 9️⃣ MENSAJES

**Archivo:** `src/app/padres/pages/mensajes/mensajes.ts`

```typescript
@Component({
  selector: 'app-mensajes',
  standalone: true,
})
export class MensajesComponent {
  // Lista de chats con:
  // - Terapeutas
  // - Coordinador
  // - Administrador
  // Historial por hijo
  // Badge de mensajes no leídos
}
```

**Chat:** `src/app/padres/pages/mensajes/chat/chat.ts`

```typescript
@Component({
  selector: 'app-chat',
  standalone: true,
})
export class ChatComponent {
  // Soporte:
  // - Texto
  // - Audio
  // - Archivos
  // Historial de conversación
  // Marca como leído automáticamente
}
```

---

### 🔟 NOTIFICACIONES

**Archivo:** `src/app/padres/pages/notificaciones/notificaciones.ts`

```typescript
@Component({
  selector: 'app-notificaciones',
  standalone: true,
})
export class NotificacionesComponent {
  // Eventos:
  // - Nueva sesión
  // - Reprogramación
  // - Documento nuevo
  // - Comentario del terapeuta
  // - Pago próximo
  // Filtros y búsqueda
  // Estados: Leída/No leída
}
```

---

## 🛠️ SERVICIOS NECESARIOS

```typescript
// src/app/padres/services/

// hijo.service.ts
export class HijoService {
  getHijos(): Observable<Hijo[]>;
  getHijoById(id: string): Observable<Hijo>;
  updateHijo(id: string, data: any): Observable<any>;
}

// session.service.ts
export class SessionService {
  getSessions(filtro?): Observable<Session[]>;
  getSessionById(id: string): Observable<Session>;
  getSessionsByType(type: 'today' | 'scheduled' | 'week'): Observable<Session[]>;
}

// task.service.ts
export class TaskService {
  getTasks(): Observable<Task[]>;
  getTaskById(id: string): Observable<Task>;
  markTaskComplete(id: string): Observable<any>;
}

// payment.service.ts
export class PaymentService {
  getPaymentSummary(): Observable<PaymentSummary>;
  getPaymentHistory(): Observable<Payment[]>;
  downloadPaymentReport(): Observable<Blob>;
}

// document.service.ts
export class DocumentService {
  getDocuments(): Observable<Document[]>;
  getDocumentById(id: string): Observable<Document>;
  markAsViewed(id: string): Observable<any>;
}

// resource.service.ts
export class ResourceService {
  getResources(filtro?): Observable<Resource[]>;
  markResourceViewed(id: string): Observable<any>;
}

// message.service.ts
export class MessageService {
  getChats(): Observable<Chat[]>;
  getChatById(id: string): Observable<Chat>;
  sendMessage(chatId: string, message: string): Observable<any>;
}

// notification.service.ts
export class NotificationService {
  getNotifications(): Observable<Notification[]>;
  markAsRead(id: string): Observable<any>;
  subscribe(events: string[]): Observable<Notification>;
}
```

---

## 📍 INTEGRACIÓN EN RUTAS

**app.routes.ts**

```typescript
import { PADRES_ROUTES } from './padres/padres.routes';

export const routes: Routes = [
  // ... otras rutas
  {
    path: 'padres',
    children: PADRES_ROUTES,
  },
];
```

---

## 🎨 GUÍA DE ESTILOS

### Colores

- Principal: `#4CAF50` (verde)
- Secundario: `#667eea` (púrpura)
- Fondo: `#f5f5f5`
- Texto: `#333`
- Error: `#f44336` (rojo)
- Éxito: `#4CAF50` (verde)

### Espaciado

- Pequeño: `0.5rem`
- Medio: `1rem`
- Grande: `1.5rem`
- XLarge: `2rem`

### Tipografía

- Títulos: `2rem`, Bold
- Subtítulos: `1.5rem`, Semi-bold
- Texto: `1rem`, Regular
- Pequeño: `0.875rem`, Regular

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Ejecutar crear-estructura-padres.bat
- [ ] Crear InicioComponent
- [ ] Crear MisHijosComponent
- [ ] Crear SesionesComponent
- [ ] Crear HistorialTerapeuticoComponent (con gráficas)
- [ ] Crear TareasComponent
- [ ] Crear PagosComponent
- [ ] Crear DocumentosComponent
- [ ] Crear RecursosComponent
- [ ] Crear MensajesComponent
- [ ] Crear NotificacionesComponent
- [ ] Crear servicios en /services
- [ ] Integrar en app.routes.ts
- [ ] Pruebas unitarias
- [ ] Pruebas de navegación
- [ ] Verificar accesibilidad (texto grande, contraste, etc.)
- [ ] Pruebas en móvil

---

## 📱 RESPONSABILIDAD POR ROL

| Elemento             | Responsable    | Ver      | Editar   |
| -------------------- | -------------- | -------- | -------- |
| Información del niño | Coordinador    | ✅ Padre | ❌       |
| Sesiones             | Terapeuta      | ✅ Padre | ❌       |
| Bitácoras            | Terapeuta      | ✅ Padre | ❌       |
| Medicamentos         | Coordinador    | ✅ Padre | ❌       |
| Recursos             | Terapeuta      | ✅ Padre | ❌       |
| Pagos                | Administración | ✅ Padre | ❌       |
| Mensajes             | Todos          | ✅ Padre | ✅ Padre |
| Notificaciones       | Sistema        | ✅ Padre | ❌       |

---

## 📥 DESCARGAS DISPONIBLES

| Funcionalidad         | Ubicación                               |
| --------------------- | --------------------------------------- |
| Bitácora diaria       | Detalle Sesión → Botón PDF              |
| Reportes terapéuticos | Historial Terapéutico → Botón Descargar |
| Reporte de pagos      | Pagos → Botón PDF                       |
| Comprobantes          | Historial Pagos → Por pago              |
| Documentos oficiales  | Documentos → Botón Descargar            |

---

## 🧩 ACCESIBILIDAD

Implementar en todas las páginas:

- [ ] Opción de texto grande (16px, 18px)
- [ ] Opción de colores suaves (menos contraste)
- [ ] Opción de modo lectura (sin navegación lateral)
- [ ] Opción de contraste alto
- [ ] Guardar preferencias en localStorage por usuario
- [ ] ARIA labels en formularios
- [ ] Navegación por teclado
- [ ] Tamaño mínimo de botones: 48x48px

---

## 🚀 PRÓXIMOS PASOS

1. **Crear estructura de carpetas** → `crear-estructura-padres.bat`
2. **Crear componentes base** → Usar templates proporcionados
3. **Integrar servicios** → Conectar con API
4. **Pruebas** → Unit tests y e2e
5. **Deployment** → Integrar en producción

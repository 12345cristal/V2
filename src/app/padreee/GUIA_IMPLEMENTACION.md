# 🏗️ ESTRUCTURA COMPLETA MÓDULO PADRE - GUÍA DE IMPLEMENTACIÓN

## 📋 COMPONENTES A CREAR / ACTUALIZAR

### 1️⃣ INICIO (Dashboard) ✅

- **Path**: `/padre/inicio`
- **Componente**: `InicioComponent`
- **Estado**: ✅ CREADO
- **Archivos**:
  - `inicio.component.ts` ✅
  - `inicio.component.html` ✅
  - `inicio.component.scss` ✅

---

### 2️⃣ MIS HIJOS (Info Clínica) - Renombrado de info-nino

- **Path**: `/padre/mis-hijos` o `/padre/info-nino`
- **Componente**: `InfoNinoComponent` (reutilizar existente)
- **Estado**: ✅ EXISTE
- **Archivos**: Ya existen en `/padre/info-nino/`

---

### 3️⃣ SESIONES - Renombrado de terapias

- **Path**: `/padre/sesiones` o `/padre/terapias`
- **Componente**: `TerapiasComponent` (reutilizar)
- **Estado**: ✅ EXISTE
- **Archivos**: Ya existen en `/padre/terapias/`

---

### 4️⃣ HISTORIAL TERAPÉUTICO (Gráficas y análisis)

- **Path**: `/padre/historial`
- **Componente**: `HistorialTerapeuticoComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Gráfica de asistencia por mes
  - Sesiones realizadas vs canceladas
  - Evolución de objetivos
  - Frecuencia de terapias
  - Botón descargar reporte PDF

---

### 5️⃣ TAREAS PARA CASA

- **Path**: `/padre/tareas`
- **Componente**: `TareasComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Tareas asignadas por terapeuta
  - Fecha, objetivo, instrucciones
  - Estados: Pendiente, Realizada, Vencida
  - Recursos asociados

---

### 6️⃣ PAGOS Y FACTURAS

- **Path**: `/padre/pagos`
- **Componente**: `PagosComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Total del plan
  - Monto pagado
  - Saldo pendiente
  - Próxima fecha
  - Último pago
  - Historial de pagos
  - Descargar reporte PDF

---

### 7️⃣ DOCUMENTOS

- **Path**: `/padre/documentos`
- **Componente**: Ya existe
- **Estado**: ✅ EXISTE (estructura parcial)
- **Mejoras necesarias**:
  - Acuerdo de servicios
  - Reportes terapéuticos
  - Documentos médicos
  - Actualización de medicamentos
  - Marcar como visto
  - Indicador de nuevo

---

### 8️⃣ RECURSOS RECOMENDADOS

- **Path**: `/padre/recursos`
- **Componente**: `RecursosComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - PDFs, videos, enlaces externos
  - Organización por terapeuta/objetivo
  - Estados: Visto/No visto

---

### 9️⃣ MENSAJES CON EQUIPO

- **Path**: `/padre/mensajes`
- **Componente**: `MensajesComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Chats con terapeutas
  - Chats con coordinador
  - Chats con administrador
  - Texto, audio, archivos
  - Historial por hijo

---

### 🔟 NOTIFICACIONES

- **Path**: `/padre/notificaciones`
- **Componente**: `NotificacionesComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Nueva sesión
  - Reprogramación
  - Documento nuevo
  - Comentario del terapeuta
  - Pago próximo
  - Estados: Leída/No leída

---

### 1️⃣1️⃣ PERFIL Y ACCESIBILIDAD

- **Path**: `/padre/perfil-accesibilidad`
- **Componente**: `PerfilAccesibilidadComponent`
- **Estado**: ❌ CREAR
- **Contenido**:
  - Texto grande (toggle)
  - Colores suaves (toggle)
  - Modo lectura (toggle)
  - Contraste alto (toggle)
  - Guardar preferencias

---

## 🛠️ PRÓXIMAS ACCIONES

1. Crear las carpetas faltantes en `/padre/`
2. Implementar cada componente con TypeScript, HTML y SCSS
3. Actualizar `padre.routes.ts` con todas las rutas
4. Integrar servicios backend para cada módulo
5. Implementar descargas PDF
6. Implementar gráficas con Chart.js o similar

---

## 📌 RUTAS FINALES (padre.routes.ts)

```typescript
/padre/inicio           → Dashboard principal
/padre/mis-hijos        → Info clínica del niño (info-nino)
/padre/sesiones         → Sesiones (terapias)
/padre/historial        → Historial terapéutico
/padre/tareas           → Tareas para casa
/padre/pagos            → Pagos y facturas
/padre/documentos       → Documentos centralizados
/padre/recursos         → Recursos recomendados
/padre/mensajes         → Mensajes con equipo
/padre/notificaciones   → Notificaciones
/padre/perfil-accesibilidad → Configuración de accesibilidad
```

---

## 🎯 PRIORIDADES

1. ⭐⭐⭐ Historial terapéutico (gráficas)
2. ⭐⭐⭐ Tareas para casa
3. ⭐⭐⭐ Pagos y facturas
4. ⭐⭐ Recursos recomendados
5. ⭐⭐ Mensajes
6. ⭐ Notificaciones
7. ⭐ Perfil y accesibilidad

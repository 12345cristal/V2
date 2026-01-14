# 📅 Guía Completa: Asignar Citas de Terapia en el Calendario

## 🎯 Objetivo
Asignar citas de terapia a niños y visualizarlas en el calendario del coordinador.

---

## 📍 Ubicación del Calendario

**URL**: http://localhost:4200/coordinador/asignar-terapias

El componente se encuentra en:
- [src/app/coordinador/asignar-terapias/asignar-terapias.component.ts](../../src/app/coordinador/asignar-terapias/asignar-terapias.component.ts)
- [src/app/coordinador/asignar-terapias/asignar-terapias.component.html](../../src/app/coordinador/asignar-terapias/asignar-terapias.component.html)

---

## ✨ Características del Calendario

### Vistas Disponibles
1. **Vista Semana** (por defecto)
   - Muestra los días lunes a sábado
   - Horario de 8:00 AM a 6:00 PM
   - Citas mostradas como bloques arrastrables

2. **Vista Día**
   - Enfoque en un día específico
   - Mejor para detalles de citas individuales

3. **Vista Mes**
   - Overview general (en desarrollo)

### Funcionalidades
- ✅ Crear nuevas citas
- ✅ Editar citas existentes
- ✅ Cancelar citas
- ✅ Arrastrar y soltar citas (drag & drop)
- ✅ Filtrar por niño, terapeuta o terapia
- ✅ Mini calendario para navegación rápida
- ✅ Sincronización con Google Calendar (opcional)
- ✅ Citas recurrentes (crear múltiples sesiones)

---

## 🚀 Cómo Asignar una Cita de Terapia

### Paso 1: Ir al Calendario
```
http://localhost:4200/coordinador/asignar-terapias
```

### Paso 2: Clickea el Botón "Nueva Terapia"
- En la esquina superior derecha del header
- O double-click en un horario vacío del calendario

### Paso 3: Completa el Formulario Modal

**Sección 1: Información Principal**
- **Niño**: Selecciona el niño al que le asignarás la terapia
- **Tipo de Terapia**: Selecciona qué terapia requiere (ej: Psicomotricidad, Lenguaje, etc.)
- **Terapeuta**: Se filtra automáticamente según la terapia seleccionada
  - ⚠️ Solo muestra terapeutas especializados en esa terapia

**Sección 2: Fecha y Horario**
- **Fecha**: Selecciona la fecha en formato calendario
- **Hora Inicio**: Selecciona hora (ej: 09:00)
- **Hora Fin**: Se calcula automáticamente según duración de la terapia
  - No necesitas llenarla, se ajusta automáticamente

**Sección 3: Recurrencia** (solo si es nueva cita)
- ☑️ Marca "Terapia recurrente" si quieres crear múltiples sesiones
- Selecciona los días de la semana (Lunes, Martes, etc.)
- Especifica cuántas semanas durará

**Sección 4: Observaciones**
- Notas adicionales (opcional)

**Sección 5: Sincronización**
- ☑️ Marca para sincronizar automáticamente con Google Calendar

### Paso 4: Guarda la Cita
- Click en botón "Crear Terapia" o "Guardar Cambios"
- La cita aparecerá inmediatamente en el calendario

---

## 📊 Ejemplo: Crear una Cita Simple

1. **Ir al calendario**
   ```
   http://localhost:4200/coordinador/asignar-terapias
   ```

2. **Clickear "Nueva Terapia"**

3. **Completar:**
   - Niño: "Juan Pérez"
   - Terapia: "Fisioterapia"
   - Terapeuta: "Dr. Carlos López" (se filtra automáticamente)
   - Fecha: 15 de enero, 2026
   - Hora Inicio: 09:00
   - Hora Fin: (se calcula automáticamente a 10:00)

4. **Guardar**
   - Click en "Crear Terapia"
   - ✅ La cita aparecerá en el calendario

---

## 📅 Ejemplo: Crear Citas Recurrentes

Crear terapia todas las semanas durante 4 semanas:

1. **Abrir formulario** → "Nueva Terapia"

2. **Datos Básicos:**
   - Niño: "María García"
   - Terapia: "Logopedia"
   - Terapeuta: "Dra. Sandra Ruiz"
   - Fecha Inicio: 13 de enero, 2026

3. **Activar Recurrencia:**
   - ☑️ Marcar "Terapia recurrente"
   - Seleccionar: Lunes, Miércoles, Viernes
   - Cantidad: 4 semanas

4. **Guardar**
   - Se crearán 12 citas (3 días × 4 semanas)
   - Todas aparecerán en el calendario

---

## 🎬 Acciones sobre Citas Existentes

### Editar una Cita
1. Clickea en el bloque de la cita en el calendario
2. Se abre el modal con los datos
3. Modifica lo que necesites
4. Clickea "Guardar Cambios"

### Cancelar una Cita
1. Abre la cita (click en el bloque)
2. Clickea el botón rojo "Cancelar Terapia"
3. Se marca como "cancelada" en el calendario

### Arrastrar una Cita (Drag & Drop)
1. Click y arrastra el bloque de la cita
2. Suéltalo en un nuevo horario
3. Se actualiza automáticamente

---

## 🔍 Filtrar Citas en el Calendario

### Usando el Sidebar Izquierdo

**Filtro por Niño:**
```
Filtros → Niño → Selecciona un niño → Se actualizan las citas
```

**Filtro por Terapeuta:**
```
Filtros → Terapeuta → Selecciona un terapeuta → Se actualizan las citas
```

**Filtro por Tipo de Terapia:**
```
Filtros → Tipo de Terapia → Selecciona una terapia → Se actualizan las citas
```

**Limpiar Filtros:**
```
Clickea el botón "Clear" al lado de "Filtros"
```

---

## 🗓️ Navegación del Calendario

### Cambiar de Semana
- **Flecha Izquierda (◀)**: Semana anterior
- **Flecha Derecha (▶)**: Semana siguiente
- **Botón "Hoy"**: Vuelve a la semana actual

### Mini Calendario (Lado Izquierdo)
- Click en un día para ir a esa semana
- Navegación por mes/año
- Los días seleccionados están destacados

### Cambiar Período
- Click en el texto del período actual (ej: "13–19 enero 2026")
- Se abre un selector de fechas

---

## 💾 Datos que se Guardan

Cuando creas/editas una cita, se registra:

```json
{
  "nino_id": 1,
  "terapeuta_id": 5,
  "terapia_id": 3,
  "fecha": "2026-01-15",
  "hora_inicio": "09:00:00",
  "hora_fin": "10:00:00",
  "estado": "PROGRAMADA",
  "observaciones": "Observación opcional",
  "sincronizar_google_calendar": true
}
```

---

## 🔌 API Endpoints Utilizados

### Obtener Niños
```
GET /api/v1/ninos
```

### Obtener Terapeutas
```
GET /api/v1/personal
```

### Obtener Terapias
```
GET /api/v1/terapias
```

### Filtrar Terapeutas por Terapia
```
GET /api/v1/personal/por-terapia/{terapia_id}
```

### Obtener Citas por Fecha
```
GET /api/v1/citas-calendario/por-fecha?fecha=2026-01-15
```

### Crear Cita
```
POST /api/v1/citas-calendario
```

### Actualizar Cita
```
PUT /api/v1/citas-calendario/{id}
```

---

## 🎨 Colores de Estados

| Estado | Color | Significado |
|--------|-------|-------------|
| Programada | Azul | Cita confirmada y pendiente |
| Reprogramada | Naranja | Cita movida de su horario original |
| Cancelada | Rojo | Cita cancelada |

---

## ⚙️ Configuración Importante

**Cambio Realizado:** Se configuró `verTodo = true` para que el calendario muestre todas las citas por defecto al cargar.

**Archivo Modificado:**
[src/app/coordinador/asignar-terapias/asignar-terapias.component.ts](../../src/app/coordinador/asignar-terapias/asignar-terapias.component.ts#L145)

```typescript
verTodo = true; // 🔥 Mostrar todas las citas por defecto
```

---

## 📱 Responsividad

El calendario es **totalmente responsivo**:
- Desktop: Vista completa con sidebar
- Tablet: Sidebar colapsable (click ≡)
- Mobile: Interfaz optimizada (en desarrollo)

---

## 🐛 Troubleshooting

### Las citas no aparecen
- ✅ Verifica que el backend esté corriendo en puerto 8000
- ✅ Recarga la página (F5)
- ✅ Abre la consola (F12) y verifica que no haya errores

### El dropdown de terapeutas está vacío
- ✅ Primero selecciona una terapia válida
- ✅ Verifica que existan terapeutas especializados en esa terapia
- ✅ Consulta el endpoint `/api/v1/personal/por-terapia/{id}`

### Google Calendar no sincroniza
- ✅ Verifica que tengas una API key de Google configurada
- ✅ Revisa el archivo `.env` en el backend
- ✅ Consulta `GEMINI_API_KEY` y configuración de Google

---

## 📚 Documentación Relacionada

- [Componente de Asignar Terapias](../../src/app/coordinador/asignar-terapias/)
- [Servicio de Citas Calendario](../../src/app/service/citas-calendario.service.ts)
- [Interfaces de Cita](../../src/app/interfaces/cita.interface.ts)

---

## 🚀 Próximos Pasos

1. ✅ Crear citas desde el calendario (COMPLETADO)
2. ✅ Ver citas en vista semana (COMPLETADO)
3. ⏳ Mejorar vista mes (EN DESARROLLO)
4. ⏳ Exportar citas a PDF (PRÓXIMO)
5. ⏳ Enviar notificaciones a padres (PRÓXIMO)

---

**Última Actualización:** 13 de enero de 2026  
**Commit:** 858488a  
**Branch:** version-5246422

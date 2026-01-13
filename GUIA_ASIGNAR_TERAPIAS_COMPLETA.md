# 🎯 Guía Completa: Asignar Terapias a Niños

## Acceso a la Página

**URL:** `http://localhost:4200/coordinador/asignar-terapias`

---

## 📋 Flujo de Asignación de Terapias

### Paso 1: Cargar Catálogos

Cuando abres la página, se cargan automáticamente:

- ✅ **Niños:** Lista de todos los niños del sistema
- ✅ **Terapeutas:** Personal registrado como terapeutas
- ✅ **Terapias:** Tipos de terapias disponibles (Logopedia, Terapia Ocupacional, etc.)

### Paso 2: Abrindo el Modal de Nueva Terapia

Haz clic en el botón **"+ Nueva Terapia"** en la esquina superior derecha

### Paso 3: Llenar el Formulario

**Campos Obligatorios:**

1. **Niño:** Selecciona el niño que recibirá la terapia
2. **Terapeuta:** Selecciona el profesional que impartirá la terapia
3. **Tipo de Terapia:** Elige la terapia (Logopedia, Ocupacional, etc.)
4. **Fecha:** Selecciona la fecha de inicio
5. **Hora Inicio:** Ej: 09:00
6. **Hora Fin:** Ej: 10:00

**Campos Opcionales:**

- **Observaciones:** Notas sobre la sesión
- **Terapia Recurrente:** Activa si se repite semanalmente
  - Si activas esto:
    - Selecciona los **días de la semana** (Lunes, Martes, etc.)
    - Define **cantidad de semanas** que se repetirá
- **Sincronizar Google Calendar:** Crea evento en Google Calendar

### Paso 4: Vista Previa

- Haz clic en **"Previsualizar"** para ver todas las citas que se crearán
- Especialmente útil para terapias recurrentes

### Paso 5: Guardar

- Haz clic en **"Guardar Terapia"**
- Las citas se crearán en la base de datos y aparecerán en el calendario

---

## 📅 Visualización en el Calendario

### Vistas Disponibles

**1. Vista Día**

- Muestra todas las citas de un día específico
- Útil para ver el agenda por hora

**2. Vista Semana**

- Muestra los 7 días de la semana
- Ideal para planificación semanal

**3. Vista Mes**

- Panorámica completa del mes
- Útil para planificación estratégica

### Navegar por el Calendario

- **Botón "Hoy":** Vuelve a la fecha actual
- **Flechas ◄ ►:** Navega entre períodos
- **Clic en el título:** Abre selector de fecha

---

## 🔍 Filtros del Calendario

En la barra lateral izquierda puedes filtrar por:

1. **Niño:** Ver solo citas de un niño específico
2. **Terapeuta:** Ver solo citas de un terapeuta
3. **Tipo de Terapia:** Filtrar por tipo (Logopedia, etc.)
4. **Estados:**
   - ✅ Programadas
   - 🔄 Reprogramadas
   - ❌ Canceladas

**Botón "Limpiar Filtros":** Reinicia todos los filtros

---

## ✏️ Editar una Cita Existente

1. Haz clic en la cita en el calendario
2. Se abre un modal con los detalles
3. Modifica los campos que necesites
4. Haz clic en **"Guardar Cambios"**

---

## ❌ Cancelar una Cita

1. Haz clic en la cita
2. En el modal, haz clic en **"Cancelar Terapia"**
3. La cita cambiará a estado "Cancelada"
4. Aparecerá en rojo en el calendario

---

## 📊 Estadísticas Rápidas

La barra lateral muestra:

- **Total de Citas:** Número de sesiones programadas
- **Niños en Seguimiento:** Cuántos niños tienen terapias activas

---

## 🔄 Ejemplo Práctico: Crear Terapia Recurrente

**Objetivo:** Asignar sesiones de Logopedia a Juan cada lunes, miércoles y viernes durante 8 semanas

**Pasos:**

1. Abre "Nueva Terapia"
2. Selecciona niño: **Juan Pérez**
3. Selecciona terapeuta: **Dra. María López**
4. Selecciona terapia: **Logopedia**
5. Fecha de inicio: **Lunes 13 Enero 2025**
6. Hora: **10:00 - 11:00**
7. **Activa "Terapia Recurrente"**
8. Selecciona días: ✓ Lunes, ✓ Miércoles, ✓ Viernes
9. Cantidad de semanas: **8**
10. Haz clic **"Previsualizar"** - verás 24 citas (8 semanas × 3 días)
11. Haz clic **"Guardar Terapia"**
12. ✅ Se crean 24 sesiones automáticamente

**Resultado en Calendario:**

- Todas las sesiones aparecen en sus respectivos días
- Color distintivo según tipo de terapia
- Puedes hacer clic en cualquiera para editar o cancelar

---

## ⚙️ Integración con Google Calendar

Si tienes Google Calendar conectado:

- Activa **"Sincronizar Google Calendar"** al crear la terapia
- Las citas aparecerán automáticamente en tu Google Calendar
- Los cambios se sincronizan en ambos sentidos

---

## 💡 Consejos Prácticos

1. **Usa filtros** para evitar sobrecargar el calendario
2. **Revisa la previsualización** antes de guardar terapias recurrentes
3. **Colorea mentalmente:** Cada terapeuta puede tener un color asignado en el calendario
4. **Exporta datos:** El calendario tiene opciones de exportación/impresión

---

## ❌ Solución de Problemas

| Problema                    | Solución                                      |
| --------------------------- | --------------------------------------------- |
| No aparecen niños           | Recarga la página (Ctrl+F5)                   |
| La cita no se guarda        | Verifica que todos los campos estén llenos    |
| Calendario vacío            | Aplica filtros - quizá estén muy restrictivos |
| Error al sincronizar Google | Verifica que Google Calendar esté conectado   |

---

## 📞 Resumen de Endpoints API Utilizados

- **POST** `/citas-calendario/` - Crear nueva cita
- **GET** `/citas-calendario/` - Obtener citas (con filtros)
- **PUT** `/citas-calendario/{id}` - Actualizar cita
- **PATCH** `/citas-calendario/{id}/estado/{estado_id}` - Cambiar estado

---

¡El coordinador ahora puede asignar terapias a los niños de forma visual y sencilla! 🎉

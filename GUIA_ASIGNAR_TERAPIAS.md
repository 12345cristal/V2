# Interfaz de Asignación de Terapias - Coordinador

## Descripción General

Este módulo permite a los **Coordinadores** asignar sesiones de terapia a niños con terapeutas específicos, con sincronización automática a Google Calendar.

## Ubicación en la Aplicación

**Ruta:** `/coordinador/asignar-terapias`

**Navegación desde el menú:**
- Login como COORDINADOR
- Ir a **Módulo Terapias**
- Seleccionar **Asignar Terapias**

## Características Principales

### 1. **Selección de Datos Principales**
- **Niño:** Selecciona el niño que recibirá la terapia
- **Terapeuta:** Elige el profesional que impartirá la terapia
- **Tipo de Terapia:** Selecciona el tipo de terapia según su duración

### 2. **Configuración de Horarios**
- **Fecha de Inicio:** Selecciona el día de inicio (mínimo mañana)
- **Duración:** Define cuántas semanas durará el programa
- **Días de la Semana:** Marca los días que se repetirá (Lunes a Sábado)
- **Hora de Inicio y Fin:** Define el horario de cada sesión
  - Las horas se ajustan automáticamente según la duración de la terapia

### 3. **Sincronización con Google Calendar**
- **Checkbox:** "Sincronizar automáticamente con Google Calendar"
- Si está activo, todas las citas se crearán como eventos en el calendario de Google
- Incluye recordatorios automáticos para el terapeuta

### 4. **Previsualización**
- Haz clic en **"Previsualizar"** para ver todas las citas que se crearán
- Se muestra:
  - Resumen de datos (niño, terapeuta, terapia, total de citas)
  - Lista de todas las sesiones programadas
  - Opción para volver atrás o confirmar la creación

### 5. **Creación de Citas**
- Haz clic en **"Asignar Terapias"** para crear todas las citas
- El sistema las crea una por una
- Si está habilitada la sincronización, cada cita se refleja en Google Calendar
- Se muestra un mensaje de confirmación al terminar

## Flujo de Uso

```
1. Seleccionar Niño
   ↓
2. Seleccionar Terapeuta
   ↓
3. Seleccionar Tipo de Terapia
   ↓
4. Configurar Fecha, Días y Horario
   ↓
5. Activar sincronización con Google (opcional)
   ↓
6. Previsualizar citas (recomendado)
   ↓
7. Confirmar creación
   ↓
8. Sistema crea todas las citas y sincroniza
```

## Validaciones

El formulario valida:
- ✅ Debe seleccionar niño, terapeuta y terapia
- ✅ Debe seleccionar al menos un día de la semana
- ✅ Debe ingresar fecha de inicio válida
- ✅ La hora de fin debe ser posterior a la de inicio
- ✅ La duración debe estar entre 1 y 52 semanas

## Ejemplo Práctico

**Caso:** Asignar terapia ocupacional a Juan García

1. **Niño:** Juan García Pérez
2. **Terapeuta:** Dra. María López Silva - Especialidad: Terapia Ocupacional
3. **Terapia:** Terapia Ocupacional - 60 minutos
4. **Fecha de Inicio:** 20 de diciembre de 2024
5. **Duración:** 4 semanas
6. **Días:** Lunes, Miércoles, Viernes
7. **Horario:** 9:00 AM - 10:00 AM
8. **Sincronización:** Activada

**Resultado:**
- Se crearán 12 citas (4 semanas × 3 días)
- Cada cita aparecerá en el calendario de Google del terapeuta
- Las citas estarán listadas en el módulo de Citas

## Integración con Google Calendar

Cuando la sincronización está **ACTIVA**:

✅ Cada cita se crea como un evento de Google Calendar  
✅ El evento incluye:
- Título: "Terapia Ocupacional - Juan García"
- Descripción: Datos del paciente y tipo de terapia
- Horario: Exacto a la hora programada
- Recordatorios: 24 horas y 30 minutos antes

✅ El evento está vinculado en la BD con `google_event_id`  
✅ Puede abrirse directamente desde la aplicación

## Mensajes de Confirmación

### Éxito ✅
- "Se crearon 12 citas exitosamente y se sincronizaron con Google Calendar"
- Todos los campos se limpian automáticamente
- Las citas quedan disponibles en el módulo de Citas

### Error ⚠️
- "Debe seleccionar un niño"
- "La hora de inicio debe ser anterior a la hora de fin"
- etc.

## Botones de Acción

| Botón | Función |
|-------|---------|
| **Previsualizar** | Ver listado de citas a crear (sin crear nada) |
| **Asignar Terapias** | Crear todas las citas en la BD y Google Calendar |
| **Limpiar** | Resetear el formulario |

## Notas Importantes

⚠️ **Requisitos:**
- Google Calendar debe estar configurado (ver documentación de backend)
- El terapeuta debe tener una cuenta de Google Calendar
- La cita debe ser futura (mínimo mañana)

⚠️ **Permisos:**
- Solo COORDINADOR y ADMIN pueden acceder
- COORDINADOR solo puede crear citas, no modificarlas (ver módulo Citas)

⚠️ **Sincronización:**
- Si Google Calendar no está disponible, la cita se crea en la BD pero NO sincroniza
- Puedes reintentarlo desde el módulo de Citas

## Troubleshooting

### Problema: No se crea la cita
**Solución:** Verifica que todos los campos estén completos

### Problema: Google Calendar no sincroniza
**Solución:** 
1. Verifica configuración de Google en backend
2. Revisa que el terapeuta tenga Google Calendar activo
3. Intenta nuevamente desde módulo Citas

### Problema: Horario incorrecto
**Solución:** La hora de fin se calcula automáticamente con la duración de la terapia. Ajusta si es necesario.

## Versión
- Última actualización: Diciembre 2024
- Estado: PRODUCCIÓN
- Autor: Sistema de Terapias

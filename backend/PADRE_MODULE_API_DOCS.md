# Módulo Padre - Documentación de Endpoints

Este documento describe todos los endpoints implementados para el módulo Padre (Dashboard de Padres/Tutores).

## Autenticación

Todos los endpoints requieren autenticación mediante JWT token:
- Header: `Authorization: Bearer <token>`
- El token debe ser de un usuario con rol_id = 4 (Padre/Tutor)
- Los padres solo pueden acceder a sus propios datos y los de sus hijos

## Base URL

```
http://localhost:8000/api/v1/padre
```

## Endpoints por Módulo

### 1. Dashboard

#### GET /dashboard/{padre_id}
Obtiene el resumen completo del dashboard del padre.

**Respuesta incluye:**
- Información del padre
- Próxima sesión programada
- Avance de cada hijo (progreso, sesiones, objetivos)
- Pagos pendientes
- Documentos nuevos
- Mensajes no leídos
- Notificaciones
- Tareas pendientes
- Observaciones recientes

**Ejemplo de respuesta:**
```json
{
  "padre": {
    "id": 1,
    "nombres": "Juan",
    "apellido_paterno": "Pérez",
    "email": "juan@example.com",
    "activo": true
  },
  "proxima_sesion": {
    "id": 1,
    "hijo_nombre": "María Pérez",
    "terapia": "Lenguaje",
    "terapeuta": "Ana García",
    "fecha": "2026-01-15T10:00:00",
    "duracion_minutos": 60
  },
  "hijos": [...],
  "pagos_pendientes": 0,
  "mensajes_no_leidos": 3
}
```

### 2. Mis Hijos

#### GET /hijos/{padre_id}
Lista todos los hijos del padre.

#### GET /hijos/{hijo_id}/detalle
Obtiene detalles completos de un hijo específico.

#### GET /hijos/{hijo_id}/alergias
Lista solo las alergias del hijo.

#### GET /hijos/{hijo_id}/medicamentos
Lista los medicamentos actuales del hijo.

#### PUT /hijos/{hijo_id}
Actualiza información básica del hijo (solo datos permitidos para el padre).

**Body:**
```json
{
  "nombre": "María",
  "apellido_paterno": "Pérez",
  "telefono_emergencia": "6681234567"
}
```

### 3. Sesiones

#### GET /sesiones/hoy/{hijo_id}
Obtiene las sesiones programadas para hoy.

#### GET /sesiones/programadas/{hijo_id}
Obtiene sesiones futuras programadas (límite: 20 sesiones).

#### GET /sesiones/semana/{hijo_id}?fecha=2026-01-12
Obtiene sesiones de la semana (lunes a domingo).
- `fecha` (opcional): Fecha de referencia, por defecto hoy

#### GET /sesiones/{sesion_id}/detalle
Obtiene detalles completos de una sesión específica.

**Respuesta incluye:**
- Información básica (fecha, hora, terapeuta, terapia)
- Duración
- Objetivos trabajados
- Actividades realizadas
- Progreso porcentual
- Comentarios del terapeuta
- Materiales usados
- Recomendaciones

#### GET /sesiones/{sesion_id}/bitacora
Descarga la bitácora diaria en PDF (en desarrollo).

#### GET /sesiones/{sesion_id}/grabacion
Descarga la grabación de la sesión (en desarrollo).

#### POST /sesiones/{sesion_id}/comentarios
El terapeuta agrega comentarios a la sesión.

**Body:**
```json
{
  "comentario": "Excelente progreso en lenguaje expresivo",
  "progreso_porcentaje": 85,
  "recomendaciones": "Practicar ejercicios en casa"
}
```

### 4. Historial Terapéutico

#### GET /historial/{hijo_id}?periodo=mes&mes=01&año=2026
Obtiene datos del historial para gráficas.

**Parámetros:**
- `periodo`: mes|trimestre|semestre|año
- `mes`: 1-12 (opcional)
- `año`: 2020-2030 (opcional)

#### GET /historial/{hijo_id}/asistencia
Obtiene datos de asistencia por mes.

#### GET /historial/{hijo_id}/evolucion
Obtiene evolución de objetivos terapéuticos.

#### GET /historial/{hijo_id}/frecuencia
Obtiene frecuencia de terapias.

#### GET /historial/{hijo_id}/reporte?periodo=mes
Descarga reporte del historial en PDF (en desarrollo).

### 5. Tareas

#### GET /tareas/{hijo_id}?estado=PENDIENTE
Lista tareas del hijo con filtro opcional por estado.

**Estados disponibles:**
- PENDIENTE
- EN_PROGRESO
- COMPLETADA
- VENCIDA

#### GET /tareas/detalle/{tarea_id}
Obtiene detalle de una tarea específica.

#### PUT /tareas/{tarea_id}/estado
Actualiza el estado de una tarea.

**Body:**
```json
{
  "estado": "COMPLETADA",
  "fecha_completada": "2026-01-12T15:30:00",
  "notas_padre": "Completada con éxito"
}
```

#### GET /tareas/{tarea_id}/recursos
Obtiene recursos asociados a una tarea.

### 6. Pagos

#### GET /pagos/{padre_id}/info
Obtiene información del plan de pago y saldo actual.

**Respuesta:**
```json
{
  "plan": {
    "nombre": "Plan Básico",
    "monto_mensual": 5000.0,
    "fecha_corte": 15,
    "terapias_incluidas": 3,
    "sesiones_mes": 12
  },
  "saldo_actual": 0.0,
  "proximo_vencimiento": "2026-02-15",
  "dias_para_vencimiento": 34,
  "meses_adeudados": 0
}
```

#### GET /pagos/{padre_id}/historial
Obtiene historial de pagos realizados.

#### GET /pagos/{padre_id}/historial/{pago_id}/comprobante
Descarga comprobante de un pago específico (en desarrollo).

#### GET /pagos/{padre_id}/reporte
Descarga reporte completo de pagos en PDF (en desarrollo).

### 7. Documentos

#### GET /documentos/{hijo_id}
Lista todos los documentos del hijo.

**Tipos de documentos:**
- INFORME
- EVALUACION
- CONSENTIMIENTO
- PLAN_TERAPEUTICO
- BITACORA
- REPORTE
- OTRO

#### GET /documentos/detalle/{documento_id}
Descarga o visualiza el documento PDF.

#### PUT /documentos/{documento_id}/leido
Marca un documento como visto.

#### GET /documentos/{documento_id}/preview
Obtiene preview del documento (en desarrollo).

### 8. Recursos Recomendados

#### GET /recursos/{hijo_id}
Lista recursos recomendados por los terapeutas.

**Tipos de recursos:**
- PDF
- VIDEO
- AUDIO
- IMAGEN
- ENLACE
- EJERCICIO

#### GET /recursos/filtrar?tipo=PDF&terapeuta_id=1&objetivo=lenguaje
Filtra recursos por tipo, terapeuta u objetivo.

#### PUT /recursos/{recurso_id}/visto
Marca un recurso como visto.

### 9. Mensajes

#### GET /chats/{padre_id}
Lista todos los chats activos del padre.

**Tipos de chat:**
- PADRE_TERAPEUTA
- PADRE_COORDINADOR
- GRUPO_TERAPEUTAS

#### GET /chats/{chat_id}/mensajes?limite=50
Obtiene historial de mensajes (límite: 1-200).

#### POST /chats/{chat_id}/mensajes
Envía un mensaje nuevo.

**Body:**
```json
{
  "contenido": "Hola, tengo una pregunta sobre la tarea",
  "tipo": "TEXTO",
  "archivo_url": null
}
```

**Tipos de mensaje:**
- TEXTO
- AUDIO
- ARCHIVO
- IMAGEN

#### GET /chats/{chat_id}/mensajes/{mensaje_id}
Obtiene detalle de un mensaje específico.

### 10. Notificaciones

#### GET /notificaciones/{padre_id}?leidas=false
Lista notificaciones con filtro opcional.

**Tipos de notificaciones:**
- SESION_PROXIMA
- SESION_CANCELADA
- TAREA_ASIGNADA
- DOCUMENTO_NUEVO
- MENSAJE_NUEVO
- PAGO_PENDIENTE
- PAGO_RECIBIDO
- OBSERVACION_NUEVA

#### PUT /notificaciones/{notificacion_id}/leida
Marca una notificación como leída.

#### DELETE /notificaciones/{notificacion_id}
Elimina una notificación.

### 11. Perfil y Accesibilidad

#### GET /perfil/{padre_id}
Obtiene datos del perfil del padre.

#### PUT /perfil/{padre_id}
Actualiza el perfil del padre.

**Body:**
```json
{
  "nombres": "Juan Carlos",
  "telefono": "6681234567",
  "ocupacion": "Ingeniero"
}
```

#### GET /accesibilidad/{padre_id}
Obtiene preferencias de accesibilidad.

#### PUT /accesibilidad/{padre_id}
Actualiza preferencias de accesibilidad.

**Body:**
```json
{
  "tamaño_fuente": "GRANDE",
  "contraste_alto": true,
  "modo_oscuro": false,
  "lectura_voz": true,
  "subtitulos_video": true,
  "notificaciones_sonido": true,
  "notificaciones_vibracion": true
}
```

**Opciones de tamaño de fuente:**
- PEQUEÑO
- NORMAL
- GRANDE
- MUY_GRANDE

## Códigos de Estado HTTP

- **200**: Solicitud exitosa
- **201**: Recurso creado exitosamente
- **400**: Error de validación en la solicitud
- **401**: No autenticado (token inválido o ausente)
- **403**: No autorizado (sin permisos para esta acción)
- **404**: Recurso no encontrado
- **500**: Error interno del servidor
- **501**: Funcionalidad no implementada (en desarrollo)

## Manejo de Errores

Todos los errores retornan un JSON con el formato:

```json
{
  "detail": "Descripción del error"
}
```

Para errores de validación (400):

```json
{
  "detail": "Error de validación en la solicitud",
  "errores": [
    {
      "campo": "body -> email",
      "mensaje": "value is not a valid email address",
      "tipo": "value_error.email"
    }
  ]
}
```

## Paginación

Los endpoints que retornan listas incluyen paginación:

```json
{
  "total": 45,
  "page": 1,
  "page_size": 20,
  "total_pages": 3,
  "items": [...]
}
```

## Documentación Interactiva

Accede a la documentación interactiva en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notas de Implementación

- Algunos endpoints están marcados como "en desarrollo" y retornan HTTP 501
- Los TODOs indican funcionalidad que requiere modelos adicionales en la base de datos
- La lógica de cálculo de progreso y objetivos está simulada y debe implementarse según requerimientos específicos
- Los padres solo pueden acceder a información de sus propios hijos mediante validación de tutor_id

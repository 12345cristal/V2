# 📋 ENDPOINTS DEL BACKEND - Autismo Mochis IA

Base URL: `http://localhost:8000/api/v1`

## 🔐 AUTENTICACIÓN

### POST /api/v1/auth/login
- **Descripción**: Iniciar sesión
- **Body**: `{"email": "string", "password": "string"}`
- **Response**: `{"access_token": "string", "token_type": "bearer", "usuario": {...}}`

### POST /api/v1/auth/change-password
- **Descripción**: Cambiar contraseña del usuario autenticado
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"current_password": "string", "new_password": "string"}`

### GET /api/v1/auth/me
- **Descripción**: Obtener información del usuario actual
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{...usuario_info}`

---

## 👥 USUARIOS

### GET /api/v1/usuarios
- **Descripción**: Listar usuarios con filtros y paginación
- **Query Params**: `skip`, `limit`, `search`, `rol_id`, `activo`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/usuarios
- **Descripción**: Crear nuevo usuario
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...usuario_data}`

### GET /api/v1/usuarios/{usuario_id}
- **Descripción**: Obtener usuario por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/usuarios/{usuario_id}
- **Descripción**: Actualizar usuario
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...usuario_data}`

### DELETE /api/v1/usuarios/{usuario_id}
- **Descripción**: Eliminar usuario
- **Headers**: `Authorization: Bearer TOKEN`

### PATCH /api/v1/usuarios/{usuario_id}/toggle-activo
- **Descripción**: Activar/desactivar usuario
- **Headers**: `Authorization: Bearer TOKEN`

---

## 🎭 ROLES Y PERMISOS

### GET /api/v1/roles
- **Descripción**: Listar roles
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/roles
- **Descripción**: Crear nuevo rol
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"nombre": "string", "descripcion": "string"}`

### GET /api/v1/roles/{rol_id}
- **Descripción**: Obtener rol por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/roles/{rol_id}
- **Descripción**: Actualizar rol
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/roles/{rol_id}/permisos
- **Descripción**: Asignar permisos a un rol
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"permiso_ids": [1, 2, 3]}`

### GET /api/v1/permisos
- **Descripción**: Listar todos los permisos disponibles
- **Headers**: `Authorization: Bearer TOKEN`

---

## 👨‍⚕️ PERSONAL (TERAPEUTAS)

### GET /api/v1/personal
- **Descripción**: Listar personal con filtros
- **Query Params**: `skip`, `limit`, `search`, `activo`, `especialidad_id`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/personal
- **Descripción**: Crear nuevo personal (terapeuta)
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...personal_data}`

### GET /api/v1/personal/{personal_id}
- **Descripción**: Obtener personal por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/personal/{personal_id}
- **Descripción**: Actualizar personal
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/personal/{personal_id}
- **Descripción**: Eliminar personal
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/personal/{personal_id}/perfil
- **Descripción**: Crear perfil extendido del personal
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...perfil_data}`

### PUT /api/v1/personal/{personal_id}/perfil
- **Descripción**: Actualizar perfil del personal
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/personal/{personal_id}/horarios
- **Descripción**: Listar horarios del personal
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/personal/horarios
- **Descripción**: Crear horario para personal
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"personal_id": 1, "dia_semana": "LUNES", "hora_inicio": "08:00", "hora_fin": "16:00"}`

### PUT /api/v1/personal/horarios/{horario_id}
- **Descripción**: Actualizar horario
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/personal/horarios/{horario_id}
- **Descripción**: Eliminar horario
- **Headers**: `Authorization: Bearer TOKEN`

---

## 👨‍👩‍👧 TUTORES (PADRES/TUTORES)

### GET /api/v1/tutores
- **Descripción**: Listar tutores
- **Query Params**: `skip`, `limit`, `search`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/tutores
- **Descripción**: Crear nuevo tutor
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...tutor_data}`

### GET /api/v1/tutores/{tutor_id}
- **Descripción**: Obtener tutor por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/tutores/{tutor_id}
- **Descripción**: Actualizar tutor
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/tutores/{tutor_id}
- **Descripción**: Eliminar tutor
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/tutores/{tutor_id}/ninos
- **Descripción**: Obtener niños asociados a un tutor
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/tutores/usuario/{usuario_id}
- **Descripción**: Obtener tutor por usuario_id
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/tutores/{tutor_id}/tiene-acceso/{nino_id}
- **Descripción**: Verificar si el tutor tiene acceso a un niño
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{"tiene_acceso": true/false}`

---

## 👶 NIÑOS (BENEFICIARIOS)

### GET /api/v1/ninos
- **Descripción**: Listar niños con filtros y paginación
- **Query Params**: `skip`, `limit`, `search`, `estado`, `tutor_id`
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{"items": [...], "total": 50, "skip": 0, "limit": 100}`

### POST /api/v1/ninos
- **Descripción**: Crear nuevo niño
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...nino_data}`

### GET /api/v1/ninos/{nino_id}
- **Descripción**: Obtener niño por ID (con datos completos)
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/ninos/{nino_id}
- **Descripción**: Actualizar niño
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/ninos/{nino_id}
- **Descripción**: Eliminar niño
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/ninos/{nino_id}/direccion
- **Descripción**: Obtener dirección del niño
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/ninos/{nino_id}/direccion
- **Descripción**: Crear dirección del niño
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/ninos/{nino_id}/direccion
- **Descripción**: Actualizar dirección del niño
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/ninos/{nino_id}/diagnostico
- **Descripción**: Obtener diagnóstico del niño
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/ninos/{nino_id}/diagnostico
- **Descripción**: Crear diagnóstico del niño
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/ninos/{nino_id}/diagnostico
- **Descripción**: Actualizar diagnóstico del niño
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/ninos/{nino_id}/info-emocional
- **Descripción**: Obtener información emocional del niño
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/ninos/{nino_id}/info-emocional
- **Descripción**: Crear información emocional del niño
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/ninos/{nino_id}/info-emocional
- **Descripción**: Actualizar información emocional del niño
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/ninos/{nino_id}/archivos
- **Descripción**: Obtener archivos del niño (acta, CURP, comprobante)
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/ninos/{nino_id}/archivos
- **Descripción**: Crear registro de archivos del niño
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/ninos/{nino_id}/archivos
- **Descripción**: Actualizar archivos del niño
- **Headers**: `Authorization: Bearer TOKEN`

---

## 🧩 TERAPIAS Y SESIONES

### GET /api/v1/terapias
- **Descripción**: Listar terapias disponibles
- **Query Params**: `activo`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/terapias
- **Descripción**: Crear nueva terapia
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"nombre": "string", "descripcion": "string", "tipo_terapia_id": 1}`

### GET /api/v1/terapias/{terapia_id}
- **Descripción**: Obtener terapia por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/terapias/{terapia_id}
- **Descripción**: Actualizar terapia
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/terapias/{terapia_id}
- **Descripción**: Eliminar terapia
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/terapias/{terapia_id}/personal/{personal_id}
- **Descripción**: Asignar personal a terapia
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/terapias/{terapia_id}/personal/{personal_id}
- **Descripción**: Desasignar personal de terapia
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/terapias/nino/{nino_id}
- **Descripción**: Obtener terapias asignadas a un niño
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/terapias/asignar-nino
- **Descripción**: Asignar terapia a un niño
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"nino_id": 1, "terapia_id": 2, "terapeuta_id": 3, "prioridad_id": 1}`

### PUT /api/v1/terapias/asignaciones/{asignacion_id}
- **Descripción**: Actualizar asignación de terapia
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/terapias/asignaciones/{asignacion_id}
- **Descripción**: Eliminar asignación de terapia
- **Headers**: `Authorization: Bearer TOKEN`

---

## 📅 SESIONES

### GET /api/v1/sesiones
- **Descripción**: Listar sesiones
- **Query Params**: `skip`, `limit`, `nino_id`, `terapeuta_id`, `fecha_inicio`, `fecha_fin`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/sesiones
- **Descripción**: Crear nueva sesión
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...sesion_data}`

### GET /api/v1/sesiones/{sesion_id}
- **Descripción**: Obtener sesión por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/sesiones/{sesion_id}
- **Descripción**: Actualizar sesión
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/sesiones/{sesion_id}
- **Descripción**: Eliminar sesión
- **Headers**: `Authorization: Bearer TOKEN`

---

## 🔁 REPOSICIONES

### GET /api/v1/reposiciones
- **Descripción**: Listar reposiciones de sesiones
- **Query Params**: `skip`, `limit`, `estado`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/reposiciones
- **Descripción**: Crear solicitud de reposición
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...reposicion_data}`

### PUT /api/v1/reposiciones/{reposicion_id}
- **Descripción**: Actualizar reposición
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/reposiciones/{reposicion_id}/aprobar
- **Descripción**: Aprobar reposición
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/reposiciones/{reposicion_id}/rechazar
- **Descripción**: Rechazar reposición
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"motivo_rechazo": "string"}`

---

## 📅 CITAS

### GET /api/v1/citas
- **Descripción**: Listar citas
- **Query Params**: `skip`, `limit`, `nino_id`, `personal_id`, `estado`, `fecha_inicio`, `fecha_fin`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/citas
- **Descripción**: Crear nueva cita
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...cita_data}`

### GET /api/v1/citas/{cita_id}
- **Descripción**: Obtener cita por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/citas/{cita_id}
- **Descripción**: Actualizar cita
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/citas/{cita_id}
- **Descripción**: Eliminar cita
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/citas/fecha/{fecha}
- **Descripción**: Obtener citas de una fecha específica
- **Headers**: `Authorization: Bearer TOKEN`
- **Params**: `fecha` (formato: YYYY-MM-DD)

### POST /api/v1/citas/{cita_id}/asistencia
- **Descripción**: Marcar asistencia a cita
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"asistio": true, "observaciones": "string"}`

### POST /api/v1/citas/{cita_id}/cancelar
- **Descripción**: Cancelar cita
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"motivo": "string"}`

---

## 📚 RECURSOS EDUCATIVOS

### GET /api/v1/recursos
- **Descripción**: Listar recursos educativos
- **Query Params**: `skip`, `limit`, `tipo`, `categoria`, `nivel`
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/recursos
- **Descripción**: Crear nuevo recurso
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...recurso_data}`

### GET /api/v1/recursos/{recurso_id}
- **Descripción**: Obtener recurso por ID
- **Headers**: `Authorization: Bearer TOKEN`

### PUT /api/v1/recursos/{recurso_id}
- **Descripción**: Actualizar recurso
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/recursos/{recurso_id}
- **Descripción**: Eliminar recurso
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/recursos/asignar-tarea
- **Descripción**: Asignar tarea (recurso) a un niño
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"recurso_id": 1, "nino_id": 2, "personal_id": 3, "fecha_limite": "2024-12-31"}`

### GET /api/v1/recursos/tareas/nino/{nino_id}
- **Descripción**: Obtener tareas asignadas a un niño
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/recursos/tareas/{tarea_id}/completar
- **Descripción**: Marcar tarea como completada
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"observaciones": "string"}`

---

## 🔔 NOTIFICACIONES

### GET /api/v1/notificaciones/mis-notificaciones
- **Descripción**: Obtener notificaciones del usuario actual
- **Query Params**: `skip`, `limit`, `leida`
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/notificaciones/no-leidas/count
- **Descripción**: Contar notificaciones no leídas
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{"count": 5}`

### POST /api/v1/notificaciones/{notificacion_id}/marcar-leida
- **Descripción**: Marcar notificación como leída
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/notificaciones/marcar-todas-leidas
- **Descripción**: Marcar todas las notificaciones como leídas
- **Headers**: `Authorization: Bearer TOKEN`

### DELETE /api/v1/notificaciones/{notificacion_id}
- **Descripción**: Eliminar notificación
- **Headers**: `Authorization: Bearer TOKEN`

### POST /api/v1/notificaciones/admin/crear
- **Descripción**: Crear notificación (solo admin)
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"usuario_id": 1, "tipo": "INFO", "titulo": "string", "mensaje": "string"}`

---

## 📊 PRIORIZACIÓN (TOPSIS)

### POST /api/v1/priorizacion/topsis
- **Descripción**: Ejecutar algoritmo TOPSIS genérico
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{...topsis_data}`

### POST /api/v1/priorizacion/ninos
- **Descripción**: Priorizar niños usando TOPSIS
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"terapia_id": 1}`

### POST /api/v1/priorizacion/terapeutas
- **Descripción**: Priorizar terapeutas usando TOPSIS
- **Headers**: `Authorization: Bearer TOKEN`
- **Body**: `{"nino_id": 1, "terapia_id": 2}`

### GET /api/v1/priorizacion/logs
- **Descripción**: Obtener logs de decisiones de priorización
- **Query Params**: `skip`, `limit`, `tipo_decision`
- **Headers**: `Authorization: Bearer TOKEN`

---

## 🤖 INTELIGENCIA ARTIFICIAL (GEMINI)

### POST /api/v1/ia/resumen-progreso/{nino_id}
- **Descripción**: Generar resumen de progreso con IA
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{"resumen": "string", "recomendaciones": "string"}`

### POST /api/v1/ia/sugerencias-recursos/{nino_id}
- **Descripción**: Sugerir recursos usando IA
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**: `{"sugerencias": [...]}`

### GET /api/v1/ia/analizar-dashboard
- **Descripción**: Analizar datos del dashboard con IA
- **Headers**: `Authorization: Bearer TOKEN`

### GET /api/v1/ia/status
- **Descripción**: Verificar si la IA está disponible
- **Response**: `{"disponible": true/false, "modelo": "string"}`

---

## 📈 DASHBOARD COORDINADOR

### GET /api/v1/coordinador/dashboard
- **Descripción**: Obtener estadísticas del dashboard del coordinador
- **Headers**: `Authorization: Bearer TOKEN`
- **Response**:
```json
{
  "total_ninos": 50,
  "total_terapeutas": 10,
  "total_terapias_activas": 15,
  "total_citas_hoy": 8,
  "citas_pendientes": 5,
  "progreso_promedio": 75.5,
  "ninos_nuevos_mes": 3,
  "total_sesiones": 150,
  "tasa_asistencia": 92.5,
  "terapias_mas_demandadas": [...],
  "terapeutas_con_mas_pacientes": [...],
  "fecha_consulta": "2024-12-08"
}
```

---

## ⚕️ HEALTH CHECK

### GET /health
- **Descripción**: Verificar estado del servidor
- **Response**: `{"status": "ok", "timestamp": "..."}`

### GET /
- **Descripción**: Endpoint raíz
- **Response**: `{"message": "Autismo Mochis IA - API v1.0"}`

---

## 📝 NOTAS IMPORTANTES

1. **Autenticación**: La mayoría de los endpoints requieren token JWT en el header:
   ```
   Authorization: Bearer <tu_token_aqui>
   ```

2. **Paginación**: Los endpoints de listado usan `skip` y `limit`:
   - `skip`: Número de registros a saltar (default: 0)
   - `limit`: Máximo de registros a retornar (default: 100)

3. **Filtros**: Muchos endpoints permiten búsqueda con `search` (busca en múltiples campos)

4. **Respuestas paginadas**: Formato estándar:
   ```json
   {
     "items": [...],
     "total": 100,
     "skip": 0,
     "limit": 50
   }
   ```

5. **WebSocket**: Para notificaciones en tiempo real:
   - URL: `ws://localhost:8000/ws?token=<tu_token_jwt>`
   - Requiere token JWT en query string

6. **Documentación interactiva**:
   - Swagger UI: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

---

## 🚨 ERRORES COMUNES

- **401 Unauthorized**: Token inválido o expirado
- **403 Forbidden**: Usuario no tiene permisos para la acción
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Error de validación en los datos enviados
- **500 Internal Server Error**: Error del servidor (revisar logs)

---

**Total de Endpoints**: **105**
- GET: 40
- POST: 35
- PUT: 17
- PATCH: 1
- DELETE: 12

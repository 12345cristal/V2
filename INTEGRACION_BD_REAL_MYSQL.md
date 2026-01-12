# Integración Base de Datos Real MySQL: autismo_mochis_ia

## 📋 Resumen de Cambios

Esta actualización reemplaza completamente la estructura de datos mock por la integración real con la base de datos MySQL `autismo_mochis_ia`.

## 🗄️ Estructura de Base de Datos

### Tablas Principales

#### `ninos`
- Información de los niños beneficiarios
- Relaciones: tutores, direcciones, diagnósticos, terapias, tareas, pagos

#### `recursos`
- Recursos educativos y terapéuticos
- Catálogos: tipos, categorías, niveles
- Asignación a tareas

#### `tareas_recurso`
- Asignación de recursos a niños
- Seguimiento de completado
- Evidencias subidas por padres
- Estadísticas de progreso

#### `terapias_nino`
- Asignación de terapias a niños
- Frecuencia y prioridad
- Terapeutas asignados

#### `planes_pago`
- Planes de pago para servicios
- Soporte para abonos
- Cálculo automático de saldos

#### `pagos`
- Registro de pagos realizados
- Comprobantes y referencias
- Historial completo

#### `notificaciones`
- Sistema de notificaciones actualizado
- Títulos y tipos mejorados

## 🔧 Backend (FastAPI + SQLAlchemy)

### Modelos Creados/Actualizados

**Nuevos:**
- `app/models/recurso.py` - Recursos y catálogos
- `app/models/tarea_recurso.py` - Tareas asignadas
- `app/models/plan_pago.py` - Planes de pago

**Actualizados:**
- `app/models/pago.py` - Nueva estructura con plan_id
- `app/models/notificacion.py` - Campos actualizados
- `app/models/nino.py` - Relaciones agregadas

### Schemas Pydantic

Todos los schemas incluyen:
- Modelos Base (validación)
- Create (creación)
- Update (actualización)
- Response (respuesta completa)
- ListItem (versión simplificada)

Ubicación: `app/schemas/`

### Routers FastAPI

**Nuevos Routers:**

1. **`/api/v1/recursos`**
   - GET / - Listar recursos con filtros
   - GET /{id} - Obtener recurso
   - POST / - Crear recurso
   - PUT /{id} - Actualizar recurso
   - DELETE /{id} - Eliminar recurso
   - GET /destacados/listar - Recursos destacados
   - GET /tipos, /categorias, /niveles - Catálogos

2. **`/api/v1/tareas-recurso`**
   - GET /nino/{id} - Listar tareas de niño
   - GET /{id} - Obtener tarea
   - POST / - Crear tarea
   - PUT /{id} - Actualizar tarea
   - POST /{id}/completar - Marcar completada (con evidencia)
   - DELETE /{id} - Eliminar tarea
   - GET /nino/{id}/estadisticas - Estadísticas de tareas

3. **`/api/v1/planes-pago`**
   - GET / - Listar planes
   - GET /nino/{id} - Planes de un niño
   - GET /{id} - Obtener plan
   - POST / - Crear plan
   - PUT /{id} - Actualizar plan
   - DELETE /{id} - Eliminar plan
   - GET /{id}/saldo - Calcular saldo
   - POST /{id}/recalcular - Recalcular plan

4. **`/api/v1/pagos`**
   - GET / - Listar pagos
   - GET /plan/{id} - Pagos de un plan
   - GET /{id} - Obtener pago
   - POST / - Registrar pago
   - PUT /{id} - Actualizar pago
   - DELETE /{id} - Eliminar pago
   - GET /usuario/{id}/historial - Historial de usuario

5. **`/api/v1/ninos`**
   - GET / - Listar niños
   - GET /tutor/{id} - Niños de un tutor
   - GET /{id} - Obtener niño completo
   - POST / - Crear niño
   - PUT /{id} - Actualizar niño
   - DELETE /{id} - Eliminar niño

6. **`/api/v1/terapias-nino`**
   - GET /nino/{id} - Terapias de un niño
   - GET /activas/nino/{id} - Solo terapias activas
   - GET /terapeuta/{id}/ninos - Niños de un terapeuta
   - GET /{id} - Obtener asignación
   - POST / - Asignar terapia
   - PUT /{id} - Actualizar asignación
   - DELETE /{id} - Desactivar terapia
   - POST /{id}/reactivar - Reactivar terapia

### Configuración

**main.py:**
- Todos los routers registrados
- Archivos estáticos configurados
- CORS configurado correctamente
- Creación automática de directorios de uploads

**Directorios de Uploads:**
- `uploads/tareas_recurso/evidencias/` - Evidencias de tareas

## 🎨 Frontend (Angular)

### Interfaces TypeScript

**Nuevas:**
- `recurso.interface.ts` - Recursos y catálogos
- `tarea-recurso.interface.ts` - Tareas y estadísticas
- `plan-pago.interface.ts` - Planes de pago
- `pago.interface.ts` - Pagos e historial

**Actualizadas:**
- `terapias-nino.interface.ts` - Nueva estructura
- `nino.interface.ts` - Compatible con BD real

### Services Angular

**Nuevos:**
- `recursos.service.ts`
- `tareas-recurso.service.ts`
- `planes-pago.service.ts`
- `pagos.service.ts`

**Actualizados:**
- `terapias-nino.service.ts` - Métodos nuevos + legacy
- `nino.service.ts` - CRUD completo

Todos los servicios incluyen:
- Métodos tipados con interfaces
- Parámetros opcionales de filtrado
- Manejo de HttpParams
- Soporte para paginación

## 🚀 Cómo Usar

### 1. Configurar Base de Datos

Asegurarse que existe la base de datos:
```sql
CREATE DATABASE IF NOT EXISTS autismo_mochis_ia 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;
```

### 2. Configurar Variables de Entorno

Crear `.env` en `backend/`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=autismo_mochis_ia
```

### 3. Instalar Dependencias

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ..
npm install
```

### 4. Iniciar Aplicación

```bash
# Backend (desde directorio backend/)
python run_server.py
# O con uvicorn directamente:
uvicorn app.main:app --reload

# Frontend (desde raíz)
ng serve
```

### 5. Verificar Conexión

Visitar:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Frontend: http://localhost:4200

## 📊 Endpoints Disponibles

### Documentación Interactiva

FastAPI genera automáticamente documentación interactiva:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Aquí puedes:
- Ver todos los endpoints disponibles
- Probar cada endpoint
- Ver esquemas de request/response
- Ejecutar requests directamente

## 🔐 Seguridad

### Consideraciones Implementadas

1. **Validación de Datos**: Todos los endpoints usan Pydantic para validación
2. **Transacciones BD**: Operaciones críticas usan transacciones
3. **Manejo de Archivos**: Validación de tipos y tamaños
4. **CORS**: Configurado para orígenes permitidos

### Pendientes (Recomendaciones)

1. **Autenticación**: Implementar middleware de autenticación JWT
2. **Autorización**: Validar permisos por rol
3. **Rate Limiting**: Limitar requests por IP
4. **Validación de Archivos**: Escaneo de virus en uploads
5. **Logs de Auditoría**: Registrar acciones críticas

## 🧪 Testing

### Backend

```bash
# Probar endpoint de salud
curl http://localhost:8000/health

# Listar recursos
curl http://localhost:8000/api/v1/recursos

# Obtener niños de un tutor
curl http://localhost:8000/api/v1/ninos/tutor/1
```

### Frontend

Los servicios ya están listos para usarse en componentes:

```typescript
// Ejemplo: Listar tareas de un niño
constructor(private tareasService: TareasRecursoService) {}

ngOnInit() {
  this.tareasService.listarPorNino(1, { completado: 0 })
    .subscribe(tareas => {
      console.log('Tareas pendientes:', tareas);
    });
}
```

## 📁 Estructura de Archivos

```
backend/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── recurso.py
│   │   ├── tarea_recurso.py
│   │   ├── plan_pago.py
│   │   └── ...
│   ├── schemas/         # Schemas Pydantic
│   │   ├── recurso.py
│   │   ├── tarea_recurso.py
│   │   └── ...
│   ├── api/v1/routers/  # Routers FastAPI
│   │   ├── recursos.py
│   │   ├── tareas_recurso.py
│   │   ├── planes_pago.py
│   │   ├── pagos.py
│   │   ├── ninos.py
│   │   └── terapias_nino.py
│   └── main.py          # Aplicación principal
└── uploads/             # Archivos subidos

src/app/
├── interfaces/          # Interfaces TypeScript
│   ├── recurso.interface.ts
│   ├── tarea-recurso.interface.ts
│   └── ...
└── service/            # Servicios Angular
    ├── recursos.service.ts
    ├── tareas-recurso.service.ts
    └── ...
```

## 🐛 Troubleshooting

### Error: "No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused" (Base de datos)
- Verificar que MySQL esté corriendo
- Verificar credenciales en `.env`
- Verificar que la BD existe

### Error: "CORS"
- Verificar configuración en `backend/app/core/config.py`
- Agregar origen del frontend a CORS_ORIGINS

### Error: "File not found" (Uploads)
- Los directorios se crean automáticamente al iniciar
- Verificar permisos de escritura

## 📝 Notas Adicionales

### Compatibilidad

- Los servicios mantienen métodos legacy para compatibilidad
- Interfaces legacy incluidas en TypeScript
- Migración gradual permitida

### Rendimiento

- Uso de `joinedload` para optimizar queries
- Paginación implementada en todos los listados
- Índices en campos clave de BD

### Mantenimiento

- Código documentado en español
- Nombres de variables consistentes
- Estructura modular y escalable

## 🎯 Próximos Pasos

1. **Testing Completo**: Probar todos los endpoints con datos reales
2. **Autenticación**: Implementar JWT y middleware de auth
3. **Componentes UI**: Actualizar componentes Angular para usar nuevos servicios
4. **Documentación**: Completar documentación de usuario
5. **Deploy**: Configurar para ambiente de producción

## 📞 Soporte

Para problemas o preguntas sobre la integración, consultar:
- Documentación de API: http://localhost:8000/docs
- Este README
- Código fuente comentado

---

**Versión**: 2.0.0
**Fecha**: Enero 2026
**Estado**: ✅ Integración Completa

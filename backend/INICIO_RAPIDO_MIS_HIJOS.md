# 🚀 INICIO RÁPIDO - Módulo Mis Hijos Backend

## ✅ Estado del Backend

El backend para el módulo "Mis Hijos" está **COMPLETAMENTE IMPLEMENTADO** y listo para usar.

## 📦 ¿Qué Incluye?

### ✅ Modelos de Base de Datos
- **Medicamento**: Información de medicamentos del niño
- **Alergia**: Información de alergias del niño
- **Relaciones**: Correctamente vinculadas con Nino y Tutor

### ✅ Endpoints API (5 endpoints)
1. `GET /api/v1/padres/mis-hijos` - Lista todos los hijos del padre
2. `GET /api/v1/padres/mis-hijos/{nino_id}` - Detalles de un hijo
3. `GET /api/v1/padres/mis-hijos/{nino_id}/medicamentos` - Medicamentos del hijo
4. `GET /api/v1/padres/mis-hijos/{nino_id}/alergias` - Alergias del hijo
5. `PUT /api/v1/padres/mis-hijos/{nino_id}/medicamentos/{med_id}/visto` - Marcar medicamento visto

### ✅ Servicios
- `obtener_mis_hijos()` - Obtiene todos los hijos del padre
- `obtener_hijo_por_id()` - Obtiene detalles de un hijo
- `obtener_medicamentos_por_hijo()` - Obtiene medicamentos
- `obtener_alergias_por_hijo()` - Obtiene alergias
- `marcar_medicamento_como_visto()` - Marca medicamento como visto

### ✅ Schemas Pydantic
- `HijoResponse` - Respuesta con información del hijo
- `MedicamentoResponse` - Respuesta con información del medicamento
- `AlergiaResponse` - Respuesta con información de alergia
- `MisHijosPageResponse` - Respuesta con lista de hijos
- `MisHijosApiResponse` - Respuesta estándar de API

### ✅ Seguridad
- Autenticación JWT requerida
- Validación de rol padre/tutor
- Los padres solo ven sus propios hijos
- Protección contra SQL injection

---

## 🚀 Pasos para Activar

### PASO 1: Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

**Dependencias principales:**
- FastAPI >= 0.110.0
- SQLAlchemy >= 2.0.25
- PyMySQL >= 1.1.0
- python-jose[cryptography] (para JWT)
- pydantic-settings

### PASO 2: Configurar Base de Datos

Crear archivo `backend/.env`:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=autismo_mochis_ia

# JWT
JWT_SECRET_KEY=tu_clave_secreta_aqui
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=240

# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True
```

### PASO 3: Ejecutar Migración de Base de Datos

```bash
cd backend
python migracion_mis_hijos.py
```

**¿Qué hace este script?**
- Crea tabla `medicamentos`
- Crea tabla `alergias`
- Verifica que las tablas se crearon correctamente
- Opcionalmente inserta datos de prueba

**Salida esperada:**
```
============================================================
🔧 MIGRACIÓN: MEDICAMENTOS Y ALERGIAS
============================================================
🔄 Creando tablas de medicamentos y alergias...
✅ Tablas creadas exitosamente!

Tablas creadas:
  - medicamentos
  - alergias

✅ Tabla 'medicamentos' verificada
✅ Tabla 'alergias' verificada

✅ Migración completada exitosamente!
============================================================
```

### PASO 4: Verificar Implementación

Ejecutar tests de verificación:

```bash
cd backend
python test_mis_hijos_api.py
```

**Salida esperada:**
```
============================================================
🚀 INICIANDO TESTS DE MIS HIJOS BACKEND
============================================================

============================================================
🧪 TEST 1: Verificando Imports
============================================================
✓ Importando modelos...
  ✅ Modelos importados correctamente
✓ Importando schemas...
  ✅ Schemas importados correctamente
✓ Importando servicios...
  ✅ Servicios importados correctamente
✓ Importando endpoints...
  ✅ Endpoints importados correctamente

✅ TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE

[... más tests ...]

============================================================
📊 RESUMEN DE RESULTADOS
============================================================
Imports             : ✅ PASÓ
Relaciones          : ✅ PASÓ
Rutas               : ✅ PASÓ
Schemas             : ✅ PASÓ

============================================================
✅ TODOS LOS TESTS PASARON EXITOSAMENTE
============================================================
```

### PASO 5: Iniciar Servidor Backend

```bash
cd backend
python run_server.py
```

**Salida esperada:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**El backend estará disponible en:**
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- Documentación alternativa: http://localhost:8000/redoc

---

## 🧪 Probar los Endpoints

### Opción 1: Usar Swagger UI (Recomendado)

1. Abrir navegador en: http://localhost:8000/docs
2. Expandir la sección "Padres - Mis Hijos"
3. Click en "Authorize" (botón con candado)
4. Ingresar tu JWT token
5. Probar los endpoints directamente desde la interfaz

### Opción 2: Usar cURL

```bash
# Configurar token (reemplazar con tu token real)
TOKEN="tu_jwt_token_aqui"

# Obtener lista de hijos
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Obtener detalles de un hijo
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Obtener medicamentos de un hijo
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos/1/medicamentos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Obtener alergias de un hijo
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos/1/alergias" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"

# Marcar medicamento como visto
curl -X PUT "http://localhost:8000/api/v1/padres/mis-hijos/1/medicamentos/1/visto" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

### Opción 3: Usar Postman

Importar la colección de endpoints desde la documentación Swagger.

---

## 📊 Estructura de Respuestas

### Respuesta Exitosa
```json
{
  "exito": true,
  "datos": {
    "hijos": [...]
  },
  "mensaje": "Se encontraron X hijo(s)"
}
```

### Respuesta de Error
```json
{
  "exito": false,
  "error": "Descripción del error"
}
```

---

## 🔍 Verificar Tablas en Base de Datos

```sql
-- Ver estructura de tabla medicamentos
DESCRIBE medicamentos;

-- Ver estructura de tabla alergias
DESCRIBE alergias;

-- Contar registros
SELECT COUNT(*) FROM medicamentos;
SELECT COUNT(*) FROM alergias;

-- Ver datos de ejemplo
SELECT * FROM medicamentos LIMIT 5;
SELECT * FROM alergias LIMIT 5;
```

---

## 📝 Crear Datos de Prueba (Opcional)

### Opción A: Durante la Migración

Cuando ejecutes `python migracion_mis_hijos.py`, responde "s" cuando pregunte:
```
¿Deseas agregar datos de prueba? (s/n): s
```

### Opción B: SQL Manual

```sql
-- Insertar medicamento de prueba (ajustar nino_id según tu BD)
INSERT INTO medicamentos (
    nino_id, nombre, dosis, frecuencia, razon, 
    fecha_inicio, activo, novedadReciente, actualizado_por
) VALUES (
    1, 'Metilfenidato', '10 mg', 'Dos veces al día', 'TDAH',
    CURDATE(), TRUE, TRUE, 'Coordinador Sistema'
);

-- Insertar alergia de prueba
INSERT INTO alergias (
    nino_id, nombre, severidad, reaccion, tratamiento
) VALUES (
    1, 'Penicilina', 'severa', 'Anafilaxia', 
    'Evitar completamente. Usar alternativas como cefalosporinas.'
);
```

---

## 🔧 Troubleshooting

### Error: "No module named 'sqlalchemy'"
**Solución:**
```bash
pip install sqlalchemy pymysql
```

### Error: "Access denied for user"
**Solución:**
- Verificar credenciales en `.env`
- Verificar que MySQL esté corriendo
- Verificar permisos del usuario de base de datos

### Error: "Table 'medicamentos' doesn't exist"
**Solución:**
```bash
cd backend
python migracion_mis_hijos.py
```

### Error: "Invalid token"
**Solución:**
- Verificar que el token JWT sea válido
- Verificar que no haya expirado
- Verificar JWT_SECRET_KEY en `.env`

### Error: "Tutor no encontrado"
**Solución:**
- Verificar que el usuario tenga un registro en tabla `tutores`
- Verificar que `tutores.usuario_id` corresponda al ID del usuario

---

## 📚 Documentación Adicional

- **API Completa:** Ver `API_MIS_HIJOS_DOCUMENTACION.md`
- **Tests:** Ver `test_mis_hijos_api.py`
- **Frontend:** Ver `src/app/padres/mis-hijos/README.md`

---

## ✅ Checklist de Activación

- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado
- [ ] Base de datos creada
- [ ] Migración ejecutada exitosamente
- [ ] Tests pasaron correctamente
- [ ] Servidor backend iniciado
- [ ] Endpoints responden correctamente
- [ ] Frontend configurado (opcional)

---

## 🎯 Resultado Esperado

Después de completar todos los pasos:

✅ Backend corriendo en http://localhost:8000  
✅ 5 endpoints funcionando correctamente  
✅ Autenticación JWT operativa  
✅ Tablas creadas en base de datos  
✅ Relaciones entre modelos correctas  
✅ Validación de permisos funcionando  
✅ Respuestas JSON correctamente formateadas  
✅ Listo para integrar con frontend

---

## 🎉 ¡Listo para Usar!

El backend del módulo "Mis Hijos" está completamente funcional y listo para conectar con el frontend Angular.

**Siguiente paso:** Iniciar el frontend y configurar el servicio para consumir estos endpoints.

---

**Versión:** 1.0  
**Fecha:** 2026-01-12  
**Estado:** ✅ Completamente Funcional

# API DE NIÑOS BENEFICIARIOS

Documentación completa de los endpoints para gestionar niños beneficiarios.

## 📚 Base URL

```
http://localhost:8000/api/v1/ninos
```

## 🔐 Autenticación Requerida

Todos los endpoints requieren autenticación JWT. Incluye el token en el header:

```
Authorization: Bearer <tu_token_jwt>
```

## 📋 Endpoints Disponibles

### 1. Listar Niños (Con paginación y búsqueda)

**GET** `/api/v1/ninos/`

**Query Parameters:**
- `page` (int, opcional): Número de página (default: 1)
- `page_size` (int, opcional): Elementos por página (default: 10, max: 100)
- `buscar` (string, opcional): Buscar por nombre, apellido o CURP
- `estado` (string, opcional): Filtrar por estado (ACTIVO, BAJA_TEMPORAL, INACTIVO)

**Ejemplo con curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/ninos/?page=1&page_size=10&buscar=Juan&estado=ACTIVO" \
  -H "Authorization: Bearer <token>"
```

**Ejemplo con PowerShell:**
```powershell
$token = "tu_token_aqui"
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ninos/?page=1&page_size=10" `
  -Method Get `
  -Headers @{ Authorization = "Bearer $token" }
```

**Respuesta:**
```json
{
  "total": 45,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "nombre": "Juan",
      "apellido_paterno": "Pérez",
      "apellido_materno": "García",
      "fecha_nacimiento": "2015-05-15",
      "sexo": "M",
      "edad": 9,
      "estado": "ACTIVO",
      "tutor_nombre": "María García López",
      "diagnostico_principal": "Trastorno del Espectro Autista"
    }
  ]
}
```

---

### 2. Obtener Niño por ID

**GET** `/api/v1/ninos/{nino_id}`

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/ninos/1" \
  -H "Authorization: Bearer <token>"
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido_paterno": "Pérez",
  "apellido_materno": "García",
  "fecha_nacimiento": "2015-05-15",
  "sexo": "M",
  "curp": "PEGJ150515HDFRRN03",
  "tutor_id": 1,
  "estado": "ACTIVO",
  "fecha_registro": "2024-01-15T10:30:00",
  "direccion": {
    "id": 1,
    "nino_id": 1,
    "calle": "Av. Principal",
    "numero": "123",
    "colonia": "Centro",
    "municipio": "Los Mochis",
    "codigo_postal": "81200"
  },
  "diagnostico": {
    "id": 1,
    "nino_id": 1,
    "diagnostico_principal": "Trastorno del Espectro Autista",
    "diagnostico_resumen": "TEA nivel 2",
    "archivo_url": "/files/diagnostico_123.pdf",
    "fecha_diagnostico": "2020-03-15",
    "especialista": "Dr. Roberto Sánchez",
    "institucion": "Hospital Infantil"
  },
  "info_emocional": {
    "id": 1,
    "nino_id": 1,
    "estimulos": "Música suave, juegos con agua",
    "calmantes": "Abrazos de presión, música",
    "preferencias": "Dinosaurios, carros",
    "no_tolera": "Ruidos fuertes, luces brillantes",
    "palabras_clave": "Tranquilo, espacio",
    "forma_comunicacion": "Verbal limitado, pictogramas",
    "nivel_comprension": "MEDIO"
  },
  "archivos": {
    "id": 1,
    "nino_id": 1,
    "acta_url": "/files/acta_123.pdf",
    "curp_url": "/files/curp_123.pdf",
    "comprobante_url": "/files/comprobante_123.pdf",
    "foto_url": "/files/foto_123.jpg",
    "diagnostico_url": "/files/diagnostico_123.pdf",
    "consentimiento_url": "/files/consentimiento_123.pdf",
    "hoja_ingreso_url": "/files/hoja_ingreso_123.pdf"
  },
  "tutor_nombre": "María García López"
}
```

---

### 3. Crear Niño

**POST** `/api/v1/ninos/`

**Body (JSON):**
```json
{
  "nombre": "Carlos",
  "apellido_paterno": "Ramírez",
  "apellido_materno": "López",
  "fecha_nacimiento": "2016-08-20",
  "sexo": "M",
  "curp": "RALC160820HDFMPR05",
  "tutor_id": 2,
  "estado": "ACTIVO",
  "direccion": {
    "calle": "Calle Hidalgo",
    "numero": "456",
    "colonia": "Las Flores",
    "municipio": "Los Mochis",
    "codigo_postal": "81210"
  },
  "diagnostico": {
    "diagnostico_principal": "Trastorno del Espectro Autista",
    "diagnostico_resumen": "TEA nivel 1",
    "fecha_diagnostico": "2021-05-10",
    "especialista": "Dra. Ana Martínez",
    "institucion": "Centro de Desarrollo Infantil"
  },
  "info_emocional": {
    "estimulos": "Música, movimiento",
    "calmantes": "Peluche favorito",
    "preferencias": "Dibujar, colorear",
    "no_tolera": "Cambios repentinos",
    "palabras_clave": "Calma, rutina",
    "forma_comunicacion": "Verbal",
    "nivel_comprension": "ALTO"
  }
}
```

**Ejemplo con PowerShell:**
```powershell
$token = "tu_token_aqui"
$body = @{
  nombre = "Carlos"
  apellido_paterno = "Ramírez"
  apellido_materno = "López"
  fecha_nacimiento = "2016-08-20"
  sexo = "M"
  curp = "RALC160820HDFMPR05"
  tutor_id = 2
  estado = "ACTIVO"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ninos/" `
  -Method Post `
  -Body $body `
  -ContentType "application/json" `
  -Headers @{ Authorization = "Bearer $token" }
```

---

### 4. Actualizar Niño

**PUT** `/api/v1/ninos/{nino_id}`

**Body (JSON) - Todos los campos son opcionales:**
```json
{
  "nombre": "Carlos Alberto",
  "estado": "ACTIVO",
  "direccion": {
    "calle": "Nueva Calle",
    "numero": "789"
  },
  "diagnostico": {
    "diagnostico_resumen": "TEA nivel 1 con avances significativos"
  }
}
```

**Ejemplo:**
```bash
curl -X PUT "http://localhost:8000/api/v1/ninos/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Carlos Alberto",
    "estado": "ACTIVO"
  }'
```

---

### 5. Eliminar Niño

**DELETE** `/api/v1/ninos/{nino_id}`

**Ejemplo:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/ninos/1" \
  -H "Authorization: Bearer <token>"
```

**Respuesta:**
```
204 No Content
```

---

### 6. Cambiar Estado del Niño

**PATCH** `/api/v1/ninos/{nino_id}/estado?estado=BAJA_TEMPORAL`

**Query Parameters:**
- `estado` (required): ACTIVO | BAJA_TEMPORAL | INACTIVO

**Ejemplo:**
```bash
curl -X PATCH "http://localhost:8000/api/v1/ninos/1/estado?estado=BAJA_TEMPORAL" \
  -H "Authorization: Bearer <token>"
```

**Respuesta:**
```json
{
  "message": "Estado del niño actualizado a BAJA_TEMPORAL",
  "nino_id": 1,
  "estado": "BAJA_TEMPORAL"
}
```

---

### 7. Estadísticas de Niños

**GET** `/api/v1/ninos/estadisticas/resumen`

**Ejemplo:**
```bash
curl -X GET "http://localhost:8000/api/v1/ninos/estadisticas/resumen" \
  -H "Authorization: Bearer <token>"
```

**Respuesta:**
```json
{
  "total": 45,
  "por_estado": {
    "activos": 40,
    "baja_temporal": 3,
    "inactivos": 2
  },
  "por_sexo": {
    "masculino": 30,
    "femenino": 14,
    "otro": 1
  }
}
```

---

## 🔒 Permisos Requeridos

- **Listar**: `ver_ninos` (Admin, Coordinador, Terapeuta, Padre)
- **Ver detalle**: `ver_ninos` (Admin, Coordinador, Terapeuta, Padre)
- **Crear**: `crear_ninos` (Admin, Coordinador)
- **Actualizar**: `editar_ninos` (Admin, Coordinador)
- **Eliminar**: `eliminar_ninos` (Solo Admin)
- **Cambiar estado**: `editar_ninos` (Admin, Coordinador)
- **Estadísticas**: `ver_reportes` (Admin, Coordinador)

---

## 📝 Notas Importantes

1. **Validaciones**:
   - El CURP debe ser único
   - El sexo debe ser: M (Masculino), F (Femenino), O (Otro)
   - El estado debe ser: ACTIVO, BAJA_TEMPORAL, INACTIVO
   - La fecha de nacimiento no puede ser futura

2. **Relaciones**:
   - Al crear un niño con `tutor_id`, el tutor debe existir
   - Los datos relacionados (dirección, diagnóstico, etc.) son opcionales
   - Al eliminar un niño, se eliminan automáticamente todos sus datos relacionados

3. **Búsqueda**:
   - La búsqueda no distingue mayúsculas/minúsculas
   - Busca en: nombre, apellido paterno, apellido materno y CURP

4. **Paginación**:
   - Por defecto muestra 10 elementos por página
   - Máximo 100 elementos por página
   - Los resultados se ordenan por fecha de registro (más recientes primero)

---

## 🧪 Probar en Swagger UI

1. Ve a: http://localhost:8000/docs
2. Autorízate con tu token JWT
3. Navega a la sección "Niños Beneficiarios"
4. Prueba cada endpoint con datos de ejemplo

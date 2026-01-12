# 🚀 BACKEND FASTAPI - PERFIL CON SUBIDA DE ARCHIVOS

## 📋 RESUMEN DE CAMBIOS

Se ha completado el backend FastAPI para soportar la subida y descarga protegida de archivos del perfil de usuario.

### ✅ Cambios Realizados

1. **Modelo actualizado** (`personal_perfil.py`)

   - Campos para almacenar rutas relativas
   - `foto_perfil`, `cv_archivo`, `documentos_extra` (JSON)

2. **Schema actualizado** (`perfil.py`)

   - Campo `documentos_extra: List[str]`
   - Parseo de JSON en `from_db()`

3. **Endpoint completo** (`endpoints/perfil.py`)
   - GET /api/v1/perfil/me → Obtener perfil
   - PUT /api/v1/perfil/me → Actualizar perfil + archivos
   - GET /api/v1/perfil/archivos/{tipo}/{filename} → Descargar archivos protegidos

---

## 🏗️ ESTRUCTURA DE DIRECTORIOS

```
proyecto/
├── uploads/                    # Raíz de uploads (NUEVO)
│   ├── fotos/                  # Fotos de perfil
│   │   ├── personal_1_1700000000_foto.png
│   │   ├── personal_2_1700000100_mi_foto.jpg
│   │   └── ...
│   ├── cv/                     # Currículums
│   │   ├── personal_1_1700000000_cv.pdf
│   │   ├── personal_2_1700000050_curriculum.pdf
│   │   └── ...
│   └── documentos/             # Documentos extra
│       ├── personal_1_1700000000_constancia.pdf
│       ├── personal_1_1700000001_certificado.png
│       └── ...
└── backend/
    └── app/
        ├── models/
        │   └── personal_perfil.py    # ACTUALIZADO
        ├── schemas/
        │   └── perfil.py             # ACTUALIZADO
        └── api/v1/endpoints/
            └── perfil.py             # COMPLETAMENTE REESCRITO
```

---

## 📝 CAMBIOS EN MODELOS

### `personal_perfil.py`

```python
# ANTES
cv_url = Column(String(255), nullable=True)
foto_url = Column(String(255), nullable=True)

# DESPUÉS
foto_perfil = Column(String(255), nullable=True)     # fotos/personal_1_...
cv_archivo = Column(String(255), nullable=True)      # cv/personal_1_...
documentos_extra = Column(Text, nullable=True)       # JSON: ["documentos/...", ...]
```

---

## 📊 CAMBIOS EN SCHEMAS

### `perfil.py`

```python
# ANTES
foto_perfil: Optional[str] = None
cv_archivo: Optional[str] = None
# (sin documentos_extra)

# DESPUÉS
foto_perfil: Optional[str] = None              # Ruta relativa
cv_archivo: Optional[str] = None               # Ruta relativa
documentos_extra: List[str] = []               # Lista de rutas

# En from_db()
docs_extra = []
if perfil.documentos_extra:
    try:
        docs_extra = json.loads(perfil.documentos_extra)
    except (json.JSONDecodeError, TypeError):
        docs_extra = []
```

---

## 🔧 ENDPOINTS

### 1️⃣ GET /api/v1/perfil/me

**Obtiene el perfil completo del usuario autenticado**

```bash
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/v1/perfil/me
```

**Respuesta (200):**

```json
{
  "id_personal": 1,
  "nombres": "Juan",
  "apellido_paterno": "Pérez",
  "foto_perfil": "fotos/personal_1_1700000000_foto.png",
  "cv_archivo": "cv/personal_1_1700000050_cv.pdf",
  "documentos_extra": [
    "documentos/personal_1_1700000100_constancia.pdf",
    "documentos/personal_1_1700000110_certificado.png"
  ],
  "telefono_personal": "555-1234",
  "correo_personal": "juan@example.com",
  ...
}
```

---

### 2️⃣ PUT /api/v1/perfil/me

**Actualiza perfil y sube archivos**

```bash
curl -X PUT \
  -H "Authorization: Bearer {token}" \
  -F "telefono_personal=555-9999" \
  -F "correo_personal=nuevo@email.com" \
  -F "foto_perfil=@mi_foto.jpg" \
  -F "cv_archivo=@curriculum.pdf" \
  -F "documentos_extra_0=@constancia.pdf" \
  -F "documentos_extra_1=@certificado.png" \
  http://localhost:8000/api/v1/perfil/me
```

**Campos aceptados:**

| Parámetro                | Tipo   | Descripción                         |
| ------------------------ | ------ | ----------------------------------- |
| `telefono_personal`      | string | Teléfono personal                   |
| `correo_personal`        | string | Correo personal                     |
| `grado_academico`        | string | Grado académico                     |
| `especialidades`         | string | Especialidades (separadas por coma) |
| `experiencia`            | string | Descripción de experiencia          |
| `domicilio_calle`        | string | Calle y número                      |
| `domicilio_colonia`      | string | Colonia                             |
| `domicilio_cp`           | string | Código postal                       |
| `domicilio_municipio`    | string | Municipio                           |
| `domicilio_estado`       | string | Estado                              |
| `foto_perfil`            | File   | Imagen (JPG, PNG, etc.)             |
| `cv_archivo`             | File   | PDF del currículum                  |
| `documentos_extra_0 a 4` | File   | PDFs o imágenes adicionales         |

**Respuesta (200):**

```json
{
  "id_personal": 1,
  "nombres": "Juan",
  "foto_perfil": "fotos/personal_1_1700000000_foto.png",
  "cv_archivo": "cv/personal_1_1700000050_cv.pdf",
  "documentos_extra": [...],
  ...
}
```

**Errores:**

- `400`: Tipo de archivo inválido
- `404`: No existe registro de personal
- `401`: Token JWT inválido o expirado

---

### 3️⃣ GET /api/v1/perfil/archivos/{tipo}/{filename}

**Descarga archivos protegidos (requiere JWT)**

```bash
curl -H "Authorization: Bearer {token}" \
  -o mi_foto.png \
  http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.png
```

**Tipos válidos:**

- `fotos` → Archivos en `uploads/fotos/`
- `cv` → Archivos en `uploads/cv/`
- `documentos` → Archivos en `uploads/documentos/`

**Errores:**

- `400`: Tipo de archivo inválido
- `403`: Acceso denegado (path traversal)
- `404`: Archivo no encontrado
- `401`: Token JWT inválido

---

## 🔐 SEGURIDAD

### ✅ Implementado

1. **JWT Obligatorio** - Todos los endpoints requieren `Depends(get_current_user)`
2. **Validación de tipos** - Solo se aceptan:
   - Fotos: `image/*` (JPG, PNG, GIF, etc.)
   - CV: `application/pdf`
   - Documentos: `application/pdf` + `image/*`
3. **Path Traversal Prevention** - `.resolve()` y verificación de ruta
4. **Nombres únicos** - `personal_<id>_<timestamp>_<filename>`

### 📂 Directorio de uploads

El directorio `uploads/` debe estar:

- **Fuera del repo** (agregar a `.gitignore`)
- **Con permisos de escritura**
- **Separado de static/** (NO usar /static)

---

## 🔄 FLUJO COMPLETO

### 1. Angular envía FormData

```typescript
const formData = new FormData();
formData.append('telefono_personal', '555-1234');
formData.append('foto_perfil', fotoFile);
formData.append('cv_archivo', cvFile);
formData.append('documentos_extra_0', doc1);
formData.append('documentos_extra_1', doc2);

this.httpClient.put('/api/v1/perfil/me', formData).subscribe(...);
```

### 2. Backend recibe y valida

```python
@router.put("/me")
def actualizar_perfil(
    foto_perfil: Optional[UploadFile] = File(None),
    cv_archivo: Optional[UploadFile] = File(None),
    documentos_extra_0: Optional[UploadFile] = File(None),
    ...
):
    # 1. Validar tipos
    # 2. Generar nombres únicos
    # 3. Guardar en uploads/
    # 4. Almacenar rutas en DB
    # 5. Retornar respuesta
```

### 3. Backend guarda archivos

```
Archivo original: "mi foto.jpg"
↓
Nombre único: "personal_1_1700000000_mi_foto.jpg"
↓
Ruta completa: "uploads/fotos/personal_1_1700000000_mi_foto.jpg"
↓
Ruta relativa guardada en DB: "fotos/personal_1_1700000000_mi_foto.jpg"
```

### 4. Angular descarga archivos protegidos

```typescript
// Desde ArchivosService
descargarComoBlob(rutaRelativa: string) {
  // rutaRelativa = "fotos/personal_1_1700000000_foto.png"
  // URL = "/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.png"

  return this.httpClient.get(url, { responseType: 'blob' });
}

// Con token JWT (vía interceptor)
```

---

## 📦 HELPER FUNCTIONS

### `generar_nombre_unico(personal_id: int, filename: str) -> str`

```python
# Entrada
personal_id = 1
filename = "mi foto.jpg"

# Salida
"personal_1_1700000000_mi_foto.jpg"
```

### `guardar_archivo(file, directorio, personal_id) -> str`

```python
# 1. Genera nombre único
# 2. Crea ruta completa (uploads/fotos/...)
# 3. Guarda archivo en disco
# 4. Retorna ruta relativa (fotos/...)
# 5. Maneja errores con HTTPException
```

---

## 🧪 PRUEBAS

### Test 1: Subir Foto

```bash
curl -X PUT \
  -H "Authorization: Bearer eyJ..." \
  -F "foto_perfil=@foto.jpg" \
  http://localhost:8000/api/v1/perfil/me

# ✅ 200 OK
# {
#   "foto_perfil": "fotos/personal_1_1700000000_foto.jpg",
#   ...
# }
```

### Test 2: Descargar Foto (Protegida)

```bash
curl -H "Authorization: Bearer eyJ..." \
  -o mi_foto.jpg \
  http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.jpg

# ✅ 200 OK (archivo descargado)
```

### Test 3: Sin Token

```bash
curl http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.jpg

# ❌ 401 Unauthorized
```

### Test 4: Path Traversal Attack

```bash
curl -H "Authorization: Bearer eyJ..." \
  http://localhost:8000/api/v1/perfil/archivos/fotos/../../../../etc/passwd

# ❌ 403 Forbidden (ruta bloqueada)
```

---

## 📋 CHECKLIST

### Modelo

- [x] Campos: `foto_perfil`, `cv_archivo`, `documentos_extra` (JSON)
- [x] Rutas relativas (sin path absoluto)
- [x] Nullable para campos opcionales

### Schema

- [x] `documentos_extra: List[str]`
- [x] Parseo de JSON en `from_db()`
- [x] Validación de tipos

### Endpoints

- [x] GET /api/v1/perfil/me
- [x] PUT /api/v1/perfil/me (con uploads)
- [x] GET /api/v1/perfil/archivos/{tipo}/{filename}

### Seguridad

- [x] JWT en todos los endpoints
- [x] Validación de tipos (image, pdf)
- [x] Path traversal prevention
- [x] Sin referencias a /static
- [x] Nombres únicos con timestamp

### Errores

- [x] 400: Tipo inválido, error al guardar
- [x] 401: Token inválido (automático)
- [x] 403: Path traversal
- [x] 404: Archivo/personal no encontrado

### Base de datos

- [x] Transacciones correctas
- [x] Flush/commit adecuados
- [x] Relaciones intactas

---

## 🚀 CONFIGURACIÓN

### 1. Crear directorio

```bash
# En la raíz del proyecto backend
mkdir -p uploads/{fotos,cv,documentos}
chmod 755 uploads/*
```

### 2. Agregar .gitignore

```bash
# Ignorar archivos subidos
uploads/
!uploads/.gitkeep
```

### 3. Verif icar settings.py

```python
# Debe existir BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Los códigos usan:
UPLOADS_DIR = Path(settings.BASE_DIR) / "uploads"
```

### 4. Instalar dependencias (si no están)

```bash
pip install fastapi python-multipart sqlalchemy pathlib
```

---

## 📚 INTEGRACIÓN CON FRONTEND

### Angular ArchivosService

```typescript
descargarComoBlob(rutaRelativa: string): Observable<Blob> {
  // rutaRelativa = "fotos/personal_1_1700000000_foto.png"

  const [tipo, filename] = rutaRelativa.split('/');
  const url = `${environment.apiBaseUrl}/perfil/archivos/${tipo}/${filename}`;

  return this.httpClient.get(url, { responseType: 'blob' });
  // Token JWT agregado por interceptor automáticamente
}
```

### Normalización de rutas

El frontend YA tiene código para normalizar rutas antiguas:

```typescript
private normalizarRuta(ruta: string): string {
  // static/fotos/... → /api/v1/perfil/archivos/fotos/...
  if (ruta.startsWith('static/')) {
    const resto = ruta.replace('static/', '');
    const [tipo, ...resto_path] = resto.split('/');
    return `/api/v1/perfil/archivos/${tipo}/${resto_path.join('/')}`;
  }
  return ruta;
}
```

---

## ⚡ PERFORMANCE

### Consideraciones

1. **Almacenamiento**: Los archivos están en disco (uploads/)
2. **Descarga**: FileResponse es eficiente (streaming)
3. **Nombre único con timestamp**: Previene colisiones

### Optimizaciones futuras

- [ ] Validar tamaño máximo (5MB foto, 10MB CV, 10MB docs)
- [ ] Comprimir imágenes automáticamente
- [ ] Implementar CDN para archivos
- [ ] Caché de headers HTTP

---

## 🐛 TROUBLESHOOTING

### Error: "Permission denied" al guardar

```
Solución: chmod 755 uploads/
```

### Error: "uploads directory not found"

```
Solución: mkdir -p uploads/{fotos,cv,documentos}
```

### Error: "No module named pathlib"

```
Solución: pip install pathlib
# O usar: from pathlib import Path (está en stdlib)
```

### Error en Swagger: "Expected UploadFile"

```
Solución: Asegurar que File está importado:
from fastapi import File, UploadFile
```

---

## 📊 RESPUESTAS ESPERADAS

### Upload exitoso

```json
{
  "id_personal": 1,
  "nombres": "Juan",
  "foto_perfil": "fotos/personal_1_1700000000_foto.png",
  "cv_archivo": "cv/personal_1_1700000050_cv.pdf",
  "documentos_extra": [
    "documentos/personal_1_1700000100_constancia.pdf"
  ],
  "telefono_personal": "555-1234",
  ...
}
```

### Error: Tipo inválido

```json
{
  "detail": "La foto debe ser una imagen."
}
```

### Error: Archivo muy grande (futuro)

```json
{
  "detail": "La foto no debe superar 5MB"
}
```

---

## ✅ VALIDACIÓN FINAL

Antes de desplegar:

1. ✅ Directorios creados: `uploads/{fotos,cv,documentos}`
2. ✅ Permisos: `chmod 755 uploads/`
3. ✅ `.gitignore`: `uploads/` agregado
4. ✅ Tests: Probar los 3 endpoints
5. ✅ Swagger: `/docs` funciona correctamente
6. ✅ Frontend: ArchivosService usa rutas correctas
7. ✅ Token JWT: Funciona en endpoints protegidos

---

**Fecha:** 2026-01-12  
**Versión:** 1.0.0  
**Status:** ✅ COMPLETADO Y TESTEADO

# RESUMEN INTEGRACIÓN PERFIL - BACKEND Y FRONTEND ✅

## 📋 Cambios Realizados

### 🔧 BACKEND - Python/FastAPI

#### 1. **backend/app/api/v1/endpoints/perfil.py**

- ✅ Agregados imports faltantes: `time`, `json`, `Path`
- ✅ Configuración centralizada de directorios (`FOTOS_DIR`, `CV_DIR`, `DOCUMENTOS_DIR`)
- ✅ Función `guardar_archivo()` mejorada con manejo robusto de errores
- ✅ Función `generar_nombre_unico()` para evitar conflictos de archivos
- ✅ Endpoint `GET /me` - Retorna perfil con archivos (foto, CV, documentos)
- ✅ Endpoint `PUT /me` - Acepta FormData con campos editables + archivos
- ✅ Endpoint `GET /archivos/{tipo}/{filename}` - Descargas protegidas por JWT
  - Validación de seguridad (path traversal prevention)
  - Tipos válidos: fotos, cv, documentos
  - Ejemplo: `/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.png`

#### 2. **backend/app/models/personal_perfil.py**

- ✅ Agregado campo `grado_academico` (String editable)
- ✅ Se mantiene relación con `grado_academico_id` (FK)
- ✅ Campos de archivos: `foto_perfil`, `cv_archivo`, `documentos_extra` (JSON)

#### 3. **backend/app/schemas/perfil.py**

- ✅ Schema `PerfilResponse` actualizado con:
  - `foto_perfil`: URL relativa (fotos/...)
  - `cv_archivo`: URL relativa (cv/...)
  - `documentos_extra`: Lista de URLs relativas
- ✅ Método `from_db()` convierte datos de modelos a response

---

### 🎨 FRONTEND - Angular/TypeScript

#### 1. **src/app/interfaces/perfil-usuario.interface.ts**

- ✅ Agregado campo `documentos_extra?: string[] | null`
- ✅ Comentarios con descripción de cada campo
- ✅ Tipos bien definidos para interfaz de datos

#### 2. **src/app/service/perfil.service.ts**

- ✅ Método `getMiPerfil()` - GET a `/api/v1/perfil/me`
- ✅ Método `actualizarMiPerfil(FormData)` - PUT a `/api/v1/perfil/me`
- ✅ Función auxiliar `construirUrlsArchivos()` que:
  - Convierte rutas relativas a URLs completas de API
  - Ejemplo: `"fotos/personal_1_..."` → `"/api/v1/perfil/archivos/fotos/personal_1_..."`
  - Maneja campos: `foto_perfil`, `cv_archivo`, `documentos_extra`

#### 3. **src/app/shared/perfil/perfil.ts** (Component)

- ✅ Signals para estado reactivo:
  - `perfil` - datos del usuario
  - `cargando`, `guardando` - estados de operación
  - `dirtyState` - cambios pendientes
  - `mostrarToast`, `toastTipo`, `toastMensaje`
  - `mostrarModalConfirmar` - confirmación antes de guardar
  - `mostrarModalPassword` - cambio de contraseña
- ✅ Manejo de archivos:

  - `onFotoChange()` - Carga imagen de perfil (preview local)
  - `onCvChange()` - Carga PDF del CV
  - `cargarDocumentosExtra()` - Carga documentos adicionales desde API
  - Gestión de Object URLs para memoria

- ✅ Funciones principales:
  - `cargarPerfil()` - GET datos del backend
  - `guardarPerfil()` - PUT con FormData (archivos + campos)
  - `intentarGuardar()` - Abre modal de confirmación
  - `confirmarGuardado()` - Guarda después de confirmación
- ✅ Modales confirmación:
  - Abiertos por signals `mostrarModalConfirmar()`, `mostrarModalPassword()`
  - Acciones: Cancelar o Confirmar
  - Toast de éxito/error al finalizar

#### 4. **src/app/shared/perfil/perfil.html** (Template)

- ✅ Modal de Confirmación de Guardado:

  ```html
  @if (mostrarModalConfirmar()) {
  <div class="modal-overlay" (click)="cancelarGuardado()">
    <!-- Contenido modal -->
  </div>
  }
  ```

- ✅ Modal de Cambio de Contraseña:

  ```html
  @if (mostrarModalPassword()) {
  <div class="modal-overlay" (click)="cerrarModalPassword()">
    <div class="modal-content password-modal">
      <!-- 3 inputs: actual, nueva, confirmar -->
    </div>
  </div>
  }
  ```

- ✅ Secciones dinámicas:
  - Alertas en tiempo real (`@if (alertas().length > 0)`)
  - Loader mientras carga (`@if (cargando())`)
  - Documentos extra (`@if (docsPreviews().length > 0)`)
  - Botón Guardar deshabilitado si no hay cambios (`[disabled]="!dirtyState()"`)

#### 5. **src/app/shared/perfil/perfil.scss** (Estilos)

- ✅ Estilos para modales:
  - `.modal-overlay` - Fondo oscuro con blur
  - `.modal-content` - Caja modal centrada
  - `.password-modal` - Estilos específicos para form de contraseña
  - `.modal-actions` - Botones de confirmación
- ✅ Animaciones:
  - `fadeIn` - Modal aparece gradualmente
  - `slideUp` - Modal sube desde abajo
- ✅ Responsive:
  - Grid 2 columnas en desktop → 1 en mobile
  - Modales ajustados en pantallas pequeñas

---

## 🔗 FLUJO DE DATOS

### Cargar Perfil (GET)

```
Frontend GET → /api/v1/perfil/me
    ↓
Backend query(Personal, PersonalPerfil)
    ↓
PerfilResponse.from_db() convierte datos
    ↓
Frontend recibe datos + rutas relativas
    ↓
construirUrlsArchivos() → rutas completas de API
    ↓
descargarComoBlob() descarga via /api/v1/perfil/archivos/{tipo}/{filename}
```

### Guardar Perfil (PUT)

```
Usuario hace cambios → dirtyState = true
    ↓
Click "Guardar cambios"
    ↓
Abre modal de confirmación
    ↓
Usuario confirma
    ↓
guardarPerfil() crea FormData con:
  - Campos de texto (telefono, email, grado, etc)
  - Files: fotoFile, cvFile, documentosExtras
    ↓
Frontend PUT → /api/v1/perfil/me (FormData)
    ↓
Backend valida y guarda archivos
    ↓
Backend retorna PerfilResponse actualizado
    ↓
Frontend actualiza signals + muestra toast
```

---

## 📁 ESTRUCTURA DE ARCHIVOS GUARDADOS

```
uploads/
├── fotos/
│   └── personal_1_1704067200_foto.png
├── cv/
│   └── personal_1_1704067200_curriculum.pdf
└── documentos/
    ├── personal_1_1704067200_certificado.pdf
    └── personal_1_1704067200_diploma.jpg
```

**Formato de nombre**: `personal_{id}_{timestamp}_{nombre_original}`

- Garantiza unicidad
- Evita colisiones
- Fácil de rastrear

---

## 🔐 SEGURIDAD

### Protección de Archivos

- ✅ Acceso solo con JWT válido (`@Depends(get_current_user)`)
- ✅ Validación de path (previene directory traversal)
- ✅ Whitelist de directorios permitidos
- ✅ Descarga como blob (no expone ruta real)

### Validación Frontend

- ✅ Aceptar solo: imágenes (foto), PDF (CV), PDF/imágenes (docs)
- ✅ Validar tipos MIME antes de enviar
- ✅ Modal de confirmación antes de guardar

---

## ✨ CARACTERÍSTICAS IMPLEMENTADAS

### ✅ Funcionales

1. **Carga de archivos** - Foto, CV, Documentos adicionales
2. **Edición de datos** - Campos de texto con validación
3. **Previsualización** - PDF embed + imágenes
4. **Descargas protegidas** - Solo usuarios autenticados
5. **Modalizado** - Confirmación y cambio de contraseña
6. **Alertas dinámicas** - Avisa si faltan foto o CV
7. **Toast notificaciones** - Éxito/error al guardar

### ✅ No estático

1. Datos se cargan desde API (no hardcodeado)
2. URLs dinámicas construidas en tiempo de ejecución
3. Previsualización local antes de enviar
4. Estados reactivos (Signals de Angular)
5. Validación dinámica de campos

---

## 🧪 CÓMO PROBAR

### 1. Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
ng serve --open
```

### 3. Pruebas Manuales

1. Navega a `/perfil`
2. Upload foto (JPG/PNG)
3. Upload CV (PDF)
4. Upload documentos extra (PDF/IMG)
5. Edita campos (teléfono, email, grado académico, especialidades, experiencia)
6. Click "Guardar cambios"
7. Confirma en modal
8. Verifica toast de éxito
9. Recarga página → verifica datos persistidos

---

## 📝 NOTAS

- Los archivos se guardan en `uploads/` (configurable en `settings.BASE_DIR`)
- Las rutas se almacenan en BD como strings relativos (facilita migración)
- Las URLs se construyen dinámicamente al cargar datos
- Los Object URLs se revoken al destruir el componente (gestión de memoria)
- Soporta múltiples archivos en "documentos extra"

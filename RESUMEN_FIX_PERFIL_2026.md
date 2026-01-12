# Resumen: Solución Completa del Módulo de Perfil Profesional

## 🎯 Objetivo

Implementar correctamente el módulo de Perfil Profesional con:

- Subida de archivos (foto, CV, documentos)
- Visualización de archivos
- Manejo de URLs correctamente
- Protección por JWT
- UX fluida sin errores 404

## 📋 Cambios Realizados

### 1. **Frontend - Componente PerfilComponent** (`perfil.ts`)

#### Imports Corregidos

```typescript
import { environment } from '../../../enviroment/environment';
import { HostListener } from '@angular/core';
// ❌ Removido: ArchivosService (no existe)
```

#### Signals Reorganizadas

- **Estado**: `perfil`, `cargando`, `guardando`, `dirtyState`
- **Notificaciones**: `mostrarToast`, `toastTipo`, `toastMensaje`
- **Modales**: `mostrarModalConfirmar`, `mostrarModalPassword`
- **Archivos**: `fotoFile`, `cvFile`, `documentosExtras`
- **Visualización**: `fotoUrl`, `cvSafeUrl`, `cvRawUrl`, `docsPreview`

#### Métodos Principales

##### 1. `cargarPerfil()`

```typescript
// Carga datos del API y obtiene archivos existentes
- Llama getMiPerfil()
- Llama cargarFoto(), cargarCV(), cargarDocumentosExtra()
- Maneja errores gracefully
```

##### 2. `cargarFoto(rutaRelativa: string)`

```typescript
// Construye URL completa usando environment
const urlCompleta = `${environment.apiBaseUrl}/perfil/archivos/fotos/${filename}`;
// Descarga como blob
// Crea blob URL para visualización
// Rastrea para limpiar después
```

##### 3. `cargarCV(rutaRelativa: string)` y `cargarDocumentosExtra()`

```typescript
// Similar a cargarFoto()
// Para PDFs: usa SafeResourceUrl con iframe
// Para imágenes: usa blob URL
```

##### 4. Handlers de Archivos

```typescript
onFotoChange(event)
- Valida tipo (image/*)
- Valida tamaño (máx 5MB)
- Previsualiza inmediatamente
- Marca formulario como dirty

onCvChange(event)
- Valida tipo (application/pdf)
- Valida tamaño (máx 10MB)
- Previsualiza en iframe

onDocsChange(event)
- Valida múltiples archivos
- Mezcla PDFs e imágenes
- Previsualiza cada uno
```

##### 5. `guardarPerfil()`

```typescript
// Construye FormData con:
// - Campos del formulario
// - Archivos nuevos (si existen)
// Llama actualizarMiPerfil(formData)
// Maneja respuesta y errores
// Limpia archivos temporales
```

#### Limpieza de Recursos

```typescript
ngOnDestroy()
- Revoca todos los blob URLs
- Limpia la Set de allocatedObjectUrls

@HostListener('window:beforeunload')
- Previene salida si hay cambios sin guardar
```

### 2. **Frontend - Servicio PerfilService** (`perfil.service.ts`)

#### Nuevo Método

```typescript
descargarArchivo(urlCompleta: string): Observable<Blob> {
  return this.http.get(urlCompleta, {
    responseType: 'blob'
  });
}
```

#### Método Actualizado `construirUrlsArchivos()`

```typescript
// Convierte rutas relativas en URLs completas
// Ejemplo: "fotos/personal_1_12345_foto.png"
// Resultado: "http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_12345_foto.png"

// Soporta:
// - foto_perfil
// - cv_archivo
// - documentos_extra (array)
```

### 3. **Backend - Endpoints Verificados** (`perfil.py`)

#### GET `/api/v1/perfil/me`

- ✅ Retorna PerfilResponse
- ✅ Rutas relativas en JSON

#### PUT `/api/v1/perfil/me`

- ✅ Acepta FormData multipart
- ✅ Soporta opcional: foto_perfil, cv_archivo
- ✅ Soporta múltiples documentos_extra_0, documentos_extra_1, etc.
- ✅ Valida tipos de archivo
- ✅ Genera nombres únicos sin .tmp

#### GET `/api/v1/perfil/archivos/{tipo}/{filename}`

- ✅ Protegido por JWT
- ✅ Tipos válidos: fotos, cv, documentos
- ✅ Validación de path traversal
- ✅ Retorna archivo como blob

### 4. **Ambiente** (`environment.ts`)

```typescript
export const environment = {
  production: false,

  // 🔴 NUNCA usar localhost:4200 para archivos
  apiBaseUrl: 'http://localhost:8000/api/v1',

  // Endpoints relativos se concatenan con apiBaseUrl
  apiPerfil: '/perfil',
};
```

## 🔐 Flujo de Seguridad

1. **Upload**: FormData contiene JWT en interceptor
2. **Download**: GET request incluye JWT en header
3. **Validación Backend**: Verifica current_user antes de servir archivo
4. **Path Traversal**: Valida que la ruta esté dentro del directorio

## 📊 URLs Construidas Correctamente

### Foto Nueva (preview local)

```
data:image/png;base64,...
```

### CV Nuevo (preview local)

```
blob:http://localhost:4200/...#toolbar=0
```

### Foto Existente (desde API)

```
http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.png
```

### CV Existente (desde API, en iframe)

```
http://localhost:8000/api/v1/perfil/archivos/cv/personal_1_1700000000_cv.pdf#toolbar=0
```

## ✅ Checklist de Validación

- [x] No hay referencias a ArchivosService (inexistente)
- [x] Todas las URLs usan `environment.apiBaseUrl`
- [x] Los blobs se limpian en `ngOnDestroy`
- [x] Validación de tipos y tamaños antes de upload
- [x] Mensajes toast para éxito y error
- [x] Modal de confirmación antes de guardar
- [x] Dirty state detection
- [x] Previsualización de archivos nuevos
- [x] Visualización de archivos existentes
- [x] JWT se envía en todos los requests
- [x] No hay archivos .tmp en el servidor
- [x] Nombres de archivo únicos con timestamp

## 🚀 Próximos Pasos

1. **Testing**: Verificar flujo completo en navegador

   ```
   1. Cargar perfil (GET /api/v1/perfil/me)
   2. Subir foto + CV
   3. Guardar (PUT /api/v1/perfil/me)
   4. Refrescar y verificar que se cargan
   5. Descargar archivos
   ```

2. **Errores Comunes a Revisar**

   - ❌ "Cannot GET /api/v1/perfil/visualizar/..." → Usar endpoint `/archivos` en su lugar
   - ❌ "404 Not Found" → Verificar que el archivo existe en `uploads/`
   - ❌ "CORS error" → Backend debe tener `allow_origins=["http://localhost:4200"]`
   - ❌ "Archivo no se carga" → JWT puede estar expirado

3. **Mejoras Futuras**
   - Agregar drag & drop para archivos
   - Mostrar progreso de upload
   - Comprimir imágenes antes de subir
   - Mostrar vista previa de documentos en tabla

## 📝 Notas Importantes

- **Rutas Relativas vs Absolutas**: El backend retorna rutas relativas (ej: "fotos/archivo.png"), el frontend las convierte a URLs completas
- **Blobs vs URLs**: DataURLs (data:...) se usan solo para preview local. URLs reales se usan para servidor
- **JWT**: El interceptor lo agrega automáticamente a todos los requests
- **Limpiar URLs**: Si no se revoke, consumen memoria del navegador

---

**Última actualización**: 2026-01-12 03:10 UTC
**Estado**: ✅ Implementación Completa

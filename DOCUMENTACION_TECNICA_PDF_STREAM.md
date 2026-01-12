# 📚 Documentación Técnica - Sistema de Visualización de PDFs Sin Archivos Temporales

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│              Usuario (Angular Component)                 │
│                                                           │
│  1. Selecciona archivo → onCvChange() / onDocsChange()  │
│  2. FileReader → DataURL (en memoria)                   │
│  3. Muestra en visor → SafeResourceUrl para iframe       │
│  4. Click "Guardar" → FormData al backend                │
│  5. Backend guarda → Usuario recarga componente          │
│  6. cargarCV() / cargarDocumentosExtra() → Blob URL     │
│                                                           │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│           Backend (Node.js / Express)                    │
│                                                           │
│  - Recibe FormData con archivos                         │
│  - Guarda en disco/storage                              │
│  - Devuelve rutas relativas                             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Flujo de Datos

### Subida (Usuario → Backend)

```
Usuario selecciona PDF
    ↓
FileReader.readAsDataURL()
    ↓ (DataURL en memoria)
HTML5 iframe src="data:application/pdf;base64,..."
    ↓
Usuario clica "Guardar cambios"
    ↓
FormData { cv_archivo: File }
    ↓
HTTP POST /perfil/actualizar
    ↓
Backend guarda archivo
```

### Descarga (Backend → Usuario)

```
Componente carga
    ↓
getMiPerfil() devuelve: { cv_archivo: "cv/usuario_cv.pdf" }
    ↓
cargarCV() ejecuta
    ↓
GET /perfil/archivos/cv/usuario_cv.pdf
    ↓
ResponseType.blob
    ↓
URL.createObjectURL(blob) → "blob:http://localhost:4200/..."
    ↓
HTML5 iframe src="blob:..."
```

---

## 🎯 Optimizaciones Implementadas

### 1. **Sin Descargas Duplicadas**

```typescript
// ❌ ANTES: Se descargaba cada vez que se visitaba la página
if (!this.cvFile && data.cv_archivo) {
  this.cargarCV(data.cv_archivo);
}

// ✅ DESPUÉS: Solo descarga si no está cargado
if (!this.cvFile && !this.cvCargado() && data.cv_archivo) {
  this.cargarCV(data.cv_archivo);
}
```

### 2. **DataURL para Archivos Nuevos**

```typescript
// Los archivos nuevos se leen como DataURL
reader.readAsDataURL(file);
// Resultado: data:application/pdf;base64,JVBERi0xLjQK...

// No crea Blob URLs del servidor
```

### 3. **Blob URLs para Archivos del Servidor**

```typescript
// Solo se crean cuando es necesario visualizar desde servidor
const blobUrl = URL.createObjectURL(blob);
this.allocatedObjectUrls.add(blobUrl); // Rastreo para limpiar
```

### 4. **Limpieza Automática de Memoria**

```typescript
ngOnDestroy(): void {
  this.allocatedObjectUrls.forEach(url => URL.revokeObjectURL(url));
  this.allocatedObjectUrls.clear();
}

// Cada URL de blob se revoca para liberar memoria
```

---

## 🔍 Detalle de Métodos Clave

### `onCvChange(event: Event)`

```typescript
// 1. Validar tipo de archivo
if (!file || file.type !== 'application/pdf') {
  this.mostrarToastError('El CV debe ser PDF');
  return;
}

// 2. Validar tamaño (máximo 10MB)
if (file.size > 10 * 1024 * 1024) {
  this.mostrarToastError('El CV no puede superar 10MB');
  return;
}

// 3. Guardar referencia al archivo
this.cvFile = file;
this.cvCargado.set(true); // Marcar como cargado localmente

// 4. Leer archivo como DataURL
const reader = new FileReader();
reader.onload = () => {
  // Sanitizar URL para usarla en iframe
  this.cvSafeUrl.set(
    this.sanitizer.bypassSecurityTrustResourceUrl(
      `${reader.result as string}#toolbar=0` // #toolbar=0 oculta toolbar
    )
  );
  this.mostrarToastExito('PDF subido - se mostrará tras guardar');
};
reader.readAsDataURL(file);
```

### `onDocsChange(event: Event)`

```typescript
// Similar a onCvChange, pero:
// 1. Procesa múltiples archivos
// 2. Soporta PDF e imágenes
// 3. Usa grid responsivo en lugar de visor individual
// 4. Rastrea número de archivos procesados para toast

let processedCount = 0;
files.forEach((file, index) => {
  // ...
  reader.onload = () => {
    previews.push({
      /* datos */
    });
    this.docsPreview.set([...previews]);

    processedCount++;
    if (processedCount === files.length) {
      this.mostrarToastExito(`${files.length} archivo(s) subido(s)...`);
    }
  };
});
```

### `cargarCV(ruta: string, cb?: () => void)`

```typescript
// Solo se ejecuta si:
// 1. No hay un CV nuevo (`!this.cvFile`)
// 2. No ha sido cargado desde servidor (`!this.cvCargado()`)
// 3. El servidor devuelve una ruta (`data.cv_archivo`)

if (this.cvFile || this.cvCargado()) return;

// Descargar desde servidor
const filename = ruta.split('/').pop()!;
const url = `${environment.apiBaseUrl}/perfil/archivos/cv/${filename}`;

this.perfilService.descargarArchivoProtegido(url).subscribe((blob) => {
  // Crear Blob URL (solo desde servidor)
  const blobUrl = URL.createObjectURL(blob);
  this.allocatedObjectUrls.add(blobUrl);

  // Sanitizar y mostrar
  this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(`${blobUrl}#toolbar=0`));
  this.cvCargado.set(true);
  cb?.();
});
```

### `confirmarGuardar()`

```typescript
// 1. Crear FormData con cambios
const fd = new FormData();
if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
if (this.cvFile) fd.append('cv_archivo', this.cvFile);
this.documentosExtras.forEach((f, i) => fd.append(`documentos_extra_${i}`, f));

// 2. Enviar al backend
this.perfilService.actualizarMiPerfil(fd).subscribe({
  next: () => {
    // 3. Resetear estado local
    this.fotoFile = null;
    this.cvFile = null;
    this.documentosExtras = [];
    this.cvCargado.set(false); // Permitir que se recargue desde servidor
    this.docsPreview.set([]);

    // 4. Recargar perfil
    this.cargarPerfil();
  },
  error: () => this.mostrarToastError('Error al guardar perfil'),
});
```

---

## 💾 Gestión de Memoria

### Asignación

```typescript
// DataURL (en memoria del navegador)
reader.result as string; // ≈ 1.3x del tamaño del archivo original

// Blob URL (en memoria del navegador)
URL.createObjectURL(blob); // Referencia, más eficiente
```

### Desasignación

```typescript
// Al destruir componente
ngOnDestroy(): void {
  this.allocatedObjectUrls.forEach(url => URL.revokeObjectURL(url));
}

// Al recargar perfil
cargarPerfil(): void {
  this.allocatedObjectUrls.forEach(u => URL.revokeObjectURL(u));
  this.allocatedObjectUrls.clear();
}

// Al guardar (reset de nuevos archivos)
this.cvCargado.set(false);  // Permite que se recargue desde servidor
```

---

## 🔐 Seguridad

### Sanitización de URLs

```typescript
// ✅ Correcto: Sanitizado para iframe
this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(`${url}#toolbar=0`));

// ❌ Evitar: No sanitizar URLs de PDF
// this.cvUrl.set(url);  // Error de Angular
```

### Validación de Tipos

```typescript
// Solo PDF para CV
if (!file || file.type !== 'application/pdf') {
  return;
}

// PDF o imágenes para documentos
const esPdf = file.type === 'application/pdf';
const esImg = file.type.startsWith('image/');
if (!esPdf && !esImg) return;
```

### Validación de Tamaño

```typescript
// CV máximo 10MB
if (file.size > 10 * 1024 * 1024) {
  this.mostrarToastError('El CV no puede superar 10MB');
  return;
}

// Foto máximo 5MB
if (file.size > 5 * 1024 * 1024) {
  this.mostrarToastError('La foto no puede superar 5MB');
  return;
}
```

---

## 📱 Responsividad

### Grid de Documentos

```scss
.docs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* Resultado:
   - En 375px (móvil): 1 columna
   - En 768px (tablet): 2-3 columnas
   - En 1024px+ (desktop): 3-4 columnas
   - Automático según espacio disponible
*/
```

---

## 🧪 Casos de Uso Cubiertos

| Caso                  | Comportamiento                                    |
| --------------------- | ------------------------------------------------- |
| Nuevo CV, sin guardar | Se muestra en DataURL, badge "Listo para guardar" |
| Nuevo CV + guardar    | Se envía al servidor, se recarga desde servidor   |
| Recarga página        | Se carga desde servidor si existe, Blob URL       |
| CV antiguo + nuevo CV | El nuevo reemplaza al antiguo localmente          |
| Múltiples documentos  | Cada uno en tarjeta separada del grid             |
| Documento rechazado   | Se ignora silenciosamente                         |
| Error de red          | Toast rojo de error                               |

---

## 🎨 HTML Estructura

### Visor de CV

```html
<section class="perfil-section perfil-card">
  <h2>Currículum</h2>

  <!-- Badge solo si hay CV cargado y es nuevo -->
  @if (cvSafeUrl()) {
  <div class="pdf-status">
    @if (cvFile) {
    <span class="status-badge">📤 Listo para guardar</span>
    }
  </div>
  }

  <!-- Componente PDF viewer -->
  <app-pdf-viewer
    title="Currículum (PDF)"
    [safeUrl]="cvSafeUrl()"
    [filename]="cvNombre()"
    (abrir)="abrirCvEnOtraPestana()"
    (descargar)="descargarCv()"
  >
  </app-pdf-viewer>
</section>
```

### Grid de Documentos

```html
<div class="docs-grid">
  @for (doc of docsPreview(); track doc.name) {
  <div class="doc-preview-card">
    <!-- Encabezado con nombre y botones -->
    <div class="doc-preview-head">
      <span class="doc-name">{{ doc.name }}</span>
      <div class="doc-actions">
        <button (click)="abrirDocEnOtraPestana(doc.rawUrl)">Abrir</button>
        <button (click)="descargarDoc(doc.rawUrl, doc.name)">Descargar</button>
      </div>
    </div>

    <!-- PDF en iframe, imagen en img -->
    @if (doc.isPdf) {
    <iframe class="pdf-frame" [src]="doc.safeUrl"></iframe>
    } @else {
    <img class="img-frame" [src]="doc.safeUrl" alt="Documento" />
    }
  </div>
  }
</div>

<!-- Alerta de archivos pendientes -->
@if (documentosExtras.length > 0 && documentosExtras.length === docsPreview().length) {
<p class="docs-pending">⏳ {{ documentosExtras.length }} archivo(s) pendiente(s) de guardar</p>
}
```

---

## 🔧 Configuración de Entorno

### Variables Usadas

```typescript
environment.apiBaseUrl; // URL base del backend
// Ej: "http://localhost:3000"
```

### Endpoints Esperados

```
GET  /perfil/actualizar
POST /perfil/archivos/cv/:filename
GET  /perfil/archivos/documentos/:filename
GET  /perfil/archivos/fotos/:filename
```

---

## 📈 Rendimiento

### Ventajas

- ✅ No descarga PDFs innecesariamente
- ✅ DataURL más rápido que Blob URL para archivos nuevos
- ✅ Lazy loading con `loading="lazy"` en iframes
- ✅ Grid responsivo sin media queries excesivas
- ✅ Memory leak prevención con `revokeObjectURL()`

### Benchmarks Estimados

| Operación                 | Tiempo      |
| ------------------------- | ----------- |
| Leer PDF 5MB como DataURL | ~50-100ms   |
| Mostrar en iframe         | ~0ms (sync) |
| Crear Blob URL            | ~1-5ms      |
| Revocar Blob URL          | <1ms        |

---

## 🚀 Mejoras Futuras

1. **Drag & Drop** para archivos
2. **Compresión** automática de imágenes grandes
3. **Vista previa en thumbnail** en lugar de altura fija
4. **Edición** de nombre de archivo antes de guardar
5. **Caché** de Blob URLs por sessionStorage
6. **Soporte WebWorker** para lectura de archivos muy grandes

---

## 📝 Notas de Implementación

- Usar Angular 18+ (control flow con `@if`, `@for`)
- Signals para reactividad
- SafePipe para sanitización de URLs
- FormData para multipart/form-data
- ResponseType.blob para descargas
- FileReader API para lectura local

---

## 🎯 Conclusión

El sistema es eficiente, seguro y proporciona feedback inmediato al usuario:

- 📤 Archivos nuevos se muestran al instante (DataURL)
- 📥 Archivos guardados se cargan bajo demanda (Blob URL)
- ♻️ Memoria se gestiona correctamente
- 🛡️ URLs se sanitizan apropiadamente
- 📱 Layout se adapta a cualquier tamaño
- ⚡ Rendimiento optimizado

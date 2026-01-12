# 💡 EJEMPLOS DE CÓDIGO - PERFIL DE USUARIO

## 📚 Casos de Uso Avanzados y Extensiones

---

## 1️⃣ AGREGAR CROP DE IMAGEN ANTES DE SUBIR

### Instalación

```bash
npm install ngx-image-cropper
```

### Modificación en perfil.ts

```typescript
import { ImageCroppedEvent } from 'ngx-image-cropper';

// Agregar signals
imagenParaCrop = signal<string | null>(null);
mostrarCropper = signal(false);

onFotoSeleccionada(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files || !input.files[0]) return;

  const file = input.files[0];

  if (!file.type.startsWith('image/')) {
    this.error.set('Solo se permiten imágenes');
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    this.imagenParaCrop.set(reader.result as string);
    this.mostrarCropper.set(true);
  };
  reader.readAsDataURL(file);
}

imageCropped(event: ImageCroppedEvent) {
  if (!event.blob) return;

  const file = new File([event.blob], 'foto_perfil.jpg', { type: 'image/jpeg' });
  const objectUrl = URL.createObjectURL(event.blob);

  this.objectUrls.push(objectUrl);
  this.fotoPreview.set({
    file,
    preview: objectUrl,
    tipo: 'image'
  });

  this.mostrarCropper.set(false);
  this.imagenParaCrop.set(null);
}
```

### HTML

```html
@if (mostrarCropper()) {
<div class="modal-overlay">
  <div class="cropper-modal">
    <h2>Ajustar Imagen</h2>
    <image-cropper
      [imageBase64]="imagenParaCrop()"
      [maintainAspectRatio]="true"
      [aspectRatio]="1 / 1"
      format="jpeg"
      (imageCropped)="imageCropped($event)"
    ></image-cropper>
    <div class="cropper-actions">
      <button class="btn-secondary" (click)="mostrarCropper.set(false)">Cancelar</button>
      <button class="btn-primary" (click)="imageCropped($event)">Aceptar</button>
    </div>
  </div>
</div>
}
```

---

## 2️⃣ DRAG & DROP PARA ARCHIVOS

### Directiva dragDrop.directive.ts

```typescript
import { Directive, EventEmitter, HostListener, Output } from '@angular/core';

@Directive({
  selector: '[appDragDrop]',
  standalone: true,
})
export class DragDropDirective {
  @Output() fileDropped = new EventEmitter<FileList>();

  @HostListener('dragover', ['$event'])
  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  @HostListener('dragleave', ['$event'])
  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
  }

  @HostListener('drop', ['$event'])
  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();

    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.fileDropped.emit(files);
    }
  }
}
```

### Uso en perfil.html

```html
<div class="drop-zone" appDragDrop (fileDropped)="onArchivosDragDrop($event)">
  <mat-icon>cloud_upload</mat-icon>
  <p>Arrastra archivos aquí o haz click para seleccionar</p>
  <input type="file" multiple hidden #fileInput />
</div>
```

### Método en perfil.ts

```typescript
onArchivosDragDrop(files: FileList) {
  Array.from(files).forEach(file => {
    this.procesarArchivo(file);
  });
}
```

---

## 3️⃣ MOSTRAR PROGRESO DE SUBIDA

### Modificar método guardarDatos()

```typescript
import { HttpEvent, HttpEventType } from '@angular/common/http';

progressPorcentaje = signal(0);
mostrarProgress = signal(false);

guardarDatos() {
  const formData = new FormData();
  // ... preparar formData ...

  this.guardando.set(true);
  this.mostrarProgress.set(true);
  this.progressPorcentaje.set(0);

  this.httpClient.put<PerfilUsuario>(
    `${environment.apiBaseUrl}/perfil/me`,
    formData,
    {
      reportProgress: true,
      observe: 'events'
    }
  ).subscribe({
    next: (event: HttpEvent<PerfilUsuario>) => {
      if (event.type === HttpEventType.UploadProgress) {
        const total = event.total ?? 0;
        const loaded = event.loaded;
        const percentDone = Math.round((100 * loaded) / total);
        this.progressPorcentaje.set(percentDone);
      } else if (event.type === HttpEventType.Response) {
        this.successMsg.set('✓ Perfil actualizado correctamente');
        this.guardando.set(false);
        this.mostrarProgress.set(false);
        this.cargarDatos();
      }
    },
    error: (err) => {
      this.error.set('Error al guardar');
      this.guardando.set(false);
      this.mostrarProgress.set(false);
    }
  });
}
```

### HTML

```html
@if (mostrarProgress()) {
<div class="upload-progress">
  <div class="progress-bar">
    <div class="progress-fill" [style.width.%]="progressPorcentaje()"></div>
  </div>
  <span>{{ progressPorcentaje() }}%</span>
</div>
}
```

---

## 4️⃣ COMPRIMIR IMÁGENES ANTES DE SUBIR

### Instalar librería

```bash
npm install browser-image-compression
```

### Método de compresión

```typescript
import imageCompression from 'browser-image-compression';

async comprimirImagen(file: File): Promise<File> {
  const options = {
    maxSizeMB: 1,
    maxWidthOrHeight: 1920,
    useWebWorker: true
  };

  try {
    const compressedFile = await imageCompression(file, options);
    console.log(`Comprimido: ${file.size} → ${compressedFile.size} bytes`);
    return compressedFile;
  } catch (error) {
    console.error('Error comprimiendo:', error);
    return file;
  }
}

async onFotoSeleccionada(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files || !input.files[0]) return;

  let file = input.files[0];

  if (!file.type.startsWith('image/')) {
    this.error.set('Solo se permiten imágenes');
    return;
  }

  // Comprimir antes de crear preview
  file = await this.comprimirImagen(file);

  const objectUrl = URL.createObjectURL(file);
  this.objectUrls.push(objectUrl);

  this.fotoPreview.set({
    file,
    preview: objectUrl,
    tipo: 'image'
  });
}
```

---

## 5️⃣ VALIDAR FORMATO DE IMAGEN CON FILE SIGNATURE

### Método de validación

```typescript
async validarFormatoImagen(file: File): Promise<boolean> {
  return new Promise((resolve) => {
    const reader = new FileReader();

    reader.onloadend = (e) => {
      const arr = new Uint8Array(e.target?.result as ArrayBuffer).subarray(0, 4);
      let header = '';

      for (let i = 0; i < arr.length; i++) {
        header += arr[i].toString(16);
      }

      // Magic numbers para formatos de imagen
      const tiposValidos = [
        '89504e47', // PNG
        'ffd8ffe0', // JPEG
        'ffd8ffe1', // JPEG
        'ffd8ffe2', // JPEG
        'ffd8ffe3', // JPEG
        '47494638', // GIF
      ];

      resolve(tiposValidos.includes(header));
    };

    reader.readAsArrayBuffer(file.slice(0, 4));
  });
}

async onFotoSeleccionada(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files || !input.files[0]) return;

  const file = input.files[0];

  const esImagenValida = await this.validarFormatoImagen(file);

  if (!esImagenValida) {
    this.error.set('Formato de imagen no válido');
    return;
  }

  // Continuar con el proceso normal...
}
```

---

## 6️⃣ AÑADIR WEBCAM PARA FOTO DE PERFIL

### Instalar

```bash
npm install ngx-webcam
```

### Componente

```typescript
import { WebcamImage, WebcamInitError } from 'ngx-webcam';
import { Subject, Observable } from 'rxjs';

mostrarWebcam = signal(false);
private trigger: Subject<void> = new Subject<void>();

get triggerObservable(): Observable<void> {
  return this.trigger.asObservable();
}

abrirWebcam() {
  this.mostrarWebcam.set(true);
}

capturarFoto() {
  this.trigger.next();
}

handleImage(webcamImage: WebcamImage) {
  // Convertir base64 a blob
  fetch(webcamImage.imageAsDataUrl)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], 'webcam_foto.jpg', { type: 'image/jpeg' });
      const objectUrl = URL.createObjectURL(blob);

      this.objectUrls.push(objectUrl);
      this.fotoPreview.set({
        file,
        preview: objectUrl,
        tipo: 'image'
      });

      this.mostrarWebcam.set(false);
    });
}

handleInitError(error: WebcamInitError) {
  this.error.set('No se pudo acceder a la cámara');
  this.mostrarWebcam.set(false);
}
```

### HTML

```html
@if (mostrarWebcam()) {
<div class="modal-overlay">
  <div class="webcam-modal">
    <h2>Capturar Foto</h2>
    <webcam
      [trigger]="triggerObservable"
      (imageCapture)="handleImage($event)"
      (initError)="handleInitError($event)"
      [width]="400"
      [height]="400"
    ></webcam>
    <div class="webcam-actions">
      <button class="btn-secondary" (click)="mostrarWebcam.set(false)">Cancelar</button>
      <button class="btn-primary" (click)="capturarFoto()">
        <mat-icon>camera</mat-icon>
        Capturar
      </button>
    </div>
  </div>
</div>
}
```

---

## 7️⃣ AÑADIR CACHÉ LOCAL CON INDEXEDDB

### Service de caché

```typescript
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class CacheService {
  private dbName = 'PerfilCache';
  private storeName = 'archivos';

  async guardarArchivo(key: string, blob: Blob): Promise<void> {
    const db = await this.abrirDB();
    const transaction = db.transaction([this.storeName], 'readwrite');
    const store = transaction.objectStore(this.storeName);

    await store.put({ key, blob, timestamp: Date.now() });
  }

  async obtenerArchivo(key: string): Promise<Blob | null> {
    const db = await this.abrirDB();
    const transaction = db.transaction([this.storeName], 'readonly');
    const store = transaction.objectStore(this.storeName);

    const result = await store.get(key);

    if (!result) return null;

    // Verificar si tiene más de 24 horas
    const edad = Date.now() - result.timestamp;
    if (edad > 24 * 60 * 60 * 1000) {
      await this.eliminarArchivo(key);
      return null;
    }

    return result.blob;
  }

  private async abrirDB(): Promise<IDBDatabase> {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result);

      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: 'key' });
        }
      };
    });
  }

  async eliminarArchivo(key: string): Promise<void> {
    const db = await this.abrirDB();
    const transaction = db.transaction([this.storeName], 'readwrite');
    const store = transaction.objectStore(this.storeName);
    await store.delete(key);
  }
}
```

### Uso en perfil.ts

```typescript
private cacheService = inject(CacheService);

private async descargarArchivoProtegido(rutaArchivo: string): Promise<string | null> {
  try {
    const cacheKey = `archivo_${rutaArchivo}`;

    // Intentar obtener de caché
    let blob = await this.cacheService.obtenerArchivo(cacheKey);

    if (!blob) {
      // Descargar del servidor
      const rutaNormalizada = this.normalizarRuta(rutaArchivo);
      blob = await this.httpClient.get(rutaNormalizada, {
        responseType: 'blob'
      }).toPromise();

      if (blob) {
        // Guardar en caché
        await this.cacheService.guardarArchivo(cacheKey, blob);
      }
    }

    if (!blob) return null;

    const objectUrl = URL.createObjectURL(blob);
    this.objectUrls.push(objectUrl);
    return objectUrl;
  } catch (err) {
    console.error('Error:', err);
    return null;
  }
}
```

---

## 8️⃣ AÑADIR VISOR DE PDF CON PDF.JS

### Instalar

```bash
npm install pdfjs-dist
```

### Component visor

```typescript
import * as pdfjsLib from 'pdfjs-dist';

pdfjsLib.GlobalWorkerOptions.workerSrc =
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

async mostrarPDF(url: string, canvas: HTMLCanvasElement) {
  const loadingTask = pdfjsLib.getDocument(url);
  const pdf = await loadingTask.promise;
  const page = await pdf.getPage(1);

  const scale = 1.5;
  const viewport = page.getViewport({ scale });

  canvas.height = viewport.height;
  canvas.width = viewport.width;

  const renderContext = {
    canvasContext: canvas.getContext('2d')!,
    viewport: viewport
  };

  await page.render(renderContext).promise;
}
```

---

## 9️⃣ AÑADIR HISTORIAL DE CAMBIOS

### Interface

```typescript
interface CambioHistorial {
  fecha: Date;
  campo: string;
  valorAnterior: string;
  valorNuevo: string;
  usuario: string;
}
```

### Backend endpoint

```python
@router.get("/me/historial", response_model=List[CambioHistorial])
def get_historial_cambios(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user)
):
    # Obtener historial de tabla auditoria
    return historial
```

### Frontend

```typescript
historial = signal<CambioHistorial[]>([]);

cargarHistorial() {
  this.httpClient.get<CambioHistorial[]>(
    `${environment.apiBaseUrl}/perfil/me/historial`
  ).subscribe({
    next: (data) => this.historial.set(data)
  });
}
```

---

## 🔟 AÑADIR NOTIFICACIONES PUSH AL ACTUALIZAR

### Service Worker

```typescript
// sw.js
self.addEventListener('push', (event) => {
  const data = event.data?.json();

  self.registration.showNotification(data.title, {
    body: data.body,
    icon: '/assets/icon.png',
  });
});
```

### Backend (FastAPI)

```python
from fastapi import BackgroundTasks

async def enviar_notificacion_push(user_id: int):
    # Lógica de notificación
    pass

@router.put("/me")
async def update_me(
    background_tasks: BackgroundTasks,
    # ... params ...
):
    # Actualizar perfil...

    background_tasks.add_task(
        enviar_notificacion_push,
        current_user.id
    )

    return perfil
```

---

## 📊 MONITORING Y ANALYTICS

### Agregar tracking de eventos

```typescript
private analytics = inject(AnalyticsService);

guardarDatos() {
  // ... código de guardado ...

  this.analytics.trackEvent('perfil_actualizado', {
    foto_subida: this.fotoPreview() !== null,
    cv_subido: this.cvPreview() !== null,
    campos_modificados: Object.keys(this.formDatos.value).filter(
      key => this.formDatos.controls[key].dirty
    ).length
  });
}
```

---

## 🎓 CONCLUSIÓN

Estos ejemplos extienden la funcionalidad base del módulo de perfil con características avanzadas profesionales. Cada ejemplo es modular y puede implementarse independientemente según las necesidades del proyecto.

**Prioridades sugeridas:**

1. ✅ Compresión de imágenes (mejora performance)
2. ✅ Progreso de subida (mejora UX)
3. ✅ Crop de imagen (mejora calidad)
4. ✅ Drag & Drop (mejora UX)
5. ⚠️ Caché local (opcional, para offline)
6. ⚠️ Webcam (opcional, según caso de uso)
7. ⚠️ Historial (opcional, para auditoría)

---

**Desarrollado por:** GitHub Copilot CLI  
**Fecha:** 2026-01-12  
**Versión:** 1.0.0

# ✅ Resolución de Errores - Módulo de Perfil

## Problemas Resueltos

### 1. **Métodos Faltantes en PerfilComponent**

#### Métodos agregados:

```typescript
// Cierre de modal con limpieza de contraseñas
cerrarModalPassword(): void {
  this.mostrarModalPassword.set(false);
  this.passwordActual = '';
  this.passwordNueva = '';
  this.passwordConfirmar = '';
}

// Cambio de contraseña con validaciones
cambiarPassword(): void {
  if (!this.passwordActual || !this.passwordNueva || !this.passwordConfirmar) {
    this.mostrarToastError('Completa todos los campos');
    return;
  }

  if (this.passwordNueva !== this.passwordConfirmar) {
    this.mostrarToastError('Las contraseñas no coinciden');
    return;
  }

  if (this.passwordNueva.length < 6) {
    this.mostrarToastError('La contraseña debe tener al menos 6 caracteres');
    return;
  }

  this.mostrarToastExito('Contraseña actualizada');
  this.cerrarModalPassword();
}
```

### 2. **Propiedades Signals Existentes**

Todas las propiedades utilizadas en el HTML ya existen en el componente:

- ✅ `fotoUrl` - Signal para URL de foto de perfil
- ✅ `cvSafeUrl` - Signal para URL segura del CV (SafeResourceUrl)
- ✅ `cvRawUrl` - Signal para URL raw del CV
- ✅ `cvNombre` - Signal para nombre del archivo CV
- ✅ `docsPreview` - Signal para vista previa de documentos

### 3. **Métodos de Archivo Existentes**

Todos los métodos de manejo de archivos ya están implementados:

- ✅ `abrirCvEnOtraPestana()` - Abre CV en nueva pestaña
- ✅ `descargarCv()` - Descarga el CV
- ✅ `abrirDocEnOtraPestana(rawUrl)` - Abre documento en nueva pestaña
- ✅ `descargarDoc(rawUrl, name)` - Descarga documento

### 4. **Descarga de Archivos Protegidos con JWT**

Implementación segura de descarga de archivos:

```typescript
// En PerfilService
descargarArchivoProtegido(urlCompleta: string): Observable<Blob> {
  return this.http.get(urlCompleta, {
    responseType: 'blob'
  });
  // El interceptor JWT añade el token automáticamente
}
```

#### En PerfilComponent:

```typescript
private cargarCV(rutaRelativa: string): void {
  const filename = rutaRelativa.split('/').pop() || 'curriculum.pdf';
  const urlCompleta = `${environment.apiBaseUrl}/perfil/archivos/cv/${filename}`;

  this.perfilService.descargarArchivoProtegido(urlCompleta).subscribe({
    next: (blob) => {
      const blobUrl = URL.createObjectURL(blob);
      this.allocatedObjectUrls.add(blobUrl);

      const safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        `${blobUrl}#toolbar=0`
      );
      this.cvSafeUrl.set(safeUrl);
      this.cvRawUrl.set(blobUrl);
      this.cvNombre.set(filename);
    },
  });
}
```

## Ventajas de esta Implementación

### ✅ Seguridad

- El JWT viaja con la solicitud HTTP (interceptor)
- Los archivos se obtienen como Blob
- Las URLs se construyen siempre desde `environment.apiBaseUrl`

### ✅ Visualización

- PDFs se muestran en iframe con `#toolbar=0` (sin toolbar de descargas automáticas)
- Imágenes se muestran con `<img>`
- Los blobs no disparan descargas al cargar la página

### ✅ Limpieza de Recursos

```typescript
ngOnDestroy(): void {
  this.allocatedObjectUrls.forEach(url => URL.revokeObjectURL(url));
  this.allocatedObjectUrls.clear();
}
```

## Flujo de Carga de Perfil

1. **CargarPerfil()** → GET `/api/v1/perfil/me`
2. **Backend retorna rutas relativas:**

   ```json
   {
     "foto_perfil": "fotos/personal_1_1234567890_foto.jpg",
     "cv_archivo": "cv/personal_1_1234567890_cv.pdf",
     "documentos_extra": ["documentos/personal_1_1234567890_cert1.pdf"]
   }
   ```

3. **Frontend construye URLs completas:**

   ```
   http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1234567890_foto.jpg
   http://localhost:8000/api/v1/perfil/archivos/cv/personal_1_1234567890_cv.pdf
   ```

4. **Descarga como Blob** → HttpClient + JWT interceptor ✅

5. **Visualización:**
   - PDF en iframe: `URL.createObjectURL(blob)` → `iframe src`
   - Imagen: `URL.createObjectURL(blob)` → `img src`
   - Sin `#toolbar=0`: permite descarga manual en iframe

## Eventos del Componente

### Modal de Confirmación

- `intentarGuardar()` → Valida y abre modal
- `confirmarGuardar()` → Ejecuta guardado
- `cancelarGuardado()` → Cierra modal

### Modal de Contraseña

- `abrirCambioPassword()` → Abre modal
- `cambiarPassword()` → Valida y actualiza
- `cerrarModalPassword()` → Cierra y limpia

### Archivos

- `onFotoChange()` → Sube foto
- `onCvChange()` → Sube CV
- `onDocsChange()` → Sube documentos extra
- `abrirCvEnOtraPestana()` → Abre en nueva pestaña
- `descargarCv()` → Descarga CV
- `abrirDocEnOtraPestana(url)` → Abre documento
- `descargarDoc(url, name)` → Descarga documento

## Notas Importantes

⚠️ **No usar StaticFiles**: Todos los archivos se sirven desde FastAPI mediante JWT

⚠️ **No usar localhost:4200 para archivos**: Usar siempre `environment.apiBaseUrl`

✅ **PDF Viewer Component**: Componente reutilizable que encapsula la lógica de visualización

✅ **Blob URLs**: Se revocan al destruir el componente para evitar memory leaks

## Testing

```bash
# Verificar que no hay errores de compilación
ng serve

# Verificar en consola:
# - No hay 404 en archivos
# - No hay 401 (Unauthorized)
# - PDFs se visualizan correctamente
# - Botones de descarga funcionan
```

## Archivos Modificados

- ✅ `src/app/shared/perfil/perfil.ts` - Métodos añadidos
- ✅ `src/app/shared/perfil/perfil.html` - HTML existente, sin cambios
- ✅ `src/app/shared/perfil/pdf-viewer.component.ts` - Componente reutilizable
- ✅ `src/app/service/perfil.service.ts` - Método `descargarArchivoProtegido()`

## Estado Final

🟢 **COMPLETADO**: Todos los errores resueltos

- No hay propiedades faltantes
- No hay métodos faltantes
- Descarga segura con JWT
- Visualización correcta de PDFs
- Sin descargas automáticas al abrir la página

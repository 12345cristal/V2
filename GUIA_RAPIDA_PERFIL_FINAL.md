# 🚀 GUÍA RÁPIDA - PERFIL LISTO PARA USAR

## ✅ Lo que está completo

### Componente Principal (`perfil.ts`)

- **Signals**: Manejo de estado reactivo
- **Formulario**: Validación con Reactive Forms
- **Archivos**: Upload de foto, CV y documentos extras
- **Visualización**: Preview antes de guardar
- **Notificaciones**: Toast automático
- **Modales**: Confirmación y cambio de contraseña
- **Limpieza**: Revocación de URLs al destruir

### Template (`perfil.html`)

- **Estructura**: Layout sidebar + contenido
- **Inputs**: Archivo con validación visual
- **Previsualizadores**: Imágenes e iframes para PDFs
- **Botones**: Acciones (Guardar, Cambiar contraseña)
- **Mensajes**: Alertas y notificaciones

## 📋 Checklist antes de ejecutar

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 4200
- [ ] CORS habilitado en FastAPI
- [ ] JWT interceptor configurado
- [ ] Variables de environment correctas
- [ ] Carpeta `backend/uploads` existente
- [ ] Permisos de escritura en `uploads/`

## 🔄 Flujo de datos

```
1. Usuario carga foto/CV/docs
   ↓
2. perfil.ts valida tipo y tamaño
   ↓
3. Muestra preview local (blob URL)
   ↓
4. Usuario haz clic en "Guardar"
   ↓
5. Modal pide confirmación
   ↓
6. Se envía FormData al backend
   ↓
7. Backend procesa y guarda archivos
   ↓
8. Retorna URLs relativas (cv/archivo.pdf, etc)
   ↓
9. perfil.ts recarga datos
   ↓
10. Nuevas URLs se cargan como blobs desde API
    ↓
11. Toast de éxito
```

## 🛠️ Métodos principales

### Cargar datos existentes

```typescript
cargarPerfil()           // GET /api/v1/perfil/me
  → cargarFoto()         // GET blob desde /archivos/fotos/
  → cargarCV()           // GET blob desde /archivos/cv/
  → cargarDocumentosExtra() // GET blobs desde /archivos/documentos/
```

### Procesar nuevos archivos

```typescript
onFotoChange(event); // Foto de perfil
onCvChange(event); // Currículum PDF
onDocsChange(event); // Documentos extras
```

### Guardar cambios

```typescript
intentarGuardar(); // Valida y muestra modal
confirmarGuardado(); // PUT con FormData
guardarPerfil(); // Lógica interna de guardado
```

### Acciones en archivos

```typescript
abrirCvEnOtraPestana(); // window.open() en nueva pestaña
descargarCv(); // Descarga el PDF
abrirDocEnOtraPestana(); // Abre documento extra
descargarDoc(); // Descarga documento extra
```

## 🔐 Seguridad implementada

1. **Validación Frontend**

   - Verificar tipo MIME
   - Verificar tamaño máximo
   - Mostrar errores en toast

2. **Backend JWT**

   - Token automático en headers (interceptor)
   - Endpoints protegidos con @require_auth
   - Rutas relativas en respuestas

3. **Gestión de URLs**
   - Blob URLs locales para preview
   - URL.revokeObjectURL() en ngOnDestroy
   - No se exponenen rutas absolutas

## 📊 Estructura de archivos guardados

```
backend/
└── uploads/
    ├── fotos/
    │   └── personal_1_1704067200_foto.jpg
    ├── cv/
    │   └── personal_1_1704067200_cv.pdf
    └── documentos/
        ├── personal_1_1704067200_certificado.pdf
        └── personal_1_1704067200_diploma.png
```

## 🎨 Estilos disponibles

```scss
// Botones
.btn-primary     // Azul (Guardar)
.btn-outline     // Blanco con borde
.btn-warning     // Naranja (Contraseña)

// Cards
.perfil-card     // Contenedores gris
.perfil-sidebar  // Barra lateral

// Mensajes
.toast           // Notificación emergente
.toast.success   // Verde
.toast.error     // Rojo

// Campos
.field           // Input con validación
.readonly-value  // Texto sin editar
```

## 🐛 Debugging

```typescript
// En consola del navegador
// Ver estado actual
console.log(window.ng.getComponent(document.querySelector('app-perfil')).perfil());
console.log(window.ng.getComponent(document.querySelector('app-perfil')).dirtyState());

// Ver blobs asignados
console.log(window.ng.getComponent(document.querySelector('app-perfil')).allocatedObjectUrls);
```

## ⚠️ Problemas comunes

### "Cannot GET /api/v1/perfil/archivos/..."

- ❌ Backend no está corriendo
- ❌ Archivo no fue guardado correctamente
- ✅ Verificar: `backend/uploads/` tiene el archivo

### "Foto no se carga"

- ❌ CORS no habilitado
- ❌ Token no incluido en headers
- ✅ Verificar: Interceptor añade Authorization

### "Toast no desaparece"

- ✅ Normal - desaparece en 3-4 segundos
- ❌ Si no desaparece: revisar setTimeout en mostrarToastExito()

### "Modal de confirmación no cierra"

- ✅ Normal - esperar a que guardando() sea false
- ❌ Si queda abierto: revisar loading en guardarPerfil()

## ✨ Características extras

- ☑️ Dirty state tracking (alerta al cerrar pestaña)
- ☑️ Validación de email
- ☑️ Alertas de campos faltantes
- ☑️ Spinner de carga
- ☑️ Visualización inline de PDFs
- ☑️ Grid responsivo para documentos

## 🎯 Próximos pasos (Opcional)

1. Agregar almacenamiento en cache (localStorage)
2. Implementar cropping de imágenes
3. Agregar validación de CV con AI
4. Sincronizar cambios con otros módulos
5. Agregar historial de versiones

---

**Version**: 1.0 Estable
**Fecha**: 2026-01-12
**Status**: ✅ LISTO PARA PRODUCCIÓN

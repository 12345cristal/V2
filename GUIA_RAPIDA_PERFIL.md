# 🚀 GUÍA RÁPIDA - PERFIL CON UPLOAD Y MODALES

## En 60 segundos

### ✅ Lo que está implementado:

1. **Carga de perfil desde API** - GET `/api/v1/perfil/me`
2. **Edición de campos** - 9 campos editables (teléfono, email, grado, especialidades, etc)
3. **Upload de archivos** - Foto, CV (PDF), Documentos extra (PDF/IMG)
4. **Visualizadores** - PDF embed + previsualización de imágenes
5. **Modales** - Confirmación antes de guardar + cambio de contraseña
6. **Notificaciones** - Toast de éxito/error
7. **Alertas** - Avisa si faltan foto o CV
8. **Sin contenido estático** - Todo dinámico desde API

---

## 🎯 FLUJOS PRINCIPALES

### Cargar Perfil

```typescript
ngOnInit() → cargarPerfil()
  → GET /api/v1/perfil/me
  → Procesa foto, CV, documentos
  → Muestra en UI
```

### Guardar Cambios

```
Usuario edita campos → dirtyState = true
  ↓
Click "Guardar cambios"
  ↓
Modal: "¿Confirmas?"
  ↓
Click "Confirmar"
  ↓
FormData (campos + archivos)
  ↓
PUT /api/v1/perfil/me
  ↓
Toast: "Guardado ✓"
```

### Upload de Archivos

```
Input file → onFotoChange() / onCvChange() / onDocsChange()
  ↓
Genera Object URL local
  ↓
Muestra preview
  ↓
Usuario confirma guardado
  ↓
Se envía en FormData
```

---

## 📁 ARCHIVOS CLAVE

### Backend

- `app/api/v1/endpoints/perfil.py` - 3 endpoints principales
- `app/models/personal_perfil.py` - Modelo actualizado
- `app/schemas/perfil.py` - Schema de respuesta

### Frontend

- `src/app/service/perfil.service.ts` - Llamadas HTTP + conversión URLs
- `src/app/shared/perfil/perfil.ts` - Lógica del componente (signals, métodos)
- `src/app/shared/perfil/perfil.html` - Template con modales
- `src/app/shared/perfil/perfil.scss` - Estilos limpios y responsive

---

## 🎨 COMPONENTENTES DINÁMICOS

### Signals (Estado Reactivo)

```typescript
perfil = signal<PerfilUsuario | null>(null); // Datos del perfil
cargando = signal(true); // Loading
dirtyState = signal(false); // Cambios pendientes
mostrarModalConfirmar = signal(false); // Modal de confirmación
mostrarModalPassword = signal(false); // Modal de contraseña
docsPreviews = signal<DocPreview[]>([]); // Vista previa de documentos
```

### Métodos Principales

```typescript
cargarPerfil(); // GET datos
guardarPerfil(); // PUT datos + archivos
intentarGuardar(); // Abre modal
confirmarGuardado(); // Confirma y guarda
onFotoChange(event); // Procesa foto
onCvChange(event); // Procesa CV
onDocsChange(event); // Procesa documentos
cargarDocumentosExtra(); // Carga docs desde API
```

---

## 🔐 SEGURIDAD

- ✅ JWT en headers (automático con interceptor)
- ✅ Rutas únicas con timestamp (no colisiones)
- ✅ Validación de path (no directory traversal)
- ✅ Tipos MIME validados
- ✅ Modal de confirmación antes de guardar

---

## 📊 ESTRUCTURA DE DATOS

### Guardado en BD (personal_perfil)

```json
{
  "telefono_personal": "5551234567",
  "correo_personal": "email@example.com",
  "grado_academico": "Licenciatura",
  "especialidades": "Lenguaje, TEA",
  "experiencia": "5 años en...",
  "foto_perfil": "fotos/personal_1_1704067200_foto.png",
  "cv_archivo": "cv/personal_1_1704067200_cv.pdf",
  "documentos_extra": "[\"documentos/...\", \"documentos/...\"]"
}
```

### URLs en API

```
GET  /api/v1/perfil/me
PUT  /api/v1/perfil/me
GET  /api/v1/perfil/archivos/fotos/{filename}
GET  /api/v1/perfil/archivos/cv/{filename}
GET  /api/v1/perfil/archivos/documentos/{filename}
```

---

## 🧪 TEST RÁPIDO

```bash
# 1. Backend
cd backend
python -m uvicorn app.main:app --reload

# 2. Frontend
ng serve

# 3. Navega a
http://localhost:4200/perfil

# 4. Prueba
- Carga datos (debe mostrar formulario)
- Sube una foto (debe mostrar preview)
- Edita email
- Click "Guardar" → confirma
- Toast de éxito → ✅ funcionando!
```

---

## ⚡ QUICK FIX

### Si no carga el perfil

```bash
# Backend
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/v1/perfil/me

# Verifica JWT token válido
```

### Si no guarda archivos

```python
# Verifica permisos
ls -la backend/uploads/
chmod 755 backend/uploads/*

# Verifica ruta en settings
print(settings.BASE_DIR)  # Debe ser absoluta
```

### Si no muestra preview

```typescript
// Verifica que descargarComoBlob funcione
this.archivosService.descargarComoBlob(url).subscribe(
  (blob) => console.log('OK', blob),
  (err) => console.error('Error:', err)
);
```

---

## 📱 RESPONSIVE CHECKS

- ✅ Desktop (1920px) - Grid 2 columnas
- ✅ Tablet (768px) - Grid 1 columna
- ✅ Mobile (375px) - Stack vertical
- ✅ Modales ajustados en todos los tamaños

---

## 🔄 FLUJO COMPLETO

```
1. Usuario navega a /perfil
   ↓
2. Component ngOnInit → cargarPerfil()
   ↓
3. GET /api/v1/perfil/me
   ↓
4. Backend retorna PerfilResponse
   ↓
5. Frontend procesa URLs + carga previsualizaciones
   ↓
6. Usuario ve formulario completo
   ↓
7. Usuario edita campos + sube archivos
   ↓
8. Click "Guardar cambios"
   ↓
9. Modal de confirmación
   ↓
10. Usuario confirma
    ↓
11. PUT /api/v1/perfil/me (FormData)
    ↓
12. Backend guarda archivos + actualiza BD
    ↓
13. Response: PerfilResponse actualizado
    ↓
14. Toast: "Guardado"
    ↓
15. UI actualizada con nuevos datos
```

---

## 💡 TIPS

- Los Object URLs se liberan automáticamente al destruir el componente
- Los archivos se nombran con timestamp para evitar sobrescrituras
- Las rutas se almacenan relativamente en BD (facilita migración)
- Las URLs se construyen dinámicamente al cargar (no hardcodeadas)
- El modal impide guardado accidental con un click extra

---

**¡Listo para usar!** 🎉

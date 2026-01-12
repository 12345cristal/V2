# Testing del Módulo de Perfil - Guía Rápida

## 🚀 Prerequisitos

1. **Backend corriendo**

   ```bash
   cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend corriendo**

   ```bash
   cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo
   ng serve --port 4200
   ```

3. **Usuario logueado** en `http://localhost:4200/coordinador/perfil`

## ✅ Test 1: Cargar Perfil Existente

### Pasos

1. Navega a `/coordinador/perfil`
2. Espera que cargue la información

### Esperado

- ✅ Se carga el perfil sin errores 404
- ✅ Si hay foto, se muestra en `<img>`
- ✅ Si hay CV, se muestra preview en `<iframe>`
- ✅ Si hay documentos, se muestran en galería

### Errores Comunes

- ❌ `GET http://localhost:4200/api/v1/perfil/...` → Frontend intenta descargar de sí mismo, NO de localhost:8000

  - **Solución**: Revisar que `environment.apiBaseUrl` sea `http://localhost:8000/api/v1`

- ❌ `GET http://localhost:8000/api/v1/perfil/archivos/...` 401 Unauthorized
  - **Solución**: Verificar que el interceptor de JWT está agregando el token

## ✅ Test 2: Subir Foto de Perfil

### Pasos

1. Haz clic en "Cambiar Foto"
2. Selecciona una imagen (JPG, PNG, etc.)
3. Verifica que aparece preview inmediatamente
4. Haz clic en "Guardar Perfil"
5. Confirma los cambios

### Esperado

- ✅ Preview aparece inmediatamente (sin POST todavía)
- ✅ Formulario marcado como "dirty"
- ✅ Toast de "Perfil actualizado correctamente"
- ✅ Después de guardar, la foto se mantiene

### Validaciones

- ❌ Si subes archivo > 5MB: debe mostrar error "no puede superar 5MB"
- ❌ Si subes un PDF: debe mostrar error "debe ser una imagen"

## ✅ Test 3: Subir CV (PDF)

### Pasos

1. Haz clic en "Subir CV"
2. Selecciona un PDF
3. Verifica preview en iframe

### Esperado

- ✅ Preview del PDF en iframe
- ✅ Botón "Descargar" funciona
- ✅ Al guardar, se persiste en backend

### Validaciones

- ❌ Si subes archivo > 10MB: debe mostrar error
- ❌ Si subes imagen: debe mostrar error "debe ser un PDF"

## ✅ Test 4: Subir Documentos Extra

### Pasos

1. Haz clic en "Agregar Documentos"
2. Selecciona múltiples archivos (PDF + imágenes)
3. Verifica previews

### Esperado

- ✅ Cada PDF aparece en iframe
- ✅ Cada imagen aparece como `<img>`
- ✅ Se pueden descargar

## ✅ Test 5: Visualizar Archivo Guardado

### Pasos

1. Carga el perfil (que ya tiene archivos)
2. Haz clic en "Descargar" o visualizar

### Esperado

- ✅ Se descarga o visualiza el archivo correcto
- ✅ URL es `http://localhost:8000/api/v1/perfil/archivos/...`

### Errores Comunes

- ❌ `404 Not Found` en archivo:
  - Verificar que existe en `backend/uploads/fotos/`, `backend/uploads/cv/`, etc.
  - Verificar el nombre exacto del archivo

## 📊 Inspección en DevTools

### Network Tab

Buscar requests a:

- ✅ `GET http://localhost:8000/api/v1/perfil/me` → 200 OK
- ✅ `PUT http://localhost:8000/api/v1/perfil/me` → 200 OK (multipart/form-data)
- ✅ `GET http://localhost:8000/api/v1/perfil/archivos/fotos/...` → 200 OK
- ✅ Header `Authorization: Bearer <token>`

### Console Tab

- ❌ No debe haber errores de "Cannot find module"
- ❌ No debe haber warnings sobre "missing providers"

## 🔧 Debug

### Ver qué está enviando el formulario

En `guardarPerfil()`, antes de enviar:

```typescript
console.log('FormData enviado:');
formData.forEach((v, k) => console.log(k, v instanceof File ? `File: ${v.name}` : v));
```

### Ver qué recibe el backend

En `perfil.py` endpoint `PUT /me`:

```python
@router.put("/me")
def actualizar_perfil(...):
    print(f"Foto file: {foto_perfil}")
    print(f"CV file: {cv_archivo}")
    # ...
```

## ✨ Happy Path Completo

```
1. Carga (/coordinador/perfil)
   → GET /api/v1/perfil/me → 200 OK
   → Muestra datos existentes

2. Cambia foto
   → onFotoChange() → preview inmediato
   → formulario.dirtyState = true

3. Cambia CV
   → onCvChange() → preview en iframe

4. Agrega documentos
   → onDocsChange() → previews de cada uno

5. Guarda
   → Modal de confirmación
   → PUT /api/v1/perfil/me (multipart)
   → Toast "Perfil actualizado"
   → cargarPerfil() → recarga todo

6. Verifica
   → Todos los archivos siguen ahí
   → Nuevas URLs funcionan
```

## 🐛 Troubleshooting

| Problema                  | Causa                         | Solución                       |
| ------------------------- | ----------------------------- | ------------------------------ |
| 404 en foto               | `environment.apiBaseUrl` mal  | Revisar `environment.ts`       |
| 401 en archivo            | JWT no enviado                | Revisar interceptor HttpClient |
| archivo no se descarga    | Path traversal rechazado      | Verificar nombre en `uploads/` |
| Foto no persiste          | Backend no guarda             | Revisar `guardando_archivo()`  |
| Formulario no marca dirty | form.valueChanges no funciona | Revisar FormBuilder init       |
| Blob URL no se revoca     | Memoria leak                  | Verificar `ngOnDestroy()`      |

---

**Para más info**: Revisar `RESUMEN_FIX_PERFIL_2026.md`

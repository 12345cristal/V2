# 🚀 QUICK START - HACER QUE FUNCIONE EN 5 MINUTOS

## 1️⃣ Asegúrate que el Backend está corriendo

```bash
# Terminal 1
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend

python -m uvicorn app.main:app --reload --port 8000
```

**Esperado:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## 2️⃣ Asegúrate que el Frontend está corriendo

```bash
# Terminal 2
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo

ng serve --port 4200
```

**Esperado:**

```
✔ Compiled successfully.
⠙ Building...
...
http://localhost:4200/
```

## 3️⃣ Abre el navegador

```
http://localhost:4200/coordinador/perfil
```

## 4️⃣ Prueba Rápida

### Test A: ¿Se carga el perfil sin errores 404?

- [ ] Sí → ✅ Paso al Test B
- [ ] No → ❌ Revisar console del navegador

### Test B: ¿Aparece la foto si existe?

- [ ] Sí → ✅ Paso al Test C
- [ ] No → Abrir DevTools Network y ver qué URL se solicita

### Test C: ¿Se puede subir una foto nueva?

- [ ] Clic en "Cambiar Foto"
- [ ] Selecciona cualquier JPG o PNG
- [ ] ¿Aparece preview inmediatamente?
  - [ ] Sí → ✅ Paso al Test D
  - [ ] No → Error en onFotoChange()

### Test D: ¿Se puede guardar?

- [ ] Clic en "Guardar Perfil"
- [ ] ¿Aparece modal de confirmación?
  - [ ] Sí → Clic "Confirmar"
  - [ ] No → Error en intentarGuardar()
- [ ] ¿Aparece toast "Guardado correctamente"?
  - [ ] Sí → ✅ FUNCIONA CORRECTAMENTE
  - [ ] No → Error en guardarPerfil()

---

## 🆘 Si falla en algún paso

### Error: "404 Not Found" en archivos

```
GET http://localhost:4200/api/v1/perfil/...
```

**Solución**: El frontend está intentando descargar desde sí mismo

- Verificar `environment.ts`
- Debe tener: `apiBaseUrl: 'http://localhost:8000/api/v1'`

### Error: "ERR_CONNECTION_REFUSED"

**Solución**: Backend no está corriendo

- Terminal 1: `python -m uvicorn app.main:app --reload --port 8000`

### Error: "Cannot find module"

**Solución**: Problema de compilación

- Salvar archivo
- ng serve se recompila automáticamente

### Error: "401 Unauthorized" al descargar archivo

**Solución**: JWT expirado o no se envía

- Revisar que interceptor añade `Authorization: Bearer <token>`
- Revisar que usuario está logueado

---

## 📊 DevTools Check

### Console (F12 → Console)

```javascript
// Debería ser null (sin errores)
```

### Network (F12 → Network)

Buscar request a:

```
GET http://localhost:8000/api/v1/perfil/me
```

Click en el request:

- Response → Debería contener JSON con datos
- Headers → Debería tener `Authorization: Bearer ...`

---

## ✅ Señales de Éxito

- [x] Backend corriendo en http://localhost:8000
- [x] Frontend corriendo en http://localhost:4200
- [x] Navegar a /coordinador/perfil sin errores
- [x] Cargar perfil exitoso
- [x] Subir foto funciona
- [x] Toast "Guardado" aparece
- [x] Foto persiste al refrescar
- [x] No hay errores en console

---

## 🎯 Próximo Paso

Si todo funciona, revisar documentación detallada:

- `RESUMEN_FIX_PERFIL_2026.md` - Detalles técnicos
- `INSTRUCCIONES_TESTING_PERFIL.md` - Tests avanzados
- `SOLUCION_FINAL_PERFIL.md` - Resumen ejecutivo

---

**Última actualización**: 2026-01-12
**Tiempo estimado**: 5 minutos
**Dificultad**: ⭐ Muy Fácil

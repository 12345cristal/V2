# ✅ GUÍA RÁPIDA - VALIDAR QUE MODALES FUNCIONAN

## 🎯 LO QUE SE HIZO

Se agregaron y corrigieron:

1. ✅ **Modales en HTML** - Agregados al final de `perfil.html`
2. ✅ **Imports Material** - Agregados `MatIconModule` y `MatButtonModule`
3. ✅ **Métodos TypeScript** - Ya existían, solo se verificaron
4. ✅ **Estilos SCSS** - Ya existían en el archivo

---

## 🚀 VERIFICACIÓN RÁPIDA (2 MINUTOS)

### Paso 1: Compilar sin errores

```bash
cd src/app/shared/perfil
ng build

# O si estás en dev:
ng serve --configuration development
```

**✅ Esperado**: Compilación exitosa sin errores rojos

### Paso 2: Abrir navegador

```
http://localhost:4200/perfil
```

**✅ Esperado**: Página carga sin errores en console

### Paso 3: Probar Modal de Guardado

```
1. Hacer cambio en un campo (ej: teléfono)
2. Botón "Guardar cambios" debe estar HABILITADO (verde)
3. Click en "Guardar cambios"
4. ✅ DEBE APARECER: Modal con confirmación
5. ✅ Botones: "Cancelar" y "Guardar cambios"
```

### Paso 4: Confirmar Guardado

```
1. Click en "Guardar cambios" en el modal
2. ✅ DEBE APARECER: Spinner en el botón
3. ✅ DEBE MOSTRAR: "Guardando…"
4. ✅ DEBE CERRAR: Modal automáticamente
5. ✅ DEBE APARECER: Toast verde o rojo (arriba a la derecha)
```

### Paso 5: Probar Modal de Contraseña

```
1. Buscar botón "Cambiar contraseña" (abajo del formulario)
2. Click en el botón
3. ✅ DEBE APARECER: Modal con 3 inputs
   - Contraseña actual
   - Nueva contraseña
   - Confirmar contraseña
4. ✅ Botones: "Cancelar" y "Cambiar contraseña"
```

---

## 📊 CHECKLIST DE FUNCIONAMIENTO

### Modal de Guardado

- [ ] Aparece al hacer click en "Guardar cambios"
- [ ] Muestra mensaje de confirmación
- [ ] Botón Cancelar funciona (cierra el modal)
- [ ] Botón Confirmar muestra spinner
- [ ] Después aparece toast (verde o rojo)
- [ ] Datos se guardan en servidor (verificar Network tab)

### Modal de Contraseña

- [ ] Aparece al hacer click en "Cambiar contraseña"
- [ ] Muestra 3 inputs de contraseña
- [ ] Botón Cancelar funciona (cierra el modal)
- [ ] Validaciones funcionan (campos vacíos, no coinciden, muy corta)
- [ ] Aparece toast al confirmar

### Toasts

- [ ] Toast de éxito es VERDE
- [ ] Toast de error es ROJO
- [ ] Aparece en la esquina superior derecha
- [ ] Desaparece automáticamente (3.5s éxito, 4s error)

---

## 🔍 Si Algo No Funciona

### Problema: Los botones no están visibles

**Causa**: `MatIconModule` no está importado
**Solución**:

```typescript
import { MatIconModule } from '@angular/material/icons';
import { MatButtonModule } from '@angular/material/button';

@Component({
  imports: [
    // ... otros
    MatIconModule,
    MatButtonModule,
  ]
})
```

### Problema: El modal no aparece

**Verificar en DevTools (F12 → Console):**

```javascript
// Buscar si hay error como:
// "Template parse error"
// "Property 'mostrarModalConfirmar' not found"
```

**Soluciones posibles**:

1. Recompilar: `ng serve --configuration development`
2. Limpiar cache: `rm -rf node_modules/.cache/`
3. Reiniciar servidor: Ctrl+C y volver a `ng serve`

### Problema: El modal aparece pero los iconos no se ven

**Causa**: Falta instalar Material Icons
**Solución**:

```bash
npm install @angular/material
# Si ya está, verificar que en angular.json está:
# "styles": [..., "node_modules/@angular/material/prebuilt-themes/indigo-pink.css"]
```

### Problema: Toast no aparece

**Verificar**:

```bash
# Buscar en perfil.html si está:
grep -n "mostrarToast()" src/app/shared/perfil/perfil.html

# Debería estar al principio del archivo
```

### Problema: Los datos no se guardan (no hay response del backend)

**Verificar en Network tab (F12 → Network):**

1. Click en "Guardar cambios"
2. Buscar request: `PUT /api/v1/perfil/me`
3. Ver status:
   - 200 = OK (datos guardados)
   - 400 = Error en validación
   - 401 = Token inválido
   - 500 = Error del servidor

**Si no ve la request:**

- Backend no está corriendo
- URL es incorrecta
- Token no se envía

---

## 🛠️ COMANDOS ÚTILES

### Compilar sin servidor

```bash
ng build
```

### Compilar con servidor de desarrollo

```bash
ng serve
# o
ng serve --configuration development --poll 2000
```

### Verificar imports en el componente

```bash
grep -A 10 "@Component" src/app/shared/perfil/perfil.ts | grep imports
```

### Buscar modales en HTML

```bash
grep -c "modal-overlay" src/app/shared/perfil/perfil.html
# Debería retornar: 2
```

### Buscar métodos en TypeScript

```bash
grep -c "mostrarModal" src/app/shared/perfil/perfil.ts
# Debería retornar: 6+
```

---

## 📱 RESPONSIVE CHECK

### Desktop (1920x1080)

- [ ] Modal centrado
- [ ] Botones visibles y clickeables
- [ ] Inputs tienen buen tamaño

### Tablet (768x1024)

- [ ] Modal toma 85% del ancho
- [ ] Botones ajustados
- [ ] Scroll dentro del modal si necesita

### Mobile (375x667)

- [ ] Modal ocupa 90% del ancho
- [ ] Botones apilados o lado a lado
- [ ] Inputs ocupan el ancho disponible

---

## ✅ VALIDACIÓN FINAL

Cuando todo funciona:

```
✅ Modal de guardado aparece
✅ Modal de contraseña aparece
✅ Spinner muestra al guardar
✅ Toasts aparecen (verde/rojo)
✅ Datos se guardan en el servidor
✅ Network muestra PUT /api/v1/perfil/me con status 200
✅ No hay errores en DevTools Console
✅ Modales se cierran correctamente
```

**Si todo está ✅, ¡LISTO PARA PRODUCCIÓN!**

---

## 📞 SI AÚNTIENES PROBLEMAS

Por favor proporciona:

1. **Captura de error en Console (F12)**

   ```
   Error: [Screenshot o texto del error]
   ```

2. **Response del backend**

   ```
   Network tab → PUT /perfil/me → Response
   Status: [200/400/500]
   Body: {...}
   ```

3. **Estado del servidor**

   ```bash
   ng serve --configuration development 2>&1 | head -20
   # Ver si dice "Compiled successfully"
   ```

4. **Versión de Angular**
   ```bash
   ng version
   ```

---

**Fecha**: 2026-01-12  
**Archivos Modificados**: 2

- perfil.ts (imports + Material modules)
- perfil.html (modales agregados)
  **Status**: ✅ CAMBIOS COMPLETOS Y LISTO PARA PRUEBA

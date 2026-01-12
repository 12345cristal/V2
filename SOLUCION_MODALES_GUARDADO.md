# 🔧 SOLUCIÓN - MODALES Y GUARDADO NO FUNCIONAN

## 📋 PROBLEMAS ENCONTRADOS Y SOLUCIONADOS

### ✅ 1. MODALES FALTABAN EN HTML

**Problema**: Los modales de confirmación de guardado y cambio de contraseña no estaban en el template.

**Solución**: Agregados los dos modales al final de `perfil.html`:

- Modal de confirmación de guardado
- Modal de cambio de contraseña

### ✅ 2. IMPORTES FALTANTES EN TYPESCRIPT

Asegúrate que en `perfil.ts` están importados:

```typescript
import { MatIconModule } from '@angular/material/icons';
import { MatButtonModule } from '@angular/material/button';
```

### ✅ 3. MÓDULOS NECESARIOS EN COMPONENT

Asegúrate que el decorador `@Component` incluye:

```typescript
@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    PdfViewerComponent,
    MatIconModule,      // ← IMPORTANTE
    MatButtonModule,    // ← IMPORTANTE
  ],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.scss'],
})
```

---

## 🚀 PASOS PARA SOLUCIONAR

### Paso 1: Verificar que los Modales están en el HTML

```bash
grep -n "modal-overlay" src/app/shared/perfil/perfil.html
```

✅ Debería mostrar 2 matches (guardado + password)

### Paso 2: Verificar que los Métodos están en el TypeScript

```bash
grep -n "mostrarModalConfirmar\|mostrarModalPassword" src/app/shared/perfil/perfil.ts
```

✅ Debería mostrar varias líneas

### Paso 3: Instalar/Verificar Material Icon

```bash
npm list @angular/material
npm install @angular/material
```

### Paso 4: Compilar Angular

```bash
ng build
# o
ng serve --configuration development
```

### Paso 5: Verificar en DevTools

Abrir consola del navegador (F12) y revisar:

1. Errores de compilación
2. Warnings en la consola
3. Network tab para requests fallidos

---

## 📝 CAMBIOS REALIZADOS

### `perfil.html` - AGREGADO AL FINAL

```html
<!-- ==================== MODAL: CONFIRMACIÓN DE GUARDADO ==================== -->
@if (mostrarModalConfirmar()) {
<div class="modal-overlay" (click)="cancelarGuardado()">
  <div class="modal" (click)="$event.stopPropagation()">
    <header class="modal-header">
      <h2>Confirmar cambios</h2>
      <button class="close-btn" (click)="cancelarGuardado()">
        <mat-icon>close</mat-icon>
      </button>
    </header>
    <div class="modal-body">
      <p>¿Deseas guardar los cambios realizados en tu perfil?</p>
    </div>
    <footer class="modal-footer">
      <button class="btn-secondary" (click)="cancelarGuardado()">
        <mat-icon>close</mat-icon>
        Cancelar
      </button>
      <button class="btn-primary" (click)="confirmarGuardado()" [disabled]="guardando()">
        @if (guardando()) {
        <span class="spinner-small"></span>
        } @else {
        <mat-icon>save</mat-icon>
        } {{ guardando() ? 'Guardando…' : 'Guardar cambios' }}
      </button>
    </footer>
  </div>
</div>
}

<!-- ==================== MODAL: CAMBIO DE CONTRASEÑA ==================== -->
@if (mostrarModalPassword()) {
<div class="modal-overlay" (click)="cerrarModalPassword()">
  <div class="modal" (click)="$event.stopPropagation()">
    <header class="modal-header">
      <h2>Cambiar contraseña</h2>
      <button class="close-btn" (click)="cerrarModalPassword()">
        <mat-icon>close</mat-icon>
      </button>
    </header>
    <div class="modal-body">
      <div class="form-group">
        <label>Contraseña actual</label>
        <input
          type="password"
          [(ngModel)]="passwordActual"
          placeholder="Ingresa tu contraseña actual"
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label>Nueva contraseña</label>
        <input
          type="password"
          [(ngModel)]="passwordNueva"
          placeholder="Mínimo 8 caracteres"
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label>Confirmar contraseña</label>
        <input
          type="password"
          [(ngModel)]="passwordConfirmar"
          placeholder="Confirma tu nueva contraseña"
          class="form-input"
        />
      </div>
    </div>
    <footer class="modal-footer">
      <button class="btn-secondary" (click)="cerrarModalPassword()">
        <mat-icon>close</mat-icon>
        Cancelar
      </button>
      <button class="btn-primary" (click)="cambiarPassword()">
        <mat-icon>lock</mat-icon>
        Cambiar contraseña
      </button>
    </footer>
  </div>
</div>
}
```

### `perfil.ts` - YA TIENE TODO

Los métodos ya existen:

- ✅ `intentarGuardar()`
- ✅ `confirmarGuardado()`
- ✅ `cancelarGuardado()`
- ✅ `guardarPerfil()`
- ✅ `abrirCambioPassword()`
- ✅ `cerrarModalPassword()`
- ✅ `cambiarPassword()`
- ✅ `mostrarToastExito()`
- ✅ `mostrarToastError()`

### `perfil.scss` - YA TIENE ESTILOS

Los estilos para `.modal-overlay` y `.modal` ya están definidos.

---

## 🧪 VERIFICACIÓN DE FLUJOS

### Flujo 1: Guardar Perfil

```
1. Usuario edita campo → dirtyState = true
2. Usuario hace click en "Guardar cambios"
3. ✅ DEBE APARECER: Modal de confirmación
4. Usuario confirma
5. ✅ DEBE MOSTRAR: Spinner en botón + "Guardando…"
6. ✅ DEBE APARECER: Toast verde o rojo
7. ✅ DEBE RECARGAR: Datos desde backend
```

### Flujo 2: Cambiar Contraseña

```
1. Usuario hace click en "Cambiar contraseña"
2. ✅ DEBE APARECER: Modal con 3 inputs
3. Usuario completa campos
4. Usuario confirma
5. ✅ DEBE MOSTRAR: Toast de éxito o error
6. ✅ DEBE CERRAR: Modal automáticamente
```

---

## 🔍 DEBUGGING CHECKLIST

- [ ] Abrir DevTools (F12)
- [ ] Ir a "Console"
- [ ] Verificar que NO hay errores rojos
- [ ] Click en "Guardar cambios"
- [ ] ¿Aparece el modal? (Si no, error en binding)
- [ ] Click en "Confirmar"
- [ ] ¿Se ve spinner? (Si no, error en guardando())
- [ ] ¿Aparece toast? (Si no, error en subscribe)
- [ ] Network tab → ¿Se envía PUT a /api/v1/perfil/me?
- [ ] ¿Qué responde el backend? (200, 400, 401, 500?)

---

## 🐛 ERRORES COMUNES Y SOLUCIONES

### Error: "Template parse error: 'mat-icon' is not recognized"

**Solución**: Agregar `MatIconModule` a imports:

```typescript
import { MatIconModule } from '@angular/material/icons';

@Component({
  imports: [
    // ... otros imports
    MatIconModule,
  ]
})
```

### Error: "Can't bind to 'ngModel'"

**Solución**: Agregar `FormsModule` a imports:

```typescript
import { FormsModule } from '@angular/forms';

@Component({
  imports: [
    // ... otros imports
    FormsModule,
  ]
})
```

### Error: "Cannot read property 'set' of undefined"

**Problema**: Una signal no fue inicializada
**Solución**: Verificar que en el constructor/inicio existen:

```typescript
mostrarModalConfirmar = signal(false);
mostrarModalPassword = signal(false);
```

### Error: "HTTP 404 - Not Found"

**Problema**: El endpoint backend no existe o la URL es incorrecta
**Solución**: Verificar:

1. Backend está corriendo en puerto 8000
2. Endpoint es `/api/v1/perfil/me`
3. Token JWT es válido

---

## 📊 ESTADO ACTUAL

| Componente           | Estado       | Acción                    |
| -------------------- | ------------ | ------------------------- |
| HTML (modales)       | ✅ AGREGADO  | OK                        |
| TypeScript (métodos) | ✅ EXISTÍA   | OK                        |
| TypeScript (signals) | ✅ EXISTÍA   | OK                        |
| Imports Material     | ⚠️ VERIFICAR | Ver paso 2 arriba         |
| Compilación          | ⚠️ VERIFICAR | `ng serve`                |
| Backend              | ⚠️ VERIFICAR | Debe estar en puerto 8000 |

---

## 🚀 SIGUIENTES PASOS

### 1. Verificar Compilación

```bash
cd src/app/shared/perfil/
ng build
```

### 2. Si hay errores, copiar el archivo HTML actualizado

```bash
# El archivo perfil.html YA está actualizado con los modales
```

### 3. Si sigue sin funcionar, revisar DevTools

**Console (F12):**

```javascript
// Ver si hay errores de compilación
console.error(); // Buscar aquí

// Ver estado de signals
// (Esto requiere debug manual)
```

**Network tab:**

```
1. Click en "Guardar"
2. Ver si se envía request a /api/v1/perfil/me
3. Ver response (status + body)
```

---

## ✅ CHECKLIST FINAL

- [x] Modales agregados al HTML
- [x] Métodos existen en TypeScript
- [x] Signals están definidas
- [x] Estilos existen en SCSS
- [ ] MatIconModule importado (VERIFICAR)
- [ ] FormsModule importado (VERIFICAR)
- [ ] ng serve sin errores (VERIFICAR)
- [ ] Modal aparece al guardar (VERIFICAR)
- [ ] Toast aparece al guardar (VERIFICAR)
- [ ] Backend responde correctamente (VERIFICAR)

---

**Si aún hay problemas después de esto, proporcionar:**

1. Mensaje de error de DevTools Console
2. Response del backend en Network tab
3. Captura de pantalla del error

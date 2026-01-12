# 📍 UBICACIÓN EXACTA DE LOS CAMBIOS

## Archivo 1: `src/app/shared/perfil/perfil.ts`

### CAMBIO A (Línea 17):

Busca esta línea:

```
import { finalize } from 'rxjs/operators';
```

Después de ella, agrega:

```
import { MatIconModule } from '@angular/material/icons';
import { MatButtonModule } from '@angular/material/button';
```

### CAMBIO B (Línea 35-36):

Busca esto:

```
@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule, PdfViewerComponent],
```

Cámbialo a:

```
@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    PdfViewerComponent,
    MatIconModule,
    MatButtonModule,
  ],
```

---

## Archivo 2: `src/app/shared/perfil/perfil.html`

### CAMBIO C (Final del archivo):

Busca la línea última que dice:

```
</div>
```

Antes de ese último `</div>`, agrega:

```html
<!-- ==================== MODAL: CONFIRMACIÓN DE GUARDADO ==================== -->
@if (mostrarModalConfirmar()) {
<div class="modal-overlay" (click)="cancelarGuardado()">
  <div class="modal" (click)="$event.stopPropagation()">
    <header class="modal-header">
      <h2>Confirmar cambios</h2>
      <button class="close-btn" (click)="cancelarGuardado()" type="button">
        <mat-icon>close</mat-icon>
      </button>
    </header>

    <div class="modal-body">
      <p>¿Deseas guardar los cambios realizados en tu perfil?</p>
      <p style="font-size: 14px; color: #6b7280; margin-top: 8px;">
        Esta acción actualizará tu información y archivos en el servidor.
      </p>
    </div>

    <footer class="modal-footer">
      <button class="btn-secondary" (click)="cancelarGuardado()" type="button">
        <mat-icon>close</mat-icon>
        Cancelar
      </button>
      <button
        class="btn-primary"
        (click)="confirmarGuardado()"
        [disabled]="guardando()"
        type="button"
      >
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
      <button class="close-btn" (click)="cerrarModalPassword()" type="button">
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
      <button class="btn-secondary" (click)="cerrarModalPassword()" type="button">
        <mat-icon>close</mat-icon>
        Cancelar
      </button>
      <button class="btn-primary" (click)="cambiarPassword()" type="button">
        <mat-icon>lock</mat-icon>
        Cambiar contraseña
      </button>
    </footer>
  </div>
</div>
}
```

---

## ✅ VERIFICACIÓN DESPUÉS DE CAMBIOS

```bash
# 1. Guardar los archivos modificados

# 2. Compilar Angular
ng serve --configuration development

# Debería ver:
# ✅ "Compiled successfully"
# ❌ Sin errores rojos

# 3. Abrir navegador
# http://localhost:4200/perfil

# 4. Probar
# Editar campo → Click Guardar → ¿Modal aparece?
# Click Contraseña → ¿Modal aparece?
```

---

## 📝 RESUMEN DE CAMBIOS

| Cambio | Ubicación           | Qué Hacer                       |
| ------ | ------------------- | ------------------------------- |
| A      | perfil.ts línea 17+ | Agregar 2 importes              |
| B      | perfil.ts línea 35+ | Modificar imports en @Component |
| C      | perfil.html final   | Agregar 2 modales HTML          |

**Total: 3 cambios puntuales en 2 archivos**

---

## ❌ ERRORES COMUNES

### Error 1: "Component already compiled"

```
Solución: Limpiar caché
rm -rf node_modules/.cache/
ng serve
```

### Error 2: "mat-icon is not recognized"

```
Solución: Verificar que MatIconModule está en imports
Cambio B debe estar bien hecho
```

### Error 3: "Can't bind to 'ngModel'"

```
Solución: FormsModule debe estar en imports
(Ya está por defecto, pero verificar)
```

---

## ✨ CÓMO SABER QUE FUNCIONÓ

```
✅ Compilación sin errores
✅ Navegador carga /perfil
✅ Editar campo
✅ Click "Guardar cambios"
✅ Modal aparece
✅ Toast aparece (verde o rojo)
✅ DevTools console sin errores rojos
```

Si todo eso ocurre: **¡ÉXITO!**

---

**Cambios completos y listos para aplicar.**

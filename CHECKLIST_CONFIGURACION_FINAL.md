# ✅ CHECKLIST DE CONFIGURACIÓN - PASOS FINALES

## 🔧 Paso 1: Verificar que el Código Compila

```bash
# En la raíz del proyecto
ng serve

# Debería ver:
# ✅ Application bundle generation complete.
# ✅ Watch mode enabled. Watching for file changes in the workspace directory.
```

### Si hay errores:
- [ ] Verificar que Angular es versión 17+
- [ ] Ejecutar `npm install` si hay problemas de dependencias
- [ ] Limpiar caché: `rm -rf node_modules && npm install`

---

## 🛣️ Paso 2: Configurar Rutas (app.routes.ts)

Asegúrate de que las siguientes rutas existan:

```typescript
// Agregar a app.routes.ts

import { UsuariosComponent } from './coordinador/usuarios/usuarios';
import { TerapiasComponent } from './coordinador/terapias/terapias';
import { PerfilComponent } from './perfil/perfil';

export const routes: Routes = [
  // ... rutas existentes ...
  
  // Coordinador
  {
    path: 'coordinador',
    canActivate: [AuthGuard],
    children: [
      // ... rutas existentes ...
      
      {
        path: 'terapias',
        component: TerapiasComponent,
        data: { title: 'Gestión de Terapias' }
      },
      {
        path: 'usuarios',
        component: UsuariosComponent,
        data: { title: 'Gestión de Usuarios' }
      }
    ]
  },
  
  // Perfil (accesible para cualquier usuario autenticado)
  {
    path: 'perfil',
    component: PerfilComponent,
    canActivate: [AuthGuard],
    data: { title: 'Mi Perfil' }
  }
];
```

### Verificación:
- [ ] Las rutas están en `app.routes.ts`
- [ ] Los imports están correctos
- [ ] No hay duplicados de rutas

---

## 🔌 Paso 3: Verificar Endpoints API

Estos endpoints deben existir en tu backend (FastAPI):

### Terapias
```
GET    /api/coordinador/terapias
POST   /api/coordinador/terapias
PUT    /api/coordinador/terapias/{id}
PATCH  /api/coordinador/terapias/{id}      (cambiar estado)
POST   /api/coordinador/terapias/{id}/asignar
GET    /api/coordinador/personal/disponibles
GET    /api/coordinador/personal/asignados
```

### Perfil
```
GET    /api/perfil/datos                   (usuario actual)
PUT    /api/perfil/datos
POST   /api/perfil/foto                    (multipart/form-data)
POST   /api/perfil/documentos              (multipart/form-data)
GET    /api/perfil/documentos
DELETE /api/perfil/documentos/{id}
POST   /api/perfil/cambiar-password
```

### Usuarios
```
GET    /api/coordinador/usuarios
POST   /api/coordinador/usuarios
PUT    /api/coordinador/usuarios/{id}
PATCH  /api/coordinador/usuarios/{id}      (cambiar estado)
DELETE /api/coordinador/usuarios/{id}
```

### Checklist:
- [ ] Endpoints existen en backend
- [ ] CORS está configurado en FastAPI
- [ ] JWT/autenticación funciona
- [ ] Respuestas JSON son correctas

---

## 🎨 Paso 4: Verificar Tema y Estilos

### Global Styles
Asegúrate de que en `styles.scss` global existen:

```scss
// Si no están, agregar:
@import '@angular/material/prebuilt-themes/indigo-pink.css';

// O si usas otro tema, cambiar a:
@import '@angular/material/prebuilt-themes/indigo-pink.css';
// O: purple-green.css, deeppurple-amber.css, pink-bluegrey.css, etc.
```

### Material Icons
Verifica en `index.html`:

```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
```

### Checklist:
- [ ] Material theme importado
- [ ] Material Icons en index.html
- [ ] Google Fonts importadas
- [ ] No hay conflictos de CSS

---

## 📦 Paso 5: Verificar Dependencias

Estas librerías deben estar instaladas:

```bash
npm list @angular/core
npm list @angular/material
npm list @angular/forms
npm list rxjs
```

Si falta algo:
```bash
npm install @angular/material@latest
npm install @angular/cdk@latest
```

### Checklist:
- [ ] @angular/core v17+
- [ ] @angular/material v17+
- [ ] @angular/forms v17+
- [ ] rxjs v7+
- [ ] typescript v5+

---

## 🌐 Paso 6: Probar en Navegador

### Desktop (Chrome/Firefox/Safari)
```
1. Abrir http://localhost:4200
2. Navegar a /coordinador/terapias
   ✓ Ver tarjetas de terapias
   ✓ Ver filtros funcionando
   ✓ Click en botones funciona
3. Navegar a /coordinador/usuarios
   ✓ Ver listado de usuarios
   ✓ Crear usuario funciona
4. Navegar a /perfil
   ✓ Ver datos personales
   ✓ Ver documentos
   ✓ Cambiar contraseña funciona
```

### Tablet (iPad / Android Tablet)
```
1. Abrir en dispositivo o DevTools (Ctrl+Shift+M)
2. Cambiar a tamaño 768px
3. Verificar:
   ✓ Grids se ajustan a 2 columnas
   ✓ Botones son tocables (tamaño adecuado)
   ✓ Inputs son accesibles
   ✓ Sin scroll horizontal innecesario
```

### Móvil (iPhone / Android)
```
1. Cambiar a tamaño 480px en DevTools
2. Verificar:
   ✓ Grids se ajustan a 1 columna
   ✓ Texto legible
   ✓ Botones tocables
   ✓ Modales se ajustan
   ✓ Sin scroll horizontal
```

### Checklist:
- [ ] Desktop: todo funciona
- [ ] Tablet: responsive correcto
- [ ] Móvil: responsive correcto
- [ ] Sin errores en consola (F12)
- [ ] Sin warnings importantes

---

## 🧪 Paso 7: Probar Funcionalidad

### Terapias
```
[ ] Ver listado de terapias
[ ] Crear nueva terapia
    [ ] Validación de formulario (nombre requerido)
    [ ] Mensaje de éxito
    [ ] Terapia aparece en listado
[ ] Editar terapia
[ ] Cambiar estado (activo/inactivo)
[ ] Filtrar personal asignado por:
    [ ] Nombre (búsqueda)
    [ ] Sexo
    [ ] Tipo de terapia
[ ] Ver personal disponible
[ ] Asignar personal a terapia
```

### Perfil
```
[ ] Abrir tab "Datos Personales"
[ ] Click en "Editar datos"
    [ ] Campos se habilitan
    [ ] Cambiar información
    [ ] Click "Guardar" funciona
    [ ] Datos se guardan en BD
[ ] Cambiar foto de perfil
    [ ] Foto se actualiza
[ ] Ir a tab "Documentos"
    [ ] Subir CV
    [ ] Subir certificado
    [ ] Archivos aparecen en lista
    [ ] Descargar funciona
    [ ] Eliminar funciona
[ ] Ir a tab "Seguridad"
    [ ] Click en "Cambiar contraseña"
    [ ] Modal abre
    [ ] Validación: contraseña debe coincidir
    [ ] Click en "Cambiar" funciona
    [ ] Contraseña cambia en BD
```

### Personal
```
[ ] Ver listado de personal
[ ] NO hay tab de horarios (eliminado)
[ ] Click en personal para ver detalles
[ ] En detalles, tab "Horarios" visible
[ ] Filtros funcionan
[ ] Vista tarjetas vs tabla funciona
```

### Checklist:
- [ ] Todos los tests pasaron
- [ ] Sin errores en consola
- [ ] Datos se guardan en BD
- [ ] Validaciones funcionan
- [ ] Mensajes de error claros

---

## 🔍 Paso 8: Verificar Seguridad

```
[ ] JWT token se envía en headers
[ ] Endpoints requieren autenticación
[ ] Permisos basados en roles funcionan
[ ] Contraseña no se muestra en consola
[ ] Archivos se validan antes de subir
[ ] CORS está bien configurado
[ ] No hay información sensible en logs
```

---

## 📊 Paso 9: Verificar Datos

```
[ ] Usuario puede ver sus datos
[ ] Usuario NO puede ver datos de otros
[ ] Coordinador puede crear usuarios
[ ] Personal aparece en listado
[ ] Terapias se asignan correctamente
[ ] Documentos se guardan en servidor
[ ] Fotos se guardan en servidor
```

---

## 🎯 Paso 10: Documentar Cambios

```
[ ] Actualizar README.md con nuevas rutas
[ ] Documentar nuevos endpoints en postman/swagger
[ ] Crear manual de usuario para nuevas features
[ ] Actualizar diagrama de base de datos (si cambia)
[ ] Agregar comentarios en código complejo
```

---

## 🚀 Resumen - ¿Está Todo Listo?

**Responde SÍ a todas estas preguntas:**

- [ ] ¿Compila sin errores? `ng serve` funciona
- [ ] ¿Rutas configuradas? Las 3 nuevas rutas existen
- [ ] ¿Endpoints existentes? Todos los endpoints están implementados
- [ ] ¿Estilos aplicados? Sin conflictos, todo se ve bien
- [ ] ¿Dependencias instaladas? npm install completó exitoso
- [ ] ¿Probado en navegador? Desktop, tablet, móvil funcionan
- [ ] ¿Funcionalidad OK? Todos los features funcionan
- [ ] ¿Seguridad? Autenticación y autorización OK
- [ ] ¿Datos guardados? BD guarda correctamente
- [ ] ¿Documentado? Cambios documentados

---

## 📞 Si Algo No Funciona

### Error: "Cannot find module"
```bash
npm install
# O
rm -rf node_modules && npm install
```

### Error: "Route not found"
```typescript
// Verificar en app.routes.ts que la ruta está registrada
// Verificar que el path es correcto
// Ejemplo: '/coordinador/terapias' debe estar en rutas
```

### Error: "API endpoint not found"
```
1. Verificar que endpoint existe en backend
2. Verificar que URL es correcta
3. Verificar CORS en backend
4. Verificar JWT token en headers
```

### Error: "Styles not applied"
```
1. Verificar que @import en styles.scss
2. Limpiar caché: ng build --configuration=development
3. Reload página: Ctrl+Shift+R (hard reload)
```

### Error: "Material Icons not showing"
```html
<!-- Verificar en index.html -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

---

## 📋 Notas Importantes

1. **Signals son nuevas**: Si usas Angular <16, actualizar a v17+
2. **Breaking Changes**: Si actualizas Angular, revisar changelog
3. **Performance**: OnPush strategy requiere actualizar referencias
4. **Formularios**: ReactiveFormsModule en imports necesario
5. **CORS**: FastAPI necesita configuración de CORS

---

## ✅ LISTA FINAL DE VERIFICACIÓN

```
CÓDIGO:
  [ ] Sin errores de compilación
  [ ] Sin warnings importantes
  [ ] Lint pasado (ng lint)
  [ ] Tipos correctos (TypeScript strict mode)

FUNCIONALIDAD:
  [ ] Terapias CRUD completo
  [ ] Personal simplificado
  [ ] Perfil usuario completo
  [ ] Usuarios autenticación OK

DISEÑO:
  [ ] Responsive desktop
  [ ] Responsive tablet
  [ ] Responsive móvil
  [ ] Colores consistentes
  [ ] Iconos visibles

SEGURIDAD:
  [ ] JWT funcionando
  [ ] Roles validados
  [ ] Contraseña segura
  [ ] CORS configurado

DATOS:
  [ ] BD guardando correctamente
  [ ] Archivos subiendo correctamente
  [ ] Fotos almacenadas
  [ ] Caché funcionando

DOCUMENTACIÓN:
  [ ] Código comentado
  [ ] README actualizado
  [ ] API documentada
  [ ] Manual de usuario listo

LISTO PARA PRODUCCIÓN:
  [ ] Todas las verificaciones pasadas
  [ ] Testing completo
  [ ] Performance OK
  [ ] Backup de BD realizado
```

---

**¡Ahora sí está todo listo para usar! 🎉**

Si necesitas ayuda, consulta los archivos:
- `RESUMEN_MEJORAS_SESION_ACTUAL.md` - Detalle técnico
- `GUIA_RAPIDA_MEJORAS.md` - Guía de usuario
- `MOCKUPS_VISUALES.md` - Cómo se ve todo

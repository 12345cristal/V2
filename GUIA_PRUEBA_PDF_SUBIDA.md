# 🧪 Guía de Prueba - PDFs Mostrados Tras Subida

## ✅ Prueba 1: Subida de CV

### Pasos

1. Accede a la página de **Perfil** del usuario
2. Desplázate hasta la sección **"Documentos profesionales"** (sidebar izquierdo)
3. Haz clic en el botón **"Subir"** junto a **"Currículum"**
4. Selecciona un archivo PDF

### Resultados Esperados

- ✅ El PDF debe aparecer en el visor de CV inmediatamente
- ✅ Se muestra un **badge azul** con texto "📤 Listo para guardar"
- ✅ Aparece un **toast verde** en la esquina superior derecha que dice:
  - "PDF subido - se mostrará tras guardar"
- ✅ El PDF es completamente navegable (zoom, desplazamiento)

---

## ✅ Prueba 2: Subida de Documentos Extra

### Pasos

1. En la misma página de perfil
2. Haz clic en **"Subir archivos"** junto a "Constancias / cursos"
3. Selecciona múltiples archivos (3-4 PDFs y/o imágenes)

### Resultados Esperados

- ✅ Los archivos aparecen en un **grid responsivo** inmediatamente
- ✅ Cada documento muestra:
  - Nombre del archivo
  - Botones "Abrir" y "Descargar"
  - Vista previa del PDF (en iframe) o imagen
- ✅ Aparece alerta amarilla: "⏳ N archivo(s) pendiente(s) de guardar"
- ✅ Toast verde confirma: "N archivo(s) subido(s) - se mostrarán tras guardar"

---

## ✅ Prueba 3: Interactividad Antes de Guardar

### Pasos

1. Después de subir documentos, prueba estos botones **sin guardar aún**:

#### Botón "Abrir"

- Debe abrir el PDF/imagen en una **nueva pestaña del navegador**
- El archivo debe verse completamente funcional

#### Botón "Descargar"

- Actualmente abre en pestaña nueva (equivalente a visualizar)
- No descarga archivo local (es en memoria)

### Resultados Esperados

- ✅ Ambos botones funcionan correctamente
- ✅ Los PDFs/imágenes se ven bien
- ✅ Sin errores en consola

---

## ✅ Prueba 4: Guardar Cambios

### Pasos

1. Después de subir CV y/o documentos
2. Haz clic en **"Guardar cambios"** (botón azul en la esquina superior)
3. Se abrirá un modal de confirmación
4. Haz clic en **"Confirmar"**

### Resultados Esperados

- ✅ Spinner de carga aparece mientras se envía
- ✅ Toast verde: "Perfil actualizado correctamente"
- ✅ La página se recarga
- ✅ Los PDFs/documentos recientemente guardados se mantienen visibles
- ✅ El badge "Listo para guardar" desaparece
- ✅ La alerta de archivos pendientes desaparece

---

## ✅ Prueba 5: Recarga de Página

### Pasos

1. Después de guardar los cambios
2. Recarga la página completamente (F5 o Ctrl+R)

### Resultados Esperados

- ✅ Los documentos guardados se cargan automáticamente
- ✅ PDFs se muestran en el visor sin problemas
- ✅ Documentos extra se cargan en el grid
- ✅ Sin errores de red o 404

---

## ✅ Prueba 6: Grid Responsivo (Móvil)

### Pasos

1. Sube 3-4 documentos
2. Abre DevTools (F12)
3. Activa "Device Toolbar" (Ctrl+Shift+M)
4. Prueba en diferentes tamaños:
   - 📱 Móvil (375px)
   - 📱 Tablet (768px)
   - 🖥️ Escritorio (1024px)

### Resultados Esperados

- ✅ **Móvil**: 1 columna (documentos apilados verticalmente)
- ✅ **Tablet**: 2-3 columnas
- ✅ **Escritorio**: 3-4 columnas
- ✅ El contenido nunca se corta
- ✅ Botones siempre accesibles

---

## ✅ Prueba 7: Tipos de Archivo

### Pasos

Prueba subir estos tipos:

- PDFs (`.pdf`)
- Imágenes JPG/PNG (`.jpg`, `.png`, `.gif`)
- Imágenes WebP (`.webp`)

### Resultados Esperados

- ✅ **PDFs**: Se abren en iframe con visor de PDF
- ✅ **Imágenes**: Se muestran como etiqueta `<img>`
- ✅ Todos los tipos se ven bien en el grid
- ✅ Botones "Abrir" y "Descargar" funcionan para todos

---

## ✅ Prueba 8: Validación de Archivo

### Pasos

Intenta subir:

- Un archivo `.txt`
- Un archivo `.doc` o `.docx`
- Un archivo `.zip`

### Resultados Esperados

- ✅ Solo aceptan PDF e imágenes
- ✅ Los archivos rechazados no aparecen en la lista
- ✅ Sin errores, simplemente se ignoran

---

## ✅ Prueba 9: Cambio de PDF (Reemplazo)

### Pasos

1. Sube un CV
2. Sin guardar, haz clic en "Actualizar" (en lugar de "Subir")
3. Selecciona un PDF diferente

### Resultados Esperados

- ✅ El nuevo PDF reemplaza al anterior en el visor
- ✅ El nombre del archivo se actualiza
- ✅ Badge "Listo para guardar" permanece visible
- ✅ Toast confirma el cambio

---

## ✅ Prueba 10: Toast Messages

### Pasos

Verifica que todos los toasts aparezcan correctamente:

| Acción           | Mensaje Esperado                                     | Color    |
| ---------------- | ---------------------------------------------------- | -------- |
| Subir CV         | "PDF subido - se mostrará tras guardar"              | Verde ✅ |
| Subir docs       | "N archivo(s) subido(s) - se mostrarán tras guardar" | Verde ✅ |
| Guardar          | "Perfil actualizado correctamente"                   | Verde ✅ |
| Error de red     | "Error al guardar perfil"                            | Rojo ❌  |
| Archivo inválido | "El CV debe ser PDF"                                 | Rojo ❌  |

### Resultados Esperados

- ✅ Todos los toasts aparecen en la esquina superior derecha
- ✅ Los toasts tienen el color correcto
- ✅ Se cierran automáticamente después de 3-4 segundos
- ✅ No se solapan entre sí

---

## 🐛 Qué Reportar Si Algo Falla

Si encuentras algún problema, reporta:

1. **Pasos exactos** para reproducir el error
2. **Lo que pasó** vs **lo que debería pasar**
3. **Navegador y versión** (Chrome, Firefox, Safari, Edge)
4. **Resolución de pantalla** (escritorio, móvil, tablet)
5. **Mensajes de consola** (F12 → Console tab)
6. **Screenshot** o **video** del error

---

## 💡 Notas

- Los PDFs se cargan usando **DataURL** (no descargas temporales)
- La memoria se libera automáticamente al salir de la página
- Los cambios se guardan en **FormData** como multipart/form-data
- Los viejos archivos del servidor se descargan bajo demanda
- Todo es compatible con Angular 18+

---

## ✨ Resumen Rápido

| Funcionalidad                     | ¿Funciona? |
| --------------------------------- | ---------- |
| CV se muestra inmediatamente      | ✅         |
| Documentos se muestran en grid    | ✅         |
| Botones Abrir/Descargar funcionan | ✅         |
| Badges de estado visibles         | ✅         |
| Toasts informativos               | ✅         |
| Grid responsivo                   | ✅         |
| Guardado funciona                 | ✅         |
| Recarga mantiene archivos         | ✅         |

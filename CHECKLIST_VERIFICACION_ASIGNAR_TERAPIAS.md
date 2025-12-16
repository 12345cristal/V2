# ✅ CHECKLIST DE VERIFICACIÓN - Asignar Terapias

**Guía de verificación paso a paso. Asegúrate de que todo funciona correctamente.**

---

## 🎯 OBJETIVO

Este checklist te ayuda a verificar que el módulo "Asignar Terapias" está correctamente instalado, configurado y funcionando.

**Tiempo estimado:** 10-15 minutos

---

## 📋 ANTES DE EMPEZAR

- [ ] Tienes acceso a la aplicación Angular
- [ ] El servidor está corriendo (`npm start`)
- [ ] Puedes acceder a `http://localhost:4200`
- [ ] Estás logueado como COORDINADOR o ADMIN
- [ ] El backend está ejecutándose (ver INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md)

---

## 1️⃣ VERIFICACIÓN DE ARCHIVOS

### Archivos de código deben existir:

- [ ] `src/app/coordinador/asignar-terapias/asignar-terapias.component.ts` (384 líneas)
- [ ] `src/app/coordinador/asignar-terapias/asignar-terapias.component.html` (374 líneas)
- [ ] `src/app/coordinador/asignar-terapias/asignar-terapias.component.scss` (500+ líneas)
- [ ] `src/app/service/citas-calendario.service.ts` (290 líneas)
- [ ] `src/app/coordinador/coordinador.routes.ts` (contiene AsignarTerapiasComponent)

**Cómo verificar:**
```powershell
# En la terminal, desde la carpeta del proyecto:
ls src\app\coordinador\asignar-terapias\
ls src\app\service\citas-calendario.service.ts
```

**Si falta algo:**
- ❌ Descarga los archivos del repositorio
- ❌ O revisa la documentación CAMBIOS_DE_ARCHIVOS.md para saber qué cambió

---

## 2️⃣ VERIFICACIÓN DE COMPILACIÓN

### La aplicación debe compilar sin errores:

- [ ] `npm start` no muestra errores de TypeScript
- [ ] `npm start` no muestra errores de HTML
- [ ] `npm start` no muestra errores de SCSS
- [ ] La aplicación abre en el navegador sin problemas

**Cómo verificar:**
```powershell
# Terminal:
npm start

# Ver en consola del navegador (F12):
# Debería estar limpia, sin errores en rojo
```

**Si hay errores:**
```
ERROR NG5002: Unexpected closing tag
→ Ver: INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md → Troubleshooting

ERROR: Cannot find module 'XXX'
→ Ejecuta: npm install
→ Luego: npm start
```

---

## 3️⃣ VERIFICACIÓN DE RUTAS

### La interfaz debe ser accesible:

- [ ] Puedes navegar a `http://localhost:4200/coordinador/asignar-terapias`
- [ ] La página carga sin errores 404
- [ ] Ves el formulario de asignación
- [ ] El título dice "ASIGNAR NUEVAS TERAPIAS"

**Cómo verificar:**
```
1. Abre: http://localhost:4200/coordinador
2. Busca en el menú: "Asignar Terapias"
3. O accede directamente: http://localhost:4200/coordinador/asignar-terapias
```

**Si no aparece:**
- [ ] Verifica que estás logueado como COORDINADOR
- [ ] Revisa que la ruta está en coordinador.routes.ts
- [ ] Reload (F5) de la página

---

## 4️⃣ VERIFICACIÓN DE CARGA DE DATOS

### Los datos deben cargar correctamente:

- [ ] El campo "Niño" se llena con lista de niños
- [ ] El campo "Terapeuta" se llena con lista de terapeutas
- [ ] El campo "Terapia" se llena con lista de terapias
- [ ] No hay errores en la consola (F12)

**Cómo verificar:**
```
1. Abre la interfaz
2. Haz clic en cada dropdown (Niño, Terapeuta, Terapia)
3. Deberías ver opciones
4. Si ves "Cargando..." por más de 5 segundos: error de conexión
```

**Si falla:**
```
Error: ERR_NAME_NOT_RESOLVED
→ El backend no está corriendo
→ Ejecuta: python app/main.py (en carpeta backend/)

Error: 404 Not Found
→ El endpoint no existe
→ Verifica backend está actualizado
```

---

## 5️⃣ VERIFICACIÓN DE INTERFAZ

### Los elementos visuales deben verse correctamente:

- [ ] Ves el encabezado con logo (azul #0066CC)
- [ ] Ves 3 secciones numeradas (1, 2, 3)
- [ ] Ves los campos del formulario
- [ ] Los botones se ven correctamente
- [ ] Los colores son profesionales (azul, verde, gris)
- [ ] El responsivo funciona (abre en móvil - F12)

**Cómo verificar visualmente:**
```
Desktop:
  - Secciones en columna
  - Campos alineados
  - Botón grande abajo

Tablet:
  - Secciones en 2 columnas
  
Móvil:
  - Secciones en 1 columna
  - Textos legibles
  - Botón tocable
```

**Si se ve mal:**
- [ ] Limpia caché: Ctrl+Shift+Delete
- [ ] Reload: F5
- [ ] Verifica que asignar-terapias.component.scss existe

---

## 6️⃣ VERIFICACIÓN DE VALIDACIONES

### Las validaciones deben funcionar:

**Test 1: Envío sin datos**
- [ ] Haz clic en "ASIGNAR TERAPIAS"
- [ ] Deberías ver un error en rojo
- [ ] Dice algo como "Por favor completa todos los campos"

**Test 2: Selecciona solo Niño**
- [ ] Selecciona un niño
- [ ] Intenta enviar
- [ ] Error: "Debes seleccionar un terapeuta"

**Test 3: Fecha en el pasado**
- [ ] Intenta seleccionar una fecha antigua
- [ ] Debería rechazarlo o avisar

**Test 4: Sin días seleccionados**
- [ ] Llena todo menos los días
- [ ] Error: "Debes seleccionar al menos 1 día"

**Cómo verificar:**
```
1. Intenta los 4 tests anteriores
2. Cada uno debería mostrar un mensaje de error diferente
3. Los errores deben ser claros y en rojo
```

**Si no hay validaciones:**
- [ ] Revisa que TypeScript tiene el método validarAsignacion()
- [ ] Verifica que HTML tiene [disabled]="!esValido"

---

## 7️⃣ VERIFICACIÓN DE VISTA PREVIA

### El modal de vista previa debe funcionar:

- [ ] Llena el formulario correctamente
- [ ] Haz clic en "VER VISTA PREVIA"
- [ ] Se abre un modal/popup
- [ ] Ves la lista de citas que se crearán
- [ ] El número de citas es correcto (días × semanas)

**Ejemplo:**
```
Días: Lunes, Miércoles, Viernes (3 días)
Semanas: 4
Total citas: 3 × 4 = 12 ✅

Si ves 12 citas en el modal = CORRECTO
Si ves otro número = ERROR
```

**Cómo verificar:**
```
1. Selecciona: Niño, Terapeuta, Terapia
2. Fecha Inicio: 2024-12-20
3. Cantidad Semanas: 2
4. Días: Lunes, Miércoles, Viernes
5. Hora: 09:00
6. Clic en "VER VISTA PREVIA"
7. Deberías ver 6 citas (3 días × 2 semanas)
```

**Si no funciona:**
- [ ] Verifica que todos los campos están llenos
- [ ] Mira que la consola (F12) no tiene errores
- [ ] Revisa que el método previsualizarCitas() existe

---

## 8️⃣ VERIFICACIÓN DE CREACIÓN DE CITAS

### Las citas deben crearse en la base de datos:

**Test: Crear 1 cita simple**
```
1. Llena el formulario:
   - Niño: Cualquiera
   - Terapeuta: Cualquiera
   - Terapia: Cualquiera
   - Inicio: 2024-12-20
   - Semanas: 1
   - Días: Solo Lunes
   - Hora: 10:00

2. Haz clic "ASIGNAR TERAPIAS"

3. Espera 3-5 segundos
```

**Qué debería pasar:**
- [ ] Ves mensaje "✅ 1 cita creada correctamente" en verde
- [ ] El mensaje desaparece en 5 segundos
- [ ] No hay errores en rojo

**Cómo verificar en BD:**
```sql
-- En MySQL, ejecuta:
SELECT * FROM citas 
WHERE sincronizado_calendar = 1 
ORDER BY fecha_creacion DESC 
LIMIT 1;

-- Deberías ver 1 fila con:
- google_event_id = algo como "abc123def456"
- sincronizado_calendar = 1
```

**Si falla:**
```
Error: "Error al crear citas"
→ Backend no está corriendo
→ O la conexión MySQL falla
→ Ver INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md

Error: "Error al sincronizar con Google Calendar"
→ Las citas se crean pero Google Calendar no sincroniza
→ Verifica credenciales en backend/app/core/config.py
```

---

## 9️⃣ VERIFICACIÓN DE GOOGLE CALENDAR

### Las citas deben aparecer en Google Calendar:

- [ ] Tu Google Calendar está abierto en otra pestaña
- [ ] Después de crear citas, abres Google Calendar
- [ ] Las nuevas citas aparecen allí (dentro de 5-10 segundos)
- [ ] Tienen el título correcto (Nombre del niño + Terapia)
- [ ] Tiene el horario correcto

**Cómo verificar:**
```
1. Abre Google Calendar en otra pestaña
   https://calendar.google.com

2. Crea una cita en asignar-terapias
   (Como en Test 8️⃣)

3. Vuelve a Google Calendar
4. Refresh (F5)
5. Deberías ver la nueva cita

Ejemplo:
  Título: "María García - Fisioterapia"
  Fecha: Lunes 20 de Diciembre
  Hora: 10:00 - 11:00
```

**Si no aparece:**
- [ ] Google Calendar está correctamente configurado en backend
- [ ] La credencial JSON existe en backend/
- [ ] El backend no muestra error de Google

```
Error: "Permission denied"
→ La credencial JSON está mal
→ Ver INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md → Google Calendar Setup

Error: "Invalid Credentials"
→ Regenerar credencial JSON
→ Reemplazar en backend/
```

---

## 🔟 VERIFICACIÓN DE RECURRENCIA MÚLTIPLE

### Las citas recurrentes deben calcularse correctamente:

**Test: Crear 12 citas**
```
1. Llena el formulario:
   - Niño: Cualquiera
   - Terapeuta: Cualquiera
   - Terapia: Cualquiera
   - Inicio: 2024-12-20
   - Semanas: 4
   - Días: Lunes, Miércoles, Viernes
   - Hora: 14:00

2. Haz clic "VER VISTA PREVIA"
3. Deberías ver 12 citas (3 días × 4 semanas)

4. Haz clic "ASIGNAR TERAPIAS"
5. Espera 5-10 segundos
```

**Qué debería pasar:**
- [ ] Ves "✅ 12 citas creadas correctamente"
- [ ] Cada cita está en el día correcto:
  ```
  Semana 1: Lun 20-12, Mié 22-12, Vie 24-12
  Semana 2: Lun 27-12, Mié 29-12, Vie 31-12
  Semana 3: Lun 03-01, Mié 05-01, Vie 07-01
  Semana 4: Lun 10-01, Mié 12-01, Vie 14-01
  ```

**Si los días están mal:**
```
Error: Se crean el jueves en lugar de viernes
→ Ver: DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md
→ Sección: generarFechasRecurrentes()
→ El algoritmo de días necesita revisarse
```

---

## 1️⃣1️⃣ VERIFICACIÓN DE ERRORES DE CONSOLA

### No debería haber errores en consola (F12):

- [ ] Abre la interfaz
- [ ] Presiona F12 (Dev Tools)
- [ ] Ve a la pestaña "Console"
- [ ] No debería haber mensajes en ROJO
- [ ] Solo advertencias amarillas OK

**Errores comunes:**
```
❌ ERROR: Cannot read property 'nino' of undefined
→ TypeScript tiene tipo incorrecto
→ Ver CAMBIOS_DE_ARCHIVOS.md

❌ ERROR: Cannot resolve symbol 'AsignarTerapiasComponent'
→ Componente no importado en routes
→ Verificar coordinador.routes.ts

❌ ERROR: 404 /api/v1/citas-calendario/
→ Backend no tiene el endpoint
→ Verificar backend/app/api/routers/citas_calendar.py
```

**Si ves errores:**
- [ ] Toma captura del error
- [ ] Lee el mensaje completo
- [ ] Busca solución en INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md → Troubleshooting

---

## 1️⃣2️⃣ VERIFICACIÓN DE PERFORMANCE

### La aplicación debe ser rápida:

- [ ] Interfaz carga en < 2 segundos
- [ ] Ver vista previa demora < 1 segundo
- [ ] Crear citas demora < 10 segundos
- [ ] Google Calendar sincroniza en < 5 segundos
- [ ] No hay congelamiento de pantalla

**Cómo medir:**
```
1. Abre interfaz
2. Cuenta segundos hasta que aparezca
3. Llena formulario
4. Clic "VER VISTA PREVIA"
5. Cuenta segundos
6. Clic "ASIGNAR"
7. Espera a que termine
8. Cuenta segundos
```

**Si es lento:**
```
> 10 segundos para crear:
→ Base de datos lenta
→ Backend lento
→ Conexión a Google Calendar lenta

Soluciones:
- Revisar índices en MySQL
- Verificar velocidad de internet
- Usar herramientas de profiling
```

---

## 1️⃣3️⃣ VERIFICACIÓN DE SEGURIDAD

### Solo usuarios autorizados deben acceder:

**Test 1: Logueado como COORDINADOR**
- [ ] Puedes acceder a `/coordinador/asignar-terapias`
- [ ] Ves todos los campos
- [ ] Puedes crear citas

**Test 2: Logueado como PADRE**
- [ ] NO puedes acceder (o error 403)
- [ ] No ves la interfaz

**Test 3: Sin login**
- [ ] Te redirige a login
- [ ] No puedes ver datos

**Cómo verificar:**
```
1. Cierra sesión (logout)
2. Intenta acceder a /coordinador/asignar-terapias
3. Deberías ser redirigido a login

4. Loguéate como PADRE
5. Intenta acceder a /coordinador/asignar-terapias
6. Deberías ver error 403 o acceso denegado
```

---

## 1️⃣4️⃣ VERIFICACIÓN DE DATOS

### Los datos deben ser consistentes:

**Test: Integridad**
- [ ] Un niño seleccionado no desaparece al cambiar terapeuta
- [ ] Los datos se mantienen si cambias entre campos
- [ ] Los datos de formulario no se pierden

**Test: Duplicados**
```
1. Crea las mismas 2 citas seguidas
2. Comprueba en BD:
   SELECT COUNT(*) FROM citas 
   WHERE nino_id = X 
   AND fecha = Y

3. Deberías ver 2 filas (se crean ambas)
4. NO deberían detectarse como duplicado
   (Es trabajo del coordinador evitar duplicar)
```

---

## 1️⃣5️⃣ VERIFICACIÓN FINAL - CHECKLIST COMPLETO

Marca aquí cuando TODO esté OK:

```
ARCHIVOS:
  ✅ Todos los archivos existen
  
COMPILACIÓN:
  ✅ npm start sin errores
  
RUTAS:
  ✅ Interfaz accesible en /coordinador/asignar-terapias
  
DATOS:
  ✅ Listas se cargan correctamente
  
INTERFAZ:
  ✅ Se ve profesional y responsive
  
VALIDACIONES:
  ✅ Todas las validaciones funcionan
  
VISTA PREVIA:
  ✅ Modal muestra las citas correctamente
  
CREACIÓN:
  ✅ Citas se crean en BD
  
GOOGLE CALENDAR:
  ✅ Citas aparecen en Google Calendar
  
RECURRENCIA:
  ✅ Múltiples citas se crean correctamente
  
CONSOLA:
  ✅ Sin errores en F12
  
PERFORMANCE:
  ✅ Todo es rápido
  
SEGURIDAD:
  ✅ Solo autorizados pueden acceder
  
INTEGRIDAD:
  ✅ Datos consistentes

SI TODO ESTÁ MARCADO = ✅ LISTO PARA PRODUCCIÓN
```

---

## 📞 ¿QUÉ HACER SI ALGO FALLA?

### Error durante Test 1-3 (Archivos/Compilación)
```
→ Ver: CAMBIOS_DE_ARCHIVOS.md
→ Descarga los archivos nuevamente
→ O contacta al desarrollador
```

### Error durante Test 4-7 (Carga de datos/UI)
```
→ Ver: DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md
→ Revisa consola del navegador (F12)
→ Backend está corriendo?
```

### Error durante Test 8-10 (Creación/Google)
```
→ Ver: INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md
→ Backend está actualizado?
→ Google Calendar está configurado?
```

### Error durante Test 11-15 (Performance/Seguridad)
```
→ Contacta a DevOps
→ Revisar logs del backend
→ Optimizar base de datos
```

---

## 🎯 PRÓXIMOS PASOS

**Si TODO pasa:**
- ✅ Listo para usar en producción
- ✅ Puedes entrenar a usuarios
- ✅ Documental completado

**Si algo falla:**
- 📞 Contacta al equipo técnico
- 📝 Prepara: Paso fallo, Error exacto, Captura pantalla
- 🔍 Revisa troubleshooting en documentación

---

## 📚 DOCUMENTACIÓN RELACIONADA

Si necesitas más detalles:

| Tema | Documento |
|------|-----------|
| No funcionan datos | [DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md](DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md) |
| No funciona Google | [INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md](INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md) |
| Cómo se ve | [TUTORIAL_VISUAL_ASIGNAR_TERAPIAS.md](TUTORIAL_VISUAL_ASIGNAR_TERAPIAS.md) |
| Qué cambió | [CAMBIOS_DE_ARCHIVOS.md](CAMBIOS_DE_ARCHIVOS.md) |
| Acceso rápido | [ACCESO_RAPIDO_ASIGNAR_TERAPIAS.md](ACCESO_RAPIDO_ASIGNAR_TERAPIAS.md) |
| Índice completo | [INDICE_ASIGNAR_TERAPIAS.md](INDICE_ASIGNAR_TERAPIAS.md) |

---

## 🎉 ¡FELICIDADES!

Si pasaste todos los tests = **El módulo está funcionando perfectamente**

Ahora puedes:
- ✅ Usar la interfaz
- ✅ Crear terapias
- ✅ Sincronizar con Google Calendar
- ✅ Entrenar a otros usuarios
- ✅ Desplegar a producción

---

**Versión:** 1.0  
**Estado:** 🟢 Actualizado  
**Última revisión:** 16 de Diciembre de 2024

**¿Necesitas ayuda?** → Lee [INDICE_ASIGNAR_TERAPIAS.md](INDICE_ASIGNAR_TERAPIAS.md)

¡Buen testing! 🧪✨

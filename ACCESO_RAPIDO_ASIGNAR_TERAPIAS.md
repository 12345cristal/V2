# ⚡ ACCESO RÁPIDO - Asignar Terapias

**Guía de referencia rápida. Léelo en 2 minutos.**

---

## 🎯 ¿QUÉ ES ESTO?

Un nuevo módulo de Angular que permite a COORDINADORES asignar terapias a niños con terapeuta asignado.  
Las citas se sincronizan automáticamente con Google Calendar.

---

## 🚀 INICIO INMEDIATO

### Paso 1: Accede a la interfaz
```
URL: http://localhost:4200/coordinador/asignar-terapias
```

### Paso 2: Llena el formulario
```
1. Selecciona un NIÑO
2. Selecciona un TERAPEUTA
3. Selecciona una TERAPIA
4. Elige días y horarios
5. Haz clic en "ASIGNAR TERAPIAS"
```

### Paso 3: Verifica en Google Calendar
```
✅ Las citas aparecerán automáticamente
```

---

## 📝 CAMPOS DEL FORMULARIO

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| Niño | Selecciona de la lista | ✅ Sí |
| Terapeuta | Selecciona de la lista | ✅ Sí |
| Terapia | Tipo de terapia (Física, Psicológica, etc.) | ✅ Sí |
| Fecha Inicio | Desde cuándo comienza | ✅ Sí |
| Cantidad Semanas | Cuántas semanas durará | ✅ Sí |
| Días | Qué días de la semana (Lunes-Sábado) | ✅ Sí |
| Hora Inicio | A qué hora comienza | ✅ Sí |

---

## 📋 EJEMPLO PRÁCTICO

```
Niño:        María García (8 años)
Terapeuta:   Dr. Carlos López
Terapia:     Fisioterapia
Inicio:      2024-12-20
Semanas:     8 semanas
Días:        Lunes, Miércoles, Viernes
Hora:        09:00 - 10:00

Resultado:
✅ 24 citas creadas (3 días × 8 semanas)
✅ Todas sincronizadas a Google Calendar
✅ Notificaciones automáticas enviadas
```

---

## ✅ VALIDACIONES

Se validará automáticamente que:

- ✔️ Todos los campos estén completos
- ✔️ La fecha de inicio sea futura
- ✔️ Al menos 1 día sea seleccionado
- ✔️ Mínimo 1 semana
- ✔️ Máximo 52 semanas
- ✔️ Hora inicio < hora fin

Si hay error, verás un mensaje en rojo explicando qué falta.

---

## 🎨 INTERFAZ

La pantalla tiene 3 secciones:

```
┌─────────────────────────────────────┐
│  ASIGNAR NUEVAS TERAPIAS           │ ← Título con ícono
├─────────────────────────────────────┤
│ 1. DATOS DE LA ASIGNACIÓN          │ ← Sección 1: Nino, Terapeuta, Terapia
├─────────────────────────────────────┤
│ 2. HORARIOS Y RECURRENCIA          │ ← Sección 2: Fechas y días
├─────────────────────────────────────┤
│ 3. SINCRONIZACIÓN                  │ ← Sección 3: Vista previa y botón
├─────────────────────────────────────┤
│        [ASIGNAR TERAPIAS]           │ ← Botón principal
└─────────────────────────────────────┘
```

---

## 📱 DISPOSITIVOS

Funciona en:
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768x1024)
- ✅ Móvil (320x480+)

---

## 🔔 NOTIFICACIONES

Verás 3 tipos de mensajes:

```
✅ ÉXITO (Verde)
   "24 citas creadas correctamente"
   Desaparece en 5 segundos

⚠️ ADVERTENCIA (Amarillo)
   "Algunos datos están incompletos"
   
❌ ERROR (Rojo)
   "Error al conectar con Google Calendar"
   Botón para reintentar
```

---

## 💾 DATOS GUARDADOS

Cuando creas una cita:

```
Base de datos MySQL:
  → Nueva fila en tabla CITAS

Google Calendar:
  → Nuevo evento automáticamente

Sistema:
  → Notificaciones enviadas a usuarios
```

---

## 🔒 SEGURIDAD

Solo pueden acceder:

```
✅ COORDINADOR
✅ ADMIN

❌ Otros roles: Acceso denegado
```

---

## 📅 VISTA PREVIA

Antes de asignar, puedes ver:

```
[VER VISTA PREVIA]
  ↓
┌──────────────────────────────────┐
│ Citas que se crearán:            │
├──────────────────────────────────┤
│ • Lunes 20-12 09:00-10:00       │
│ • Miércoles 22-12 09:00-10:00   │
│ • Viernes 24-12 09:00-10:00     │
│ ... (24 total)                   │
└──────────────────────────────────┘
  ↓
[ASIGNAR TERAPIAS]
```

---

## 🆘 TROUBLESHOOTING RÁPIDO

### No aparece la interfaz
- Verifica que estés en: `http://localhost:4200/coordinador/asignar-terapias`
- Refresh de página (F5)
- Comprobar que tienes rol COORDINADOR

### No se crean las citas
- Verifica que todos los campos están llenos
- Busca el mensaje de error en rojo
- Revisa que Google Calendar está configurado

### Citas con hora incorrecta
- Las horas se calculan automáticamente según duración de terapia
- Si necesitas cambiar: edita la terapia primero

### Google Calendar no sincroniza
- Espera 5 segundos (es lento)
- Refresca Google Calendar (F5)
- Verifica credenciales en backend

---

## 📞 CONTACTO Y SOPORTE

**Problema técnico:**
→ Ver: [DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md](DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md)

**No sé usar:**
→ Ver: [GUIA_ASIGNAR_TERAPIAS.md](GUIA_ASIGNAR_TERAPIAS.md)

**Quiero desplegar:**
→ Ver: [INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md](INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md)

**Quiero entender todo:**
→ Ver: [INDICE_ASIGNAR_TERAPIAS.md](INDICE_ASIGNAR_TERAPIAS.md)

---

## 🎯 CASOS DE USO

### Caso 1: Crear terapias semanales para un niño
```
1. Selecciona el niño
2. Selecciona terapeuta
3. Selecciona terapia
4. Elige Lunes, Miércoles, Viernes
5. 8 semanas
6. 09:00
7. Haz clic ASIGNAR
✅ 24 citas creadas
```

### Caso 2: Terapia especial de martes y jueves
```
1. Selecciona niño
2. Selecciona terapeuta
3. Selecciona terapia especial
4. Elige Martes, Jueves
5. 12 semanas
6. 14:00
7. Haz clic ASIGNAR
✅ 24 citas creadas
```

### Caso 3: Sesión única puntual
```
1. Selecciona niño
2. Selecciona terapeuta
3. Selecciona terapia
4. Elige Solo LUNES
5. 1 semana (sesión puntual)
6. 10:30
7. Haz clic ASIGNAR
✅ 1 cita creada
```

---

## ⚙️ CONFIGURACIÓN TÉCNICA

No necesitas configurar nada. Todo está ya hecho:

- ✅ Backend listo
- ✅ Google Calendar configurado
- ✅ Base de datos actualizada
- ✅ Rutas registradas
- ✅ Permisos configurados

---

## 🔄 FLUJO COMPLETO

```
USUARIO ABRE INTERFAZ
   ↓
LLENA FORMULARIO
   ↓
VE VISTA PREVIA
   ↓
HACE CLIC "ASIGNAR"
   ↓
BACKEND CREA CITAS (MySQL)
   ↓
GOOGLE CALENDAR SINCRONIZA
   ↓
NOTIFICACIONES ENVIADAS
   ↓
✅ ÉXITO
```

---

## 📊 ESTADÍSTICAS

```
Citas máximo por asignación: 260 (52 semanas × 5 días)
Citas mínimo por asignación: 1
Duración máxima: 52 semanas
Duración mínima: 1 semana
Sincronización: Automática (< 5 segundos)
Disponibilidad: 24/7
```

---

## 🌐 LOCALIZACIÓN

Idioma: **Español**  
Zona horaria: **Sistema local**  
Moneda: **No aplica**  

---

## 🔐 PERMISOS

```
Nivel: COORDINADOR
Acción:
  ✅ Ver interfaz
  ✅ Crear citas
  ✅ Ver vista previa
  ✅ Asignar terapias

  ❌ Modificar (usa módulo separado)
  ❌ Eliminar (usa módulo separado)
```

---

## 📱 ATAJOS

```
Enter        → Asignar (si todo está validado)
Tab          → Siguiente campo
Shift+Tab    → Campo anterior
Escape       → Cerrar modal de vista previa
```

---

## 🎉 LISTO PARA USAR

Ya está:
- ✅ Código implementado
- ✅ Base de datos actualizada
- ✅ Google Calendar configurado
- ✅ Rutas registradas
- ✅ Documentación completa

Solo abre la URL y comienza a asignar terapias.

---

## 📚 DOCUMENTACIÓN COMPLETA

| Documento | Contenido |
|-----------|----------|
| [README_ASIGNAR_TERAPIAS.md](README_ASIGNAR_TERAPIAS.md) | Punto de entrada |
| [GUIA_ASIGNAR_TERAPIAS.md](GUIA_ASIGNAR_TERAPIAS.md) | Guía de usuario |
| [TUTORIAL_VISUAL_ASIGNAR_TERAPIAS.md](TUTORIAL_VISUAL_ASIGNAR_TERAPIAS.md) | Visual paso a paso |
| [DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md](DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md) | Técnica |
| [INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md](INTEGRACION_RAPIDA_ASIGNAR_TERAPIAS.md) | Deploy |
| [CAMBIOS_DE_ARCHIVOS.md](CAMBIOS_DE_ARCHIVOS.md) | Qué cambió |
| [INDICE_ASIGNAR_TERAPIAS.md](INDICE_ASIGNAR_TERAPIAS.md) | Índice |
| [ACCESO_RAPIDO_ASIGNAR_TERAPIAS.md](ACCESO_RAPIDO_ASIGNAR_TERAPIAS.md) | Este documento |

---

**Versión:** 1.0  
**Estado:** 🟢 Producción  
**Última actualización:** 16 de Diciembre de 2024

**¿Listo? Abre:**  
→ `http://localhost:4200/coordinador/asignar-terapias`

¡Que disfrutes asignando terapias! 🚀

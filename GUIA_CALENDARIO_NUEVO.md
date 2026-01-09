# 📅 Guía de Uso - Calendario de Terapias Mejorado

## Inicio Rápido

### Acceso al Calendario
```
URL: http://localhost:57317
Navegación: Dashboard → Coordinador → Asignar Terapias
```

---

## 🎯 Características Principales

### 1. **Vista Semanal (Por defecto)**
La vista principal muestra 6 días de la semana con una cuadrícula de 11 horas (08:00 - 18:00).

#### Elementos:
```
┌─────────────────────────────────────────┐
│ Lunes    Martes    Miércoles  Jueves...│  ← Días
├─────────────────────────────────────────┤
│ 08:00 │ ┌─────────────────────────────┐ │  ← Horas
│ 09:00 │ │ 09:00 - 10:00              │ │
│ 10:00 │ │ Terapia de Lenguaje        │ │
│ 11:00 │ │ Juan Pérez / Dra. María    │ │
│       │ │                            │ │
└─────────────────────────────────────────┘
```

#### Interacciones:
- **Click en evento**: Editar detalles
- **Drag & drop**: Mover evento a otro día
- **Resize**: Arrastrar bottom handle para cambiar duración

### 2. **Vista Diaria**
Muestra un solo día con más espacio por evento.

#### Cómo Acceder:
```
Header → View Switcher → [Día icon]
```

#### Beneficio:
- Más detalles por evento
- Mejor para ediciones
- Ideal para móviles

### 3. **Vista Mensual**
Calendario tipo Google Calendar mostrando todos los días del mes.

#### Cómo Acceder:
```
Header → View Switcher → [Mes icon]
```

---

## 🔍 Sistema de Filtros

### Localización
```
Sidebar izquierdo → Sección "FILTROS"
```

### Filtros Disponibles

#### 1. Niño (👧)
```
☐ Todos los niños (por defecto)
☐ Juan Pérez
☐ María López
☐ Carlos García
...
```

#### 2. Terapeuta (👤)
```
☐ Todos los terapeutas
☐ Dra. María García
☐ Lic. Roberto López
☐ Ps. Ana Martínez
...
```

#### 3. Tipo de Terapia (💊)
```
☐ Todas las terapias
☐ Logopedia
☐ Fisioterapia
☐ Psicología
☐ Terapia Ocupacional
...
```

#### 4. Estados de Cita
```
☑ ● Programadas (Azul)
☑ ● Reprogramadas (Naranja)
☑ ● Canceladas (Rojo)
```

#### 5. Ver Todo
```
☐ Ver todo (carga completa)
  └─ Carga todos los eventos sin filtros
  └─ Más pesado en navegadores lentos
```

### Cómo Usar los Filtros

**Paso 1:** Seleccionar criterios
```
1. Click en dropdown "Niño" → Seleccionar niño
2. Click en dropdown "Terapeuta" → Seleccionar terapeuta
3. Click en dropdown "Terapia" → Seleccionar tipo
4. Marcar checkboxes de estados a mostrar
```

**Paso 2:** Aplicar
```
Click en botón "Aplicar Filtros"
```

**Resultado:** Calendario se actualiza mostrando solo eventos que coinciden

### Limpiar Filtros
```
Click en botón [X] en header de filtros
O
Click en "Limpiar" en acciones
```

---

## 📅 Navegación del Calendario

### Navegación Semanal

**Botón "Hoy"**
```
Click → Vuelve a la semana actual
```

**Botones Anterior/Siguiente** (◀ ▶)
```
◀ Click → Semana anterior
▶ Click → Semana siguiente
```

**Período Mostrado**
```
Ej: "25–31 de diciembre 2025"
└─ Click para ver selector de fecha (próxima versión)
```

### Navegación Mini Calendario (Sidebar)

**Navegación Meses/Años**
```
⏪ ◀ Diciembre 2025 ▶ ⏫
│  │                │  │
│  │                │  └─ Siguiente año
│  │                └───── Siguiente mes
│  └───────────────────── Mes anterior
└──────────────────────── Año anterior
```

**Seleccionar Día**
```
Click en número del día en mini calendario
→ Salta a esa semana
→ Marca el día como seleccionado
```

---

## ➕ Crear Nueva Terapia

### Método 1: Botón Rápido
```
Header derecho → Click en botón [+] Nueva Terapia
```

### Método 2: Click Doble en Calendario
```
Hacer click en espacio vacío del calendario
→ Abre modal de nueva terapia
```

### Rellenar Formulario

```
┌─────────────────────────────────────────┐
│ ✏️ Nueva Terapia                  [✕]  │
├─────────────────────────────────────────┤
│                                         │
│ INFORMACIÓN PRINCIPAL                   │
│ ┌─────────────────┬─────────────────┐  │
│ │ Niño *          │ Tipo Terapia *  │  │
│ │ [Juan Pérez   ▼]│ [Logopedia     ▼]  │
│ └─────────────────┴─────────────────┘  │
│ │ Terapeuta * (se habilita al sel)    │  │
│ │ [Dra. María García            ▼]   │  │
│                                         │
│ FECHA Y HORARIO                         │
│ ┌──────────┬──────────┬──────────┐    │
│ │ Fecha *  │ Inicio * │ Fin *    │    │
│ │ 12/27/25 │ 09:00    │ 10:00    │    │
│ └──────────┴──────────┴──────────┘    │
│                                         │
│ ☐ Terapia recurrente                   │
│   └─ Si marcar: seleccionar días y sem │
│                                         │
│ ☐ Observaciones                         │
│   └─ Notas adicionales (opcional)      │
│                                         │
│ ☐ Sincronizar con Google Calendar     │
│                                         │
│              [Cancelar] [Crear Terapia]│
└─────────────────────────────────────────┘
```

### Paso a Paso

1. **Seleccionar Niño** (obligatorio)
   ```
   Click en dropdown "Niño"
   → Seleccionar niño de la lista
   ```

2. **Seleccionar Terapia** (obligatorio)
   ```
   Click en dropdown "Tipo de Terapia"
   → Seleccionar tipo de terapia
   → Se activa selector de Terapeuta
   ```

3. **Seleccionar Terapeuta** (obligatorio)
   ```
   Click en dropdown "Terapeuta"
   → Seleccionar terapeuta disponible
   ```

4. **Ingresar Fecha** (obligatorio)
   ```
   Click en campo "Fecha"
   → Aparece date picker
   → Seleccionar fecha
   ```

5. **Ingresar Hora Inicio** (obligatorio)
   ```
   Click en campo "Hora Inicio"
   → Ingresar hora (ej: 09:00)
   → Automáticamente se calcula Fin según duración
   ```

6. **Opcionales - Recurrencia**
   ```
   Si desea sesiones semanales:
   ☑ Terapia recurrente
   
   Seleccionar días: L M X J V S
   Cantidad semanas: [spinner con + -]
   
   Resultado: Se crean múltiples eventos
   ```

7. **Opcionales - Notas**
   ```
   Campo "Observaciones"
   → Escribir notas importantes
   → Se guardan en el evento
   ```

8. **Sincronización Google**
   ```
   Si está configurado:
   ☑ Sincronizar con Google Calendar
   → El evento aparecerá en Google Calendar
   ```

### Guardar
```
Click en botón "Crear Terapia"
→ Se validan datos obligatorios
→ Si todo OK: aparece mensaje de éxito
→ Modal se cierra y calendario se actualiza
```

---

## ✏️ Editar Terapia

### Cómo Abrir Edición
```
Opción 1: Click en evento en calendario
Opción 2: Click en evento en vista diaria
```

### En Modo Edición
```
┌─────────────────────────────────────────┐
│ ✏️ Editar Terapia                  [✕]  │
├─────────────────────────────────────────┤
│                                         │
│ [Mismos campos que crear, pre-rellenados]
│                                         │
│ Nota: Campo recurrencia deshabilitado   │
│ (solo se permite editar evento único)   │
│                                         │
│      [Cancelar Terapia] [Guardar]      │
└─────────────────────────────────────────┘
```

### Cambiar Hora/Duración
```
Opción 1: En modal editar - cambiar Inicio/Fin
Opción 2: En calendario - resize handle en evento
          └─ Arrastrar bottom para alargar/acortar
```

### Cambiar Día
```
Opción 1: En modal - cambiar fecha y guardar
Opción 2: En calendario - drag & drop evento
          └─ Mantener presionado y arrastrar a otro día
```

### Cancelar Terapia
```
En modal editar:
Click en botón "Cancelar Terapia"
→ Cambia estado a "Cancelada"
→ Evento se muestra tachado en rojo
→ Se mantiene en historial
```

---

## 🎨 Entender los Colores

### Estado de Terapia

| Color | Significado | Acción |
|-------|-------------|--------|
| 🔵 Azul | Programada | Normal, en calendario |
| 🟠 Naranja | Reprogramada | Se movió de fecha original |
| 🔴 Rojo | Cancelada | Se canceló, no se realizará |

### En Filtros
```
☑ ● Programadas (Azul)     → Muestra eventos azules
☑ ● Reprogramadas (Naranja) → Muestra eventos naranjas  
☑ ● Canceladas (Rojo)      → Muestra eventos rojos
```

---

## 📊 Estadísticas Rápidas (Sidebar)

```
┌──────────────┬──────────────┐
│ 📅 Citas     │ 👥 Niños    │
│     24       │     12      │
└──────────────┴──────────────┘
```

- **Citas**: Total de terapias programadas
- **Niños**: Cantidad de niños con terapias activas

**Nota:** Se actualizan automáticamente al filtrar

---

## 📱 Uso en Móvil

### Sidebar
```
Desktop: Visible a la izquierda
Móvil:   Oculto por defecto
         Click en [≡] para abrir flotante
```

### Vista Recomendada
```
Móvil: Usar "Vista Día" para mejor experiencia
       Scroll vertical es fácil
       Eventos más legibles
```

### Toque (Touch)
```
- Tap: Seleccionar/editar
- Drag: Mover eventos (si se mantiene presionado)
- Pinch: No soportado (usar scroll)
```

---

## ⌨️ Atajos de Teclado

```
(Próxima versión)
Ctrl/Cmd + N    → Nueva terapia
Ctrl/Cmd + L    → Limpiar filtros
Escape          → Cerrar modal
Tab/Shift+Tab   → Navegar campos
```

---

## 🐛 Solucionar Problemas

### Problema: "El evento no se guarda"
```
Solución:
1. Verificar campos obligatorios (con *)
2. Verificar que fecha esté en formato correcto
3. Verificar que Hora Inicio < Hora Fin
4. Revisar consola (F12) para mensajes de error
```

### Problema: "No puedo mover evento con drag & drop"
```
Solución:
1. Asegurarse que está en Vista Semana
2. Hacer click y mantener presionado
3. Arrastrar a otro día en la misma semana
4. Soltar en el nuevo día
```

### Problema: "Calendario no se actualiza"
```
Solución:
1. Aplicar filtros nuevamente
2. Recargar página (F5)
3. Revisar que backend está activo (http://localhost:8000)
4. Ver consola para errores
```

### Problema: "Ver Mas" botones no funcionan
```
Solución:
1. Pasar a Vista Mes para ver todos los eventos del día
2. O usar Vista Día para ver detalles
```

---

## 💡 Tips y Trucos

### Crear Múltiples Sesiones Rápidamente
```
1. Abrir Nueva Terapia
2. Marcar ☑ Terapia recurrente
3. Seleccionar días (Ej: L, M, X, J, V)
4. Cantidad semanas (Ej: 8)
→ Se crean 40 eventos de una vez
```

### Buscar Evento Específico
```
1. Filtrar por Niño específico
2. Filtrar por Terapeuta específico
3. Cambiar vista si es necesario
→ Más fácil localizar
```

### Sincronizar con Google Calendar
```
1. Al crear/editar, marcar ☑ Sincronizar
2. Si está configurado: evento aparece en Google
3. Click en 🔗 ícono para abrir en Google
```

### Navegar a Meses Lejanos
```
En vez de hacer click 10 veces en ▶:
1. Mini Calendario → ⏫ botón
2. Click en año para cambiar rápido
3. Click en mes para cambiar
4. Click en día para ir a esa semana
```

---

## 📞 Soporte

### Reportar Problema
```
1. Tomar captura de pantalla
2. Anotar hora exacta
3. Describir pasos para reproducir
4. Enviar a administrador
```

### Información Útil
```
- Navegador: Chrome 120+ (recomendado)
- Resolución pantalla: 1024x768 mínimo
- Backend debe estar activo
- Cache del navegador: Limpiar si hay problemas
```

---

**Última Actualización:** 27 de Diciembre, 2025  
**Versión:** 2.0 - Calendario Profesional  
**Estado:** ✅ Funcional

# 📋 Organización del Sidebar - Sistema TEA

## 🎯 Estructura Actualizada

### 👨‍💼 MENÚ COORDINADOR / ADMINISTRADOR

#### 📌 **Principal**
- **Inicio** - Dashboard con métricas y resumen
- **Citas** - Gestión de citas y calendario

#### 📊 **Gestión**
- **Niños** - Registro y administración de niños
- **Personal** - Gestión de terapeutas y personal
  - Lista de personal
  - Detalles de terapeuta
  - Horarios de terapeuta
- **Terapias** - Catálogo y seguimiento de terapias
- **Usuarios** - Gestión de cuentas de usuario

#### 🧠 **Análisis y Decisión**
- **Priorización TOPSIS** - Análisis multicriterio para priorizar niños
  - Definición de criterios
  - Matriz de decisión
  - Resultados con ranking
- **Recomendaciones** - Sistema de recomendación de contenido
  - Actividades recomendadas
  - Terapias sugeridas
- **Selección Terapeutas** - TOPSIS para asignación de terapeutas
  - Análisis de carga de trabajo
  - Compatibilidad terapeuta-niño

#### ⚙️ **Administración**
- **Auditoría** - Registro de acciones y cambios del sistema

#### 👤 **Cuenta**
- **Mi Perfil** - Información personal y configuración

---

### 👨‍⚕️ MENÚ TERAPEUTA

#### 📌 **Principal**
- **Inicio** - Dashboard del terapeuta
  - Resumen de sesiones del día
  - Próximas citas
  - Estadísticas personales

#### 💼 **Mi Trabajo**
- **Mis Pacientes** - Lista de niños asignados
  - Información de cada paciente
  - Historial de sesiones
  - Notas y observaciones
- **Actividades** - Gestión de actividades terapéuticas
  - Crear y editar actividades
  - Marcar completadas
  - Progreso de actividades
- **Mi Horario** - Calendario personal
  - Disponibilidad
  - Sesiones programadas
  - Gestión de tiempo

#### 📚 **Recursos**
- **Mis Recursos** - Materiales y herramientas
  - Documentos educativos
  - Plantillas de ejercicios
  - Material multimedia
- **Recomendaciones** - Panel de recomendaciones para pacientes
  - Actividades sugeridas por el sistema
  - Terapias recomendadas
  - Personalización de contenido

#### 👤 **Cuenta**
- **Mi Perfil** - Información personal y configuración

---

### 👨‍👩‍👦 MENÚ PADRE/TUTOR

#### 📌 **Principal**
- **Inicio** - Vista general del progreso
- **Mi Hijo(a)** - Información detallada del niño

#### 📈 **Seguimiento**
- **Terapias** - Seguimiento de terapias
- **Actividades** - Tareas y ejercicios
- **Documentos** - Reportes y archivos
- **Recomendaciones** - Sugerencias personalizadas

#### 👤 **Cuenta**
- **Mi Perfil** - Información personal

---

## 🔄 Rutas Configuradas

### Coordinador (`/coordinador/...`)
```
/inicio
/citas
/ninos
/nino/nuevo
/nino/:id/editar
/personal
/personal/nuevo
/personal/editar/:id
/personal/detalle/:id
/personal/horarios/:id
/terapias
/usuarios
/usuarios/nuevo
/usuarios/editar/:id
/prioridad-ninos
/topsis-prioridad
/recomendacion-nino
/topsis-terapeutas ✅ NUEVA
/auditoria
/perfil
/terapeutas/:id (detalle)
```

### Terapeuta (`/terapeuta/...`)
```
/inicio
/pacientes
/actividades ✅ AGREGADA AL SIDEBAR
/horarios
/recursos
/recomendaciones ✅ AGREGADA AL SIDEBAR
/perfil
```

### Padre (`/padre/...`)
```
/inicio
/info-nino
/terapias
/actividades
/documentos
/recomendaciones
/perfil
```

---

## 🎨 Iconografía Utilizada

| Sección | Ícono | Descripción |
|---------|-------|-------------|
| Inicio | `dashboard` | Dashboard general |
| Citas | `calendar_month` | Calendario |
| Niños | `child_care` | Gestión de niños |
| Personal | `badge` | Personal del centro |
| Terapias | `medical_services` | Servicios terapéuticos |
| Usuarios | `manage_accounts` | Cuentas de usuario |
| Priorización TOPSIS | `bar_chart` | Análisis estadístico |
| Recomendaciones | `lightbulb` | Sugerencias inteligentes |
| Selección Terapeutas | `psychology` | Análisis psicológico |
| Auditoría | `history` | Historial de cambios |
| Pacientes | `groups` | Grupo de pacientes |
| Actividades | `task_alt` | Tareas completadas |
| Horarios | `schedule` | Gestión de tiempo |
| Recursos | `folder_open` | Carpeta de archivos |
| Perfil | `person` | Usuario personal |

---

## ✅ Mejoras Implementadas

### 1. **Coordinador**
- ✅ Reorganizado en secciones lógicas: Principal, Gestión, Análisis y Decisión, Administración
- ✅ Agregada ruta **Selección Terapeutas** (`/topsis-terapeutas`)
- ✅ Renombrado "Priorización" a "Priorización TOPSIS" para mayor claridad
- ✅ Nueva sección "Análisis y Decisión" agrupando herramientas de IA

### 2. **Terapeuta**
- ✅ Agregada opción **Actividades** en "Mi Trabajo"
- ✅ Agregada opción **Recomendaciones** en "Recursos"
- ✅ Reorganizado en secciones: Principal, Mi Trabajo, Recursos, Cuenta
- ✅ Mejorados textos: "Mis Pacientes", "Mi Horario", "Mis Recursos"

### 3. **Consistencia**
- ✅ Todas las rutas del sidebar coinciden con las definidas en `*.routes.ts`
- ✅ Iconografía consistente y semántica
- ✅ Estructura de secciones similar entre roles
- ✅ Nomenclatura clara y descriptiva

---

## 🚀 Próximas Mejoras Sugeridas

### Coordinador
- [ ] Agregar submenu desplegable para "Personal" (lista, horarios, detalles)
- [ ] Badge con contador de citas pendientes
- [ ] Indicador visual de alertas en "Auditoría"

### Terapeuta
- [ ] Badge con contador de pacientes del día
- [ ] Notificaciones de nuevas recomendaciones
- [ ] Progreso visual de actividades completadas

### General
- [ ] Modo oscuro/claro
- [ ] Sidebar colapsable con iconos únicamente
- [ ] Búsqueda rápida dentro del sidebar
- [ ] Favoritos/Accesos rápidos personalizables
- [ ] Indicadores de progreso en items del menú

---

## 📱 Responsive Design

El sidebar está completamente adaptado para dispositivos móviles:
- Overlay oscuro cuando está abierto
- Animación suave de apertura/cierre
- Botón de cierre visible
- Touch-friendly (botones grandes)
- Scroll automático si el contenido excede la altura

---

## 🎯 Conclusión

El sidebar ahora refleja **todas las funcionalidades disponibles** en el sistema, organizadas de manera lógica y accesible. La navegación es clara, con iconografía apropiada y textos descriptivos que facilitan la experiencia del usuario.

**Estado:** ✅ Completamente funcional y actualizado
**Compilación:** ✅ Sin errores
**Rutas:** ✅ Todas registradas correctamente

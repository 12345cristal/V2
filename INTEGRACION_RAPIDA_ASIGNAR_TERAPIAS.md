# Integración Rápida - Módulo Asignar Terapias

## 🚀 Inicio Rápido

### 1. Verificar Archivos (5 min)

Los siguientes archivos están listos:

```
✅ src/app/coordinador/asignar-terapias/asignar-terapias.component.ts
✅ src/app/coordinador/asignar-terapias/asignar-terapias.component.html
✅ src/app/coordinador/asignar-terapias/asignar-terapias.component.scss
✅ src/app/service/citas-calendario.service.ts (Actualizado)
✅ src/app/coordinador/coordinador.routes.ts (Con ruta)
```

### 2. Iniciar Aplicación (2 min)

```powershell
npm start
```

### 3. Acceder a la Interfaz (1 min)

```
Ruta: http://localhost:4200/coordinador/asignar-terapias
Requerimiento: Login como COORDINADOR
```

---

## 📋 Datos de Ejemplo

### Crear Terapias de Prueba

Si necesitas datos de prueba, ejecuta en el backend:

```bash
# Backend (Python)
python backend/scripts/crear_datos_recomendaciones.py
```

O crea manualmente:

**Base de datos - tabla terapias:**
```sql
INSERT INTO terapias (nombre, duracion_minutos, descripcion) VALUES
('Terapia Ocupacional', 60, 'Mejora habilidades funcionales'),
('Fonoaudiología', 45, 'Mejora del lenguaje'),
('Psicología', 50, 'Apoyo emocional y conductual'),
('Fisioterapia', 60, 'Movimiento y motricidad');
```

---

## ✨ Características Principales

### 1. Asignación de Terapias
- Selecciona niño, terapeuta y tipo de terapia
- Elige fecha, días y horario
- Sistema genera automáticamente todas las citas

### 2. Previsualización
- Haz clic en "Previsualizar" antes de crear
- Verifica todas las citas que se crearán
- Vuelve atrás si necesitas cambios

### 3. Google Calendar
- Activa "Sincronizar con Google Calendar"
- Cada cita aparece automáticamente en el calendario
- Los terapeutas reciben eventos y recordatorios

### 4. Validación Automática
- El sistema valida fechas, horarios, selecciones
- Mensajes claros si algo falta
- Hora de fin se calcula automáticamente

---

## 🔧 Configuración Backend

### Asegurar que Backend Tiene:

1. **Endpoints de Catálogos:**
   ```
   GET /api/v1/ninos              → Lista de niños
   GET /api/v1/personal           → Lista de terapeutas
   GET /api/v1/terapias           → Lista de terapias
   ```

2. **Endpoint de Citas:**
   ```
   POST /api/v1/citas-calendario/ → Crear cita con sync Google
   ```

3. **Google Calendar Configurado:**
   ```python
   # Backend: app/core/google_calendar_service.py
   # Debe tener:
   - Credenciales de Service Account
   - googleapi >= 2.0
   - google-auth >= 2.0
   ```

4. **Tabla de Citas Extendida:**
   ```sql
   ALTER TABLE citas ADD COLUMN (
     google_event_id VARCHAR(255),
     google_calendar_link TEXT,
     sincronizado_calendar BOOLEAN DEFAULT FALSE,
     fecha_sincronizacion DATETIME
   );
   ```

---

## 🌐 Estructura de Datos

### Interfaz de Creación

```typescript
{
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string;              // "YYYY-MM-DD"
  hora_inicio: string;        // "HH:MM:SS"
  hora_fin: string;          // "HH:MM:SS"
  sincronizar_google_calendar: boolean;
}
```

### Respuesta del Backend

```json
{
  "id_cita": 42,
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2024-12-20",
  "hora_inicio": "09:00:00",
  "hora_fin": "10:00:00",
  "google_event_id": "abcd1234efgh5678",
  "google_calendar_link": "https://calendar.google.com/...",
  "sincronizado_calendar": true,
  "fecha_sincronizacion": "2024-12-16T17:30:45"
}
```

---

## 🎨 Interfaz Visual

### Secciones del Formulario

```
┌─────────────────────────────────────────┐
│  📅 ASIGNAR TERAPIAS                    │
│  Programa sesiones con Google Calendar  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ① DATOS DE LA ASIGNACIÓN               │
├─────────────────────────────────────────┤
│ [Seleccionar Niño]  [Seleccionar Terapeuta]
│ [Tipo de Terapia]
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ② CONFIGURACIÓN DE HORARIOS            │
├─────────────────────────────────────────┤
│ [Fecha]  [Duración Semanas]
│ [L] [M] [X] [J] [V] [S]
│ [Hora Inicio]  [Hora Fin]
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ③ SINCRONIZACIÓN                        │
├─────────────────────────────────────────┤
│ ☑ Sincronizar con Google Calendar
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ [Previsualizar] [Asignar] [Limpiar]    │
└─────────────────────────────────────────┘
```

---

## 📝 Ejemplo de Uso Paso a Paso

### Escenario: Asignar Terapia Ocupacional a Juan García

**Paso 1:** Login como COORDINADOR

**Paso 2:** Navega a "Módulo Terapias" → "Asignar Terapias"

**Paso 3:** Completa el formulario
- Niño: "Juan García Pérez"
- Terapeuta: "Dra. María López - Terapia Ocupacional"
- Terapia: "Terapia Ocupacional (60 min)"
- Fecha: "20 Diciembre 2024"
- Duración: "4" semanas
- Días: Lunes, Miércoles, Viernes
- Hora: 09:00 - 10:00
- Google: ☑ Activado

**Paso 4:** Haz clic en "Previsualizar"
- Se abre modal mostrando 12 citas (4 semanas × 3 días)
- Verifica que las fechas sean correctas

**Paso 5:** Haz clic en "Asignar Terapias"
- Sistema crea 12 citas secuencialmente
- Cada una se sincroniza con Google Calendar
- Mensaje de éxito: "Se crearon 12 citas exitosamente"

**Paso 6:** Verifica en Google Calendar
- Las citas aparecen en el calendario del terapeuta
- Incluyen descripción, hora y recordatorios

---

## 🔐 Control de Acceso

### Quién puede acceder:

```javascript
// Roles permitidos:
✅ COORDINADOR (id: 2)
✅ ADMIN (id: 1)

❌ TERAPEUTA
❌ PADRE
❌ Cualquier otro rol
```

### Protección en Rutas:

```typescript
// En coordinador.routes.ts
{
  path: 'asignar-terapias',
  component: AsignarTerapiasComponent,
  canActivate: [AuthGuard, RoleGuard],
  data: { roles: [1, 2] }
}
```

---

## ⚡ Troubleshooting Rápido

### P: "No cargan los niños/terapeutas"
**R:** Verifica que los endpoints del backend estén disponibles:
```bash
curl http://localhost:8000/api/v1/ninos
```

### P: "No se crean las citas"
**R:** Verifica en console (F12) qué error HTTP retorna el backend

### P: "Google Calendar no sincroniza"
**R:** 
1. Verifica que Google esté configurado en backend
2. Intenta crear sin sincronización primero
3. Revisa logs del backend para errores

### P: "La hora de fin es incorrecta"
**R:** Se calcula automáticamente con duración de terapia. Ajusta manualmente si lo necesitas.

---

## 📚 Documentación Relacionada

- **GUIA_ASIGNAR_TERAPIAS.md** - Guía completa para usuarios
- **DOCUMENTACION_TECNICA_ASIGNAR_TERAPIAS.md** - Especificaciones técnicas
- **RESUMEN_ASIGNAR_TERAPIAS.md** - Resumen ejecutivo del proyecto

---

## ✅ Checklist de Verificación

```
Backend:
- [ ] Endpoints de catálogos funcionando
- [ ] Endpoint POST /citas-calendario/ funciona
- [ ] Google Calendar configurado
- [ ] BD con columnas de Google (google_event_id, etc.)

Frontend:
- [ ] npm start sin errores
- [ ] Acceder a /coordinador/asignar-terapias
- [ ] Cargan niños, terapeutas, terapias
- [ ] Previsualizar muestra citas correctas
- [ ] Crear citas funciona
- [ ] Mensajes de éxito/error aparecen
- [ ] Responsive en mobile

Testing:
- [ ] Crear 5+ citas de prueba
- [ ] Verificar en módulo Citas
- [ ] Verificar en Google Calendar
- [ ] Probar validaciones
- [ ] Probar en móvil/tablet
```

---

## 🚀 Despliegue

### Producción:

```bash
# Build
npm run build

# Resultado
dist/autismo/  # Carpeta lista para subir

# En servidor
ng serve --prod
# O con servidor estático
serve -s dist/autismo/
```

### Logs de Auditoría:

Las citas creadas quedan registradas en la BD con:
- `fecha_creacion`
- `creado_por` (ID del usuario coordinador)
- `google_event_id` (si sincronizado)

---

## 📞 Soporte

Para issues o preguntas:
1. Revisa la documentación técnica
2. Verifica los logs del navegador (F12 → Console)
3. Verifica los logs del backend
4. Contacta al equipo de desarrollo

---

**Versión:** 1.0  
**Última Actualización:** 16 de Diciembre de 2024  
**Estado:** 🟢 Listo para Producción

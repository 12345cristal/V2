# 🚀 GUÍA DE IMPLEMENTACIÓN: MIS HIJOS BACKEND

## 📋 Resumen

Se ha generado completamente el **backend para el módulo "Mis Hijos"** con:

- ✅ Modelos de base de datos (Medicamentos y Alergias)
- ✅ Endpoints API para obtener información del hijo
- ✅ Servicios de lógica de negocio
- ✅ Schemas de validación (Pydantic)
- ✅ Scripts de migración de BD

---

## 📂 Archivos Creados/Modificados

### 📁 Backend

```
backend/
├── app/
│   ├── models/
│   │   └── medicamentos.py          ✅ Modelos: Medicamento, Alergia
│   ├── services/
│   │   └── padres_mis_hijos_service.py  ✅ Lógica de negocio
│   ├── schemas/
│   │   └── padres_mis_hijos.py      ✅ Esquemas de respuesta (DTOs)
│   ├── api/v1/padres/
│   │   ├── __init__.py              ✅ Combinador de routers
│   │   ├── inicio.py                (existente)
│   │   └── mis_hijos.py             ✅ Endpoints API
│   └── api/v1/
│       └── api.py                   ✅ (actualizado con padres_router)
├── sql/
│   └── migracion_medicamentos_alergias.sql  ✅ Script SQL
└── migracion_mis_hijos.py           ✅ Script Python de migración
```

---

## 🔧 PASO 1: Migrar la Base de Datos

### Opción A: Usar Script Python (Recomendado)

```bash
# Desde la carpeta backend
cd backend
python migracion_mis_hijos.py
```

**Lo que hace:**

- Crea tabla `medicamentos`
- Crea tabla `alergias`
- Inserta datos de prueba (opcional)

### Opción B: Usar SQL Directo

1. Abrir phpMyAdmin
2. Seleccionar tu base de datos
3. Ir a "SQL"
4. Copiar y ejecutar el contenido de:
   ```
   backend/sql/migracion_medicamentos_alergias.sql
   ```

---

## 🔄 PASO 2: Verificar Modelos y Relaciones

El modelo `Nino` ya ha sido actualizado con las relaciones:

```python
medicamentos = relationship("Medicamento", back_populates="nino", cascade="all, delete-orphan")
alergias = relationship("Alergia", back_populates="nino", cascade="all, delete-orphan")
```

---

## 📡 PASO 3: Endpoints API Disponibles

El backend expone los siguientes endpoints:

### 1. Obtener Todos los Hijos

```http
GET /api/v1/padres/mis-hijos
Authorization: Bearer {token}
```

**Respuesta:**

```json
{
  "exito": true,
  "datos": {
    "hijos": [
      {
        "id": 1,
        "nombre": "Juan",
        "apellidoPaterno": "García",
        "apellidoMaterno": "López",
        "foto": "https://...",
        "fechaNacimiento": "2015-03-15",
        "edad": 8,
        "diagnostico": "TEA Leve",
        "cuatrimestre": 3,
        "fechaIngreso": "2023-01-10",
        "alergias": [
          {
            "id": 1,
            "nombre": "Penicilina",
            "severidad": "severa",
            "reaccion": "Anafilaxia"
          }
        ],
        "medicamentos": [
          {
            "id": 1,
            "nombre": "Metilfenidato",
            "dosis": "10 mg",
            "frecuencia": "Dos veces al día",
            "razon": "TDAH",
            "fechaInicio": "2024-01-15",
            "fechaFin": null,
            "activo": true,
            "novedadReciente": true,
            "fechaActualizacion": "2026-01-12T10:30:00"
          }
        ],
        "visto": true,
        "novedades": 1
      }
    ]
  },
  "mensaje": "Se encontraron 1 hijo(s)"
}
```

### 2. Obtener Hijo Específico

```http
GET /api/v1/padres/mis-hijos/{nino_id}
Authorization: Bearer {token}
```

### 3. Marcar Medicamento como Visto

```http
PUT /api/v1/padres/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto
Authorization: Bearer {token}
```

---

## 🔐 Autenticación Requerida

Todos los endpoints requieren:

- **Token JWT** en header `Authorization: Bearer {token}`
- **Rol:** Padre (role_id = 4)

El sistema verifica automáticamente que:

- El usuario sea un padre
- El niño pertenezca a ese padre

---

## 📦 Estructura de Datos en BD

### Tabla: medicamentos

```sql
CREATE TABLE medicamentos (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nino_id INT NOT NULL,
  nombre VARCHAR(200),
  dosis VARCHAR(100),
  frecuencia VARCHAR(100),
  razon VARCHAR(255),
  fecha_inicio DATE,
  fecha_fin DATE,
  activo BOOLEAN DEFAULT TRUE,
  novedadReciente BOOLEAN DEFAULT FALSE,
  fecha_actualizacion DATETIME,
  actualizado_por VARCHAR(100),
  notas TEXT,
  fecha_creacion DATETIME,
  FOREIGN KEY (nino_id) REFERENCES ninos(id)
);
```

### Tabla: alergias

```sql
CREATE TABLE alergias (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nino_id INT NOT NULL,
  nombre VARCHAR(200),
  severidad ENUM('leve', 'moderada', 'severa'),
  reaccion TEXT,
  tratamiento TEXT,
  fecha_registro DATETIME,
  FOREIGN KEY (nino_id) REFERENCES ninos(id)
);
```

---

## 🔌 Integración con Frontend

El frontend Angular ya está configurado para usar estos endpoints:

**Archivo:** `src/app/padres/padres.service.ts`

```typescript
getMisHijos(): Observable<RespuestaApi<MisHijosPage>> {
  return this.http.get<RespuestaApi<MisHijosPage>>(`${this.apiUrl}/padres/mis-hijos`);
}
```

---

## ✅ Checklist de Verificación

- [ ] Base de datos migrada (tablas creadas)
- [ ] Modelos importados en `app/models/__init__.py`
- [ ] Servicios funcionando correctamente
- [ ] Endpoints registrados en `api.py`
- [ ] Token JWT válido al probar endpoints
- [ ] Datos de prueba insertados en BD
- [ ] Frontend cargando correctamente los datos
- [ ] Animaciones y estilos aplicados

---

## 🧪 Pruebas Rápidas

### Test 1: Probar endpoint en Postman

```
GET http://localhost:8000/api/v1/padres/mis-hijos
Headers:
  Authorization: Bearer {tu_token_jwt}
```

### Test 2: Revisar logs

```bash
# En la consola donde corre el backend
# Debe mostrar las queries SQL ejecutadas
```

### Test 3: Verificar en navegador

```
http://localhost:4200/padre/mis-hijos
```

---

## 🐛 Troubleshooting

### Problema: "Table 'medicamentos' doesn't exist"

**Solución:** Ejecutar script de migración

```bash
python migracion_mis_hijos.py
```

### Problema: "Module not found: medicamentos"

**Solución:** Agregar a `app/models/__init__.py`:

```python
from app.models.medicamentos import Medicamento, Alergia
```

### Problema: "Current user is not a padre"

**Solución:** Verificar que el usuario tenga rol_id = 4 (Padre)

### Problema: "Hijo no encontrado"

**Solución:** El niño debe estar asociado al padre (tutor_id correcto)

---

## 📊 Campos Calculados

El backend calcula automáticamente:

1. **edad**: A partir de `fecha_nacimiento`

   ```python
   edad = hoy.year - nacimiento.year
   ```

2. **cuatrimestre**: A partir de `fecha_registro`

   ```python
   meses = (ahora - fecha_registro).days // 30
   cuatrimestre = max(1, (meses // 4) + 1)
   ```

3. **novedades**: Cuenta de medicamentos con `novedadReciente=True`

---

## 🔄 Flujo de Datos

```
Frontend (Angular)
    ↓
  [mis-hijos.component.ts]
    ↓
  [PadresService.getMisHijos()]
    ↓
  GET /api/v1/padres/mis-hijos
    ↓
Backend FastAPI
    ↓
  [AuthGuard + RoleGuard] → Verifica usuario padre
    ↓
  [obtener_mis_hijos()] → Service
    ↓
  [Query: Nino + Medicamento + Alergia]
    ↓
  [Mapeo a Response DTOs]
    ↓
  [JSON Response]
    ↓
Frontend (Renderiza en HTML)
```

---

## 📚 Documentación Adicional

- **Frontend:** `src/app/padres/mis-hijos/README.md`
- **Interfaces:** `src/app/padres/padres.interfaces.ts`
- **Servicio:** `src/app/padres/padres.service.ts`

---

## 🎯 Próximos Pasos

1. ✅ Ejecutar migración de BD
2. ✅ Iniciar backend (`python run_server.py`)
3. ✅ Iniciar frontend (`ng serve`)
4. ✅ Login como padre
5. ✅ Navegar a `/padre/mis-hijos`
6. ✅ Ver lista de hijos con información completa

---

## 📞 Soporte

Si hay errores:

1. Revisar logs del backend (terminal)
2. Verificar consola del navegador (F12)
3. Confirmar que tablas existen en BD
4. Validar token JWT

---

**Estado:** ✅ COMPLETO Y LISTO PARA USAR
**Fecha:** 2026-01-12
**Versión:** 1.0

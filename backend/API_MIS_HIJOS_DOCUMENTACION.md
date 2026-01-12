# 📚 API Documentation - Módulo Mis Hijos para Padres

## 🎯 Descripción General

Este módulo proporciona endpoints RESTful para que los padres/tutores accedan a la información clínica y administrativa de sus hijos en el sistema.

## 🔐 Autenticación

Todos los endpoints requieren autenticación JWT Bearer token:

```http
Authorization: Bearer <JWT_TOKEN>
```

El token debe corresponder a un usuario con rol de padre/tutor. El sistema verifica:
- Token JWT válido
- Usuario existe en la base de datos
- Usuario está activo
- Usuario tiene relación tutor con los niños solicitados

## 📋 Endpoints Disponibles

### 1. Obtener Lista de Hijos

Obtiene todos los hijos asociados al padre autenticado.

**Endpoint:** `GET /api/v1/padres/mis-hijos`

**Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "exito": true,
  "datos": {
    "hijos": [
      {
        "id": 1,
        "nombre": "Juan",
        "apellidoPaterno": "Pérez",
        "apellidoMaterno": "García",
        "foto": "http://example.com/foto.jpg",
        "fechaNacimiento": "2015-05-15",
        "edad": 8,
        "diagnostico": "Trastorno del Espectro Autista",
        "cuatrimestre": 2,
        "fechaIngreso": "2023-01-15",
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
            "fechaInicio": "2024-01-01",
            "fechaFin": null,
            "activo": true,
            "novedadReciente": true,
            "fechaActualizacion": "2024-01-10T10:30:00"
          }
        ],
        "visto": false,
        "novedades": 1
      }
    ]
  },
  "mensaje": "Se encontraron 1 hijo(s)"
}
```

**Respuesta de Error:**
```json
{
  "exito": false,
  "error": "Tutor no encontrado"
}
```

---

### 2. Obtener Detalles de un Hijo

Obtiene los detalles completos de un hijo específico.

**Endpoint:** `GET /api/v1/padres/mis-hijos/{nino_id}`

**Parámetros de Ruta:**
- `nino_id` (int): ID del niño

**Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "exito": true,
  "datos": {
    "hijos": [
      {
        "id": 1,
        "nombre": "Juan",
        "apellidoPaterno": "Pérez",
        "apellidoMaterno": "García",
        "foto": "http://example.com/foto.jpg",
        "fechaNacimiento": "2015-05-15",
        "edad": 8,
        "diagnostico": "Trastorno del Espectro Autista",
        "cuatrimestre": 2,
        "fechaIngreso": "2023-01-15",
        "alergias": [...],
        "medicamentos": [...],
        "visto": false,
        "novedades": 1
      }
    ]
  }
}
```

**Validaciones:**
- El padre solo puede ver sus propios hijos
- El hijo debe existir y estar activo

---

### 3. Obtener Medicamentos de un Hijo

Obtiene todos los medicamentos de un hijo específico.

**Endpoint:** `GET /api/v1/padres/mis-hijos/{nino_id}/medicamentos`

**Parámetros de Ruta:**
- `nino_id` (int): ID del niño

**Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "exito": true,
  "datos": {
    "medicamentos": [
      {
        "id": 1,
        "nombre": "Metilfenidato",
        "dosis": "10 mg",
        "frecuencia": "Dos veces al día",
        "razon": "TDAH",
        "fechaInicio": "2024-01-01",
        "fechaFin": null,
        "activo": true,
        "novedadReciente": true,
        "fechaActualizacion": "2024-01-10T10:30:00"
      },
      {
        "id": 2,
        "nombre": "Fluoxetina",
        "dosis": "20 mg",
        "frecuencia": "Una vez al día",
        "razon": "Ansiedad",
        "fechaInicio": "2023-06-15",
        "fechaFin": null,
        "activo": true,
        "novedadReciente": false,
        "fechaActualizacion": "2023-06-15T08:00:00"
      }
    ]
  }
}
```

**Validaciones:**
- El padre solo puede ver medicamentos de sus propios hijos
- Los medicamentos están ordenados por activo (primero) y fecha de actualización (más reciente primero)

---

### 4. Obtener Alergias de un Hijo

Obtiene todas las alergias de un hijo específico.

**Endpoint:** `GET /api/v1/padres/mis-hijos/{nino_id}/alergias`

**Parámetros de Ruta:**
- `nino_id` (int): ID del niño

**Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "exito": true,
  "datos": {
    "alergias": [
      {
        "id": 1,
        "nombre": "Penicilina",
        "severidad": "severa",
        "reaccion": "Anafilaxia"
      },
      {
        "id": 2,
        "nombre": "Maní",
        "severidad": "moderada",
        "reaccion": "Picazón en la boca, hinchazón de labios"
      }
    ]
  }
}
```

**Valores de Severidad:**
- `leve`: Reacción leve, no requiere atención inmediata
- `moderada`: Reacción moderada, requiere monitoreo
- `severa`: Reacción severa, requiere atención médica inmediata

**Validaciones:**
- El padre solo puede ver alergias de sus propios hijos

---

### 5. Marcar Medicamento como Visto

Marca un medicamento como visto, quitando el badge de "novedad".

**Endpoint:** `PUT /api/v1/padres/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto`

**Parámetros de Ruta:**
- `nino_id` (int): ID del niño
- `medicamento_id` (int): ID del medicamento

**Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Respuesta Exitosa (200 OK):**
```json
{
  "exito": true,
  "mensaje": "Medicamento marcado como visto"
}
```

**Efecto:**
- El campo `novedadReciente` del medicamento se establece en `false`
- El badge "🆕 Actualizado recientemente" ya no se mostrará en el frontend
- El contador de novedades del hijo se actualiza automáticamente

**Validaciones:**
- El padre solo puede marcar como vistos medicamentos de sus propios hijos
- El medicamento debe existir

---

## 🔒 Seguridad

### Autenticación
- Todos los endpoints requieren JWT Bearer token válido
- El token debe contener el ID del usuario en el campo `sub`
- El token debe estar firmado con la clave secreta configurada

### Autorización
- Los padres solo pueden acceder a información de sus propios hijos
- La validación se hace a nivel de tutor_id
- Cualquier intento de acceder a hijos de otro padre resultará en error

### Validación de Datos
- Todos los datos de entrada son validados por Pydantic
- Los IDs deben ser enteros positivos
- Las fechas deben estar en formato ISO 8601

### Protección contra SQL Injection
- Se utiliza SQLAlchemy ORM
- Todos los queries son parametrizados
- No se construyen queries SQL manualmente

---

## 📊 Modelos de Base de Datos

### Tabla: `ninos`
```sql
CREATE TABLE ninos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(60) NOT NULL,
    apellido_materno VARCHAR(60),
    fecha_nacimiento DATE NOT NULL,
    sexo VARCHAR(1) NOT NULL,
    curp VARCHAR(18) UNIQUE,
    tutor_id INT,
    estado VARCHAR(20) DEFAULT 'ACTIVO',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tutor_id) REFERENCES tutores(id)
);
```

### Tabla: `medicamentos`
```sql
CREATE TABLE medicamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nino_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    frecuencia VARCHAR(100) NOT NULL,
    razon VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    activo BOOLEAN DEFAULT TRUE,
    novedadReciente BOOLEAN DEFAULT FALSE,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    actualizado_por VARCHAR(100),
    notas TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE
);
```

### Tabla: `alergias`
```sql
CREATE TABLE alergias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nino_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    severidad ENUM('leve', 'moderada', 'severa') NOT NULL DEFAULT 'leve',
    reaccion TEXT NOT NULL,
    tratamiento TEXT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE
);
```

### Tabla: `tutores`
```sql
CREATE TABLE tutores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    ocupacion VARCHAR(120),
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

---

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

Editar `backend/.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=autismo_mochis_ia
```

### 3. Ejecutar Migración

```bash
cd backend
python migracion_mis_hijos.py
```

### 4. Iniciar Servidor

```bash
python run_server.py
```

El servidor estará disponible en: `http://localhost:8000`

---

## 🧪 Testing

### Ejecutar Tests Unitarios

```bash
cd backend
python test_mis_hijos_api.py
```

### Probar Endpoints con cURL

```bash
# Obtener lista de hijos
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# Obtener detalles de un hijo
curl -X GET "http://localhost:8000/api/v1/padres/mis-hijos/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# Marcar medicamento como visto
curl -X PUT "http://localhost:8000/api/v1/padres/mis-hijos/1/medicamentos/1/visto" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 📝 Notas de Desarrollo

### Arquitectura
- **Framework:** FastAPI 0.110.0+
- **ORM:** SQLAlchemy 2.0+
- **Base de Datos:** MySQL/MariaDB
- **Autenticación:** JWT (PyJWT)
- **Validación:** Pydantic

### Estructura de Archivos
```
backend/
├── app/
│   ├── api/v1/padres/
│   │   ├── __init__.py
│   │   ├── inicio.py
│   │   └── mis_hijos.py          # Endpoints
│   ├── models/
│   │   ├── nino.py                # Modelo Nino
│   │   ├── medicamentos.py        # Modelos Medicamento y Alergia
│   │   └── tutor.py               # Modelo Tutor
│   ├── schemas/
│   │   └── padres_mis_hijos.py    # DTOs Pydantic
│   ├── services/
│   │   └── padres_mis_hijos_service.py  # Lógica de negocio
│   └── core/
│       ├── config.py              # Configuración
│       └── database.py            # Conexión DB
├── migracion_mis_hijos.py         # Script de migración
└── test_mis_hijos_api.py          # Tests
```

### Convenciones
- Nombres de tablas en plural minúsculas: `ninos`, `medicamentos`, `alergias`
- Nombres de modelos en singular CamelCase: `Nino`, `Medicamento`, `Alergia`
- Endpoints REST siguiendo convenciones de FastAPI
- Respuestas siempre en formato JSON con estructura consistente

---

## 🐛 Troubleshooting

### Error: "Tutor no encontrado"
- Verificar que el usuario tenga un registro en la tabla `tutores`
- Verificar que `tutores.usuario_id` coincida con el ID del usuario autenticado

### Error: "Hijo no encontrado"
- Verificar que el hijo exista en la base de datos
- Verificar que `ninos.tutor_id` apunte al tutor correcto
- Verificar que el estado del hijo sea "ACTIVO"

### Error: "Invalid token"
- Verificar que el token JWT sea válido
- Verificar que el token no haya expirado
- Verificar que JWT_SECRET_KEY en la configuración sea correcta

---

## 📞 Soporte

Para reportar problemas o solicitar nuevas funcionalidades, contactar al equipo de desarrollo.

---

**Versión:** 1.0  
**Última actualización:** 2026-01-12  
**Estado:** ✅ Producción Ready

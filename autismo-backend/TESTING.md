# 🧪 Guía de Pruebas Rápidas - Endpoints Usuarios y Roles

## 📋 Pre-requisitos

1. **Backend ejecutándose:**
   ```powershell
   .\start_backend.ps1
   # O manualmente:
   uvicorn app.main:app --reload
   ```

2. **Base de datos inicializada:**
   ```powershell
   cd scripts
   python init_database.py
   ```

3. **Swagger UI abierto:**
   - URL: http://localhost:8000/api/docs

---

## 🔐 Paso 1: Autenticación

### Login como ADMIN

**Endpoint:** `POST /api/v1/auth/login`

**Body:**
```json
{
  "email": "admin@demo.com",
  "password": "12345678"
}
```

**Respuesta esperada:**
```json
{
  "token": {
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
  },
  "user": {
    "id": 1,
    "nombres": "Ana",
    "apellido_paterno": "Ramírez",
    "email": "admin@demo.com",
    "rol_id": 1,
    "rol_nombre": "ADMIN",
    "permisos": ["usuarios:ver", "usuarios:crear", ...]
  }
}
```

**✅ Copiar el `access_token` para los siguientes pasos**

---

## 🔑 Paso 2: Autorizar en Swagger

1. Click en el botón **"Authorize"** (candado verde) en la parte superior derecha de Swagger
2. Pegar el token en el campo "Value" (sin comillas, sin "Bearer ")
3. Click en **"Authorize"** y luego **"Close"**

**Nota:** Ahora todos los endpoints protegidos funcionarán con tu sesión de ADMIN

---

## 👥 Paso 3: Probar Endpoints de Usuarios

### 3.1 Listar Usuarios

**Endpoint:** `GET /api/v1/usuarios`

**Query params (opcionales):**
- skip: 0
- limit: 100
- search: "" (vacío)
- rol_id: null
- activo: null

**Click en "Try it out" → "Execute"**

**Respuesta esperada:**
```json
{
  "items": [
    {
      "id": 1,
      "nombres": "Ana",
      "apellido_paterno": "Ramírez",
      "email": "admin@demo.com",
      "rol_nombre": "ADMIN",
      "activo": 1,
      ...
    },
    ...
  ],
  "total": 4,
  "skip": 0,
  "limit": 100
}
```

---

### 3.2 Crear Usuario

**Endpoint:** `POST /api/v1/usuarios`

**Body:**
```json
{
  "nombres": "Pedro",
  "apellido_paterno": "González",
  "apellido_materno": "Muñoz",
  "email": "pedro.gonzalez@test.com",
  "telefono": "6671234567",
  "password": "password123",
  "rol_id": 3
}
```

**Respuesta esperada (Status 201):**
```json
{
  "id": 5,
  "nombres": "Pedro",
  "apellido_paterno": "González",
  "email": "pedro.gonzalez@test.com",
  "rol_id": 3,
  "rol_nombre": "TERAPEUTA",
  "activo": 1,
  ...
}
```

**✅ Copiar el `id` del usuario creado**

---

### 3.3 Obtener Usuario por ID

**Endpoint:** `GET /api/v1/usuarios/{usuario_id}`

**Path param:**
- usuario_id: 5 (el ID del usuario recién creado)

**Respuesta esperada:**
```json
{
  "id": 5,
  "nombres": "Pedro",
  "apellido_paterno": "González",
  "email": "pedro.gonzalez@test.com",
  "rol_nombre": "TERAPEUTA",
  ...
}
```

---

### 3.4 Actualizar Usuario

**Endpoint:** `PUT /api/v1/usuarios/{usuario_id}`

**Path param:**
- usuario_id: 5

**Body (solo campos a actualizar):**
```json
{
  "telefono": "6679876543",
  "apellido_materno": "López"
}
```

**Respuesta esperada:**
```json
{
  "id": 5,
  "telefono": "6679876543",
  "apellido_materno": "López",
  ...
}
```

---

### 3.5 Toggle Activo/Inactivo

**Endpoint:** `PATCH /api/v1/usuarios/{usuario_id}/toggle-activo`

**Path param:**
- usuario_id: 5

**Respuesta esperada:**
```json
{
  "id": 5,
  "activo": 0,  // Cambió de 1 a 0
  ...
}
```

**Ejecutar de nuevo para reactivar (activo: 1)**

---

### 3.6 Filtros de Búsqueda

**Endpoint:** `GET /api/v1/usuarios`

**Query params:**
```
search: pedro
rol_id: 3
activo: 1
```

**Respuesta:** Solo usuarios que coincidan con los filtros

---

### 3.7 Eliminar Usuario (Soft Delete)

**Endpoint:** `DELETE /api/v1/usuarios/{usuario_id}`

**Path param:**
- usuario_id: 5

**Respuesta esperada (Status 204):**
- Sin contenido (el usuario se marcó como inactivo)

**Verificar:** Hacer GET del usuario, debería tener `activo: 0`

---

## 🛡️ Paso 4: Probar Endpoints de Roles

### 4.1 Listar Roles

**Endpoint:** `GET /api/v1/roles`

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "nombre": "ADMIN",
    "descripcion": "Administrador del sistema con acceso total"
  },
  {
    "id": 2,
    "nombre": "COORDINADOR",
    "descripcion": "Coordinador del centro de terapias"
  },
  ...
]
```

---

### 4.2 Obtener Rol con Permisos

**Endpoint:** `GET /api/v1/roles/{rol_id}`

**Path param:**
- rol_id: 1 (ADMIN)

**Respuesta esperada:**
```json
{
  "id": 1,
  "nombre": "ADMIN",
  "descripcion": "Administrador del sistema con acceso total",
  "permisos": [
    {
      "id": 1,
      "codigo": "usuarios:ver",
      "descripcion": "Ver listado de usuarios"
    },
    {
      "id": 2,
      "codigo": "usuarios:crear",
      "descripcion": "Crear nuevos usuarios"
    },
    ...
  ]
}
```

---

### 4.3 Listar Todos los Permisos

**Endpoint:** `GET /api/v1/permisos`

**Respuesta esperada:**
```json
[
  {
    "id": 1,
    "codigo": "usuarios:ver",
    "descripcion": "Ver listado de usuarios"
  },
  {
    "id": 2,
    "codigo": "usuarios:crear",
    "descripcion": "Crear nuevos usuarios"
  },
  ...
]
```

**✅ Copiar algunos IDs de permisos para el siguiente paso**

---

### 4.4 Crear Nuevo Rol

**Endpoint:** `POST /api/v1/roles`

**Body:**
```json
{
  "nombre": "SUPERVISOR",
  "descripcion": "Supervisor con permisos limitados"
}
```

**Respuesta esperada (Status 201):**
```json
{
  "id": 5,
  "nombre": "SUPERVISOR",
  "descripcion": "Supervisor con permisos limitados"
}
```

**✅ Copiar el `id` del rol creado**

---

### 4.5 Asignar Permisos a Rol

**Endpoint:** `POST /api/v1/roles/{rol_id}/permisos`

**Path param:**
- rol_id: 5 (el rol SUPERVISOR recién creado)

**Body:**
```json
{
  "permiso_ids": [1, 7, 11, 21]
}
```

**Respuesta esperada:**
```json
{
  "id": 5,
  "nombre": "SUPERVISOR",
  "descripcion": "Supervisor con permisos limitados",
  "permisos": [
    {
      "id": 1,
      "codigo": "usuarios:ver",
      "descripcion": "Ver listado de usuarios"
    },
    ...
  ]
}
```

---

### 4.6 Actualizar Rol

**Endpoint:** `PUT /api/v1/roles/{rol_id}`

**Path param:**
- rol_id: 5

**Body:**
```json
{
  "descripcion": "Supervisor de operaciones diarias"
}
```

**Respuesta esperada:**
```json
{
  "id": 5,
  "nombre": "SUPERVISOR",
  "descripcion": "Supervisor de operaciones diarias"
}
```

---

## 🧪 Paso 5: Probar Validaciones y Errores

### 5.1 Email Duplicado

**Endpoint:** `POST /api/v1/usuarios`

**Body:**
```json
{
  "nombres": "Test",
  "apellido_paterno": "User",
  "email": "admin@demo.com",  // Email ya existe
  "password": "12345678",
  "rol_id": 2
}
```

**Respuesta esperada (Status 400):**
```json
{
  "detail": "El email admin@demo.com ya está registrado"
}
```

---

### 5.2 Rol Inválido

**Endpoint:** `POST /api/v1/usuarios`

**Body:**
```json
{
  "nombres": "Test",
  "apellido_paterno": "User",
  "email": "nuevo@test.com",
  "password": "12345678",
  "rol_id": 999  // Rol no existe
}
```

**Respuesta esperada (Status 400):**
```json
{
  "detail": "El rol con ID 999 no existe"
}
```

---

### 5.3 Usuario No Encontrado

**Endpoint:** `GET /api/v1/usuarios/9999`

**Respuesta esperada (Status 404):**
```json
{
  "detail": "Usuario con ID 9999 no encontrado"
}
```

---

### 5.4 Auto-eliminación Prohibida

**Endpoint:** `DELETE /api/v1/usuarios/1`

*(Intentar eliminar tu propio usuario estando logueado como admin@demo.com con ID 1)*

**Respuesta esperada (Status 400):**
```json
{
  "detail": "No puedes eliminarte a ti mismo"
}
```

---

## 🎯 Paso 6: Probar Permisos (Opcional)

### 6.1 Login como PADRE

**Endpoint:** `POST /api/v1/auth/login`

**Body:**
```json
{
  "email": "padre@demo.com",
  "password": "12345678"
}
```

### 6.2 Intentar Crear Usuario

**Endpoint:** `POST /api/v1/usuarios`

*(Sin cambiar el token, intentar crear usuario)*

**Respuesta esperada (Status 403):**
```json
{
  "detail": "Permisos insuficientes: se requiere ['usuarios:crear']"
}
```

**✅ El sistema de permisos funciona correctamente!**

---

## ✅ Checklist de Pruebas

- [ ] Login exitoso como ADMIN
- [ ] Listar usuarios con paginación
- [ ] Crear nuevo usuario
- [ ] Obtener usuario por ID
- [ ] Actualizar usuario
- [ ] Toggle activo/inactivo
- [ ] Buscar usuarios con filtros
- [ ] Eliminar usuario (soft delete)
- [ ] Listar roles
- [ ] Obtener rol con permisos
- [ ] Listar todos los permisos
- [ ] Crear nuevo rol
- [ ] Asignar permisos a rol
- [ ] Actualizar rol
- [ ] Validar email duplicado (error)
- [ ] Validar rol inválido (error)
- [ ] Validar usuario no encontrado (error)
- [ ] Validar auto-eliminación prohibida (error)
- [ ] Probar acceso sin permisos (error 403)

---

## 🐛 Troubleshooting

### Error: "Not authenticated"
- Verifica que hiciste login y copiaste el token
- Asegúrate de autorizar en Swagger con el token

### Error: "Database error"
- Verifica que MySQL está corriendo
- Confirma que ejecutaste `init_database.py`
- Revisa las credenciales en `.env`

### Error: "Module not found"
- Verifica que instalaste las dependencias: `pip install -r requirements.txt`

### Servidor no inicia
- Verifica puerto 8000 disponible
- Revisa logs en la terminal
- Confirma que `.env` existe y está configurado

---

## 📊 Métricas de Éxito

Si completaste todas las pruebas exitosamente:

✅ **Sistema de autenticación funcionando**  
✅ **CRUD de usuarios operativo**  
✅ **Sistema de roles y permisos funcionando**  
✅ **Validaciones de negocio implementadas**  
✅ **Manejo de errores correcto**  
✅ **Paginación y filtros operativos**  

**🎉 ¡Backend de Usuarios/Roles completamente funcional!**

---

## 🚀 Módulos Adicionales Completados

### ✅ Personal (Terapeutas) - 10 endpoints
- CRUD completo
- Gestión de perfiles profesionales
- Horarios de disponibilidad

### ✅ Tutores (Padres) - 9 endpoints
- CRUD completo
- Relación con niños
- Verificación de accesos

### ✅ Niños (Beneficiados) - 20 endpoints
- CRUD base + 4 tablas relacionadas
- Direcciones, diagnósticos, info emocional, archivos

### ✅ Terapias - 25 endpoints
- CRUD terapias
- Asignaciones (personal/niños)
- Sesiones y reposiciones

### ✅ Citas - 10 endpoints
- Programación con detección de conflictos
- Marcar asistencia/cancelar

### ✅ Recursos - 9 endpoints
- Biblioteca educativa
- Asignación como tareas

### ✅ Notificaciones - 6 endpoints
- Sistema de alertas por usuario

### ✅ TOPSIS - 4 endpoints
- Algoritmo de priorización multi-criterio

### ✅ IA Gemini - 4 endpoints
- Análisis y recomendaciones inteligentes

---

## 📊 BACKEND 100% COMPLETADO

**Total:** 109+ endpoints REST funcionando ✅

**Ver documentación completa:** `COMPLETADO.md`

**Swagger UI:** http://localhost:8000/api/docs

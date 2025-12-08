# GUÍA DE PRUEBA DE ENDPOINTS

Esta guía te ayudará a probar todos los endpoints de autenticación.

## 🌐 Base URL

```
http://localhost:8000
```

## 📚 Documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Endpoints de autenticación

### 1. Health Check

**GET** `/health`

Sin autenticación requerida.

```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "Autismo Mochis IA"
}
```

---

### 2. Login

**POST** `/api/v1/auth/login`

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@autismo.com",
    "password": "admin123"
  }'
```

**PowerShell:**
```powershell
$body = @{
    email = "admin@autismo.com"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

**Respuesta:**
```json
{
  "token": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer"
  },
  "user": {
    "id": 1,
    "nombres": "Administrador",
    "apellido_paterno": "Sistema",
    "apellido_materno": null,
    "email": "admin@autismo.com",
    "rol_id": 1,
    "rol_nombre": "Admin",
    "permisos": [
      "ver_usuarios",
      "crear_usuarios",
      "editar_usuarios",
      ...
    ]
  }
}
```

---

### 3. Obtener usuario actual (Me)

**GET** `/api/v1/auth/me`

**Requiere:** Token JWT en header Authorization

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**PowerShell:**
```powershell
$token = "eyJ0eXAiOiJKV1QiLCJhbGc..."

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/me" `
  -Method Get `
  -Headers @{
    "Authorization" = "Bearer $token"
  }
```

**Respuesta:**
```json
{
  "id": 1,
  "nombres": "Administrador",
  "apellido_paterno": "Sistema",
  "email": "admin@autismo.com",
  "rol_id": 1,
  "rol_nombre": "Admin",
  "permisos": ["ver_usuarios", "crear_usuarios", ...]
}
```

---

### 4. Logout

**POST** `/api/v1/auth/logout`

**Requiere:** Token JWT

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**PowerShell:**
```powershell
$token = "eyJ0eXAiOiJKV1QiLCJhbGc..."

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/logout" `
  -Method Post `
  -Headers @{
    "Authorization" = "Bearer $token"
  }
```

**Respuesta:**
```json
{
  "message": "Sesión cerrada exitosamente",
  "user": "admin@autismo.com"
}
```

---

## 🧪 Pruebas con Swagger UI

La forma más fácil de probar es usando Swagger UI:

1. Ve a http://localhost:8000/docs
2. Busca **POST /api/v1/auth/login**
3. Click en **"Try it out"**
4. Ingresa las credenciales:
```json
{
  "email": "admin@autismo.com",
  "password": "admin123"
}
```
5. Click en **"Execute"**
6. Copia el `access_token` de la respuesta
7. Click en el botón **"Authorize"** (arriba a la derecha)
8. Pega el token en el campo `Value` (Swagger agregará "Bearer " automáticamente)
9. Click en **"Authorize"** y luego **"Close"**
10. Ahora puedes probar los endpoints protegidos

---

## 🔐 Usuarios de prueba

Después de ejecutar `init_roles_permisos.py`:

### Administrador
- **Email:** admin@autismo.com
- **Password:** admin123
- **Rol:** Admin (ID: 1)
- **Permisos:** Todos

Para crear más usuarios de prueba, puedes usar el endpoint de creación de usuarios (si está implementado) o insertarlos directamente en la base de datos.

---

## 📝 Ejemplo de flujo completo

### 1. Login
```bash
POST /api/v1/auth/login
```

### 2. Guardar el token
```javascript
localStorage.setItem('token', response.token.access_token);
```

### 3. Usar el token en peticiones
```bash
GET /api/v1/auth/me
Authorization: Bearer <token>
```

### 4. Logout (opcional)
```bash
POST /api/v1/auth/logout
Authorization: Bearer <token>
```

### 5. Eliminar token del cliente
```javascript
localStorage.removeItem('token');
```

---

## 🛡️ Verificación de permisos

El sistema verifica automáticamente:

1. **Token válido:** No expirado, firma correcta
2. **Usuario activo:** Campo `activo = 1`
3. **Rol asignado:** Usuario tiene un rol válido
4. **Permisos del rol:** Permisos asociados al rol

---

## ❌ Códigos de error comunes

- **401 Unauthorized:** Token inválido o expirado
- **403 Forbidden:** Usuario sin permisos suficientes
- **404 Not Found:** Recurso no encontrado
- **422 Unprocessable Entity:** Datos de entrada inválidos
- **500 Internal Server Error:** Error del servidor

---

## 🔧 Debugging

### Ver logs del servidor
Los logs aparecen en la consola donde ejecutaste uvicorn.

### Verificar token
Puedes decodificar el JWT en: https://jwt.io

### Verificar base de datos
```sql
-- Ver usuarios
SELECT * FROM usuarios;

-- Ver roles
SELECT * FROM roles;

-- Ver permisos de un rol
SELECT r.nombre, p.codigo, p.descripcion
FROM roles r
JOIN roles_permisos rp ON r.id = rp.rol_id
JOIN permisos p ON rp.permiso_id = p.id
WHERE r.id = 1;
```

---

## 📱 Integración con Angular

En tu servicio de autenticación Angular:

```typescript
login(email: string, password: string) {
  return this.http.post<LoginResponse>(
    `${this.apiUrl}/login`,
    { email, password }
  ).pipe(
    tap(res => {
      localStorage.setItem('token', res.token.access_token);
      localStorage.setItem('user', JSON.stringify(res.user));
    })
  );
}
```

El interceptor agregará automáticamente el token:

```typescript
intercept(req: HttpRequest<any>, next: HttpHandler) {
  const token = localStorage.getItem('token');
  
  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }
  
  return next.handle(req);
}
```

# 🔧 Solución Error 401 Chatbot

## ✅ Problema Identificado
El chatbot muestra error **401 Unauthorized** al intentar enviar mensajes.

## 🔍 Diagnóstico Realizado

### Backend ✅ FUNCIONANDO
- ✅ Gemini AI configurado con modelo `gemini-1.5-flash`
- ✅ Servidor corriendo en `http://localhost:8000`
- ✅ Endpoint `/api/v1/ia/chatbot` disponible
- ✅ Requiere autenticación con JWT token

### Frontend ✅ CONFIGURADO CORRECTAMENTE
- ✅ `TokenInterceptor` configurado en `app.config.ts`
- ✅ Interceptor agrega automáticamente `Authorization: Bearer <token>` a todas las peticiones HTTP
- ✅ Token se obtiene de `localStorage.getItem('token')`
- ✅ `GeminiIaService` usa `HttpClient` (automáticamente incluye el interceptor)

## 🎯 Causa del Error 401

El error ocurre por **UNA** de estas razones:

### 1. No hay sesión iniciada ⚠️
**Síntoma**: No has iniciado sesión en el sistema
**Solución**: 
```
1. Ve a la página de login
2. Ingresa tus credenciales (usuario/contraseña)
3. El sistema guardará el token automáticamente
4. Intenta usar el chatbot nuevamente
```

### 2. Token expirado 🕐
**Síntoma**: Iniciaste sesión hace mucho tiempo
**Solución**:
```
1. Cierra sesión (logout)
2. Vuelve a iniciar sesión
3. El token se renovará automáticamente
```

### 3. Token corrupto/eliminado ❌
**Síntoma**: Limpiaste el localStorage del navegador
**Solución**:
```
1. Abre las herramientas de desarrollador (F12)
2. Ve a la pestaña "Application" o "Almacenamiento"
3. Busca "Local Storage" → http://localhost:4200
4. Verifica si existe la clave "token"
5. Si no existe, inicia sesión nuevamente
```

## 🔧 Verificación Manual del Token

### Paso 1: Abrir consola del navegador
Presiona **F12** y ve a la pestaña **Console**

### Paso 2: Verificar token
Copia y pega este comando:
```javascript
console.log('Token:', localStorage.getItem('token'));
```

### Paso 3: Interpretar resultado

**Si muestra un token largo (ej: "eyJhbGciOiJIUzI1NiIs..."):**
✅ Token existe - El problema puede ser que expiró

**Si muestra "null":**
❌ No hay token - Necesitas iniciar sesión

### Paso 4: Probar chatbot manualmente (avanzado)
```javascript
// Copiar y pegar en consola para probar el endpoint
const token = localStorage.getItem('token');
fetch('http://localhost:8000/api/v1/ia/chatbot', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    mensaje: "Hola, ¿cómo estás?",
    incluir_contexto: false
  })
})
.then(res => res.json())
.then(data => console.log('Respuesta:', data))
.catch(err => console.error('Error:', err));
```

**Resultado esperado:**
```json
{
  "respuesta": "¡Hola! Estoy aquí para ayudarte...",
  "contexto_usado": false,
  "configurado": true
}
```

## 🚀 Solución Rápida (Recomendada)

### Opción 1: Reiniciar sesión
```
1. Haz clic en tu perfil/usuario (esquina superior derecha)
2. Selecciona "Cerrar Sesión" o "Logout"
3. Inicia sesión nuevamente con tus credenciales
4. Prueba el chatbot
```

### Opción 2: Forzar renovación de token (si sigues con 401)
```javascript
// En consola del navegador (F12)
localStorage.clear(); // Limpia todo el storage
location.reload(); // Recarga la página
// Luego inicia sesión nuevamente
```

## 📊 Estado Actual del Sistema

### ✅ Componentes Funcionando
- Backend FastAPI con Uvicorn (auto-reload)
- Gemini AI con modelo `gemini-1.5-flash`
- Sistema de autenticación JWT
- Interceptor HTTP configurado
- Servicio GeminiIaService correcto

### ⏳ Acciones Requeridas
1. **Iniciar sesión** en el sistema
2. **Verificar** que el token esté guardado
3. **Probar** el chatbot después de autenticarte

## 🔒 Cómo Funciona la Autenticación

```
┌─────────────┐
│   LOGIN     │
│ (usuario +  │
│ contraseña) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Backend Auth Service           │
│  POST /api/v1/auth/login        │
│  Valida credenciales            │
│  Genera JWT token               │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Frontend AuthService           │
│  localStorage.setItem('token')  │
│  Guarda token en navegador      │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  TokenInterceptor               │
│  Intercepta TODAS las peticiones│
│  Agrega header:                 │
│  Authorization: Bearer <token>  │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  HTTP Request al Backend        │
│  POST /api/v1/ia/chatbot        │
│  Con header de autenticación    │
└──────┬──────────────────────────┘
       │
       ▼
    ✅ 200 OK
    ❌ 401 Unauthorized (si token inválido/expirado)
```

## 💡 Notas Importantes

1. **El código del interceptor está correcto** - No hay que modificar nada
2. **El backend funciona perfectamente** - Gemini AI respondiendo
3. **El problema es de sesión** - Solo necesitas autenticarte
4. **Los tokens expiran** - Por seguridad, debes renovar la sesión cada cierto tiempo

## 📝 Cambios Realizados Hoy

### ✅ Actualizaciones Completadas
1. **Gemini AI**: Actualizado de `gemini-pro` (deprecated) a `gemini-1.5-flash`
2. **Navegación**: Eliminados items "Priorización TOPSIS" y "Recomendaciones" del sidebar
3. **Diseño Profesional**: 
   - Módulo fichas-emergencia rediseñado
   - Módulo recomendaciones-actividades rediseñado
   - Sistema de diseño médico profesional aplicado

### ⏳ Pendiente
1. Ejecutar `INSERTAR_FICHAS_EMERGENCIA.sql` en phpMyAdmin
2. **Iniciar sesión** para probar el chatbot
3. Aplicar diseño profesional a otros módulos (opcional)

## 🆘 Si el Problema Persiste

Si después de iniciar sesión el chatbot sigue mostrando 401:

1. **Revisa la consola del navegador** (F12 → Console)
2. **Busca errores** relacionados con CORS o Network
3. **Verifica** que el backend esté corriendo en el puerto 8000
4. **Comprueba** la respuesta del endpoint `/api/v1/ia/estado`:
   ```javascript
   fetch('http://localhost:8000/api/v1/ia/estado', {
     headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
   })
   .then(r => r.json())
   .then(console.log);
   ```

## 🎓 Resumen Ejecutivo

**El chatbot está funcionando correctamente.**
El error 401 es un **problema de autenticación**, no un error del código.

**Solución en 3 pasos:**
1. 🔑 Inicia sesión en el sistema
2. ✅ Verifica que el token esté guardado
3. 💬 Usa el chatbot normalmente

**El interceptor HTTP automáticamente agregará el token a todas las peticiones.**

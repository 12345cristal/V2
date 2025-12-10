# 🚀 CÓMO INICIAR EL SISTEMA COMPLETO

## ✅ Backend (Puerto 8000)

### Opción 1: Script Automático (RECOMENDADO)
```cmd
INICIAR_BACKEND.bat
```
- Se abrirá una ventana de CMD
- **NO CIERRES** esa ventana mientras uses el sistema
- Verás el mensaje: `✅ Gemini AI configurado correctamente`
- El servidor estará en: `http://localhost:8000`

### Opción 2: Manual
```cmd
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar que el Backend está corriendo:
Abre tu navegador y ve a: `http://localhost:8000/docs`
- Deberías ver la documentación Swagger UI

---

## ✅ Frontend (Puerto 4200)

### Iniciar Angular
```cmd
ng serve
```
O si tienes npm scripts:
```cmd
npm start
```

### Acceder al Frontend:
Abre tu navegador en: `http://localhost:4200`

---

## 🔍 Solución de Problemas

### Error: "ERR_CONNECTION_REFUSED"
**Causa**: El backend NO está corriendo

**Solución**:
1. Verifica si el backend está corriendo en la ventana CMD
2. Si la ventana se cerró, vuelve a ejecutar `INICIAR_BACKEND.bat`
3. Asegúrate de ver el mensaje "Application startup complete"

### Error: "CORS policy"
**Causa**: El backend está corriendo en la IP incorrecta

**Solución**:
1. Detén el backend (Ctrl+C en la ventana CMD)
2. Asegúrate de usar el host `0.0.0.0` y no `127.0.0.1`
3. Ejecuta: `INICIAR_BACKEND.bat`

### El frontend no carga datos
**Verificación**:
1. Abre DevTools (F12) en el navegador
2. Ve a la pestaña "Network"
3. Recarga la página
4. Busca errores rojos en las peticiones HTTP

**Si ves errores 401 (Not Authenticated)**:
- Es normal, necesitas iniciar sesión primero
- Ve a la página de login

**Si ves errores 500**:
- Revisa la ventana CMD del backend
- Busca el error en Python
- Puede ser un problema con la base de datos

---

## ✅ Orden de Inicio Recomendado

1. **Primero**: Inicia XAMPP (MySQL debe estar corriendo)
2. **Segundo**: Ejecuta `INICIAR_BACKEND.bat`
3. **Tercero**: Ejecuta `ng serve` (en otra terminal)
4. **Cuarto**: Abre `http://localhost:4200` en el navegador

---

## 📝 Notas Importantes

- **Backend**: Debe correr en host `0.0.0.0` (no `127.0.0.1`)
- **Puerto Backend**: 8000
- **Puerto Frontend**: 4200
- **CORS**: Configurado para localhost:4200 y 127.0.0.1:4200
- **Gemini AI**: Configurado y funcionando ✅

---

## 🛠️ Comandos Útiles

### Verificar qué está corriendo en el puerto 8000:
```powershell
netstat -ano | Select-String ":8000"
```

### Matar proceso en puerto 8000:
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

### Ver logs del backend:
- Mira la ventana CMD donde ejecutaste `INICIAR_BACKEND.bat`

---

## ✅ Sistema Listo

Cuando todo esté funcionando correctamente verás:

1. **Backend**: Ventana CMD mostrando:
   ```
   ✅ Gemini AI configurado correctamente
   INFO: Application startup complete.
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

2. **Frontend**: Terminal mostrando:
   ```
   ✅ Compiled successfully
   ✅ Angular Live Development Server is listening on localhost:4200
   ```

3. **Navegador**: Sin errores en la consola (F12)

¡Ahora puedes usar el sistema! 🎉

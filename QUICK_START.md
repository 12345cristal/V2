# 🚀 QUICK START - SISTEMA CHATBOT IA

## 1️⃣ VERIFICAR DEPENDENCIAS

### Backend
```powershell
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend"
pip install -r requirements.txt
# Asegúrate que tenga: fastapi, uvicorn, sqlalchemy, pydantic, pydantic-settings, google-generativeai
```

### Frontend
```bash
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo"
npm install
# Debe estar @angular/common, @angular/core, @angular/forms instalados
```

---

## 2️⃣ CONFIGURAR VARIABLES DE AMBIENTE

### Backend (.env)

Crea archivo `.env` en `backend/`:

```
GEMINI_API_KEY=tu-api-key-de-gemini-aqui
GEMINI_MODEL=gemini-1.5-flash
DATABASE_URL=sqlite:///./test.db
BACKEND_CORS_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
JWT_SECRET_KEY=tu-secret-key-aqui
```

---

## 3️⃣ INICIAR BACKEND

### Opción A: Ejecución Simple
```powershell
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Opción B: Con recarga automática
```powershell
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Verifica que veas:**
```
✅ Gemini AI configurado con gemini-1.5-flash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

## 4️⃣ PROBAR BACKEND (OPCIONAL)

### En navegador
```
http://127.0.0.1:8000/docs
```

Prueba POST `/api/v1/ia/chatbot`:
```json
{
  "mensaje": "¿Cómo manejar rabietas en niños con autismo?",
  "incluir_contexto": false
}
```

Deberías recibir respuesta JSON con:
```json
{
  "respuesta": "Aquí hay estrategias...",
  "contexto_usado": false,
  "configurado": true,
  "session_id": "abc123..."
}
```

---

## 5️⃣ INICIAR FRONTEND

### En NUEVA terminal:

```bash
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo"
ng serve --proxy-config src/proxy.conf.json
```

O con npm start:
```bash
npm start -- --proxy-config src/proxy.conf.json
```

**Verifica que veas:**
```
✔ Compiled successfully.
⠙ Building...
Application bundle generation complete.
Watch mode enabled. Watching for file changes...
```

---

## 6️⃣ USAR LA APLICACIÓN

### En navegador
```
http://localhost:4200
```

1. Busca el botón flotante con ícono 🤖 (esquina inferior derecha)
2. Haz clic para abrir el chatbot
3. Escribe una pregunta:
   - "¿Cómo puedo mejorar la comunicación con mi hijo?"
   - "¿Qué actividades son recomendadas para TEA?"
   - "Consejos para establecer rutinas"
4. Presiona Enter o haz clic en enviar
5. **Deberías recibir respuesta sin errores CORS**

---

## ✅ CHECKLIST

Antes de empezar, verifica que:

- [ ] Backend en puerto 8000 ✓
- [ ] Frontend en puerto 4200 ✓
- [ ] `src/proxy.conf.json` existe ✓
- [ ] `app/main.py` importa `from app.api.v1.api import api_router` ✓
- [ ] `app/api/v1/api.py` importa endpoints chat y health ✓
- [ ] `app/services/gemini_client.py` existe ✓
- [ ] `app/db/base.py` existe ✓
- [ ] `ng serve` usa `--proxy-config src/proxy.conf.json` ✓

---

## 🔧 COMANDOS ÚTILES

### Ver qué procesos usan puerto 8000
```powershell
netstat -ano | findstr :8000
```

### Matar proceso
```powershell
taskkill /PID <PID> /F
```

### Ver logs del backend en tiempo real
```powershell
# Terminal donde corre uvicorn
# Verás logs como:
# [CHATBOT] 🔵 Iniciando consulta...
# [CHATBOT] ✅ Session ID: ...
```

### Ver logs del frontend
```
F12 → Console en navegador
```

### Limpiar caché del navegador
```
Ctrl+Shift+Delete → Clear browsing data
```

---

## 🐛 ERRORES COMUNES

### "CORS error" en navegador
**Causa:** No estás usando el proxy
**Solución:** 
```bash
# CORRECTO:
ng serve --proxy-config src/proxy.conf.json

# INCORRECTO:
ng serve  # (sin proxy)
```

### "ModuleNotFoundError: No module named 'app'"
**Causa:** No estás en el directorio backend
**Solución:**
```powershell
cd "c:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend"
```

### "Port 8000 in use"
**Causa:** Otro proceso usa el puerto
**Solución:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Gemini not configured"
**Causa:** GEMINI_API_KEY no está en .env o vacía
**Solución:**
```
Crear .env en backend/:
GEMINI_API_KEY=your-key-here
```

---

## 📊 ESTADO ESPERADO

Cuando todo está funcionando:

**Backend:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
[ESTADO] ✅ Configurado: True
```

**Frontend:**
```
✔ Compiled successfully.
 Application bundle generation complete.
 Watch mode enabled.
```

**Navegador:**
- Chatbot visible con botón flotante 🤖
- Mensajes aparecen sin retrasos
- Respuestas del servidor llegan rápidamente
- **CERO errores de CORS en console**

---

## 📞 SOPORTE

Si tienes problemas:

1. Verifica los logs del backend (terminal uvicorn)
2. Verifica la consola del navegador (F12)
3. Revisa que ambos procesos estén corriendo
4. Intenta refrescar la página (Ctrl+F5)
5. Intenta reiniciar ambos servidores

---

**¡Listo para empezar!** 🚀

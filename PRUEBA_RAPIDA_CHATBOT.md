# 🚀 PRUEBA RÁPIDA DEL CHATBOT

## En 3 Pasos

### Paso 1: Iniciar Backend
```bash
cd backend
./start.ps1
```
**Espera estos mensajes:**
```
✅ Gemini AI configurado con gemini-1.5-flash
✅ Tablas de chat verificadas/creadas
✅ Application startup complete
```

### Paso 2: Iniciar Frontend
En otra terminal:
```bash
npm start
```
**Espera:**
```
✅ Application bundle generation complete
➜ Local: http://localhost:4200 (o puerto mostrado)
```

### Paso 3: Prueba en Navegador
1. Ve a `http://localhost:4200`
2. Busca el **botón flotante** en la esquina **inferior derecha**
3. Haz clic
4. Escribe: `"¿Cuáles son las mejores actividades para niños con autismo?"`
5. ¡Espera la respuesta de Gemini!

---

## ✅ Verificación Rápida

### Backend Funciona Si:
- [ ] Terminal muestra `✅ Tablas de chat verificadas/creadas`
- [ ] Muestra `Application startup complete`
- [ ] No hay errores de MySQL

### Frontend Funciona Si:
- [ ] Terminal muestra `✅ Application bundle generation complete`
- [ ] Puedes acceder a http://localhost:4200
- [ ] La página carga sin errores

### Chatbot Funciona Si:
- [ ] Ves un botón flotante en esquina inferior derecha
- [ ] Puedes escribir mensaje
- [ ] Gemini responde en segundos
- [ ] Respuesta aparece en el chat

---

## 🔍 Dónde Está el Chatbot

Visible en ESTAS páginas:
- ✅ Inicio (landing)
- ✅ Servicios
- ✅ Tienda
- ✅ Contacto
- ✅ Donaciones
- ✅ Equipo

**Botón:** Esquina inferior derecha, flotante
**Color:** Típicamente azul/gris (según tu CSS)
**Icono:** Chat, bombilla o similar

---

## 💬 Prueba Estas Preguntas

1. "¿Qué es el Trastorno del Espectro Autista?"
2. "¿Cómo manejar rabietas en niños autistas?"
3. "¿Qué actividades recomiendan?"
4. "¿Cómo establecer rutinas?"
5. "¿Cuáles son los beneficios de terapia?"

---

## 🆘 Si No Funciona

### ❌ No veo el botón flotante
- [ ] Recarga la página (F5)
- [ ] Abre DevTools (F12) → Console
- [ ] ¿Hay errores rojos?
- [ ] Verifica que backend esté corriendo

### ❌ Botón visible pero no responde
- [ ] Revisa Console (F12)
- [ ] Verifica: Backend corriendo en puerto 8000
- [ ] Verifica: URL en servicio apunta a localhost:8000

### ❌ Error 404 o 500
- [ ] Reinicia backend completamente
- [ ] `Ctrl+C` en terminal backend
- [ ] `./start.ps1` nuevamente
- [ ] Espera el mensaje de tablas verificadas

### ❌ Gemini dice "Rate limit exceeded"
- [ ] Espera 1 minuto
- [ ] Reintenta tu pregunta
- [ ] (Límite: 20 requests/minuto)

---

## 📱 URLs Importantes

- **Frontend:** http://localhost:4200
- **Backend API:** http://localhost:8000
- **Swagger API:** http://localhost:8000/docs
- **DB:** `autismo_mochis_ia` (MySQL)

---

## 📂 Archivos Relevantes

```
src/
├── app/
│   ├── shared/
│   │   └── chatbot-ia/
│   │       ├── chatbot-ia.component.ts    ← Lógica
│   │       ├── chatbot-ia.component.html  ← Template
│   │       └── chatbot-ia.component.scss  ← Estilos
│   ├── service/
│   │   └── gemini-ia.service.ts           ← HTTP client
│   └── pages/
│       ├── landing/landing.ts             ← Con chatbot ✅
│       ├── servicios/servicios.ts         ← Con chatbot ✅
│       ├── ventas/ventas.ts               ← Con chatbot ✅
│       ├── contacto/contacto.ts           ← Con chatbot ✅
│       ├── donar/donar.ts                 ← Con chatbot ✅
│       └── equipo/equipo.ts               ← Con chatbot ✅

backend/
├── app/
│   ├── api/v1/endpoints/
│   │   └── chat.py                        ← Endpoints
│   ├── services/
│   │   └── chat_store.py                  ← BD
│   └── main.py                            ← Startup
└── start.ps1                              ← Script inicio
```

---

## 🎯 Resultado Esperado

**Cuando todo funciona:**
1. Página carga normalmente
2. Botón flotante visible (esquina inferior derecha)
3. Haces clic → Se abre panel chat
4. Escribes pregunta
5. En 1-3 segundos: Respuesta de Gemini
6. Puedes hacer más preguntas
7. Histórico se guarda en BD

---

**¿Problemas?** Abre un issue o contacta a soporte.
**¿Todo funciona?** ¡Excelente! El chatbot está listo para producción.

---

*Última verificación: 2024-12-26*

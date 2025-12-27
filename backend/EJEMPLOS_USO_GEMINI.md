# 💻 EJEMPLOS DE USO - GEMINI 2.0 FLASH

## 1. USO DESDE ANGULAR (Frontend)

### Iniciar sesión
```typescript
// chatbot.component.ts
import { HttpClient } from '@angular/common/http';

constructor(private http: HttpClient) {}

crearSesion() {
  this.http.post('/api/v1/chat/sesion', {}).subscribe(
    (res: any) => {
      this.sessionId = res.session_id;
      console.log('Sesión iniciada:', this.sessionId);
    }
  );
}
```

### Enviar pregunta
```typescript
// chatbot.component.ts
enviarMensaje(mensaje: string, rol: string = 'padre') {
  const payload = {
    mensaje: mensaje,
    session_id: this.sessionId,
    nino_id: this.currentNinoId,
    incluir_contexto: true,
    rol_usuario: rol  // "padre", "terapeuta", "educador"
  };

  this.http.post('/api/v1/chatbot', payload).subscribe(
    (res: any) => {
      this.respuestas.push({
        usuario: mensaje,
        asistente: res.respuesta
      });
      this.sesionId = res.session_id;
    }
  );
}
```

### Verificar estado
```typescript
// chatbot.component.ts
verificarGemini() {
  this.http.get('/api/v1/estado').subscribe(
    (res: any) => {
      console.log('Gemini configurado:', res.configurado);
      console.log('Modelo:', res.model);
    }
  );
}
```

---

## 2. USO DESDE PYTHON (Backend)

### Uso directo del servicio
```python
from app.services.gemini_chat_service import gemini_chat_service

# Para padre
respuesta = gemini_chat_service.chat(
    "¿Cómo manejar una rabieta?",
    contexto_nino={
        "nombre": "Juan",
        "edad": 6,
        "diagnosticos": ["TEA Moderado"]
    },
    rol_usuario="padre"
)
print(respuesta["respuesta"])

# Para terapeuta
respuesta = gemini_chat_service.chat(
    "¿Qué técnicas ABA recomiendas?",
    contexto_nino=datos_nino,
    rol_usuario="terapeuta"
)
print(respuesta["respuesta"])

# Para educador
respuesta = gemini_chat_service.chat(
    "¿Cómo adapto el aula?",
    contexto_nino=datos_nino,
    rol_usuario="educador"
)
print(respuesta["respuesta"])
```

### Uso a través de chat_service
```python
from app.services.chat_service import ask_gemini

respuesta = ask_gemini(
    mensaje="¿Actividades para estimular lenguaje?",
    contexto={"nombre": "Ana", "edad": 5},
    historial=[],  # Historial anterior
    rol_usuario="terapeuta"
)
print(respuesta)
```

---

## 3. CURL REQUESTS

### Verificar estado de Gemini
```bash
curl http://localhost:8000/api/v1/estado
```

**Response:**
```json
{
  "configurado": true,
  "model": "models/gemini-2.0-flash"
}
```

### Crear sesión
```bash
curl -X POST http://localhost:8000/api/v1/chat/sesion \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "session_id": "a1b2c3d4e5f6g7h8"
}
```

### Enviar mensaje (PADRE)
```bash
curl -X POST http://localhost:8000/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "¿Cómo mejorar la comunicación?",
    "session_id": "a1b2c3d4e5f6g7h8",
    "nino_id": 1,
    "incluir_contexto": true,
    "rol_usuario": "padre"
  }'
```

**Response:**
```json
{
  "respuesta": "Para mejorar la comunicación con tu hijo...",
  "contexto_usado": true,
  "configurado": true,
  "session_id": "a1b2c3d4e5f6g7h8"
}
```

### Enviar mensaje (TERAPEUTA)
```bash
curl -X POST http://localhost:8000/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "¿Técnicas ABA para reducir estereotipias?",
    "session_id": "a1b2c3d4e5f6g7h8",
    "nino_id": 1,
    "incluir_contexto": true,
    "rol_usuario": "terapeuta"
  }'
```

### Enviar mensaje (EDUCADOR)
```bash
curl -X POST http://localhost:8000/api/v1/chatbot \
  -H "Content-Type: application/json" \
  -d '{
    "mensaje": "¿Adaptaciones de aula para TEA?",
    "session_id": "a1b2c3d4e5f6g7h8",
    "nino_id": 1,
    "incluir_contexto": true,
    "rol_usuario": "educador"
  }'
```

---

## 4. PYTHON REQUESTS

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Crear sesión
response = requests.post(f"{BASE_URL}/chat/sesion")
session_id = response.json()["session_id"]

# 2. Enviar pregunta
payload = {
    "mensaje": "¿Cómo manejar crisis?",
    "session_id": session_id,
    "nino_id": 1,
    "incluir_contexto": True,
    "rol_usuario": "padre"
}

response = requests.post(f"{BASE_URL}/chatbot", json=payload)
resultado = response.json()

print("Respuesta:", resultado["respuesta"])
print("Session ID:", resultado["session_id"])
print("Configurado:", resultado["configurado"])
```

---

## 5. JAVASCRIPT (Vanilla)

```javascript
const API_URL = "http://localhost:8000/api/v1";

// Crear sesión
async function crearSesion() {
  const res = await fetch(`${API_URL}/chat/sesion`, { method: 'POST' });
  const data = await res.json();
  return data.session_id;
}

// Enviar mensaje
async function enviarMensaje(mensaje, sessionId, rol = 'padre') {
  const payload = {
    mensaje: mensaje,
    session_id: sessionId,
    nino_id: 1,
    incluir_contexto: true,
    rol_usuario: rol
  };

  const res = await fetch(`${API_URL}/chatbot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  return await res.json();
}

// Uso
(async () => {
  const sessionId = await crearSesion();
  
  const result = await enviarMensaje(
    "¿Cómo ayudar a mi hijo con TEA?",
    sessionId,
    "padre"
  );
  
  console.log(result.respuesta);
})();
```

---

## 6. TEST AUTOMÁTICO

```python
# backend/test_gemini_flash.py
python test_gemini_flash.py
```

---

## 7. CASOS DE USO POR ROL

### 👨‍👩‍👧 PADRE PREGUNTA
```
Pregunta: "Mi hijo tiene rabietas. ¿Qué hago?"
Rol: padre

Respuesta incluye:
✅ Estrategias prácticas para casa
✅ Qué hacer en el momento
✅ Prevención
✅ Cuándo pedir ayuda profesional
```

### 👨‍⚕️ TERAPEUTA PREGUNTA
```
Pregunta: "¿Cómo evaluar la efectividad de ABA?"
Rol: terapeuta

Respuesta incluye:
✅ Técnicas de medición
✅ Manuales clínicos
✅ Indicadores clave
✅ Literatura reciente
```

### 👨‍🏫 EDUCADOR PREGUNTA
```
Pregunta: "¿Cómo incluir a Juan en las actividades de grupo?"
Rol: educador

Respuesta incluye:
✅ Adaptaciones de aula
✅ Apoyos visuales
✅ Estrategias de colaboración
✅ Comunicación con familia
```

---

## 8. MANEJO DE ERRORES

```python
try:
    result = gemini_chat_service.chat(
        "Pregunta delicada",
        contexto_nino=datos,
        rol_usuario="terapeuta"
    )
    
    if result["configurado"]:
        print("✅ Respuesta de Gemini:")
        print(result["respuesta"])
    else:
        print("⚠️ Usando fallback clínico:")
        print(result["respuesta"])
        
except Exception as e:
    print(f"❌ Error: {e}")
    # El sistema retorna fallback automáticamente
```

---

## 9. DEPURACIÓN

```python
# Ver logs detallados
import logging
logging.basicConfig(level=logging.DEBUG)

# Verificar configuración
from app.core.config import settings
print(f"API Key: {bool(settings.GEMINI_API_KEY)}")
print(f"Modelo: {settings.GEMINI_MODEL}")

# Verificar servicio
from app.services.gemini_chat_service import gemini_chat_service
print(f"Configurado: {gemini_chat_service.configured}")
print(f"Model ID: {gemini_chat_service.model_id}")
```

---

## 10. INTEGRACIÓN CON BD

```python
# Guardar conversación en BD
from app.models import Conversacion

def guardar_conversacion(session_id, nino_id, rol_usuario):
    conv = Conversacion(
        session_id=session_id,
        nino_id=nino_id,
        rol_usuario=rol_usuario,
        historial=gemini_chat_service.store.history(session_id)
    )
    db.add(conv)
    db.commit()
    return conv
```

---

**¡Ya tienes todo para integrar Gemini 2.0 Flash en tu frontend!** 🚀


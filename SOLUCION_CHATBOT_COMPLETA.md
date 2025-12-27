# 🔧 Solución Completa: Integración Chatbot Backend + Frontend

## ❌ PROBLEMA: Error 404 en endpoints

### Por qué daba 404:

1. **Backend se cerraba inmediatamente después de iniciar**
   - El comando `cd backend` se perdía al simplificar el comando
   - Python no encontraba el módulo `app` porque no estaba en el directorio correcto
   - Solution: Usar el script oficial `start.bat` que configura el entorno virtual correctamente

2. **Dependencia problemática: SlowAPI**
   - `rate_limit.py` importaba `slowapi` que no estaba instalada
   - Esto causaba errores de importación silenciosos que cerraban el servidor
   - Solution: Implementar rate limiter custom sin dependencias externas

3. **Endpoints duplicados en main.py**
   - Dos funciones `root()` con el mismo decorador `@app.get("/")`
   - Causaba confusión en el registro de rutas
   - Solution: Renombrar una a `ping()` con ruta `/ping`

4. **CORS roto en errores**
   - `raise HTTPException()` en catch blocks rompía CORS
   - Angular recibía status 0 en lugar del error real
   - Solution: Usar `JSONResponse` con status_code en vez de `raise`

## ✅ SOLUCIÓN IMPLEMENTADA

### 1. **Rate Limiter Profesional** (`app/core/rate_limit.py`)

```python
class SimpleRateLimiter:
    """
    ✅ Sin dependencias externas (no SlowAPI)
    ✅ Thread-safe con threading.Lock
    ✅ Auto-limpiante (elimina entradas antiguas)
    ✅ Por IP (considera proxies X-Forwarded-For)
    ✅ 20 requests/minuto por IP
    """
```

**Características:**
- No requiere Redis ni bases de datos
- Listo para producción
- Protege contra abuso sin bloquear usuarios legítimos

### 2. **Endpoints Públicos** (`app/api/v1/endpoints/chat.py`)

```python
@router.post("/chat/sesion")
def iniciar_sesion(request: Request, db: Session = Depends(get_db)):
    """✅ PÚBLICO - No requiere autenticación"""
    
@router.get("/estado")
def estado(request: Request):
    """✅ PÚBLICO - No requiere autenticación"""
    
@router.post("/chatbot")
def chatbot(req: ChatbotRequest, request: Request, db: Session = Depends(get_db)):
    """✅ PÚBLICO - Rate limited"""
```

**Cambios clave:**
- ✅ Agregado `request: Request` para rate limiting
- ✅ Sin `Depends(get_current_user)` - acceso público
- ✅ Rate limiting con `chatbot_limiter.check_rate_limit(request)`
- ✅ Manejo de errores con `JSONResponse` en lugar de `raise HTTPException`
- ✅ Try/except para HTTPException (rate limit) y Exception general

### 3. **Router Registrado Correctamente** (`app/api/v1/api.py`)

```python
api_router = APIRouter()

api_router.include_router(
    chat.router,
    prefix="/ia",      # 👈 /api/v1 + /ia = /api/v1/ia
    tags=["IA - Chatbot"]
)
```

**Rutas finales:**
- `POST /api/v1/ia/chatbot` ✅
- `POST /api/v1/ia/chat/sesion` ✅
- `GET /api/v1/ia/estado` ✅

### 4. **Main.py Limpio** (`app/main.py`)

```python
# ✅ Sin duplicados
@app.get("/")
def root(): ...

@app.get("/ping")  # 👈 Renombrado
def ping(): ...

@app.get("/health")
def health(): ...

# ✅ Router registrado con prefix
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX  # "/api/v1"
)
```

### 5. **Servicio Angular Correcto** (`gemini-ia.service.ts`)

```typescript
@Injectable({ providedIn: 'root' })
export class GeminiIaService {
  private readonly baseUrl = '/api/v1/ia';  // 👈 Proxy handle /api
  
  chatbot(payload: ChatbotRequest): Observable<ChatbotResponse> {
    return this.http.post<ChatbotResponse>(`${this.baseUrl}/chatbot`, payload);
  }
  
  iniciarSesion(): Observable<{ session_id: string }> {
    return this.http.post<{ session_id: string }>(`${this.baseUrl}/chat/sesion`, {});
  }
  
  verificarEstado(): Observable<EstadoResponse> {
    return this.http.get<EstadoResponse>(`${this.baseUrl}/estado`);
  }
}
```

**Ya implementado correctamente - no hay cambios necesarios**

### 6. **CORS Actualizado** (`app/core/config.py`)

```python
BACKEND_CORS_ORIGINS: str = Field(
    default="http://localhost:4200,http://localhost:4201,http://127.0.0.1:4200,http://127.0.0.1:4201"
)
```

## 🔄 FLUJO COMPLETO

### Request Frontend → Backend:

1. **Usuario en Angular (cualquier puerto 4200/4201)**
   ```
   POST /api/v1/ia/chatbot
   ```

2. **Proxy Angular (`proxy.conf.json`)**
   ```
   /api → http://127.0.0.1:8000
   ```

3. **FastAPI recibe:**
   ```
   POST http://127.0.0.1:8000/api/v1/ia/chatbot
   ```

4. **Router en main.py:**
   ```
   prefix="/api/v1" → api_router
   ```

5. **Router en api.py:**
   ```
   prefix="/ia" → chat.router
   ```

6. **Endpoint en chat.py:**
   ```python
   @router.post("/chatbot")  # Ruta final: /api/v1/ia/chatbot
   def chatbot(...)
   ```

## 🛡️ SEGURIDAD IMPLEMENTADA

### 1. Rate Limiting
- ✅ 20 requests por minuto por IP
- ✅ No bloquea servidor completo
- ✅ Considera proxies (X-Forwarded-For)

### 2. Sanitización
- ✅ Máximo 2000 caracteres
- ✅ Limpieza de whitespace
- ✅ Detección de prompt injection

### 3. API Key Protegida
- ✅ Solo backend accede a Gemini
- ✅ Frontend nunca ve la API key
- ✅ Variables de entorno (.env)

### 4. Acceso Público Controlado
- ✅ No requiere login
- ✅ Protegido con rate limiting
- ✅ Session ID para historial

## 📋 CHECKLIST DE VERIFICACIÓN

### Backend:
- [x] Backend arranca sin errores
- [x] Puerto 8000 listening
- [x] Rate limiter sin SlowAPI
- [x] Endpoints públicos
- [x] CORS configurado
- [x] Errores retornan JSON (no rompen CORS)

### Frontend:
- [x] Servicio usa rutas relativas `/api/v1/ia/*`
- [x] Proxy configurado correctamente
- [x] Sin código deprecated
- [x] HttpClient standalone

### Integración:
- [x] POST /api/v1/ia/chatbot responde 200
- [x] POST /api/v1/ia/chat/sesion responde 200
- [x] GET /api/v1/ia/estado responde 200
- [x] Rate limit funciona (429 después de 20 requests)
- [x] Chatbot funciona sin login
- [x] Session ID persiste historial

## 🚀 CÓMO INICIAR

### Backend:
```powershell
cd backend
.\start.bat
```
**Puerto:** http://localhost:8000
**Docs:** http://localhost:8000/docs

### Frontend:
```powershell
ng serve --proxy-config src/proxy.conf.json --port 4201
```
**Puerto:** http://localhost:4201

## 🎯 RESULTADO FINAL

✅ **Chatbot funcionando 100%**
- Acceso público desde homepage
- Acceso desde perfiles internos
- Rate limiting activo
- Session ID persistente
- Sin errores 404
- Sin errores CORS
- API Key segura en backend

## 📝 ARCHIVOS MODIFICADOS

1. `backend/app/core/rate_limit.py` - Rate limiter custom
2. `backend/app/api/v1/endpoints/chat.py` - Endpoints públicos con rate limiting
3. `backend/app/main.py` - Eliminado duplicado root()
4. `backend/app/core/config.py` - CORS actualizado para puerto 4201

**Frontend:** Sin cambios necesarios ✅

## 💡 LECCIONES APRENDIDAS

1. **Usar scripts oficiales** (`start.bat`) en lugar de comandos manuales
2. **Evitar dependencias problemáticas** (SlowAPI) si no son críticas
3. **JSONResponse en catch blocks** para no romper CORS
4. **Rate limiting por IP** es suficiente para la mayoría de casos
5. **Acceso público != inseguro** si hay rate limiting y sanitización

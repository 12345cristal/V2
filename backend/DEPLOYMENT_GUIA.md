# 🚀 DEPLOYMENT - BACKEND PERFIL CON ARCHIVOS

## ⚙️ PASO A PASO DEPLOYMENT

### 1️⃣ Preparación del Proyecto

#### Crear estructura de directorios

```bash
cd backend/
mkdir -p uploads/fotos
mkdir -p uploads/cv
mkdir -p uploads/documentos

# Dar permisos
chmod -R 755 uploads/
```

#### Agregar .gitignore

```bash
# Agregar a backend/.gitignore
echo "uploads/" >> .gitignore
echo "!uploads/.gitkeep" >> .gitignore

# Crear archivos .gitkeep para que git rastree los directorios
touch uploads/fotos/.gitkeep
touch uploads/cv/.gitkeep
touch uploads/documentos/.gitkeep
```

---

### 2️⃣ Actualizar Código

#### A) Modelo (app/models/personal_perfil.py)

✅ YA ACTUALIZADO

```python
foto_perfil = Column(String(255), nullable=True)
cv_archivo = Column(String(255), nullable=True)
documentos_extra = Column(Text, nullable=True)
```

#### B) Schema (app/schemas/perfil.py)

✅ YA ACTUALIZADO

```python
foto_perfil: Optional[str] = None
cv_archivo: Optional[str] = None
documentos_extra: List[str] = []
```

#### C) Endpoint (app/api/v1/endpoints/perfil.py)

✅ YA COMPLETAMENTE REESCRITO

- GET /me
- PUT /me (con manejo de archivos)
- GET /archivos/{tipo}/{filename}

---

### 3️⃣ Verificación de Dependencies

#### Verificar que existen en requirements.txt

```bash
# Debe contener:
fastapi>=0.95.0
python-multipart>=0.0.5
sqlalchemy>=2.0.0
pathlib  # Está en stdlib, pero incluir por si acaso
```

#### Instalar si falta

```bash
pip install python-multipart pathlib
```

---

### 4️⃣ Verificar Configuración

#### settings.py o config.py

```python
from pathlib import Path

# Debe tener BASE_DIR definido
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# El código usa:
UPLOADS_DIR = Path(settings.BASE_DIR) / "uploads"
```

---

### 5️⃣ Testing Local

#### Iniciar servidor

```bash
cd backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Test 1: Obtener perfil

```bash
curl -H "Authorization: Bearer {token_aqui}" \
  http://localhost:8000/api/v1/perfil/me
```

#### Test 2: Subir archivo

```bash
curl -X PUT \
  -H "Authorization: Bearer {token_aqui}" \
  -F "foto_perfil=@/ruta/a/foto.jpg" \
  http://localhost:8000/api/v1/perfil/me
```

#### Test 3: Descargar archivo

```bash
curl -H "Authorization: Bearer {token_aqui}" \
  -o descargada.jpg \
  http://localhost:8000/api/v1/perfil/archivos/fotos/personal_1_1700000000_foto.jpg
```

#### Test 4: Ver Swagger

```
http://localhost:8000/docs
```

---

### 6️⃣ Integración con Frontend

#### Verificar ArchivosService (src/app/service/archivos.service.ts)

```typescript
descargarComoBlob(rutaRelativa: string): Observable<Blob> {
  // rutaRelativa = "fotos/personal_1_1700000000_foto.png"
  const partes = rutaRelativa.split('/');
  const tipo = partes[0];
  const filename = partes.slice(1).join('/');

  return this.httpClient.get(
    `${environment.apiBaseUrl}/perfil/archivos/${tipo}/${filename}`,
    { responseType: 'blob' }
  );
  // Token JWT agregado por interceptor
}
```

#### Verificar PerfilService (src/app/service/perfil.service.ts)

```typescript
actualizarMiPerfil(formData: FormData): Observable<PerfilUsuario> {
  return this.httpClient.put<PerfilUsuario>(
    `${environment.apiBaseUrl}/perfil/me`,
    formData
    // Content-Type: multipart/form-data (automático con FormData)
    // Authorization: Bearer token (automático con interceptor)
  );
}
```

---

### 7️⃣ Verificar Estructura de Respuesta

#### Esperado en GET /perfil/me

```json
{
  "id_personal": 1,
  "nombres": "Juan",
  "apellido_paterno": "Pérez",
  "foto_perfil": "fotos/personal_1_1700000000_foto.png",  // ← Ruta relativa
  "cv_archivo": "cv/personal_1_1700000050_cv.pdf",        // ← Ruta relativa
  "documentos_extra": [
    "documentos/personal_1_1700000100_cert.pdf",          // ← Rutas relativas
    "documentos/personal_1_1700000110_imagen.png"
  ],
  "telefono_personal": "555-1234",
  "correo_personal": "juan@example.com",
  ...
}
```

---

### 8️⃣ Errores Comunes y Soluciones

#### Error: "module not found: pathlib"

```
Solución: python -c "from pathlib import Path"
(pathlib es parte de stdlib desde Python 3.4)
```

#### Error: "Permission denied" al escribir

```
Solución:
chmod -R 755 uploads/
# O cambiar owner:
chown -R www-data:www-data uploads/
```

#### Error: "Endpoint not found" en Swagger

```
Solución: Verificar que router está incluido en main.py:
from app.api.v1.endpoints import perfil
app.include_router(perfil.router, prefix="/api/v1/perfil")
```

#### Error: "File too large"

```
Solución: FastAPI por defecto acepta 25MB
Futuro: implementar validación en endpoint
```

---

### 9️⃣ Checklist Pre-Deployment

- [ ] `uploads/` directorio creado
- [ ] `.gitignore` actualizado (uploads/)
- [ ] `requirements.txt` incluye `python-multipart`
- [ ] `settings.py` tiene `BASE_DIR` definido
- [ ] `perfil.py` endpoint actualizado
- [ ] `personal_perfil.py` modelo actualizado
- [ ] `perfil.py` schema actualizado
- [ ] Tests locales pasando
- [ ] Swagger funciona
- [ ] Frontend ArchivosService compatible
- [ ] JWT interceptor en Angular
- [ ] CORS habilitado si es necesario

---

### 🔟 Deployment a Producción

#### Opción A: Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear uploads con permisos
RUN mkdir -p uploads/{fotos,cv,documentos} && \
    chmod -R 755 uploads/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t perfil-api .
docker run -v uploads:/app/uploads -p 8000:8000 perfil-api
```

#### Opción B: Systemd (Linux)

```ini
# /etc/systemd/system/perfil-api.service
[Unit]
Description=Perfil API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/perfil-api
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable perfil-api
sudo systemctl start perfil-api
```

#### Opción C: Gunicorn + Nginx

```bash
# Instalar
pip install gunicorn uvicorn

# Ejecutar
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

```nginx
# /etc/nginx/sites-available/perfil-api
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Authorization $http_authorization;
    }

    location /uploads/ {
        alias /var/www/perfil-api/uploads/;
        expires 30d;
    }
}
```

---

### 🔐 Seguridad en Producción

#### 1. HTTPS

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ...
}
```

#### 2. CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Especificar origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("100/minute")
@router.put("/me")
def actualizar_perfil(...):
    ...
```

#### 4. Validar tamaño de archivo

```python
MAX_FOTO_SIZE = 5 * 1024 * 1024  # 5MB
MAX_CV_SIZE = 10 * 1024 * 1024   # 10MB

if foto_perfil.size > MAX_FOTO_SIZE:
    raise HTTPException(400, "Foto muy grande")
```

#### 5. Sanitizar nombres

```python
import re

def sanitizar_nombre(filename: str) -> str:
    # Remover caracteres peligrosos
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename.strip()
```

---

### 📊 Monitoreo

#### Logs

```bash
# Servidor
tail -f /var/log/systemd/perfil-api.log

# Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

#### Disk Space

```bash
# Monitorear uploads/
du -sh uploads/
df -h /var/www/perfil-api/uploads/
```

#### Limpieza automática (opcional)

```bash
# Cron job: limpiar archivos > 90 días
0 2 * * * find /var/www/perfil-api/uploads -type f -mtime +90 -delete
```

---

### 🎯 Resumen

| Paso | Acción               | Status |
| ---- | -------------------- | ------ |
| 1    | Crear directorios    | ✅     |
| 2    | Actualizar código    | ✅     |
| 3    | Verificar deps       | ✅     |
| 4    | Testing local        | 🔄     |
| 5    | Integración frontend | 🔄     |
| 6    | Deploy producción    | ⏳     |
| 7    | Monitoreo            | ⏳     |

---

**Fecha:** 2026-01-12  
**Versión:** 1.0.0  
**Status:** LISTO PARA DEPLOY

# ================================================================
# CÓDIGO PARA AGREGAR EN: backend/app/main.py
# ================================================================
# Copiar estas líneas en las secciones correspondientes

# ============================================================
# SECCIÓN 1: IMPORTS (agregar al inicio del archivo)
# ============================================================
from app.api.v1.endpoints import citas_calendario

# ============================================================
# SECCIÓN 2: REGISTRAR ROUTER (después de otros routers)
# ============================================================
# Ejemplo de ubicación: después de otros include_router

app.include_router(
    citas_calendario.router,
    prefix=f"{settings.API_V1_PREFIX}/citas-calendario",
    tags=["Citas y Calendario"],
    dependencies=[Depends(require_admin_or_coordinator)]
)

# ============================================================
# CÓDIGO COMPLETO DE EJEMPLO
# ============================================================
"""
# main.py - Fragmento relevante

from fastapi import FastAPI, Depends
from app.core.config import settings
from app.api.deps import require_admin_or_coordinator

# ... otros imports

# Importar el router de citas con calendario
from app.api.v1.endpoints import citas_calendario

app = FastAPI(
    title=settings.PROJECT_NAME,
    # ... otras configuraciones
)

# ... otros routers

# NUEVO: Router de citas con Google Calendar
app.include_router(
    citas_calendario.router,
    prefix=f"{settings.API_V1_PREFIX}/citas-calendario",
    tags=["Citas y Calendario"]
)

# ... resto del código
"""

# ============================================================
# VERIFICAR QUE EXISTE ESTE IMPORT EN deps.py
# ============================================================
# from app.api.deps import require_admin_or_coordinator
# ✅ Ya existe en tu sistema según la revisión previa

# ============================================================
# ENDPOINTS DISPONIBLES DESPUÉS DE AGREGAR EL ROUTER
# ============================================================
"""
POST   /api/v1/citas-calendario/              - Crear cita
PUT    /api/v1/citas-calendario/{id}/reprogramar - Reprogramar
PUT    /api/v1/citas-calendario/{id}/cancelar    - Cancelar
GET    /api/v1/citas-calendario/calendario       - Ver calendario
GET    /api/v1/citas-calendario/{id}             - Detalles
GET    /api/v1/docs                               - Swagger UI
"""

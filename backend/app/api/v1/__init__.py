from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Routers base
from app.api.v1 import auth, ninos

# Routers por módulo (endpoints)
from app.api.v1.endpoints import (
    personal,
    terapias,
    citas,
    coordinador,
    perfil,
    topsis,
    recomendacion,
    topsis_terapeutas,
    recomendaciones_actividades,
    fichas_emergencia,
    gemini_ia,
)

# Dependencias
from app.api.deps import get_db, get_current_user

# Modelos / Schemas
from app.models.cita import EstadoCita
from app.models.usuario import Usuario
from app.schemas.cita import EstadoCitaRead


# ======================================================
# API ROUTER PRINCIPAL v1
# ======================================================
api_router = APIRouter()


# ======================================================
# AUTH & USUARIOS
# ======================================================
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticación"],
)

api_router.include_router(
    ninos.router,
    prefix="/ninos",
    tags=["Niños Beneficiarios"],
)


# ======================================================
# PERSONAL & TERAPIAS
# ======================================================
api_router.include_router(
    personal.router,
    prefix="/personal",
    tags=["Personal"],
)

api_router.include_router(
    terapias.router,
    prefix="/terapias",
    tags=["Terapias"],
)

api_router.include_router(
    citas.router,
    prefix="/citas",
    tags=["Citas"],
)


# ======================================================
# COORDINACIÓN & PERFIL
# ======================================================
api_router.include_router(
    coordinador.router,
    prefix="/coordinador",
    tags=["Coordinador"],
)

api_router.include_router(
    perfil.router,
    prefix="/perfil",
    tags=["Perfil de Usuario"],
)


# ======================================================
# IA & DECISIÓN
# ======================================================
api_router.include_router(
    topsis.router,
    prefix="/topsis",
    tags=["TOPSIS"],
)

api_router.include_router(
    topsis_terapeutas.router,
    prefix="/topsis-terapeutas",
    tags=["TOPSIS Terapeutas"],
)

api_router.include_router(
    recomendacion.router,
    prefix="/recomendaciones",
    tags=["Recomendaciones Inteligentes"],
)

api_router.include_router(
    recomendaciones_actividades.router,
    prefix="/recomendaciones-actividades",
    tags=["Recomendaciones de Actividades"],
)

api_router.include_router(
    gemini_ia.router,
    prefix="/ia",
    tags=["Inteligencia Artificial - Gemini"],
)


# ======================================================
# CATÁLOGOS
# ======================================================
@api_router.get(
    "/estados-cita",
    response_model=List[EstadoCitaRead],
    tags=["Catálogos"],
)
def get_estados_cita(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Obtiene el catálogo de estados de citas
    """
    return db.query(EstadoCita).all()

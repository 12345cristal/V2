# app/api/v1/__init__.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.v1 import auth, ninos
from app.api.v1.endpoints import personal, terapias, citas, coordinador, perfil
from app.api.deps import get_db, get_current_user
from app.models.cita import EstadoCita
from app.models.usuario import Usuario
from app.schemas.cita import EstadoCitaRead

api_router = APIRouter()

# Incluir routers
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(ninos.router, prefix="/ninos", tags=["Niños Beneficiarios"])
api_router.include_router(personal.router, prefix="/personal", tags=["Personal"])
api_router.include_router(terapias.router, prefix="/terapias", tags=["Terapias"])
api_router.include_router(citas.router, prefix="/citas", tags=["Citas"])
api_router.include_router(coordinador.router, prefix="/coordinador", tags=["Coordinador"])
api_router.include_router(perfil.router, prefix="/perfil", tags=["Perfil de Usuario"])


# Endpoint adicional para estados-cita en la raíz
@api_router.get("/estados-cita", response_model=List[EstadoCitaRead], tags=["Catálogos"])
def get_estados_cita(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene el catálogo de estados de citas
    """
    return db.query(EstadoCita).all()

# app/api/v1/endpoints/catalogos.py
"""
Catálogos públicos y comunes (no requieren autenticación)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.models.cita import EstadoCita
from app.schemas.cita import EstadoCitaRead

router = APIRouter(tags=["Catálogos"])


@router.get("/estados-cita", response_model=List[EstadoCitaRead])
def obtener_estados_cita(db: Session = Depends(get_db_session)):
    """
    Obtiene el catálogo de estados de cita.
    
    Endpoint público - sin autenticación requerida.
    
    Returns:
        List[EstadoCitaRead]: Lista de estados disponibles
    """
    estados = db.query(EstadoCita).order_by(EstadoCita.id).all()
    return estados


@router.get("/especialidades", response_model=List[dict])
def obtener_especialidades(db: Session = Depends(get_db_session)):
    """
    Obtiene el catálogo de especialidades disponibles.
    
    Endpoint público - sin autenticación requerida.
    
    Returns:
        List[dict]: Lista de especialidades
    """
    from app.models.personal import Personal
    from sqlalchemy import distinct, func
    
    especialidades = db.query(
        distinct(Personal.especialidad_principal)
    ).filter(
        Personal.especialidad_principal.isnot(None),
        Personal.especialidad_principal != ""
    ).order_by(Personal.especialidad_principal).all()
    
    return [
        {"id": i, "nombre": esp[0]}
        for i, esp in enumerate(especialidades, 1)
    ]


@router.get("/roles", response_model=List[dict])
def obtener_roles(db: Session = Depends(get_db_session)):
    """
    Obtiene el catálogo de roles disponibles.
    
    Endpoint público - sin autenticación requerida.
    
    Returns:
        List[dict]: Lista de roles (admin, coordinador, terapeuta, padre)
    """
    from app.models.rol import Rol
    
    roles = db.query(Rol).all()
    return [
        {"id": r.id, "nombre": r.nombre, "descripcion": r.descripcion}
        for r in roles
    ]

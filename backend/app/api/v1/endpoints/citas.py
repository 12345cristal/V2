# app/api/v1/endpoints/citas.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import date, datetime

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.cita import Cita, EstadoCita
from app.models.nino import Nino
from app.models.personal import Personal
from app.models.terapia import Terapia
from app.schemas.cita import (
    CitaCreate,
    CitaUpdate,
    CitaRead,
    CitaListResponse,
    EstadoCitaRead
)
import math

router = APIRouter()


# ============================================================
# CATÁLOGOS
# ============================================================

@router.get("/catalogos/estados", response_model=List[EstadoCitaRead])
def listar_estados_cita(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene el catálogo de estados de citas
    """
    estados = db.query(EstadoCita).all()
    return estados


# ============================================================
# CRUD CITAS
# ============================================================

@router.get("", response_model=CitaListResponse)
def listar_citas(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    fecha: Optional[str] = None,
    nino_id: Optional[int] = None,
    terapeuta_id: Optional[int] = None,
    terapia_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    buscar: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las citas con filtros opcionales
    """
    query = db.query(Cita)
    
    # Filtros
    if fecha:
        query = query.filter(Cita.fecha == fecha)
    
    if nino_id:
        query = query.filter(Cita.nino_id == nino_id)
    
    if terapeuta_id:
        query = query.filter(Cita.terapeuta_id == terapeuta_id)
    
    if terapia_id:
        query = query.filter(Cita.terapia_id == terapia_id)
    
    if estado_id:
        query = query.filter(Cita.estado_id == estado_id)
    
    if buscar:
        query = query.join(Nino, Cita.nino_id == Nino.id).filter(
            or_(
                Nino.nombre.contains(buscar),
                Nino.apellido_paterno.contains(buscar),
                Nino.apellido_materno.contains(buscar)
            )
        )
    
    # Contar total
    total = query.count()
    
    # Paginación
    offset = (page - 1) * page_size
    citas = query.order_by(Cita.fecha.desc(), Cita.hora_inicio.desc())\
                 .offset(offset)\
                 .limit(page_size)\
                 .all()
    
    # Transformar a response
    items = []
    for cita in citas:
        # Obtener nombres relacionados
        nino_nombre = None
        if cita.nino:
            nino_nombre = f"{cita.nino.nombre} {cita.nino.apellido_paterno}"
            if cita.nino.apellido_materno:
                nino_nombre += f" {cita.nino.apellido_materno}"
        
        terapeuta_nombre = None
        if cita.terapeuta:
            terapeuta_nombre = f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}"
        
        terapia_nombre = cita.terapia.nombre if cita.terapia else None
        estado_nombre = cita.estado.nombre if cita.estado else None
        
        items.append(CitaRead(
            id_cita=cita.id,
            nino_id=cita.nino_id or 0,
            terapeuta_id=cita.terapeuta_id or 0,
            terapia_id=cita.terapia_id or 0,
            fecha=cita.fecha,
            hora_inicio=cita.hora_inicio,
            hora_fin=cita.hora_fin,
            estado_id=cita.estado_id,
            motivo=cita.motivo,
            observaciones=cita.observaciones,
            es_reposicion=cita.es_reposicion or 0,
            nino_nombre=nino_nombre,
            terapeuta_nombre=terapeuta_nombre,
            terapia_nombre=terapia_nombre,
            estado_nombre=estado_nombre
        ))
    
    return CitaListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{cita_id}", response_model=CitaRead)
def obtener_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene una cita por su ID
    """
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    # Obtener nombres relacionados
    nino_nombre = None
    if cita.nino:
        nino_nombre = f"{cita.nino.nombre} {cita.nino.apellido_paterno}"
        if cita.nino.apellido_materno:
            nino_nombre += f" {cita.nino.apellido_materno}"
    
    terapeuta_nombre = None
    if cita.terapeuta:
        terapeuta_nombre = f"{cita.terapeuta.nombres} {cita.terapeuta.apellido_paterno}"
    
    terapia_nombre = cita.terapia.nombre if cita.terapia else None
    estado_nombre = cita.estado.nombre if cita.estado else None
    
    return CitaRead(
        id_cita=cita.id,
        nino_id=cita.nino_id or 0,
        terapeuta_id=cita.terapeuta_id or 0,
        terapia_id=cita.terapia_id or 0,
        fecha=cita.fecha,
        hora_inicio=cita.hora_inicio,
        hora_fin=cita.hora_fin,
        estado_id=cita.estado_id,
        motivo=cita.motivo,
        observaciones=cita.observaciones,
        es_reposicion=cita.es_reposicion or 0,
        nino_nombre=nino_nombre,
        terapeuta_nombre=terapeuta_nombre,
        terapia_nombre=terapia_nombre,
        estado_nombre=estado_nombre
    )


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(
    cita_in: CitaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva cita
    """
    nueva_cita = Cita(
        nino_id=cita_in.nino_id,
        terapeuta_id=cita_in.terapeuta_id,
        terapia_id=cita_in.terapia_id,
        fecha=cita_in.fecha,
        hora_inicio=cita_in.hora_inicio,
        hora_fin=cita_in.hora_fin,
        estado_id=cita_in.estado_id,
        motivo=cita_in.motivo,
        observaciones=cita_in.observaciones,
        es_reposicion=cita_in.es_reposicion
    )
    
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    
    return obtener_cita(nueva_cita.id, db, current_user)


@router.put("/{cita_id}", response_model=CitaRead)
def actualizar_cita(
    cita_id: int,
    cita_in: CitaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza una cita existente
    """
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    # Actualizar campos
    update_data = cita_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cita, field, value)
    
    db.commit()
    db.refresh(cita)
    
    return obtener_cita(cita.id, db, current_user)


@router.patch("/{cita_id}/estado")
def cambiar_estado_cita(
    cita_id: int,
    estado_id: int = Query(..., description="Nuevo estado de la cita"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cambia el estado de una cita
    """
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    cita.estado_id = estado_id
    db.commit()
    db.refresh(cita)
    
    return obtener_cita(cita.id, db, current_user)


@router.delete("/{cita_id}")
def eliminar_cita(
    cita_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina una cita
    """
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    db.delete(cita)
    db.commit()
    
    return {"message": "Cita eliminada correctamente"}

# app/api/v1/endpoints/padre/mis_hijos.py
"""
Router para gestión de Hijos desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino, NinoDiagnostico
from app.schemas.padre import Hijo, HijoDetalle, HijoUpdate, Alergia, Medicamento


router = APIRouter()


@router.get("/hijos/{padre_id}", response_model=List[Hijo])
async def listar_hijos(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista todos los hijos del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # Obtener hijos
    hijos = db.query(Nino).filter(Nino.tutor_id == padre_id).all()
    
    result = []
    for hijo in hijos:
        # Calcular edad
        hoy = date.today()
        edad = hoy.year - hijo.fecha_nacimiento.year
        if hoy.month < hijo.fecha_nacimiento.month or (
            hoy.month == hijo.fecha_nacimiento.month and 
            hoy.day < hijo.fecha_nacimiento.day
        ):
            edad -= 1
        
        # Obtener diagnóstico
        diagnostico = None
        if hijo.diagnostico:
            diagnostico = hijo.diagnostico.diagnostico_principal
        
        result.append(Hijo(
            id=hijo.id,
            nombre=hijo.nombre,
            apellido_paterno=hijo.apellido_paterno,
            apellido_materno=hijo.apellido_materno,
            fecha_nacimiento=hijo.fecha_nacimiento,
            sexo=hijo.sexo,
            curp=hijo.curp,
            edad=edad,
            diagnostico_principal=diagnostico,
            estado=hijo.estado,
            fecha_registro=hijo.fecha_registro
        ))
    
    return result


@router.get("/hijos/{hijo_id}/detalle", response_model=HijoDetalle)
async def obtener_detalle_hijo(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene detalles completos del hijo
    """
    # Obtener hijo
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or hijo.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # Calcular edad
    hoy = date.today()
    edad = hoy.year - hijo.fecha_nacimiento.year
    if hoy.month < hijo.fecha_nacimiento.month or (
        hoy.month == hijo.fecha_nacimiento.month and 
        hoy.day < hijo.fecha_nacimiento.day
    ):
        edad -= 1
    
    # Obtener diagnóstico
    diagnostico = None
    if hijo.diagnostico:
        diagnostico = hijo.diagnostico.diagnostico_principal
    
    # TODO: Implementar lógica real para alergias, medicamentos, terapias y próxima sesión
    alergias = []  # Simulado
    medicamentos = []  # Simulado
    terapias_activas = []  # Simulado
    proxima_sesion = None  # Simulado
    
    return HijoDetalle(
        id=hijo.id,
        nombre=hijo.nombre,
        apellido_paterno=hijo.apellido_paterno,
        apellido_materno=hijo.apellido_materno,
        fecha_nacimiento=hijo.fecha_nacimiento,
        sexo=hijo.sexo,
        curp=hijo.curp,
        edad=edad,
        diagnostico_principal=diagnostico,
        estado=hijo.estado,
        fecha_registro=hijo.fecha_registro,
        alergias=alergias,
        medicamentos=medicamentos,
        terapias_activas=terapias_activas,
        proxima_sesion=proxima_sesion
    )


@router.get("/hijos/{hijo_id}/alergias", response_model=List[str])
async def obtener_alergias(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene solo las alergias del hijo
    """
    # Obtener hijo y verificar permisos
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or hijo.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar modelo de alergias y obtener de BD
    # Por ahora, retornar lista vacía
    alergias = []
    
    return alergias


@router.get("/hijos/{hijo_id}/medicamentos", response_model=List[str])
async def obtener_medicamentos(
    hijo_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene medicamentos actuales del hijo
    """
    # Obtener hijo y verificar permisos
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or hijo.tutor_id != tutor.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar modelo de medicamentos y obtener de BD
    # Por ahora, retornar lista vacía
    medicamentos = []
    
    return medicamentos


@router.put("/hijos/{hijo_id}", response_model=Hijo)
async def actualizar_hijo(
    hijo_id: int,
    hijo_update: HijoUpdate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Actualizar información del hijo (solo padre o coordinador)
    Padre puede actualizar datos básicos
    Coordinador puede actualizar todo
    """
    # Obtener hijo
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    # Verificar permisos
    es_coordinador = current_user.rol_id in [1, 2]  # Admin o Coordinador
    es_padre = current_user.rol_id == 4
    
    if es_padre:
        tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
        if not tutor or hijo.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para actualizar este hijo"
            )
    
    # Actualizar campos permitidos
    if hijo_update.nombre is not None:
        hijo.nombre = hijo_update.nombre
    if hijo_update.apellido_paterno is not None:
        hijo.apellido_paterno = hijo_update.apellido_paterno
    if hijo_update.apellido_materno is not None:
        hijo.apellido_materno = hijo_update.apellido_materno
    
    # Guardar cambios
    db.commit()
    db.refresh(hijo)
    
    # Calcular edad
    hoy = date.today()
    edad = hoy.year - hijo.fecha_nacimiento.year
    if hoy.month < hijo.fecha_nacimiento.month or (
        hoy.month == hijo.fecha_nacimiento.month and 
        hoy.day < hijo.fecha_nacimiento.day
    ):
        edad -= 1
    
    # Obtener diagnóstico
    diagnostico = None
    if hijo.diagnostico:
        diagnostico = hijo.diagnostico.diagnostico_principal
    
    return Hijo(
        id=hijo.id,
        nombre=hijo.nombre,
        apellido_paterno=hijo.apellido_paterno,
        apellido_materno=hijo.apellido_materno,
        fecha_nacimiento=hijo.fecha_nacimiento,
        sexo=hijo.sexo,
        curp=hijo.curp,
        edad=edad,
        diagnostico_principal=diagnostico,
        estado=hijo.estado,
        fecha_registro=hijo.fecha_registro
    )

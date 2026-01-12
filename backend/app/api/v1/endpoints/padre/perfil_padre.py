# app/api/v1/endpoints/padre/perfil_padre.py
"""
Router para Perfil y Accesibilidad del Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.schemas.padre import Padre, PadreUpdate, Accesibilidad, AccesibilidadBase


router = APIRouter()


@router.get("/perfil/{padre_id}", response_model=Padre)
async def obtener_perfil(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene datos del perfil del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    return Padre(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        telefono=current_user.telefono,
        ocupacion=tutor.ocupacion,
        activo=current_user.activo,
        fecha_creacion=current_user.fecha_creacion
    )


@router.put("/perfil/{padre_id}", response_model=Padre)
async def actualizar_perfil(
    padre_id: int,
    padre_update: PadreUpdate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Actualiza el perfil del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar este perfil"
        )
    
    # Actualizar usuario
    if padre_update.nombres is not None:
        current_user.nombres = padre_update.nombres
    if padre_update.apellido_paterno is not None:
        current_user.apellido_paterno = padre_update.apellido_paterno
    if padre_update.apellido_materno is not None:
        current_user.apellido_materno = padre_update.apellido_materno
    if padre_update.telefono is not None:
        current_user.telefono = padre_update.telefono
    
    # Actualizar tutor
    if padre_update.ocupacion is not None:
        tutor.ocupacion = padre_update.ocupacion
    
    db.commit()
    db.refresh(current_user)
    db.refresh(tutor)
    
    return Padre(
        id=current_user.id,
        nombres=current_user.nombres,
        apellido_paterno=current_user.apellido_paterno,
        apellido_materno=current_user.apellido_materno,
        email=current_user.email,
        telefono=current_user.telefono,
        ocupacion=tutor.ocupacion,
        activo=current_user.activo,
        fecha_creacion=current_user.fecha_creacion
    )


@router.get("/accesibilidad/{padre_id}", response_model=Accesibilidad)
async def obtener_accesibilidad(
    padre_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene preferencias de accesibilidad del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta información"
        )
    
    # TODO: Implementar modelo de accesibilidad
    # Por ahora, retornar valores por defecto
    from datetime import datetime
    return Accesibilidad(
        id=1,
        padre_id=padre_id,
        tamaño_fuente="NORMAL",
        contraste_alto=False,
        modo_oscuro=False,
        lectura_voz=False,
        subtitulos_video=True,
        notificaciones_sonido=True,
        notificaciones_vibracion=True,
        fecha_actualizacion=datetime.now()
    )


@router.put("/accesibilidad/{padre_id}", response_model=Accesibilidad)
async def actualizar_accesibilidad(
    padre_id: int,
    accesibilidad: AccesibilidadBase,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Actualiza preferencias de accesibilidad del padre
    """
    # Verificar permisos
    tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
    if not tutor or tutor.id != padre_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar esta información"
        )
    
    # TODO: Implementar actualización en BD
    from datetime import datetime
    return Accesibilidad(
        id=1,
        padre_id=padre_id,
        tamaño_fuente=accesibilidad.tamaño_fuente,
        contraste_alto=accesibilidad.contraste_alto,
        modo_oscuro=accesibilidad.modo_oscuro,
        lectura_voz=accesibilidad.lectura_voz,
        subtitulos_video=accesibilidad.subtitulos_video,
        notificaciones_sonido=accesibilidad.notificaciones_sonido,
        notificaciones_vibracion=accesibilidad.notificaciones_vibracion,
        fecha_actualizacion=datetime.now()
    )

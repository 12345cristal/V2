# app/api/v1/endpoints/padre/tareas.py
"""
Router para gestión de Tareas desde el módulo Padre
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db_session, require_padre
from app.models.usuario import Usuario
from app.models.tutor import Tutor
from app.models.nino import Nino
from app.schemas.padre import Tarea, TareaUpdate, TareasListResponse
from app.schemas.enums import EstadoTarea


router = APIRouter()


def verificar_acceso_hijo(hijo_id: int, current_user: Usuario, db: Session) -> Nino:
    """Helper para verificar que el padre tenga acceso al hijo"""
    hijo = db.query(Nino).filter(Nino.id == hijo_id).first()
    if not hijo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hijo no encontrado"
        )
    
    if current_user.rol_id == 4:
        tutor = db.query(Tutor).filter(Tutor.usuario_id == current_user.id).first()
        if not tutor or hijo.tutor_id != tutor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para acceder a esta información"
            )
    
    return hijo


@router.get("/tareas/{hijo_id}", response_model=List[Tarea])
async def listar_tareas(
    hijo_id: int,
    estado: Optional[EstadoTarea] = Query(None),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Lista todas las tareas del hijo con filtro opcional por estado
    """
    hijo = verificar_acceso_hijo(hijo_id, current_user, db)
    
    # TODO: Implementar modelo de tareas y consulta real
    # Por ahora retornar lista vacía
    tareas = []
    
    return tareas


@router.get("/tareas/detalle/{tarea_id}", response_model=Tarea)
async def obtener_detalle_tarea(
    tarea_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene detalle de una tarea específica
    """
    # TODO: Implementar lógica real
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tarea no encontrada"
    )


@router.put("/tareas/{tarea_id}/estado")
async def actualizar_estado_tarea(
    tarea_id: int,
    tarea_update: TareaUpdate,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Marca una tarea como realizada o actualiza su estado
    """
    # TODO: Implementar lógica real
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Tarea no encontrada"
    )


@router.get("/tareas/{tarea_id}/recursos")
async def obtener_recursos_tarea(
    tarea_id: int,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(require_padre)
):
    """
    Obtiene recursos asociados a una tarea
    """
    # TODO: Implementar lógica real
    return {"message": "Funcionalidad en desarrollo", "recursos": []}

"""
Endpoints para recursos educativos
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.recurso import (
    RecursoInDB,
    RecursoCreate,
    RecursoUpdate,
    TareaRecursoInDB,
    TareaRecursoCreate,
)
from app.services.recurso_service import recurso_service


router = APIRouter()


@router.get("/recursos", response_model=list)
async def listar_recursos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Buscar en título, descripción, etiquetas"),
    tipo_id: Optional[int] = Query(None),
    categoria_id: Optional[int] = Query(None),
    nivel_id: Optional[int] = Query(None),
    es_destacado: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:ver")),
):
    """
    Listar recursos educativos con filtros.
    
    **Permisos requeridos:** `recursos:ver`
    """
    return recurso_service.get_recurso_list(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        tipo_id=tipo_id,
        categoria_id=categoria_id,
        nivel_id=nivel_id,
        es_destacado=es_destacado,
    )


@router.post("/recursos", response_model=RecursoInDB, status_code=status.HTTP_201_CREATED)
async def crear_recurso(
    recurso_data: RecursoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:crear")),
):
    """
    Crear nuevo recurso educativo.
    
    **Permisos requeridos:** `recursos:crear`
    """
    return recurso_service.create_recurso(db=db, recurso_data=recurso_data)


@router.get("/recursos/{recurso_id}", response_model=RecursoInDB)
async def obtener_recurso(
    recurso_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:ver")),
):
    """Obtener recurso por ID"""
    return recurso_service.get_recurso_by_id(db=db, recurso_id=recurso_id)


@router.put("/recursos/{recurso_id}", response_model=RecursoInDB)
async def actualizar_recurso(
    recurso_id: int,
    recurso_data: RecursoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:editar")),
):
    """Actualizar recurso"""
    return recurso_service.update_recurso(db=db, recurso_id=recurso_id, recurso_data=recurso_data)


@router.delete("/recursos/{recurso_id}")
async def eliminar_recurso(
    recurso_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:eliminar")),
):
    """Eliminar recurso"""
    return recurso_service.delete_recurso(db=db, recurso_id=recurso_id)


@router.post("/recursos/asignar-tarea", response_model=TareaRecursoInDB, status_code=status.HTTP_201_CREATED)
async def asignar_tarea(
    tarea_data: TareaRecursoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:asignar")),
):
    """Asignar recurso como tarea a un niño"""
    return recurso_service.asignar_tarea(db=db, tarea_data=tarea_data)


@router.get("/recursos/tareas/nino/{nino_id}")
async def obtener_tareas_nino(
    nino_id: int,
    completado: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:ver")),
):
    """Obtener tareas asignadas a un niño"""
    return recurso_service.get_tareas_nino(db=db, nino_id=nino_id, completado=completado)


@router.post("/recursos/tareas/{tarea_id}/completar")
async def marcar_tarea_completada(
    tarea_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("recursos:completar")),
):
    """Marcar tarea como completada"""
    return recurso_service.marcar_tarea_completada(db=db, tarea_id=tarea_id)

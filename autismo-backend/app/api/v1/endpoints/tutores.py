"""
Endpoints para tutores/padres
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_active_user, require_permissions
from app.models.usuario import Usuario
from app.schemas.tutor import TutorWithUsuario, TutorCreate, TutorUpdate
from app.services.tutor_service import tutor_service


router = APIRouter()


# ============= ENDPOINTS =============

@router.get("/tutores", response_model=dict)
async def listar_tutores(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Límite de registros"),
    search: Optional[str] = Query(None, description="Buscar por nombre, teléfono o email"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus (ACTIVO/INACTIVO)"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:ver")),
):
    """
    Listar tutores con filtros y paginación.
    
    **Permisos requeridos:** `tutores:ver`
    
    **Filtros disponibles:**
    - `search`: Busca en nombres, apellidos, teléfono, email
    - `estatus`: ACTIVO o INACTIVO
    
    **Retorna:**
    - `items`: Lista de tutores
    - `total`: Total de registros (con filtros aplicados)
    - `skip`: Registros saltados
    - `limit`: Límite aplicado
    """
    tutores = tutor_service.get_tutor_list(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        estatus=estatus,
    )
    
    total = tutor_service.count_tutores(
        db=db,
        search=search,
        estatus=estatus,
    )
    
    return {
        "items": tutores,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/tutores", response_model=TutorWithUsuario, status_code=status.HTTP_201_CREATED)
async def crear_tutor(
    tutor_data: TutorCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:crear")),
):
    """
    Crear nuevo tutor.
    
    **Permisos requeridos:** `tutores:crear`
    
    **Validaciones:**
    - El usuario debe existir
    - El usuario no debe tener ya un tutor asociado
    
    **Retorna:** Tutor creado con relaciones
    """
    return tutor_service.create_tutor(db=db, tutor_data=tutor_data)


@router.get("/tutores/{tutor_id}", response_model=TutorWithUsuario)
async def obtener_tutor(
    tutor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:ver")),
):
    """
    Obtener tutor por ID.
    
    **Permisos requeridos:** `tutores:ver`
    
    **Retorna:** Tutor con usuario y niños asociados
    """
    return tutor_service.get_tutor_by_id(db=db, tutor_id=tutor_id)


@router.put("/tutores/{tutor_id}", response_model=TutorWithUsuario)
async def actualizar_tutor(
    tutor_id: int,
    tutor_data: TutorUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:editar")),
):
    """
    Actualizar tutor.
    
    **Permisos requeridos:** `tutores:editar`
    
    **Nota:** Solo se actualizan los campos proporcionados (partial update).
    
    **Retorna:** Tutor actualizado
    """
    return tutor_service.update_tutor(
        db=db,
        tutor_id=tutor_id,
        tutor_data=tutor_data,
    )


@router.delete("/tutores/{tutor_id}")
async def eliminar_tutor(
    tutor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:eliminar")),
):
    """
    Eliminar tutor (soft delete).
    
    **Permisos requeridos:** `tutores:eliminar`
    
    **Nota:** No se elimina físicamente, solo se marca como INACTIVO.
    
    **Retorna:** Mensaje de confirmación
    """
    return tutor_service.delete_tutor(db=db, tutor_id=tutor_id)


@router.get("/tutores/{tutor_id}/ninos")
async def obtener_ninos_tutor(
    tutor_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:ver")),
):
    """
    Obtener niños asociados a un tutor.
    
    **Permisos requeridos:** `tutores:ver`
    
    **Retorna:** Lista de niños
    """
    return tutor_service.get_ninos_by_tutor(db=db, tutor_id=tutor_id)


@router.get("/tutores/usuario/{usuario_id}", response_model=TutorWithUsuario)
async def obtener_tutor_por_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:ver")),
):
    """
    Obtener tutor por ID de usuario.
    
    **Permisos requeridos:** `tutores:ver`
    
    **Retorna:** Tutor asociado al usuario o 404 si no existe
    """
    tutor = tutor_service.get_tutor_by_usuario_id(db=db, usuario_id=usuario_id)
    
    if not tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe tutor para el usuario {usuario_id}",
        )
    
    return tutor


@router.get("/tutores/{tutor_id}/tiene-acceso/{nino_id}")
async def verificar_acceso_nino(
    tutor_id: int,
    nino_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_active_user),
    __: None = Depends(require_permissions("tutores:ver")),
):
    """
    Verificar si un tutor tiene acceso a un niño.
    
    **Permisos requeridos:** `tutores:ver`
    
    **Uso:** Para validar que un padre puede ver información de un niño específico.
    
    **Retorna:**
    - `tiene_acceso`: bool
    - `tutor_id`: int
    - `nino_id`: int
    """
    tiene_acceso = tutor_service.verificar_acceso_nino(
        db=db,
        tutor_id=tutor_id,
        nino_id=nino_id,
    )
    
    return {
        "tiene_acceso": tiene_acceso,
        "tutor_id": tutor_id,
        "nino_id": nino_id,
    }

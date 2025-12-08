"""
Endpoints para gestión de personal (terapeutas)
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import require_permissions
from app.services import personal_service
from app.schemas.personal import (
    PersonalCreate,
    PersonalUpdate,
    PersonalInDB,
    PersonalCompleto,
    PersonalList,
    PersonalPerfilCreate,
    PersonalPerfilUpdate,
    PersonalPerfilInDB,
    PersonalHorarioCreate,
    PersonalHorarioUpdate,
    PersonalHorarioInDB,
)


router = APIRouter()


@router.get("/personal", response_model=dict)
async def listar_personal(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar por nombre"),
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus (ACTIVO, INACTIVO, LICENCIA)"),
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:ver")),
):
    """
    Listar personal con filtros opcionales.
    
    **Permisos requeridos:** `personal:ver`
    """
    personal_list = personal_service.get_personal_list(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        especialidad=especialidad,
        estatus=estatus,
    )
    
    total = personal_service.count_personal(
        db=db,
        search=search,
        especialidad=especialidad,
        estatus=estatus,
    )
    
    # Construir respuesta
    items = []
    for personal in personal_list:
        item = {
            "id": personal.id,
            "usuario_id": personal.usuario_id,
            "nombres": personal.usuario.nombres if personal.usuario else None,
            "apellido_paterno": personal.usuario.apellido_paterno if personal.usuario else None,
            "apellido_materno": personal.usuario.apellido_materno if personal.usuario else None,
            "email": personal.usuario.email if personal.usuario else None,
            "telefono": personal.usuario.telefono if personal.usuario else None,
            "especialidad": personal.especialidad,
            "anos_experiencia": personal.anos_experiencia,
            "estatus": personal.estatus,
        }
        items.append(item)
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/personal", response_model=PersonalCompleto, status_code=status.HTTP_201_CREATED)
async def crear_personal(
    personal_data: PersonalCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:crear")),
):
    """
    Crear nuevo personal (terapeuta).
    
    **Permisos requeridos:** `personal:crear`
    
    **Nota:** El usuario debe existir previamente y tener rol TERAPEUTA.
    """
    personal = personal_service.create_personal(db=db, personal_data=personal_data)
    
    return {
        "id": personal.id,
        "usuario_id": personal.usuario_id,
        "nombres": personal.usuario.nombres if personal.usuario else None,
        "apellido_paterno": personal.usuario.apellido_paterno if personal.usuario else None,
        "apellido_materno": personal.usuario.apellido_materno if personal.usuario else None,
        "email": personal.usuario.email if personal.usuario else None,
        "telefono": personal.usuario.telefono if personal.usuario else None,
        "especialidad": personal.especialidad,
        "certificaciones": personal.certificaciones,
        "anos_experiencia": personal.anos_experiencia,
        "numero_licencia": personal.numero_licencia,
        "estatus": personal.estatus,
        "perfil": None,
        "horarios": [],
    }


@router.get("/personal/{personal_id}", response_model=PersonalCompleto)
async def obtener_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:ver")),
):
    """
    Obtener personal por ID con perfil y horarios.
    
    **Permisos requeridos:** `personal:ver`
    """
    personal = personal_service.get_personal_by_id(db=db, personal_id=personal_id)
    
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personal con ID {personal_id} no encontrado",
        )
    
    return {
        "id": personal.id,
        "usuario_id": personal.usuario_id,
        "nombres": personal.usuario.nombres if personal.usuario else None,
        "apellido_paterno": personal.usuario.apellido_paterno if personal.usuario else None,
        "apellido_materno": personal.usuario.apellido_materno if personal.usuario else None,
        "email": personal.usuario.email if personal.usuario else None,
        "telefono": personal.usuario.telefono if personal.usuario else None,
        "especialidad": personal.especialidad,
        "certificaciones": personal.certificaciones,
        "anos_experiencia": personal.anos_experiencia,
        "numero_licencia": personal.numero_licencia,
        "estatus": personal.estatus,
        "perfil": personal.perfil,
        "horarios": personal.horarios,
    }


@router.put("/personal/{personal_id}", response_model=PersonalCompleto)
async def actualizar_personal(
    personal_id: int,
    personal_data: PersonalUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Actualizar datos de personal existente.
    
    **Permisos requeridos:** `personal:editar`
    """
    personal = personal_service.update_personal(
        db=db,
        personal_id=personal_id,
        personal_data=personal_data,
    )
    
    return {
        "id": personal.id,
        "usuario_id": personal.usuario_id,
        "nombres": personal.usuario.nombres if personal.usuario else None,
        "apellido_paterno": personal.usuario.apellido_paterno if personal.usuario else None,
        "apellido_materno": personal.usuario.apellido_materno if personal.usuario else None,
        "email": personal.usuario.email if personal.usuario else None,
        "telefono": personal.usuario.telefono if personal.usuario else None,
        "especialidad": personal.especialidad,
        "certificaciones": personal.certificaciones,
        "anos_experiencia": personal.anos_experiencia,
        "numero_licencia": personal.numero_licencia,
        "estatus": personal.estatus,
        "perfil": personal.perfil,
        "horarios": personal.horarios,
    }


@router.delete("/personal/{personal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:eliminar")),
):
    """
    Eliminar personal (soft delete - marca como INACTIVO).
    
    **Permisos requeridos:** `personal:eliminar`
    """
    personal_service.delete_personal(db=db, personal_id=personal_id)
    return None


# ============= ENDPOINTS DE PERFIL =============

@router.post("/personal/{personal_id}/perfil", response_model=PersonalPerfilInDB, status_code=status.HTTP_201_CREATED)
async def crear_perfil_personal(
    personal_id: int,
    perfil_data: PersonalPerfilCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Crear perfil para personal.
    
    **Permisos requeridos:** `personal:editar`
    
    **Nota:** Sobrescribe personal_id del body con el de la URL.
    """
    perfil_data.personal_id = personal_id
    perfil = personal_service.create_perfil(db=db, personal_id=personal_id, perfil_data=perfil_data)
    return perfil


@router.put("/personal/{personal_id}/perfil", response_model=PersonalPerfilInDB)
async def actualizar_perfil_personal(
    personal_id: int,
    perfil_data: PersonalPerfilUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Actualizar perfil de personal.
    
    **Permisos requeridos:** `personal:editar`
    """
    perfil = personal_service.update_perfil(db=db, personal_id=personal_id, perfil_data=perfil_data)
    return perfil


# ============= ENDPOINTS DE HORARIOS =============

@router.get("/personal/{personal_id}/horarios", response_model=List[PersonalHorarioInDB])
async def listar_horarios_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:ver")),
):
    """
    Obtener horarios de un personal.
    
    **Permisos requeridos:** `personal:ver`
    """
    return personal_service.get_horarios_by_personal(db=db, personal_id=personal_id)


@router.post("/personal/horarios", response_model=PersonalHorarioInDB, status_code=status.HTTP_201_CREATED)
async def crear_horario_personal(
    horario_data: PersonalHorarioCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Crear horario para personal.
    
    **Permisos requeridos:** `personal:editar`
    """
    return personal_service.create_horario(db=db, horario_data=horario_data)


@router.put("/personal/horarios/{horario_id}", response_model=PersonalHorarioInDB)
async def actualizar_horario_personal(
    horario_id: int,
    horario_data: PersonalHorarioUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Actualizar horario de personal.
    
    **Permisos requeridos:** `personal:editar`
    """
    return personal_service.update_horario(db=db, horario_id=horario_id, horario_data=horario_data)


@router.delete("/personal/horarios/{horario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_horario_personal(
    horario_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_permissions("personal:editar")),
):
    """
    Eliminar horario de personal.
    
    **Permisos requeridos:** `personal:editar`
    """
    personal_service.delete_horario(db=db, horario_id=horario_id)
    return None

# app/api/v1/endpoints/terapias.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.terapia import Terapia, TerapiaPersonal, TipoTerapia
from app.models.personal import Personal
from app.schemas.terapia import (
    TerapiaCreate,
    TerapiaUpdate,
    TerapiaRead,
    TerapiaPersonalCreate,
    TerapiaPersonalRead,
    PersonalDisponible,
    PersonalAsignado,
    TipoTerapiaRead
)

router = APIRouter()


# ============================================================
# CRUD TERAPIAS
# ============================================================

@router.get("", response_model=List[TerapiaRead])
def listar_terapias(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todas las terapias registradas
    """
    terapias = db.query(Terapia).all()
    return [TerapiaRead.from_orm_with_estado(t) for t in terapias]


# ============================================================
# ENDPOINTS ESPECÍFICOS (ANTES DE /{id} para evitar conflictos)
# ============================================================

@router.get("/personal-asignado", response_model=List[PersonalAsignado])
def listar_personal_asignado(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene el listado de personal con sus terapias asignadas
    """
    try:
        query = db.query(
            Personal.id.label('id_personal'),
            Personal.nombres,
            Personal.apellido_paterno,
            Personal.apellido_materno,
            Personal.especialidad_principal,
            Terapia.nombre.label('terapia_nombre'),
            Terapia.id.label('id_terapia')
        ).join(
            TerapiaPersonal, TerapiaPersonal.personal_id == Personal.id
        ).join(
            Terapia, TerapiaPersonal.terapia_id == Terapia.id
        ).filter(
            TerapiaPersonal.activo == 1
        ).all()

        resultado = []
        for row in query:
            nombre_completo = f"{row.nombres} {row.apellido_paterno}"
            if row.apellido_materno:
                nombre_completo += f" {row.apellido_materno}"
            
            resultado.append(PersonalAsignado(
                id_personal=row.id_personal,
                nombre_completo=nombre_completo,
                terapia=row.terapia_nombre,
                id_terapia=row.id_terapia
            ))

        return resultado
    except Exception as e:
        # Si hay error, devolver lista vacía en lugar de fallar
        return []


@router.get("/catalogos/tipos", response_model=List[TipoTerapiaRead])
def listar_tipos_terapia(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene el catálogo de tipos de terapia
    """
    tipos = db.query(TipoTerapia).all()
    return tipos


@router.get("/{terapia_id}", response_model=TerapiaRead)
def obtener_terapia(
    terapia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene una terapia por su ID
    """
    terapia = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not terapia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapia no encontrada"
        )
    return TerapiaRead.from_orm_with_estado(terapia)


@router.post("", response_model=TerapiaRead, status_code=status.HTTP_201_CREATED)
def crear_terapia(
    terapia_in: TerapiaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea una nueva terapia
    """
    # Verificar que el tipo de terapia existe
    tipo = db.query(TipoTerapia).filter(TipoTerapia.id == terapia_in.tipo_id).first()
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de terapia no válido"
        )

    nueva_terapia = Terapia(
        nombre=terapia_in.nombre,
        descripcion=terapia_in.descripcion,
        tipo_id=terapia_in.tipo_id,
        duracion_minutos=terapia_in.duracion_minutos,
        objetivo_general=terapia_in.objetivo_general,
        activo=1
    )
    
    db.add(nueva_terapia)
    db.commit()
    db.refresh(nueva_terapia)
    
    return TerapiaRead.from_orm_with_estado(nueva_terapia)


@router.put("/{terapia_id}", response_model=TerapiaRead)
def actualizar_terapia(
    terapia_id: int,
    terapia_in: TerapiaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza una terapia existente
    """
    terapia = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not terapia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapia no encontrada"
        )

    update_data = terapia_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(terapia, field, value)

    db.commit()
    db.refresh(terapia)
    
    return TerapiaRead.from_orm_with_estado(terapia)


@router.patch("/{terapia_id}/estado", response_model=TerapiaRead)
def cambiar_estado_terapia(
    terapia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cambia el estado de una terapia (activo/inactivo)
    """
    terapia = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not terapia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapia no encontrada"
        )

    terapia.activo = 0 if terapia.activo == 1 else 1
    db.commit()
    db.refresh(terapia)
    
    return TerapiaRead.from_orm_with_estado(terapia)


@router.delete("/{terapia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_terapia(
    terapia_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina una terapia (soft delete - marca como inactiva)
    """
    terapia = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not terapia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapia no encontrada"
        )

    terapia.activo = 0
    db.commit()
    
    return None


# ============================================================
# ASIGNACIÓN DE PERSONAL
# ============================================================

@router.post("/asignar", response_model=TerapiaPersonalRead, status_code=status.HTTP_201_CREATED)
def asignar_personal(
    asignacion: TerapiaPersonalCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Asigna un personal (terapeuta) a una terapia
    """
    # Verificar que la terapia existe
    terapia = db.query(Terapia).filter(Terapia.id == asignacion.id_terapia).first()
    if not terapia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Terapia no encontrada"
        )

    # Verificar que el personal existe
    personal = db.query(Personal).filter(Personal.id == asignacion.id_personal).first()
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal no encontrado"
        )

    # Verificar si ya existe la asignación
    existe = db.query(TerapiaPersonal).filter(
        TerapiaPersonal.terapia_id == asignacion.id_terapia,
        TerapiaPersonal.personal_id == asignacion.id_personal
    ).first()

    if existe:
        # Si existe pero está inactiva, reactivarla
        if existe.activo == 0:
            existe.activo = 1
            db.commit()
            db.refresh(existe)
            return TerapiaPersonalRead(
                id=existe.id,
                id_personal=existe.personal_id,
                id_terapia=existe.terapia_id,
                activo=existe.activo
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El personal ya está asignado a esta terapia"
            )

    nueva_asignacion = TerapiaPersonal(
        terapia_id=asignacion.id_terapia,
        personal_id=asignacion.id_personal,
        activo=1
    )
    
    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    
    return TerapiaPersonalRead(
        id=nueva_asignacion.id,
        id_personal=nueva_asignacion.personal_id,
        id_terapia=nueva_asignacion.terapia_id,
        activo=nueva_asignacion.activo
    )

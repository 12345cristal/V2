# app/api/v1/routers/terapias_nino.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.terapia import TerapiaNino, Terapia, Prioridad
from app.models.nino import Nino
from app.models.personal import Personal
from app.schemas.terapia import (
    TerapiaNinoCreate,
    TerapiaNinoUpdate,
    TerapiaNinoResponse
)

router = APIRouter(prefix="/terapias-nino", tags=["Terapias Niño"])


# ==================== FUNCIONES AUXILIARES ====================

def construir_respuesta_terapia_nino(tn: TerapiaNino) -> dict:
    """Construye diccionario de respuesta para terapia_nino"""
    return {
        "id": tn.id,
        "ninoId": tn.nino_id,
        "terapiaId": tn.terapia_id,
        "terapeutaId": tn.terapeuta_id,
        "prioridadId": tn.prioridad_id,
        "frecuenciaSemana": tn.frecuencia_semana,
        "fechaAsignacion": tn.fecha_asignacion,
        "activo": tn.activo,
        "terapiaNombre": tn.terapia.nombre if tn.terapia else None,
        "terapiaDescripcion": tn.terapia.descripcion if tn.terapia else None,
        "terapiaDuracion": tn.terapia.duracion_minutos if tn.terapia else None,
        "ninoNombre": f"{tn.nino.nombre} {tn.nino.apellido_paterno}" if tn.nino else None,
        "terapeutaNombre": f"{tn.terapeuta.nombres} {tn.terapeuta.apellido_paterno}" if tn.terapeuta else None,
        "prioridadNombre": tn.prioridad.nombre if tn.prioridad else None
    }


# ==================== ENDPOINTS ====================

@router.get("/nino/{nino_id}", response_model=List[TerapiaNinoResponse])
def listar_terapias_nino(
    nino_id: int,
    activo: Optional[int] = Query(None, description="Filtrar por activo (0/1)"),
    db: Session = Depends(get_db)
):
    """Lista todas las terapias asignadas a un niño"""
    # Verificar que el niño existe
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    query = db.query(TerapiaNino).options(
        joinedload(TerapiaNino.terapia),
        joinedload(TerapiaNino.nino),
        joinedload(TerapiaNino.terapeuta),
        joinedload(TerapiaNino.prioridad)
    ).filter(TerapiaNino.nino_id == nino_id)
    
    if activo is not None:
        query = query.filter(TerapiaNino.activo == activo)
    
    # Ordenar por prioridad y fecha de asignación
    query = query.order_by(TerapiaNino.prioridad_id, TerapiaNino.fecha_asignacion.desc())
    
    terapias = query.all()
    
    return [construir_respuesta_terapia_nino(tn) for tn in terapias]


@router.get("/activas/nino/{nino_id}", response_model=List[TerapiaNinoResponse])
def listar_terapias_activas_nino(nino_id: int, db: Session = Depends(get_db)):
    """Lista solo las terapias activas de un niño"""
    return listar_terapias_nino(nino_id, activo=1, db=db)


@router.get("/{terapia_nino_id}", response_model=TerapiaNinoResponse)
def obtener_terapia_nino(terapia_nino_id: int, db: Session = Depends(get_db)):
    """Obtiene una asignación de terapia por ID"""
    tn = db.query(TerapiaNino).options(
        joinedload(TerapiaNino.terapia),
        joinedload(TerapiaNino.nino),
        joinedload(TerapiaNino.terapeuta),
        joinedload(TerapiaNino.prioridad)
    ).filter(TerapiaNino.id == terapia_nino_id).first()
    
    if not tn:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    
    return construir_respuesta_terapia_nino(tn)


@router.post("", response_model=TerapiaNinoResponse, status_code=201)
def asignar_terapia(terapia_data: TerapiaNinoCreate, db: Session = Depends(get_db)):
    """Asigna una terapia a un niño"""
    # Validar niño
    nino = db.query(Nino).filter(Nino.id == terapia_data.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Validar terapia
    terapia = db.query(Terapia).filter(Terapia.id == terapia_data.terapia_id).first()
    if not terapia:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    
    # Validar terapeuta si se proporciona
    if terapia_data.terapeuta_id:
        terapeuta = db.query(Personal).filter(Personal.id == terapia_data.terapeuta_id).first()
        if not terapeuta:
            raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Validar prioridad
    prioridad = db.query(Prioridad).filter(Prioridad.id == terapia_data.prioridad_id).first()
    if not prioridad:
        raise HTTPException(status_code=404, detail="Prioridad no encontrada")
    
    # Verificar si ya existe una asignación activa
    existe = db.query(TerapiaNino).filter(
        TerapiaNino.nino_id == terapia_data.nino_id,
        TerapiaNino.terapia_id == terapia_data.terapia_id,
        TerapiaNino.activo == 1
    ).first()
    
    if existe:
        raise HTTPException(
            status_code=400,
            detail="El niño ya tiene esta terapia asignada y activa"
        )
    
    # Crear asignación
    nueva_terapia_nino = TerapiaNino(
        nino_id=terapia_data.nino_id,
        terapia_id=terapia_data.terapia_id,
        terapeuta_id=terapia_data.terapeuta_id,
        prioridad_id=terapia_data.prioridad_id,
        frecuencia_semana=terapia_data.frecuencia_semana,
        fecha_asignacion=terapia_data.fecha_asignacion or datetime.utcnow().isoformat()
    )
    
    db.add(nueva_terapia_nino)
    db.commit()
    db.refresh(nueva_terapia_nino)
    
    return obtener_terapia_nino(nueva_terapia_nino.id, db)


@router.put("/{terapia_nino_id}", response_model=TerapiaNinoResponse)
def actualizar_terapia_nino(
    terapia_nino_id: int,
    terapia_data: TerapiaNinoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una asignación de terapia"""
    tn = db.query(TerapiaNino).filter(TerapiaNino.id == terapia_nino_id).first()
    
    if not tn:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    
    # Validar terapeuta si se cambia
    if terapia_data.terapeuta_id is not None:
        terapeuta = db.query(Personal).filter(Personal.id == terapia_data.terapeuta_id).first()
        if not terapeuta:
            raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Validar prioridad si se cambia
    if terapia_data.prioridad_id is not None:
        prioridad = db.query(Prioridad).filter(Prioridad.id == terapia_data.prioridad_id).first()
        if not prioridad:
            raise HTTPException(status_code=404, detail="Prioridad no encontrada")
    
    # Actualizar campos proporcionados
    update_data = terapia_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tn, key, value)
    
    db.commit()
    db.refresh(tn)
    
    return obtener_terapia_nino(terapia_nino_id, db)


@router.delete("/{terapia_nino_id}", status_code=204)
def desactivar_terapia_nino(terapia_nino_id: int, db: Session = Depends(get_db)):
    """Desactiva una terapia asignada a un niño"""
    tn = db.query(TerapiaNino).filter(TerapiaNino.id == terapia_nino_id).first()
    
    if not tn:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    
    # Marcar como inactiva
    tn.activo = 0
    db.commit()
    
    return None


@router.post("/{terapia_nino_id}/reactivar", response_model=TerapiaNinoResponse)
def reactivar_terapia_nino(terapia_nino_id: int, db: Session = Depends(get_db)):
    """Reactiva una terapia desactivada"""
    tn = db.query(TerapiaNino).filter(TerapiaNino.id == terapia_nino_id).first()
    
    if not tn:
        raise HTTPException(status_code=404, detail="Terapia no encontrada")
    
    # Marcar como activa
    tn.activo = 1
    db.commit()
    db.refresh(tn)
    
    return obtener_terapia_nino(terapia_nino_id, db)


@router.get("/terapeuta/{terapeuta_id}/ninos", response_model=List[TerapiaNinoResponse])
def listar_ninos_terapeuta(
    terapeuta_id: int,
    activo: Optional[int] = Query(1, description="Filtrar por activo (0/1)"),
    db: Session = Depends(get_db)
):
    """Lista todos los niños asignados a un terapeuta"""
    # Verificar que el terapeuta existe
    terapeuta = db.query(Personal).filter(Personal.id == terapeuta_id).first()
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    query = db.query(TerapiaNino).options(
        joinedload(TerapiaNino.terapia),
        joinedload(TerapiaNino.nino),
        joinedload(TerapiaNino.terapeuta),
        joinedload(TerapiaNino.prioridad)
    ).filter(TerapiaNino.terapeuta_id == terapeuta_id)
    
    if activo is not None:
        query = query.filter(TerapiaNino.activo == activo)
    
    # Ordenar por niño
    query = query.order_by(TerapiaNino.nino_id)
    
    terapias = query.all()
    
    return [construir_respuesta_terapia_nino(tn) for tn in terapias]

# app/api/v1/routers/tareas_recurso.py
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from pathlib import Path
import uuid
import shutil

from app.db.session import get_db
from app.models.tarea_recurso import TareaRecurso
from app.models.recurso import Recurso
from app.models.nino import Nino
from app.models.personal import Personal
from app.schemas.tarea_recurso import (
    TareaRecursoCreate,
    TareaRecursoUpdate,
    TareaRecursoMarcarCompletada,
    TareaRecursoResponse,
    TareaRecursoListItem,
    EstadisticasTareasResponse
)

router = APIRouter(prefix="/tareas-recurso", tags=["Tareas Recurso"])

# Directorio para evidencias
EVIDENCIAS_DIR = Path("uploads/tareas_recurso/evidencias")
EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)


# ==================== FUNCIONES AUXILIARES ====================

def guardar_evidencia(file: UploadFile) -> tuple[str, str]:
    """Guarda archivo de evidencia y retorna (url, tipo)"""
    extension = file.filename.split('.')[-1].lower() if file.filename else 'bin'
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    
    ruta_archivo = EVIDENCIAS_DIR / nombre_unico
    
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determinar tipo
    content_type = file.content_type or ""
    if any(t in content_type for t in ["image", "png", "jpg", "jpeg"]):
        tipo = "imagen"
    elif "video" in content_type:
        tipo = "video"
    elif "pdf" in content_type or extension == "pdf":
        tipo = "pdf"
    else:
        tipo = "archivo"
    
    url = f"/archivos/tareas_recurso/evidencias/{nombre_unico}"
    return url, tipo


def construir_respuesta_tarea(tarea: TareaRecurso) -> dict:
    """Construye diccionario de respuesta para una tarea"""
    return {
        "id": tarea.id,
        "recurso_id": tarea.recurso_id,
        "nino_id": tarea.nino_id,
        "asignado_por": tarea.asignado_por,
        "fecha_asignacion": tarea.fecha_asignacion,
        "fecha_limite": tarea.fecha_limite,
        "fecha_completado": tarea.fecha_completado,
        "completado": tarea.completado,
        "comentarios_padres": tarea.comentarios_padres,
        "notas_terapeuta": tarea.notas_terapeuta,
        "evidencia_url": tarea.evidencia_url,
        "evidencia_tipo": tarea.evidencia_tipo,
        "recurso_titulo": tarea.recurso.titulo if tarea.recurso else None,
        "recurso_descripcion": tarea.recurso.descripcion if tarea.recurso else None,
        "recurso_archivo_url": tarea.recurso.archivo_url if tarea.recurso else None,
        "recurso_tipo": tarea.recurso.tipo.nombre if tarea.recurso and tarea.recurso.tipo else None,
        "nino_nombre": tarea.nino.nombre if tarea.nino else None,
        "nino_apellido": f"{tarea.nino.apellido_paterno}" if tarea.nino else None,
        "asignador_nombre": f"{tarea.asignador.nombres} {tarea.asignador.apellido_paterno}" if tarea.asignador else None
    }


# ==================== ENDPOINTS ====================

@router.get("/nino/{nino_id}", response_model=List[TareaRecursoListItem])
def listar_tareas_nino(
    nino_id: int,
    completado: Optional[int] = Query(None, description="Filtrar por completado (0/1)"),
    vencidas: Optional[bool] = Query(None, description="Filtrar vencidas"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista todas las tareas asignadas a un niño"""
    # Verificar que el niño existe
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    query = db.query(TareaRecurso).options(
        joinedload(TareaRecurso.recurso).joinedload(Recurso.tipo),
        joinedload(TareaRecurso.nino),
        joinedload(TareaRecurso.asignador)
    ).filter(TareaRecurso.nino_id == nino_id)
    
    # Aplicar filtros
    if completado is not None:
        query = query.filter(TareaRecurso.completado == completado)
    
    if vencidas is not None:
        hoy = date.today()
        if vencidas:
            query = query.filter(
                TareaRecurso.completado == 0,
                TareaRecurso.fecha_limite < hoy
            )
        else:
            query = query.filter(
                (TareaRecurso.fecha_limite >= hoy) | (TareaRecurso.fecha_limite.is_(None))
            )
    
    # Ordenar: pendientes primero, luego completadas
    query = query.order_by(
        TareaRecurso.completado,
        TareaRecurso.fecha_limite.asc().nullslast()
    )
    
    tareas = query.offset(skip).limit(limit).all()
    
    # Construir respuesta
    result = []
    for tarea in tareas:
        result.append({
            "id": tarea.id,
            "recurso_id": tarea.recurso_id,
            "recurso_titulo": tarea.recurso.titulo if tarea.recurso else "Sin título",
            "recurso_tipo": tarea.recurso.tipo.nombre if tarea.recurso and tarea.recurso.tipo else None,
            "nino_id": tarea.nino_id,
            "nino_nombre": f"{tarea.nino.nombre} {tarea.nino.apellido_paterno}" if tarea.nino else "Sin nombre",
            "fecha_asignacion": tarea.fecha_asignacion,
            "fecha_limite": tarea.fecha_limite,
            "completado": tarea.completado,
            "asignador_nombre": f"{tarea.asignador.nombres} {tarea.asignador.apellido_paterno}" if tarea.asignador else None
        })
    
    return result


@router.get("/{tarea_id}", response_model=TareaRecursoResponse)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """Obtiene una tarea por ID con todos sus detalles"""
    tarea = db.query(TareaRecurso).options(
        joinedload(TareaRecurso.recurso).joinedload(Recurso.tipo),
        joinedload(TareaRecurso.nino),
        joinedload(TareaRecurso.asignador)
    ).filter(TareaRecurso.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    return construir_respuesta_tarea(tarea)


@router.post("", response_model=TareaRecursoResponse, status_code=201)
def crear_tarea(tarea_data: TareaRecursoCreate, db: Session = Depends(get_db)):
    """Asigna un recurso a un niño como tarea"""
    # Validar recurso
    recurso = db.query(Recurso).filter(Recurso.id == tarea_data.recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Validar niño
    nino = db.query(Nino).filter(Nino.id == tarea_data.nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Validar asignador si se proporciona
    if tarea_data.asignado_por:
        asignador = db.query(Personal).filter(Personal.id == tarea_data.asignado_por).first()
        if not asignador:
            raise HTTPException(status_code=404, detail="Asignador no encontrado")
    
    # Crear tarea
    nueva_tarea = TareaRecurso(
        recurso_id=tarea_data.recurso_id,
        nino_id=tarea_data.nino_id,
        asignado_por=tarea_data.asignado_por,
        fecha_limite=tarea_data.fecha_limite,
        notas_terapeuta=tarea_data.notas_terapeuta
    )
    
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    
    return obtener_tarea(nueva_tarea.id, db)


@router.put("/{tarea_id}", response_model=TareaRecursoResponse)
def actualizar_tarea(
    tarea_id: int,
    tarea_data: TareaRecursoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza una tarea existente"""
    tarea = db.query(TareaRecurso).filter(TareaRecurso.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Actualizar campos proporcionados
    update_data = tarea_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tarea, key, value)
    
    db.commit()
    db.refresh(tarea)
    
    return obtener_tarea(tarea_id, db)


@router.post("/{tarea_id}/completar", response_model=TareaRecursoResponse)
async def marcar_completada(
    tarea_id: int,
    comentarios_padres: Optional[str] = Form(None),
    evidencia: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Marca una tarea como completada con evidencia opcional"""
    tarea = db.query(TareaRecurso).filter(TareaRecurso.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if tarea.completado == 1:
        raise HTTPException(status_code=400, detail="La tarea ya está completada")
    
    # Marcar como completada
    tarea.completado = 1
    tarea.fecha_completado = datetime.utcnow()
    tarea.comentarios_padres = comentarios_padres
    
    # Guardar evidencia si se proporciona
    if evidencia and evidencia.filename:
        url, tipo = guardar_evidencia(evidencia)
        tarea.evidencia_url = url
        tarea.evidencia_tipo = tipo
    
    db.commit()
    db.refresh(tarea)
    
    return obtener_tarea(tarea_id, db)


@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """Elimina una tarea asignada"""
    tarea = db.query(TareaRecurso).filter(TareaRecurso.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(tarea)
    db.commit()
    
    return None


@router.get("/nino/{nino_id}/estadisticas", response_model=EstadisticasTareasResponse)
def obtener_estadisticas(nino_id: int, db: Session = Depends(get_db)):
    """Obtiene estadísticas de tareas de un niño"""
    # Verificar que el niño existe
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Contar tareas
    total = db.query(func.count(TareaRecurso.id)).filter(
        TareaRecurso.nino_id == nino_id
    ).scalar() or 0
    
    completadas = db.query(func.count(TareaRecurso.id)).filter(
        TareaRecurso.nino_id == nino_id,
        TareaRecurso.completado == 1
    ).scalar() or 0
    
    pendientes = db.query(func.count(TareaRecurso.id)).filter(
        TareaRecurso.nino_id == nino_id,
        TareaRecurso.completado == 0
    ).scalar() or 0
    
    # Tareas vencidas (pendientes con fecha límite pasada)
    hoy = date.today()
    vencidas = db.query(func.count(TareaRecurso.id)).filter(
        TareaRecurso.nino_id == nino_id,
        TareaRecurso.completado == 0,
        TareaRecurso.fecha_limite < hoy
    ).scalar() or 0
    
    # Calcular porcentaje
    porcentaje_completadas = (completadas / total * 100) if total > 0 else 0.0
    
    return {
        "total": total,
        "pendientes": pendientes,
        "completadas": completadas,
        "vencidas": vencidas,
        "porcentaje_completadas": round(porcentaje_completadas, 2)
    }

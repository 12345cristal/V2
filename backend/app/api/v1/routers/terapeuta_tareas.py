from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import uuid
import shutil

from app.db.session import get_db
from app.models.tarea import Tarea, RecursoTarea, EstadoTarea, TipoRecurso
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/terapeuta/tareas", tags=["Terapeuta - Tareas"])

RECURSOS_DIR = Path("uploads/tareas/recursos")
RECURSOS_DIR.mkdir(parents=True, exist_ok=True)

# ==================== MODELOS PYDANTIC ====================

class RecursoResponse(BaseModel):
    id: int
    titulo: str
    tipo: str
    url: str
    nombreArchivo: Optional[str] = None
    
    class Config:
        from_attributes = True

class TareaResponse(BaseModel):
    id: int
    hijoId: int
    objetivo: str
    instrucciones: str
    terapeuta: str
    fechaAsignacion: str
    fechaLimite: Optional[str] = None
    estado: str
    recursos: List[RecursoResponse] = []
    
    class Config:
        from_attributes = True

# ==================== FUNCIONES ====================

def guardar_recurso(file: UploadFile) -> tuple[str, str, str]:
    """Guarda recurso y retorna (url, nombre_archivo, tipo)."""
    extension = file.filename.split('.')[-1].lower() if file.filename else 'bin'
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    
    ruta_archivo = RECURSOS_DIR / nombre_unico
    
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determinar tipo
    content_type = file.content_type or ""
    if "pdf" in content_type or extension == "pdf":
        tipo = "PDF"
    elif any(t in content_type for t in ["image", "png", "jpg", "jpeg"]):
        tipo = "IMAGEN"
    elif "video" in content_type:
        tipo = "VIDEO"
    else:
        tipo = "ENLACE"
    
    url = f"http://localhost:8000/archivos/tareas/recursos/{nombre_unico}"
    return url, file.filename or nombre_unico, tipo

def tarea_to_response(tarea: Tarea) -> dict:
    """Convierte tarea a respuesta."""
    return {
        "id": tarea.id,
        "hijoId": tarea.hijo_id,
        "objetivo": tarea.objetivo,
        "instrucciones": tarea.instrucciones,
        "terapeuta": tarea.terapeuta.nombre if tarea.terapeuta else "Sin asignar",
        "fechaAsignacion": tarea.fecha_asignacion.isoformat(),
        "fechaLimite": tarea.fecha_limite.isoformat() if tarea.fecha_limite else None,
        "estado": tarea.estado.value,
        "recursos": [
            {
                "id": r.id,
                "titulo": r.titulo,
                "tipo": r.tipo.value,
                "url": r.url,
                "nombreArchivo": r.nombre_archivo
            }
            for r in tarea.recursos
        ]
    }

# ==================== ENDPOINTS ====================

@router.post("", response_model=TareaResponse, status_code=201)
async def crear_tarea(
    hijoId: int = Form(...),
    objetivo: str = Form(...),
    instrucciones: str = Form(...),
    terapeutaId: int = Form(...),
    fechaLimite: Optional[str] = Form(None),
    recursos: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    """Crea una nueva tarea asignada por el terapeuta."""
    # Validar terapeuta
    terapeuta = db.query(Usuario).filter(Usuario.id == terapeutaId).first()
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    # Validar hijo/paciente
    hijo = db.query(Paciente).filter(Paciente.id == hijoId).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Crear tarea
    fecha_limite_dt = None
    if fechaLimite:
        try:
            fecha_limite_dt = datetime.fromisoformat(fechaLimite)
        except:
            pass
    
    nueva_tarea = Tarea(
        hijo_id=hijoId,
        terapeuta_id=terapeutaId,
        objetivo=objetivo,
        instrucciones=instrucciones,
        fecha_limite=fecha_limite_dt,
        estado=EstadoTarea.PENDIENTE
    )
    
    db.add(nueva_tarea)
    db.flush()  # Para obtener el ID
    
    # Procesar recursos
    for recurso_file in recursos:
        if recurso_file.filename:
            url, nombre, tipo = guardar_recurso(recurso_file)
            
            recurso = RecursoTarea(
                tarea_id=nueva_tarea.id,
                titulo=nombre.split('.')[0],
                tipo=TipoRecurso[tipo],
                url=url,
                nombre_archivo=nombre
            )
            db.add(recurso)
    
    db.commit()
    db.refresh(nueva_tarea)
    
    # Cargar relaciones
    nueva_tarea = db.query(Tarea).filter(Tarea.id == nueva_tarea.id).options(
        joinedload(Tarea.terapeuta),
        joinedload(Tarea.recursos)
    ).first()
    
    # Notificar al padre (asumir que el padre tiene el mismo ID que el hijo por ahora)
    # En producción, deberías tener una tabla de relaciones padre-hijo
    from app.api.v1.routers.notificaciones import notificar_padre, MetadataNotificacion
    
    # Obtener padre del paciente (asumiendo que existe relación)
    # Por ahora uso el ID del paciente como padre_id
    padre_id = hijoId  # AJUSTAR según tu modelo de datos
    
    notificar_padre(
        db=db,
        padre_id=padre_id,
        hijo_id=hijoId,
        tipo="NUEVA_TAREA",
        mensaje=f"Nueva tarea asignada por {terapeuta.nombre}: {objetivo}",
        metadata=MetadataNotificacion(
            relacionadoId=nueva_tarea.id,
            relacionadoTipo="tarea",
            accion="ver_tarea",
            prioridad="media"
        )
    )
    
    return tarea_to_response(nueva_tarea)

@router.post("/{tarea_id}/recursos", response_model=RecursoResponse, status_code=201)
async def agregar_recurso(
    tarea_id: int,
    titulo: str = Form(...),
    recurso: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Agrega un recurso a una tarea existente."""
    # Buscar tarea
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # Guardar recurso
    url, nombre_archivo, tipo = guardar_recurso(recurso)
    
    nuevo_recurso = RecursoTarea(
        tarea_id=tarea_id,
        titulo=titulo,
        tipo=TipoRecurso[tipo],
        url=url,
        nombre_archivo=nombre_archivo
    )
    
    db.add(nuevo_recurso)
    db.commit()
    db.refresh(nuevo_recurso)
    
    # Notificar al padre
    from app.api.v1.routers.notificaciones import notificar_padre, MetadataNotificacion
    
    padre_id = tarea.hijo_id  # AJUSTAR según tu modelo
    
    notificar_padre(
        db=db,
        padre_id=padre_id,
        hijo_id=tarea.hijo_id,
        tipo="NUEVO_RECURSO",
        mensaje=f"Nuevo recurso agregado a la tarea: {tarea.objetivo}",
        metadata=MetadataNotificacion(
            relacionadoId=tarea_id,
            relacionadoTipo="tarea",
            accion="ver_recurso",
            prioridad="baja"
        )
    )
    
    return {
        "id": nuevo_recurso.id,
        "titulo": nuevo_recurso.titulo,
        "tipo": nuevo_recurso.tipo.value,
        "url": nuevo_recurso.url,
        "nombreArchivo": nuevo_recurso.nombre_archivo
    }

@router.get("/mis-tareas/{terapeuta_id}", response_model=List[TareaResponse])
def get_mis_tareas(terapeuta_id: int, db: Session = Depends(get_db)):
    """Obtiene todas las tareas creadas por un terapeuta."""
    # Verificar terapeuta
    terapeuta = db.query(Usuario).filter(Usuario.id == terapeuta_id).first()
    if not terapeuta:
        raise HTTPException(status_code=404, detail="Terapeuta no encontrado")
    
    tareas = db.query(Tarea).filter(
        Tarea.terapeuta_id == terapeuta_id
    ).options(
        joinedload(Tarea.terapeuta),
        joinedload(Tarea.recursos)
    ).order_by(Tarea.fecha_asignacion.desc()).all()
    
    return [tarea_to_response(t) for t in tareas]

@router.delete("/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """Elimina una tarea."""
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(tarea)
    db.commit()
    
    return None

@router.get("/hijo/{hijo_id}/estadisticas")
def get_estadisticas_tareas(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene estadísticas de tareas de un hijo."""
    tareas = db.query(Tarea).filter(Tarea.hijo_id == hijo_id).all()
    
    total = len(tareas)
    pendientes = sum(1 for t in tareas if t.estado == EstadoTarea.PENDIENTE)
    realizadas = sum(1 for t in tareas if t.estado == EstadoTarea.REALIZADA)
    vencidas = sum(1 for t in tareas if t.estado == EstadoTarea.VENCIDA)
    
    return {
        "total": total,
        "pendientes": pendientes,
        "realizadas": realizadas,
        "vencidas": vencidas,
        "porcentajeCompletadas": round((realizadas / total * 100), 2) if total > 0 else 0
    }
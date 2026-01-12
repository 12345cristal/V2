from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import uuid
import shutil

from app.db.session import get_db
from app.models.tarea import Tarea, RecursoTarea, EvidenciaTarea, EstadoTarea, TipoRecurso
from app.models.usuario import Usuario
from app.models.paciente import Paciente
from pydantic import BaseModel

router = APIRouter(prefix="/padre/tareas", tags=["Padre - Tareas"])

UPLOAD_DIR = Path("uploads/tareas")
EVIDENCIAS_DIR = UPLOAD_DIR / "evidencias"
EVIDENCIAS_DIR.mkdir(parents=True, exist_ok=True)

# ==================== MODELOS PYDANTIC ====================

class RecursoResponse(BaseModel):
    id: int
    titulo: str
    tipo: str
    url: str
    nombreArchivo: Optional[str] = None
    
    class Config:
        from_attributes = True

class EvidenciaResponse(BaseModel):
    id: int
    tipo: str
    url: str
    nombreArchivo: str
    fechaSubida: str
    
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
    evidencia: Optional[EvidenciaResponse] = None
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True

# ==================== FUNCIONES AUXILIARES ====================

def guardar_evidencia(file: UploadFile) -> tuple[str, str, str]:
    """Guarda archivo de evidencia y retorna (url, nombre_archivo, tipo)."""
    extension = file.filename.split('.')[-1].lower() if file.filename else 'bin'
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    
    ruta_archivo = EVIDENCIAS_DIR / nombre_unico
    
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determinar tipo
    content_type = file.content_type or ""
    if "pdf" in content_type or extension == "pdf":
        tipo = "PDF"
    elif any(t in content_type for t in ["image", "png", "jpg", "jpeg"]):
        tipo = "IMAGEN"
    else:
        tipo = "PDF"  # Default
    
    url = f"http://localhost:8000/archivos/tareas/evidencias/{nombre_unico}"
    return url, file.filename or nombre_unico, tipo

def tarea_to_response(tarea: Tarea) -> dict:
    """Convierte tarea de BD a diccionario de respuesta."""
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
        ],
        "evidencia": {
            "id": tarea.evidencia.id,
            "tipo": tarea.evidencia.tipo.value,
            "url": tarea.evidencia.url,
            "nombreArchivo": tarea.evidencia.nombre_archivo,
            "fechaSubida": tarea.evidencia.fecha_subida.isoformat()
        } if tarea.evidencia else None,
        "observaciones": tarea.observaciones
    }

def actualizar_estados_vencidas(db: Session, hijo_id: int):
    """Actualiza tareas pendientes vencidas."""
    ahora = datetime.now()
    
    tareas_vencidas = db.query(Tarea).filter(
        Tarea.hijo_id == hijo_id,
        Tarea.estado == EstadoTarea.PENDIENTE,
        Tarea.fecha_limite < ahora
    ).all()
    
    for tarea in tareas_vencidas:
        tarea.estado = EstadoTarea.VENCIDA
    
    if tareas_vencidas:
        db.commit()

# ==================== ENDPOINTS ====================

@router.get("/{hijo_id}", response_model=List[TareaResponse])
def get_tareas(hijo_id: int, db: Session = Depends(get_db)):
    """Obtiene todas las tareas de un hijo."""
    # Verificar que el hijo existe
    hijo = db.query(Paciente).filter(Paciente.id == hijo_id).first()
    if not hijo:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    # Actualizar estados vencidos
    actualizar_estados_vencidas(db, hijo_id)
    
    # Obtener tareas con relaciones cargadas
    tareas = db.query(Tarea).filter(
        Tarea.hijo_id == hijo_id
    ).options(
        joinedload(Tarea.terapeuta),
        joinedload(Tarea.recursos),
        joinedload(Tarea.evidencia)
    ).all()
    
    # Ordenar: pendientes, vencidas, realizadas
    orden = {EstadoTarea.PENDIENTE: 0, EstadoTarea.VENCIDA: 1, EstadoTarea.REALIZADA: 2}
    tareas_ordenadas = sorted(tareas, key=lambda t: orden.get(t.estado, 3))
    
    return [tarea_to_response(t) for t in tareas_ordenadas]

@router.put("/{tarea_id}/marcar-realizada", response_model=TareaResponse)
async def marcar_realizada(
    tarea_id: int,
    observaciones: Optional[str] = Form(None),
    evidencia: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Marca una tarea como realizada con evidencia opcional."""
    # Buscar tarea
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).options(
        joinedload(Tarea.terapeuta),
        joinedload(Tarea.recursos),
        joinedload(Tarea.evidencia)
    ).first()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
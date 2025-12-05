from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.core.deps import get_current_active_user
from app.services.actividades_padre_service import ActividadesPadreService
from app.models.recursos import RecursoTarea, ValoracionActividad

router = APIRouter(prefix="/padre/actividades")


class CompletarActividadPadreDto(BaseModel):
    completado: bool
    comentariosPadres: str | None = None


class CrearValoracionPadreDto(BaseModel):
    puntuacion: int
    comentario: str | None = None


class ResumenActividadesPadre(BaseModel):
    totalPendientes: int
    totalCompletadas: int
    pendientesHoy: int


@router.get("")
def get_mis_actividades(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    # Buscar ninos del tutor actual, luego sus tareas (RecursoTarea)
    return ActividadesPadreService.mis_actividades(current_user, db)


@router.get("/{asignacion_id}")
def get_actividad_asignada(
    asignacion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    t = db.query(RecursoTarea).filter(RecursoTarea.id == asignacion_id).first()
    if not t:
        raise HTTPException(404, "Asignación no encontrada")
    return t


@router.post("/{asignacion_id}/completar")
def completar_actividad(
    asignacion_id: int,
    dto: CompletarActividadPadreDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return ActividadesPadreService.completar(asignacion_id, dto, db)


@router.post("/{asignacion_id}/valorar")
def valorar_actividad(
    asignacion_id: int,
    dto: CrearValoracionPadreDto,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    val = ValoracionActividad(
        asignacion_id=asignacion_id,
        puntuacion=dto.puntuacion,
        comentario=dto.comentario,
        fecha=datetime.now(),
    )
    db.add(val)
    db.commit()
    db.refresh(val)
    return val


@router.get("/resumen")
def resumen_actividades(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
) -> ResumenActividadesPadre:
    # Calcula contadores simples sobre RecursoTarea
    q = db.query(RecursoTarea)
    total = q.count()
    completadas = q.filter(RecursoTarea.completado == True).count()
    # pendientes hoy: ejemplo rápido
    pendientes_hoy = q.filter(
        RecursoTarea.completado == False
    ).count()
    return ResumenActividadesPadre(
        totalPendientes=total - completadas,
        totalCompletadas=completadas,
        pendientesHoy=pendientes_hoy,
    )

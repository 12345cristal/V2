from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.deps import get_current_active_user
from app.services.terapeuta_agenda_service import TerapeutaAgendaService
from app.services.terapeuta_pacientes_service import TerapeutaPacientesService

router = APIRouter(prefix="/terapeutas")


@router.get("/horarios/semana")
def get_sesiones_semana(db: Session = Depends(get_db),
                        current=Depends(get_current_active_user)):
    return TerapeutaAgendaService.get_sesiones_semana(current, db)


@router.get("/reposiciones")
def get_reposiciones(db: Session = Depends(get_db),
                     current=Depends(get_current_active_user)):
    return TerapeutaAgendaService.get_reposiciones(current, db)


@router.post("/sesiones/{sesion_id}/completar")
def marcar_sesion_completada(sesion_id: int, db: Session = Depends(get_db),
                             current=Depends(get_current_active_user)):
    return TerapeutaAgendaService.marcar_sesion_completada(sesion_id, current, db)


@router.post("/reposiciones/{repo_id}/aprobar")
def aprobar_reposicion(repo_id: int, db: Session = Depends(get_db),
                       current=Depends(get_current_active_user)):
    return TerapeutaAgendaService.aprobar_reposicion(repo_id, current, db)


@router.post("/reposiciones/{repo_id}/rechazar")
def rechazar_reposicion(repo_id: int, db: Session = Depends(get_db),
                        current=Depends(get_current_active_user)):
    return TerapeutaAgendaService.rechazar_reposicion(repo_id, current, db)


@router.get("/mis-pacientes")
def get_pacientes_asignados(db: Session = Depends(get_db),
                            current=Depends(get_current_active_user)):
    return TerapeutaPacientesService.get_pacientes_asignados(current, db)


@router.get("/pacientes/{nino_id}")
def get_detalle_paciente(nino_id: int, db: Session = Depends(get_db),
                         current=Depends(get_current_active_user)):
    return TerapeutaPacientesService.get_detalle_paciente(nino_id, current, db)


@router.get("/pacientes/{nino_id}/bitacora")
def get_historial_bitacora(nino_id: int, db: Session = Depends(get_db),
                           current=Depends(get_current_active_user)):
    return TerapeutaPacientesService.get_historial_bitacora(nino_id, current, db)

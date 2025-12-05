from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services.terapias_service import TerapiasService
from app.core.deps import require_permissions, get_current_active_user
from app.models.terapias import TerapiaNino, Terapia

router = APIRouter()


class TerapiaDto(BaseModel):
    nombre: str
    descripcion: str
    tipo_terapia_id: int
    duracion_minutos: int
    objetivo_general: str
    activo: bool = True


class AsignacionTerapiaDto(BaseModel):
    nino_id: int
    terapia_id: int
    terapeuta_id: int | None = None
    frecuencia_semana: int
    prioridad_id: int


@router.get("/terapias", dependencies=[Depends(get_current_active_user)])
def listar_terapias(db: Session = Depends(get_db)):
    return TerapiasService.catalogo(db)


@router.post("/terapias", dependencies=[Depends(require_permissions("terapias.crear"))])
def crear_terapia(dto: TerapiaDto, db: Session = Depends(get_db)):
    t = Terapia(**dto.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.put("/terapias/{terapia_id}", dependencies=[Depends(require_permissions("terapias.editar"))])
def actualizar_terapia(terapia_id: int, dto: TerapiaDto, db: Session = Depends(get_db)):
    t = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not t:
        raise HTTPException(404, "Terapia no encontrada")
    for k, v in dto.dict().items():
        setattr(t, k, v)
    db.commit()
    return t


@router.patch("/terapias/{terapia_id}/estado", dependencies=[Depends(require_permissions("terapias.editar"))])
def cambiar_estado_terapia(terapia_id: int, db: Session = Depends(get_db)):
    t = db.query(Terapia).filter(Terapia.id == terapia_id).first()
    if not t:
        raise HTTPException(404, "Terapia no encontrada")
    t.activo = not t.activo
    db.commit()
    return t


@router.post("/terapias/asignar", dependencies=[Depends(require_permissions("terapias.asignar"))])
def asignar_terapia(dto: AsignacionTerapiaDto, db: Session = Depends(get_db)):
    return TerapiasService.asignar(dto.dict(), db)


# ========= TERAPIAS DE UN NIÑO (padres) =========

@router.get("/ninos/{nino_id}/terapias", dependencies=[Depends(get_current_active_user)])
def obtener_terapias_nino_detalle(nino_id: int, db: Session = Depends(get_db)):
    # Puedes mapear al NinoTerapiasDetalle de tu TS
    asignaciones = (
        db.query(TerapiaNino)
        .filter(TerapiaNino.nino_id == nino_id, TerapiaNino.activo == True)
        .all()
    )
    return asignaciones  # luego lo transformas al DTO que necesitas


@router.get("/ninos/{nino_id}/terapias/listado", dependencies=[Depends(get_current_active_user)])
def obtener_terapias_nino_listado(nino_id: int, db: Session = Depends(get_db)):
    asignaciones = (
        db.query(TerapiaNino)
        .filter(TerapiaNino.nino_id == nino_id, TerapiaNino.activo == True)
        .all()
    )
    return asignaciones

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.services.citas_service import CitasService
from app.schemas.cita import (
    CitaListadoResponse,
    CitaCrearRequest,
    CitaActualizarRequest,
    CatalogosCitaResponse
)

router = APIRouter(
    prefix="/citas",
    tags=["citas"],
    dependencies=[Depends(get_current_active_user)]
)

# ============================================================
# GET — CATÁLOGOS (solo estados)
# ============================================================
@router.get("/catalogos", response_model=CatalogosCitaResponse)
def obtener_catalogos(db: Session = Depends(get_db)):
    """
    Carga estados de cita EXACTAMENTE como los usa Angular:
    { id, codigo, nombre }
    """

    estados = CitasService.obtener_catalogo_estados(db)
    return CatalogosCitaResponse(estadosCita=estados)


# ============================================================
# GET — LISTADO DE CITAS CON FILTROS
# ============================================================
@router.get("/", response_model=list[CitaListadoResponse])
def listar_citas(
    fecha: str | None = Query(None),
    estado: str | None = Query(None),
    nino: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """
    Angular manda:
    filtroFecha
    filtroEstado
    filtroNino

    Regresamos EXACTAMENTE CitaListado[]
    """
    citas = CitasService.listar(
        fecha=fecha,
        estado=estado,
        nino=nino,
        db=db
    )

    return citas


# ============================================================
# POST — CREAR CITA
# ============================================================
@router.post("/", response_model=CitaListadoResponse)
def crear_cita(
    payload: CitaCrearRequest,
    db: Session = Depends(get_db)
):
    """
    Angular envía CrearCitaDto desde el modal.
    """
    nueva = CitasService.crear(dto=payload.dict(), db=db)
    return nueva


# ============================================================
# PUT — ACTUALIZAR CITA
# ============================================================
@router.put("/{id}", response_model=CitaListadoResponse)
def actualizar_cita(
    id: int,
    payload: CitaActualizarRequest,
    db: Session = Depends(get_db)
):
    """
    Modo edición del modal.
    """
    actualizada = CitasService.actualizar(id=id, dto=payload.dict(), db=db)
    return actualizada


# ============================================================
# DELETE — CANCELAR CITA
# ============================================================
@router.delete("/{id}/cancelar")
def cancelar_cita(
    id: int,
    motivo: str,
    db: Session = Depends(get_db)
):
    """
    Angular llama:
    cancelarCita(id, motivo)
    """
    cancelada = CitasService.cancelar(id=id, motivo=motivo, db=db)
    return {"mensaje": "Cita cancelada", "id": id}

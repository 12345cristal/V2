from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import json

from app.api.deps import get_db, get_current_active_user
from app.schemas.nino import NinoListado, NinoDetalle
from app.services.ninos_service import NinosService

router = APIRouter(
    prefix="/ninos",
    tags=["ninos"],
    dependencies=[Depends(get_current_active_user)]
)

# ============================================================
# LISTAR NIÑOS (para ninos.ts)
# ============================================================
@router.get("/", response_model=list[NinoListado])
def listar_ninos(db: Session = Depends(get_db)):
    return NinosService.listar_todos(db)


# ============================================================
# OBTENER DETALLE (para nino-form.ts)
# ============================================================
@router.get("/{id}", response_model=NinoDetalle)
def obtener_nino(id: int, db: Session = Depends(get_db)):
    n = NinosService.obtener_detalle(id, db)
    if not n:
        raise HTTPException(404, "Niño no encontrado")
    return n


# ============================================================
# CREAR NIÑO (multipart formdata)
# ============================================================
@router.post("/", response_model=NinoDetalle)
async def crear_nino(
    nino: str = Form(...),
    actaNacimiento: UploadFile | None = File(None),
    curp: UploadFile | None = File(None),
    comprobanteDomicilio: UploadFile | None = File(None),
    foto: UploadFile | None = File(None),
    diagnostico: UploadFile | None = File(None),
    consentimiento: UploadFile | None = File(None),
    hojaIngreso: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    data = json.loads(nino)

    archivos = {
        "actaNacimiento": actaNacimiento,
        "curp": curp,
        "comprobanteDomicilio": comprobanteDomicilio,
        "foto": foto,
        "diagnostico": diagnostico,
        "consentimiento": consentimiento,
        "hojaIngreso": hojaIngreso
    }

    nuevo = NinosService.crear(data, archivos, db)
    return nuevo


# ============================================================
# EDITAR NIÑO (multipart formdata)
# ============================================================
@router.put("/{id}", response_model=NinoDetalle)
async def actualizar_nino(
    id: int,
    nino: str = Form(...),
    actaNacimiento: UploadFile | None = File(None),
    curp: UploadFile | None = File(None),
    comprobanteDomicilio: UploadFile | None = File(None),
    foto: UploadFile | None = File(None),
    diagnostico: UploadFile | None = File(None),
    consentimiento: UploadFile | None = File(None),
    hojaIngreso: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    data = json.loads(nino)

    archivos = {
        "actaNacimiento": actaNacimiento,
        "curp": curp,
        "comprobanteDomicilio": comprobanteDomicilio,
        "foto": foto,
        "diagnostico": diagnostico,
        "consentimiento": consentimiento,
        "hojaIngreso": hojaIngreso
    }

    actualizado = NinosService.actualizar(id, data, archivos, db)
    return actualizado


# ============================================================
# RESUMEN PARA TERAPEUTA Y PADRE
# ============================================================
@router.get("/{id}/resumen/terapeuta")
def resumen_terapeuta(id: int, db: Session = Depends(get_db)):
    return NinosService.resumen_terapeuta(id, db)


@router.get("/{id}/resumen/padre")
def resumen_padre(id: int, db: Session = Depends(get_db)):
    return NinosService.resumen_padre(id, db)

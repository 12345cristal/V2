# app/api/v1/endpoints/ninos.py
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    status
)
from sqlalchemy.orm import Session
from typing import Optional, List
import json

from app.api.deps import get_db, get_current_active_user, require_roles
from app.schemas.nino import NinoCreate, NinoUpdate, NinoResumen, NinoDetalle
from app.services.ninos_service import (
    list_ninos,
    get_nino_by_id,
    create_nino,
    update_nino
)
from app.models.usuario import Usuario

router = APIRouter(prefix="/ninos", tags=["Ninos"])


# =============================
# LISTAR
# =============================

@router.get("/", response_model=List[NinoResumen], dependencies=[Depends(require_roles(2))])
def listar_ninos_endpoint(
    search: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return list_ninos(db, search=search, estado=estado)


# =============================
# DETALLE
# =============================

@router.get("/{nino_id}", response_model=NinoDetalle, dependencies=[Depends(require_roles(2))])
def obtener_nino_endpoint(
    nino_id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_nino_by_id(db, nino_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Niño no encontrado")


# =============================
# CREAR
# =============================

@router.post("/", response_model=NinoDetalle, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(require_roles(2))])
async def crear_nino_endpoint(
    nino: str = Form(...),  # JSON del niño
    actaNacimiento: UploadFile | None = File(None),
    curp: UploadFile | None = File(None),
    comprobanteDomicilio: UploadFile | None = File(None),
    foto: UploadFile | None = File(None),
    diagnostico: UploadFile | None = File(None),
    consentimiento: UploadFile | None = File(None),
    hojaIngreso: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_active_user)
):
    data_json = json.loads(nino)
    data_schema = NinoCreate(**data_json)

    archivos = {
        "actaNacimiento": actaNacimiento,
        "curp": curp,
        "comprobanteDomicilio": comprobanteDomicilio,
        "foto": foto,
        "diagnostico": diagnostico,
        "consentimiento": consentimiento,
        "hojaIngreso": hojaIngreso,
    }

    return await create_nino(db, data_schema, archivos, usuario_id=user.id)


# =============================
# ACTUALIZAR
# =============================

@router.put("/{nino_id}", response_model=NinoDetalle, dependencies=[Depends(require_roles(2))])
async def actualizar_nino_endpoint(
    nino_id: int,
    nino: str = Form(...),
    actaNacimiento: UploadFile | None = File(None),
    curp: UploadFile | None = File(None),
    comprobanteDomicilio: UploadFile | None = File(None),
    foto: UploadFile | None = File(None),
    diagnostico: UploadFile | None = File(None),
    consentimiento: UploadFile | None = File(None),
    hojaIngreso: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_active_user)
):
    data_json = json.loads(nino)
    data_schema = NinoUpdate(id=nino_id, **data_json)

    archivos = {
        "actaNacimiento": actaNacimiento,
        "curp": curp,
        "comprobanteDomicilio": comprobanteDomicilio,
        "foto": foto,
        "diagnostico": diagnostico,
        "consentimiento": consentimiento,
        "hojaIngreso": hojaIngreso,
    }

    try:
        return await update_nino(db, nino_id, data_schema, archivos, usuario_id=user.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Niño no encontrado")

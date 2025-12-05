from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import json

from app.api.deps import get_db, get_current_active_user
from app.schemas.personal import PersonalBase, PersonalDetalle, RolSchema
from app.services.personal_service import PersonalService

router = APIRouter(
    prefix="/personal",
    tags=["personal"],
    dependencies=[Depends(get_current_active_user)]
)

# ============================================================
# ROLES PARA SELECTOR (personal-form & usuarios-form)
# ============================================================
@router.get("/roles", response_model=list[RolSchema])
def obtener_roles(db: Session = Depends(get_db)):
    return PersonalService.obtener_roles(db)


# ============================================================
# LISTAR PERSONAL (para personal-list.ts)
# ============================================================
@router.get("/", response_model=list[PersonalBase])
def listar_personal(db: Session = Depends(get_db)):
    return PersonalService.listar(db)


# ============================================================
# DETALLE PERSONAL
# ============================================================
@router.get("/{id}", response_model=PersonalDetalle)
def obtener_personal(id: int, db: Session = Depends(get_db)):
    p = PersonalService.obtener_detalle(id, db)
    if not p:
        raise HTTPException(404, "Personal no encontrado")
    return p


# ============================================================
# CREAR PERSONAL (multipart)
# ============================================================
@router.post("/", response_model=PersonalDetalle)
async def crear_personal(
    data: str = Form(...),
    foto: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    body = json.loads(data)
    nuevo = PersonalService.crear(body, foto, db)
    return nuevo


# ============================================================
# ACTUALIZAR PERSONAL (multipart)
# ============================================================
@router.put("/{id}", response_model=PersonalDetalle)
async def actualizar_personal(
    id: int,
    data: str = Form(...),
    foto: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    body = json.loads(data)
    actualizado = PersonalService.actualizar(id, body, foto, db)
    return actualizado


# ============================================================
# HORARIOS DEL PERSONAL
# ============================================================
@router.get("/{id}/horarios")
def obtener_horarios(id: int, db: Session = Depends(get_db)):
    return PersonalService.horarios(id, db)

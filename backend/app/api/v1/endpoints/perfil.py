from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid, os

from app.db.session import get_db
from app.core.deps import get_current_active_user
from app.models.roles_usuarios import PerfilPersonal

router = APIRouter(prefix="/perfil")


class PerfilUpdateDto(BaseModel):
    telefono_personal: str
    correo_personal: str
    grado_academico: str
    especialidad_principal: str
    especialidades: str
    experiencia: str
    domicilio_calle: str
    domicilio_colonia: str
    domicilio_cp: str
    domicilio_municipio: str
    domicilio_estado: str


@router.get("/me")
def get_mi_perfil(db: Session = Depends(get_db),
                  current=Depends(get_current_active_user)):
    perfil = db.query(PerfilPersonal).filter(
        PerfilPersonal.usuario_id == current.id
    ).first()
    return perfil


@router.put("/me")
async def actualizar_mi_perfil(
    telefono_personal: str = Form(...),
    correo_personal: str = Form(...),
    grado_academico: str = Form(...),
    especialidad_principal: str = Form(...),
    especialidades: str = Form(...),
    experiencia: str = Form(...),
    domicilio_calle: str = Form(...),
    domicilio_colonia: str = Form(...),
    domicilio_cp: str = Form(...),
    domicilio_municipio: str = Form(...),
    domicilio_estado: str = Form(...),
    cv_archivo: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current=Depends(get_current_active_user),
):
    perfil = db.query(PerfilPersonal).filter(
        PerfilPersonal.usuario_id == current.id
    ).first()
    if not perfil:
        perfil = PerfilPersonal(usuario_id=current.id)
        db.add(perfil)

    perfil.telefono_personal = telefono_personal
    perfil.correo_personal = correo_personal
    perfil.experiencia = experiencia
    perfil.domicilio_calle = domicilio_calle
    perfil.domicilio_colonia = domicilio_colonia
    perfil.domicilio_cp = domicilio_cp
    perfil.domicilio_municipio = domicilio_municipio
    perfil.domicilio_estado = domicilio_estado
    # etc.

    if cv_archivo:
        filename = f"{uuid.uuid4()}_{cv_archivo.filename}"
        path = f"uploads/cv/{filename}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(await cv_archivo.read())
        perfil.cv_url = path

    db.commit()
    db.refresh(perfil)
    return perfil

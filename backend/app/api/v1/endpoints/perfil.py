# app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid

from app.api.deps import get_db_session, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil
from app.schemas.perfil import PerfilResponse

router = APIRouter(
    tags=["Perfil"]
)


# ===============================
# CONFIGURACIÓN DE UPLOADS
# ===============================
UPLOADS_BASE = Path("uploads")
FOTOS_DIR = UPLOADS_BASE / "fotos"
CV_DIR = UPLOADS_BASE / "cv"

FOTOS_DIR.mkdir(parents=True, exist_ok=True)
CV_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 3 * 1024 * 1024  # 3MB
MAX_PDF_SIZE = 5 * 1024 * 1024    # 5MB


# ===============================
# GET PERFIL
# ===============================
@router.get("/me", response_model=PerfilResponse)
def get_me(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = (
        db.query(Personal)
        .filter(Personal.id_usuario == current_user.id)
        .first()
    )

    if not personal:
        raise HTTPException(404, "No existe un registro de personal asociado.")

    perfil = (
        db.query(PersonalPerfil)
        .filter(PersonalPerfil.personal_id == personal.id)
        .first()
    )

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)
        db.commit()
        db.refresh(perfil)

    return PerfilResponse.from_db(personal, perfil, current_user)


# ===============================
# UPDATE PERFIL
# ===============================
@router.put("/me", response_model=PerfilResponse)
def update_me(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),

    # -------- FORM DATA --------
    telefono_personal: str | None = Form(None),
    correo_personal: str | None = Form(None),

    grado_academico: str | None = Form(None),
    especialidades: str | None = Form(None),
    experiencia: str | None = Form(None),

    domicilio_calle: str | None = Form(None),
    domicilio_colonia: str | None = Form(None),
    domicilio_cp: str | None = Form(None),
    domicilio_municipio: str | None = Form(None),
    domicilio_estado: str | None = Form(None),

    # -------- FILES --------
    foto_perfil: UploadFile | None = File(None),
    cv_archivo: UploadFile | None = File(None),
):
    personal = (
        db.query(Personal)
        .filter(Personal.id_usuario == current_user.id)
        .first()
    )

    if not personal:
        raise HTTPException(404, "No existe Personal asociado.")

    perfil = (
        db.query(PersonalPerfil)
        .filter(PersonalPerfil.personal_id == personal.id)
        .first()
    )

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)

    # ===============================
    # ACTUALIZAR CAMPOS
    # ===============================
    if telefono_personal is not None:
        perfil.telefono_personal = telefono_personal
    if correo_personal is not None:
        perfil.correo_personal = correo_personal
    if grado_academico is not None:
        personal.grado_academico = grado_academico
    if especialidades is not None:
        perfil.especialidades = especialidades
    if experiencia is not None:
        perfil.experiencia = experiencia

    if domicilio_calle is not None:
        perfil.domicilio_calle = domicilio_calle
    if domicilio_colonia is not None:
        perfil.domicilio_colonia = domicilio_colonia
    if domicilio_cp is not None:
        perfil.domicilio_cp = domicilio_cp
    if domicilio_municipio is not None:
        perfil.domicilio_municipio = domicilio_municipio
    if domicilio_estado is not None:
        perfil.domicilio_estado = domicilio_estado

    # ===============================
    # FOTO DE PERFIL
    # ===============================
    if foto_perfil and foto_perfil.filename:
        if not foto_perfil.content_type.startswith("image/"):
            raise HTTPException(400, "La foto debe ser una imagen")

        contents = foto_perfil.file.read()
        if len(contents) > MAX_IMAGE_SIZE:
            raise HTTPException(400, "La imagen supera el tamaño permitido (3MB)")
        foto_perfil.file.seek(0)

        ext = Path(foto_perfil.filename).suffix.lower()
        filename = f"personal_{personal.id}_foto_{uuid.uuid4().hex}{ext}"
        destino = FOTOS_DIR / filename

        with destino.open("wb") as f:
            shutil.copyfileobj(foto_perfil.file, f)

        # eliminar foto anterior si existía
        if perfil.foto_url:
            anterior = FOTOS_DIR / perfil.foto_url
            if anterior.exists():
                anterior.unlink(missing_ok=True)

        perfil.foto_url = filename

    # ===============================
    # CV (PDF)
    # ===============================
    if cv_archivo and cv_archivo.filename:
        if cv_archivo.content_type != "application/pdf":
            raise HTTPException(400, "El currículum debe ser un PDF")

        contents = cv_archivo.file.read()
        if len(contents) > MAX_PDF_SIZE:
            raise HTTPException(400, "El PDF supera el tamaño permitido (5MB)")
        cv_archivo.file.seek(0)

        ext = Path(cv_archivo.filename).suffix.lower()
        filename = f"personal_{personal.id}_cv_{uuid.uuid4().hex}{ext}"
        destino = CV_DIR / filename

        with destino.open("wb") as f:
            shutil.copyfileobj(cv_archivo.file, f)

        # eliminar CV anterior si existía
        if perfil.cv_url:
            anterior = CV_DIR / perfil.cv_url
            if anterior.exists():
                anterior.unlink(missing_ok=True)

        perfil.cv_url = filename

    db.commit()
    db.refresh(perfil)
    db.refresh(personal)

    return PerfilResponse.from_db(personal, perfil, current_user)

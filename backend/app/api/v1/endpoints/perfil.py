# app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.api.deps import get_db_session, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil
from app.schemas.perfil import PerfilResponse

router = APIRouter(tags=["Perfil"])


@router.get("/me", response_model=PerfilResponse)
def get_me(db: Session = Depends(get_db_session), current_user: Usuario = Depends(get_current_user)):
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(404, "No existe un registro de personal asociado.")

    perfil = db.query(PersonalPerfil).filter(
        PersonalPerfil.personal_id == personal.id
    ).first()

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)
        db.commit()
        db.refresh(perfil)

    return PerfilResponse.from_db(personal, perfil, current_user)


@router.put("/me", response_model=PerfilResponse)
def update_me(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),

    telefono_personal: str = Form(None),
    correo_personal: str = Form(None),

    grado_academico: str = Form(None),
    especialidades: str = Form(None),
    experiencia: str = Form(None),

    domicilio_calle: str = Form(None),
    domicilio_colonia: str = Form(None),
    domicilio_cp: str = Form(None),
    domicilio_municipio: str = Form(None),
    domicilio_estado: str = Form(None),

    foto_perfil: UploadFile = File(None),
    cv_archivo: UploadFile = File(None)
):
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(404, "No existe Personal asociado.")

    perfil = db.query(PersonalPerfil).filter(
        PersonalPerfil.personal_id == personal.id
    ).first()

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)

    # Crear directorio si no existe
    os.makedirs("static/fotos", exist_ok=True)
    os.makedirs("static/cv", exist_ok=True)

    # FOTO (solo si se sube)
    if foto_perfil and foto_perfil.filename:
        ruta = f"static/fotos/personal_{personal.id}_{foto_perfil.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(foto_perfil.file, f)
        perfil.foto_url = ruta

    # CV (solo si se sube)
    if cv_archivo and cv_archivo.filename:
        ruta = f"static/cv/personal_{personal.id}_{cv_archivo.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(cv_archivo.file, f)
        perfil.cv_url = ruta

    # CAMPOS (solo actualizar si se envían)
    if telefono_personal is not None:
        perfil.telefono_personal = telefono_personal
    if correo_personal is not None:
        perfil.correo_personal = correo_personal
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

    db.commit()
    db.refresh(perfil)
    db.refresh(personal)

    return PerfilResponse.from_db(personal, perfil, current_user)

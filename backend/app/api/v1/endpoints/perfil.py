# app/api/v1/endpoints/perfil.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.personal_perfil import PersonalPerfil
from app.schemas.perfil import PerfilResponse

router = APIRouter(prefix="/perfil", tags=["Perfil"])


@router.get("/me", response_model=PerfilResponse)
def get_me(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    personal = db.query(Personal).filter(Personal.usuario_id == current_user.id).first()
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
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),

    telefono_personal: str = Form(...),
    correo_personal: str = Form(...),

    grado_academico: str = Form(...),
    especialidades: str = Form(...),
    experiencia: str = Form(...),

    domicilio_calle: str = Form(...),
    domicilio_colonia: str = Form(...),
    domicilio_cp: str = Form(...),
    domicilio_municipio: str = Form(...),
    domicilio_estado: str = Form(...),

    foto_perfil: UploadFile = File(None),
    cv_archivo: UploadFile = File(None)
):
    personal = db.query(Personal).filter(Personal.usuario_id == current_user.id).first()
    if not personal:
        raise HTTPException(404, "No existe Personal asociado.")

    perfil = db.query(PersonalPerfil).filter(
        PersonalPerfil.personal_id == personal.id
    ).first()

    if not perfil:
        perfil = PersonalPerfil(personal_id=personal.id)
        db.add(perfil)

    # FOTO
    if foto_perfil:
        ruta = f"static/fotos/personal_{personal.id}_{foto_perfil.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(foto_perfil.file, f)
        perfil.foto_url = ruta

    # CV
    if cv_archivo:
        ruta = f"static/cv/personal_{personal.id}_{cv_archivo.filename}"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(cv_archivo.file, f)
        perfil.cv_url = ruta

    # CAMPOS
    perfil.telefono_personal = telefono_personal
    perfil.correo_personal = correo_personal
    perfil.especialidades = especialidades
    perfil.experiencia = experiencia

    perfil.domicilio_calle = domicilio_calle
    perfil.domicilio_colonia = domicilio_colonia
    perfil.domicilio_cp = domicilio_cp
    perfil.domicilio_municipio = domicilio_municipio
    perfil.domicilio_estado = domicilio_estado

    db.commit()
    db.refresh(perfil)
    db.refresh(personal)

    return PerfilResponse.from_db(personal, perfil, current_user)

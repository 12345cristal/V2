# app/api/v1/endpoints/personal.py
import shutil
from fastapi import (
    APIRouter, Depends, UploadFile, HTTPException, Form
)
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, require_permissions
from app.models.personal import Personal
from app.models.perfil_personal import PerfilPersonal
from app.models.usuario import Usuario
from app.schemas.personal import PersonalCreate, PersonalRead, PersonalUpdate


router = APIRouter(
    prefix="/personal",
    tags=["personal"]
)


# ===============================
# LISTAR PERSONAL
# ===============================
@router.get("/", response_model=List[PersonalRead])
def listar_personal(
    db: Session = Depends(get_db),
    _: bool = Depends(require_permissions(["personal:ver"]))
):
    personas = db.query(Personal).all()
    resultado = []

    for p in personas:
        resultado.append(
            PersonalRead(
                id_personal=p.id,
                nombres=p.usuario.nombres,
                apellido_paterno=p.usuario.apellido_paterno,
                apellido_materno=p.usuario.apellido_materno,
                id_rol=p.rol_id,
                nombre_rol=p.rol.nombre,
                correo_personal=p.perfil.correo_personal if p.perfil else None,
                telefono_personal=p.perfil.telefono_personal if p.perfil else None,
                especialidad_principal=p.perfil.especialidad_principal if p.perfil else None,
                estado_laboral="ACTIVO",
                rating=p.perfil.rating if p.perfil else 0,
            )
        )

    return resultado


# ===============================
# OBTENER POR ID
# ===============================
@router.get("/{personal_id}", response_model=PersonalRead)
def obtener_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permissions(["personal:ver"]))
):
    p = db.query(Personal).filter(Personal.id == personal_id).first()
    if not p:
        raise HTTPException(404, "Personal no encontrado")

    return PersonalRead(
        id_personal=p.id,
        nombres=p.usuario.nombres,
        apellido_paterno=p.usuario.apellido_paterno,
        apellido_materno=p.usuario.apellido_materno,
        id_rol=p.rol_id,
        nombre_rol=p.rol.nombre,
        correo_personal=p.perfil.correo_personal,
        telefono_personal=p.perfil.telefono_personal,
        especialidad_principal=p.perfil.especialidad_principal,
        estado_laboral="ACTIVO",
        rating=p.perfil.rating,
        foto_url=p.usuario.foto_url if hasattr(p.usuario, "foto_url") else None
    )


# ===============================
# CREAR PERSONAL (CON FOTO)
# ===============================
@router.post("/", response_model=PersonalRead)
def crear_personal(
    nombres: str = Form(...),
    apellido_paterno: str = Form(...),
    apellido_materno: str = Form(None),
    correo_personal: str = Form(...),
    telefono_personal: str = Form(...),
    id_rol: int = Form(...),
    especialidad_principal: str = Form(...),
    fecha_ingreso: str = Form(...),
    fecha_nacimiento: str = Form(...),
    rfc: str = Form(...),
    curp: str = Form(...),
    experiencia: str = Form(...),
    domicilio_calle: str = Form(...),
    domicilio_colonia: str = Form(...),
    domicilio_cp: str = Form(...),
    domicilio_municipio: str = Form(...),
    domicilio_estado: str = Form(...),
    foto: UploadFile | None = None,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permissions(["personal:crear"]))
):
    # Crear usuario
    user = Usuario(
        nombres=nombres,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        email=correo_personal,
        hashed_password="TEMP",  # luego cambias esto
        rol_id=id_rol,
        activo=1
    )
    db.add(user)
    db.flush()

    # Crear personal
    persona = Personal(
        usuario_id=user.id,
        rol_id=id_rol
    )
    db.add(persona)
    db.flush()

    # Crear perfil
    perfil = PerfilPersonal(
        usuario_id=user.id,
        fecha_ingreso=fecha_ingreso,
        fecha_nacimiento=fecha_nacimiento,
        curp=curp,
        rfc=rfc,
        correo_personal=correo_personal,
        telefono_personal=telefono_personal,
        experiencia=experiencia,
        domicilio_calle=domicilio_calle,
        domicilio_colonia=domicilio_colonia,
        domicilio_cp=domicilio_cp,
        domicilio_municipio=domicilio_municipio,
        domicilio_estado=domicilio_estado,
        especialidad_principal=especialidad_principal
    )
    db.add(perfil)
    db.flush()

    # Guardar FOTO
    if foto:
        ruta = f"uploads/personal/{user.id}.jpg"
        with open(ruta, "wb") as f:
            shutil.copyfileobj(foto.file, f)
        user.foto_url = ruta

    db.commit()
    db.refresh(persona)

    return obtener_personal(persona.id, db)


# ===============================
# ACTUALIZAR PERSONAL
# ===============================
@router.put("/{personal_id}", response_model=PersonalRead)
def actualizar_personal(
    personal_id: int,
    data: PersonalUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permissions(["personal:editar"]))
):
    persona = db.query(Personal).filter_by(id=personal_id).first()
    if not persona:
        raise HTTPException(404, "Personal no encontrado")

    user = persona.usuario
    perfil = persona.perfil

    payload = data.model_dump(exclude_unset=True)

    for campo, valor in payload.items():
        # Usuario
        if hasattr(user, campo):
            setattr(user, campo, valor)

        # Perfil
        elif hasattr(perfil, campo):
            setattr(perfil, campo, valor)

    db.commit()
    return obtener_personal(persona.id, db)


# ===============================
# ELIMINAR PERSONAL
# ===============================
@router.delete("/{personal_id}", status_code=204)
def eliminar_personal(
    personal_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permissions(["personal:eliminar"]))
):
    persona = db.query(Personal).filter_by(id=personal_id).first()
    if not persona:
        raise HTTPException(404, "Personal no encontrado")

    db.delete(persona)
    db.commit()
    return

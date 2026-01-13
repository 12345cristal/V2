# app/api/v1/endpoints/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.personal import Personal
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioListado,
    UsuarioDetalle,
)
from app.core.security import get_password_hash

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# =====================================================
# LISTAR USUARIOS
# =====================================================
@router.get("", response_model=List[UsuarioListado])
def listar_usuarios(
    db: Session = Depends(get_db),
    buscar: Optional[str] = None,
    id_rol: Optional[int] = None,
):
    query = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol), joinedload(Usuario.personal))
    )

    if buscar:
        filtro = f"%{buscar}%"
        query = query.filter(
            (Usuario.nombres.ilike(filtro))
            | (Usuario.apellido_paterno.ilike(filtro))
            | (Usuario.email.ilike(filtro))
        )

    if id_rol:
        query = query.filter(Usuario.rol_id == id_rol)

    usuarios = query.all()
    resultado = []

    for u in usuarios:
        resultado.append({
            "id_usuario": u.id,
            "id_personal": u.personal.id if u.personal else None,
            "email": u.email,
            "nombre_completo": f"{u.nombres} {u.apellido_paterno} {u.apellido_materno or ''}".strip(),
            "rol_id": u.rol_id,
            "nombre_rol": u.rol.nombre if u.rol else "Sin rol",
            "estado": "ACTIVO" if u.activo else "INACTIVO",
            "estado_laboral": u.personal.estado_laboral if u.personal else None,
            "ultima_sesion": u.ultimo_login,
            "fecha_creacion": u.fecha_creacion,
        })

    return resultado


# =====================================================
# OBTENER USUARIO
# =====================================================
@router.get("/{id_usuario}", response_model=UsuarioDetalle)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
):
    usuario = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol))
        .filter(Usuario.id == id_usuario)
        .first()
    )

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "rol_id": usuario.rol_id,
        "nombre_rol": usuario.rol.nombre if usuario.rol else "Sin rol",
        "telefono": usuario.telefono,
        "activo": usuario.activo,
        "fecha_creacion": usuario.fecha_creacion,
        "ultimo_login": usuario.ultimo_login,
    }


# =====================================================
# CREAR USUARIO
# =====================================================
@router.post("", response_model=UsuarioDetalle)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    if db.query(Usuario).filter(Usuario.email == data.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    personal = None
    if data.id_personal:
        personal = db.query(Personal).filter(Personal.id == data.id_personal).first()
        if not personal:
            raise HTTPException(status_code=404, detail="Personal no encontrado")

    usuario = Usuario(
        nombres=data.nombres,
        apellido_paterno=data.apellido_paterno,
        apellido_materno=data.apellido_materno,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        rol_id=data.rol_id,
        telefono=data.telefono,
        activo=True,
    )

    db.add(usuario)
    db.flush()

    if personal:
        personal.id_usuario = usuario.id

    db.commit()
    db.refresh(usuario)

    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "rol_id": usuario.rol_id,
        "nombre_rol": usuario.rol.nombre if usuario.rol else "Sin rol",
        "telefono": usuario.telefono,
        "activo": usuario.activo,
        "fecha_creacion": usuario.fecha_creacion,
        "ultimo_login": usuario.ultimo_login,
    }


# =====================================================
# ACTUALIZAR USUARIO
# =====================================================
@router.put("/{id_usuario}", response_model=UsuarioDetalle)
def actualizar_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "rol_id": usuario.rol_id,
        "nombre_rol": usuario.rol.nombre if usuario.rol else "Sin rol",
        "telefono": usuario.telefono,
        "activo": usuario.activo,
        "fecha_creacion": usuario.fecha_creacion,
        "ultimo_login": usuario.ultimo_login,
    }


# =====================================================
# CAMBIAR ESTADO
# =====================================================
@router.patch("/{id_usuario}/estado")
def cambiar_estado_usuario(
    id_usuario: int,
    data: dict,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    estado = data.get("estado")
    usuario.activo = estado == "ACTIVO"

    db.commit()
    db.refresh(usuario)

    return {
        "id_usuario": usuario.id,
        "estado": "ACTIVO" if usuario.activo else "INACTIVO",
    }


# =====================================================
# ELIMINAR USUARIO
# =====================================================
@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
):
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado correctamente"}

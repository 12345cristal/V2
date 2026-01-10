# backend/app/api/v1/endpoints/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.personal import Personal
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash

router = APIRouter()


@router.get("/")
def listar_usuarios(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    buscar: Optional[str] = None,
    id_rol: Optional[int] = None
):
    """Lista todos los usuarios del sistema con su rol y personal vinculado"""

    query = (
        db.query(Usuario)
        .options(joinedload(Usuario.rol), joinedload(Usuario.personal))
    )

    if buscar:
        buscar_lower = f"%{buscar.lower()}%"
        query = query.filter(
            (Usuario.nombres.ilike(buscar_lower))
            | (Usuario.apellido_paterno.ilike(buscar_lower))
            | (Usuario.email.ilike(buscar_lower))
        )

    if id_rol:
        query = query.filter(Usuario.rol_id == id_rol)

    usuarios = query.all()

    resultado = []
    for usuario in usuarios:
        nombre_completo = f"{usuario.nombres} {usuario.apellido_paterno}"
        if usuario.apellido_materno:
            nombre_completo += f" {usuario.apellido_materno}"

        resultado.append({
            "id_usuario": usuario.id,
            "id_personal": usuario.personal.id if usuario.personal else None,
            "username": usuario.email.split("@")[0] if usuario.email else "sin_nombre",
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "nombre_rol": usuario.rol.nombre if usuario.rol else "Sin rol",
            "nombre_completo": nombre_completo,
            "estado": "ACTIVO" if usuario.activo else "INACTIVO",
            "estado_laboral": usuario.personal.estado_laboral if usuario.personal else None,
            "ultima_sesion": usuario.ultimo_login.isoformat() if usuario.ultimo_login else None,
            "fecha_creacion": usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None,
        })

    return resultado


@router.get("/{id_usuario}")
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtiene un usuario específico"""
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    
    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "rol_id": usuario.rol_id,
        "nombre_rol": rol.nombre if rol else "Sin rol",
        "telefono": usuario.telefono,
        "activo": usuario.activo,
        "fecha_creacion": usuario.fecha_creacion.isoformat() if usuario.fecha_creacion else None
    }


@router.post("/")
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Crea un nuevo usuario y vincula un personal si se envía id_personal"""

    usuario_existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    personal_obj = None
    if data.id_personal:
        personal_obj = db.query(Personal).filter(Personal.id == data.id_personal).first()
        if not personal_obj:
            raise HTTPException(status_code=404, detail="Personal no encontrado")

    nuevo_usuario = Usuario(
        nombres=data.nombres,
        apellido_paterno=data.apellido_paterno,
        apellido_materno=data.apellido_materno,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        rol_id=data.rol_id,
        telefono=data.telefono,
        activo=True,
    )

    db.add(nuevo_usuario)
    db.flush()

    if personal_obj:
        personal_obj.id_usuario = nuevo_usuario.id

    db.commit()
    db.refresh(nuevo_usuario)

    return {
        "id_usuario": nuevo_usuario.id,
        "id_personal": personal_obj.id if personal_obj else None,
        "email": nuevo_usuario.email,
        "nombres": nuevo_usuario.nombres,
        "apellido_paterno": nuevo_usuario.apellido_paterno,
        "apellido_materno": nuevo_usuario.apellido_materno,
        "rol_id": nuevo_usuario.rol_id,
        "nombre_rol": personal_obj.rol.nombre if personal_obj and personal_obj.rol else None,
        "activo": nuevo_usuario.activo,
    }


@router.put("/{id_usuario}")
def actualizar_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Actualiza un usuario existente"""
    
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos solo si se proporcionan
    if data.nombres is not None:
        usuario.nombres = data.nombres
    if data.apellido_paterno is not None:
        usuario.apellido_paterno = data.apellido_paterno
    if data.apellido_materno is not None:
        usuario.apellido_materno = data.apellido_materno
    if data.rol_id is not None:
        usuario.rol_id = data.rol_id
    if data.telefono is not None:
        usuario.telefono = data.telefono
    if data.activo is not None:
        usuario.activo = data.activo
    
    db.commit()
    db.refresh(usuario)
    
    rol = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    
    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "nombres": usuario.nombres,
        "apellido_paterno": usuario.apellido_paterno,
        "apellido_materno": usuario.apellido_materno,
        "rol_id": usuario.rol_id,
        "nombre_rol": rol.nombre if rol else "Sin rol",
        "activo": usuario.activo
    }


@router.patch("/{id_usuario}/estado")
def cambiar_estado_usuario(
    id_usuario: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Activa o desactiva un usuario"""

    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    nuevo_estado = data.get("estado")
    if isinstance(nuevo_estado, str):
        usuario.activo = nuevo_estado.upper() == "ACTIVO"
    elif isinstance(nuevo_estado, bool):
        usuario.activo = nuevo_estado
    else:
        usuario.activo = data.get("activo", True)

    db.commit()
    db.refresh(usuario)

    return {
        "id_usuario": usuario.id,
        "email": usuario.email,
        "estado": "ACTIVO" if usuario.activo else "INACTIVO",
    }


@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Elimina un usuario"""
    
    usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    
    return {"mensaje": "Usuario eliminado correctamente"}

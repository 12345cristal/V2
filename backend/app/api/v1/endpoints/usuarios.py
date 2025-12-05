from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.schemas.usuario import (
    UsuarioListado,
    UsuarioDetalle,
    UsuarioCreateRequest,
    UsuarioUpdateRequest,
    PersonalSimple,
    RolSchema
)
from app.services.usuarios_service import UsuariosService

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(get_current_active_user)]
)

# ============================================================
# ROLES DEL SISTEMA
# ============================================================
@router.get("/roles", response_model=list[RolSchema])
def obtener_roles(db: Session = Depends(get_db)):
    return UsuariosService.obtener_roles(db)


# ============================================================
# PERSONAL SIN USUARIO (selector del formulario)
# ============================================================
@router.get("/personal-disponible", response_model=list[PersonalSimple])
def personal_disponible(db: Session = Depends(get_db)):
    return UsuariosService.personal_sin_usuario(db)


# ============================================================
# LISTAR USUARIOS
# ============================================================
@router.get("/", response_model=list[UsuarioListado])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuariosService.listar(db)


# ============================================================
# OBTENER DETALLE
# ============================================================
@router.get("/{id}", response_model=UsuarioDetalle)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    u = UsuariosService.obtener(id, db)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u


# ============================================================
# CREAR USUARIO
# ============================================================
@router.post("/", response_model=UsuarioDetalle)
def crear_usuario(dto: UsuarioCreateRequest, db: Session = Depends(get_db)):
    return UsuariosService.crear(dto, db)


# ============================================================
# EDITAR USUARIO
# ============================================================
@router.put("/{id}", response_model=UsuarioDetalle)
def actualizar_usuario(id: int, dto: UsuarioUpdateRequest, db: Session = Depends(get_db)):
    return UsuariosService.actualizar(id, dto, db)


# ============================================================
# CAMBIAR ESTADO (ACTIVO / INACTIVO)
# ============================================================
@router.put("/{id}/estado")
def cambiar_estado(id: int, db: Session = Depends(get_db)):
    UsuariosService.cambiar_estado(id, db)
    return {"mensaje": "Estado actualizado"}

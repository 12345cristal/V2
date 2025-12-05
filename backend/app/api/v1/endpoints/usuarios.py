from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services.usuarios_service import UsuariosService
from app.core.deps import get_current_active_user, require_permissions

router = APIRouter(prefix="/usuarios")


class UsuarioCreateDto(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: str
    password: str
    rol_id: int


class UsuarioUpdateDto(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: str
    rol_id: int


class CambiarEstadoDto(BaseModel):
    estado: bool


class CambiarPasswordDto(BaseModel):
    password: str


@router.get("", dependencies=[Depends(require_permissions("usuarios.ver"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuariosService.listar(db)


@router.post("", dependencies=[Depends(require_permissions("usuarios.crear"))])
def crear_usuario(dto: UsuarioCreateDto, db: Session = Depends(get_db)):
    return UsuariosService.crear(dto, db)


@router.put("/{usuario_id}", dependencies=[Depends(require_permissions("usuarios.editar"))])
def actualizar_usuario(usuario_id: int, dto: UsuarioUpdateDto, db: Session = Depends(get_db)):
    return UsuariosService.actualizar(usuario_id, dto, db)


@router.patch("/{usuario_id}/estado", dependencies=[Depends(require_permissions("usuarios.editar"))])
def cambiar_estado(usuario_id: int, dto: CambiarEstadoDto, db: Session = Depends(get_db)):
    return UsuariosService.cambiar_estado(usuario_id, dto.estado, db)


@router.patch("/{usuario_id}/password")
def cambiar_password(usuario_id: int, dto: CambiarPasswordDto, db: Session = Depends(get_db),
                     current=Depends(get_current_active_user)):
    # puedes validar que current.id == usuario_id o que tenga permiso global
    return UsuariosService.cambiar_password(usuario_id, dto.password, db)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.roles_service import RolesService
from app.core.deps import get_current_active_user, require_permissions

router = APIRouter(prefix="/roles")


@router.get("", dependencies=[Depends(require_permissions("roles.ver"))])
def listar_roles(db: Session = Depends(get_db)):
    return RolesService.listar(db)


@router.get("/{rol_id}/permisos", dependencies=[Depends(require_permissions("roles.ver"))])
def permisos_de_rol(rol_id: int, db: Session = Depends(get_db)):
    return RolesService.permisos_de_rol(rol_id, db)

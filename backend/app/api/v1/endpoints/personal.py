from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services.personal_service import PersonalService
from app.core.deps import require_permissions

router = APIRouter(prefix="/personal")


class PersonalDto(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str | None = None
    id_rol: int
    especialidad_principal: str
    telefono_personal: str
    correo_personal: str
    fecha_ingreso: str
    estado_laboral: str
    fecha_nacimiento: str
    grado_academico: str
    especialidades: str
    rfc: str
    ine: str
    curp: str
    domicilio_calle: str
    domicilio_colonia: str
    domicilio_cp: str
    domicilio_municipio: str
    domicilio_estado: str
    experiencia: str


@router.get("/roles", dependencies=[Depends(require_permissions("roles.ver"))])
def listar_roles_personal(db: Session = Depends(get_db)):
    # puedes mapear desde tabla roles
    from app.models.roles_usuarios import Rol
    return db.query(Rol).all()


@router.get("/personal", dependencies=[Depends(require_permissions("personal.ver"))])
def listar_personal(db: Session = Depends(get_db)):
    return PersonalService.listar(db)


@router.get("/personal/{personal_id}", dependencies=[Depends(require_permissions("personal.ver"))])
def obtener_personal(personal_id: int, db: Session = Depends(get_db)):
    return PersonalService.obtener(personal_id, db)


@router.post("/personal", dependencies=[Depends(require_permissions("personal.crear"))])
def crear_personal(dto: PersonalDto, db: Session = Depends(get_db)):
    # Aquí normalmente crearías usuario + perfil + registro en personal
    # por simplicidad delega a PersonalService.actualizar/crear según tu FASE 4.
    return PersonalService.crear(dto, db)  # si lo implementas así


@router.put("/personal/{personal_id}", dependencies=[Depends(require_permissions("personal.editar"))])
def actualizar_personal(personal_id: int, dto: PersonalDto, db: Session = Depends(get_db)):
    return PersonalService.actualizar(personal_id, dto, db)


@router.delete("/personal/{personal_id}", dependencies=[Depends(require_permissions("personal.eliminar"))])
def eliminar_personal(personal_id: int, db: Session = Depends(get_db)):
    p = PersonalService.obtener(personal_id, db)
    db.delete(p)
    db.commit()
    return {"ok": True}

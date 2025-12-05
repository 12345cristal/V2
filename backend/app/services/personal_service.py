import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.models.personal import Personal
from app.models.perfiles_personal import PerfilPersonal
from app.models.roles import Rol


def guardar_foto(file: UploadFile):
    if not file:
        return None
    ext = file.filename.split(".")[-1]
    fname = f"{uuid.uuid4()}.{ext}"
    path = f"uploads/personal/{fname}"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path


class PersonalService:

    # ============================================================
    # ROLES
    # ============================================================
    @staticmethod
    def obtener_roles(db: Session):
        return db.query(Rol).all()

    # ============================================================
    # LISTADO
    # ============================================================
    @staticmethod
    def listar(db: Session):
        return db.query(Personal).all()

    # ============================================================
    # DETALLE
    # ============================================================
    @staticmethod
    def obtener_detalle(id: int, db: Session):
        p = db.query(Personal).filter(Personal.id_personal == id).first()
        return p

    # ============================================================
    # CREAR PERSONAL
    # ============================================================
    @staticmethod
    def crear(data: dict, foto: UploadFile | None, db: Session):

        foto_url = guardar_foto(foto)

        p = Personal(
            nombres=data["nombres"],
            apellido_paterno=data["apellido_paterno"],
            apellido_materno=data.get("apellido_materno"),
            id_rol=data["id_rol"],

            especialidad_principal=data["especialidad_principal"],
            telefono_personal=data["telefono_personal"],
            correo_personal=data["correo_personal"],

            fecha_ingreso=data["fecha_ingreso"],
            fecha_nacimiento=data["fecha_nacimiento"],

            rfc=data["rfc"],
            curp=data["curp"],

            domicilio_calle=data["domicilio_calle"],
            domicilio_colonia=data["domicilio_colonia"],
            domicilio_cp=data["domicilio_cp"],
            domicilio_municipio=data["domicilio_municipio"],
            domicilio_estado=data["domicilio_estado"],

            experiencia=data["experiencia"],
            foto_url=foto_url
        )

        db.add(p)
        db.commit()
        db.refresh(p)

        return p

    # ============================================================
    # ACTUALIZAR PERSONAL
    # ============================================================
    @staticmethod
    def actualizar(id: int, data: dict, foto: UploadFile | None, db: Session):

        p = PersonalService.obtener_detalle(id, db)
        if not p:
            raise HTTPException(404, "Personal no encontrado")

        p.nombres = data["nombres"]
        p.apellido_paterno = data["apellido_paterno"]
        p.apellido_materno = data.get("apellido_materno")
        p.id_rol = data["id_rol"]

        p.especialidad_principal = data["especialidad_principal"]
        p.telefono_personal = data["telefono_personal"]
        p.correo_personal = data["correo_personal"]

        p.fecha_ingreso = data["fecha_ingreso"]
        p.fecha_nacimiento = data["fecha_nacimiento"]

        p.rfc = data["rfc"]
        p.curp = data["curp"]

        p.domicilio_calle = data["domicilio_calle"]
        p.domicilio_colonia = data["domicilio_colonia"]
        p.domicilio_cp = data["domicilio_cp"]
        p.domicilio_municipio = data["domicilio_municipio"]
        p.domicilio_estado = data["domicilio_estado"]

        p.experiencia = data["experiencia"]

        # Nueva foto
        if foto:
            p.foto_url = guardar_foto(foto)

        db.commit()
        return p

  # ============================================================
# HORARIOS
# ============================================================
@staticmethod
def horarios(id: int, db: Session):
    p = PersonalService.obtener_detalle(id, db)
    if not p:
        raise HTTPException(404, "Personal no encontrado")

    # Ejemplo temporal de horarios
    return {
        "lunes":      ["08:00-13:00", "15:00-18:00"],
        "martes":     ["09:00-14:00", "15:00-18:00"],
        "miercoles":  ["08:00-13:00", "15:00-18:00"],
        "jueves":     ["09:00-14:00", "15:00-18:00"],
        "viernes":    ["08:00-13:00", "15:00-18:00"]
    }

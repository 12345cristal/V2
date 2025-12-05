from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.terapias import Terapia
from app.models.personal import Personal
from app.models.terapias_personal import TerapiaPersonal


class TerapiasService:

    # ============================================================
    # LISTAR
    # ============================================================
    @staticmethod
    def listar(db: Session):
        return db.query(Terapia).all()

    # ============================================================
    # CREAR
    # ============================================================
    @staticmethod
    def crear(data: dict, db: Session):
        t = Terapia(
            nombre=data["nombre"],
            descripcion=data.get("descripcion"),
            activo=True
        )
        db.add(t)
        db.commit()
        db.refresh(t)
        return t

    # ============================================================
    # ACTUALIZAR
    # ============================================================
    @staticmethod
    def actualizar(id: int, data: dict, db: Session):
        t = db.query(Terapia).filter(Terapia.id_terapia == id).first()
        if not t:
            raise HTTPException(404, "Terapia no encontrada")

        t.nombre = data["nombre"]
        t.descripcion = data.get("descripcion")
        db.commit()
        return t

    # ============================================================
    # CAMBIAR ESTADO
    # ============================================================
    @staticmethod
    def cambiar_estado(id: int, db: Session):
        t = db.query(Terapia).filter(Terapia.id_terapia == id).first()
        if not t:
            raise HTTPException(404, "Terapia no encontrada")

        t.activo = not t.activo
        db.commit()
        return t

    # ============================================================
    # PERSONAL DISPONIBLE
    # ============================================================
    @staticmethod
    def personal_disponible(db: Session):
        """
        Personal que no está asignado a ninguna terapia o está disponible.
        Lo puedes adaptar según reglas.
        """
        return db.query(Personal).filter(Personal.estado_laboral == "ACTIVO").all()

    # ============================================================
    # PERSONAL ASIGNADO
    # ============================================================
    @staticmethod
    def personal_asignado(db: Session):

        q = (
            db.query(
                Personal.id_personal,
                Personal.nombres,
                Personal.apellido_paterno,
                Personal.apellido_materno,
                Personal.especialidad_principal,
                TerapiaPersonal.id_terapia
            )
            .join(TerapiaPersonal, TerapiaPersonal.id_personal == Personal.id_personal)
            .all()
        )

        return [{
            "id_personal": r.id_personal,
            "nombres": r.nombres,
            "apellido_paterno": r.apellido_paterno,
            "apellido_materno": r.apellido_materno,
            "especialidad_principal": r.especialidad_principal,
            "id_terapia": r.id_terapia
        } for r in q]

    # ============================================================
    # ASIGNAR PERSONAL A TERAPIA
    # ============================================================
    @staticmethod
    def asignar(id_personal: int, id_terapia: int, db: Session):

        existe = (
            db.query(TerapiaPersonal)
            .filter(
                TerapiaPersonal.id_personal == id_personal,
                TerapiaPersonal.id_terapia == id_terapia
            )
            .first()
        )

        if existe:
            raise HTTPException(400, "El personal ya está asignado a esta terapia")

        asignacion = TerapiaPersonal(
            id_personal=id_personal,
            id_terapia=id_terapia,
            activo=True
        )

        db.add(asignacion)
        db.commit()
        return asignacion

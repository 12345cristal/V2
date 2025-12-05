from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.models.citas import Cita
from app.models.catalogo_estados_cita import EstadoCita


# ============================================================
# SERVICIO DE CITAS
# ============================================================
class CitasService:

    # ---------------------------
    # CATÁLOGOS
    # ---------------------------
    @staticmethod
    def obtener_catalogo_estados(db: Session):
        estados = db.query(EstadoCita).filter(EstadoCita.activo == 1).all()
        return estados

    # ---------------------------
    # LISTAR CITAS (filtros)
    # ---------------------------
    @staticmethod
    def listar(fecha, estado, nino, db: Session):

        q = db.query(Cita)

        if fecha:
            q = q.filter(Cita.fecha == fecha)

        if estado:
            q = q.filter(Cita.estado.has(codigo=estado))

        if nino:
            q = q.filter(Cita.nino_id == nino)

        return q.all()

    # ---------------------------
    # CREAR CITA
    # ---------------------------
    @staticmethod
    def crear(dto, db: Session):

        hora_inicio = datetime.strptime(dto["horaInicio"], "%H:%M")
        hora_fin = hora_inicio + timedelta(minutes=dto["duracionMinutos"])

        cita = Cita(
            nombre_nino=dto["nombreNino"],
            tutor_nombre=dto["tutorNombre"],
            telefono_tutor_1=dto["telefonoTutor1"],
            telefono_tutor_2=dto["telefonoTutor2"],

            fecha=dto["fecha"],
            hora_inicio=dto["horaInicio"],
            hora_fin=hora_fin.strftime("%H:%M"),

            estado_id=dto["estadoId"],
            es_reposicion=dto["esReposicion"],
            cita_original_id=dto["citaOriginalId"],

            motivo=dto["motivo"],
            diagnostico_presuntivo=dto["diagnosticoPresuntivo"],
            observaciones=dto["observaciones"]
        )

        db.add(cita)
        db.commit()
        db.refresh(cita)
        return cita

    # ---------------------------
    # EDITAR CITA
    # ---------------------------
    @staticmethod
    def actualizar(id: int, dto, db: Session):
        cita = db.query(Cita).filter(Cita.id == id).first()
        if not cita:
            raise HTTPException(404, "Cita no encontrada")

        hora_inicio = datetime.strptime(dto["horaInicio"], "%H:%M")
        hora_fin = hora_inicio + timedelta(minutes=dto["duracionMinutos"])

        cita.nombre_nino = dto["nombreNino"]
        cita.tutor_nombre = dto["tutorNombre"]
        cita.telefono_tutor_1 = dto["telefonoTutor1"]
        cita.telefono_tutor_2 = dto["telefonoTutor2"]

        cita.fecha = dto["fecha"]
        cita.hora_inicio = dto["horaInicio"]
        cita.hora_fin = hora_fin.strftime("%H:%M")

        cita.estado_id = dto["estadoId"]
        cita.es_reposicion = dto["esReposicion"]
        cita.cita_original_id = dto["citaOriginalId"]

        cita.motivo = dto["motivo"]
        cita.diagnostico_presuntivo = dto["diagnosticoPresuntivo"]
        cita.observaciones = dto["observaciones"]

        db.commit()
        return cita

    # ---------------------------
    # CANCELAR CITA
    # ---------------------------
    @staticmethod
    def cancelar(id: int, motivo: str, db: Session):
        cita = db.query(Cita).filter(Cita.id == id).first()
        if not cita:
            raise HTTPException(404, "Cita no encontrada")

        # Estado CANCELADA = código "CANCELADA"
        estado_cancelada = (
            db.query(EstadoCita)
            .filter(EstadoCita.codigo == "CANCELADA")
            .first()
        )
        cita.estado_id = estado_cancelada.id
        cita.motivo = motivo

        db.commit()
        return cita

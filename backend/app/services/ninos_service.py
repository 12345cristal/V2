import os
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException

from app.models.ninos import Nino
from app.models.ninos_direccion import NinoDireccion
from app.models.ninos_diagnostico import NinoDiagnostico
from app.models.ninos_escolar import NinoEscolar
from app.models.ninos_info_centro import NinoInfoCentro
from app.models.ninos_contactos import NinoContactoEmergencia
from app.models.ninos_medicamentos import NinoMedicamento
from app.models.ninos_alergias import NinoAlergias
from app.models.ninos_archivos import NinoArchivo


def guardar_archivo(file: UploadFile, carpeta: str):
    if not file:
        return None
    ext = file.filename.split(".")[-1]
    fname = f"{uuid.uuid4()}.{ext}"
    path = f"uploads/{carpeta}/{fname}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path



class NinosService:

    # -----------------------------
    # LISTAR PARA ninos.ts
    # -----------------------------
    @staticmethod
    def listar_todos(db: Session):
        q = db.query(Nino).all()
        return q

    # -----------------------------
    # DETALLE COMPLETO (editar)
    # -----------------------------
    @staticmethod
    def obtener_detalle(id: int, db: Session):
        n = db.query(Nino).filter(Nino.id == id).first()
        return n

    # -----------------------------
    # CREAR NIÑO
    # -----------------------------
    @staticmethod
    def crear(data: dict, archivos: dict, db: Session):

        n = Nino(
            nombre=data["nombre"],
            apellido_paterno=data["apellidoPaterno"],
            apellido_materno=data["apellidoMaterno"],
            fecha_nacimiento=data["fechaNacimiento"],
            edad=data["edad"],
            sexo=data["sexo"],
            curp=data.get("curp")
        )

        db.add(n)
        db.commit()
        db.refresh(n)

        # SUBTABLAS ===================================

        db.add(NinoDireccion(
            nino_id=n.id,
            **data["direccion"]
        ))

        db.add(NinoDiagnostico(
            nino_id=n.id,
            diagnostico_principal=data["diagnostico"]["diagnosticoPrincipal"],
            fecha_diagnostico=data["diagnostico"].get("fechaDiagnostico"),
            diagnosticos_secundarios=",".join(
                data["diagnostico"]["diagnosticosSecundarios"]
            ),
            especialista=data["diagnostico"].get("especialista"),
            institucion=data["diagnostico"].get("institucion")
        ))

        db.add(NinoAlergias(
            nino_id=n.id,
            **data["alergias"]
        ))

        db.add(NinoEscolar(
            nino_id=n.id,
            **data["escolar"]
        ))

        # Contactos emergencia
        for c in data["contactosEmergencia"]:
            db.add(NinoContactoEmergencia(
                nino_id=n.id,
                nombre=c["nombreCompleto"],
                relacion=c["relacion"],
                telefono=c["telefono"],
                telefono_secundario=c.get("telefonoSecundario")
            ))

        # Medicamentos
        for m in data["medicamentosActuales"]:
            db.add(NinoMedicamento(
                nino_id=n.id,
                nombre=m["nombre"],
                dosis=m.get("dosis"),
                horario=m.get("horario")
            ))

        # Info centro
        infoCentro = data["infoCentro"]
        terapias = infoCentro["terapias"]

        db.add(NinoInfoCentro(
            nino_id=n.id,
            fecha_ingreso=infoCentro["fechaIngreso"],
            costo_mensual=infoCentro.get("costoMensual"),
            modalidad_pago=infoCentro.get("modalidadPago"),
            terapeuta_asignado=infoCentro.get("terapeutaAsignado"),
            horarios_terapia=infoCentro.get("horariosTerapia"),
            estado=infoCentro["estado"],
            terapia_lenguaje=terapias["lenguaje"],
            terapia_conductual=terapias["conductual"],
            terapia_ocupacional=terapias["ocupacional"],
            terapia_sensorial=terapias["sensorial"],
            terapia_psicologia=terapias["psicologia"],
        ))


        # ARCHIVOS ===================================
        for key, file in archivos.items():
            ruta = guardar_archivo(file, "ninos")
            if ruta:
                db.add(NinoArchivo(
                    nino_id=n.id,
                    tipo_archivo=key,
                    url_archivo=ruta
                ))

        db.commit()
        return n


    # ---------------------------------
    # ACTUALIZAR NIÑO
    # ---------------------------------
    @staticmethod
    def actualizar(id: int, data: dict, archivos: dict, db: Session):

        n = db.query(Nino).filter(Nino.id == id).first()
        if not n:
            raise HTTPException(404, "Niño no encontrado")

        n.nombre = data["nombre"]
        n.apellido_paterno = data["apellidoPaterno"]
        n.apellido_materno = data["apellidoMaterno"]
        n.fecha_nacimiento = data["fechaNacimiento"]
        n.edad = data["edad"]
        n.sexo = data["sexo"]
        n.curp = data.get("curp")

        # Más updates a subtablas...
        # (idéntico al crear, pero usando UPDATE)

        # Archivos nuevos
        for key, file in archivos.items():
            ruta = guardar_archivo(file, "ninos")
            if ruta:
                db.add(NinoArchivo(
                    nino_id=id,
                    tipo_archivo=key,
                    url_archivo=ruta
                ))

        db.commit()
        return n


    # ---------------------------------
    # RESUMEN PARA TERAPEUTA
    # ---------------------------------
    @staticmethod
    def resumen_terapeuta(id: int, db: Session):
        n = NinosService.obtener_detalle(id, db)
        return {
            "nombre": n.nombre,
            "progresoGeneral": n.progreso_general,
            "diagnostico": n.diagnostico.diagnostico_principal,
            "actividadPendientes": 0,  # luego se conecta
        }

    # ---------------------------------
    # RESUMEN PARA PADRE
    # ---------------------------------
    @staticmethod
    def resumen_padre(id: int, db: Session):
        n = NinosService.obtener_detalle(id, db)
        return {
            "nombre": n.nombre,
            "fechaIngreso": n.info_centro.fecha_ingreso,
            "actividadesPendientes": 0,
            "proximaTerapia": None
        }

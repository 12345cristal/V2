# app/services/ninos_service.py
import json
import os
from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.nino import (
    Nino,
    NinoDireccion,
    NinoDiagnostico,
    NinoAlergias,
    NinoMedicamentoActual,
    NinoEscolar,
    NinoContactoEmergencia,
    NinoInfoEmocional,
    NinoArchivos,
)
from app.schemas.nino import (
    NinoCreate,
    NinoUpdate,
    NinoResumen,
    NinoDetalle,
    InfoCentroOut,
)
from app.services.ai.ninos_ai_service import calcular_progreso_y_riesgo
from app.services.auditoria_service import registrar_accion
from app.services.decision_logs_service import registrar_decision


MEDIA_ROOT = "media/ninos"  # ajusta la ruta a tu gusto


# =============================
# HELPERS
# =============================

def _ensure_media_folder(nino_id: int) -> str:
    folder = os.path.join(MEDIA_ROOT, str(nino_id))
    os.makedirs(folder, exist_ok=True)
    return folder


async def _guardar_archivo(folder: str, field_name: str, file: UploadFile | None) -> Optional[str]:
    if not file:
        return None
    filename = f"{field_name}_{int(datetime.utcnow().timestamp())}_{file.filename}"
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(await file.read())
    # Aquí podrías regresar una URL pública
    return path


def _mapear_a_resumen(n: Nino, progreso: float) -> NinoResumen:
    info_centro = InfoCentroOut(
        fechaIngreso=n.fecha_registro,
        estado=n.estado,
        costoMensual=None,
        modalidadPago=None,
        terapeutaAsignado=None,
        horariosTerapia=None,
    )
    return NinoResumen(
        id=n.id,
        nombre=n.nombre,
        apellidoPaterno=n.apellido_paterno,
        apellidoMaterno=n.apellido_materno,
        infoCentro=info_centro,
        progresoGeneral=progreso,
    )


def _mapear_a_detalle(n: Nino, progreso: float) -> NinoDetalle:
    info_centro = InfoCentroOut(
        fechaIngreso=n.fecha_registro,
        estado=n.estado,
        costoMensual=None,
        modalidadPago=None,
        terapeutaAsignado=None,
        horariosTerapia=None,
    )

    # direccion
    direccion = None
    if n.direccion:
        direccion = {
            "calle": n.direccion.calle,
            "numero": n.direccion.numero,
            "colonia": n.direccion.colonia,
            "municipio": n.direccion.municipio,
            "codigoPostal": n.direccion.codigo_postal,
        }

    diagnostico = None
    if n.diagnostico:
        diagnostico = {
            "diagnosticoPrincipal": n.diagnostico.diagnostico_principal,
            "fechaDiagnostico": n.diagnostico.fecha_diagnostico,
            "diagnosticosSecundarios": [],
            "especialista": n.diagnostico.especialista,
            "institucion": n.diagnostico.institucion,
        }

    alergias = None
    if n.alergias:
        alergias = {
            "medicamentos": n.alergias.medicamentos,
            "alimentos": n.alergias.alimentos,
            "ambiental": n.alergias.ambiental,
        }

    medicamentos = [
        {
            "nombre": m.nombre,
            "dosis": m.dosis,
            "horario": m.horario,
        }
        for m in n.medicamentos_actuales
        if not m.sin_medicamentos
    ]

    escolar = None
    if n.escolar:
        escolar = {
            "escuela": n.escolar.escuela,
            "grado": n.escolar.grado,
            "maestro": None,
            "horarioClases": n.escolar.horario_clases,
            "adaptaciones": n.escolar.adaptaciones,
        }

    contactos = [
        {
            "nombreCompleto": c.nombre_completo,
            "relacion": c.relacion,
            "telefono": c.telefono,
            "telefonoSecundario": c.telefono_secundario,
            "direccion": c.direccion,
        }
        for c in n.contactos_emergencia
    ]

    edad = None
    if n.fecha_nacimiento:
        hoy = datetime.utcnow().date()
        edad = hoy.year - n.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (n.fecha_nacimiento.month, n.fecha_nacimiento.day)
        )

    return NinoDetalle(
        id=n.id,
        nombre=n.nombre,
        apellidoPaterno=n.apellido_paterno,
        apellidoMaterno=n.apellido_materno,
        fechaNacimiento=n.fecha_nacimiento,
        sexo=n.sexo,
        curp=n.curp,
        direccion=direccion,
        diagnostico=diagnostico,
        alergias=alergias,
        medicamentosActuales=medicamentos,
        escolar=escolar,
        contactosEmergencia=contactos,
        infoCentro=info_centro,
        edad=edad,
        progresoGeneral=progreso,
    )


# =============================
# LISTAR
# =============================

def list_ninos(
    db: Session,
    search: Optional[str] = None,
    estado: Optional[str] = None
) -> List[NinoResumen]:
    q = db.query(Nino)

    if estado:
        q = q.filter(Nino.estado == estado)

    if search:
        like = f"%{search.lower()}%"
        q = q.filter(
            (Nino.nombre.ilike(like)) |
            (Nino.apellido_paterno.ilike(like)) |
            (Nino.apellido_materno.ilike(like))
        )

    ninos = q.order_by(Nino.fecha_registro.desc()).all()

    resultados: List[NinoResumen] = []
    for n in ninos:
        progreso, riesgo = calcular_progreso_y_riesgo(db, n.id)
        # podrías usar riesgo luego
        resultados.append(_mapear_a_resumen(n, progreso))

    return resultados


# =============================
# OBTENER POR ID
# =============================

def get_nino_by_id(db: Session, nino_id: int) -> NinoDetalle:
    n = db.query(Nino).filter(Nino.id == nino_id).first()
    if not n:
        raise ValueError("Niño no encontrado")

    progreso, riesgo = calcular_progreso_y_riesgo(db, n.id)
    detalle = _mapear_a_detalle(n, progreso)

    # Log de decisión IA
    registrar_decision(
        db,
        tipo="NINO_PROGRESO_RIESGO",
        entrada={"nino_id": n.id},
        resultado={"progreso": progreso, "riesgo": riesgo},
        usuario_id=None
    )

    return detalle


# =============================
# CREAR
# =============================

async def create_nino(
    db: Session,
    data: NinoCreate,
    archivos: dict,
    usuario_id: int
) -> NinoDetalle:
    n = Nino(
        nombre=data.nombre,
        apellido_paterno=data.apellidoPaterno,
        apellido_materno=data.apellidoMaterno,
        fecha_nacimiento=data.fechaNacimiento,
        sexo=data.sexo,
        curp=data.curp,
        fecha_registro=datetime.utcnow(),
        estado=data.infoCentro.estado if data.infoCentro else "ACTIVO"
    )
    db.add(n)
    db.commit()
    db.refresh(n)

    # Direccion
    if data.direccion:
        db.add(NinoDireccion(
            nino_id=n.id,
            calle=data.direccion.calle,
            numero=data.direccion.numero,
            colonia=data.direccion.colonia,
            municipio=data.direccion.municipio,
            codigo_postal=data.direccion.codigoPostal
        ))

    # Diagnostico
    if data.diagnostico:
        db.add(NinoDiagnostico(
            nino_id=n.id,
            diagnostico_principal=data.diagnostico.diagnosticoPrincipal,
            fecha_diagnostico=data.diagnostico.fechaDiagnostico,
            especialista=data.diagnostico.especialista,
            institucion=data.diagnostico.institucion
        ))

    # Alergias
    if data.alergias:
        db.add(NinoAlergias(
            nino_id=n.id,
            medicamentos=data.alergias.medicamentos,
            alimentos=data.alergias.alimentos,
            ambiental=data.alergias.ambiental
        ))

    # Escolar
    if data.escolar:
        db.add(NinoEscolar(
            nino_id=n.id,
            escuela=data.escolar.escuela,
            grado=data.escolar.grado,
            horario_clases=data.escolar.horarioClases,
            adaptaciones=data.escolar.adaptaciones
        ))

    # Medicamentos
    for m in data.medicamentosActuales:
        db.add(NinoMedicamentoActual(
            nino_id=n.id,
            sin_medicamentos=False,
            nombre=m.nombre,
            dosis=m.dosis,
            horario=m.horario
        ))

    # Contactos emergencia
    for c in data.contactosEmergencia:
        db.add(NinoContactoEmergencia(
            nino_id=n.id,
            nombre_completo=c.nombreCompleto,
            relacion=c.relacion,
            telefono=c.telefono,
            telefono_secundario=c.telefonoSecundario,
            direccion=c.direccion
        ))

    db.commit()

    # Archivos
    folder = _ensure_media_folder(n.id)
    archivos_model = NinoArchivos(nino_id=n.id)

    if archivos:
        if archivos.get("actaNacimiento"):
            archivos_model.acta_nacimiento_url = await _guardar_archivo(folder, "acta", archivos["actaNacimiento"])
        if archivos.get("curp"):
            archivos_model.curp_url = await _guardar_archivo(folder, "curp", archivos["curp"])
        if archivos.get("comprobanteDomicilio"):
            archivos_model.comprobante_domicilio_url = await _guardar_archivo(folder, "comprobante", archivos["comprobanteDomicilio"])
        if archivos.get("foto"):
            archivos_model.foto_url = await _guardar_archivo(folder, "foto", archivos["foto"])
        if archivos.get("diagnostico"):
            archivos_model.diagnostico_url = await _guardar_archivo(folder, "diagnostico", archivos["diagnostico"])
        if archivos.get("consentimiento"):
            archivos_model.consentimiento_url = await _guardar_archivo(folder, "consentimiento", archivos["consentimiento"])
        if archivos.get("hojaIngreso"):
            archivos_model.hoja_ingreso_url = await _guardar_archivo(folder, "hojaIngreso", archivos["hojaIngreso"])

        db.add(archivos_model)
        db.commit()

    registrar_accion(db, usuario_id, "crear", "ninos", n.id)

    progreso, riesgo = calcular_progreso_y_riesgo(db, n.id)
    return _mapear_a_detalle(n, progreso)


# =============================
# ACTUALIZAR
# =============================

async def update_nino(
    db: Session,
    nino_id: int,
    data: NinoUpdate,
    archivos: dict,
    usuario_id: int
) -> NinoDetalle:
    n = db.query(Nino).filter(Nino.id == nino_id).first()
    if not n:
        raise ValueError("Niño no encontrado")

    n.nombre = data.nombre
    n.apellido_paterno = data.apellidoPaterno
    n.apellido_materno = data.apellidoMaterno
    n.fecha_nacimiento = data.fechaNacimiento
    n.sexo = data.sexo
    n.curp = data.curp
    if data.infoCentro:
        n.estado = data.infoCentro.estado

    # Direccion
    if data.direccion:
        if not n.direccion:
            n.direccion = NinoDireccion(nino_id=n.id)
        n.direccion.calle = data.direccion.calle
        n.direccion.numero = data.direccion.numero
        n.direccion.colonia = data.direccion.colonia
        n.direccion.municipio = data.direccion.municipio
        n.direccion.codigo_postal = data.direccion.codigoPostal

    # Diagnostico
    if data.diagnostico:
        if not n.diagnostico:
            n.diagnostico = NinoDiagnostico(nino_id=n.id, diagnostico_principal=data.diagnostico.diagnosticoPrincipal)
        n.diagnostico.diagnostico_principal = data.diagnostico.diagnosticoPrincipal
        n.diagnostico.fecha_diagnostico = data.diagnostico.fechaDiagnostico
        n.diagnostico.especialista = data.diagnostico.especialista
        n.diagnostico.institucion = data.diagnostico.institucion

    # Alergias
    if data.alergias:
        if not n.alergias:
            n.alergias = NinoAlergias(nino_id=n.id)
        n.alergias.medicamentos = data.alergias.medicamentos
        n.alergias.alimentos = data.alergias.alimentos
        n.alergias.ambiental = data.alergias.ambiental

    # Escolar
    if data.escolar:
        if not n.escolar:
            n.escolar = NinoEscolar(nino_id=n.id)
        n.escolar.escuela = data.escolar.escuela
        n.escolar.grado = data.escolar.grado
        n.escolar.horario_clases = data.escolar.horarioClases
        n.escolar.adaptaciones = data.escolar.adaptaciones

    # Medicamentos: borra y vuelve a crear
    for m in list(n.medicamentos_actuales):
        db.delete(m)
    for m in data.medicamentosActuales:
        db.add(NinoMedicamentoActual(
            nino_id=n.id,
            sin_medicamentos=False,
            nombre=m.nombre,
            dosis=m.dosis,
            horario=m.horario
        ))

    # Contactos emergencia: igual
    for c in list(n.contactos_emergencia):
        db.delete(c)
    for c in data.contactosEmergencia:
        db.add(NinoContactoEmergencia(
            nino_id=n.id,
            nombre_completo=c.nombreCompleto,
            relacion=c.relacion,
            telefono=c.telefono,
            telefono_secundario=c.telefonoSecundario,
            direccion=c.direccion
        ))

    db.commit()
    db.refresh(n)

    # Archivos
    if archivos:
        if not n.archivos:
            n.archivos = NinoArchivos(nino_id=n.id)
        folder = _ensure_media_folder(n.id)

        if archivos.get("actaNacimiento"):
            n.archivos.acta_nacimiento_url = await _guardar_archivo(folder, "acta", archivos["actaNacimiento"])
        if archivos.get("curp"):
            n.archivos.curp_url = await _guardar_archivo(folder, "curp", archivos["curp"])
        if archivos.get("comprobanteDomicilio"):
            n.archivos.comprobante_domicilio_url = await _guardar_archivo(folder, "comprobante", archivos["comprobanteDomicilio"])
        if archivos.get("foto"):
            n.archivos.foto_url = await _guardar_archivo(folder, "foto", archivos["foto"])
        if archivos.get("diagnostico"):
            n.archivos.diagnostico_url = await _guardar_archivo(folder, "diagnostico", archivos["diagnostico"])
        if archivos.get("consentimiento"):
            n.archivos.consentimiento_url = await _guardar_archivo(folder, "consentimiento", archivos["consentimiento"])
        if archivos.get("hojaIngreso"):
            n.archivos.hoja_ingreso_url = await _guardar_archivo(folder, "hojaIngreso", archivos["hojaIngreso"])

        db.commit()

    registrar_accion(db, usuario_id, "actualizar", "ninos", n.id)

    progreso, riesgo = calcular_progreso_y_riesgo(db, n.id)
    return _mapear_a_detalle(n, progreso)

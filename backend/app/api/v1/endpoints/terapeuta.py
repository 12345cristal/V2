from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body
from sqlalchemy.orm import Session
import os

from app.api.deps import get_db_session, get_current_user, require_role
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.nino import Nino
from app.models.terapia import Terapia, TerapiaNino, Sesion, Reposicion
from app.schemas.terapeuta import RegistrarAsistencia, ReprogramarSesion, EnviarMensaje

router = APIRouter(tags=["Terapeuta"])


def _get_personal(db: Session, current_user: Usuario) -> Personal:
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="No existe registro de personal para este usuario")
    return personal


# ============= NIÑOS ASIGNADOS =============
@router.get("/ninos", dependencies=[Depends(require_role([3]))])
def obtener_ninos_asignados(
    especialidad: Optional[str] = None,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    # Niños con terapias asignadas al terapeuta actual
    q = (
        db.query(Nino)
        .join(TerapiaNino, TerapiaNino.nino_id == Nino.id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .filter(TerapiaNino.activo == 1)
    )

    # Filtrar por especialidad recibida o usar la principal del terapeuta
    filtro = (especialidad or personal.especialidad_principal or '').strip()
    if filtro:
        q = q.filter((Terapia.categoria == filtro) | (Terapia.nombre.ilike(f"%{filtro}%")))

    ninos = q.distinct().all()

    return [
        {
            "id": n.id,
            "nombre": n.nombre,
            "apellido_paterno": n.apellido_paterno,
            "apellido_materno": n.apellido_materno,
        }
        for n in ninos
    ]


@router.get("/mis-pacientes", dependencies=[Depends(require_role([3]))])
def obtener_mis_pacientes(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Alias para obtener_ninos_asignados - devuelve los pacientes/niños del terapeuta"""
    personal = _get_personal(db, current_user)

    q = (
        db.query(Nino)
        .join(TerapiaNino, TerapiaNino.nino_id == Nino.id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .filter(TerapiaNino.activo == 1)
    )

    ninos = q.distinct().all()

    return [
        {
            "id": n.id,
            "nombre": n.nombre,
            "apellido_paterno": n.apellido_paterno,
            "apellido_materno": n.apellido_materno,
        }
        for n in ninos
    ]


# ============= SESIONES =============
@router.get("/sesiones", dependencies=[Depends(require_role([3]))])
def obtener_sesiones_terapeuta(
    especialidad: Optional[str] = None,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    q = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
    )
    filtro = (especialidad or personal.especialidad_principal or '').strip()
    if filtro:
        q = q.filter((Terapia.categoria == filtro) | (Terapia.nombre.ilike(f"%{filtro}%")))

    sesiones = q.all()

    data = []
    for s in sesiones:
        n = s.terapia_nino.nino
        t = s.terapia_nino.terapia
        data.append({
            "id_sesion": s.id,
            "id_nino": n.id,
            "nombre_nino": f"{n.nombre} {n.apellido_paterno}",
            "terapia": t.nombre,
            "fecha": s.fecha,
            "asistio": bool(s.asistio),
            "observaciones": s.observaciones or "",
        })
    return data


@router.post("/sesiones/registrar", dependencies=[Depends(require_role([3]))])
async def registrar_sesion(
    id_nino: int = Form(...),
    fecha: str = Form(...),
    informacion_clinica: str = Form(...),
    informacion_padres: str = Form(...),
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    # Buscar terapia asignada del niño con este terapeuta
    t_nino = (
        db.query(TerapiaNino)
        .filter(TerapiaNino.nino_id == id_nino, TerapiaNino.terapeuta_id == personal.id, TerapiaNino.activo == 1)
        .first()
    )
    if not t_nino:
        raise HTTPException(status_code=404, detail="El niño no tiene una terapia activa con este terapeuta")

    sesion = Sesion(
        terapia_nino_id=t_nino.id,
        fecha=fecha,
        asistio=1,
        observaciones=f"CLINICA:{informacion_clinica}\nPADRES:{informacion_padres}",
        creado_por=personal.id,
    )
    db.add(sesion)
    db.commit()
    db.refresh(sesion)

    return {"ok": True, "id": sesion.id}


@router.post("/sesiones/reprogramar", dependencies=[Depends(require_role([3]))])
def reprogramar_sesion(
    data: ReprogramarSesion,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    sesion = db.query(Sesion).filter(Sesion.id == data.id_sesion).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    # Crear reposición
    rep = Reposicion(
        nino_id=sesion.terapia_nino.nino_id,
        terapia_id=sesion.terapia_nino.terapia_id,
        fecha_original=sesion.fecha,
        fecha_nueva=f"{data.nueva_fecha} {data.nueva_hora}",
        motivo=data.motivo,
        estado="PENDIENTE",
    )
    db.add(rep)
    db.commit()
    db.refresh(rep)
    return {"ok": True, "id": rep.id}


# ============= ASISTENCIAS =============
@router.get("/asistencias", dependencies=[Depends(require_role([3]))])
def obtener_asistencias(
    periodo: Optional[str] = None,
    especialidad: Optional[str] = None,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)
    q = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .join(Terapia, Terapia.id == TerapiaNino.terapia_id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
    )
    # periodos tipo YYYY-MM
    if periodo:
        q = q.filter(Sesion.fecha.startswith(periodo))

    filtro = (especialidad or personal.especialidad_principal or '').strip()
    if filtro:
        q = q.filter((Terapia.categoria == filtro) | (Terapia.nombre.ilike(f"%{filtro}%")))

    sesiones = q.all()
    data = []
    for s in sesiones:
        n = s.terapia_nino.nino
        t = s.terapia_nino.terapia
        estado = "asistio" if s.asistio else "cancelada"
        data.append({
            "id_sesion": s.id,
            "id_nino": n.id,
            "nombre_nino": f"{n.nombre} {n.apellido_paterno}",
            "terapia": t.nombre,
            "fecha": s.fecha,
            "estado_asistencia": estado,
            "asistencia_registrada": True,
        })
    return data


@router.post("/asistencias/registrar", dependencies=[Depends(require_role([3]))])
def registrar_asistencia(
    data: RegistrarAsistencia,
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    sesion = db.query(Sesion).filter(Sesion.id == data.id_sesion).first()
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    if data.estado == "reprogramada":
        # marcar como no asistió y dejar registro en reposiciones si hay nota
        sesion.asistio = 0
        if data.nota:
            rep = Reposicion(
                nino_id=sesion.terapia_nino.nino_id,
                terapia_id=sesion.terapia_nino.terapia_id,
                fecha_original=sesion.fecha,
                fecha_nueva=data.fecha_registro,
                motivo=data.nota,
                estado="PENDIENTE",
            )
            db.add(rep)
    else:
        sesion.asistio = 1 if data.estado == "asistio" else 0

    db.commit()
    return {"ok": True}


# ============= REPORTES CUATRIMESTRALES =============
@router.post("/reportes/subir", dependencies=[Depends(require_role([3]))])
async def subir_reporte(
    id_nino: int = Form(...),
    cuatrimestre: str = Form(...),
    tipo_reporte: str = Form(...),
    archivo: UploadFile = File(...),
    observaciones: Optional[str] = Form(None),
    current_user: Usuario = Depends(get_current_user),
):
    folder = os.path.join("static", "reportes", str(id_nino))
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{cuatrimestre}_{tipo_reporte}_{archivo.filename}")
    with open(path, "wb") as f:
        f.write(await archivo.read())

    return {
        "ok": True,
        "archivo_url": path.replace("\\", "/"),
        "observaciones": observaciones or "",
    }


@router.get("/reportes", dependencies=[Depends(require_role([3]))])
def obtener_reportes(id_nino: Optional[int] = None):
    # Placeholder: se listaría desde BD; devolvemos vacío para compatibilidad
    return []


@router.delete("/reportes/{id_reporte}", dependencies=[Depends(require_role([3]))])
def eliminar_reporte(id_reporte: int):
    # Placeholder: lógica real eliminaría de BD/FS
    return {"ok": True, "eliminado": id_reporte}


# ============= MENSAJERÍA (PLACEHOLDER) =============
@router.get("/mensajes/conversaciones", dependencies=[Depends(require_role([3]))])
def conversaciones():
    return []


@router.get("/mensajes/conversacion/{id_conv}", dependencies=[Depends(require_role([3]))])
def mensajes(id_conv: int):
    return []


@router.post("/mensajes/enviar", dependencies=[Depends(require_role([3]))])
def enviar_mensaje(data: EnviarMensaje):
    # Placeholder de envío
    return {"ok": True, "to": data.id_destinatario}


@router.put("/mensajes/marcar-leidos/{id_conv}", dependencies=[Depends(require_role([3]))])
def marcar_leidos(id_conv: int):
    # Placeholder de lectura
    return {"ok": True, "conversacion": id_conv}


# ============= INDICADORES =============
@router.get("/indicadores", dependencies=[Depends(require_role([3]))])
def indicadores(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    total_ninos = (
        db.query(Nino)
        .join(TerapiaNino, TerapiaNino.nino_id == Nino.id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .distinct()
        .count()
    )
    total_sesiones = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .count()
    )
    asistencias = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .filter(TerapiaNino.terapeuta_id == personal.id, Sesion.asistio == 1)
        .count()
    )

    return {
        "total_ninos": total_ninos,
        "total_sesiones": total_sesiones,
        "tasa_asistencia": (asistencias / total_sesiones * 100) if total_sesiones else 0,
    }

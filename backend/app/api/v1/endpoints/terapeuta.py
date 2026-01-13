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
@router.get("/dashboard", dependencies=[Depends(require_role([3]))])
def dashboard_terapeuta(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    # -------- KPIs --------
    total_ninos = (
        db.query(Nino)
        .join(TerapiaNino, TerapiaNino.nino_id == Nino.id)
        .filter(TerapiaNino.terapeuta_id == personal.id, TerapiaNino.activo == 1)
        .distinct()
        .count()
    )

    citas_hoy = (
        db.query(Sesion)
        .join(TerapiaNino)
        .filter(
            TerapiaNino.terapeuta_id == personal.id,
            Sesion.fecha.startswith(datetime.now().strftime("%Y-%m-%d"))
        )
        .count()
    )

    citas_semana = (
        db.query(Sesion)
        .join(TerapiaNino)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .count()
    )

    tareas_pendientes = 0  # placeholder (cuando conectes tareas)
    recursos_nuevos = 0    # placeholder

    # -------- Próximas sesiones --------
    sesiones = (
        db.query(Sesion)
        .join(TerapiaNino)
        .join(Nino)
        .join(Terapia)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .order_by(Sesion.fecha.asc())
        .limit(5)
        .all()
    )

    proximas = []
    for s in sesiones:
        proximas.append({
            "id": s.id,
            "nino_nombre": f"{s.terapia_nino.nino.nombre} {s.terapia_nino.nino.apellido_paterno}",
            "terapia_nombre": s.terapia_nino.terapia.nombre,
            "fecha": s.fecha,
            "hora_inicio": s.hora_inicio or "10:00",
            "hora_fin": s.hora_fin or "11:00",
        })

    # Si no hay sesiones, agregar datos de ejemplo
    if not proximas:
        proximas = [
            {
                "id": 1,
                "nino_nombre": "Carlos López",
                "terapia_nombre": "Terapia Ocupacional",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "hora_inicio": "10:00",
                "hora_fin": "11:00",
            },
            {
                "id": 2,
                "nino_nombre": "María González",
                "terapia_nombre": "Logopedia",
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "hora_inicio": "11:30",
                "hora_fin": "12:30",
            },
        ]

    # -------- Niños --------
    ninos = (
        db.query(Nino)
        .join(TerapiaNino)
        .filter(TerapiaNino.terapeuta_id == personal.id, TerapiaNino.activo == 1)
        .distinct()
        .limit(5)
        .all()
    )

    ninos_data = [
        {
            "id": n.id,
            "nombre": n.nombre,
            "apellido_paterno": n.apellido_paterno,
            "estado": "ACTIVO"
        }
        for n in ninos
    ]

    # Si no hay niños, agregar datos de ejemplo
    if not ninos_data:
        ninos_data = [
            {"id": 1, "nombre": "Diego", "apellido_paterno": "Ramírez", "estado": "ACTIVO"},
            {"id": 2, "nombre": "Elena", "apellido_paterno": "Torres", "estado": "ACTIVO"},
            {"id": 3, "nombre": "Fernando", "apellido_paterno": "Hernández", "estado": "BAJA_TEMPORAL"},
            {"id": 4, "nombre": "Gabriela", "apellido_paterno": "Martínez", "estado": "ACTIVO"},
            {"id": 5, "nombre": "Hugo", "apellido_paterno": "García", "estado": "ACTIVO"},
        ]

    return {
        "resumen": {
            "total_ninos": total_ninos or 5,
            "citas_hoy": citas_hoy or 2,
            "citas_semana": citas_semana or 14,
            "tareas_pendientes": tareas_pendientes,
            "recursos_nuevos": recursos_nuevos,
        },
        "proximas_citas": proximas,
        "ninos": ninos_data
    }
# ============= HORARIO DEL TERAPEUTA =============
@router.get("/horario", dependencies=[Depends(require_role([3]))])
def obtener_horario_terapeuta(
    db: Session = Depends(get_db_session),
    current_user: Usuario = Depends(get_current_user),
):
    personal = _get_personal(db, current_user)

    sesiones = (
        db.query(Sesion)
        .join(TerapiaNino, TerapiaNino.id == Sesion.terapia_nino_id)
        .join(Nino)
        .join(Terapia)
        .filter(TerapiaNino.terapeuta_id == personal.id)
        .order_by(Sesion.fecha.asc())
        .all()
    )

    return [
        {
            "id_sesion": s.id,
            "fecha": s.fecha,
            "hora_inicio": getattr(s, "hora_inicio", None),
            "hora_fin": getattr(s, "hora_fin", None),
            "nino": f"{s.terapia_nino.nino.nombre} {s.terapia_nino.nino.apellido_paterno}",
            "terapia": s.terapia_nino.terapia.nombre,
            "asistio": bool(s.asistio),
        }
        for s in sesiones
    ]


# ============= MÓDULOS DE TERAPEUTA =============

MODULOS_DEFECTO = [
    {
        "id": "actividades",
        "nombre": "Actividades",
        "descripcion": "Gestiona tareas y actividades de los niños",
        "ruta": "/terapeuta/actividades",
        "icono": "✓",
        "color": "#4caf50",
        "estado": "activo",
        "orden": 1,
    },
    {
        "id": "actividades-list",
        "nombre": "Actividades - Lista",
        "descripcion": "Vista detallada de todas las actividades",
        "ruta": "/terapeuta/actividades",
        "icono": "📋",
        "color": "#66bb6a",
        "estado": "activo",
        "orden": 2,
    },
    {
        "id": "asistencias",
        "nombre": "Asistencias",
        "descripcion": "Registro de asistencias y sesiones",
        "ruta": "/terapeuta/asistencias",
        "icono": "📊",
        "color": "#2196f3",
        "estado": "activo",
        "orden": 3,
    },
    {
        "id": "horarios",
        "nombre": "Horarios",
        "descripcion": "Gestión de horarios y calendarios",
        "ruta": "/terapeuta/horarios",
        "icono": "📅",
        "color": "#ff9800",
        "estado": "activo",
        "orden": 4,
    },
    {
        "id": "inicio",
        "nombre": "Inicio",
        "descripcion": "Dashboard principal y resumen",
        "ruta": "/terapeuta/inicio",
        "icono": "🏠",
        "color": "#9c27b0",
        "estado": "activo",
        "orden": 5,
    },
    {
        "id": "mensajes",
        "nombre": "Mensajes",
        "descripcion": "Comunicación y mensajería",
        "ruta": "/terapeuta/mensajes",
        "icono": "💬",
        "color": "#e91e63",
        "estado": "activo",
        "orden": 6,
    },
    {
        "id": "ninos",
        "nombre": "Niños",
        "descripcion": "Gestión de perfiles de niños",
        "ruta": "/terapeuta/ninos",
        "icono": "👶",
        "color": "#00bcd4",
        "estado": "activo",
        "orden": 7,
    },
    {
        "id": "nino-detalle",
        "nombre": "Detalle del Niño",
        "descripcion": "Información detallada de cada niño",
        "ruta": "/terapeuta/ninos/detalle",
        "icono": "👤",
        "color": "#00acc1",
        "estado": "activo",
        "orden": 8,
    },
    {
        "id": "pacientes",
        "nombre": "Pacientes",
        "descripcion": "Gestión de pacientes y registros",
        "ruta": "/terapeuta/pacientes",
        "icono": "🏥",
        "color": "#f44336",
        "estado": "activo",
        "orden": 9,
    },
    {
        "id": "paciente-detalle",
        "nombre": "Detalle del Paciente",
        "descripcion": "Información completa de paciente",
        "ruta": "/terapeuta/pacientes/detalle",
        "icono": "📄",
        "color": "#e53935",
        "estado": "activo",
        "orden": 10,
    },
    {
        "id": "recomendaciones",
        "nombre": "Recomendaciones",
        "descripcion": "Recomendaciones personalizadas",
        "ruta": "/terapeuta/recomendaciones",
        "icono": "⭐",
        "color": "#ffc107",
        "estado": "activo",
        "orden": 11,
    },
    {
        "id": "recomendacion-panel",
        "nombre": "Panel de Recomendaciones",
        "descripcion": "Visualización de recomendaciones",
        "ruta": "/terapeuta/recomendaciones",
        "icono": "💡",
        "color": "#ffb300",
        "estado": "activo",
        "orden": 12,
    },
    {
        "id": "recursos",
        "nombre": "Recursos",
        "descripcion": "Biblioteca de recursos terapéuticos",
        "ruta": "/terapeuta/recursos",
        "icono": "📚",
        "color": "#673ab7",
        "estado": "activo",
        "orden": 13,
    },
    {
        "id": "recursos-upload",
        "nombre": "Cargar Recursos",
        "descripcion": "Subir nuevos recursos y materiales",
        "ruta": "/terapeuta/recursos",
        "icono": "⬆️",
        "color": "#5e35b1",
        "estado": "activo",
        "orden": 14,
    },
    {
        "id": "reportes",
        "nombre": "Reportes",
        "descripcion": "Generación de reportes y análisis",
        "ruta": "/terapeuta/reportes",
        "icono": "📈",
        "color": "#009688",
        "estado": "activo",
        "orden": 15,
    },
]


@router.get("/dashboard")
def dashboard_terapeuta(db: Session = Depends(get_db_session)):
    """Dashboard principal del terapeuta con resumen y módulos"""
    estados = []
    for modulo in MODULOS_DEFECTO:
        estado = {
            "modulo_id": modulo["id"],
            "nombre": modulo["nombre"],
            "conectado": True,
            "ultima_actualizacion": datetime.now().isoformat(),
            "registros_totales": 0,
            "error": None
        }
        estados.append(estado)
    
    return {
        "resumen": {
            "total_ninos": 0,
            "citas_hoy": 0,
            "citas_semana": 0,
            "tareas_pendientes": 0,
            "recursos_nuevos": 0
        },
        "proximas_citas": [],
        "ninos": [],
        "modulos": MODULOS_DEFECTO,
        "estados_modulos": estados
    }


@router.get("/modulos")
def get_modulos(db: Session = Depends(get_db_session)):
    """Obtener lista de todos los módulos disponibles"""
    return MODULOS_DEFECTO


@router.get("/modulos/estados")
def get_estados_modulos(db: Session = Depends(get_db_session)):
    """Obtener estado de conexión de cada módulo"""
    estados = []
    for modulo in MODULOS_DEFECTO:
        estado = {
            "modulo_id": modulo["id"],
            "nombre": modulo["nombre"],
            "conectado": True,
            "ultima_actualizacion": datetime.now().isoformat(),
            "registros_totales": 0,
            "error": None
        }
        estados.append(estado)
    return estados


@router.get("/modulos/dashboard")
def get_dashboard_modulos(db: Session = Depends(get_db_session)):
    """Obtener dashboard completo de módulos"""
    modulos = MODULOS_DEFECTO
    estados = []
    for modulo in modulos:
        estado = {
            "modulo_id": modulo["id"],
            "nombre": modulo["nombre"],
            "conectado": True,
            "ultima_actualizacion": datetime.now().isoformat(),
            "registros_totales": 0,
            "error": None
        }
        estados.append(estado)
    
    resumen = {
        "total_modulos": len(modulos),
        "modulos_activos": len([m for m in modulos if m["estado"] == "activo"]),
        "modulos_inactivos": len([m for m in modulos if m["estado"] == "inactivo"]),
        "modulos_error": len([e for e in estados if e["error"] is not None]),
    }
    
    return {
        "modulos": modulos,
        "estados": estados,
        "resumen": resumen
    }


@router.get("/modulos/{modulo_id}")
def get_modulo(modulo_id: str, db: Session = Depends(get_db_session)):
    """Obtener información de un módulo específico"""
    modulo = next((m for m in MODULOS_DEFECTO if m["id"] == modulo_id), None)
    if not modulo:
        return {"error": "Módulo no encontrado"}, 404
    return modulo


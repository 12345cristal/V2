from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List

from app.db.session import get_db
from app.api.deps import get_current_user

# 👉 IMPORTS DIRECTOS (BUENA PRÁCTICA)
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.models.nino import Nino
from app.models.tutor import Tutor
from app.models.sesion import Sesion
from app.models.progreso import Progreso
from app.models.recurso import Recurso
from app.models.recomendacion import Recomendacion


router = APIRouter(
    prefix="/terapeutas",
    tags=["Terapeutas"]
)

# ======================================================
# UTILIDAD: VALIDAR TERAPEUTA
# ======================================================
def validar_terapeuta(
    db: Session,
    current_user: Usuario
) -> Personal:
    if current_user.rol.nombre.upper() != "TERAPEUTA":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para terapeutas"
        )

    terapeuta = db.query(Personal).filter(
        Personal.id_usuario == current_user.id
    ).first()

    if not terapeuta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de terapeuta no encontrado"
        )

    return terapeuta


# ======================================================
# OBTENER PACIENTES DEL TERAPEUTA
# ======================================================
@router.get("/mis-pacientes")
def obtener_mis_pacientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    busqueda: Optional[str] = None
):
    terapeuta = validar_terapeuta(db, current_user)

    query = (
        db.query(Nino)
        .join(Sesion, Sesion.nino_id == Nino.id)
        .filter(Sesion.terapeuta_id == terapeuta.id)
        .distinct()
    )

    if busqueda:
        query = query.filter(
            func.concat(
                Nino.nombre,
                " ",
                Nino.apellido_paterno,
                " ",
                Nino.apellido_materno
            ).ilike(f"%{busqueda}%")
        )

    ninos = query.all()
    respuesta = []

    for nino in ninos:
        tutor = db.query(Tutor).filter(Tutor.id == nino.tutor_id).first()
        usuario_tutor = (
            db.query(Usuario)
            .filter(Usuario.id == tutor.usuario_id)
            .first()
            if tutor else None
        )

        total_sesiones = db.query(func.count(Sesion.id)).filter(
            Sesion.nino_id == nino.id,
            Sesion.terapeuta_id == terapeuta.id
        ).scalar()

        ultima_sesion = db.query(Sesion).filter(
            Sesion.nino_id == nino.id,
            Sesion.terapeuta_id == terapeuta.id
        ).order_by(Sesion.fecha.desc()).first()

        respuesta.append({
            "id": nino.id,
            "nombre": f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip(),
            "estado": nino.estado,
            "padre": usuario_tutor.nombres if usuario_tutor else None,
            "email_padre": usuario_tutor.email if usuario_tutor else None,
            "total_sesiones": total_sesiones or 0,
            "ultima_sesion": ultima_sesion.fecha.isoformat() if ultima_sesion else None
        })

    return respuesta


# ======================================================
# DETALLE COMPLETO DE UN PACIENTE
# ======================================================
@router.get("/paciente/{nino_id}")
def obtener_detalle_paciente(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    terapeuta = validar_terapeuta(db, current_user)

    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    sesiones = db.query(Sesion).filter(
        Sesion.nino_id == nino.id,
        Sesion.terapeuta_id == terapeuta.id
    ).order_by(Sesion.fecha.desc()).all()

    progresos = db.query(Progreso).filter(
        Progreso.nino_id == nino.id
    ).order_by(Progreso.fecha.desc()).limit(5).all()

    recomendaciones = db.query(Recomendacion).filter(
        Recomendacion.nino_id == nino.id
    ).order_by(Recomendacion.fecha.desc()).limit(5).all()

    return {
        "paciente": {
            "id": nino.id,
            "nombre": f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip(),
            "estado": nino.estado,
        },
        "sesiones": [
            {
                "fecha": s.fecha.isoformat(),
                "asistio": s.asistio,
                "observaciones": s.observaciones
            } for s in sesiones
        ],
        "progresos": [
            {
                "area": p.area,
                "nivel": p.nivel,
                "puntuacion": p.puntuacion,
                "fecha": p.fecha.isoformat()
            } for p in progresos
        ],
        "recomendaciones": [
            {
                "recurso_id": r.recurso_id,
                "score": r.score,
                "fuente": r.fuente,
                "fecha": r.fecha.isoformat()
            } for r in recomendaciones
        ]
    }


# ======================================================
# PERFIL DEL TERAPEUTA
# ======================================================
@router.get("/perfil")
def obtener_perfil_terapeuta(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    terapeuta = validar_terapeuta(db, current_user)

    total_pacientes = db.query(
        func.count(func.distinct(Sesion.nino_id))
    ).filter(
        Sesion.terapeuta_id == terapeuta.id
    ).scalar()

    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.terapeuta_id == terapeuta.id
    ).scalar()

    total_recursos = db.query(func.count(Recurso.id)).filter(
        Recurso.personal_id == terapeuta.id
    ).scalar()

    return {
        "nombre": current_user.nombres,
        "email": current_user.email,
        "especialidad": terapeuta.especialidad_principal,
        "estadisticas": {
            "pacientes": total_pacientes or 0,
            "sesiones": total_sesiones or 0,
            "recursos": total_recursos or 0
        }
    }

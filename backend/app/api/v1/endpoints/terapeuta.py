from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import (
    Usuario,
    Personal,
    Nino,
    Tutor,
    Sesion,
    Progreso,
    Recurso,
    Recomendacion
)

router = APIRouter(
    prefix="/terapeutas",
    tags=["Terapeutas"]
)

# ======================================================
# OBTENER PACIENTES DEL TERAPEUTA
# ======================================================
@router.get("/mis-pacientes")
def obtener_mis_pacientes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    busqueda: Optional[str] = None
):
    # Validar rol (TERAPEUTA)
    if current_user.rol.nombre.upper() != "TERAPEUTA":
        raise HTTPException(status_code=403, detail="Acceso solo para terapeutas")

    terapeuta = db.query(Personal).filter(
        Personal.usuario_id == current_user.id
    ).first()

    if not terapeuta:
        raise HTTPException(status_code=404, detail="Perfil de terapeuta no encontrado")

    # Obtener niños por sesiones asociadas al terapeuta
    query = (
        db.query(Nino)
        .join(Sesion, Sesion.nino_id == Nino.id)
        .filter(Sesion.personal_id == terapeuta.id)
        .distinct()
    )

    if busqueda:
        query = query.filter(
            (Nino.nombres.ilike(f"%{busqueda}%")) |
            (Nino.apellidos.ilike(f"%{busqueda}%"))
        )

    ninos = query.all()

    resultado = []

    for nino in ninos:
        tutor = db.query(Tutor).filter(Tutor.id == nino.tutor_id).first()
        usuario_tutor = db.query(Usuario).filter(Usuario.id == tutor.usuario_id).first()

        total_sesiones = db.query(func.count(Sesion.id)).filter(
            Sesion.nino_id == nino.id,
            Sesion.personal_id == terapeuta.id
        ).scalar()

        ultima_sesion = db.query(Sesion).filter(
            Sesion.nino_id == nino.id,
            Sesion.personal_id == terapeuta.id
        ).order_by(Sesion.fecha.desc()).first()

        resultado.append({
            "id": nino.id,
            "nombre": f"{nino.nombres} {nino.apellidos}",
            "diagnostico": nino.diagnostico,
            "nivel_tea": nino.nivel_tea,
            "padre": usuario_tutor.nombres if usuario_tutor else "",
            "email_padre": usuario_tutor.email if usuario_tutor else "",
            "total_sesiones": total_sesiones or 0,
            "ultima_sesion": ultima_sesion.fecha.isoformat() if ultima_sesion else None
        })

    return resultado


# ======================================================
# DETALLE COMPLETO DE UN PACIENTE
# ======================================================
@router.get("/paciente/{nino_id}")
def obtener_detalle_paciente(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre.upper() != "TERAPEUTA":
        raise HTTPException(status_code=403, detail="Acceso solo para terapeutas")

    terapeuta = db.query(Personal).filter(
        Personal.usuario_id == current_user.id
    ).first()

    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    sesiones = db.query(Sesion).filter(
        Sesion.nino_id == nino.id,
        Sesion.personal_id == terapeuta.id
    ).order_by(Sesion.fecha.desc()).all()

    progresos = db.query(Progreso).filter(
        Progreso.nino_id == nino.id
    ).order_by(Progreso.fecha.desc()).limit(5).all()

    recomendaciones = db.query(Recomendacion).filter(
        Recomendacion.nino_id == nino.id,
        Recomendacion.personal_id == terapeuta.id
    ).all()

    return {
        "paciente": {
            "id": nino.id,
            "nombre": f"{nino.nombres} {nino.apellidos}",
            "diagnostico": nino.diagnostico,
            "nivel_tea": nino.nivel_tea,
        },
        "sesiones": [
            {
                "fecha": s.fecha.isoformat(),
                "estado": s.estado,
                "duracion": s.duracion,
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
        "recursos": [
            {
                "titulo": r.recurso.titulo,
                "fecha": r.fecha_recomendacion.isoformat()
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
    if current_user.rol.nombre.upper() != "TERAPEUTA":
        raise HTTPException(status_code=403, detail="Acceso solo para terapeutas")

    terapeuta = db.query(Personal).filter(
        Personal.usuario_id == current_user.id
    ).first()

    total_pacientes = db.query(func.count(func.distinct(Sesion.nino_id))).filter(
        Sesion.personal_id == terapeuta.id
    ).scalar()

    total_sesiones = db.query(func.count(Sesion.id)).filter(
        Sesion.personal_id == terapeuta.id
    ).scalar()

    total_recursos = db.query(func.count(Recurso.id)).filter(
        Recurso.personal_id == terapeuta.id
    ).scalar()

    return {
        "nombre": current_user.nombres,
        "email": current_user.email,
        "especialidad": terapeuta.especialidad,
        "estadisticas": {
            "pacientes": total_pacientes or 0,
            "sesiones": total_sesiones or 0,
            "recursos": total_recursos or 0
        }
    }

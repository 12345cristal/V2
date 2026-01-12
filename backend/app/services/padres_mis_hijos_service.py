# app/services/padres_mis_hijos_service.py
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import and_

from app.models.nino import Nino
from app.models.medicamentos import Medicamento, Alergia
from app.models.tutor import Tutor
from app.schemas.padres_mis_hijos import (
    HijoResponse, AlergiaResponse, MedicamentoResponse,
    MisHijosPageResponse, MisHijosApiResponse
)


def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula la edad basada en la fecha de nacimiento"""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    
    # Ajustar si el cumpleaños aún no ha pasado este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    
    return edad


def obtener_medicamentos_recientes(nino_id: int, db: Session, dias: int = 30) -> List[int]:
    """Obtiene IDs de medicamentos actualizados recientemente"""
    fecha_limite = datetime.now().date()
    # Simplemente retorna medicamentos con flag novedadReciente activo
    medicamentos_recientes = db.query(Medicamento).filter(
        and_(
            Medicamento.nino_id == nino_id,
            Medicamento.novedadReciente == True
        )
    ).all()
    return [m.id for m in medicamentos_recientes]


def obtener_alergias_hijo(nino_id: int, db: Session) -> List[AlergiaResponse]:
    """Obtiene todas las alergias de un niño"""
    alergias = db.query(Alergia).filter(
        Alergia.nino_id == nino_id
    ).all()
    
    return [
        AlergiaResponse(
            id=a.id,
            nombre=a.nombre,
            severidad=a.severidad,
            reaccion=a.reaccion
        )
        for a in alergias
    ]


def obtener_medicamentos_hijo(nino_id: int, db: Session) -> List[MedicamentoResponse]:
    """Obtiene todos los medicamentos de un niño"""
    medicamentos = db.query(Medicamento).filter(
        Medicamento.nino_id == nino_id
    ).order_by(Medicamento.activo.desc(), Medicamento.fecha_actualizacion.desc()).all()
    
    return [
        MedicamentoResponse(
            id=m.id,
            nombre=m.nombre,
            dosis=m.dosis,
            frecuencia=m.frecuencia,
            razon=m.razon,
            fechaInicio=m.fecha_inicio,
            fechaFin=m.fecha_fin,
            activo=m.activo,
            novedadReciente=m.novedadReciente,
            fechaActualizacion=m.fecha_actualizacion
        )
        for m in medicamentos
    ]


def obtener_hijo_detalle(nino: Nino, db: Session) -> HijoResponse:
    """Obtiene los detalles completos de un hijo"""
    # Obtener diagnóstico
    diagnostico = None
    cuatrimestre = None
    fecha_ingreso = None
    
    if nino.diagnostico:
        diagnostico = nino.diagnostico.diagnostico_principal or "No especificado"
    
    # Calcular cuatrimestre (opcional - basado en fecha de registro)
    if nino.fecha_registro:
        meses_registro = (datetime.now() - nino.fecha_registro).days // 30
        cuatrimestre = max(1, (meses_registro // 4) + 1)
        fecha_ingreso = nino.fecha_registro.date()
    
    # Obtener foto
    foto = None
    if nino.archivos and nino.archivos.foto_url:
        foto = nino.archivos.foto_url
    
    # Obtener alergias y medicamentos
    alergias = obtener_alergias_hijo(nino.id, db)
    medicamentos = obtener_medicamentos_hijo(nino.id, db)
    
    # Contar medicamentos nuevos
    novedades = len([m for m in medicamentos if m.novedadReciente])
    
    return HijoResponse(
        id=nino.id,
        nombre=nino.nombre,
        apellidoPaterno=nino.apellido_paterno,
        apellidoMaterno=nino.apellido_materno,
        foto=foto,
        fechaNacimiento=nino.fecha_nacimiento,
        edad=calcular_edad(nino.fecha_nacimiento),
        diagnostico=diagnostico or "Sin diagnóstico",
        cuatrimestre=cuatrimestre or 1,
        fechaIngreso=fecha_ingreso,
        alergias=alergias,
        medicamentos=medicamentos,
        visto=True,  # Por defecto marcado como visto
        novedades=novedades
    )


def obtener_mis_hijos(tutor_id: int, db: Session) -> MisHijosApiResponse:
    """Obtiene todos los hijos del tutor con sus detalles completos"""
    try:
        # Verificar que el tutor existe
        tutor = db.query(Tutor).filter(Tutor.usuario_id == tutor_id).first()
        if not tutor:
            return MisHijosApiResponse(
                exito=False,
                error="Tutor no encontrado"
            )
        
        # Obtener todos los hijos activos del tutor
        ninos = db.query(Nino).filter(
            and_(
                Nino.tutor_id == tutor.id,
                Nino.estado == "ACTIVO"
            )
        ).order_by(Nino.nombre).all()
        
        # Construir respuesta con detalles de cada hijo
        hijos = [obtener_hijo_detalle(nino, db) for nino in ninos]
        
        return MisHijosApiResponse(
            exito=True,
            datos=MisHijosPageResponse(hijos=hijos),
            mensaje=f"Se encontraron {len(hijos)} hijo(s)"
        )
    
    except Exception as e:
        return MisHijosApiResponse(
            exito=False,
            error=str(e)
        )


def obtener_hijo_por_id(tutor_id: int, nino_id: int, db: Session) -> MisHijosApiResponse:
    """Obtiene detalles de un hijo específico"""
    try:
        # Verificar que el tutor existe
        tutor = db.query(Tutor).filter(Tutor.usuario_id == tutor_id).first()
        if not tutor:
            return MisHijosApiResponse(
                exito=False,
                error="Tutor no encontrado"
            )
        
        # Obtener el hijo específico
        nino = db.query(Nino).filter(
            and_(
                Nino.id == nino_id,
                Nino.tutor_id == tutor.id
            )
        ).first()
        
        if not nino:
            return MisHijosApiResponse(
                exito=False,
                error="Hijo no encontrado"
            )
        
        # Construir respuesta
        hijo = obtener_hijo_detalle(nino, db)
        
        return MisHijosApiResponse(
            exito=True,
            datos=MisHijosPageResponse(hijos=[hijo])
        )
    
    except Exception as e:
        return MisHijosApiResponse(
            exito=False,
            error=str(e)
        )


def marcar_medicamento_como_visto(tutor_id: int, nino_id: int, medicamento_id: int, db: Session) -> MisHijosApiResponse:
    """Marca un medicamento como visto (quita la novedad)"""
    try:
        # Verificar que el tutor existe
        tutor = db.query(Tutor).filter(Tutor.usuario_id == tutor_id).first()
        if not tutor:
            return MisHijosApiResponse(
                exito=False,
                error="Tutor no encontrado"
            )
        
        # Obtener el medicamento
        medicamento = db.query(Medicamento).filter(
            and_(
                Medicamento.id == medicamento_id,
                Medicamento.nino_id == nino_id
            )
        ).first()
        
        if not medicamento:
            return MisHijosApiResponse(
                exito=False,
                error="Medicamento no encontrado"
            )
        
        # Marcar como visto (quitar novedad)
        medicamento.novedadReciente = False
        db.commit()
        
        return MisHijosApiResponse(
            exito=True,
            mensaje="Medicamento marcado como visto"
        )
    
    except Exception as e:
        db.rollback()
        return MisHijosApiResponse(
            exito=False,
            error=str(e)
        )

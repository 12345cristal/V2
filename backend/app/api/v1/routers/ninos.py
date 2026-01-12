# app/api/v1/routers/ninos.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, date

from app.db.session import get_db
from app.models.nino import Nino, NinoDireccion, NinoDiagnostico, NinoInfoEmocional, NinoArchivos
from app.models.tutor import Tutor
from app.schemas.nino import (
    NinoCreate,
    NinoUpdate,
    NinoResponse,
    NinoListResponse
)

router = APIRouter(prefix="/ninos", tags=["Niños"])


# ==================== FUNCIONES AUXILIARES ====================

def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula la edad a partir de la fecha de nacimiento"""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    return edad


def construir_respuesta_nino(nino: Nino) -> dict:
    """Construye diccionario de respuesta completo para un niño"""
    edad = calcular_edad(nino.fecha_nacimiento) if nino.fecha_nacimiento else None
    
    return {
        "id": nino.id,
        "nombre": nino.nombre,
        "apellidoPaterno": nino.apellido_paterno,
        "apellidoMaterno": nino.apellido_materno,
        "fechaNacimiento": nino.fecha_nacimiento.isoformat() if nino.fecha_nacimiento else None,
        "edad": edad,
        "sexo": nino.sexo,
        "curp": nino.curp,
        "tutorId": nino.tutor_id,
        "estado": nino.estado,
        "fechaRegistro": nino.fecha_registro.isoformat() if nino.fecha_registro else None,
        "direccion": {
            "calle": nino.direccion.calle if nino.direccion else None,
            "numero": nino.direccion.numero if nino.direccion else None,
            "colonia": nino.direccion.colonia if nino.direccion else None,
            "municipio": nino.direccion.municipio if nino.direccion else None,
            "codigoPostal": nino.direccion.codigo_postal if nino.direccion else None
        } if nino.direccion else None,
        "diagnostico": {
            "diagnosticoPrincipal": nino.diagnostico.diagnostico_principal if nino.diagnostico else None,
            "diagnosticoResumen": nino.diagnostico.diagnostico_resumen if nino.diagnostico else None,
            "archivoUrl": nino.diagnostico.archivo_url if nino.diagnostico else None,
            "fechaDiagnostico": nino.diagnostico.fecha_diagnostico.isoformat() if nino.diagnostico and nino.diagnostico.fecha_diagnostico else None,
            "especialista": nino.diagnostico.especialista if nino.diagnostico else None,
            "institucion": nino.diagnostico.institucion if nino.diagnostico else None
        } if nino.diagnostico else None,
        "infoEmocional": {
            "estimulos": nino.info_emocional.estimulos if nino.info_emocional else None,
            "calmantes": nino.info_emocional.calmantes if nino.info_emocional else None,
            "preferencias": nino.info_emocional.preferencias if nino.info_emocional else None,
            "noTolera": nino.info_emocional.no_tolera if nino.info_emocional else None,
            "palabrasClave": nino.info_emocional.palabras_clave if nino.info_emocional else None,
            "formaComunicacion": nino.info_emocional.forma_comunicacion if nino.info_emocional else None,
            "nivelComprension": nino.info_emocional.nivel_comprension if nino.info_emocional else None
        } if nino.info_emocional else None,
        "archivos": {
            "actaUrl": nino.archivos.acta_url if nino.archivos else None,
            "curpUrl": nino.archivos.curp_url if nino.archivos else None,
            "comprobanteUrl": nino.archivos.comprobante_url if nino.archivos else None,
            "fotoUrl": nino.archivos.foto_url if nino.archivos else None,
            "diagnosticoUrl": nino.archivos.diagnostico_url if nino.archivos else None,
            "consentimientoUrl": nino.archivos.consentimiento_url if nino.archivos else None,
            "hojaIngresoUrl": nino.archivos.hoja_ingreso_url if nino.archivos else None
        } if nino.archivos else None,
        "tutorNombre": f"{nino.tutor.usuario.nombres} {nino.tutor.usuario.apellido_paterno}" if nino.tutor and nino.tutor.usuario else None
    }


# ==================== ENDPOINTS ====================

@router.get("", response_model=List[NinoListResponse])
def listar_ninos(
    tutor_id: Optional[int] = Query(None, description="Filtrar por tutor"),
    estado: Optional[str] = Query(None, description="Filtrar por estado (ACTIVO/INACTIVO)"),
    busqueda: Optional[str] = Query(None, description="Buscar por nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista todos los niños con filtros opcionales"""
    query = db.query(Nino).options(
        joinedload(Nino.tutor).joinedload(Tutor.usuario)
    )
    
    # Aplicar filtros
    if tutor_id is not None:
        query = query.filter(Nino.tutor_id == tutor_id)
    if estado:
        query = query.filter(Nino.estado == estado)
    if busqueda:
        search_term = f"%{busqueda}%"
        query = query.filter(
            (Nino.nombre.like(search_term)) |
            (Nino.apellido_paterno.like(search_term)) |
            (Nino.apellido_materno.like(search_term))
        )
    
    # Ordenar por fecha de registro descendente
    query = query.order_by(Nino.fecha_registro.desc())
    
    ninos = query.offset(skip).limit(limit).all()
    
    # Construir respuesta simplificada para listado
    result = []
    for nino in ninos:
        edad = calcular_edad(nino.fecha_nacimiento) if nino.fecha_nacimiento else None
        result.append({
            "id": nino.id,
            "nombre": nino.nombre,
            "apellidoPaterno": nino.apellido_paterno,
            "apellidoMaterno": nino.apellido_materno,
            "edad": edad,
            "sexo": nino.sexo,
            "estado": nino.estado,
            "tutorNombre": f"{nino.tutor.usuario.nombres} {nino.tutor.usuario.apellido_paterno}" if nino.tutor and nino.tutor.usuario else None,
            "fotoUrl": nino.archivos.foto_url if nino.archivos else None
        })
    
    return result


@router.get("/tutor/{tutor_id}", response_model=List[NinoListResponse])
def listar_ninos_tutor(
    tutor_id: int,
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Lista todos los niños de un tutor específico (para módulo padre)"""
    # Verificar que el tutor existe
    tutor = db.query(Tutor).filter(Tutor.id == tutor_id).first()
    if not tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    query = db.query(Nino).options(
        joinedload(Nino.archivos)
    ).filter(Nino.tutor_id == tutor_id)
    
    if estado:
        query = query.filter(Nino.estado == estado)
    
    query = query.order_by(Nino.nombre)
    
    ninos = query.all()
    
    # Construir respuesta
    result = []
    for nino in ninos:
        edad = calcular_edad(nino.fecha_nacimiento) if nino.fecha_nacimiento else None
        result.append({
            "id": nino.id,
            "nombre": nino.nombre,
            "apellidoPaterno": nino.apellido_paterno,
            "apellidoMaterno": nino.apellido_materno,
            "edad": edad,
            "sexo": nino.sexo,
            "estado": nino.estado,
            "tutorNombre": None,  # No necesario en vista de padre
            "fotoUrl": nino.archivos.foto_url if nino.archivos else None
        })
    
    return result


@router.get("/{nino_id}", response_model=NinoResponse)
def obtener_nino(nino_id: int, db: Session = Depends(get_db)):
    """Obtiene un niño por ID con toda su información"""
    nino = db.query(Nino).options(
        joinedload(Nino.tutor).joinedload(Tutor.usuario),
        joinedload(Nino.direccion),
        joinedload(Nino.diagnostico),
        joinedload(Nino.info_emocional),
        joinedload(Nino.archivos)
    ).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    return construir_respuesta_nino(nino)


@router.post("", response_model=NinoResponse, status_code=201)
def crear_nino(nino_data: NinoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo niño en el sistema"""
    # Validar tutor si se proporciona
    if nino_data.tutor_id:
        tutor = db.query(Tutor).filter(Tutor.id == nino_data.tutor_id).first()
        if not tutor:
            raise HTTPException(status_code=404, detail="Tutor no encontrado")
    
    # Crear niño
    nuevo_nino = Nino(
        nombre=nino_data.nombre,
        apellido_paterno=nino_data.apellido_paterno,
        apellido_materno=nino_data.apellido_materno,
        fecha_nacimiento=nino_data.fecha_nacimiento,
        sexo=nino_data.sexo,
        curp=nino_data.curp,
        tutor_id=nino_data.tutor_id,
        estado=nino_data.estado or "ACTIVO"
    )
    
    db.add(nuevo_nino)
    db.flush()  # Para obtener el ID
    
    # Crear registros relacionados si se proporcionan
    if nino_data.direccion:
        direccion = NinoDireccion(
            nino_id=nuevo_nino.id,
            **nino_data.direccion.dict()
        )
        db.add(direccion)
    
    if nino_data.diagnostico:
        diagnostico = NinoDiagnostico(
            nino_id=nuevo_nino.id,
            **nino_data.diagnostico.dict()
        )
        db.add(diagnostico)
    
    if nino_data.info_emocional:
        info_emocional = NinoInfoEmocional(
            nino_id=nuevo_nino.id,
            **nino_data.info_emocional.dict()
        )
        db.add(info_emocional)
    
    if nino_data.archivos:
        archivos = NinoArchivos(
            nino_id=nuevo_nino.id,
            **nino_data.archivos.dict()
        )
        db.add(archivos)
    
    db.commit()
    db.refresh(nuevo_nino)
    
    return obtener_nino(nuevo_nino.id, db)


@router.put("/{nino_id}", response_model=NinoResponse)
def actualizar_nino(
    nino_id: int,
    nino_data: NinoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un niño existente"""
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Actualizar campos principales
    update_data = nino_data.dict(exclude_unset=True, exclude={'direccion', 'diagnostico', 'info_emocional', 'archivos'})
    for key, value in update_data.items():
        setattr(nino, key, value)
    
    # Actualizar o crear dirección
    if nino_data.direccion:
        if nino.direccion:
            for key, value in nino_data.direccion.dict(exclude_unset=True).items():
                setattr(nino.direccion, key, value)
        else:
            direccion = NinoDireccion(nino_id=nino_id, **nino_data.direccion.dict())
            db.add(direccion)
    
    # Actualizar o crear diagnóstico
    if nino_data.diagnostico:
        if nino.diagnostico:
            for key, value in nino_data.diagnostico.dict(exclude_unset=True).items():
                setattr(nino.diagnostico, key, value)
        else:
            diagnostico = NinoDiagnostico(nino_id=nino_id, **nino_data.diagnostico.dict())
            db.add(diagnostico)
    
    # Actualizar o crear info emocional
    if nino_data.info_emocional:
        if nino.info_emocional:
            for key, value in nino_data.info_emocional.dict(exclude_unset=True).items():
                setattr(nino.info_emocional, key, value)
        else:
            info_emocional = NinoInfoEmocional(nino_id=nino_id, **nino_data.info_emocional.dict())
            db.add(info_emocional)
    
    # Actualizar o crear archivos
    if nino_data.archivos:
        if nino.archivos:
            for key, value in nino_data.archivos.dict(exclude_unset=True).items():
                setattr(nino.archivos, key, value)
        else:
            archivos = NinoArchivos(nino_id=nino_id, **nino_data.archivos.dict())
            db.add(archivos)
    
    db.commit()
    db.refresh(nino)
    
    return obtener_nino(nino_id, db)


@router.delete("/{nino_id}", status_code=204)
def eliminar_nino(nino_id: int, db: Session = Depends(get_db)):
    """Elimina (desactiva) un niño"""
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(status_code=404, detail="Niño no encontrado")
    
    # Marcar como inactivo en lugar de eliminar
    nino.estado = "INACTIVO"
    db.commit()
    
    return None

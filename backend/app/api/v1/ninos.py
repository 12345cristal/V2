# app/api/v1/ninos.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from datetime import date
from app.db.session import get_db
from app.api.deps import get_current_active_user, require_admin_or_coordinator
from app.models.usuario import Usuario
from app.models.nino import Nino, NinoDireccion, NinoDiagnostico, NinoInfoEmocional, NinoArchivos
from app.models.tutor import Tutor
from app.schemas.nino import (
    NinoCreate,
    NinoUpdate,
    NinoRead,
    NinoDetalle,
    NinoListItem,
    NinoListResponse
)


router = APIRouter()


def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula la edad en años"""
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


# ==================================================
# LISTAR NIÑOS (con paginación y búsqueda)
# ==================================================
@router.get("/", response_model=NinoListResponse)
def listar_ninos(
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, apellido o CURP"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Lista todos los niños beneficiarios con paginación y filtros
    
    - **page**: Número de página (default: 1)
    - **page_size**: Elementos por página (default: 10, max: 100)
    - **buscar**: Texto a buscar en nombre, apellidos o CURP
    - **estado**: Filtrar por estado (ACTIVO, BAJA_TEMPORAL, INACTIVO)
    """
    # Query base
    query = db.query(Nino)
    
    # Filtro por búsqueda
    if buscar:
        search_filter = or_(
            Nino.nombre.ilike(f"%{buscar}%"),
            Nino.apellido_paterno.ilike(f"%{buscar}%"),
            Nino.apellido_materno.ilike(f"%{buscar}%"),
            Nino.curp.ilike(f"%{buscar}%")
        )
        query = query.filter(search_filter)
    
    # Filtro por estado
    if estado:
        query = query.filter(Nino.estado == estado)
    
    # Contar total
    total = query.count()
    
    # Ordenar y paginar
    offset = (page - 1) * page_size
    ninos = query.order_by(Nino.fecha_registro.desc()).offset(offset).limit(page_size).all()
    
    # Construir items de respuesta
    items = []
    for nino in ninos:
        # Obtener nombre del tutor
        tutor_nombre = None
        if nino.tutor and nino.tutor.usuario:
            usuario = nino.tutor.usuario
            tutor_nombre = f"{usuario.nombres} {usuario.apellido_paterno}"
        
        # Obtener diagnóstico principal
        diagnostico_principal = None
        if nino.diagnostico:
            diagnostico_principal = nino.diagnostico.diagnostico_principal
        
        item = NinoListItem(
            id=nino.id,
            nombre=nino.nombre,
            apellido_paterno=nino.apellido_paterno,
            apellido_materno=nino.apellido_materno,
            fecha_nacimiento=nino.fecha_nacimiento,
            sexo=nino.sexo,
            edad=calcular_edad(nino.fecha_nacimiento),
            estado=nino.estado,
            tutor_nombre=tutor_nombre,
            diagnostico_principal=diagnostico_principal
        )
        items.append(item)
    
    return NinoListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )


# ==================================================
# OBTENER NIÑO POR ID (detalle completo)
# ==================================================
@router.get("/{nino_id}", response_model=NinoDetalle)
def obtener_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Obtiene el detalle completo de un niño por su ID
    """
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Niño con ID {nino_id} no encontrado"
        )
    
    # Construir respuesta con todos los datos
    tutor_nombre = None
    if nino.tutor and nino.tutor.usuario:
        usuario = nino.tutor.usuario
        tutor_nombre = f"{usuario.nombres} {usuario.apellido_paterno}"
    
    return NinoDetalle(
        id=nino.id,
        nombre=nino.nombre,
        apellido_paterno=nino.apellido_paterno,
        apellido_materno=nino.apellido_materno,
        fecha_nacimiento=nino.fecha_nacimiento,
        sexo=nino.sexo,
        curp=nino.curp,
        tutor_id=nino.tutor_id,
        estado=nino.estado,
        fecha_registro=nino.fecha_registro,
        direccion=nino.direccion,
        diagnostico=nino.diagnostico,
        info_emocional=nino.info_emocional,
        archivos=nino.archivos,
        tutor_nombre=tutor_nombre
    )


# ==================================================
# CREAR NIÑO
# ==================================================
@router.post("/", response_model=NinoRead, status_code=status.HTTP_201_CREATED)
def crear_nino(
    nino_data: NinoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Crea un nuevo niño beneficiario
    """
    # Verificar si existe el tutor
    if nino_data.tutor_id:
        tutor = db.query(Tutor).filter(Tutor.id == nino_data.tutor_id).first()
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor con ID {nino_data.tutor_id} no encontrado"
            )
    
    # Verificar CURP único (si se proporciona)
    if nino_data.curp:
        existe_curp = db.query(Nino).filter(Nino.curp == nino_data.curp).first()
        if existe_curp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un niño registrado con ese CURP"
            )
    
    # Crear niño
    nino = Nino(
        nombre=nino_data.nombre,
        apellido_paterno=nino_data.apellido_paterno,
        apellido_materno=nino_data.apellido_materno,
        fecha_nacimiento=nino_data.fecha_nacimiento,
        sexo=nino_data.sexo,
        curp=nino_data.curp,
        tutor_id=nino_data.tutor_id,
        estado=nino_data.estado
    )
    
    db.add(nino)
    db.commit()
    db.refresh(nino)
    
    # Crear datos relacionados si existen
    if nino_data.direccion:
        direccion = NinoDireccion(
            nino_id=nino.id,
            **nino_data.direccion.model_dump()
        )
        db.add(direccion)
    
    if nino_data.diagnostico:
        diagnostico = NinoDiagnostico(
            nino_id=nino.id,
            **nino_data.diagnostico.model_dump()
        )
        db.add(diagnostico)
    
    if nino_data.info_emocional:
        info_emocional = NinoInfoEmocional(
            nino_id=nino.id,
            **nino_data.info_emocional.model_dump()
        )
        db.add(info_emocional)
    
    if nino_data.archivos:
        archivos = NinoArchivos(
            nino_id=nino.id,
            **nino_data.archivos.model_dump()
        )
        db.add(archivos)
    
    db.commit()
    db.refresh(nino)
    
    return nino


# ==================================================
# ACTUALIZAR NIÑO
# ==================================================
@router.put("/{nino_id}", response_model=NinoRead)
def actualizar_nino(
    nino_id: int,
    nino_data: NinoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Actualiza los datos de un niño existente
    """
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Niño con ID {nino_id} no encontrado"
        )
    
    # Verificar tutor si se está actualizando
    if nino_data.tutor_id is not None:
        tutor = db.query(Tutor).filter(Tutor.id == nino_data.tutor_id).first()
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor con ID {nino_data.tutor_id} no encontrado"
            )
    
    # Verificar CURP único (si se está actualizando)
    if nino_data.curp:
        existe_curp = db.query(Nino).filter(
            Nino.curp == nino_data.curp,
            Nino.id != nino_id
        ).first()
        if existe_curp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro niño registrado con ese CURP"
            )
    
    # Actualizar datos principales
    update_data = nino_data.model_dump(exclude_unset=True, exclude={"direccion", "diagnostico", "info_emocional", "archivos"})
    for field, value in update_data.items():
        setattr(nino, field, value)
    
    # Actualizar o crear dirección
    if nino_data.direccion:
        if nino.direccion:
            for field, value in nino_data.direccion.model_dump(exclude_unset=True).items():
                setattr(nino.direccion, field, value)
        else:
            direccion = NinoDireccion(nino_id=nino.id, **nino_data.direccion.model_dump())
            db.add(direccion)
    
    # Actualizar o crear diagnóstico
    if nino_data.diagnostico:
        if nino.diagnostico:
            for field, value in nino_data.diagnostico.model_dump(exclude_unset=True).items():
                setattr(nino.diagnostico, field, value)
        else:
            diagnostico = NinoDiagnostico(nino_id=nino.id, **nino_data.diagnostico.model_dump())
            db.add(diagnostico)
    
    # Actualizar o crear info emocional
    if nino_data.info_emocional:
        if nino.info_emocional:
            for field, value in nino_data.info_emocional.model_dump(exclude_unset=True).items():
                setattr(nino.info_emocional, field, value)
        else:
            info_emocional = NinoInfoEmocional(nino_id=nino.id, **nino_data.info_emocional.model_dump())
            db.add(info_emocional)
    
    # Actualizar o crear archivos
    if nino_data.archivos:
        if nino.archivos:
            for field, value in nino_data.archivos.model_dump(exclude_unset=True).items():
                setattr(nino.archivos, field, value)
        else:
            archivos = NinoArchivos(nino_id=nino.id, **nino_data.archivos.model_dump())
            db.add(archivos)
    
    db.commit()
    db.refresh(nino)
    
    return nino


# ==================================================
# ELIMINAR NIÑO
# ==================================================
@router.delete("/{nino_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_nino(
    nino_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Elimina un niño del sistema
    """
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Niño con ID {nino_id} no encontrado"
        )
    
    db.delete(nino)
    db.commit()
    
    return None


# ==================================================
# CAMBIAR ESTADO DEL NIÑO
# ==================================================
@router.patch("/{nino_id}/estado")
def cambiar_estado_nino(
    nino_id: int,
    estado: str = Query(..., pattern="^(ACTIVO|BAJA_TEMPORAL|INACTIVO)$"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Cambia el estado de un niño (ACTIVO, BAJA_TEMPORAL, INACTIVO)
    """
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    
    if not nino:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Niño con ID {nino_id} no encontrado"
        )
    
    nino.estado = estado
    db.commit()
    db.refresh(nino)
    
    return {
        "message": f"Estado del niño actualizado a {estado}",
        "nino_id": nino.id,
        "estado": nino.estado
    }


# ==================================================
# ESTADÍSTICAS DE NIÑOS
# ==================================================
@router.get("/estadisticas/resumen")
def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_admin_or_coordinator)
):
    """
    Obtiene estadísticas generales de los niños
    """
    total = db.query(func.count(Nino.id)).scalar()
    activos = db.query(func.count(Nino.id)).filter(Nino.estado == "ACTIVO").scalar()
    baja_temporal = db.query(func.count(Nino.id)).filter(Nino.estado == "BAJA_TEMPORAL").scalar()
    inactivos = db.query(func.count(Nino.id)).filter(Nino.estado == "INACTIVO").scalar()
    
    # Por sexo
    masculino = db.query(func.count(Nino.id)).filter(Nino.sexo == "M").scalar()
    femenino = db.query(func.count(Nino.id)).filter(Nino.sexo == "F").scalar()
    otro = db.query(func.count(Nino.id)).filter(Nino.sexo == "O").scalar()
    
    return {
        "total": total,
        "por_estado": {
            "activos": activos,
            "baja_temporal": baja_temporal,
            "inactivos": inactivos
        },
        "por_sexo": {
            "masculino": masculino,
            "femenino": femenino,
            "otro": otro
        }
    }

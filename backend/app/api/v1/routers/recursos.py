# app/api/v1/routers/recursos.py
from fastapi import APIRouter, HTTPException, Depends, Query, status, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime
import shutil
import os
from pathlib import Path

from app.db.session import get_db
from app.models.recurso import Recurso, TipoRecurso, CategoriaRecurso, NivelRecurso
from app.models.personal import Personal
from app.models.usuario import Usuario
from app.schemas.recurso import (
    RecursoCreate,
    RecursoUpdate,
    RecursoResponse,
    RecursoListItem,
    TipoRecursoResponse,
    CategoriaRecursoResponse,
    NivelRecursoResponse
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/recursos", tags=["Recursos"])

UPLOAD_DIR = Path("uploads/recursos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ==================== ENDPOINTS DE CATÁLOGOS ====================

@router.get("/tipos", response_model=List[TipoRecursoResponse])
def listar_tipos_recurso(db: Session = Depends(get_db)):
    """Obtiene el catálogo de tipos de recurso"""
    tipos = db.query(TipoRecurso).all()
    return tipos


@router.get("/categorias", response_model=List[CategoriaRecursoResponse])
def listar_categorias_recurso(db: Session = Depends(get_db)):
    """Obtiene el catálogo de categorías de recurso"""
    categorias = db.query(CategoriaRecurso).all()
    return categorias


@router.get("/niveles", response_model=List[NivelRecursoResponse])
def listar_niveles_recurso(db: Session = Depends(get_db)):
    """Obtiene el catálogo de niveles de recurso"""
    niveles = db.query(NivelRecurso).order_by(NivelRecurso.orden).all()
    return niveles


# ==================== ENDPOINTS DE RECURSOS ====================

@router.get("", response_model=List[RecursoListItem])
def listar_recursos(
    activo: Optional[int] = Query(None, description="Filtrar por estado activo (0/1)"),
    tipo_id: Optional[int] = Query(None, description="Filtrar por tipo"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    nivel_id: Optional[int] = Query(None, description="Filtrar por nivel"),
    destacado: Optional[int] = Query(None, description="Filtrar destacados"),
    busqueda: Optional[str] = Query(None, description="Buscar en título y descripción"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Lista todos los recursos con filtros opcionales"""
    query = db.query(Recurso).options(
        joinedload(Recurso.tipo),
        joinedload(Recurso.categoria),
        joinedload(Recurso.nivel),
        joinedload(Recurso.personal)
    )
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Recurso.activo == activo)
    if tipo_id is not None:
        query = query.filter(Recurso.tipo_id == tipo_id)
    if categoria_id is not None:
        query = query.filter(Recurso.categoria_id == categoria_id)
    if nivel_id is not None:
        query = query.filter(Recurso.nivel_id == nivel_id)
    if destacado is not None:
        query = query.filter(Recurso.es_destacado == destacado)
    if busqueda:
        search_term = f"%{busqueda}%"
        query = query.filter(
            (Recurso.titulo.like(search_term)) | 
            (Recurso.descripcion.like(search_term))
        )
    
    # Ordenar por fecha de publicación descendente
    query = query.order_by(Recurso.fecha_publicacion.desc())
    
    recursos = query.offset(skip).limit(limit).all()
    
    # Convertir a response
    result = []
    for recurso in recursos:
        result.append({
            "id": recurso.id,
            "titulo": recurso.titulo,
            "descripcion": recurso.descripcion,
            "tipo_nombre": recurso.tipo.nombre if recurso.tipo else None,
            "categoria_nombre": recurso.categoria.nombre if recurso.categoria else None,
            "nivel_nombre": recurso.nivel.nombre if recurso.nivel else None,
            "es_destacado": recurso.es_destacado,
            "fecha_publicacion": recurso.fecha_publicacion
        })
    
    return result


@router.get("/{recurso_id}", response_model=RecursoResponse)
def obtener_recurso(recurso_id: int, db: Session = Depends(get_db)):
    """Obtiene un recurso por ID"""
    recurso = db.query(Recurso).options(
        joinedload(Recurso.tipo),
        joinedload(Recurso.categoria),
        joinedload(Recurso.nivel),
        joinedload(Recurso.personal)
    ).filter(Recurso.id == recurso_id).first()
    
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Construir respuesta
    response_data = {
        "id": recurso.id,
        "personal_id": recurso.personal_id,
        "titulo": recurso.titulo,
        "descripcion": recurso.descripcion,
        "tipo_id": recurso.tipo_id,
        "categoria_id": recurso.categoria_id,
        "nivel_id": recurso.nivel_id,
        "etiquetas": recurso.etiquetas or [],
        "archivo_url": recurso.archivo_url,
        "es_destacado": recurso.es_destacado,
        "fecha_publicacion": recurso.fecha_publicacion,
        "fecha_modificacion": recurso.fecha_modificacion,
        "activo": recurso.activo,
        "personal_nombre": f"{recurso.personal.nombres} {recurso.personal.apellido_paterno}" if recurso.personal else None,
        "tipo_nombre": recurso.tipo.nombre if recurso.tipo else None,
        "categoria_nombre": recurso.categoria.nombre if recurso.categoria else None,
        "nivel_nombre": recurso.nivel.nombre if recurso.nivel else None
    }
    
    return response_data


@router.post("", response_model=RecursoResponse, status_code=201)
def crear_recurso(recurso_data: RecursoCreate, db: Session = Depends(get_db)):
    """Crea un nuevo recurso"""
    # Validar personal si se proporciona
    if recurso_data.personal_id:
        personal = db.query(Personal).filter(Personal.id == recurso_data.personal_id).first()
        if not personal:
            raise HTTPException(status_code=404, detail="Personal no encontrado")
    
    # Crear recurso
    nuevo_recurso = Recurso(
        personal_id=recurso_data.personal_id,
        titulo=recurso_data.titulo,
        descripcion=recurso_data.descripcion,
        tipo_id=recurso_data.tipo_id,
        categoria_id=recurso_data.categoria_id,
        nivel_id=recurso_data.nivel_id,
        etiquetas=recurso_data.etiquetas,
        archivo_url=recurso_data.archivo_url,
        es_destacado=recurso_data.es_destacado,
        fecha_publicacion=datetime.utcnow()
    )
    
    db.add(nuevo_recurso)
    db.commit()
    db.refresh(nuevo_recurso)
    
    # Recargar con relaciones
    return obtener_recurso(nuevo_recurso.id, db)


@router.put("/{recurso_id}", response_model=RecursoResponse)
def actualizar_recurso(
    recurso_id: int,
    recurso_data: RecursoUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza un recurso existente"""
    recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Actualizar campos proporcionados
    update_data = recurso_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(recurso, key, value)
    
    recurso.fecha_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(recurso)
    
    return obtener_recurso(recurso_id, db)


@router.delete("/{recurso_id}", status_code=204)
def eliminar_recurso(recurso_id: int, db: Session = Depends(get_db)):
    """Elimina (desactiva) un recurso"""
    recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Marcar como inactivo en lugar de eliminar
    recurso.activo = 0
    db.commit()
    
    return None


@router.get("/destacados/listar", response_model=List[RecursoListItem])
def listar_recursos_destacados(
    limite: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Lista los recursos destacados"""
    recursos = db.query(Recurso).options(
        joinedload(Recurso.tipo),
        joinedload(Recurso.categoria),
        joinedload(Recurso.nivel)
    ).filter(
        Recurso.es_destacado == 1,
        Recurso.activo == 1
    ).order_by(
        Recurso.fecha_publicacion.desc()
    ).limit(limite).all()
    
    # Convertir a response
    result = []
    for recurso in recursos:
        result.append({
            "id": recurso.id,
            "titulo": recurso.titulo,
            "descripcion": recurso.descripcion,
            "tipo_nombre": recurso.tipo.nombre if recurso.tipo else None,
            "categoria_nombre": recurso.categoria.nombre if recurso.categoria else None,
            "nivel_nombre": recurso.nivel.nombre if recurso.nivel else None,
            "es_destacado": recurso.es_destacado,
            "fecha_publicacion": recurso.fecha_publicacion
        })
    
    return result


@router.get("/recomendados", response_model=List[RecursoResponse])
def obtener_recursos_recomendados(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene recursos recomendados para el padre actual.
    Filtra por hijos asociados al padre.
    """
    if current_user.rol != "padre":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo padres pueden acceder a este endpoint"
        )
    
    # Obtener hijos del padre
    hijos = db.query(Hijo).filter(Hijo.padre_id == current_user.id).all()
    
    if not hijos:
        return []
    
    hijo_ids = [hijo.id for hijo in hijos]
    
    # Obtener recomendaciones para esos hijos
    recomendaciones = db.query(Recomendacion).filter(
        Recomendacion.hijo_id.in_(hijo_ids)
    ).all()
    
    recurso_ids = [rec.recurso_id for rec in recomendaciones]
    
    # Obtener recursos
    recursos = db.query(Recurso).filter(
        Recurso.id.in_(recurso_ids)
    ).order_by(Recurso.fecha_creacion.desc()).all()
    
    # Verificar cuáles están vistos
    recursos_vistos = db.query(RecursoVisto).filter(
        RecursoVisto.usuario_id == current_user.id,
        RecursoVisto.recurso_id.in_(recurso_ids)
    ).all()
    
    vistos_ids = {rv.recurso_id for rv in recursos_vistos}
    
    # Construir respuesta
    resultado = []
    for recurso in recursos:
        # Obtener información del personal que creó el recurso
        personal = db.query(Personal).filter(
            Personal.id == recurso.terapeuta_id
        ).first()
        
        personal_nombre = "Sin asignar"
        if personal and personal.id_usuario:
            usuario = db.query(Usuario).filter(Usuario.id == personal.id_usuario).first()
            if usuario:
                personal_nombre = f"{usuario.nombres} {usuario.apellido_paterno}"
        
        resultado.append({
            "id": recurso.id,
            "titulo": recurso.titulo,
            "descripcion": recurso.descripcion,
            "tipo_recurso": recurso.tipo_recurso,
            "categoria_recurso": recurso.categoria_recurso,
            "nivel_recurso": recurso.nivel_recurso,
            "url": recurso.url or "",
            "archivo": recurso.archivo,
            "objetivo_terapeutico": recurso.objetivo_terapeutico,
            "terapeuta_nombre": personal_nombre,
            "fecha_creacion": recurso.fecha_creacion.isoformat(),
            "visto": recurso.id in vistos_ids
        })
    
    return resultado


@router.post("/{recurso_id}/marcar-visto")
def marcar_recurso_como_visto(
    recurso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Marca un recurso como visto por el usuario actual.
    """
    # Verificar que el recurso existe
    recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso no encontrado"
        )
    
    # Verificar si ya está marcado como visto
    visto_existente = db.query(RecursoVisto).filter(
        RecursoVisto.recurso_id == recurso_id,
        RecursoVisto.usuario_id == current_user.id
    ).first()
    
    if visto_existente:
        return {"message": "Ya marcado como visto", "fecha_visto": visto_existente.fecha_visto}
    
    # Crear registro
    nuevo_visto = RecursoVisto(
        recurso_id=recurso_id,
        usuario_id=current_user.id,
        fecha_visto=datetime.now()
    )
    
    db.add(nuevo_visto)
    db.commit()
    
    return {"message": "Marcado como visto", "fecha_visto": nuevo_visto.fecha_visto}


# ENDPOINTS PARA TERAPEUTA

@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_recurso(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    tipo_recurso: str = Form(...),
    categoria_recurso: str = Form(...),
    nivel_recurso: str = Form(...),
    objetivo_terapeutico: str = Form(...),
    hijo_id: int = Form(...),
    url: Optional[str] = Form(None),
    archivo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un nuevo recurso (solo personal con rol de terapeuta).
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden crear recursos"
        )
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de personal no encontrado"
        )
    
    archivo_path = None
    
    # Guardar archivo si es PDF
    if tipo_recurso == "PDF" and archivo:
        file_extension = archivo.filename.split(".")[-1]
        filename = f"{datetime.now().timestamp()}_{titulo.replace(' ', '_')}.{file_extension}"
        file_path = UPLOAD_DIR / filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
        
        archivo_path = f"/uploads/recursos/{filename}"
    
    # Crear recurso
    nuevo_recurso = Recurso(
        titulo=titulo,
        descripcion=descripcion,
        tipo_recurso=tipo_recurso,
        categoria_recurso=categoria_recurso,
        nivel_recurso=nivel_recurso,
        objetivo_terapeutico=objetivo_terapeutico,
        url=url,
        archivo=archivo_path,
        terapeuta_id=personal.id,
        fecha_creacion=datetime.now()
    )
    
    db.add(nuevo_recurso)
    db.commit()
    db.refresh(nuevo_recurso)
    
    # Note: Removed Recomendacion creation as the model structure has changed
    # This should be handled separately through the recomendaciones endpoint
    
    return {
        "id": nuevo_recurso.id,
        "titulo": nuevo_recurso.titulo,
        "mensaje": "Recurso creado exitosamente"
    }
    
    return {"message": "Recurso creado exitosamente", "id": nuevo_recurso.id}


@router.get("/mis-recursos", response_model=List[RecursoResponse])
def obtener_mis_recursos(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene recursos creados por el personal actual (terapeuta).
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo terapeutas pueden acceder"
        )
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    recursos = db.query(Recurso).filter(
        Recurso.terapeuta_id == personal.id
    ).order_by(Recurso.fecha_creacion.desc()).all()
    
    return recursos


@router.delete("/{recurso_id}")
def eliminar_recurso(
    recurso_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un recurso (solo personal propietario).
    """
    # Verificar que el usuario sea terapeuta (rol_id == 3)
    if current_user.rol_id != 3:
        raise HTTPException(status_code=403, detail="Solo terapeutas")
    
    # Obtener registro de Personal del terapeuta
    personal = db.query(Personal).filter(Personal.id_usuario == current_user.id).first()
    if not personal:
        raise HTTPException(status_code=404, detail="Registro de personal no encontrado")
    
    recurso = db.query(Recurso).filter(
        Recurso.id == recurso_id,
        Recurso.terapeuta_id == personal.id
    ).first()
    
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    # Eliminar archivo si existe
    if recurso.archivo and os.path.exists(recurso.archivo):
        os.remove(recurso.archivo)
    
    db.delete(recurso)
    db.commit()
    
    return {"message": "Recurso eliminado"}

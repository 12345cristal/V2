# app/api/v1/routers/recursos.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.recurso import Recurso, TipoRecurso, CategoriaRecurso, NivelRecurso
from app.models.personal import Personal
from app.schemas.recurso import (
    RecursoCreate,
    RecursoUpdate,
    RecursoResponse,
    RecursoListItem,
    TipoRecursoResponse,
    CategoriaRecursoResponse,
    NivelRecursoResponse
)

router = APIRouter(prefix="/recursos", tags=["Recursos"])


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

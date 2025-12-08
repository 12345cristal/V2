"""
Recurso Service - Lógica de negocio para recursos y tareas
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.recurso import Recurso, TareaRecurso
from app.models.personal import Personal
from app.models.nino import Nino
from app.schemas.recurso import RecursoCreate, RecursoUpdate, TareaRecursoCreate


class RecursoService:
    """Servicio para gestión de recursos educativos"""

    @staticmethod
    def get_recurso_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        tipo_id: Optional[int] = None,
        categoria_id: Optional[int] = None,
        nivel_id: Optional[int] = None,
        es_destacado: Optional[bool] = None,
    ) -> List[Recurso]:
        """
        Obtener lista de recursos con filtros opcionales
        """
        query = db.query(Recurso)

        # Filtrado por búsqueda en título o descripción
        if search:
            query = query.filter(
                or_(
                    Recurso.titulo.ilike(f"%{search}%"),
                    Recurso.descripcion.ilike(f"%{search}%")
                )
            )

        if tipo_id:
            query = query.filter(Recurso.tipo_recurso_id == tipo_id)
        if categoria_id:
            query = query.filter(Recurso.categoria_recurso_id == categoria_id)
        if nivel_id:
            query = query.filter(Recurso.nivel_recurso_id == nivel_id)
        if es_destacado is not None:
            query = query.filter(Recurso.destacado == (1 if es_destacado else 0))

        return query.order_by(Recurso.fecha_creacion.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def get_recurso_by_id(db: Session, recurso_id: int) -> Recurso:
        """Obtener un recurso por su ID"""
        recurso = db.query(Recurso).filter(Recurso.id == recurso_id).first()
        if not recurso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Recurso con ID {recurso_id} no encontrado"
            )
        return recurso

    @staticmethod
    def create_recurso(db: Session, recurso_data: RecursoCreate) -> Recurso:
        """Crear un nuevo recurso"""
        recurso = Recurso(**recurso_data.model_dump())
        db.add(recurso)
        db.commit()
        db.refresh(recurso)
        return recurso

    @staticmethod
    def update_recurso(db: Session, recurso_id: int, recurso_data: RecursoUpdate) -> Recurso:
        """Actualizar un recurso existente"""
        recurso = RecursoService.get_recurso_by_id(db, recurso_id)
        
        update_data = recurso_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(recurso, field, value)
        
        db.commit()
        db.refresh(recurso)
        return recurso

    @staticmethod
    def delete_recurso(db: Session, recurso_id: int) -> dict:
        """Eliminar un recurso por su ID"""
        recurso = RecursoService.get_recurso_by_id(db, recurso_id)
        db.delete(recurso)
        db.commit()
        return {"message": f"Recurso {recurso_id} eliminado exitosamente"}

    @staticmethod
    def asignar_tarea(db: Session, tarea_data: TareaRecursoCreate) -> TareaRecurso:
        """Asignar recurso como tarea a un niño"""
        # Validar que exista el recurso
        recurso = RecursoService.get_recurso_by_id(db, tarea_data.recurso_id)
        
        # Validar que exista el niño
        nino = db.query(Nino).filter(Nino.id == tarea_data.nino_id).first()
        if not nino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Niño con ID {tarea_data.nino_id} no encontrado"
            )
        
        # Crear la tarea
        tarea = TareaRecurso(
            recurso_id=tarea_data.recurso_id,
            nino_id=tarea_data.nino_id,
            personal_id=1,  # TODO: Obtener del usuario actual
            fecha_asignacion=datetime.now(),
            fecha_objetivo=tarea_data.fecha_objetivo,
            observaciones=tarea_data.observaciones,
            completado=0
        )
        
        db.add(tarea)
        db.commit()
        db.refresh(tarea)
        return tarea

    @staticmethod
    def get_tareas_nino(
        db: Session,
        nino_id: int,
        completado: Optional[bool] = None
    ) -> List[TareaRecurso]:
        """Obtener tareas asignadas a un niño"""
        query = db.query(TareaRecurso).filter(TareaRecurso.nino_id == nino_id)
        
        if completado is not None:
            query = query.filter(TareaRecurso.completado == (1 if completado else 0))
        
        return query.order_by(TareaRecurso.fecha_asignacion.desc()).all()

    @staticmethod
    def marcar_tarea_completada(db: Session, tarea_id: int) -> TareaRecurso:
        """Marcar tarea como completada"""
        tarea = db.query(TareaRecurso).filter(TareaRecurso.id == tarea_id).first()
        if not tarea:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarea con ID {tarea_id} no encontrada"
            )
        
        tarea.completado = 1
        tarea.fecha_completado = datetime.now()
        
        db.commit()
        db.refresh(tarea)
        return tarea


# Instancia global del servicio
recurso_service = RecursoService()

"""
Tutor Service - Lógica de negocio para tutores/padres
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.tutor import Tutor
from app.models.usuario import Usuario
from app.schemas.tutor import TutorCreate, TutorUpdate


class TutorService:
    """Servicio para gestión de tutores"""
    
    @staticmethod
    def get_tutor_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        estatus: Optional[str] = None,
    ) -> List[Tutor]:
        """
        Obtener lista de tutores con filtros
        
        Args:
            db: Session de base de datos
            skip: Registros a saltar (paginación)
            limit: Límite de registros
            search: Texto a buscar en nombres/teléfono/email
            estatus: Filtrar por estatus (ACTIVO/INACTIVO)
        
        Returns:
            Lista de tutores
        """
        query = db.query(Tutor).options(
            joinedload(Tutor.usuario),
            joinedload(Tutor.ninos),
        )
        
        # Filtros
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Tutor.nombres.ilike(search_filter),
                    Tutor.apellido_paterno.ilike(search_filter),
                    Tutor.apellido_materno.ilike(search_filter),
                    Tutor.telefono.ilike(search_filter),
                    Tutor.email.ilike(search_filter),
                )
            )
        
        if estatus:
            query = query.filter(Tutor.estatus == estatus)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_tutor_by_id(db: Session, tutor_id: int) -> Tutor:
        """
        Obtener tutor por ID con relaciones
        
        Args:
            db: Session de base de datos
            tutor_id: ID del tutor
        
        Returns:
            Tutor encontrado
        
        Raises:
            HTTPException: Si no existe
        """
        tutor = (
            db.query(Tutor)
            .options(
                joinedload(Tutor.usuario),
                joinedload(Tutor.ninos),
            )
            .filter(Tutor.id == tutor_id)
            .first()
        )
        
        if not tutor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tutor con ID {tutor_id} no encontrado",
            )
        
        return tutor
    
    @staticmethod
    def get_tutor_by_usuario_id(db: Session, usuario_id: int) -> Optional[Tutor]:
        """
        Obtener tutor por ID de usuario
        
        Args:
            db: Session de base de datos
            usuario_id: ID del usuario
        
        Returns:
            Tutor encontrado o None
        """
        return (
            db.query(Tutor)
            .options(
                joinedload(Tutor.usuario),
                joinedload(Tutor.ninos),
            )
            .filter(Tutor.usuario_id == usuario_id)
            .first()
        )
    
    @staticmethod
    def create_tutor(
        db: Session,
        tutor_data: TutorCreate,
    ) -> Tutor:
        """
        Crear nuevo tutor
        
        Args:
            db: Session de base de datos
            tutor_data: Datos del tutor
        
        Returns:
            Tutor creado
        
        Raises:
            HTTPException: Si el usuario no existe o ya tiene tutor
        """
        # Verificar que el usuario existe
        usuario = db.query(Usuario).filter(Usuario.id == tutor_data.usuario_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {tutor_data.usuario_id} no encontrado",
            )
        
        # Verificar que no exista ya un tutor para este usuario
        existing_tutor = TutorService.get_tutor_by_usuario_id(db, tutor_data.usuario_id)
        if existing_tutor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un tutor asociado al usuario {tutor_data.usuario_id}",
            )
        
        # Crear tutor
        tutor = Tutor(**tutor_data.model_dump())
        db.add(tutor)
        db.commit()
        db.refresh(tutor)
        
        return tutor
    
    @staticmethod
    def update_tutor(
        db: Session,
        tutor_id: int,
        tutor_data: TutorUpdate,
    ) -> Tutor:
        """
        Actualizar tutor
        
        Args:
            db: Session de base de datos
            tutor_id: ID del tutor
            tutor_data: Datos a actualizar
        
        Returns:
            Tutor actualizado
        
        Raises:
            HTTPException: Si no existe
        """
        tutor = TutorService.get_tutor_by_id(db, tutor_id)
        
        # Actualizar solo campos proporcionados
        update_data = tutor_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tutor, field, value)
        
        db.commit()
        db.refresh(tutor)
        
        return tutor
    
    @staticmethod
    def delete_tutor(db: Session, tutor_id: int) -> dict:
        """
        Eliminar tutor (soft delete)
        
        Args:
            db: Session de base de datos
            tutor_id: ID del tutor
        
        Returns:
            Dict con mensaje de confirmación
        
        Raises:
            HTTPException: Si no existe
        """
        tutor = TutorService.get_tutor_by_id(db, tutor_id)
        
        # Soft delete
        tutor.estatus = "INACTIVO"
        
        db.commit()
        
        return {"message": f"Tutor {tutor_id} eliminado exitosamente"}
    
    @staticmethod
    def count_tutores(
        db: Session,
        search: Optional[str] = None,
        estatus: Optional[str] = None,
    ) -> int:
        """
        Contar tutores con filtros
        
        Args:
            db: Session de base de datos
            search: Texto a buscar
            estatus: Filtrar por estatus
        
        Returns:
            Número de tutores
        """
        query = db.query(Tutor)
        
        # Aplicar los mismos filtros que get_tutor_list
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Tutor.nombres.ilike(search_filter),
                    Tutor.apellido_paterno.ilike(search_filter),
                    Tutor.apellido_materno.ilike(search_filter),
                    Tutor.telefono.ilike(search_filter),
                    Tutor.email.ilike(search_filter),
                )
            )
        
        if estatus:
            query = query.filter(Tutor.estatus == estatus)
        
        return query.count()
    
    @staticmethod
    def get_ninos_by_tutor(db: Session, tutor_id: int) -> list:
        """
        Obtener niños asociados a un tutor
        
        Args:
            db: Session de base de datos
            tutor_id: ID del tutor
        
        Returns:
            Lista de niños
        """
        tutor = TutorService.get_tutor_by_id(db, tutor_id)
        return tutor.ninos
    
    @staticmethod
    def verificar_acceso_nino(
        db: Session,
        tutor_id: int,
        nino_id: int,
    ) -> bool:
        """
        Verificar si un tutor tiene acceso a un niño
        
        Args:
            db: Session de base de datos
            tutor_id: ID del tutor
            nino_id: ID del niño
        
        Returns:
            True si tiene acceso, False si no
        """
        tutor = TutorService.get_tutor_by_id(db, tutor_id)
        return any(nino.id == nino_id for nino in tutor.ninos)


# Instancia global del servicio
tutor_service = TutorService()

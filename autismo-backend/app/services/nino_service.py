"""
Nino Service - Lógica de negocio para niños (módulo más complejo)
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException, status

from app.models.nino import Nino, NinoDireccion, NinoDiagnostico, NinoInfoEmocional, NinoArchivos
from app.models.tutor import Tutor
from app.schemas.nino import (
    NinoCreate,
    NinoUpdate,
    NinoDireccionCreate,
    NinoDireccionUpdate,
    NinoDiagnosticoCreate,
    NinoDiagnosticoUpdate,
    NinoInfoEmocionalCreate,
    NinoInfoEmocionalUpdate,
    NinoArchivosCreate,
    NinoArchivosUpdate,
)


class NinoService:
    """Servicio para gestión de niños y sus datos relacionados"""
    
    # ============= CRUD NIÑO (BASE) =============
    
    @staticmethod
    def get_nino_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        estado: Optional[str] = None,
        tutor_id: Optional[int] = None,
    ) -> List[Nino]:
        """
        Obtener lista de niños con filtros
        
        Args:
            db: Session de base de datos
            skip: Registros a saltar
            limit: Límite de registros
            search: Buscar en nombres
            estado: Filtrar por estado (ACTIVO/BAJA_TEMPORAL/INACTIVO)
            tutor_id: Filtrar por tutor
        
        Returns:
            Lista de niños
        """
        query = db.query(Nino).options(
            joinedload(Nino.tutor),
            joinedload(Nino.direccion),
            joinedload(Nino.diagnostico),
            joinedload(Nino.info_emocional),
            joinedload(Nino.archivos),
        )
        
        # Filtros
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Nino.nombre.ilike(search_filter),
                    Nino.apellido_paterno.ilike(search_filter),
                    Nino.apellido_materno.ilike(search_filter),
                    Nino.curp.ilike(search_filter),
                )
            )
        
        if estado:
            query = query.filter(Nino.estado == estado)
        
        if tutor_id:
            query = query.filter(Nino.tutor_id == tutor_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_nino_by_id(db: Session, nino_id: int) -> Nino:
        """
        Obtener niño por ID con todas sus relaciones
        
        Args:
            db: Session de base de datos
            nino_id: ID del niño
        
        Returns:
            Niño encontrado
        
        Raises:
            HTTPException: Si no existe
        """
        nino = (
            db.query(Nino)
            .options(
                joinedload(Nino.tutor),
                joinedload(Nino.direccion),
                joinedload(Nino.diagnostico),
                joinedload(Nino.info_emocional),
                joinedload(Nino.archivos),
            )
            .filter(Nino.id == nino_id)
            .first()
        )
        
        if not nino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Niño con ID {nino_id} no encontrado",
            )
        
        return nino
    
    @staticmethod
    def create_nino(db: Session, nino_data: NinoCreate) -> Nino:
        """
        Crear nuevo niño
        
        Args:
            db: Session de base de datos
            nino_data: Datos del niño
        
        Returns:
            Niño creado
        
        Raises:
            HTTPException: Si el tutor no existe
        """
        # Verificar que el tutor existe (si se proporciona)
        if nino_data.tutor_id:
            tutor = db.query(Tutor).filter(Tutor.id == nino_data.tutor_id).first()
            if not tutor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tutor con ID {nino_data.tutor_id} no encontrado",
                )
        
        # Crear niño
        nino = Nino(**nino_data.model_dump())
        db.add(nino)
        db.commit()
        db.refresh(nino)
        
        return nino
    
    @staticmethod
    def update_nino(
        db: Session,
        nino_id: int,
        nino_data: NinoUpdate,
    ) -> Nino:
        """
        Actualizar niño
        
        Args:
            db: Session de base de datos
            nino_id: ID del niño
            nino_data: Datos a actualizar
        
        Returns:
            Niño actualizado
        """
        nino = NinoService.get_nino_by_id(db, nino_id)
        
        # Verificar tutor si se actualiza
        update_data = nino_data.model_dump(exclude_unset=True)
        if "tutor_id" in update_data and update_data["tutor_id"]:
            tutor = db.query(Tutor).filter(Tutor.id == update_data["tutor_id"]).first()
            if not tutor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Tutor con ID {update_data['tutor_id']} no encontrado",
                )
        
        # Actualizar campos
        for field, value in update_data.items():
            setattr(nino, field, value)
        
        db.commit()
        db.refresh(nino)
        
        return nino
    
    @staticmethod
    def delete_nino(db: Session, nino_id: int) -> dict:
        """
        Eliminar niño (soft delete)
        
        Args:
            db: Session de base de datos
            nino_id: ID del niño
        
        Returns:
            Dict con mensaje de confirmación
        """
        nino = NinoService.get_nino_by_id(db, nino_id)
        
        # Soft delete
        nino.estado = "INACTIVO"
        
        db.commit()
        
        return {"message": f"Niño {nino_id} eliminado exitosamente"}
    
    @staticmethod
    def count_ninos(
        db: Session,
        search: Optional[str] = None,
        estado: Optional[str] = None,
        tutor_id: Optional[int] = None,
    ) -> int:
        """Contar niños con filtros"""
        query = db.query(Nino)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Nino.nombre.ilike(search_filter),
                    Nino.apellido_paterno.ilike(search_filter),
                    Nino.apellido_materno.ilike(search_filter),
                    Nino.curp.ilike(search_filter),
                )
            )
        
        if estado:
            query = query.filter(Nino.estado == estado)
        
        if tutor_id:
            query = query.filter(Nino.tutor_id == tutor_id)
        
        return query.count()
    
    # ============= DIRECCIÓN =============
    
    @staticmethod
    def get_direccion_by_nino(db: Session, nino_id: int) -> Optional[NinoDireccion]:
        """Obtener dirección del niño"""
        NinoService.get_nino_by_id(db, nino_id)  # Verificar que existe
        return db.query(NinoDireccion).filter(NinoDireccion.nino_id == nino_id).first()
    
    @staticmethod
    def create_direccion(
        db: Session,
        nino_id: int,
        direccion_data: NinoDireccionCreate,
    ) -> NinoDireccion:
        """Crear dirección del niño"""
        NinoService.get_nino_by_id(db, nino_id)  # Verificar que existe
        
        # Verificar que no exista ya
        existing = NinoService.get_direccion_by_nino(db, nino_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El niño {nino_id} ya tiene una dirección registrada",
            )
        
        direccion = NinoDireccion(nino_id=nino_id, **direccion_data.model_dump())
        db.add(direccion)
        db.commit()
        db.refresh(direccion)
        
        return direccion
    
    @staticmethod
    def update_direccion(
        db: Session,
        nino_id: int,
        direccion_data: NinoDireccionUpdate,
    ) -> NinoDireccion:
        """Actualizar dirección del niño"""
        direccion = NinoService.get_direccion_by_nino(db, nino_id)
        
        if not direccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El niño {nino_id} no tiene dirección registrada",
            )
        
        update_data = direccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(direccion, field, value)
        
        db.commit()
        db.refresh(direccion)
        
        return direccion
    
    # ============= DIAGNÓSTICO =============
    
    @staticmethod
    def get_diagnostico_by_nino(db: Session, nino_id: int) -> Optional[NinoDiagnostico]:
        """Obtener diagnóstico del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        return db.query(NinoDiagnostico).filter(NinoDiagnostico.nino_id == nino_id).first()
    
    @staticmethod
    def create_diagnostico(
        db: Session,
        nino_id: int,
        diagnostico_data: NinoDiagnosticoCreate,
    ) -> NinoDiagnostico:
        """Crear diagnóstico del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        
        existing = NinoService.get_diagnostico_by_nino(db, nino_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El niño {nino_id} ya tiene un diagnóstico registrado",
            )
        
        diagnostico = NinoDiagnostico(nino_id=nino_id, **diagnostico_data.model_dump())
        db.add(diagnostico)
        db.commit()
        db.refresh(diagnostico)
        
        return diagnostico
    
    @staticmethod
    def update_diagnostico(
        db: Session,
        nino_id: int,
        diagnostico_data: NinoDiagnosticoUpdate,
    ) -> NinoDiagnostico:
        """Actualizar diagnóstico del niño"""
        diagnostico = NinoService.get_diagnostico_by_nino(db, nino_id)
        
        if not diagnostico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El niño {nino_id} no tiene diagnóstico registrado",
            )
        
        update_data = diagnostico_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(diagnostico, field, value)
        
        db.commit()
        db.refresh(diagnostico)
        
        return diagnostico
    
    # ============= INFO EMOCIONAL =============
    
    @staticmethod
    def get_info_emocional_by_nino(db: Session, nino_id: int) -> Optional[NinoInfoEmocional]:
        """Obtener info emocional del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        return db.query(NinoInfoEmocional).filter(NinoInfoEmocional.nino_id == nino_id).first()
    
    @staticmethod
    def create_info_emocional(
        db: Session,
        nino_id: int,
        info_data: NinoInfoEmocionalCreate,
    ) -> NinoInfoEmocional:
        """Crear info emocional del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        
        existing = NinoService.get_info_emocional_by_nino(db, nino_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El niño {nino_id} ya tiene info emocional registrada",
            )
        
        info = NinoInfoEmocional(nino_id=nino_id, **info_data.model_dump())
        db.add(info)
        db.commit()
        db.refresh(info)
        
        return info
    
    @staticmethod
    def update_info_emocional(
        db: Session,
        nino_id: int,
        info_data: NinoInfoEmocionalUpdate,
    ) -> NinoInfoEmocional:
        """Actualizar info emocional del niño"""
        info = NinoService.get_info_emocional_by_nino(db, nino_id)
        
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El niño {nino_id} no tiene info emocional registrada",
            )
        
        update_data = info_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(info, field, value)
        
        db.commit()
        db.refresh(info)
        
        return info
    
    # ============= ARCHIVOS =============
    
    @staticmethod
    def get_archivos_by_nino(db: Session, nino_id: int) -> Optional[NinoArchivos]:
        """Obtener archivos del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        return db.query(NinoArchivos).filter(NinoArchivos.nino_id == nino_id).first()
    
    @staticmethod
    def create_archivos(
        db: Session,
        nino_id: int,
        archivos_data: NinoArchivosCreate,
    ) -> NinoArchivos:
        """Crear registro de archivos del niño"""
        NinoService.get_nino_by_id(db, nino_id)
        
        existing = NinoService.get_archivos_by_nino(db, nino_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El niño {nino_id} ya tiene archivos registrados",
            )
        
        archivos = NinoArchivos(nino_id=nino_id, **archivos_data.model_dump())
        db.add(archivos)
        db.commit()
        db.refresh(archivos)
        
        return archivos
    
    @staticmethod
    def update_archivos(
        db: Session,
        nino_id: int,
        archivos_data: NinoArchivosUpdate,
    ) -> NinoArchivos:
        """Actualizar archivos del niño"""
        archivos = NinoService.get_archivos_by_nino(db, nino_id)
        
        if not archivos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El niño {nino_id} no tiene archivos registrados",
            )
        
        update_data = archivos_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(archivos, field, value)
        
        db.commit()
        db.refresh(archivos)
        
        return archivos


# Instancia global del servicio
nino_service = NinoService()

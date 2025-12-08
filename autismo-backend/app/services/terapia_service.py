"""
Terapia Service - Lógica de negocio para terapias, asignaciones y sesiones
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models.terapia import Terapia, TerapiaPersonal, TerapiaNino, Sesion, Reposicion
from app.models.personal import Personal
from app.models.nino import Nino
from app.schemas.terapia import (
    TerapiaCreate,
    TerapiaUpdate,
    TerapiaNinoCreate,
    TerapiaNinoUpdate,
    SesionCreate,
    SesionUpdate,
    ReposicionCreate,
    ReposicionUpdate,
)


class TerapiaService:
    """Servicio para gestión de terapias, asignaciones y sesiones"""
    
    # ============= TERAPIAS (BASE) =============
    
    @staticmethod
    def get_terapia_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        tipo_id: Optional[int] = None,
    ) -> List[Terapia]:
        """Obtener lista de terapias con filtros"""
        query = db.query(Terapia).options(
            joinedload(Terapia.tipo),
            joinedload(Terapia.personal_asignado),
        )
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Terapia.nombre.ilike(search_filter),
                    Terapia.descripcion.ilike(search_filter),
                )
            )
        
        if activo is not None:
            query = query.filter(Terapia.activo == (1 if activo else 0))
        
        if tipo_id:
            query = query.filter(Terapia.tipo_id == tipo_id)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_terapia_by_id(db: Session, terapia_id: int) -> Terapia:
        """Obtener terapia por ID"""
        terapia = (
            db.query(Terapia)
            .options(
                joinedload(Terapia.tipo),
                joinedload(Terapia.personal_asignado),
            )
            .filter(Terapia.id == terapia_id)
            .first()
        )
        
        if not terapia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Terapia con ID {terapia_id} no encontrada",
            )
        
        return terapia
    
    @staticmethod
    def create_terapia(db: Session, terapia_data: TerapiaCreate) -> Terapia:
        """Crear nueva terapia"""
        terapia = Terapia(**terapia_data.model_dump())
        db.add(terapia)
        db.commit()
        db.refresh(terapia)
        return terapia
    
    @staticmethod
    def update_terapia(
        db: Session,
        terapia_id: int,
        terapia_data: TerapiaUpdate,
    ) -> Terapia:
        """Actualizar terapia"""
        terapia = TerapiaService.get_terapia_by_id(db, terapia_id)
        
        update_data = terapia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(terapia, field, value)
        
        db.commit()
        db.refresh(terapia)
        return terapia
    
    @staticmethod
    def delete_terapia(db: Session, terapia_id: int) -> dict:
        """Eliminar terapia (soft delete)"""
        terapia = TerapiaService.get_terapia_by_id(db, terapia_id)
        terapia.activo = 0
        db.commit()
        return {"message": f"Terapia {terapia_id} eliminada exitosamente"}
    
    @staticmethod
    def count_terapias(
        db: Session,
        search: Optional[str] = None,
        activo: Optional[bool] = None,
        tipo_id: Optional[int] = None,
    ) -> int:
        """Contar terapias con filtros"""
        query = db.query(Terapia)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Terapia.nombre.ilike(search_filter),
                    Terapia.descripcion.ilike(search_filter),
                )
            )
        
        if activo is not None:
            query = query.filter(Terapia.activo == (1 if activo else 0))
        
        if tipo_id:
            query = query.filter(Terapia.tipo_id == tipo_id)
        
        return query.count()
    
    # ============= ASIGNACIÓN PERSONAL <-> TERAPIA =============
    
    @staticmethod
    def asignar_personal_terapia(
        db: Session,
        terapia_id: int,
        personal_id: int,
    ) -> TerapiaPersonal:
        """Asignar personal a terapia"""
        # Verificar que existan
        TerapiaService.get_terapia_by_id(db, terapia_id)
        personal = db.query(Personal).filter(Personal.id == personal_id).first()
        if not personal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Personal con ID {personal_id} no encontrado",
            )
        
        # Verificar que no exista ya
        existing = (
            db.query(TerapiaPersonal)
            .filter(
                and_(
                    TerapiaPersonal.terapia_id == terapia_id,
                    TerapiaPersonal.personal_id == personal_id,
                )
            )
            .first()
        )
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Personal {personal_id} ya está asignado a terapia {terapia_id}",
            )
        
        asignacion = TerapiaPersonal(
            terapia_id=terapia_id,
            personal_id=personal_id,
        )
        
        db.add(asignacion)
        db.commit()
        db.refresh(asignacion)
        return asignacion
    
    @staticmethod
    def desasignar_personal_terapia(
        db: Session,
        terapia_id: int,
        personal_id: int,
    ) -> dict:
        """Desasignar personal de terapia"""
        asignacion = (
            db.query(TerapiaPersonal)
            .filter(
                and_(
                    TerapiaPersonal.terapia_id == terapia_id,
                    TerapiaPersonal.personal_id == personal_id,
                )
            )
            .first()
        )
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe asignación de personal {personal_id} a terapia {terapia_id}",
            )
        
        db.delete(asignacion)
        db.commit()
        return {"message": "Asignación eliminada exitosamente"}
    
    # ============= ASIGNACIÓN NIÑO <-> TERAPIA =============
    
    @staticmethod
    def get_terapias_nino(
        db: Session,
        nino_id: int,
        activo: Optional[bool] = None,
    ) -> List[TerapiaNino]:
        """Obtener terapias asignadas a un niño"""
        query = (
            db.query(TerapiaNino)
            .options(
                joinedload(TerapiaNino.terapia),
                joinedload(TerapiaNino.terapeuta),
                joinedload(TerapiaNino.prioridad),
            )
            .filter(TerapiaNino.nino_id == nino_id)
        )
        
        if activo is not None:
            query = query.filter(TerapiaNino.activo == (1 if activo else 0))
        
        return query.all()
    
    @staticmethod
    def asignar_terapia_nino(
        db: Session,
        asignacion_data: TerapiaNinoCreate,
    ) -> TerapiaNino:
        """Asignar terapia a niño con terapeuta"""
        # Verificar que existan
        nino = db.query(Nino).filter(Nino.id == asignacion_data.nino_id).first()
        if not nino:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Niño con ID {asignacion_data.nino_id} no encontrado",
            )
        
        TerapiaService.get_terapia_by_id(db, asignacion_data.terapia_id)
        
        if asignacion_data.terapeuta_id:
            terapeuta = db.query(Personal).filter(Personal.id == asignacion_data.terapeuta_id).first()
            if not terapeuta:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Terapeuta con ID {asignacion_data.terapeuta_id} no encontrado",
                )
        
        asignacion = TerapiaNino(**asignacion_data.model_dump())
        db.add(asignacion)
        db.commit()
        db.refresh(asignacion)
        return asignacion
    
    @staticmethod
    def update_terapia_nino(
        db: Session,
        asignacion_id: int,
        asignacion_data: TerapiaNinoUpdate,
    ) -> TerapiaNino:
        """Actualizar asignación de terapia a niño"""
        asignacion = db.query(TerapiaNino).filter(TerapiaNino.id == asignacion_id).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignación con ID {asignacion_id} no encontrada",
            )
        
        update_data = asignacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(asignacion, field, value)
        
        db.commit()
        db.refresh(asignacion)
        return asignacion
    
    @staticmethod
    def delete_terapia_nino(db: Session, asignacion_id: int) -> dict:
        """Eliminar asignación (soft delete)"""
        asignacion = db.query(TerapiaNino).filter(TerapiaNino.id == asignacion_id).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignación con ID {asignacion_id} no encontrada",
            )
        
        asignacion.activo = 0
        db.commit()
        return {"message": "Asignación eliminada exitosamente"}
    
    # ============= SESIONES =============
    
    @staticmethod
    def get_sesiones(
        db: Session,
        terapia_nino_id: Optional[int] = None,
        nino_id: Optional[int] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Sesion]:
        """Obtener sesiones con filtros"""
        query = db.query(Sesion).options(
            joinedload(Sesion.terapia_nino),
            joinedload(Sesion.creado_por_personal),
        )
        
        if terapia_nino_id:
            query = query.filter(Sesion.terapia_nino_id == terapia_nino_id)
        
        if nino_id:
            query = query.join(TerapiaNino).filter(TerapiaNino.nino_id == nino_id)
        
        if fecha_desde:
            query = query.filter(Sesion.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Sesion.fecha <= fecha_hasta)
        
        return query.order_by(Sesion.fecha.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_sesion_by_id(db: Session, sesion_id: int) -> Sesion:
        """Obtener sesión por ID"""
        sesion = (
            db.query(Sesion)
            .options(
                joinedload(Sesion.terapia_nino),
                joinedload(Sesion.creado_por_personal),
            )
            .filter(Sesion.id == sesion_id)
            .first()
        )
        
        if not sesion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sesión con ID {sesion_id} no encontrada",
            )
        
        return sesion
    
    @staticmethod
    def create_sesion(db: Session, sesion_data: SesionCreate) -> Sesion:
        """Crear nueva sesión"""
        # Verificar que exista la asignación
        asignacion = db.query(TerapiaNino).filter(
            TerapiaNino.id == sesion_data.terapia_nino_id
        ).first()
        
        if not asignacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignación terapia-niño con ID {sesion_data.terapia_nino_id} no encontrada",
            )
        
        sesion = Sesion(**sesion_data.model_dump())
        db.add(sesion)
        db.commit()
        db.refresh(sesion)
        return sesion
    
    @staticmethod
    def update_sesion(
        db: Session,
        sesion_id: int,
        sesion_data: SesionUpdate,
    ) -> Sesion:
        """Actualizar sesión"""
        sesion = TerapiaService.get_sesion_by_id(db, sesion_id)
        
        update_data = sesion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(sesion, field, value)
        
        db.commit()
        db.refresh(sesion)
        return sesion
    
    @staticmethod
    def delete_sesion(db: Session, sesion_id: int) -> dict:
        """Eliminar sesión (hard delete)"""
        sesion = TerapiaService.get_sesion_by_id(db, sesion_id)
        db.delete(sesion)
        db.commit()
        return {"message": "Sesión eliminada exitosamente"}
    
    # ============= REPOSICIONES =============
    
    @staticmethod
    def get_reposiciones(
        db: Session,
        nino_id: Optional[int] = None,
        estado: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Reposicion]:
        """Obtener reposiciones con filtros"""
        query = db.query(Reposicion).options(
            joinedload(Reposicion.nino),
            joinedload(Reposicion.terapia),
        )
        
        if nino_id:
            query = query.filter(Reposicion.nino_id == nino_id)
        
        if estado:
            query = query.filter(Reposicion.estado == estado)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create_reposicion(db: Session, reposicion_data: ReposicionCreate) -> Reposicion:
        """Crear solicitud de reposición"""
        reposicion = Reposicion(**reposicion_data.model_dump())
        db.add(reposicion)
        db.commit()
        db.refresh(reposicion)
        return reposicion
    
    @staticmethod
    def update_reposicion(
        db: Session,
        reposicion_id: int,
        reposicion_data: ReposicionUpdate,
    ) -> Reposicion:
        """Actualizar reposición"""
        reposicion = db.query(Reposicion).filter(Reposicion.id == reposicion_id).first()
        
        if not reposicion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reposición con ID {reposicion_id} no encontrada",
            )
        
        update_data = reposicion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(reposicion, field, value)
        
        db.commit()
        db.refresh(reposicion)
        return reposicion
    
    @staticmethod
    def aprobar_reposicion(db: Session, reposicion_id: int) -> Reposicion:
        """Aprobar reposición"""
        reposicion = db.query(Reposicion).filter(Reposicion.id == reposicion_id).first()
        
        if not reposicion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reposición con ID {reposicion_id} no encontrada",
            )
        
        reposicion.estado = "APROBADA"
        db.commit()
        db.refresh(reposicion)
        return reposicion
    
    @staticmethod
    def rechazar_reposicion(db: Session, reposicion_id: int) -> Reposicion:
        """Rechazar reposición"""
        reposicion = db.query(Reposicion).filter(Reposicion.id == reposicion_id).first()
        
        if not reposicion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Reposición con ID {reposicion_id} no encontrada",
            )
        
        reposicion.estado = "RECHAZADA"
        db.commit()
        db.refresh(reposicion)
        return reposicion


# Instancia global del servicio
terapia_service = TerapiaService()

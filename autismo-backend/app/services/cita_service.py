"""
Cita Service - Lógica de negocio para citas y programación
"""

from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from app.models.cita import Cita
from app.models.nino import Nino
from app.models.personal import Personal
from app.models.terapia import Terapia
from app.schemas.cita import CitaCreate, CitaUpdate


class CitaService:
    """Servicio para gestión de citas"""
    
    @staticmethod
    def get_cita_list(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        nino_id: Optional[int] = None,
        terapeuta_id: Optional[int] = None,
        terapia_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        estado_id: Optional[int] = None,
        es_reposicion: Optional[bool] = None,
    ) -> List[Cita]:
        """Obtener lista de citas con filtros"""
        query = db.query(Cita).options(
            joinedload(Cita.nino),
            joinedload(Cita.terapeuta),
            joinedload(Cita.terapia),
            joinedload(Cita.estado),
        )
        
        # Filtros
        if nino_id:
            query = query.filter(Cita.nino_id == nino_id)
        
        if terapeuta_id:
            query = query.filter(Cita.terapeuta_id == terapeuta_id)
        
        if terapia_id:
            query = query.filter(Cita.terapia_id == terapia_id)
        
        if fecha_desde:
            query = query.filter(Cita.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Cita.fecha <= fecha_hasta)
        
        if estado_id:
            query = query.filter(Cita.estado_id == estado_id)
        
        if es_reposicion is not None:
            query = query.filter(Cita.es_reposicion == (1 if es_reposicion else 0))
        
        return query.order_by(Cita.fecha.desc(), Cita.hora_inicio).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_cita_by_id(db: Session, cita_id: int) -> Cita:
        """Obtener cita por ID"""
        cita = (
            db.query(Cita)
            .options(
                joinedload(Cita.nino),
                joinedload(Cita.terapeuta),
                joinedload(Cita.terapia),
                joinedload(Cita.estado),
            )
            .filter(Cita.id == cita_id)
            .first()
        )
        
        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cita con ID {cita_id} no encontrada",
            )
        
        return cita
    
    @staticmethod
    def create_cita(db: Session, cita_data: CitaCreate) -> Cita:
        """Crear nueva cita"""
        # Verificar que existan las entidades relacionadas
        if cita_data.nino_id:
            nino = db.query(Nino).filter(Nino.id == cita_data.nino_id).first()
            if not nino:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Niño con ID {cita_data.nino_id} no encontrado",
                )
        
        if cita_data.terapeuta_id:
            terapeuta = db.query(Personal).filter(Personal.id == cita_data.terapeuta_id).first()
            if not terapeuta:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Terapeuta con ID {cita_data.terapeuta_id} no encontrado",
                )
        
        if cita_data.terapia_id:
            terapia = db.query(Terapia).filter(Terapia.id == cita_data.terapia_id).first()
            if not terapia:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Terapia con ID {cita_data.terapia_id} no encontrada",
                )
        
        # Verificar conflictos de horario (mismo terapeuta, misma fecha/hora)
        if cita_data.terapeuta_id:
            conflicto = (
                db.query(Cita)
                .filter(
                    and_(
                        Cita.terapeuta_id == cita_data.terapeuta_id,
                        Cita.fecha == cita_data.fecha,
                        or_(
                            and_(
                                Cita.hora_inicio <= cita_data.hora_inicio,
                                Cita.hora_fin > cita_data.hora_inicio,
                            ),
                            and_(
                                Cita.hora_inicio < cita_data.hora_fin,
                                Cita.hora_fin >= cita_data.hora_fin,
                            ),
                            and_(
                                Cita.hora_inicio >= cita_data.hora_inicio,
                                Cita.hora_fin <= cita_data.hora_fin,
                            ),
                        ),
                    )
                )
                .first()
            )
            
            if conflicto:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El terapeuta ya tiene una cita programada en ese horario",
                )
        
        cita = Cita(**cita_data.model_dump())
        db.add(cita)
        db.commit()
        db.refresh(cita)
        return cita
    
    @staticmethod
    def update_cita(
        db: Session,
        cita_id: int,
        cita_data: CitaUpdate,
    ) -> Cita:
        """Actualizar cita"""
        cita = CitaService.get_cita_by_id(db, cita_id)
        
        update_data = cita_data.model_dump(exclude_unset=True)
        
        # Si se actualiza el horario, verificar conflictos
        if "terapeuta_id" in update_data or "fecha" in update_data or "hora_inicio" in update_data or "hora_fin" in update_data:
            terapeuta_id = update_data.get("terapeuta_id", cita.terapeuta_id)
            fecha = update_data.get("fecha", cita.fecha)
            hora_inicio = update_data.get("hora_inicio", cita.hora_inicio)
            hora_fin = update_data.get("hora_fin", cita.hora_fin)
            
            if terapeuta_id:
                conflicto = (
                    db.query(Cita)
                    .filter(
                        and_(
                            Cita.id != cita_id,  # Excluir la cita actual
                            Cita.terapeuta_id == terapeuta_id,
                            Cita.fecha == fecha,
                            or_(
                                and_(
                                    Cita.hora_inicio <= hora_inicio,
                                    Cita.hora_fin > hora_inicio,
                                ),
                                and_(
                                    Cita.hora_inicio < hora_fin,
                                    Cita.hora_fin >= hora_fin,
                                ),
                                and_(
                                    Cita.hora_inicio >= hora_inicio,
                                    Cita.hora_fin <= hora_fin,
                                ),
                            ),
                        )
                    )
                    .first()
                )
                
                if conflicto:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"El terapeuta ya tiene una cita programada en ese horario",
                    )
        
        for field, value in update_data.items():
            setattr(cita, field, value)
        
        db.commit()
        db.refresh(cita)
        return cita
    
    @staticmethod
    def delete_cita(db: Session, cita_id: int) -> dict:
        """Eliminar cita (hard delete)"""
        cita = CitaService.get_cita_by_id(db, cita_id)
        db.delete(cita)
        db.commit()
        return {"message": f"Cita {cita_id} eliminada exitosamente"}
    
    @staticmethod
    def count_citas(
        db: Session,
        nino_id: Optional[int] = None,
        terapeuta_id: Optional[int] = None,
        terapia_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        estado_id: Optional[int] = None,
        es_reposicion: Optional[bool] = None,
    ) -> int:
        """Contar citas con filtros"""
        query = db.query(Cita)
        
        if nino_id:
            query = query.filter(Cita.nino_id == nino_id)
        
        if terapeuta_id:
            query = query.filter(Cita.terapeuta_id == terapeuta_id)
        
        if terapia_id:
            query = query.filter(Cita.terapia_id == terapia_id)
        
        if fecha_desde:
            query = query.filter(Cita.fecha >= fecha_desde)
        
        if fecha_hasta:
            query = query.filter(Cita.fecha <= fecha_hasta)
        
        if estado_id:
            query = query.filter(Cita.estado_id == estado_id)
        
        if es_reposicion is not None:
            query = query.filter(Cita.es_reposicion == (1 if es_reposicion else 0))
        
        return query.count()
    
    @staticmethod
    def get_citas_by_fecha(
        db: Session,
        fecha: date,
        terapeuta_id: Optional[int] = None,
    ) -> List[Cita]:
        """Obtener citas de una fecha específica"""
        query = (
            db.query(Cita)
            .options(
                joinedload(Cita.nino),
                joinedload(Cita.terapeuta),
                joinedload(Cita.terapia),
                joinedload(Cita.estado),
            )
            .filter(Cita.fecha == fecha)
        )
        
        if terapeuta_id:
            query = query.filter(Cita.terapeuta_id == terapeuta_id)
        
        return query.order_by(Cita.hora_inicio).all()
    
    @staticmethod
    def marcar_asistencia(
        db: Session,
        cita_id: int,
        asistio: bool,
        observaciones: Optional[str] = None,
    ) -> Cita:
        """Marcar asistencia de una cita"""
        cita = CitaService.get_cita_by_id(db, cita_id)
        
        # Cambiar estado según asistencia (asumiendo IDs de estado: 1=Programada, 2=Completada, 3=Cancelada, 4=No asistió)
        if asistio:
            cita.estado_id = 2  # Completada
        else:
            cita.estado_id = 4  # No asistió
        
        if observaciones:
            cita.observaciones = observaciones
        
        db.commit()
        db.refresh(cita)
        return cita
    
    @staticmethod
    def cancelar_cita(
        db: Session,
        cita_id: int,
        motivo: Optional[str] = None,
    ) -> Cita:
        """Cancelar cita"""
        cita = CitaService.get_cita_by_id(db, cita_id)
        
        cita.estado_id = 3  # Cancelada
        if motivo:
            cita.motivo = motivo
        
        db.commit()
        db.refresh(cita)
        return cita


# Instancia global del servicio
cita_service = CitaService()

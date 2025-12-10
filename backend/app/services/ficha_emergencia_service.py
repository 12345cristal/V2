# app/services/ficha_emergencia_service.py
"""
Servicio para gestión de Fichas de Emergencia
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date

from app.models.ficha_emergencia import FichaEmergencia
from app.models.nino import Nino
from app.schemas.ficha_emergencia import (
    FichaEmergenciaCreate,
    FichaEmergenciaUpdate,
    FichaEmergenciaResponse,
    FichaEmergenciaImprimible
)


class FichaEmergenciaService:
    """Servicio para manejo de fichas de emergencia"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def calcular_edad(self, fecha_nacimiento: date) -> int:
        """Calcula edad a partir de fecha de nacimiento"""
        hoy = datetime.now().date()
        edad = hoy.year - fecha_nacimiento.year
        if hoy.month < fecha_nacimiento.month or (
            hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day
        ):
            edad -= 1
        return edad
    
    def crear_ficha(
        self,
        ficha: FichaEmergenciaCreate,
        usuario_id: int
    ) -> FichaEmergenciaResponse:
        """Crea una nueva ficha de emergencia"""
        # Verificar que el niño existe
        nino = self.db.query(Nino).filter(Nino.id == ficha.nino_id).first()
        if not nino:
            raise ValueError(f"Niño con ID {ficha.nino_id} no encontrado")
        
        # Verificar que no existe ficha previa
        ficha_existente = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.nino_id == ficha.nino_id
        ).first()
        if ficha_existente:
            raise ValueError(f"Ya existe una ficha de emergencia para el niño {ficha.nino_id}")
        
        # Crear ficha
        nueva_ficha = FichaEmergencia(
            **ficha.model_dump(),
            creado_por_id=usuario_id,
            activa=True
        )
        
        self.db.add(nueva_ficha)
        self.db.commit()
        self.db.refresh(nueva_ficha)
        
        return self._enriquecer_ficha(nueva_ficha)
    
    def obtener_ficha_por_nino(self, nino_id: int) -> Optional[FichaEmergenciaResponse]:
        """Obtiene la ficha de emergencia de un niño"""
        ficha = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.nino_id == nino_id
        ).first()
        
        if not ficha:
            return None
        
        return self._enriquecer_ficha(ficha)
    
    def obtener_ficha_por_id(self, ficha_id: int) -> Optional[FichaEmergenciaResponse]:
        """Obtiene una ficha por su ID"""
        ficha = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.id == ficha_id
        ).first()
        
        if not ficha:
            return None
        
        return self._enriquecer_ficha(ficha)
    
    def listar_fichas_activas(self) -> List[FichaEmergenciaResponse]:
        """Lista todas las fichas de emergencia activas"""
        fichas = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.activa == True
        ).all()
        
        return [self._enriquecer_ficha(f) for f in fichas]
    
    def actualizar_ficha(
        self,
        ficha_id: int,
        datos: FichaEmergenciaUpdate
    ) -> FichaEmergenciaResponse:
        """Actualiza una ficha de emergencia"""
        ficha = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.id == ficha_id
        ).first()
        
        if not ficha:
            raise ValueError(f"Ficha con ID {ficha_id} no encontrada")
        
        # Actualizar campos
        datos_dict = datos.model_dump(exclude_unset=True)
        for campo, valor in datos_dict.items():
            setattr(ficha, campo, valor)
        
        ficha.fecha_actualizacion = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(ficha)
        
        return self._enriquecer_ficha(ficha)
    
    def desactivar_ficha(self, ficha_id: int) -> bool:
        """Desactiva una ficha de emergencia"""
        ficha = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.id == ficha_id
        ).first()
        
        if not ficha:
            return False
        
        ficha.activa = False
        ficha.fecha_actualizacion = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def obtener_ficha_imprimible(self, nino_id: int) -> FichaEmergenciaImprimible:
        """Obtiene datos de ficha para impresión/visualización"""
        ficha = self.db.query(FichaEmergencia).filter(
            FichaEmergencia.nino_id == nino_id
        ).first()
        
        if not ficha:
            raise ValueError(f"No existe ficha de emergencia para el niño {nino_id}")
        
        nino = ficha.nino
        nombre_completo = f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip()
        
        # Obtener foto si existe
        foto_url = None
        if hasattr(nino, 'archivos') and nino.archivos:
            foto_url = nino.archivos.foto_url
        
        return FichaEmergenciaImprimible(
            # Datos del niño
            nino_nombre_completo=nombre_completo,
            nino_foto_url=foto_url,
            nino_fecha_nacimiento=nino.fecha_nacimiento.strftime('%d/%m/%Y'),
            nino_edad=self.calcular_edad(nino.fecha_nacimiento),
            nino_sexo=nino.sexo,
            
            # Información médica
            tipo_sangre=ficha.tipo_sangre,
            alergias=ficha.alergias,
            diagnostico_principal=ficha.diagnostico_principal,
            medicamentos_actuales=ficha.medicamentos_actuales,
            
            # Contactos
            contacto_principal_nombre=ficha.contacto_principal_nombre,
            contacto_principal_relacion=ficha.contacto_principal_relacion,
            contacto_principal_telefono=ficha.contacto_principal_telefono,
            contacto_principal_telefono_alt=ficha.contacto_principal_telefono_alt,
            contacto_secundario_nombre=ficha.contacto_secundario_nombre,
            contacto_secundario_telefono=ficha.contacto_secundario_telefono,
            
            # Información médica adicional
            seguro_medico=ficha.seguro_medico,
            hospital_preferido=ficha.hospital_preferido,
            medico_tratante=ficha.medico_tratante,
            
            # Instrucciones
            instrucciones_emergencia=ficha.instrucciones_emergencia,
            crisis_comunes=ficha.crisis_comunes,
            como_calmar=ficha.como_calmar
        )
    
    def _enriquecer_ficha(self, ficha: FichaEmergencia) -> FichaEmergenciaResponse:
        """Enriquece la ficha con información del niño"""
        nino = ficha.nino
        nombre_completo = f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip()
        
        # Obtener foto si existe
        foto_url = None
        if hasattr(nino, 'archivos') and nino.archivos:
            foto_url = nino.archivos.foto_url
        
        return FichaEmergenciaResponse(
            id=ficha.id,
            nino_id=ficha.nino_id,
            tipo_sangre=ficha.tipo_sangre,
            alergias=ficha.alergias,
            condiciones_medicas=ficha.condiciones_medicas,
            medicamentos_actuales=ficha.medicamentos_actuales,
            diagnostico_principal=ficha.diagnostico_principal,
            diagnostico_detallado=ficha.diagnostico_detallado,
            contacto_principal_nombre=ficha.contacto_principal_nombre,
            contacto_principal_relacion=ficha.contacto_principal_relacion,
            contacto_principal_telefono=ficha.contacto_principal_telefono,
            contacto_principal_telefono_alt=ficha.contacto_principal_telefono_alt,
            contacto_secundario_nombre=ficha.contacto_secundario_nombre,
            contacto_secundario_relacion=ficha.contacto_secundario_relacion,
            contacto_secundario_telefono=ficha.contacto_secundario_telefono,
            seguro_medico=ficha.seguro_medico,
            numero_seguro=ficha.numero_seguro,
            hospital_preferido=ficha.hospital_preferido,
            medico_tratante=ficha.medico_tratante,
            telefono_medico=ficha.telefono_medico,
            instrucciones_emergencia=ficha.instrucciones_emergencia,
            restricciones_alimenticias=ficha.restricciones_alimenticias,
            crisis_comunes=ficha.crisis_comunes,
            como_calmar=ficha.como_calmar,
            trigger_points=ficha.trigger_points,
            activa=ficha.activa,
            fecha_creacion=ficha.fecha_creacion,
            fecha_actualizacion=ficha.fecha_actualizacion,
            nino_nombre_completo=nombre_completo,
            nino_foto_url=foto_url,
            nino_edad=self.calcular_edad(nino.fecha_nacimiento),
            nino_estado=nino.estado
        )

# app/services/recomendacion_service.py
"""
Servicio de recomendación basado en contenido
Integra similitud vectorial con TOPSIS y Gemini
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
import numpy as np

from app.models.recomendacion import (
    PerfilNinoVectorizado,
    PerfilActividadVectorizada,
    HistorialProgreso,
    RecomendacionActividad,
    AsignacionTerapeutaTOPSIS
)
from app.models.nino import Nino, NinoDiagnostico
from app.models.actividad import Actividad
from app.models.personal import Personal
from app.services.gemini_service import gemini_service
from app.services import topsis_service


class RecomendacionService:
    """
    Servicio principal de recomendaciones
    Combina: Contenido + TOPSIS + Gemini
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.gemini = gemini_service
    
    def crear_perfil_nino(self, nino_id: int) -> PerfilNinoVectorizado:
        """
        Crea o actualiza el perfil vectorizado de un niño
        """
        # Obtener datos del niño
        nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
        if not nino:
            raise ValueError(f"Niño {nino_id} no encontrado")
        
        # Calcular edad
        from datetime import date
        hoy = date.today()
        edad = hoy.year - nino.fecha_nacimiento.year
        
        # Obtener diagnóstico
        diagnostico = self.db.query(NinoDiagnostico).filter(
            NinoDiagnostico.nino_id == nino_id
        ).first()
        
        # Preparar datos para embedding
        datos_nino = {
            'nombre': f"{nino.nombre} {nino.apellido_paterno}",
            'edad': edad,
            'diagnosticos': diagnostico.tipo_autismo.split(',') if diagnostico and diagnostico.tipo_autismo else [],
            'dificultades': diagnostico.sensibilidades.split(',') if diagnostico and diagnostico.sensibilidades else [],
            'fortalezas': [],  # Extraer de notas si están disponibles
            'notas_clinicas': diagnostico.notas if diagnostico else '',
            'sensibilidades': [],
            'areas_prioritarias': []
        }
        
        # Generar embedding con Gemini
        embedding, texto_perfil = self.gemini.generar_embedding_perfil_nino(datos_nino)
        
        # Verificar si ya existe perfil
        perfil_existente = self.db.query(PerfilNinoVectorizado).filter(
            PerfilNinoVectorizado.nino_id == nino_id
        ).first()
        
        if perfil_existente:
            # Actualizar
            perfil_existente.embedding = embedding
            perfil_existente.edad = edad
            perfil_existente.diagnosticos = datos_nino['diagnosticos']
            perfil_existente.dificultades = datos_nino['dificultades']
            perfil_existente.fortalezas = datos_nino['fortalezas']
            perfil_existente.texto_perfil = texto_perfil
            perfil_existente.fecha_actualizacion = datetime.utcnow()
            perfil = perfil_existente
        else:
            # Crear nuevo
            perfil = PerfilNinoVectorizado(
                nino_id=nino_id,
                embedding=embedding,
                edad=edad,
                diagnosticos=datos_nino['diagnosticos'],
                dificultades=datos_nino['dificultades'],
                fortalezas=datos_nino['fortalezas'],
                texto_perfil=texto_perfil
            )
            self.db.add(perfil)
        
        self.db.commit()
        self.db.refresh(perfil)
        return perfil
    
    def crear_perfil_actividad(self, actividad_id: int) -> PerfilActividadVectorizada:
        """
        Crea o actualiza el perfil vectorizado de una actividad
        """
        actividad = self.db.query(Actividad).filter(Actividad.id == actividad_id).first()
        if not actividad:
            raise ValueError(f"Actividad {actividad_id} no encontrada")
        
        # Preparar datos
        datos_actividad = {
            'nombre': actividad.nombre,
            'descripcion': actividad.descripcion or '',
            'objetivo': actividad.objetivo or '',
            'area_desarrollo': actividad.area_desarrollo or '',
            'tags': actividad.tags or [],
            'dificultad': actividad.dificultad or 1,
            'materiales': actividad.materiales or ''
        }
        
        # Generar embedding
        embedding, texto_descripcion = self.gemini.generar_embedding_actividad(datos_actividad)
        
        # Verificar si existe
        perfil_existente = self.db.query(PerfilActividadVectorizada).filter(
            PerfilActividadVectorizada.actividad_id == actividad_id
        ).first()
        
        if perfil_existente:
            perfil_existente.embedding = embedding
            perfil_existente.areas_desarrollo = [actividad.area_desarrollo] if actividad.area_desarrollo else []
            perfil_existente.tags = actividad.tags or []
            perfil_existente.nivel_dificultad = actividad.dificultad or 1
            perfil_existente.texto_descripcion = texto_descripcion
            perfil_existente.fecha_actualizacion = datetime.utcnow()
            perfil = perfil_existente
        else:
            perfil = PerfilActividadVectorizada(
                actividad_id=actividad_id,
                embedding=embedding,
                areas_desarrollo=[actividad.area_desarrollo] if actividad.area_desarrollo else [],
                tags=actividad.tags or [],
                nivel_dificultad=actividad.dificultad or 1,
                texto_descripcion=texto_descripcion
            )
            self.db.add(perfil)
        
        self.db.commit()
        self.db.refresh(perfil)
        return perfil
    
    def recomendar_actividades(
        self,
        nino_id: int,
        top_n: int = 5,
        incluir_explicacion: bool = True
    ) -> Dict:
        """
        Recomienda actividades para un niño usando similitud de contenido
        
        Args:
            nino_id: ID del niño
            top_n: Número de actividades a recomendar
            incluir_explicacion: Si se debe generar explicación con Gemini
            
        Returns:
            Diccionario con actividades recomendadas y explicación
        """
        # Obtener o crear perfil del niño
        perfil_nino = self.db.query(PerfilNinoVectorizado).filter(
            PerfilNinoVectorizado.nino_id == nino_id
        ).first()
        
        if not perfil_nino:
            perfil_nino = self.crear_perfil_nino(nino_id)
        
        # Obtener todas las actividades vectorizadas activas
        actividades_vectorizadas = self.db.query(
            PerfilActividadVectorizada
        ).join(
            Actividad, PerfilActividadVectorizada.actividad_id == Actividad.id
        ).filter(
            Actividad.activo == 1
        ).all()
        
        # Si no hay actividades vectorizadas, vectorizar todas
        if not actividades_vectorizadas:
            actividades = self.db.query(Actividad).filter(Actividad.activo == 1).all()
            for act in actividades:
                self.crear_perfil_actividad(act.id)
            # Volver a consultar
            actividades_vectorizadas = self.db.query(PerfilActividadVectorizada).all()
        
        # Calcular similitud con cada actividad
        recomendaciones = []
        embedding_nino = perfil_nino.embedding
        
        for act_vec in actividades_vectorizadas:
            similitud = self.gemini.calcular_similitud_coseno(
                embedding_nino,
                act_vec.embedding
            )
            
            # Obtener datos de la actividad
            actividad = self.db.query(Actividad).filter(
                Actividad.id == act_vec.actividad_id
            ).first()
            
            if actividad:
                recomendaciones.append({
                    'actividad_id': actividad.id,
                    'nombre': actividad.nombre,
                    'descripcion': actividad.descripcion,
                    'objetivo': actividad.objetivo,
                    'area_desarrollo': actividad.area_desarrollo,
                    'dificultad': actividad.dificultad,
                    'score': similitud,
                    'tags': actividad.tags or []
                })
        
        # Ordenar por similitud descendente
        recomendaciones.sort(key=lambda x: x['score'], reverse=True)
        top_recomendaciones = recomendaciones[:top_n]
        
        # Generar explicación con Gemini si se solicita
        explicacion = None
        if incluir_explicacion and top_recomendaciones:
            nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
            nombre_nino = f"{nino.nombre} {nino.apellido_paterno}" if nino else "el niño"
            
            explicacion = self.gemini.explicar_recomendacion_actividades(
                nombre_nino=nombre_nino,
                perfil_nino=perfil_nino.texto_perfil,
                actividades_recomendadas=top_recomendaciones
            )
        
        # Guardar recomendación en BD
        recomendacion_registro = RecomendacionActividad(
            nino_id=nino_id,
            actividades_recomendadas=top_recomendaciones,
            explicacion_humana=explicacion,
            metodo='contenido'
        )
        self.db.add(recomendacion_registro)
        self.db.commit()
        
        return {
            'nino_id': nino_id,
            'recomendaciones': top_recomendaciones,
            'explicacion': explicacion,
            'fecha_generacion': datetime.utcnow().isoformat()
        }
    
    def seleccionar_terapeuta_optimo(
        self,
        nino_id: int,
        terapia_tipo: str,
        criterios_pesos: Optional[Dict[str, float]] = None
    ) -> Dict:
        """
        Selecciona el terapeuta óptimo usando TOPSIS
        
        Args:
            nino_id: ID del niño
            terapia_tipo: Tipo de terapia ('lenguaje', 'conductual', etc.)
            criterios_pesos: Pesos para cada criterio (opcional)
            
        Returns:
            Diccionario con terapeuta seleccionado y ranking
        """
        # Obtener terapeutas disponibles para ese tipo de terapia
        terapeutas = self.db.query(Personal).filter(
            Personal.especialidad_principal.contains(terapia_tipo)
        ).all()
        
        if not terapeutas:
            raise ValueError(f"No hay terapeutas disponibles para {terapia_tipo}")
        
        # Preparar matriz de decisión para TOPSIS
        alternativas = []
        for terapeuta in terapeutas:
            alternativas.append({
                'id': terapeuta.id,
                'nombre': f"{terapeuta.nombres} {terapeuta.apellido_paterno}",
                'especialidad': terapeuta.especialidad_principal,
                'experiencia_anos': terapeuta.experiencia or 1
            })
        
        # Usar TOPSIS para calcular ranking
        resultado_topsis = topsis_service.calcular_ranking_terapeutas(
            terapeutas=alternativas,
            criterios_pesos=criterios_pesos
        )
        
        # Obtener el mejor terapeuta
        mejor_terapeuta = resultado_topsis['ranking'][0]
        
        # Generar explicación con Gemini
        nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
        nombre_nino = f"{nino.nombre} {nino.apellido_paterno}" if nino else "el niño"
        
        explicacion = self.gemini.explicar_seleccion_terapeuta(
            nombre_nino=nombre_nino,
            terapia_tipo=terapia_tipo,
            terapeuta_seleccionado=mejor_terapeuta,
            criterios_topsis=resultado_topsis['criterios_usados'],
            ranking_top3=resultado_topsis['ranking'][:3]
        )
        
        # Guardar en BD
        asignacion = AsignacionTerapeutaTOPSIS(
            nino_id=nino_id,
            terapia_tipo=terapia_tipo,
            ranking_terapeutas=resultado_topsis['ranking'],
            terapeuta_seleccionado_id=mejor_terapeuta['id'],
            explicacion_seleccion=explicacion,
            criterios_usados=resultado_topsis['criterios_usados']
        )
        self.db.add(asignacion)
        self.db.commit()
        
        return {
            'nino_id': nino_id,
            'terapia_tipo': terapia_tipo,
            'terapeuta_seleccionado': mejor_terapeuta,
            'ranking_completo': resultado_topsis['ranking'],
            'explicacion': explicacion,
            'criterios_usados': resultado_topsis['criterios_usados']
        }
    
    def flujo_completo_recomendacion(self, nino_id: int, terapia_tipo: str) -> Dict:
        """
        Flujo completo: Actividades + Terapeuta + Explicaciones
        
        Este es el flujo ideal mencionado en el documento:
        1. Recomendación basada en contenido → actividades
        2. TOPSIS → mejor terapeuta
        3. Gemini → explicaciones
        """
        # Paso 1: Recomendar actividades
        recomendacion_actividades = self.recomendar_actividades(
            nino_id=nino_id,
            top_n=5,
            incluir_explicacion=True
        )
        
        # Paso 2: Seleccionar terapeuta óptimo
        seleccion_terapeuta = self.seleccionar_terapeuta_optimo(
            nino_id=nino_id,
            terapia_tipo=terapia_tipo
        )
        
        # Paso 3: Generar resumen completo con Gemini
        nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
        
        return {
            'nino': {
                'id': nino.id,
                'nombre': f"{nino.nombre} {nino.apellido_paterno}"
            },
            'actividades_recomendadas': recomendacion_actividades,
            'terapeuta_asignado': seleccion_terapeuta,
            'fecha_generacion': datetime.utcnow().isoformat()
        }


def get_recomendacion_service(db: Session) -> RecomendacionService:
    """Factory para crear instancia del servicio"""
    return RecomendacionService(db)

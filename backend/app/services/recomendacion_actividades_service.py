# backend/app/services/recomendacion_actividades_service.py
"""
Servicio mejorado de recomendación de actividades basado en contenido
Utiliza similitud coseno entre embeddings del niño y actividades
"""
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
import numpy as np

from app.models.recomendacion import (
    PerfilNinoVectorizado,
    PerfilActividadVectorizada,
    HistorialProgreso,
    RecomendacionActividad
)
from app.models.nino import Nino
from app.models.actividad import Actividad
from app.schemas.recomendacion_actividades import (
    ActividadRecomendada,
    RecomendacionResponse,
    PerfilNinoResponse
)


class RecomendacionActividadesService:
    """
    Servicio de recomendación de actividades basado en contenido
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calcular_similitud_coseno(
        self,
        vector_a: List[float],
        vector_b: List[float]
    ) -> float:
        """
        Calcula la similitud coseno entre dos vectores
        Retorna valor entre 0 y 1 (1 = máxima similitud)
        """
        try:
            arr_a = np.array(vector_a)
            arr_b = np.array(vector_b)
            
            # Calcular producto punto
            dot_product = np.dot(arr_a, arr_b)
            
            # Calcular magnitudes
            norm_a = np.linalg.norm(arr_a)
            norm_b = np.linalg.norm(arr_b)
            
            # Evitar división por cero
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            # Similitud coseno
            similitud = dot_product / (norm_a * norm_b)
            
            # Normalizar a rango 0-1
            similitud_normalizada = (similitud + 1) / 2
            
            return float(similitud_normalizada)
            
        except Exception as e:
            print(f"Error calculando similitud: {e}")
            return 0.0
    
    def obtener_perfil_nino(self, nino_id: int) -> Optional[PerfilNinoVectorizado]:
        """Obtiene el perfil vectorizado de un niño"""
        return self.db.query(PerfilNinoVectorizado).filter(
            PerfilNinoVectorizado.nino_id == nino_id
        ).first()
    
    def obtener_actividades_vectorizadas(
        self,
        filtrar_por_area: Optional[str] = None,
        nivel_dificultad_max: Optional[int] = None
    ) -> List[PerfilActividadVectorizada]:
        """Obtiene actividades vectorizadas con filtros opcionales"""
        query = self.db.query(PerfilActividadVectorizada).join(
            Actividad,
            Actividad.id == PerfilActividadVectorizada.actividad_id
        ).filter(Actividad.activo == 1)
        
        if filtrar_por_area:
            query = query.filter(
                Actividad.area_desarrollo == filtrar_por_area
            )
        
        if nivel_dificultad_max:
            query = query.filter(
                Actividad.dificultad <= nivel_dificultad_max
            )
        
        return query.all()
    
    def generar_recomendaciones(
        self,
        nino_id: int,
        top_n: int = 10,
        filtrar_por_area: Optional[str] = None,
        nivel_dificultad_max: Optional[int] = None
    ) -> RecomendacionResponse:
        """
        Genera recomendaciones de actividades para un niño
        basadas en similitud de embeddings
        """
        # 1. Obtener perfil del niño
        perfil_nino = self.obtener_perfil_nino(nino_id)
        if not perfil_nino:
            raise ValueError(
                f"El niño {nino_id} no tiene perfil vectorizado. "
                "Primero debe generarse con POST /api/v1/recomendaciones/perfil"
            )
        
        # 2. Obtener información del niño
        nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
        if not nino:
            raise ValueError(f"Niño {nino_id} no encontrado")
        
        nombre_nino = f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip()
        
        # 3. Obtener actividades vectorizadas
        actividades_vectorizadas = self.obtener_actividades_vectorizadas(
            filtrar_por_area=filtrar_por_area,
            nivel_dificultad_max=nivel_dificultad_max
        )
        
        if not actividades_vectorizadas:
            return RecomendacionResponse(
                nino_id=nino_id,
                nombre_nino=nombre_nino,
                total_recomendaciones=0,
                perfil_actualizado=False,
                fecha_generacion=datetime.utcnow(),
                recomendaciones=[]
            )
        
        # 4. Calcular similitudes
        embedding_nino = perfil_nino.embedding
        scores_actividades = []
        
        for act_vec in actividades_vectorizadas:
            similitud = self.calcular_similitud_coseno(
                embedding_nino,
                act_vec.embedding
            )
            
            # Obtener detalles de la actividad
            actividad = self.db.query(Actividad).filter(
                Actividad.id == act_vec.actividad_id
            ).first()
            
            if actividad:
                scores_actividades.append({
                    'actividad': actividad,
                    'score': similitud,
                    'tags': act_vec.tags or [],
                    'areas': act_vec.areas_desarrollo or []
                })
        
        # 5. Ordenar por score descendente
        scores_actividades.sort(key=lambda x: x['score'], reverse=True)
        
        # 6. Tomar top N
        top_actividades = scores_actividades[:top_n]
        
        # 7. Crear objetos de respuesta
        recomendaciones = []
        for i, item in enumerate(top_actividades, start=1):
            actividad = item['actividad']
            
            # Generar razón de recomendación
            razon = self._generar_razon_recomendacion(
                actividad,
                item['score'],
                perfil_nino,
                item['areas']
            )
            
            recomendacion = ActividadRecomendada(
                actividad_id=actividad.id,
                nombre=actividad.nombre,
                descripcion=actividad.descripcion,
                area_desarrollo=actividad.area_desarrollo,
                dificultad=actividad.dificultad,
                duracion_minutos=actividad.duracion_minutos,
                score_similitud=item['score'],
                ranking=i,
                razon_recomendacion=razon,
                tags=item['tags']
            )
            recomendaciones.append(recomendacion)
        
        # 8. Guardar recomendaciones en BD para tracking
        self._guardar_recomendaciones(nino_id, recomendaciones)
        
        return RecomendacionResponse(
            nino_id=nino_id,
            nombre_nino=nombre_nino,
            total_recomendaciones=len(recomendaciones),
            perfil_actualizado=False,
            fecha_generacion=datetime.utcnow(),
            recomendaciones=recomendaciones
        )
    
    def _generar_razon_recomendacion(
        self,
        actividad: Actividad,
        score: float,
        perfil_nino: PerfilNinoVectorizado,
        areas: List[str]
    ) -> str:
        """Genera explicación de por qué se recomienda la actividad"""
        razones = []
        
        # Score alto
        if score >= 0.8:
            razones.append(f"Coincidencia excelente ({score:.1%}) con el perfil")
        elif score >= 0.6:
            razones.append(f"Buena coincidencia ({score:.1%}) con necesidades")
        else:
            razones.append(f"Coincidencia moderada ({score:.1%})")
        
        # Áreas de desarrollo
        if areas:
            razones.append(f"Trabaja: {', '.join(areas[:2])}")
        
        # Dificultad
        niveles_dif = {1: "baja", 2: "media", 3: "alta"}
        razones.append(f"Dificultad {niveles_dif.get(actividad.dificultad, 'media')}")
        
        # Diagnósticos del niño
        if perfil_nino.diagnosticos:
            razones.append(f"Adecuada para perfil TEA")
        
        return " · ".join(razones)
    
    def _guardar_recomendaciones(
        self,
        nino_id: int,
        recomendaciones: List[ActividadRecomendada]
    ):
        """Guarda las recomendaciones en BD para análisis posterior"""
        try:
            # Convertir recomendaciones a formato JSON
            actividades_json = []
            for rec in recomendaciones:
                actividades_json.append({
                    "actividad_id": rec.actividad_id,
                    "score": float(rec.score_similitud),
                    "ranking": rec.ranking,
                    "razon": rec.razon_recomendacion
                })
            
            # Crear registro con todas las recomendaciones
            nueva_rec = RecomendacionActividad(
                nino_id=nino_id,
                actividades_recomendadas=actividades_json,
                metodo="contenido",
                fecha_generacion=datetime.utcnow(),
                aplicada=0
            )
            self.db.add(nueva_rec)
            self.db.commit()
        except Exception as e:
            print(f"Error guardando recomendaciones: {e}")
            self.db.rollback()
    
    def obtener_perfil_nino_detalle(self, nino_id: int) -> PerfilNinoResponse:
        """Obtiene el perfil detallado de un niño"""
        try:
            perfil = self.obtener_perfil_nino(nino_id)
            nino = self.db.query(Nino).filter(Nino.id == nino_id).first()
            
            if not nino:
                raise ValueError(f"Niño {nino_id} no encontrado")
            
            nombre_nino = f"{nino.nombre} {nino.apellido_paterno} {nino.apellido_materno or ''}".strip()
            
            if not perfil:
                return PerfilNinoResponse(
                    nino_id=nino_id,
                    nombre_nino=nombre_nino,
                    tiene_embedding=False,
                    diagnosticos=[],
                    dificultades=[],
                    fortalezas=[],
                    areas_prioritarias=[]
                )
            
            # Asegurar que los campos JSON son listas
            diagnosticos = perfil.diagnosticos if isinstance(perfil.diagnosticos, list) else []
            dificultades = perfil.dificultades if isinstance(perfil.dificultades, list) else []
            fortalezas = perfil.fortalezas if isinstance(perfil.fortalezas, list) else []
            
            return PerfilNinoResponse(
                nino_id=nino_id,
                nombre_nino=nombre_nino,
                edad=perfil.edad,
                diagnosticos=diagnosticos,
                dificultades=dificultades,
                fortalezas=fortalezas,
                areas_prioritarias=[],
                fecha_ultima_actualizacion=perfil.fecha_actualizacion,
                tiene_embedding=True
            )
        except Exception as e:
            import traceback
            print(f"❌ Error en obtener_perfil_nino_detalle: {traceback.format_exc()}")
            raise
    
    def registrar_progreso(
        self,
        nino_id: int,
        actividad_id: int,
        terapeuta_id: int,
        calificacion: float,
        notas_progreso: Optional[str] = None,
        dificultad_encontrada: Optional[int] = None
    ) -> HistorialProgreso:
        """Registra el progreso de un niño en una actividad"""
        progreso = HistorialProgreso(
            nino_id=nino_id,
            actividad_id=actividad_id,
            terapeuta_id=terapeuta_id,
            calificacion=calificacion,
            notas_progreso=notas_progreso,
            dificultad_encontrada=dificultad_encontrada,
            fecha_registro=datetime.utcnow()
        )
        
        self.db.add(progreso)
        self.db.commit()
        self.db.refresh(progreso)
        
        return progreso

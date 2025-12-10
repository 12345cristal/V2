# backend/app/services/topsis_terapeutas_service.py
"""
Servicio para evaluación de terapeutas usando TOPSIS
(Technique for Order Preference by Similarity to Ideal Solution)

Implementa Clean Architecture con separación de responsabilidades:
- Obtención de datos
- Cálculo de métricas
- Aplicación de TOPSIS
- Generación de ranking
"""
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Tuple, Dict, Optional
from datetime import datetime, timedelta

from app.models.personal import Personal, EstadoLaboral
from app.models.cita import Cita
from app.models.terapia import Terapia, TerapiaPersonal, Sesion
from app.schemas.topsis_terapeutas import (
    TopsisEvaluacionRequest,
    TerapeutaRanking,
    MetricasTerapeuta,
    TopsisResultado,
    PesosCriterios
)


class TopsisCalculator:
    """
    Clase para cálculos TOPSIS puros (sin dependencias de BD)
    Implementa el algoritmo TOPSIS estándar
    """
    
    @staticmethod
    def normalizar_matriz(matriz: np.ndarray) -> np.ndarray:
        """
        Normalización vectorial de la matriz de decisión
        Cada elemento se divide por la raíz cuadrada de la suma de cuadrados de su columna
        """
        denominador = np.sqrt((matriz ** 2).sum(axis=0))
        # Evitar división por cero
        denominador[denominador == 0] = 1
        return matriz / denominador
    
    @staticmethod
    def aplicar_pesos(matriz_normalizada: np.ndarray, pesos: np.ndarray) -> np.ndarray:
        """Multiplica cada columna por su peso correspondiente"""
        return matriz_normalizada * pesos
    
    @staticmethod
    def calcular_ideales(
        matriz_ponderada: np.ndarray,
        tipos_criterios: List[str]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula la solución ideal positiva (A+) y negativa (A-)
        
        Args:
            matriz_ponderada: Matriz con pesos aplicados
            tipos_criterios: Lista con 'beneficio' o 'costo' para cada criterio
            
        Returns:
            Tupla (ideal_positivo, ideal_negativo)
        """
        ideal_positivo = np.zeros(matriz_ponderada.shape[1])
        ideal_negativo = np.zeros(matriz_ponderada.shape[1])
        
        for i, tipo in enumerate(tipos_criterios):
            if tipo == 'beneficio':
                # Para criterios de beneficio: max es mejor
                ideal_positivo[i] = matriz_ponderada[:, i].max()
                ideal_negativo[i] = matriz_ponderada[:, i].min()
            else:  # tipo == 'costo'
                # Para criterios de costo: min es mejor
                ideal_positivo[i] = matriz_ponderada[:, i].min()
                ideal_negativo[i] = matriz_ponderada[:, i].max()
        
        return ideal_positivo, ideal_negativo
    
    @staticmethod
    def calcular_distancias(
        matriz_ponderada: np.ndarray,
        ideal_positivo: np.ndarray,
        ideal_negativo: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula distancias euclidianas a las soluciones ideales
        
        Returns:
            Tupla (distancias_positivas, distancias_negativas)
        """
        dist_positivas = np.sqrt(
            ((matriz_ponderada - ideal_positivo) ** 2).sum(axis=1)
        )
        dist_negativas = np.sqrt(
            ((matriz_ponderada - ideal_negativo) ** 2).sum(axis=1)
        )
        return dist_positivas, dist_negativas
    
    @staticmethod
    def calcular_scores(
        dist_positivas: np.ndarray,
        dist_negativas: np.ndarray
    ) -> np.ndarray:
        """
        Calcula el coeficiente de proximidad relativa (score TOPSIS)
        Score = D- / (D+ + D-)
        Valores cercanos a 1 indican mejor alternativa
        """
        denominador = dist_positivas + dist_negativas
        # Evitar división por cero (aunque no debería ocurrir)
        denominador[denominador == 0] = 1e-10
        return dist_negativas / denominador


class MetricasService:
    """Servicio para calcular métricas de terapeutas desde la base de datos"""
    
    @staticmethod
    def obtener_carga_laboral(db: Session, terapeuta_id: int) -> int:
        """
        Obtiene las sesiones semanales del terapeuta desde la tabla personal.
        Esto representa su carga laboral actual.
        Retorna el número de sesiones por semana que tiene asignadas.
        """
        terapeuta = db.query(Personal).filter(Personal.id == terapeuta_id).first()
        if terapeuta and terapeuta.sesiones_semana:
            return int(terapeuta.sesiones_semana)
        return 0
    
    @staticmethod
    def obtener_sesiones_completadas(db: Session, terapeuta_id: int) -> int:
        """
        Obtiene el total de pacientes del terapeuta desde la tabla personal.
        Representa su experiencia práctica y volumen de trabajo histórico.
        """
        terapeuta = db.query(Personal).filter(Personal.id == terapeuta_id).first()
        if terapeuta and terapeuta.total_pacientes:
            return int(terapeuta.total_pacientes)
        return 0
    
    @staticmethod
    def obtener_rating_promedio(db: Session, terapeuta_id: int) -> float:
        """
        Obtiene el rating del terapeuta directamente desde la tabla personal.
        Este rating es la calificación promedio histórica del terapeuta.
        Retorna un valor entre 0 y 5.0
        """
        terapeuta = db.query(Personal).filter(Personal.id == terapeuta_id).first()
        if terapeuta and terapeuta.rating is not None:
            return float(terapeuta.rating)
        return 3.0  # Valor neutral si no tiene rating
    
    @staticmethod
    def verifica_especialidad_match(
        db: Session,
        terapeuta_id: int,
        terapia_id: Optional[int]
    ) -> bool:
        """
        Verifica si la especialidad del terapeuta coincide con la terapia solicitada.
        Busca por nombre de la terapia en la especialidad_principal y especialidades.
        Si no se especifica terapia_id, retorna True.
        """
        if terapia_id is None:
            return True
        
        # Obtener el terapeuta
        terapeuta = db.query(Personal).filter(Personal.id == terapeuta_id).first()
        if not terapeuta:
            return False
        
        # Obtener la terapia
        terapia = db.query(Terapia).filter(Terapia.id == terapia_id).first()
        if not terapia:
            return False
        
        # Normalizar nombres para comparación (sin acentos, minúsculas)
        terapia_nombre = terapia.nombre.lower().strip()
        especialidad_principal = (terapeuta.especialidad_principal or '').lower().strip()
        especialidades = (terapeuta.especialidades or '').lower().strip()
        
        # Mapeo de terapias a palabras clave de especialidades
        mapeo_especialidades = {
            'terapia de lenguaje': ['lenguaje', 'comunicación', 'habla'],
            'lenguaje': ['lenguaje', 'comunicación', 'habla'],
            'ocupacional': ['ocupacional', 'ocupación'],
            'psicología': ['psicología', 'psicolog', 'psico'],
            'conductual': ['conductual', 'aba', 'conducta'],
            'aba': ['aba', 'conductual', 'conducta'],
            'música': ['música', 'musicoterapia', 'musico'],
            'física': ['física', 'fisico', 'motor'],
            'sensorial': ['sensorial', 'integración'],
            'pedagog': ['pedagog', 'educación']
        }
        
        # Buscar coincidencias
        for terapia_key, keywords in mapeo_especialidades.items():
            if terapia_key in terapia_nombre:
                for keyword in keywords:
                    if keyword in especialidad_principal or keyword in especialidades:
                        return True
        
        # Si no hay match en el mapeo, buscar coincidencia directa
        palabras_terapia = terapia_nombre.split()
        for palabra in palabras_terapia:
            if len(palabra) > 4:  # Solo palabras significativas
                if palabra in especialidad_principal or palabra in especialidades:
                    return True
        
        return False


class TopsisEvaluacionService:
    """
    Servicio principal para evaluar terapeutas con TOPSIS
    Coordina la obtención de datos, cálculos y generación de resultados
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.calculator = TopsisCalculator()
        self.metricas_service = MetricasService()
    
    def obtener_terapeutas_activos(
        self,
        incluir_inactivos: bool = False
    ) -> List[Personal]:
        """Obtiene lista de terapeutas del sistema"""
        query = self.db.query(Personal)
        
        if not incluir_inactivos:
            query = query.filter(Personal.estado_laboral == EstadoLaboral.ACTIVO)
        
        return query.all()
    
    def calcular_metricas_terapeuta(
        self,
        terapeuta: Personal,
        terapia_id: Optional[int]
    ) -> MetricasTerapeuta:
        """Calcula todas las métricas para un terapeuta"""
        return MetricasTerapeuta(
            carga_laboral=self.metricas_service.obtener_carga_laboral(
                self.db, terapeuta.id
            ),
            sesiones_completadas=self.metricas_service.obtener_sesiones_completadas(
                self.db, terapeuta.id
            ),
            rating=self.metricas_service.obtener_rating_promedio(
                self.db, terapeuta.id
            ),
            especialidad_match=self.metricas_service.verifica_especialidad_match(
                self.db, terapeuta.id, terapia_id
            )
        )
    
    def construir_matriz_decision(
        self,
        terapeutas: List[Personal],
        metricas_dict: Dict[int, MetricasTerapeuta]
    ) -> np.ndarray:
        """
        Construye la matriz de decisión con las métricas de cada terapeuta
        
        Columnas: [carga_laboral, sesiones_completadas, rating, especialidad_match]
        Filas: Un terapeuta por fila
        """
        matriz = []
        for terapeuta in terapeutas:
            metricas = metricas_dict[terapeuta.id]
            fila = [
                float(metricas.carga_laboral),
                float(metricas.sesiones_completadas),
                float(metricas.rating),
                1.0 if metricas.especialidad_match else 0.0  # Convertir bool a float
            ]
            matriz.append(fila)
        
        return np.array(matriz, dtype=float)
    
    def evaluar_terapeutas(
        self,
        request: TopsisEvaluacionRequest
    ) -> TopsisResultado:
        """
        Método principal: Evalúa terapeutas usando TOPSIS
        
        Flujo:
        1. Obtener terapeutas
        2. Calcular métricas para cada uno
        3. Construir matriz de decisión
        4. Aplicar TOPSIS
        5. Generar ranking ordenado
        """
        # 1. Obtener terapeutas
        terapeutas = self.obtener_terapeutas_activos(request.incluir_inactivos)
        
        if not terapeutas:
            return TopsisResultado(
                total_evaluados=0,
                terapia_solicitada=None,
                pesos_aplicados=request.pesos,
                ranking=[]
            )
        
        # 2. Calcular métricas para cada terapeuta
        metricas_dict = {}
        for terapeuta in terapeutas:
            metricas_dict[terapeuta.id] = self.calcular_metricas_terapeuta(
                terapeuta, request.terapia_id
            )
        
        # 3. Construir matriz de decisión
        matriz = self.construir_matriz_decision(terapeutas, metricas_dict)
        
        # 4. Aplicar TOPSIS
        # Definir pesos y tipos de criterios
        pesos = np.array([
            request.pesos.carga_laboral,
            request.pesos.sesiones_completadas,
            request.pesos.rating,
            request.pesos.especialidad
        ])
        
        # Tipos: carga_laboral es 'costo' (menos es mejor), resto son 'beneficio'
        tipos = ['costo', 'beneficio', 'beneficio', 'beneficio']
        
        # Normalizar
        matriz_norm = self.calculator.normalizar_matriz(matriz)
        
        # Aplicar pesos
        matriz_pond = self.calculator.aplicar_pesos(matriz_norm, pesos)
        
        # Calcular ideales
        ideal_pos, ideal_neg = self.calculator.calcular_ideales(matriz_pond, tipos)
        
        # Calcular distancias
        dist_pos, dist_neg = self.calculator.calcular_distancias(
            matriz_pond, ideal_pos, ideal_neg
        )
        
        # Calcular scores
        scores = self.calculator.calcular_scores(dist_pos, dist_neg)
        
        # 5. Generar ranking
        # Crear lista temporal con scores para ordenar
        temp_ranking = []
        for i, terapeuta in enumerate(terapeutas):
            nombre_completo = f"{terapeuta.nombres} {terapeuta.apellido_paterno} {terapeuta.apellido_materno or ''}".strip()
            temp_ranking.append({
                'terapeuta_id': terapeuta.id,
                'nombre': nombre_completo,
                'especialidad_principal': terapeuta.especialidad_principal,
                'score': float(scores[i]),
                'metricas': metricas_dict[terapeuta.id]
            })
        
        # Ordenar por score descendente
        temp_ranking.sort(key=lambda x: x['score'], reverse=True)
        
        # Crear objetos TerapeutaRanking con ranking ya asignado
        ranking_list = []
        for i, item in enumerate(temp_ranking, start=1):
            ranking_list.append(
                TerapeutaRanking(
                    terapeuta_id=item['terapeuta_id'],
                    nombre=item['nombre'],
                    especialidad_principal=item['especialidad_principal'],
                    score=item['score'],
                    ranking=i,
                    metricas=item['metricas']
                )
            )
        
        # Obtener nombre de terapia si se especificó
        terapia_nombre = None
        if request.terapia_id:
            terapia = self.db.query(Terapia).filter(Terapia.id == request.terapia_id).first()
            if terapia:
                terapia_nombre = terapia.nombre
        
        return TopsisResultado(
            total_evaluados=len(terapeutas),
            terapia_solicitada=terapia_nombre,
            pesos_aplicados=request.pesos,
            ranking=ranking_list
        )

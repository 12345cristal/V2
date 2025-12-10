# app/services/topsis_service.py
"""
Servicio para cálculo de prioridad usando el método TOPSIS
(Technique for Order of Preference by Similarity to Ideal Solution)
"""
import numpy as np
from typing import List, Tuple, Dict
from sqlalchemy.orm import Session

from app.models.criterio_topsis import CriterioTopsis
from app.schemas.topsis import TopsisInput, TopsisResultado


def aplicar_topsis(
    matriz: List[List[float]], 
    pesos: List[float], 
    tipos: List[str]
) -> List[float]:
    """
    Aplica el método TOPSIS a una matriz de decisión
    
    Args:
        matriz: Matriz de decisión (filas=alternativas, columnas=criterios)
        pesos: Lista de pesos para cada criterio
        tipos: Lista de tipos para cada criterio ('beneficio' o 'costo')
    
    Returns:
        Lista de scores TOPSIS normalizados entre 0 y 1 para cada alternativa
    """
    # Convertir a numpy array
    matriz_np = np.array(matriz, dtype=float)
    pesos_np = np.array(pesos, dtype=float)
    
    # Paso 1: Normalizar la matriz (normalización vectorial)
    # Cada columna se divide por la raíz cuadrada de la suma de los cuadrados
    norm_matriz = matriz_np / np.sqrt((matriz_np ** 2).sum(axis=0))
    
    # Paso 2: Aplicar pesos
    matriz_ponderada = norm_matriz * pesos_np
    
    # Paso 3: Determinar ideal positivo y negativo
    ideal_positivo = np.zeros(len(tipos))
    ideal_negativo = np.zeros(len(tipos))
    
    for i, tipo in enumerate(tipos):
        if tipo == 'beneficio':
            ideal_positivo[i] = matriz_ponderada[:, i].max()
            ideal_negativo[i] = matriz_ponderada[:, i].min()
        else:  # tipo == 'costo'
            ideal_positivo[i] = matriz_ponderada[:, i].min()
            ideal_negativo[i] = matriz_ponderada[:, i].max()
    
    # Paso 4: Calcular distancias euclidianas
    distancias_positivo = np.sqrt(((matriz_ponderada - ideal_positivo) ** 2).sum(axis=1))
    distancias_negativo = np.sqrt(((matriz_ponderada - ideal_negativo) ** 2).sum(axis=1))
    
    # Paso 5: Calcular scores (similitud con ideal positivo)
    # Score = D- / (D+ + D-)
    scores = distancias_negativo / (distancias_positivo + distancias_negativo + 1e-10)
    
    return scores.tolist()


def calcular_prioridad_ninos(
    db: Session, 
    input_data: TopsisInput
) -> List[TopsisResultado]:
    """
    Calcula la prioridad de niños usando TOPSIS con criterios de la BD
    
    Args:
        db: Sesión de base de datos
        input_data: Datos de entrada con IDs de niños y matriz de decisión
    
    Returns:
        Lista de TopsisResultado ordenada por score descendente
    """
    # Obtener criterios activos de la BD
    criterios = db.query(CriterioTopsis).filter(
        CriterioTopsis.activo == 1
    ).order_by(CriterioTopsis.id).all()
    
    if not criterios:
        raise ValueError("No hay criterios TOPSIS configurados en la base de datos")
    
    # Extraer pesos y tipos
    pesos = [float(c.peso) for c in criterios]
    tipos = [c.tipo for c in criterios]
    
    # Validar que la matriz tenga el número correcto de columnas
    num_criterios = len(criterios)
    for fila in input_data.matriz:
        if len(fila) != num_criterios:
            raise ValueError(
                f"La matriz debe tener {num_criterios} columnas (una por criterio). "
                f"Se encontraron {len(fila)} columnas."
            )
    
    # Validar que el número de filas coincida con el número de IDs
    if len(input_data.matriz) != len(input_data.ids):
        raise ValueError(
            f"El número de filas de la matriz ({len(input_data.matriz)}) "
            f"debe coincidir con el número de IDs ({len(input_data.ids)})"
        )
    
    # Aplicar TOPSIS
    scores = aplicar_topsis(input_data.matriz, pesos, tipos)
    
    # Crear resultados con ranking
    resultados = [
        {"nino_id": nino_id, "score": score}
        for nino_id, score in zip(input_data.ids, scores)
    ]
    
    # Ordenar por score descendente
    resultados.sort(key=lambda x: x["score"], reverse=True)
    
    # Asignar ranking
    resultados_finales = [
        TopsisResultado(
            nino_id=r["nino_id"],
            score=r["score"],
            ranking=idx + 1
        )
        for idx, r in enumerate(resultados)
    ]
    
    return resultados_finales


def get_criterios(db: Session, incluir_inactivos: bool = False) -> List[CriterioTopsis]:
    """Obtiene todos los criterios TOPSIS"""
    query = db.query(CriterioTopsis)
    if not incluir_inactivos:
        query = query.filter(CriterioTopsis.activo == 1)
    return query.order_by(CriterioTopsis.id).all()


def create_criterio(db: Session, criterio_data: dict) -> CriterioTopsis:
    """Crea un nuevo criterio TOPSIS"""
    criterio = CriterioTopsis(**criterio_data)
    db.add(criterio)
    db.commit()
    db.refresh(criterio)
    return criterio


def update_criterio(db: Session, criterio_id: int, criterio_data: dict) -> CriterioTopsis:
    """Actualiza un criterio TOPSIS existente"""
    criterio = db.query(CriterioTopsis).filter(CriterioTopsis.id == criterio_id).first()
    if not criterio:
        raise ValueError(f"Criterio con ID {criterio_id} no encontrado")
    
    for key, value in criterio_data.items():
        if value is not None:
            setattr(criterio, key, value)
    
    db.commit()
    db.refresh(criterio)
    return criterio


def delete_criterio(db: Session, criterio_id: int) -> bool:
    """Elimina un criterio TOPSIS"""
    criterio = db.query(CriterioTopsis).filter(CriterioTopsis.id == criterio_id).first()
    if not criterio:
        raise ValueError(f"Criterio con ID {criterio_id} no encontrado")
    
    db.delete(criterio)
    db.commit()
    return True


def calcular_ranking_terapeutas(
    terapeutas: List[Dict],
    criterios_pesos: Dict[str, float] = None
) -> Dict:
    """
    Calcula ranking de terapeutas usando TOPSIS
    Función auxiliar para integración con sistema de recomendaciones
    
    Args:
        terapeutas: Lista de diccionarios con datos de terapeutas
        criterios_pesos: Pesos personalizados (opcional)
        
    Returns:
        Diccionario con ranking y criterios usados
    """
    # Pesos por defecto
    if criterios_pesos is None:
        criterios_pesos = {
            'experiencia': 0.30,
            'disponibilidad': 0.25,
            'carga_trabajo': 0.20,
            'evaluacion': 0.15,
            'especializacion': 0.10
        }
    
    # Si hay menos de 2 terapeutas, no aplicar TOPSIS
    if len(terapeutas) < 2:
        return {
            'ranking': [{
                **terapeutas[0],
                'score': 1.0,
                'posicion': 1
            }] if terapeutas else [],
            'criterios_usados': criterios_pesos
        }
    
    # Construir matriz de decisión
    n_terapeutas = len(terapeutas)
    matriz = []
    
    for terapeuta in terapeutas:
        fila = [
            terapeuta.get('experiencia_anos', 1),
            terapeuta.get('disponibilidad', 5),
            max(0, 20 - terapeuta.get('carga_trabajo', 10)),  # Invertir carga
            terapeuta.get('evaluacion', 3.5),
            terapeuta.get('nivel_especializacion', 5)
        ]
        matriz.append(fila)
    
    # Preparar pesos y tipos
    pesos = [
        criterios_pesos['experiencia'],
        criterios_pesos['disponibilidad'],
        criterios_pesos['carga_trabajo'],
        criterios_pesos['evaluacion'],
        criterios_pesos['especializacion']
    ]
    
    tipos = ['beneficio', 'beneficio', 'beneficio', 'beneficio', 'beneficio']
    
    # Aplicar TOPSIS
    scores = aplicar_topsis(matriz, pesos, tipos)
    
    # Crear ranking
    ranking = []
    for i, terapeuta in enumerate(terapeutas):
        ranking.append({
            **terapeuta,
            'score': float(scores[i]),
            'posicion': 0
        })
    
    # Ordenar por score descendente
    ranking.sort(key=lambda x: x['score'], reverse=True)
    
    # Asignar posiciones
    for i, item in enumerate(ranking, 1):
        item['posicion'] = i
    
    return {
        'ranking': ranking,
        'criterios_usados': criterios_pesos
    }

"""
TOPSIS Service - Algoritmo de toma de decisiones multi-criterio
(Technique for Order of Preference by Similarity to Ideal Solution)
"""

from typing import List, Dict, Any, Literal
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.decision_log import DecisionLog


class TOPSISService:
    """
    Servicio para ejecutar el algoritmo TOPSIS
    
    El algoritmo TOPSIS evalúa alternativas basándose en múltiples criterios,
    calculando la distancia a la solución ideal positiva y negativa.
    """
    
    @staticmethod
    def ejecutar_topsis(
        criterios: List[Dict[str, Any]],
        alternativas: List[Dict[str, Any]],
        db: Session = None,
        usuario_id: int = None,
        contexto: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Ejecutar algoritmo TOPSIS
        
        Args:
            criterios: Lista de criterios con estructura:
                [
                    {
                        "nombre": "experiencia",
                        "peso": 0.4,
                        "tipo": "beneficio"  # o "costo"
                    },
                    ...
                ]
            alternativas: Lista de alternativas con estructura:
                [
                    {
                        "id": 1,
                        "nombre": "Alternativa A",
                        "valores": [8, 5, 7, 3]  # valores para cada criterio
                    },
                    ...
                ]
            db: Session de base de datos (opcional, para logging)
            usuario_id: ID del usuario que ejecuta (opcional)
            contexto: Descripción del contexto (opcional)
        
        Returns:
            Lista de alternativas ordenadas por score descendente con estructura:
                [
                    {
                        "id": 1,
                        "nombre": "Alternativa A",
                        "score": 0.85,
                        "ranking": 1
                    },
                    ...
                ]
        
        Raises:
            HTTPException: Si hay errores en la validación de datos
        """
        try:
            # Validar entrada
            TOPSISService._validar_entrada(criterios, alternativas)
            
            # Extraer datos
            n_alternativas = len(alternativas)
            n_criterios = len(criterios)
            
            # Crear matriz de decisión
            matriz = np.array([alt["valores"] for alt in alternativas], dtype=float)
            
            # Extraer pesos y tipos
            pesos = np.array([c["peso"] for c in criterios], dtype=float)
            tipos = [c["tipo"] for c in criterios]
            
            # Paso 1: Normalizar la matriz (método euclidiano)
            matriz_normalizada = TOPSISService._normalizar_matriz(matriz)
            
            # Paso 2: Aplicar pesos
            matriz_ponderada = matriz_normalizada * pesos
            
            # Paso 3: Determinar soluciones ideales
            ideal_positiva, ideal_negativa = TOPSISService._calcular_ideales(
                matriz_ponderada, tipos
            )
            
            # Paso 4: Calcular distancias
            distancias_positivas = np.sqrt(
                np.sum((matriz_ponderada - ideal_positiva) ** 2, axis=1)
            )
            distancias_negativas = np.sqrt(
                np.sum((matriz_ponderada - ideal_negativa) ** 2, axis=1)
            )
            
            # Paso 5: Calcular scores TOPSIS
            scores = distancias_negativas / (distancias_positivas + distancias_negativas)
            
            # Construir resultado
            resultados = []
            for i, alternativa in enumerate(alternativas):
                resultados.append({
                    "id": alternativa["id"],
                    "nombre": alternativa.get("nombre", f"Alternativa {alternativa['id']}"),
                    "score": float(scores[i]),
                    "valores": alternativa["valores"],
                })
            
            # Ordenar por score descendente
            resultados.sort(key=lambda x: x["score"], reverse=True)
            
            # Agregar ranking
            for rank, resultado in enumerate(resultados, start=1):
                resultado["ranking"] = rank
            
            # Logging a base de datos (si está disponible)
            if db and usuario_id:
                TOPSISService._log_decision(
                    db=db,
                    usuario_id=usuario_id,
                    tipo="TOPSIS",
                    contexto=contexto or "Ejecución TOPSIS genérica",
                    entrada={
                        "criterios": criterios,
                        "n_alternativas": n_alternativas,
                    },
                    salida={
                        "resultados": resultados,
                        "mejor_alternativa": resultados[0],
                    },
                )
            
            return resultados
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error en los datos de entrada: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error ejecutando TOPSIS: {str(e)}",
            )
    
    @staticmethod
    def _validar_entrada(criterios: List[Dict], alternativas: List[Dict]) -> None:
        """Validar datos de entrada"""
        if not criterios:
            raise ValueError("Debe proporcionar al menos un criterio")
        
        if not alternativas:
            raise ValueError("Debe proporcionar al menos una alternativa")
        
        n_criterios = len(criterios)
        
        # Validar criterios
        for i, criterio in enumerate(criterios):
            if "nombre" not in criterio:
                raise ValueError(f"Criterio {i+1} debe tener 'nombre'")
            if "peso" not in criterio:
                raise ValueError(f"Criterio '{criterio['nombre']}' debe tener 'peso'")
            if "tipo" not in criterio:
                raise ValueError(f"Criterio '{criterio['nombre']}' debe tener 'tipo'")
            if criterio["tipo"] not in ["beneficio", "costo"]:
                raise ValueError(f"Tipo de criterio debe ser 'beneficio' o 'costo'")
            if criterio["peso"] <= 0:
                raise ValueError(f"Peso de criterio debe ser positivo")
        
        # Normalizar pesos a suma 1
        suma_pesos = sum(c["peso"] for c in criterios)
        for criterio in criterios:
            criterio["peso"] = criterio["peso"] / suma_pesos
        
        # Validar alternativas
        for i, alt in enumerate(alternativas):
            if "id" not in alt:
                raise ValueError(f"Alternativa {i+1} debe tener 'id'")
            if "valores" not in alt:
                raise ValueError(f"Alternativa {alt.get('id', i+1)} debe tener 'valores'")
            if len(alt["valores"]) != n_criterios:
                raise ValueError(
                    f"Alternativa {alt.get('id', i+1)} debe tener {n_criterios} valores "
                    f"(uno por cada criterio), tiene {len(alt['valores'])}"
                )
    
    @staticmethod
    def _normalizar_matriz(matriz: np.ndarray) -> np.ndarray:
        """Normalizar matriz usando método euclidiano"""
        # Calcular norma euclidiana para cada columna
        normas = np.sqrt(np.sum(matriz ** 2, axis=0))
        
        # Evitar división por cero
        normas[normas == 0] = 1
        
        return matriz / normas
    
    @staticmethod
    def _calcular_ideales(
        matriz_ponderada: np.ndarray,
        tipos: List[str]
    ) -> tuple:
        """Calcular soluciones ideales positiva y negativa"""
        ideal_positiva = np.zeros(matriz_ponderada.shape[1])
        ideal_negativa = np.zeros(matriz_ponderada.shape[1])
        
        for j, tipo in enumerate(tipos):
            if tipo == "beneficio":
                # Para beneficio: máximo es ideal positiva
                ideal_positiva[j] = np.max(matriz_ponderada[:, j])
                ideal_negativa[j] = np.min(matriz_ponderada[:, j])
            else:  # costo
                # Para costo: mínimo es ideal positiva
                ideal_positiva[j] = np.min(matriz_ponderada[:, j])
                ideal_negativa[j] = np.max(matriz_ponderada[:, j])
        
        return ideal_positiva, ideal_negativa
    
    @staticmethod
    def _log_decision(
        db: Session,
        usuario_id: int,
        tipo: str,
        contexto: str,
        entrada: Dict,
        salida: Dict,
    ) -> None:
        """Guardar log de decisión en base de datos"""
        try:
            import json
            
            log = DecisionLog(
                usuario_id=usuario_id,
                tipo=tipo,
                contexto=contexto,
                entrada_json=json.dumps(entrada, ensure_ascii=False),
                salida_json=json.dumps(salida, ensure_ascii=False),
            )
            
            db.add(log)
            db.commit()
        except Exception as e:
            # No fallar si el logging falla
            print(f"Warning: No se pudo guardar log de decisión: {e}")


# Instancia global del servicio
topsis_service = TOPSISService()

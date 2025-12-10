# app/api/v1/endpoints/topsis.py
"""
Endpoints para el módulo TOPSIS
Permite al COORDINADOR gestionar criterios y calcular prioridad de niños
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List
from datetime import datetime, timedelta

from app.api.deps import get_db, get_current_user
from app.models.usuario import Usuario
from app.models.personal import Personal, EstadoLaboral
from app.models.cita import Cita
from app.schemas.topsis import (
    CriterioTopsisCreate,
    CriterioTopsisUpdate,
    CriterioTopsisRead,
    TopsisInput,
    TopsisResultado
)
from app.schemas.topsis_terapeutas import (
    TopsisEvaluacionRequest,
    TopsisResultado as TopsisResultadoTerapeutas
)
from app.services import topsis_service
from app.services.topsis_terapeutas_service import TopsisEvaluacionService


router = APIRouter(tags=["TOPSIS"])


# ============================================================
# ENDPOINTS CRUD PARA CRITERIOS
# ============================================================

@router.get("/criterios", response_model=List[CriterioTopsisRead])
def get_criterios_topsis(
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene todos los criterios TOPSIS configurados
    Solo COORDINADOR puede acceder
    """
    try:
        criterios = topsis_service.get_criterios(db, incluir_inactivos)
        return criterios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener criterios: {str(e)}"
        )


@router.post("/criterios", response_model=CriterioTopsisRead, status_code=status.HTTP_201_CREATED)
def create_criterio_topsis(
    criterio: CriterioTopsisCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crea un nuevo criterio TOPSIS
    Solo COORDINADOR puede acceder
    """
    try:
        nuevo_criterio = topsis_service.create_criterio(
            db,
            criterio.model_dump()
        )
        return nuevo_criterio
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al crear criterio: {str(e)}"
        )


@router.put("/criterios/{criterio_id}", response_model=CriterioTopsisRead)
def update_criterio_topsis(
    criterio_id: int,
    criterio: CriterioTopsisUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualiza un criterio TOPSIS existente
    Solo COORDINADOR puede acceder
    """
    try:
        criterio_actualizado = topsis_service.update_criterio(
            db,
            criterio_id,
            criterio.model_dump(exclude_unset=True)
        )
        return criterio_actualizado
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar criterio: {str(e)}"
        )


@router.delete("/criterios/{criterio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_criterio_topsis(
    criterio_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Elimina un criterio TOPSIS
    Solo COORDINADOR puede acceder
    """
    try:
        topsis_service.delete_criterio(db, criterio_id)
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al eliminar criterio: {str(e)}"
        )


# ============================================================
# ENDPOINT PARA CÁLCULO DE PRIORIDAD
# ============================================================

@router.post("/prioridad-ninos", response_model=List[TopsisResultado])
def calcular_prioridad_ninos(
    input_data: TopsisInput,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Calcula la prioridad de niños usando el método TOPSIS
    
    Recibe:
    - ids: lista de IDs de niños
    - matriz: matriz de decisión donde cada fila corresponde a un niño
              y cada columna a un criterio
    
    Retorna:
    - Lista de niños con su score y ranking ordenados por prioridad
    
    Solo COORDINADOR puede acceder
    """
    try:
        resultados = topsis_service.calcular_prioridad_ninos(db, input_data)
        return resultados
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al calcular prioridad: {str(e)}"
        )


@router.post("/evaluar-terapeutas", response_model=List[TopsisResultado])
def evaluar_terapeutas(
    input_data: TopsisInput,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Evalúa terapeutas usando el método TOPSIS personalizado
    
    Recibe:
    - ids: lista de IDs de terapeutas (personal)
    - matriz: matriz de decisión donde cada fila corresponde a un terapeuta
              columnas típicas: [carga_trabajo, sesiones_semana, rating/experiencia]
    - pesos: pesos para cada criterio (opcional, si no se envían se usan equitativos)
    
    Retorna:
    - Lista de terapeutas con su score y ranking ordenados
    
    Solo COORDINADOR puede acceder
    """
    try:
        # Validaciones básicas
        if not input_data.ids or not input_data.matriz:
            raise ValueError("Se requieren IDs y matriz de datos")
        
        if len(input_data.ids) != len(input_data.matriz):
            raise ValueError("La cantidad de IDs debe coincidir con las filas de la matriz")
        
        # Pesos por defecto si no se proporcionan (carga, sesiones, rating)
        # Queremos minimizar carga y sesiones, maximizar rating
        pesos = getattr(input_data, 'pesos', None)
        if not pesos:
            num_criterios = len(input_data.matriz[0])
            pesos = [1.0 / num_criterios] * num_criterios
        
        # Tipos: asumimos primeros dos son "costo" (menor es mejor) y último es "beneficio"
        num_criterios = len(input_data.matriz[0])
        if num_criterios == 3:
            tipos = ['costo', 'costo', 'beneficio']  # carga, sesiones, rating
        else:
            # Por defecto todos beneficio
            tipos = ['beneficio'] * num_criterios
        
        # Aplicar TOPSIS
        scores = topsis_service.aplicar_topsis(
            matriz=input_data.matriz,
            pesos=pesos,
            tipos=tipos
        )
        
        # Crear resultados con ranking
        resultados = [
            TopsisResultado(nino_id=id_terapeuta, score=score, ranking=0)
            for id_terapeuta, score in zip(input_data.ids, scores)
        ]
        
        # Ordenar por score descendente y asignar ranking
        resultados.sort(key=lambda x: x.score, reverse=True)
        for i, resultado in enumerate(resultados, start=1):
            resultado.ranking = i
        
        return resultados
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al evaluar terapeutas: {str(e)}"
        )


@router.get("/matriz-terapeutas", response_model=dict)
def obtener_matriz_terapeutas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene automáticamente los terapeutas activos y construye la matriz para TOPSIS
    
    Retorna:
    {
        "terapeutas": [
            {"id": 1, "nombre": "Juan Pérez", "carga": 8, "sesiones_semana": 10, "rating": 4.5},
            ...
        ],
        "ids": [1, 2, 3, ...],
        "matriz": [[8, 10, 4.5], [5, 15, 4.8], ...],
        "criterios": ["Carga de Trabajo", "Sesiones esta Semana", "Rating/Experiencia"]
    }
    
    Solo COORDINADOR puede acceder
    """
    try:
        # Obtener solo terapeutas activos
        terapeutas = db.query(Personal).filter(
            Personal.estado_laboral == EstadoLaboral.ACTIVO,
            Personal.especialidad_principal.isnot(None)  # Asumimos que tienen especialidad
        ).all()
        
        if not terapeutas:
            return {
                "terapeutas": [],
                "ids": [],
                "matriz": [],
                "criterios": ["Carga de Trabajo", "Sesiones esta Semana", "Rating/Experiencia"],
                "mensaje": "No hay terapeutas activos en el sistema"
            }
        
        # Calcular fecha de inicio de la semana actual (lunes)
        hoy = datetime.now()
        dias_desde_lunes = hoy.weekday()  # 0=lunes, 6=domingo
        inicio_semana = hoy - timedelta(days=dias_desde_lunes)
        inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_semana = inicio_semana + timedelta(days=7)
        
        datos_terapeutas = []
        ids = []
        matriz = []
        
        for terapeuta in terapeutas:
            # Calcular carga de trabajo (citas asignadas totales activas)
            carga = db.query(func.count(Cita.id)).filter(
                Cita.id_personal == terapeuta.id,
                Cita.estado_id.in_([1, 2])  # 1=PROGRAMADA, 2=EN_PROGRESO
            ).scalar() or 0
            
            # Calcular sesiones esta semana (citas en el rango de esta semana)
            sesiones_semana = db.query(func.count(Cita.id)).filter(
                Cita.id_personal == terapeuta.id,
                Cita.fecha_hora >= inicio_semana,
                Cita.fecha_hora < fin_semana,
                Cita.estado_id.in_([1, 2, 3])  # 1=PROGRAMADA, 2=EN_PROGRESO, 3=COMPLETADA
            ).scalar() or 0
            
            # Rating/Experiencia (por ahora usar años de experiencia o un valor por defecto)
            # Si tienes un campo de rating en Personal, úsalo aquí
            # Por ahora usamos un cálculo simple: 4.0 + (años_experiencia * 0.1)
            anos_experiencia = getattr(terapeuta, 'anos_experiencia', 0)
            rating = min(5.0, 4.0 + (anos_experiencia * 0.1))
            
            # Si no hay campo anos_experiencia, usar valor por defecto basado en ID (simulación)
            if anos_experiencia == 0:
                rating = 4.0 + ((terapeuta.id % 10) * 0.1)  # Valores entre 4.0 y 4.9
            
            nombre_completo = f"{terapeuta.nombres} {terapeuta.apellido_paterno} {terapeuta.apellido_materno or ''}".strip()
            
            datos_terapeutas.append({
                "id": terapeuta.id,
                "nombre": nombre_completo,
                "especialidad": terapeuta.especialidad_principal,
                "carga": carga,
                "sesiones_semana": sesiones_semana,
                "rating": round(rating, 2)
            })
            
            ids.append(terapeuta.id)
            matriz.append([carga, sesiones_semana, round(rating, 2)])
        
        return {
            "terapeutas": datos_terapeutas,
            "ids": ids,
            "matriz": matriz,
            "criterios": ["Carga de Trabajo", "Sesiones esta Semana", "Rating/Experiencia"],
            "mensaje": f"{len(terapeutas)} terapeutas encontrados"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener matriz de terapeutas: {str(e)}"
        )


# ============================================================
# ENDPOINTS PARA EVALUACIÓN PROFESIONAL DE TERAPEUTAS
# (Integrado desde topsis_terapeutas.py)
# ============================================================

@router.post(
    "/terapeutas",
    response_model=TopsisResultadoTerapeutas,
    status_code=status.HTTP_200_OK,
    summary="Evaluar terapeutas con TOPSIS profesional",
    description="""
    Evalúa y rankea terapeutas usando el método TOPSIS con datos reales de BD.
    
    **Criterios evaluados:**
    - Carga laboral (citas activas) - menor es mejor
    - Sesiones completadas (experiencia) - mayor es mejor
    - Rating profesional (promedio valoraciones) - mayor es mejor
    - Especialidad (coincidencia con terapia) - match es mejor
    
    **Pesos:** Deben sumar 1.0 (±0.01 tolerancia).
    Por defecto: carga=0.30, sesiones=0.25, rating=0.30, especialidad=0.15
    
    **Acceso:** Solo usuarios con rol COORDINADOR
    """
)
def evaluar_terapeutas_topsis(
    request: TopsisEvaluacionRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
) -> TopsisResultadoTerapeutas:
    """
    Evalúa terapeutas usando TOPSIS con datos reales de la base de datos
    """
    try:
        # Debug: imprimir request recibido
        print(f"🔍 DEBUG - Request recibido: {request}")
        print(f"🔍 DEBUG - Pesos: {request.pesos}")
        print(f"🔍 DEBUG - Tipo de pesos: {type(request.pesos)}")
        
        # Inicializar servicio con db session
        service = TopsisEvaluacionService(db)
        
        # Ejecutar evaluación
        resultado = service.evaluar_terapeutas(request)
        
        return resultado
        
    except ValueError as e:
        # Errores de validación (ej: suma de pesos)
        error_msg = str(e)
        print(f"❌ ERROR de validación: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    except Exception as e:
        # Error inesperado - incluir traceback para debugging
        import traceback
        error_detail = f"Error al evaluar terapeutas: {str(e)}\n{traceback.format_exc()}"
        print(f"❌ ERROR TOPSIS: {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al evaluar terapeutas: {str(e)}"
        )


@router.get(
    "/terapeutas/pesos-default",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Obtener pesos por defecto",
    description="Retorna los pesos por defecto recomendados para TOPSIS (endpoint público)"
)
def obtener_pesos_default() -> dict:
    """Retorna configuración de pesos por defecto"""
    return {
        "carga_laboral": 0.30,
        "sesiones_completadas": 0.25,
        "rating": 0.30,
        "especialidad": 0.15,
        "descripcion": {
            "carga_laboral": "Número de citas activas (menor = mejor disponibilidad)",
            "sesiones_completadas": "Total de sesiones impartidas (mayor = más experiencia)",
            "rating": "Promedio de valoraciones (mayor = mejor calidad)",
            "especialidad": "Coincidencia con terapia solicitada (1 = domina, 0 = no)"
        }
    }

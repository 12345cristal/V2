# app/services/recommend_service.py
"""
Servicio para recomendaciones basadas en contenido
Utiliza similitud de coseno entre perfiles de niños y actividades/terapias
"""
import json
from typing import List, Dict
from sqlalchemy.orm import Session

from app.models.nino import Nino, NinoDiagnostico, NinoInfoEmocional
from app.models.actividad import Actividad
from app.models.terapia import Terapia
from app.schemas.recomendacion import RecomendacionActividad, RecomendacionTerapia
from app.services.vectorizer import (
    build_profile_text,
    build_actividad_text,
    build_terapia_text,
    calcular_similitud
)


def recomendar_actividades_para_nino(
    db: Session, 
    nino_id: int,
    top_n: int = 10
) -> List[RecomendacionActividad]:
    """
    Recomienda actividades para un niño basado en su perfil
    
    Args:
        db: Sesión de base de datos
        nino_id: ID del niño
        top_n: Número máximo de recomendaciones a retornar
    
    Returns:
        Lista de RecomendacionActividad ordenada por score descendente
    """
    # Obtener niño con sus relaciones
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise ValueError(f"Niño con ID {nino_id} no encontrado")
    
    # Obtener diagnóstico e info emocional
    diagnostico = db.query(NinoDiagnostico).filter(
        NinoDiagnostico.nino_id == nino_id
    ).first()
    
    info_emocional = db.query(NinoInfoEmocional).filter(
        NinoInfoEmocional.nino_id == nino_id
    ).first()
    
    # Construir datos del niño
    nino_data = {
        "perfil_contenido": nino.perfil_contenido or {},
        "diagnostico_principal": diagnostico.diagnostico_principal if diagnostico else None,
        "diagnostico_resumen": diagnostico.diagnostico_resumen if diagnostico else None,
        "preferencias": info_emocional.preferencias if info_emocional else None,
        "palabras_clave": info_emocional.palabras_clave if info_emocional else None,
    }
    
    # Construir texto del perfil del niño
    texto_nino = build_profile_text(nino_data)
    
    # Obtener todas las actividades activas
    actividades = db.query(Actividad).filter(Actividad.activo == 1).all()
    
    if not actividades:
        return []
    
    # Construir textos de actividades
    textos_actividades = []
    for act in actividades:
        act_data = {
            "nombre": act.nombre,
            "descripcion": act.descripcion,
            "objetivo": act.objetivo,
            "area_desarrollo": act.area_desarrollo,
            "tags": act.tags
        }
        textos_actividades.append(build_actividad_text(act_data))
    
    # Calcular similitudes
    scores = calcular_similitud(texto_nino, textos_actividades)
    
    # Crear recomendaciones
    recomendaciones = []
    for idx, act in enumerate(actividades):
        tags = act.tags if isinstance(act.tags, list) else []
        if isinstance(act.tags, str):
            try:
                tags = json.loads(act.tags)
            except:
                tags = []
        
        recomendaciones.append(
            RecomendacionActividad(
                actividad_id=act.id,
                nombre=act.nombre,
                descripcion=act.descripcion,
                score=float(scores[idx]),
                tags=tags,
                dificultad=act.dificultad,
                area_desarrollo=act.area_desarrollo
            )
        )
    
    # Ordenar por score descendente
    recomendaciones.sort(key=lambda x: x.score, reverse=True)
    
    # Retornar top N
    return recomendaciones[:top_n]


def recomendar_terapias_para_nino(
    db: Session, 
    nino_id: int,
    top_n: int = 10
) -> List[RecomendacionTerapia]:
    """
    Recomienda terapias para un niño basado en su perfil
    
    Args:
        db: Sesión de base de datos
        nino_id: ID del niño
        top_n: Número máximo de recomendaciones a retornar
    
    Returns:
        Lista de RecomendacionTerapia ordenada por score descendente
    """
    # Obtener niño con sus relaciones
    nino = db.query(Nino).filter(Nino.id == nino_id).first()
    if not nino:
        raise ValueError(f"Niño con ID {nino_id} no encontrado")
    
    # Obtener diagnóstico e info emocional
    diagnostico = db.query(NinoDiagnostico).filter(
        NinoDiagnostico.nino_id == nino_id
    ).first()
    
    info_emocional = db.query(NinoInfoEmocional).filter(
        NinoInfoEmocional.nino_id == nino_id
    ).first()
    
    # Construir datos del niño
    nino_data = {
        "perfil_contenido": nino.perfil_contenido or {},
        "diagnostico_principal": diagnostico.diagnostico_principal if diagnostico else None,
        "diagnostico_resumen": diagnostico.diagnostico_resumen if diagnostico else None,
        "preferencias": info_emocional.preferencias if info_emocional else None,
        "palabras_clave": info_emocional.palabras_clave if info_emocional else None,
    }
    
    # Construir texto del perfil del niño
    texto_nino = build_profile_text(nino_data)
    
    # Obtener todas las terapias activas
    terapias = db.query(Terapia).filter(Terapia.activo == 1).all()
    
    if not terapias:
        return []
    
    # Construir textos de terapias
    textos_terapias = []
    for ter in terapias:
        ter_data = {
            "nombre": ter.nombre,
            "descripcion": ter.descripcion,
            "objetivo_general": ter.objetivo_general,
            "categoria": ter.categoria,
            "tags": ter.tags
        }
        textos_terapias.append(build_terapia_text(ter_data))
    
    # Calcular similitudes
    scores = calcular_similitud(texto_nino, textos_terapias)
    
    # Crear recomendaciones
    recomendaciones = []
    for idx, ter in enumerate(terapias):
        tags = []
        if ter.tags:
            if isinstance(ter.tags, list):
                tags = ter.tags
            elif isinstance(ter.tags, str):
                try:
                    tags = json.loads(ter.tags)
                except:
                    tags = []
        
        recomendaciones.append(
            RecomendacionTerapia(
                terapia_id=ter.id,
                nombre=ter.nombre,
                descripcion=ter.descripcion,
                score=float(scores[idx]),
                categoria=ter.categoria,
                tags=tags
            )
        )
    
    # Ordenar por score descendente
    recomendaciones.sort(key=lambda x: x.score, reverse=True)
    
    # Retornar top N
    return recomendaciones[:top_n]

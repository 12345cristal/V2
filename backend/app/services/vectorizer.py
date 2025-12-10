# app/services/vectorizer.py
"""
Servicio para construir representaciones de texto para recomendación basada en contenido
Utiliza TF-IDF y similitud de coseno
"""
import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def build_profile_text(nino_data: Dict) -> str:
    """
    Construye un texto representativo del perfil del niño
    
    Args:
        nino_data: Diccionario con datos del niño incluyendo:
            - perfil_contenido: JSON con tags, intereses, dificultades
            - diagnostico: información del diagnóstico
            - info_emocional: información emocional
    
    Returns:
        String concatenado con toda la información relevante
    """
    parts = []
    
    # Perfil de contenido (tags, intereses, dificultades)
    if nino_data.get("perfil_contenido"):
        perfil = nino_data["perfil_contenido"]
        if isinstance(perfil, str):
            try:
                perfil = json.loads(perfil)
            except:
                perfil = {}
        
        if perfil.get("tags"):
            parts.append(" ".join(perfil["tags"]))
        if perfil.get("intereses"):
            parts.append(perfil["intereses"])
        if perfil.get("dificultades"):
            parts.append(perfil["dificultades"])
    
    # Diagnóstico
    if nino_data.get("diagnostico_principal"):
        parts.append(nino_data["diagnostico_principal"])
    if nino_data.get("diagnostico_resumen"):
        parts.append(nino_data["diagnostico_resumen"])
    
    # Info emocional
    if nino_data.get("preferencias"):
        parts.append(nino_data["preferencias"])
    if nino_data.get("palabras_clave"):
        parts.append(nino_data["palabras_clave"])
    
    return " ".join(filter(None, parts))


def build_actividad_text(actividad_data: Dict) -> str:
    """
    Construye un texto representativo de la actividad
    
    Args:
        actividad_data: Diccionario con datos de la actividad
    
    Returns:
        String concatenado con información relevante de la actividad
    """
    parts = []
    
    if actividad_data.get("nombre"):
        parts.append(actividad_data["nombre"])
    if actividad_data.get("descripcion"):
        parts.append(actividad_data["descripcion"])
    if actividad_data.get("objetivo"):
        parts.append(actividad_data["objetivo"])
    if actividad_data.get("area_desarrollo"):
        parts.append(actividad_data["area_desarrollo"])
    
    # Tags
    tags = actividad_data.get("tags")
    if tags:
        if isinstance(tags, list):
            parts.append(" ".join(tags))
        elif isinstance(tags, str):
            try:
                tags_list = json.loads(tags)
                parts.append(" ".join(tags_list))
            except:
                parts.append(tags)
    
    return " ".join(filter(None, parts))


def build_terapia_text(terapia_data: Dict) -> str:
    """
    Construye un texto representativo de la terapia
    
    Args:
        terapia_data: Diccionario con datos de la terapia
    
    Returns:
        String concatenado con información relevante de la terapia
    """
    parts = []
    
    if terapia_data.get("nombre"):
        parts.append(terapia_data["nombre"])
    if terapia_data.get("descripcion"):
        parts.append(terapia_data["descripcion"])
    if terapia_data.get("objetivo_general"):
        parts.append(terapia_data["objetivo_general"])
    if terapia_data.get("categoria"):
        parts.append(terapia_data["categoria"])
    
    # Tags
    tags = terapia_data.get("tags")
    if tags:
        if isinstance(tags, list):
            parts.append(" ".join(tags))
        elif isinstance(tags, str):
            try:
                tags_list = json.loads(tags)
                parts.append(" ".join(tags_list))
            except:
                parts.append(tags)
    
    return " ".join(filter(None, parts))


def calcular_similitud(
    texto_referencia: str,
    textos_candidatos: List[str]
) -> np.ndarray:
    """
    Calcula la similitud de coseno entre un texto de referencia y múltiples candidatos
    
    Args:
        texto_referencia: Texto del perfil del niño
        textos_candidatos: Lista de textos de actividades/terapias
    
    Returns:
        Array de scores de similitud (0-1) para cada candidato
    """
    if not texto_referencia or not textos_candidatos:
        return np.zeros(len(textos_candidatos))
    
    # Crear vectorizador TF-IDF
    vectorizer = TfidfVectorizer(
        lowercase=True,
        max_features=500,
        ngram_range=(1, 2),  # Unigramas y bigramas
        min_df=1
    )
    
    # Combinar todos los textos
    todos_textos = [texto_referencia] + textos_candidatos
    
    try:
        # Vectorizar
        tfidf_matrix = vectorizer.fit_transform(todos_textos)
        
        # Calcular similitud de coseno
        # Primera fila es el texto de referencia, resto son candidatos
        similitudes = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        return similitudes[0]
    except Exception as e:
        # Si hay error (ej: todos los textos vacíos), retornar ceros
        return np.zeros(len(textos_candidatos))

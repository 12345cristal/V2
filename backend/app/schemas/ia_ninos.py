# app/schemas/ia_ninos.py
from pydantic import BaseModel


class NinoIAAnalisisResponse(BaseModel):
    metricas: dict
    perfil_textual: str
    analisis_emocional: str
    recomendaciones_terapias: str
    recomendaciones_actividades: str
    explicacion_para_padres: str

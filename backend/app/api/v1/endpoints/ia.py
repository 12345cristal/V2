# app/api/v1/endpoints/ia.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.services.ai.gemini_service import GeminiClient
from app.services.decision_logs_service import registrar_decision

router = APIRouter(prefix="/ia", tags=["IA"])


@router.post("/resumen-sesion")
def resumir_sesion(texto: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    ia = GeminiClient()
    resultado = ia.resumen_sesion(texto)
    registrar_decision(db, "resumen_sesion", texto, resultado, user.id)
    return {"resultado": resultado}


@router.post("/nota-soap")
def generar_soap(texto: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    ia = GeminiClient()
    resultado = ia.generar_nota_SOAP(texto)
    registrar_decision(db, "nota_SOAP", texto, resultado, user.id)
    return {"resultado": resultado}


@router.post("/perfil-emocional")
def perfil_emocional(texto: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    ia = GeminiClient()
    resultado = ia.perfil_emocional(texto)
    registrar_decision(db, "perfil_emocional", texto, resultado, user.id)
    return {"resultado": resultado}


@router.post("/recomendar-terapias")
def recomendar_terapias(diagnostico: str, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    ia = GeminiClient()
    resultado = ia.recomendar_terapias(diagnostico)
    registrar_decision(db, "recomendar_terapias", diagnostico, resultado, user.id)
    return {"resultado": resultado}

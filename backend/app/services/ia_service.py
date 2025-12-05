# app/services/ia_service.py

from sqlalchemy.orm import Session
from app.services.gemini_client import GeminiClient
from app.services.auditoria_service import registrar_evento
from app.models.decision_logs import DecisionLog
import json


class IAService:

    @staticmethod
    def analisis_completo_nino(nino, texto_extra, db: Session, usuario_id: int):

        entrada = {
            "nino": nino.id,
            "diagnostico": nino.diagnostico.diagnostico_principal if nino.diagnostico else None,
            "emocional": nino.info_emocional.estimulos_ansiedad if nino.info_emocional else None,
            "extra": texto_extra
        }

        resultado = GeminiClient.analisis_completo_nino(entrada)

        log = DecisionLog(
            tipo_decision="ANALISIS_COMPLETO",
            entrada_json=json.dumps(entrada),
            resultado_json=json.dumps(resultado),
            usuario_id=usuario_id
        )
        db.add(log)
        db.commit()

        return resultado

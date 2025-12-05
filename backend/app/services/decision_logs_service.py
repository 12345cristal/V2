# app/services/decision_logs_service.py
from app.models.decision_logs import DecisionLog
from sqlalchemy.orm import Session

def registrar_decision(db: Session, tipo: str, entrada: str, resultado: str, user_id: int):
    log = DecisionLog(
        tipo_decision=tipo,
        entrada_json=entrada,
        resultado_json=resultado,
        usuario_id=user_id
    )
    db.add(log)
    db.commit()

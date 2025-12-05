from pydantic import BaseModel
from datetime import datetime

class DecisionLogRead(BaseModel):
    id: int
    tipo_decision: str
    entrada_json: str
    resultado_json: str
    fecha: datetime

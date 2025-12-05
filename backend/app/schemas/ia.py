# app/schemas/ia.py

from pydantic import BaseModel


class ResumenIAResponse(BaseModel):
    resumen: str

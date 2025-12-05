from fastapi import Request
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.auditoria import Auditoria
import json

async def audit_middleware(request: Request, call_next):
    response = await call_next(request)

    try:
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            db: Session = SessionLocal()

            user_id = None
            if "authorization" in request.headers:
                token = request.headers["authorization"].replace("Bearer ", "")
                # Se puede decodificar para obtener user_id si ya se montó get_current_user
                
            audit_entry = Auditoria(
                usuario_id=user_id,
                accion=f"{request.method} {request.url.path}",
                tabla_afectada=request.url.path.split("/")[2] if "/api/v1/" in request.url.path else None,
                registro_id=None
            )
            db.add(audit_entry)
            db.commit()
            db.close()
    except Exception:
        pass

    return response

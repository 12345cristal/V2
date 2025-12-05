# app/services/auth_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.security import verify_password, create_access_token

def autenticar_usuario(db: Session, correo: str, contrasena: str):
    user = db.query(Usuario).filter(Usuario.email == correo).first()

    if not user:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")

    if not verify_password(contrasena, user.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")

    if not user.activo:
        raise HTTPException(status_code=403, detail="Tu cuenta está inactiva.")

    token = create_access_token({"sub": str(user.id), "rol": user.rol_id})

    return user, token

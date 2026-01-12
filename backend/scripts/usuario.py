#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.usuario import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_usuario():
    db = SessionLocal()
    try:
        # Verificar si existe
        existe = db.query(Usuario).filter(Usuario.email == "lopez@padre.com").first()
        if existe:
            print("✓ Usuario ya existe")
            return
        
        # Crear usuario
        usuario = Usuario(
            nombres="López",
            apellido_paterno="García",
            apellido_materno="Rodríguez",
            email="lopez@padre.com",
            hashed_password=pwd_context.hash("12345678"),
            rol_id=4,
            telefono="555123456",
            activo=True
        )
        
        db.add(usuario)
        db.commit()
        
        print("✓ Usuario creado exitosamente")
        print(f"  Email: {usuario.email}")
        print(f"  Contraseña: 12345678")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    crear_usuario()

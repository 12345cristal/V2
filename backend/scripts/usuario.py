#!/usr/bin/env python3
"""
Script para crear usuario de prueba: lopez@padre.com
"""
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.usuario import Usuario
from passlib.context import CryptContext

# Configurar el contexto de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def crear_usuario():
    """Crear usuario padre de prueba"""
    db = SessionLocal()
    try:
        # Verificar si el usuario ya existe
        existe = db.query(Usuario).filter(Usuario.email == "lopez@padre.com").first()
        if existe:
            print("✓ Usuario ya existe")
            print(f"  ID: {existe.id}")
            print(f"  Email: {existe.email}")
            print(f"  Nombres: {existe.nombres}")
            print(f"  Rol ID: {existe.rol_id}")
            print(f"  Activo: {existe.activo}")
            return
        
        # Crear nuevo usuario
        usuario = Usuario(
            nombres="López",
            apellido_paterno="García",
            apellido_materno="Rodríguez",
            email="lopez@padre.com",
            hashed_password=pwd_context.hash("12345678"),
            rol_id=4,  # Rol PADRE
            telefono="555123456",
            activo=True
        )
        
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
        print("✓ Usuario creado exitosamente")
        print(f"  ID: {usuario.id}")
        print(f"  Email: {usuario.email}")
        print(f"  Contraseña: 12345678")
        print(f"  Nombres: {usuario.nombres}")
        print(f"  Rol ID: {usuario.rol_id}")
        print(f"  Activo: {usuario.activo}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    crear_usuario()

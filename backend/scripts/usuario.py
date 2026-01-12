#!/usr/bin/env python3
# backend/scripts/crear_usuario_prueba.py

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def crear_usuario_padre():
    """Crea un usuario PADRE de prueba"""
    db: Session = SessionLocal()

    try:
        # Buscar rol PADRE
        rol_padre = db.query(Rol).filter(Rol.nombre == "PADRE").first()
        if not rol_padre:
            print("✗ No existe el rol PADRE en la base de datos")
            return

        # Verificar si el usuario ya existe
        usuario_existente = db.query(Usuario).filter(
            Usuario.email == "lopez@padre.com"
        ).first()

        if usuario_existente:
            print("✗ El usuario ya existe")
            return

        # Crear usuario
        usuario = Usuario(
            nombres="López",
            apellido_paterno="García",
            apellido_materno="Rodríguez",
            email="lopez@padre.com",
            hashed_password=pwd_context.hash("12345678"),
            rol_id=rol_padre.id,
            telefono="555123456",
            activo=True,
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        print("✓ Usuario PADRE creado exitosamente")
        print(f"  ID: {usuario.id}")
        print(f"  Email: {usuario.email}")
        print(f"  Rol: {rol_padre.nombre}")
        print("\nCredenciales de acceso:")
        print("  Email: lopez@padre.com")
        print("  Contraseña: 12345678")

    except Exception as e:
        db.rollback()
        print("✗ Error al crear el usuario")
        print(str(e))
    finally:
        db.close()


if __name__ == "__main__":
    crear_usuario_padre()

"""
Script para crear usuarios demo con contraseña válida.
Contraseña para todos: 12345678
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.db.session import SessionLocal


USUARIOS_DEMO = [
    {
        "nombres": "Ana",
        "apellido_paterno": "Ramírez",
        "apellido_materno": "Lopez",
        "email": "admin@demo.com",
        "telefono": "6671000001",
        "rol_id": 1,  # ADMIN
    },
    {
        "nombres": "Carlos",
        "apellido_paterno": "Martínez",
        "apellido_materno": "Soto",
        "email": "coordinador@demo.com",
        "telefono": "6671000002",
        "rol_id": 2,  # COORDINADOR
    },
    {
        "nombres": "María",
        "apellido_paterno": "Hernández",
        "apellido_materno": "Ruiz",
        "email": "terapeuta@demo.com",
        "telefono": "6671000003",
        "rol_id": 3,  # TERAPEUTA
    },
    {
        "nombres": "Laura",
        "apellido_paterno": "Gómez",
        "apellido_materno": "Pérez",
        "email": "padre@demo.com",
        "telefono": "6671000004",
        "rol_id": 4,  # PADRE
    },
]


def crear_usuarios_demo():
    """Crear o actualizar usuarios demo en la BD"""
    db = SessionLocal()
    try:
        print("🔐 Generando hash de contraseña...")
        password_demo = hash_password("12345678")
        
        print("👥 Creando/actualizando usuarios demo...")
        for data in USUARIOS_DEMO:
            usuario = db.query(Usuario).filter(Usuario.email == data["email"]).first()

            if usuario:
                print(f"  ✏️  Actualizando: {data['email']}")
                # Actualiza contraseña y datos por si estaban mal
                usuario.hashed_password = password_demo
                usuario.rol_id = data["rol_id"]
                usuario.activo = 1
                usuario.nombres = data["nombres"]
                usuario.apellido_paterno = data["apellido_paterno"]
                usuario.apellido_materno = data.get("apellido_materno")
                usuario.telefono = data.get("telefono")
            else:
                print(f"  ➕ Creando nuevo: {data['email']}")
                usuario = Usuario(
                    nombres=data["nombres"],
                    apellido_paterno=data["apellido_paterno"],
                    apellido_materno=data.get("apellido_materno"),
                    email=data["email"],
                    telefono=data.get("telefono"),
                    hashed_password=password_demo,
                    rol_id=data["rol_id"],
                    activo=1,
                )
                db.add(usuario)

        db.commit()
        print("\n✅ Usuarios demo creados/actualizados exitosamente")
        print("📧 Email: admin@demo.com, coordinador@demo.com, terapeuta@demo.com, padre@demo.com")
        print("🔑 Contraseña: 12345678")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("CREAR USUARIOS DEMO - Autismo Mochis IA")
    print("="*60 + "\n")
    crear_usuarios_demo()
    print("\n" + "="*60 + "\n")

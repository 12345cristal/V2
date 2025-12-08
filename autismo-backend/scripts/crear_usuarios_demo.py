"""Crear/actualizar usuarios demo con contraseña válida."""

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.db.session import SessionLocal


USUARIOS_DEMO = [
    {
        "nombres": "Ana",
        "apellido_paterno": "Ramírez",
        "apellido_materno": "Lopez",
        "email": "admin@demo.com",
        "rol_id": 1,
    },
    {
        "nombres": "Carlos",
        "apellido_paterno": "Martínez",
        "apellido_materno": "Soto",
        "email": "coordinador@demo.com",
        "rol_id": 2,
    },
    {
        "nombres": "María",
        "apellido_paterno": "Hernández",
        "apellido_materno": "Ruiz",
        "email": "terapeuta@demo.com",
        "rol_id": 3,
    },
    {
        "nombres": "Laura",
        "apellido_paterno": "Gómez",
        "apellido_materno": "Pérez",
        "email": "padre@demo.com",
        "rol_id": 4,
    },
]


def crear_usuarios_demo():
    db = SessionLocal()
    try:
        password_demo = hash_password("12345678")

        for data in USUARIOS_DEMO:
            usuario = db.query(Usuario).filter(Usuario.email == data["email"]).first()

            if usuario:
                # Actualiza contraseña y rol por si estaban mal
                usuario.hashed_password = password_demo
                usuario.rol_id = data["rol_id"]
                usuario.activo = True
            else:
                usuario = Usuario(
                    **data,
                    hashed_password=password_demo,
                    activo=True,
                )
                db.add(usuario)

        db.commit()
        print("Usuarios demo creados/actualizados con contraseña 12345678.")
    finally:
        db.close()


if __name__ == "__main__":
    crear_usuarios_demo()

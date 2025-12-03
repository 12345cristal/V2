from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.usuario import Usuario

db = SessionLocal()

user = Usuario(
    nombres="Ana",
    apellido_paterno="López",
    apellido_materno="García",
    email="ana@coordi.com",
    hashed_password=hash_password("123456"),
    rol_id=2  # administrador
)

db.add(user)
db.commit()

print("Usuario creado:", user.email)

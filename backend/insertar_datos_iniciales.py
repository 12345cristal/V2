#!/usr/bin/env python3
"""
Insertar datos iniciales: Roles y Usuarios
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.personal import Personal
from app.core.config import settings
from app.core.security import get_password_hash

# Crear conexión
engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def insertar_roles():
    """Insertar roles base si no existen"""
    roles_existentes = session.query(Rol).all()
    
    if roles_existentes:
        print(f"✅ {len(roles_existentes)} roles ya existen en la BD")
        return
    
    roles = [
        Rol(nombre="admin", descripcion="Administrador del sistema"),
        Rol(nombre="coordinador", descripcion="Coordinador de terapias"),
        Rol(nombre="terapeuta", descripcion="Personal terapeuta"),
        Rol(nombre="padre", descripcion="Padre/tutor de niño"),
    ]
    
    session.add_all(roles)
    session.commit()
    print(f"✅ {len(roles)} roles creados exitosamente")


def insertar_usuarios():
    """Insertar usuarios de prueba si no existen"""
    usuarios_existentes = session.query(Usuario).all()
    
    if usuarios_existentes:
        print(f"✅ {len(usuarios_existentes)} usuarios ya existen en la BD")
        return
    
    # Obtener rol coordinador
    rol_coordinador = session.query(Rol).filter_by(nombre="coordinador").first()
    rol_terapeuta = session.query(Rol).filter_by(nombre="terapeuta").first()
    rol_admin = session.query(Rol).filter_by(nombre="admin").first()
    
    if not rol_coordinador or not rol_terapeuta or not rol_admin:
        print("❌ No se encontraron los roles. Ejecuta insertar_roles() primero")
        return
    
    usuarios = [
        Usuario(
            email="admin@sistema.com",
            password_hash=get_password_hash("admin123"),
            rol_id=rol_admin.id,
            estado="ACTIVO"
        ),
        Usuario(
            email="coordinador@sistema.com",
            password_hash=get_password_hash("coord123"),
            rol_id=rol_coordinador.id,
            estado="ACTIVO"
        ),
        Usuario(
            email="terapeuta1@sistema.com",
            password_hash=get_password_hash("tera123"),
            rol_id=rol_terapeuta.id,
            estado="ACTIVO"
        ),
        Usuario(
            email="terapeuta2@sistema.com",
            password_hash=get_password_hash("tera123"),
            rol_id=rol_terapeuta.id,
            estado="ACTIVO"
        ),
    ]
    
    session.add_all(usuarios)
    session.commit()
    print(f"✅ {len(usuarios)} usuarios creados exitosamente")
    
    # Mostrar usuarios activos
    usuarios_activos = session.query(Usuario).filter_by(estado="ACTIVO").all()
    print("\n📋 USUARIOS ACTIVOS:")
    for u in usuarios_activos:
        print(f"  • {u.email} (Rol: {u.rol.nombre if u.rol else 'N/A'})")


if __name__ == "__main__":
    try:
        print("=" * 50)
        print("INSERTANDO DATOS INICIALES")
        print("=" * 50)
        
        insertar_roles()
        insertar_usuarios()
        
        # Mostrar resumen
        print("\n" + "=" * 50)
        print("RESUMEN DE DATOS:")
        print("=" * 50)
        
        total_roles = session.query(Rol).count()
        total_usuarios = session.query(Usuario).count()
        usuarios_activos = session.query(Usuario).filter_by(estado="ACTIVO").count()
        
        print(f"✅ Total de roles: {total_roles}")
        print(f"✅ Total de usuarios: {total_usuarios}")
        print(f"✅ Usuarios activos: {usuarios_activos}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

#!/usr/bin/env python3
"""
Script para crear usuario de prueba para padre - lopez@padre.com
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.core.security import get_password_hash


def crear_usuario_padre():
    """Crear usuario padre de prueba"""
    try:
        db = SessionLocal()
    except Exception as e:
        print(f"\n❌ Error al conectar a la base de datos: {str(e)}")
        print("\n⚠️  Verifica que:")
        print("   1. MySQL está corriendo")
        print("   2. La base de datos 'autismo_mochis_ia' existe")
        print("   3. Las credenciales en .env son correctas")
        print("   4. El archivo .env existe en backend/")
        return False
    
    try:
        # Verificar que el rol Padre existe (ID = 4)
        rol_padre = db.query(Rol).filter(Rol.id == 4).first()
        if not rol_padre:
            print("❌ Error: El rol Padre (ID=4) no existe en la base de datos")
            print("   Ejecuta primero: python scripts/init_roles_permisos.py")
            return False
        
        print(f"✓ Rol encontrado: {rol_padre.nombre} (ID: {rol_padre.id})")
        
        # Verificar si el usuario ya existe
        usuario_existente = db.query(Usuario).filter(Usuario.email == "lopez@padre.com").first()
        if usuario_existente:
            print(f"\n⚠️  El usuario lopez@padre.com ya existe:")
            print(f"   ID: {usuario_existente.id}")
            print(f"   Nombre: {usuario_existente.nombres} {usuario_existente.apellido_paterno}")
            print(f"   Rol: {usuario_existente.rol.nombre} (ID: {usuario_existente.rol_id})")
            print(f"   Estado: {'Activo' if usuario_existente.activo else 'Inactivo'}")
            
            # Preguntar si desea actualizar la contraseña
            respuesta = input("\n¿Desea actualizar la contraseña a '12345678'? (s/n): ")
            if respuesta.lower() == 's':
                usuario_existente.hashed_password = get_password_hash("12345678")
                db.commit()
                print("\n✓ Contraseña actualizada exitosamente")
            else:
                print("\n- No se realizaron cambios")
            
            return True
        
        # Crear el nuevo usuario
        nuevo_usuario = Usuario(
            nombres="Lopez",
            apellido_paterno="Padre",
            apellido_materno="Test",
            email="lopez@padre.com",
            hashed_password=get_password_hash("12345678"),
            rol_id=4,  # Padre
            telefono="6681234567",
            activo=True
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        print("\n" + "="*60)
        print("✓ Usuario lopez@padre.com creado exitosamente")
        print("="*60)
        print(f"  ID: {nuevo_usuario.id}")
        print(f"  Nombre: {nuevo_usuario.nombres} {nuevo_usuario.apellido_paterno} {nuevo_usuario.apellido_materno}")
        print(f"  Email: {nuevo_usuario.email}")
        print(f"  Rol: {nuevo_usuario.rol.nombre} (ID: {nuevo_usuario.rol_id})")
        print(f"  Teléfono: {nuevo_usuario.telefono}")
        print(f"  Estado: {'Activo' if nuevo_usuario.activo else 'Inactivo'}")
        print(f"  Contraseña: 12345678")
        print("="*60)
        print("\n✓ Ahora puedes usar estas credenciales para login en el frontend")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al crear el usuario: {str(e)}")
        db.rollback()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Crear Usuario Padre de Prueba")
    print("="*60 + "\n")
    
    exito = crear_usuario_padre()
    
    if exito:
        print("\n✓ Proceso completado exitosamente")
    else:
        print("\n❌ El proceso falló")
        sys.exit(1)

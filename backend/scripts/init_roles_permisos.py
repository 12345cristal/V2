# scripts/init_roles_permisos.py
"""
Script para inicializar roles y permisos en la base de datos
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso
from app.core.security import get_password_hash
from app.models.usuario import Usuario


def init_roles():
    """Crear roles iniciales"""
    db = SessionLocal()
    
    roles = [
        {"id": 1, "nombre": "Admin", "descripcion": "Administrador del sistema"},
        {"id": 2, "nombre": "Coordinador", "descripcion": "Coordinador del centro"},
        {"id": 3, "nombre": "Terapeuta", "descripcion": "Terapeuta del centro"},
        {"id": 4, "nombre": "Padre", "descripcion": "Padre o tutor de niño"},
    ]
    
    for rol_data in roles:
        rol = db.query(Rol).filter(Rol.id == rol_data["id"]).first()
        if not rol:
            rol = Rol(**rol_data)
            db.add(rol)
            print(f"✓ Rol creado: {rol_data['nombre']}")
        else:
            print(f"- Rol ya existe: {rol_data['nombre']}")
    
    db.commit()
    db.close()


def init_permisos():
    """Crear permisos iniciales"""
    db = SessionLocal()
    
    permisos = [
        # Gestión de usuarios
        {"codigo": "ver_usuarios", "descripcion": "Ver lista de usuarios"},
        {"codigo": "crear_usuarios", "descripcion": "Crear nuevos usuarios"},
        {"codigo": "editar_usuarios", "descripcion": "Editar usuarios existentes"},
        {"codigo": "eliminar_usuarios", "descripcion": "Eliminar usuarios"},
        
        # Gestión de niños
        {"codigo": "ver_ninos", "descripcion": "Ver lista de niños"},
        {"codigo": "crear_ninos", "descripcion": "Registrar nuevos niños"},
        {"codigo": "editar_ninos", "descripcion": "Editar información de niños"},
        {"codigo": "eliminar_ninos", "descripcion": "Eliminar niños"},
        {"codigo": "ver_diagnosticos", "descripcion": "Ver diagnósticos de niños"},
        
        # Gestión de personal
        {"codigo": "ver_personal", "descripcion": "Ver lista de personal"},
        {"codigo": "crear_personal", "descripcion": "Registrar nuevo personal"},
        {"codigo": "editar_personal", "descripcion": "Editar información de personal"},
        {"codigo": "eliminar_personal", "descripcion": "Eliminar personal"},
        
        # Gestión de citas
        {"codigo": "ver_citas", "descripcion": "Ver citas"},
        {"codigo": "crear_citas", "descripcion": "Crear nuevas citas"},
        {"codigo": "editar_citas", "descripcion": "Editar citas existentes"},
        {"codigo": "cancelar_citas", "descripcion": "Cancelar citas"},
        
        # Gestión de terapias
        {"codigo": "ver_terapias", "descripcion": "Ver terapias"},
        {"codigo": "crear_terapias", "descripcion": "Crear nuevas terapias"},
        {"codigo": "editar_terapias", "descripcion": "Editar terapias"},
        {"codigo": "asignar_terapias", "descripcion": "Asignar terapias a niños"},
        
        # Gestión de sesiones
        {"codigo": "ver_sesiones", "descripcion": "Ver sesiones de terapia"},
        {"codigo": "registrar_sesiones", "descripcion": "Registrar nuevas sesiones"},
        {"codigo": "editar_sesiones", "descripcion": "Editar sesiones"},
        
        # Gestión de recursos
        {"codigo": "ver_recursos", "descripcion": "Ver recursos educativos"},
        {"codigo": "crear_recursos", "descripcion": "Crear nuevos recursos"},
        {"codigo": "editar_recursos", "descripcion": "Editar recursos"},
        {"codigo": "eliminar_recursos", "descripcion": "Eliminar recursos"},
        {"codigo": "asignar_recursos", "descripcion": "Asignar recursos a niños"},
        
        # Reportes y análisis
        {"codigo": "ver_reportes", "descripcion": "Ver reportes y estadísticas"},
        {"codigo": "ver_auditoria", "descripcion": "Ver logs de auditoría"},
        
        # IA y recomendaciones
        {"codigo": "usar_ia", "descripcion": "Usar funciones de IA"},
        {"codigo": "ver_recomendaciones", "descripcion": "Ver recomendaciones de IA"},
    ]
    
    for permiso_data in permisos:
        permiso = db.query(Permiso).filter(Permiso.codigo == permiso_data["codigo"]).first()
        if not permiso:
            permiso = Permiso(**permiso_data)
            db.add(permiso)
            print(f"✓ Permiso creado: {permiso_data['codigo']}")
        else:
            print(f"- Permiso ya existe: {permiso_data['codigo']}")
    
    db.commit()
    db.close()


def asignar_permisos_roles():
    """Asignar permisos a roles"""
    db = SessionLocal()
    
    # ADMIN - Todos los permisos
    admin = db.query(Rol).filter(Rol.id == 1).first()
    todos_permisos = db.query(Permiso).all()
    admin.permisos = todos_permisos
    print(f"✓ Asignados {len(todos_permisos)} permisos a Admin")
    
    # COORDINADOR - Gestión completa excepto usuarios admin
    coordinador = db.query(Rol).filter(Rol.id == 2).first()
    permisos_coordinador = db.query(Permiso).filter(
        Permiso.codigo.in_([
            "ver_usuarios", "crear_usuarios", "editar_usuarios",
            "ver_ninos", "crear_ninos", "editar_ninos", "ver_diagnosticos",
            "ver_personal", "crear_personal", "editar_personal",
            "ver_citas", "crear_citas", "editar_citas", "cancelar_citas",
            "ver_terapias", "crear_terapias", "editar_terapias", "asignar_terapias",
            "ver_sesiones", "ver_recursos", "crear_recursos", "editar_recursos", "asignar_recursos",
            "ver_reportes", "usar_ia", "ver_recomendaciones"
        ])
    ).all()
    coordinador.permisos = permisos_coordinador
    print(f"✓ Asignados {len(permisos_coordinador)} permisos a Coordinador")
    
    # TERAPEUTA - Gestión de sesiones y recursos
    terapeuta = db.query(Rol).filter(Rol.id == 3).first()
    permisos_terapeuta = db.query(Permiso).filter(
        Permiso.codigo.in_([
            "ver_ninos", "ver_diagnosticos",
            "ver_citas", "editar_citas",
            "ver_terapias", "ver_sesiones", "registrar_sesiones", "editar_sesiones",
            "ver_recursos", "crear_recursos", "editar_recursos", "asignar_recursos",
            "ver_recomendaciones"
        ])
    ).all()
    terapeuta.permisos = permisos_terapeuta
    print(f"✓ Asignados {len(permisos_terapeuta)} permisos a Terapeuta")
    
    # PADRE - Solo consulta
    padre = db.query(Rol).filter(Rol.id == 4).first()
    permisos_padre = db.query(Permiso).filter(
        Permiso.codigo.in_([
            "ver_ninos", "ver_citas", "ver_sesiones", "ver_recursos"
        ])
    ).all()
    padre.permisos = permisos_padre
    print(f"✓ Asignados {len(permisos_padre)} permisos a Padre")
    
    db.commit()
    db.close()


def crear_usuario_admin():
    """Crear usuario administrador por defecto"""
    db = SessionLocal()
    
    admin = db.query(Usuario).filter(Usuario.email == "admin@autismo.com").first()
    if not admin:
        admin = Usuario(
            nombres="Administrador",
            apellido_paterno="Sistema",
            email="admin@autismo.com",
            hashed_password=get_password_hash("admin123"),
            rol_id=1,
            activo=True
        )
        db.add(admin)
        db.commit()
        print("✓ Usuario administrador creado:")
        print("  Email: admin@autismo.com")
        print("  Password: admin123")
        print("  ⚠️ CAMBIA ESTA CONTRASEÑA INMEDIATAMENTE")
    else:
        print("- Usuario administrador ya existe")
    
    db.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Inicializando roles y permisos")
    print("="*50 + "\n")
    
    print("1. Creando roles...")
    init_roles()
    
    print("\n2. Creando permisos...")
    init_permisos()
    
    print("\n3. Asignando permisos a roles...")
    asignar_permisos_roles()
    
    print("\n4. Creando usuario administrador...")
    crear_usuario_admin()
    
    print("\n" + "="*50)
    print("✓ Inicialización completada exitosamente")
    print("="*50 + "\n")

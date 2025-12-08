"""
Script para inicializar roles y permisos básicos del sistema.
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models.rol import Rol
from app.models.permiso import Permiso
from app.models.role_permiso import RolePermiso


# Roles del sistema
ROLES = [
    {"id": 1, "nombre": "ADMIN", "descripcion": "Administrador del sistema con acceso total"},
    {"id": 2, "nombre": "COORDINADOR", "descripcion": "Coordinador del centro de terapias"},
    {"id": 3, "nombre": "TERAPEUTA", "descripcion": "Terapeuta que atiende a los niños"},
    {"id": 4, "nombre": "PADRE", "descripcion": "Padre o tutor de un niño"},
]

# Permisos del sistema (módulo:acción)
PERMISOS = [
    # Usuarios
    {"codigo": "usuarios:ver", "descripcion": "Ver listado de usuarios"},
    {"codigo": "usuarios:crear", "descripcion": "Crear nuevos usuarios"},
    {"codigo": "usuarios:editar", "descripcion": "Editar usuarios existentes"},
    {"codigo": "usuarios:eliminar", "descripcion": "Eliminar usuarios"},
    
    # Roles y Permisos
    {"codigo": "roles:ver", "descripcion": "Ver roles del sistema"},
    {"codigo": "roles:editar", "descripcion": "Editar roles y permisos"},
    
    # Personal (Terapeutas)
    {"codigo": "personal:ver", "descripcion": "Ver personal del centro"},
    {"codigo": "personal:crear", "descripcion": "Registrar nuevo personal"},
    {"codigo": "personal:editar", "descripcion": "Editar información de personal"},
    {"codigo": "personal:eliminar", "descripcion": "Eliminar personal"},
    
    # Niños
    {"codigo": "ninos:ver", "descripcion": "Ver listado de niños"},
    {"codigo": "ninos:crear", "descripcion": "Registrar nuevo niño"},
    {"codigo": "ninos:editar", "descripcion": "Editar información de niño"},
    {"codigo": "ninos:eliminar", "descripcion": "Eliminar niño"},
    {"codigo": "ninos:ver_propios", "descripcion": "Ver solo niños asignados (padres/terapeutas)"},
    
    # Terapias
    {"codigo": "terapias:ver", "descripcion": "Ver terapias del sistema"},
    {"codigo": "terapias:crear", "descripcion": "Crear nuevas terapias"},
    {"codigo": "terapias:editar", "descripcion": "Editar terapias"},
    {"codigo": "terapias:eliminar", "descripcion": "Eliminar terapias"},
    
    # Citas
    {"codigo": "citas:ver", "descripcion": "Ver todas las citas"},
    {"codigo": "citas:ver_propias", "descripcion": "Ver solo citas propias"},
    {"codigo": "citas:crear", "descripcion": "Crear nuevas citas"},
    {"codigo": "citas:editar", "descripcion": "Editar citas"},
    {"codigo": "citas:cancelar", "descripcion": "Cancelar citas"},
    
    # Sesiones
    {"codigo": "sesiones:ver", "descripcion": "Ver sesiones de terapia"},
    {"codigo": "sesiones:crear", "descripcion": "Registrar sesiones"},
    {"codigo": "sesiones:editar", "descripcion": "Editar sesiones"},
    
    # Recursos
    {"codigo": "recursos:ver", "descripcion": "Ver recursos disponibles"},
    {"codigo": "recursos:crear", "descripcion": "Crear nuevos recursos"},
    {"codigo": "recursos:editar", "descripcion": "Editar recursos"},
    {"codigo": "recursos:eliminar", "descripcion": "Eliminar recursos"},
    
    # Notificaciones
    {"codigo": "notificaciones:ver", "descripcion": "Ver notificaciones"},
    {"codigo": "notificaciones:enviar", "descripcion": "Enviar notificaciones"},
    
    # Priorización (TOPSIS)
    {"codigo": "priorizacion:ejecutar", "descripcion": "Ejecutar algoritmos de priorización"},
    {"codigo": "priorizacion:ver_logs", "descripcion": "Ver logs de decisiones"},
    
    # IA (Gemini)
    {"codigo": "ia:usar", "descripcion": "Usar funcionalidades de IA"},
    {"codigo": "ia:ver_logs", "descripcion": "Ver logs de IA"},
    
    # Auditoría
    {"codigo": "auditoria:ver", "descripcion": "Ver registros de auditoría"},
]

# Asignación de permisos a roles
ROLE_PERMISOS = {
    "ADMIN": [  # Todos los permisos
        "usuarios:ver", "usuarios:crear", "usuarios:editar", "usuarios:eliminar",
        "roles:ver", "roles:editar",
        "personal:ver", "personal:crear", "personal:editar", "personal:eliminar",
        "ninos:ver", "ninos:crear", "ninos:editar", "ninos:eliminar",
        "terapias:ver", "terapias:crear", "terapias:editar", "terapias:eliminar",
        "citas:ver", "citas:crear", "citas:editar", "citas:cancelar",
        "sesiones:ver", "sesiones:crear", "sesiones:editar",
        "recursos:ver", "recursos:crear", "recursos:editar", "recursos:eliminar",
        "notificaciones:ver", "notificaciones:enviar",
        "priorizacion:ejecutar", "priorizacion:ver_logs",
        "ia:usar", "ia:ver_logs",
        "auditoria:ver",
    ],
    "COORDINADOR": [
        "usuarios:ver",
        "personal:ver", "personal:crear", "personal:editar",
        "ninos:ver", "ninos:crear", "ninos:editar",
        "terapias:ver", "terapias:crear", "terapias:editar",
        "citas:ver", "citas:crear", "citas:editar", "citas:cancelar",
        "sesiones:ver", "sesiones:crear",
        "recursos:ver", "recursos:crear", "recursos:editar",
        "notificaciones:ver", "notificaciones:enviar",
        "priorizacion:ejecutar", "priorizacion:ver_logs",
        "ia:usar",
        "auditoria:ver",
    ],
    "TERAPEUTA": [
        "ninos:ver_propios",
        "terapias:ver",
        "citas:ver_propias",
        "sesiones:ver", "sesiones:crear", "sesiones:editar",
        "recursos:ver",
        "notificaciones:ver",
        "ia:usar",
    ],
    "PADRE": [
        "ninos:ver_propios",
        "citas:ver_propias",
        "recursos:ver",
        "notificaciones:ver",
    ],
}


def init_roles_permisos():
    """Inicializar roles y permisos del sistema"""
    db = SessionLocal()
    try:
        print("👥 Creando roles...")
        for rol_data in ROLES:
            rol = db.query(Rol).filter(Rol.id == rol_data["id"]).first()
            if not rol:
                rol = Rol(**rol_data)
                db.add(rol)
                print(f"  ➕ Rol creado: {rol_data['nombre']}")
            else:
                rol.nombre = rol_data["nombre"]
                rol.descripcion = rol_data["descripcion"]
                print(f"  ✏️  Rol actualizado: {rol_data['nombre']}")
        
        db.commit()
        
        print("\n🔐 Creando permisos...")
        permisos_map = {}
        for permiso_data in PERMISOS:
            permiso = db.query(Permiso).filter(Permiso.codigo == permiso_data["codigo"]).first()
            if not permiso:
                permiso = Permiso(**permiso_data)
                db.add(permiso)
                print(f"  ➕ {permiso_data['codigo']}")
            else:
                permiso.descripcion = permiso_data["descripcion"]
            
            permisos_map[permiso_data["codigo"]] = permiso
        
        db.commit()
        
        print("\n🔗 Asignando permisos a roles...")
        for rol_nombre, permisos_codigos in ROLE_PERMISOS.items():
            rol = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
            if not rol:
                print(f"  ⚠️  Rol no encontrado: {rol_nombre}")
                continue
            
            # Limpiar permisos existentes
            db.query(RolePermiso).filter(RolePermiso.role_id == rol.id).delete()
            
            # Agregar nuevos permisos
            count = 0
            for codigo in permisos_codigos:
                permiso = permisos_map.get(codigo)
                if permiso:
                    role_permiso = RolePermiso(role_id=rol.id, permiso_id=permiso.id)
                    db.add(role_permiso)
                    count += 1
            
            db.commit()
            print(f"  ✅ {rol_nombre}: {count} permisos asignados")
        
        print("\n✅ Roles y permisos inicializados correctamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("INICIALIZAR ROLES Y PERMISOS - Autismo Mochis IA")
    print("="*60 + "\n")
    init_roles_permisos()
    print("\n" + "="*60 + "\n")

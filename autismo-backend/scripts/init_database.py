"""
Script maestro para inicializar toda la base de datos.
Ejecuta en orden: catálogos -> roles/permisos -> usuarios demo
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from init_catalogos import init_catalogos
from init_roles_permisos import init_roles_permisos
from crear_usuarios_demo import crear_usuarios_demo


def init_database():
    """Inicializar toda la base de datos con datos predeterminados"""
    print("\n" + "="*70)
    print("🚀 INICIALIZACIÓN COMPLETA DE BASE DE DATOS - Autismo Mochis IA")
    print("="*70 + "\n")
    
    try:
        # Paso 1: Catálogos
        print("PASO 1/3: Inicializando catálogos...")
        print("-" * 70)
        init_catalogos()
        
        # Paso 2: Roles y Permisos
        print("\nPASO 2/3: Inicializando roles y permisos...")
        print("-" * 70)
        init_roles_permisos()
        
        # Paso 3: Usuarios Demo
        print("\nPASO 3/3: Creando usuarios demo...")
        print("-" * 70)
        crear_usuarios_demo()
        
        print("\n" + "="*70)
        print("✅ INICIALIZACIÓN COMPLETA EXITOSA")
        print("="*70)
        print("\n📋 RESUMEN:")
        print("  • Catálogos: ✅ Inicializados")
        print("  • Roles: ✅ 4 roles creados (ADMIN, COORDINADOR, TERAPEUTA, PADRE)")
        print("  • Permisos: ✅ 40+ permisos asignados")
        print("  • Usuarios: ✅ 4 usuarios demo creados")
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("  • admin@demo.com / 12345678")
        print("  • coordinador@demo.com / 12345678")
        print("  • terapeuta@demo.com / 12345678")
        print("  • padre@demo.com / 12345678")
        print("\n🌐 Puedes iniciar el backend con: uvicorn app.main:app --reload")
        print("="*70 + "\n")
        
    except Exception as e:
        print("\n" + "="*70)
        print(f"❌ ERROR EN INICIALIZACIÓN: {e}")
        print("="*70 + "\n")
        raise


if __name__ == "__main__":
    init_database()

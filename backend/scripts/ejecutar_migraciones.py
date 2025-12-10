#!/usr/bin/env python3
"""
Script para ejecutar migraciones SQL en la base de datos
"""
import mysql.connector
import os
from pathlib import Path


def ejecutar_script_sql(cursor, script_path: str, descripcion: str):
    """Ejecuta un script SQL desde un archivo"""
    print(f"\n🔧 {descripcion}...")
    print(f"   📄 Archivo: {os.path.basename(script_path)}")
    
    if not os.path.exists(script_path):
        print(f"   ❌ ERROR: Archivo no encontrado: {script_path}")
        return False
    
    try:
        # Leer contenido del archivo
        with open(script_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Dividir por punto y coma y ejecutar cada statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        for statement in statements:
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as e:
                    # Ignorar errores de "ya existe" o "no existe"
                    if 'already exists' in str(e).lower() or 'does not exist' in str(e).lower():
                        print(f"   ℹ️  Nota: {str(e)[:80]}...")
                    else:
                        raise
        
        print(f"   ✅ Completado exitosamente")
        return True
        
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False


def main():
    print("=" * 50)
    print("MIGRACIONES DE BASE DE DATOS")
    print("=" * 50)
    
    # Configuración
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Cambiar si tiene contraseña
        'database': 'autismo_mochis_ia'
    }
    
    # Rutas de scripts
    script_dir = Path(__file__).parent
    migration1 = script_dir / 'migrar_estados_y_tipo_sangre.sql'
    migration2 = script_dir / 'crear_tabla_fichas_emergencia.sql'
    
    try:
        # Conectar a la base de datos
        print(f"\n🔌 Conectando a la base de datos...")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   Database: {DB_CONFIG['database']}")
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print(f"   ✅ Conexión exitosa\n")
        
        # Ejecutar migraciones
        print("=" * 50)
        print("PASO 1: Migrar estados y tipo de sangre")
        print("=" * 50)
        result1 = ejecutar_script_sql(
            cursor, 
            str(migration1),
            "Eliminando BAJA_TEMPORAL y agregando tipo_sangre"
        )
        conn.commit()
        
        print("\n" + "=" * 50)
        print("PASO 2: Crear tabla fichas_emergencia")
        print("=" * 50)
        result2 = ejecutar_script_sql(
            cursor,
            str(migration2),
            "Creando tabla fichas_emergencia"
        )
        conn.commit()
        
        # Resumen
        print("\n" + "=" * 50)
        print("RESUMEN DE MIGRACIONES")
        print("=" * 50)
        print(f"Paso 1 (Estados): {'✅ OK' if result1 else '❌ FALLO'}")
        print(f"Paso 2 (Fichas):  {'✅ OK' if result2 else '❌ FALLO'}")
        print()
        
        if result1 and result2:
            print("✅ Todas las migraciones completadas exitosamente")
            
            # Mostrar estadísticas
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_ninos,
                    SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) as activos,
                    SUM(CASE WHEN estado = 'INACTIVO' THEN 1 ELSE 0 END) as inactivos
                FROM ninos
            """)
            stats = cursor.fetchone()
            
            print(f"\n📊 Estadísticas:")
            print(f"   Total niños: {stats[0]}")
            print(f"   Activos: {stats[1]}")
            print(f"   Inactivos: {stats[2]}")
            
            cursor.execute("SELECT COUNT(*) FROM fichas_emergencia")
            fichas_count = cursor.fetchone()[0]
            print(f"   Fichas de emergencia: {fichas_count}")
            
        else:
            print("❌ Algunas migraciones fallaron")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("\n🔌 Conexión cerrada")
        
    except mysql.connector.Error as e:
        print(f"\n❌ ERROR DE CONEXIÓN: {str(e)}")
        print("\nVerifique:")
        print("  - MySQL está corriendo")
        print("  - Las credenciales son correctas")
        print("  - La base de datos existe")
        return 1
    
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

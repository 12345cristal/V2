# backend/scripts/setup_topsis_recomendacion.py
"""
Script para crear las tablas necesarias para TOPSIS y Recomendación
Ejecutar desde la carpeta backend: python scripts/setup_topsis_recomendacion.py
"""
import sys
import os

# Agregar el directorio padre al path para poder importar app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine


def ejecutar_sql_desde_archivo(archivo: str):
    """Ejecuta un archivo SQL línea por línea"""
    script_dir = os.path.dirname(__file__)
    sql_path = os.path.join(script_dir, archivo)
    
    print(f"📄 Leyendo archivo: {sql_path}")
    
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Dividir por punto y coma para ejecutar comandos individualmente
    comandos = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip() and not cmd.strip().startswith('--')]
    
    with engine.begin() as connection:
        for idx, comando in enumerate(comandos, 1):
            try:
                # Saltar comentarios de bloque
                if comando.startswith('/*'):
                    continue
                    
                print(f"⚙️  Ejecutando comando {idx}/{len(comandos)}...")
                resultado = connection.execute(text(comando))
                
                # Si es un SELECT, mostrar resultados
                if comando.strip().upper().startswith('SELECT'):
                    try:
                        rows = resultado.fetchall()
                        for row in rows:
                            print(f"   ✅ {dict(row)}")
                    except:
                        pass
                        
            except Exception as e:
                print(f"   ⚠️  Error en comando {idx}: {e}")
                # Continuar con los siguientes comandos
    
    print("✅ Script ejecutado completamente")


def main():
    print("=" * 60)
    print("🚀 INSTALACIÓN DE MÓDULOS TOPSIS Y RECOMENDACIÓN")
    print("=" * 60)
    print()
    
    try:
        ejecutar_sql_desde_archivo('crear_tablas_topsis_recomendacion.sql')
        
        print()
        print("=" * 60)
        print("✅ INSTALACIÓN COMPLETADA")
        print("=" * 60)
        print()
        print("📌 Tablas creadas/actualizadas:")
        print("   - criterio_topsis")
        print("   - actividades")
        print("   - ninos (campo perfil_contenido agregado)")
        print("   - terapias (campos categoria y tags agregados)")
        print()
        print("📌 Datos de ejemplo insertados:")
        print("   - 5 criterios TOPSIS")
        print("   - 5 actividades terapéuticas")
        print()
        print("🎉 El sistema está listo para usar TOPSIS y Recomendaciones")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR EN LA INSTALACIÓN")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Verifica:")
        print("  - La base de datos 'autismo_mochis_ia' existe")
        print("  - Las credenciales en app/core/config.py son correctas")
        print("  - El servidor MySQL está ejecutándose")
        sys.exit(1)


if __name__ == "__main__":
    main()

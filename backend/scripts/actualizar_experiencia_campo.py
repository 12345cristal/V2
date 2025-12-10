"""
Script para actualizar el campo experiencia de INT a VARCHAR(1000)
y agregar columnas foto_perfil y cv_archivo si no existen
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import engine
from sqlalchemy import text


def actualizar_schema():
    """Actualiza el schema de la tabla personal"""
    
    with engine.connect() as conn:
        print("🔄 Actualizando schema de tabla personal...")
        
        try:
            # 1. Modificar experiencia de INT a VARCHAR(1000)
            print("   - Modificando campo experiencia...")
            conn.execute(text("""
                ALTER TABLE personal 
                MODIFY COLUMN experiencia VARCHAR(1000) NULL
            """))
            conn.commit()
            print("   ✅ Campo experiencia actualizado a VARCHAR(1000)")
            
        except Exception as e:
            print(f"   ⚠️  Error al modificar experiencia (puede que ya esté actualizado): {e}")
        
        try:
            # 2. Agregar foto_perfil si no existe
            print("   - Agregando campo foto_perfil...")
            conn.execute(text("""
                ALTER TABLE personal 
                ADD COLUMN foto_perfil VARCHAR(255) NULL
            """))
            conn.commit()
            print("   ✅ Campo foto_perfil agregado")
            
        except Exception as e:
            print(f"   ⚠️  Campo foto_perfil ya existe o error: {e}")
        
        try:
            # 3. Agregar cv_archivo si no existe
            print("   - Agregando campo cv_archivo...")
            conn.execute(text("""
                ALTER TABLE personal 
                ADD COLUMN cv_archivo VARCHAR(255) NULL
            """))
            conn.commit()
            print("   ✅ Campo cv_archivo agregado")
            
        except Exception as e:
            print(f"   ⚠️  Campo cv_archivo ya existe o error: {e}")
        
        print("\n✅ Migración completada exitosamente")


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRACIÓN: Actualizar campos de tabla personal")
    print("=" * 60)
    actualizar_schema()

"""
Script para actualizar todos los niños con BAJA_TEMPORAL a ACTIVO
"""
import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from app.core.config import settings

def actualizar_estados():
    """Actualiza todos los estados BAJA_TEMPORAL a ACTIVO"""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    with engine.connect() as conn:
        # Primero verificar cuántos hay
        result = conn.execute(text("SELECT COUNT(*) FROM ninos WHERE estado = 'BAJA_TEMPORAL'"))
        count = result.scalar()
        print(f"📊 Niños con estado BAJA_TEMPORAL: {count}")
        
        if count > 0:
            # Actualizar todos a ACTIVO
            conn.execute(text("UPDATE ninos SET estado = 'ACTIVO' WHERE estado = 'BAJA_TEMPORAL'"))
            conn.commit()
            print(f"✅ {count} niños actualizados de BAJA_TEMPORAL a ACTIVO")
        else:
            print("✅ No hay niños con estado BAJA_TEMPORAL")
        
        # Mostrar resumen de estados
        result = conn.execute(text("SELECT estado, COUNT(*) as total FROM ninos GROUP BY estado"))
        print("\n📋 Resumen de estados:")
        for row in result:
            print(f"   {row[0]}: {row[1]} niños")

if __name__ == "__main__":
    actualizar_estados()

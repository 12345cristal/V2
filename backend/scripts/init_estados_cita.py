# backend/scripts/init_estados_cita.py
"""
Script para poblar el catálogo de estados de citas
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        print("=" * 60)
        print("INICIALIZACIÓN DE ESTADOS DE CITAS")
        print("=" * 60)
        
        # Verificar si ya existen
        result = conn.execute(text("SELECT COUNT(*) as total FROM estado_cita"))
        count = result.fetchone()[0]
        
        if count == 0:
            print("\n[1/1] Insertando estados de citas...")
            conn.execute(text("""
                INSERT INTO estado_cita (id, codigo, nombre) VALUES
                (1, 'PROGRAMADA', 'Programada'),
                (2, 'REALIZADA', 'Realizada'),
                (3, 'CANCELADA', 'Cancelada')
            """))
            conn.commit()
            print("   ✓ 3 estados insertados")
        else:
            print(f"   ℹ Ya existen {count} estados de citas")
        
        # Mostrar resumen
        print("\n" + "=" * 60)
        print("ESTADOS DE CITAS DISPONIBLES")
        print("=" * 60)
        
        result = conn.execute(text("SELECT id, codigo, nombre FROM estado_cita ORDER BY id"))
        estados = result.fetchall()
        
        for estado in estados:
            print(f"  {estado[0]:>2}. {estado[1]:<15} - {estado[2]}")
        
        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA")
        print("=" * 60)


if __name__ == "__main__":
    main()

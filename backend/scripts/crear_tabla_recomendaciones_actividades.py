import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine
from sqlalchemy import text

print("=" * 80)
print("CREANDO TABLA recomendaciones_actividades")
print("=" * 80)

db = SessionLocal()

try:
    # Crear tabla recomendaciones_actividades
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS recomendaciones_actividades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nino_id INT NOT NULL,
        actividades_recomendadas JSON NOT NULL,
        explicacion_humana TEXT,
        metodo VARCHAR(50) DEFAULT 'contenido',
        fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        aplicada TINYINT DEFAULT 0,
        FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
        INDEX idx_nino_fecha (nino_id, fecha_generacion)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    db.execute(text(create_table_sql))
    db.commit()
    
    print("\n✓ Tabla recomendaciones_actividades creada exitosamente")
    
    # Verificar estructura
    print("\n=== ESTRUCTURA TABLA ===")
    result = db.execute(text("DESCRIBE recomendaciones_actividades"))
    for row in result:
        print(f"  {row[0]}: {row[1]}")
    
    print("\n✓ Tabla verificada correctamente")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    db.rollback()
finally:
    db.close()

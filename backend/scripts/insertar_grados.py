"""
Script para insertar grados académicos básicos
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import engine
from sqlalchemy import text


def insertar_grados():
    with engine.connect() as conn:
        print("📝 Insertando grados académicos...")
        
        try:
            conn.execute(text("""
                INSERT IGNORE INTO grado_academico (id, nombre) VALUES
                (1, 'Licenciatura'),
                (2, 'Maestría'),
                (3, 'Doctorado'),
                (4, 'Especialidad'),
                (5, 'Técnico'),
                (6, 'Preparatoria')
            """))
            conn.commit()
            print("✅ Grados académicos insertados")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    insertar_grados()

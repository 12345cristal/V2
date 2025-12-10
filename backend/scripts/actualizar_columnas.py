# backend/scripts/actualizar_columnas.py
"""
Script para agregar columnas necesarias a ninos y terapias
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

updates = [
    {
        'nombre': 'ninos - perfil_contenido',
        'sql': 'ALTER TABLE ninos ADD COLUMN perfil_contenido JSON'
    },
    {
        'nombre': 'terapias - categoria',
        'sql': 'ALTER TABLE terapias ADD COLUMN categoria VARCHAR(100)'
    },
    {
        'nombre': 'terapias - tags',
        'sql': 'ALTER TABLE terapias ADD COLUMN tags TEXT'
    }
]

with engine.begin() as connection:
    for update in updates:
        try:
            connection.execute(text(update['sql']))
            print(f"✅ Columna agregada: {update['nombre']}")
        except Exception as e:
            if 'Duplicate column' in str(e) or 'duplicate column' in str(e).lower():
                print(f"ℹ️  Columna ya existe: {update['nombre']}")
            else:
                print(f"❌ Error en {update['nombre']}: {e}")

print("\n🎉 Actualización de columnas completada")

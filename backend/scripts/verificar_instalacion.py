# backend/scripts/verificar_instalacion.py
"""
Verifica que todas las tablas y columnas del módulo TOPSIS/Recomendación existan
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

print("🔍 Verificando instalación del módulo TOPSIS y Recomendación...\n")

verificaciones = [
    {
        'nombre': 'Tabla criterio_topsis',
        'sql': 'SELECT COUNT(*) as total FROM criterio_topsis'
    },
    {
        'nombre': 'Tabla actividades',
        'sql': 'SELECT COUNT(*) as total FROM actividades'
    },
    {
        'nombre': 'Columna ninos.perfil_contenido',
        'sql': "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='autismo_mochis_ia' AND TABLE_NAME='ninos' AND COLUMN_NAME='perfil_contenido'"
    },
    {
        'nombre': 'Columna terapias.categoria',
        'sql': "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='autismo_mochis_ia' AND TABLE_NAME='terapias' AND COLUMN_NAME='categoria'"
    },
    {
        'nombre': 'Columna terapias.tags',
        'sql': "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='autismo_mochis_ia' AND TABLE_NAME='terapias' AND COLUMN_NAME='tags'"
    }
]

with engine.connect() as connection:
    for verif in verificaciones:
        try:
            result = connection.execute(text(verif['sql']))
            row = result.fetchone()
            count = row[0]
            
            if count > 0:
                print(f"✅ {verif['nombre']}: OK ({count} registro(s))")
            else:
                print(f"⚠️  {verif['nombre']}: Existe pero sin datos")
        except Exception as e:
            print(f"❌ {verif['nombre']}: NO ENCONTRADA")

print("\n🎉 Verificación completada")

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("\n=== TABLAS DE RECOMENDACIONES ===")
result = db.execute(text("SHOW TABLES LIKE 'recomendaciones%'"))
tables = [row[0] for row in result]
for t in tables:
    print(f"  ✓ {t}")

print("\n=== TABLAS DE PERFILES ===")
result = db.execute(text("SHOW TABLES LIKE 'perfil%'"))
tables = [row[0] for row in result]
for t in tables:
    print(f"  ✓ {t}")

print("\n=== RESUMEN DE DATOS ===")
ninos = db.execute(text("SELECT COUNT(*) FROM ninos")).scalar()
perfiles_ninos = db.execute(text("SELECT COUNT(*) FROM perfil_nino_vectorizado")).scalar()
actividades = db.execute(text("SELECT COUNT(*) FROM actividades")).scalar()
perfiles_act = db.execute(text("SELECT COUNT(*) FROM perfil_actividad_vectorizada")).scalar()

print(f"Niños totales: {ninos}")
print(f"Perfiles de niños: {perfiles_ninos}")
print(f"Actividades totales: {actividades}")
print(f"Perfiles de actividades: {perfiles_act}")

# Verificar estructura de tabla de recomendaciones
print("\n=== ESTRUCTURA recomendaciones_actividades ===")
result = db.execute(text("DESCRIBE recomendaciones_actividades"))
for row in result:
    print(f"  {row[0]}: {row[1]}")

db.close()
print("\n✓ Verificación completa")

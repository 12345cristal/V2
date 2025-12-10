import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()

try:
    print("\n=== TABLA recomendaciones ===")
    result = db.execute(text("DESCRIBE recomendaciones"))
    for row in result:
        print(f"  {row[0]}: {row[1]}")
except Exception as e:
    print(f"Error: {e}")

try:
    print("\n=== TABLA recomendacion_actividad ===")
    result = db.execute(text("DESCRIBE recomendacion_actividad"))
    for row in result:
        print(f"  {row[0]}: {row[1]}")
except Exception as e:
    print(f"Error: {e}")

db.close()

# backend/scripts/ejecutar_sql_recomendaciones.py
import pymysql
import sys

sys.path.insert(0, '.')
from app.core.config import settings

# Leer el archivo SQL
with open('scripts/crear_tablas_recomendaciones.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Conectar a la base de datos
conn = pymysql.connect(
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    charset='utf8mb4'
)

cursor = conn.cursor()

try:
    # Ejecutar cada statement
    statements = sql_content.split(';')
    for statement in statements:
        statement = statement.strip()
        if statement and not statement.startswith('--'):
            print(f"Ejecutando: {statement[:50]}...")
            cursor.execute(statement)
    
    conn.commit()
    print("✅ Tablas creadas exitosamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()

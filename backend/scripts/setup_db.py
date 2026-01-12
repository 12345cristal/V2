import mysql.connector
from pathlib import Path

# Configuración
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'autismo_mochis_ia'
}

def init_database():
    """Crea todas las tablas en MySQL."""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Leer el archivo SQL
        sql_file = Path(__file__).parent / "database" / "init.sql"
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Ejecutar las sentencias SQL
        for statement in sql_content.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Base de datos inicializada correctamente")
        
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")

if __name__ == "__main__":
    init_database()
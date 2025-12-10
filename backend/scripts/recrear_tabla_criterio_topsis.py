# backend/scripts/recrear_tabla_criterio_topsis.py
"""
Recrea la tabla criterio_topsis con la estructura correcta
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

print("🔄 Recreando tabla criterio_topsis...\n")

# Eliminar tabla si existe
with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS criterio_topsis"))
    print("✅ Tabla anterior eliminada")

# Crear tabla con estructura correcta
create_sql = """
CREATE TABLE criterio_topsis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    peso DECIMAL(5,4) NOT NULL DEFAULT 1.0000 COMMENT 'Peso del criterio (suma total debe ser 1.0)',
    tipo ENUM('beneficio', 'costo') NOT NULL DEFAULT 'beneficio' COMMENT 'beneficio: mayor es mejor, costo: menor es mejor',
    activo TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""

with engine.begin() as connection:
    connection.execute(text(create_sql))
    print("✅ Tabla criterio_topsis creada")

# Insertar criterios de ejemplo
criterios = [
    ("Severidad del diagnóstico", "Nivel de severidad según evaluación clínica (1-10)", 0.30, "beneficio"),
    ("Número de faltas", "Cantidad de sesiones perdidas en el último mes", 0.20, "costo"),
    ("Progreso terapéutico", "Avance medido en objetivos alcanzados (1-10)", 0.25, "beneficio"),
    ("Tiempo de espera", "Días desde última evaluación sin terapia", 0.15, "costo"),
    ("Riesgo de abandono", "Probabilidad de deserción (1-10)", 0.10, "beneficio")
]

with engine.begin() as connection:
    for i, (nombre, descripcion, peso, tipo) in enumerate(criterios, 1):
        sql = text("""
            INSERT INTO criterio_topsis (nombre, descripcion, peso, tipo, activo)
            VALUES (:nombre, :descripcion, :peso, :tipo, 1)
        """)
        
        connection.execute(sql, {
            'nombre': nombre,
            'descripcion': descripcion,
            'peso': peso,
            'tipo': tipo
        })
        print(f"✅ Criterio {i}: {nombre} (peso: {peso})")

print(f"\n🎉 Tabla criterio_topsis lista con {len(criterios)} criterios")

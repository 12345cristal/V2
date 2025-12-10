# backend/scripts/insertar_criterios_ejemplo.py
"""
Inserta los 5 criterios TOPSIS de ejemplo
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

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
            ON DUPLICATE KEY UPDATE
            descripcion = VALUES(descripcion),
            peso = VALUES(peso),
            tipo = VALUES(tipo)
        """)
        
        try:
            connection.execute(sql, {
                'nombre': nombre,
                'descripcion': descripcion,
                'peso': peso,
                'tipo': tipo
            })
            print(f"✅ Criterio {i}: {nombre} (peso: {peso})")
        except Exception as e:
            print(f"⚠️  Criterio {i}: {e}")

print(f"\n🎉 {len(criterios)} criterios insertados/actualizados")

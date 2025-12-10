# backend/scripts/crear_tabla_actividades.py
"""
Script para crear la tabla actividades
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.db.session import engine

sql = """
CREATE TABLE IF NOT EXISTS actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    objetivo TEXT,
    materiales TEXT,
    duracion_minutos INT DEFAULT 30,
    tags JSON,
    dificultad TINYINT DEFAULT 1 COMMENT '1=Bajo, 2=Medio, 3=Alto',
    area_desarrollo VARCHAR(100) COMMENT 'cognitivo, motor, lenguaje, social, emocional',
    activo TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_activo (activo),
    INDEX idx_area (area_desarrollo),
    INDEX idx_dificultad (dificultad)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
"""

with engine.begin() as connection:
    connection.execute(text(sql))
    print("✅ Tabla 'actividades' creada")

# Insertar datos de ejemplo
inserts = [
    """INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
    ('Reconocimiento de emociones', 'Actividad para identificar y nombrar emociones básicas usando tarjetas ilustradas', 'Desarrollar la inteligencia emocional y capacidad de reconocer estados de ánimo', 'Tarjetas con expresiones faciales, espejo, imágenes de situaciones', 30, JSON_ARRAY('emociones', 'social', 'expresión facial'), 1, 'emocional', 1)""",
    
    """INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
    ('Construcción con bloques', 'Ejercicio de motricidad fina mediante construcción de estructuras con bloques de madera', 'Mejorar coordinación óculo-manual y habilidades de planificación espacial', 'Bloques de madera de colores, plantillas de construcción', 45, JSON_ARRAY('motricidad', 'espacial', 'planificación'), 2, 'motor', 1)""",
    
    """INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
    ('Juego de roles', 'Simulación de situaciones cotidianas para practicar habilidades sociales', 'Desarrollar habilidades de comunicación y comprensión de roles sociales', 'Disfraces, objetos de la vida diaria, guiones de situaciones', 40, JSON_ARRAY('social', 'comunicación', 'juego simbólico'), 2, 'social', 1)""",
    
    """INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
    ('Secuencias lógicas', 'Ordenar tarjetas de secuencias temporales de actividades cotidianas', 'Fortalecer el pensamiento lógico y comprensión de causa-efecto', 'Tarjetas de secuencias, tablero magnético', 30, JSON_ARRAY('cognitivo', 'lógica', 'secuencias'), 1, 'cognitivo', 1)""",
    
    """INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
    ('Mímica y gestos', 'Expresión y comprensión de mensajes a través de gestos y mímica', 'Mejorar comunicación no verbal y expresión corporal', 'Tarjetas con acciones, espejo', 25, JSON_ARRAY('comunicación', 'expresión corporal', 'no verbal'), 1, 'lenguaje', 1)"""
]

with engine.begin() as connection:
    for i, insert_sql in enumerate(inserts, 1):
        try:
            connection.execute(text(insert_sql))
            print(f"✅ Actividad {i} insertada")
        except Exception as e:
            print(f"⚠️  Actividad {i} ya existe o error: {e}")

print("\n🎉 Tabla actividades lista con datos de ejemplo")

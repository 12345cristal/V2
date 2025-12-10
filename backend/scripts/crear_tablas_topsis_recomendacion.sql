-- Script SQL para crear tablas necesarias para TOPSIS y Recomendación
-- Sistema: Autismo Mochis IA
-- Base de datos: autismo_mochis_ia

USE autismo_mochis_ia;

-- ============================================================
-- TABLA: criterio_topsis
-- Almacena criterios configurables para análisis TOPSIS
-- ============================================================
CREATE TABLE IF NOT EXISTS criterio_topsis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    peso DECIMAL(5,4) NOT NULL DEFAULT 1.0,
    tipo ENUM('beneficio', 'costo') NOT NULL DEFAULT 'beneficio',
    activo TINYINT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- TABLA: actividades
-- Almacena actividades terapéuticas recomendables
-- ============================================================
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- MODIFICAR TABLA: ninos
-- Agregar campo perfil_contenido para recomendaciones
-- ============================================================
ALTER TABLE ninos 
ADD COLUMN IF NOT EXISTS perfil_contenido JSON COMMENT 'Perfil vectorizado para recomendaciones';

-- ============================================================
-- MODIFICAR TABLA: terapias
-- Agregar campos para recomendaciones basadas en contenido
-- ============================================================
ALTER TABLE terapias 
ADD COLUMN IF NOT EXISTS categoria VARCHAR(100) COMMENT 'Categoría de la terapia',
ADD COLUMN IF NOT EXISTS tags TEXT COMMENT 'JSON string con palabras clave';

-- ============================================================
-- DATOS DE EJEMPLO: criterio_topsis
-- Criterios comunes para priorización de niños
-- ============================================================
INSERT INTO criterio_topsis (nombre, descripcion, peso, tipo, activo) VALUES
('Severidad del diagnóstico', 'Nivel de gravedad del diagnóstico según especialista', 0.30, 'beneficio', 1),
('Faltas acumuladas', 'Número de inasistencias en el último mes', 0.20, 'costo', 1),
('Progreso terapéutico', 'Evaluación del avance en terapias (1-10)', 0.25, 'beneficio', 1),
('Tiempo en lista de espera', 'Días esperando asignación de terapia', 0.15, 'beneficio', 1),
('Riesgo de abandono', 'Probabilidad de abandonar el programa (1-10)', 0.10, 'costo', 1)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

-- ============================================================
-- DATOS DE EJEMPLO: actividades
-- Actividades terapéuticas de muestra
-- ============================================================
INSERT INTO actividades (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo) VALUES
(
    'Reconocimiento de emociones',
    'Actividad para identificar y nombrar emociones básicas usando tarjetas ilustradas',
    'Desarrollar la inteligencia emocional y capacidad de reconocer estados de ánimo',
    'Tarjetas con expresiones faciales, espejo, imágenes de situaciones',
    30,
    JSON_ARRAY('emociones', 'social', 'expresión facial'),
    1,
    'emocional',
    1
),
(
    'Construcción con bloques',
    'Ejercicio de motricidad fina mediante construcción de estructuras con bloques de madera',
    'Mejorar coordinación óculo-manual y habilidades de planificación espacial',
    'Bloques de madera de colores, plantillas de construcción',
    45,
    JSON_ARRAY('motricidad', 'espacial', 'planificación'),
    2,
    'motor',
    1
),
(
    'Juego de roles',
    'Simulación de situaciones cotidianas para practicar habilidades sociales',
    'Desarrollar habilidades de comunicación y comprensión de roles sociales',
    'Disfraces, objetos de la vida diaria, guiones de situaciones',
    40,
    JSON_ARRAY('social', 'comunicación', 'juego simbólico'),
    2,
    'social',
    1
),
(
    'Secuencias lógicas',
    'Ordenar tarjetas de secuencias temporales de actividades cotidianas',
    'Fortalecer el pensamiento lógico y comprensión de causa-efecto',
    'Tarjetas de secuencias, tablero magnético',
    30,
    JSON_ARRAY('cognitivo', 'lógica', 'secuencias'),
    1,
    'cognitivo',
    1
),
(
    'Mímica y gestos',
    'Expresión y comprensión de mensajes a través de gestos y mímica',
    'Mejorar comunicación no verbal y expresión corporal',
    'Tarjetas con acciones, espejo',
    25,
    JSON_ARRAY('comunicación', 'expresión corporal', 'no verbal'),
    1,
    'lenguaje',
    1
)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

-- ============================================================
-- VERIFICACIÓN
-- ============================================================
SELECT 'Tablas creadas/actualizadas correctamente' AS resultado;
SELECT COUNT(*) AS total_criterios FROM criterio_topsis;
SELECT COUNT(*) AS total_actividades FROM actividades;

-- Script de creación de tablas para sistema de recomendaciones inteligentes
-- Integra: Similitud de contenido + TOPSIS + Gemini

-- ============================================================
-- Tabla: perfil_nino_vectorizado
-- Almacena embeddings generados por Gemini del perfil completo del niño
-- ============================================================
CREATE TABLE IF NOT EXISTS perfil_nino_vectorizado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL UNIQUE,
    embedding JSON NOT NULL COMMENT 'Vector de embeddings de Gemini (array de floats)',
    edad INT,
    diagnosticos JSON COMMENT 'Array de diagnósticos: ["TEA", "TDAH"]',
    dificultades JSON COMMENT 'Array de dificultades identificadas',
    fortalezas JSON COMMENT 'Array de fortalezas identificadas',
    texto_perfil TEXT COMMENT 'Texto original usado para generar embedding',
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    INDEX idx_nino_perfil (nino_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Perfiles vectorizados de niños para recomendaciones basadas en contenido';


-- ============================================================
-- Tabla: perfil_actividad_vectorizada
-- Almacena embeddings de actividades terapéuticas
-- ============================================================
CREATE TABLE IF NOT EXISTS perfil_actividad_vectorizada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actividad_id INT NOT NULL UNIQUE,
    embedding JSON NOT NULL COMMENT 'Vector de embeddings de Gemini',
    areas_desarrollo JSON COMMENT 'Array de áreas: ["cognitivo", "motor"]',
    tags JSON COMMENT 'Tags de la actividad',
    nivel_dificultad SMALLINT DEFAULT 1 COMMENT '1=Bajo, 2=Medio, 3=Alto',
    texto_descripcion TEXT COMMENT 'Descripción completa usada para embedding',
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (actividad_id) REFERENCES actividades(id) ON DELETE CASCADE,
    INDEX idx_actividad_perfil (actividad_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Perfiles vectorizados de actividades para similitud de contenido';


-- ============================================================
-- Tabla: historial_progreso
-- Registra progreso del niño en actividades (para aprendizaje colaborativo)
-- ============================================================
CREATE TABLE IF NOT EXISTS historial_progreso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL,
    actividad_id INT NOT NULL,
    terapeuta_id INT NOT NULL,
    calificacion DECIMAL(3,2) COMMENT 'Calificación 1.0 - 5.0',
    notas_progreso TEXT COMMENT 'Notas del terapeuta sobre la sesión',
    fecha_sesion DATETIME NOT NULL,
    duracion_minutos INT,
    embedding_notas JSON COMMENT 'Embedding de las notas para análisis de similitud',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    FOREIGN KEY (actividad_id) REFERENCES actividades(id),
    FOREIGN KEY (terapeuta_id) REFERENCES personal(id),
    INDEX idx_nino_progreso (nino_id),
    INDEX idx_actividad_progreso (actividad_id),
    INDEX idx_fecha_sesion (fecha_sesion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Historial de progreso en actividades para análisis de efectividad';


-- ============================================================
-- Tabla: recomendaciones_actividades
-- Almacena recomendaciones generadas por el sistema
-- ============================================================
CREATE TABLE IF NOT EXISTS recomendaciones_actividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL,
    actividades_recomendadas JSON NOT NULL COMMENT 'Array de objetos con actividad_id, score, razon',
    explicacion_humana TEXT COMMENT 'Explicación generada por Gemini',
    metodo VARCHAR(50) DEFAULT 'contenido' COMMENT 'Método usado: contenido, colaborativo, hibrido',
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    aplicada TINYINT DEFAULT 0 COMMENT '0=No aplicada, 1=Aplicada',
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    INDEX idx_nino_recomendaciones (nino_id),
    INDEX idx_fecha_generacion (fecha_generacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Registro de recomendaciones de actividades generadas';


-- ============================================================
-- Tabla: asignaciones_terapeuta_topsis
-- Almacena resultados de selección de terapeuta usando TOPSIS
-- ============================================================
CREATE TABLE IF NOT EXISTS asignaciones_terapeuta_topsis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL,
    terapia_tipo VARCHAR(100) NOT NULL COMMENT 'Tipo de terapia: lenguaje, conductual, etc.',
    ranking_terapeutas JSON NOT NULL COMMENT 'Array ordenado con terapeuta_id, score, criterios',
    terapeuta_seleccionado_id INT,
    explicacion_seleccion TEXT COMMENT 'Explicación generada por Gemini',
    criterios_usados JSON COMMENT 'Criterios y pesos usados en TOPSIS',
    fecha_calculo DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT DEFAULT 1,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    FOREIGN KEY (terapeuta_seleccionado_id) REFERENCES personal(id),
    INDEX idx_nino_asignacion (nino_id),
    INDEX idx_terapeuta_asignacion (terapeuta_seleccionado_id),
    INDEX idx_fecha_calculo (fecha_calculo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Asignaciones de terapeutas calculadas con TOPSIS';


-- ============================================================
-- Verificación de instalación
-- ============================================================
SELECT 
    'perfil_nino_vectorizado' as tabla, 
    COUNT(*) as existe 
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_name = 'perfil_nino_vectorizado'

UNION ALL

SELECT 
    'perfil_actividad_vectorizada' as tabla, 
    COUNT(*) as existe 
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_name = 'perfil_actividad_vectorizada'

UNION ALL

SELECT 
    'historial_progreso' as tabla, 
    COUNT(*) as existe 
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_name = 'historial_progreso'

UNION ALL

SELECT 
    'recomendaciones_actividades' as tabla, 
    COUNT(*) as existe 
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_name = 'recomendaciones_actividades'

UNION ALL

SELECT 
    'asignaciones_terapeuta_topsis' as tabla, 
    COUNT(*) as existe 
FROM information_schema.tables 
WHERE table_schema = DATABASE() 
AND table_name = 'asignaciones_terapeuta_topsis';

-- ============================================================
-- SCRIPT DE INICIALIZACIÓN DE CATÁLOGOS DE TERAPIAS
-- ============================================================

USE autismo_mochis_ia;

-- ============================================================
-- TIPO DE TERAPIA
-- ============================================================
INSERT INTO tipo_terapia (codigo, nombre) VALUES
('LENGUAJE', 'Terapia de Lenguaje'),
('CONDUCTUAL', 'Terapia Conductual'),
('OCUPACIONAL', 'Terapia Ocupacional'),
('FISICA', 'Terapia Física'),
('ABA', 'Análisis Conductual Aplicado (ABA)'),
('SENSORIAL', 'Integración Sensorial'),
('COGNITIVA', 'Terapia Cognitiva'),
('SOCIAL', 'Habilidades Sociales'),
('PSICOLOGICA', 'Apoyo Psicológico'),
('ACADEMICA', 'Apoyo Académico')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- PRIORIDAD
-- ============================================================
INSERT INTO prioridad (codigo, nombre) VALUES
('URGENTE', 'Urgente'),
('ALTA', 'Alta'),
('MEDIA', 'Media'),
('BAJA', 'Baja')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- TERAPIAS DE EJEMPLO
-- ============================================================
INSERT INTO terapias (nombre, descripcion, tipo_id, duracion_minutos, objetivo_general, activo) VALUES
(
    'Terapia de Lenguaje Inicial',
    'Desarrollo de habilidades comunicativas básicas para niños con TEA',
    (SELECT id FROM tipo_terapia WHERE codigo = 'LENGUAJE'),
    45,
    'Mejorar la comunicación verbal y no verbal, desarrollar vocabulario funcional',
    1
),
(
    'ABA Intensivo',
    'Intervención conductual intensiva basada en principios ABA',
    (SELECT id FROM tipo_terapia WHERE codigo = 'ABA'),
    60,
    'Reducir conductas desafiantes y promover comportamientos adaptativos',
    1
),
(
    'Integración Sensorial',
    'Terapia para procesamiento sensorial y regulación',
    (SELECT id FROM tipo_terapia WHERE codigo = 'SENSORIAL'),
    45,
    'Mejorar el procesamiento sensorial y la autorregulación',
    1
),
(
    'Habilidades Sociales Grupales',
    'Desarrollo de competencias sociales en grupo',
    (SELECT id FROM tipo_terapia WHERE codigo = 'SOCIAL'),
    60,
    'Fomentar interacción social apropiada y trabajo en equipo',
    1
),
(
    'Terapia Ocupacional',
    'Desarrollo de habilidades para la vida diaria',
    (SELECT id FROM tipo_terapia WHERE codigo = 'OCUPACIONAL'),
    45,
    'Promover independencia en actividades cotidianas',
    1
)
ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion);

-- ============================================================
-- ESTADO DE CITA (si no existe)
-- ============================================================
INSERT INTO estado_cita (codigo, nombre) VALUES
('PROGRAMADA', 'Programada'),
('CONFIRMADA', 'Confirmada'),
('EN_PROCESO', 'En Proceso'),
('COMPLETADA', 'Completada'),
('CANCELADA', 'Cancelada'),
('NO_ASISTIO', 'No Asistió'),
('REPROGRAMADA', 'Reprogramada')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- NIVEL DE DIFICULTAD (para recursos/actividades)
-- ============================================================
INSERT INTO nivel_dificultad (codigo, nombre) VALUES
('BASICO', 'Básico'),
('INTERMEDIO', 'Intermedio'),
('AVANZADO', 'Avanzado')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- TIPO DE RECURSO
-- ============================================================
INSERT INTO tipo_recurso (codigo, nombre) VALUES
('ACTIVIDAD', 'Actividad'),
('EJERCICIO', 'Ejercicio'),
('JUEGO', 'Juego'),
('LECTURA', 'Material de Lectura'),
('VIDEO', 'Video Educativo'),
('EVALUACION', 'Evaluación'),
('TAREA', 'Tarea para Casa')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- CATEGORÍA DE RECURSO
-- ============================================================
INSERT INTO categoria_recurso (codigo, nombre) VALUES
('COMUNICACION', 'Comunicación'),
('MOTRICIDAD', 'Motricidad'),
('COGNITIVO', 'Desarrollo Cognitivo'),
('EMOCIONAL', 'Regulación Emocional'),
('SOCIAL', 'Habilidades Sociales'),
('AUTONOMIA', 'Autonomía Personal'),
('ACADEMICO', 'Académico'),
('SENSORIAL', 'Sensorial')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- ============================================================
-- NIVEL DE RECURSO
-- ============================================================
INSERT INTO nivel_recurso (codigo, nombre) VALUES
('INICIAL', 'Inicial'),
('BASICO', 'Básico'),
('INTERMEDIO', 'Intermedio'),
('AVANZADO', 'Avanzado')
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- Verificación
SELECT 'Catálogos de terapias inicializados correctamente' AS status;
SELECT COUNT(*) as total_tipos FROM tipo_terapia;
SELECT COUNT(*) as total_prioridades FROM prioridad;
SELECT COUNT(*) as total_terapias FROM terapias;

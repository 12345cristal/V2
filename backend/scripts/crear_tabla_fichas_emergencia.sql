-- Crear tabla fichas_emergencia
-- Ejecutar en MySQL

USE autismo_mochis_ia;

CREATE TABLE IF NOT EXISTS fichas_emergencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL UNIQUE,
    
    -- Información médica crítica
    tipo_sangre VARCHAR(10) COMMENT 'A+, B+, AB+, O+, A-, B-, AB-, O-',
    alergias TEXT COMMENT 'Alergias conocidas',
    condiciones_medicas TEXT COMMENT 'Condiciones médicas adicionales',
    medicamentos_actuales TEXT COMMENT 'Medicamentos que toma actualmente',
    
    -- Información de diagnóstico
    diagnostico_principal VARCHAR(255),
    diagnostico_detallado TEXT,
    
    -- Contactos de emergencia (principal)
    contacto_principal_nombre VARCHAR(200) NOT NULL,
    contacto_principal_relacion VARCHAR(100) COMMENT 'Padre, Madre, Tutor',
    contacto_principal_telefono VARCHAR(20) NOT NULL,
    contacto_principal_telefono_alt VARCHAR(20),
    
    -- Contacto de emergencia secundario
    contacto_secundario_nombre VARCHAR(200),
    contacto_secundario_relacion VARCHAR(100),
    contacto_secundario_telefono VARCHAR(20),
    
    -- Información médica adicional
    seguro_medico VARCHAR(200),
    numero_seguro VARCHAR(100),
    hospital_preferido VARCHAR(255),
    medico_tratante VARCHAR(200),
    telefono_medico VARCHAR(20),
    
    -- Instrucciones especiales
    instrucciones_emergencia TEXT,
    restricciones_alimenticias TEXT,
    
    -- Información de comportamiento crítica
    crisis_comunes TEXT COMMENT 'Tipos de crisis que puede presentar',
    como_calmar TEXT COMMENT 'Técnicas efectivas para calmarlo',
    trigger_points TEXT COMMENT 'Situaciones que desencadenan crisis',
    
    -- Control
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    creado_por_id INT,
    
    -- Foreign keys
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    FOREIGN KEY (creado_por_id) REFERENCES usuarios(id),
    
    INDEX idx_nino_id (nino_id),
    INDEX idx_activa (activa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Fichas de emergencia con información crítica de los niños';

-- Crear fichas de emergencia para todos los niños existentes
INSERT INTO fichas_emergencia (
    nino_id,
    tipo_sangre,
    diagnostico_principal,
    contacto_principal_nombre,
    contacto_principal_relacion,
    contacto_principal_telefono,
    activa
)
SELECT 
    n.id,
    n.tipo_sangre,
    nd.diagnostico_principal,
    COALESCE(t.nombre_completo, 'Sin especificar'),
    'Tutor',
    COALESCE(t.telefono, 'Sin teléfono'),
    TRUE
FROM ninos n
LEFT JOIN ninos_diagnostico nd ON n.id = nd.nino_id
LEFT JOIN tutores t ON n.tutor_id = t.id
WHERE NOT EXISTS (
    SELECT 1 FROM fichas_emergencia fe WHERE fe.nino_id = n.id
);

SELECT '✅ Tabla fichas_emergencia creada y poblada exitosamente' as resultado;
SELECT COUNT(*) as total_fichas FROM fichas_emergencia;

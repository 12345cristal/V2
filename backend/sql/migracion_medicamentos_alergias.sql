-- SQL Script para crear tablas de medicamentos y alergias
-- Ejecutar en phpmyadmin o MySQL

-- Tabla de Medicamentos
CREATE TABLE IF NOT EXISTS medicamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    frecuencia VARCHAR(100) NOT NULL,
    razon VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NULL,
    activo BOOLEAN DEFAULT TRUE NOT NULL,
    novedadReciente BOOLEAN DEFAULT FALSE NOT NULL,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    actualizado_por VARCHAR(100) NULL,
    notas TEXT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    INDEX idx_nino_id (nino_id),
    INDEX idx_activo (activo)
);

-- Tabla de Alergias
CREATE TABLE IF NOT EXISTS alergias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL,
    nombre VARCHAR(200) NOT NULL,
    severidad ENUM('leve', 'moderada', 'severa') NOT NULL DEFAULT 'leve',
    reaccion TEXT NOT NULL,
    tratamiento TEXT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    INDEX idx_nino_id (nino_id),
    INDEX idx_severidad (severidad)
);

-- Agregar columnas para ingreso de información si no existen
ALTER TABLE ninos ADD COLUMN IF NOT EXISTS cuatrimestre INT DEFAULT 1;
ALTER TABLE ninos ADD COLUMN IF NOT EXISTS fecha_ingreso DATETIME;

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_medicamentos_nino_activo ON medicamentos(nino_id, activo);
CREATE INDEX IF NOT EXISTS idx_alergias_nino ON alergias(nino_id);

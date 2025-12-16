-- ================================================================
-- MIGRACIÓN: Agregar campos de Google Calendar a tabla citas
-- Fecha: 16 de diciembre de 2025
-- Descripción: Extiende la tabla citas con integración de Google Calendar
-- ================================================================

USE autismo_mochis_ia;

-- Agregar columnas para Google Calendar
ALTER TABLE citas
ADD COLUMN IF NOT EXISTS google_event_id VARCHAR(255) NULL UNIQUE COMMENT 'ID del evento en Google Calendar',
ADD COLUMN IF NOT EXISTS google_calendar_link VARCHAR(500) NULL COMMENT 'URL del evento en Google Calendar',
ADD COLUMN IF NOT EXISTS sincronizado_calendar BOOLEAN DEFAULT FALSE COMMENT 'Indica si está sincronizado con Google Calendar',
ADD COLUMN IF NOT EXISTS fecha_sincronizacion DATETIME NULL COMMENT 'Última fecha de sincronización';

-- Agregar columnas de confirmación
ALTER TABLE citas
ADD COLUMN IF NOT EXISTS confirmada BOOLEAN DEFAULT FALSE COMMENT 'Confirmada por padre/tutor',
ADD COLUMN IF NOT EXISTS fecha_confirmacion DATETIME NULL COMMENT 'Fecha de confirmación';

-- Agregar columnas de cancelación
ALTER TABLE citas
ADD COLUMN IF NOT EXISTS cancelado_por INT NULL COMMENT 'ID del usuario que canceló',
ADD COLUMN IF NOT EXISTS fecha_cancelacion DATETIME NULL COMMENT 'Fecha de cancelación',
ADD COLUMN IF NOT EXISTS motivo_cancelacion TEXT NULL COMMENT 'Motivo de la cancelación';

-- Agregar columnas de auditoría
ALTER TABLE citas
ADD COLUMN IF NOT EXISTS creado_por INT NULL COMMENT 'ID del usuario creador',
ADD COLUMN IF NOT EXISTS fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS actualizado_por INT NULL COMMENT 'ID del usuario que actualizó',
ADD COLUMN IF NOT EXISTS fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Agregar índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_citas_google_event ON citas(google_event_id);
CREATE INDEX IF NOT EXISTS idx_citas_sincronizado ON citas(sincronizado_calendar);
CREATE INDEX IF NOT EXISTS idx_citas_confirmada ON citas(confirmada);
CREATE INDEX IF NOT EXISTS idx_citas_fecha_creacion ON citas(fecha_creacion);

-- Agregar foreign keys para auditoría
ALTER TABLE citas
ADD CONSTRAINT IF NOT EXISTS fk_citas_creado_por 
    FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE SET NULL,
ADD CONSTRAINT IF NOT EXISTS fk_citas_actualizado_por 
    FOREIGN KEY (actualizado_por) REFERENCES usuarios(id) ON DELETE SET NULL,
ADD CONSTRAINT IF NOT EXISTS fk_citas_cancelado_por 
    FOREIGN KEY (cancelado_por) REFERENCES usuarios(id) ON DELETE SET NULL;

-- Verificar estructura actualizada
DESCRIBE citas;

-- Mensaje de confirmación
SELECT '✅ Migración completada: Tabla citas extendida con Google Calendar' AS resultado;
SELECT 'Nuevos campos agregados:' AS info;
SELECT '- google_event_id' AS campo_1;
SELECT '- google_calendar_link' AS campo_2;
SELECT '- sincronizado_calendar' AS campo_3;
SELECT '- confirmada, cancelado_por, etc.' AS campo_4;

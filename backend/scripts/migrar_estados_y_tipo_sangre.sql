-- Migración: Eliminar BAJA_TEMPORAL y agregar tipo_sangre
-- Ejecutar en MySQL

USE autismo_mochis_ia;

-- 1. Agregar columna tipo_sangre si no existe
ALTER TABLE ninos 
ADD COLUMN IF NOT EXISTS tipo_sangre VARCHAR(10) NULL 
COMMENT 'Tipo de sangre: A+, B+, AB+, O+, A-, B-, AB-, O-'
AFTER curp;

-- 2. Convertir niños con BAJA_TEMPORAL a INACTIVO
UPDATE ninos 
SET estado = 'INACTIVO' 
WHERE estado = 'BAJA_TEMPORAL';

-- 3. Modificar el ENUM para eliminar BAJA_TEMPORAL
ALTER TABLE ninos 
MODIFY COLUMN estado ENUM('ACTIVO', 'INACTIVO') 
DEFAULT 'ACTIVO' 
NOT NULL;

-- 4. Verificar cambios
SELECT 
    COUNT(*) as total_ninos,
    SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) as activos,
    SUM(CASE WHEN estado = 'INACTIVO' THEN 1 ELSE 0 END) as inactivos,
    SUM(CASE WHEN tipo_sangre IS NOT NULL THEN 1 ELSE 0 END) as con_tipo_sangre
FROM ninos;

SELECT '✅ Migración completada exitosamente' as resultado;

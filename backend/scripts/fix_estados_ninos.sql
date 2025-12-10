-- Actualizar todos los estados BAJA_TEMPORAL a ACTIVO
UPDATE ninos SET estado = 'ACTIVO' WHERE estado = 'BAJA_TEMPORAL';

-- Ver resumen de estados
SELECT estado, COUNT(*) as total FROM ninos GROUP BY estado;

-- SQL: Datos de Prueba para Medicamentos y Alergias
-- Ejecutar después de la migración de tablas

-- Insertar medicamentos para cada niño activo
INSERT INTO medicamentos (nino_id, nombre, dosis, frecuencia, razon, fecha_inicio, activo, novedadReciente, actualizado_por) 
SELECT 
  ninos.id,
  'Metilfenidato',
  '10 mg',
  'Dos veces al día',
  'TDAH',
  DATE_SUB(CURDATE(), INTERVAL 30 DAY),
  TRUE,
  TRUE,
  'Coordinador Sistema'
FROM ninos 
WHERE ninos.estado = 'ACTIVO' AND ninos.id NOT IN (SELECT DISTINCT nino_id FROM medicamentos)
LIMIT 1;

-- Insertar más medicamentos
INSERT INTO medicamentos (nino_id, nombre, dosis, frecuencia, razon, fecha_inicio, activo, novedadReciente, actualizado_por) 
SELECT 
  ninos.id,
  'Fluoxetina',
  '20 mg',
  'Una vez al día',
  'Ansiedad',
  DATE_SUB(CURDATE(), INTERVAL 90 DAY),
  TRUE,
  FALSE,
  'Coordinador Sistema'
FROM ninos 
WHERE ninos.estado = 'ACTIVO' AND ninos.id NOT IN (SELECT DISTINCT nino_id FROM medicamentos WHERE nombre = 'Fluoxetina')
LIMIT 1;

-- Insertar alergias
INSERT INTO alergias (nino_id, nombre, severidad, reaccion, tratamiento) 
SELECT 
  ninos.id,
  'Penicilina',
  'severa',
  'Anafilaxia',
  'Evitar completamente. Usar alternativas como cefalosporinas.'
FROM ninos 
WHERE ninos.estado = 'ACTIVO' AND ninos.id NOT IN (SELECT DISTINCT nino_id FROM alergias WHERE nombre = 'Penicilina')
LIMIT 1;

-- Insertar más alergias
INSERT INTO alergias (nino_id, nombre, severidad, reaccion, tratamiento) 
SELECT 
  ninos.id,
  'Maní',
  'moderada',
  'Picazón en la boca, hinchazón de labios',
  'Evitar productos con maní'
FROM ninos 
WHERE ninos.estado = 'ACTIVO' AND ninos.id NOT IN (SELECT DISTINCT nino_id FROM alergias WHERE nombre = 'Maní')
LIMIT 1;

-- Insertar alergia leve
INSERT INTO alergias (nino_id, nombre, severidad, reaccion, tratamiento) 
SELECT 
  ninos.id,
  'Leche de vaca',
  'leve',
  'Molestias estomacales',
  'Considerar bebidas alternativas sin lactosa'
FROM ninos 
WHERE ninos.estado = 'ACTIVO' AND ninos.id NOT IN (SELECT DISTINCT nino_id FROM alergias WHERE nombre = 'Leche de vaca')
LIMIT 1;

-- Verificar datos insertados
SELECT 'Medicamentos totales:' as info, COUNT(*) as cantidad FROM medicamentos
UNION ALL
SELECT 'Alergias totales:', COUNT(*) FROM alergias;

-- Ver medicamentos por niño
SELECT 
  n.id,
  n.nombre as nino,
  COUNT(m.id) as medicamentos_count,
  SUM(CASE WHEN m.novedadReciente = TRUE THEN 1 ELSE 0 END) as medicamentos_nuevos
FROM ninos n
LEFT JOIN medicamentos m ON n.id = m.nino_id
WHERE n.estado = 'ACTIVO'
GROUP BY n.id;

-- Ver alergias por niño
SELECT 
  n.id,
  n.nombre as nino,
  COUNT(a.id) as alergias_count
FROM ninos n
LEFT JOIN alergias a ON n.id = a.nino_id
WHERE n.estado = 'ACTIVO'
GROUP BY n.id;

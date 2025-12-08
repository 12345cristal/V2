-- =============================================
-- COMPLETAR DATOS DE LOS 50 NIÑOS
-- Tablas relacionadas: diagnóstico, info_emocional, archivos
-- =============================================

-- 7. DIAGNÓSTICOS (ninos_diagnostico) - Uno por cada niño
INSERT INTO ninos_diagnostico (id, nino_id, diagnostico_principal, diagnostico_resumen, fecha_diagnostico, especialista, institucion)
VALUES
  (1, 1, 'Trastorno del Espectro Autista (TEA) - Nivel 2', 'Requiere apoyo sustancial', '2018-03-15', 'Dra. María López Hernández', 'Hospital Pediátrico de Sinaloa'),
  (2, 2, 'TEA - Nivel 1', 'Requiere apoyo', '2019-05-20', 'Dr. Carlos Ramírez Ortega', 'CRIT Sinaloa'),
  (3, 3, 'TEA - Nivel 2', 'Requiere apoyo sustancial', '2021-08-10', 'Dra. Ana Sofía García', 'Hospital Infantil de México'),
  (4, 4, 'TEA - Nivel 1', 'Requiere apoyo', '2019-11-12', 'Dr. Jorge Luis Martínez', 'Centro de Desarrollo Infantil'),
  (5, 5, 'TEA - Nivel 3', 'Requiere apoyo muy sustancial', '2017-06-08', 'Dra. Patricia Sánchez', 'IMSS'),
  (6, 6, 'TEA - Nivel 1', 'Requiere apoyo', '2022-09-14', 'Dr. Ricardo Torres', 'Clínica Pediátrica Los Mochis'),
  (7, 7, 'TEA - Nivel 2', 'Requiere apoyo sustancial', '2018-01-22', 'Dra. Elena Vargas', 'Hospital General'),
  (8, 8, 'TEA - Nivel 1', 'Requiere apoyo', '2019-07-30', 'Dr. Luis Miguel Pérez', 'Centro de Atención Infantil'),
  (9, 9, 'TEA - Nivel 2', 'Requiere apoyo sustancial', '2020-03-18', 'Dra. Mónica Delgado', 'Hospital Pediátrico'),
  (10, 10, 'TEA - Nivel 1', 'Requiere apoyo', '2021-11-05', 'Dr. Hugo Andrés Núñez', 'Clínica del Niño');

-- Continuar con los 40 restantes (simplificado - puedes expandir según necesites)
INSERT INTO ninos_diagnostico (nino_id, diagnostico_principal, diagnostico_resumen, fecha_diagnostico, especialista, institucion)
SELECT 
  n.id,
  CASE 
    WHEN n.id % 3 = 0 THEN 'TEA - Nivel 1'
    WHEN n.id % 3 = 1 THEN 'TEA - Nivel 2'
    ELSE 'TEA - Nivel 3'
  END,
  CASE 
    WHEN n.id % 3 = 0 THEN 'Requiere apoyo'
    WHEN n.id % 3 = 1 THEN 'Requiere apoyo sustancial'
    ELSE 'Requiere apoyo muy sustancial'
  END,
  DATE_ADD(n.fecha_nacimiento, INTERVAL FLOOR(1 + RAND() * 24) MONTH),
  CONCAT('Dr(a). ', SUBSTRING_INDEX(SUBSTRING_INDEX('Ana María|Carlos Luis|Jorge Alberto|Patricia Elena|Ricardo José', '|', FLOOR(1 + RAND() * 5)), '|', -1)),
  SUBSTRING_INDEX(SUBSTRING_INDEX('Hospital Pediátrico|CRIT Sinaloa|Centro de Desarrollo|IMSS|Clínica Infantil', '|', FLOOR(1 + RAND() * 5)), '|', -1)
FROM ninos n
WHERE n.id > 10 AND n.id <= 50;


-- 8. INFO EMOCIONAL (ninos_info_emocional) - Uno por cada niño
INSERT INTO ninos_info_emocional (nino_id, estimulos, calmantes, preferencias, no_tolera, palabras_clave, forma_comunicacion, nivel_comprension)
SELECT 
  n.id,
  'Música suave, luces tenues, texturas suaves',
  'Abrazos profundos, balanceo, música clásica',
  'Dinosaurios, trenes, bloques de construcción',
  'Ruidos fuertes, multitudes, cambios bruscos',
  'mamá, agua, más, no',
  CASE 
    WHEN n.id % 4 = 0 THEN 'Verbal con apoyo'
    WHEN n.id % 4 = 1 THEN 'Comunicación aumentativa (PECS)'
    WHEN n.id % 4 = 2 THEN 'Gestos y señas'
    ELSE 'Lenguaje verbal'
  END,
  CASE 
    WHEN n.id % 3 = 0 THEN 'ALTO'
    WHEN n.id % 3 = 1 THEN 'MEDIO'
    ELSE 'BAJO'
  END
FROM ninos n;


-- 9. ARCHIVOS (ninos_archivos) - Opcional, puede ser NULL
INSERT INTO ninos_archivos (nino_id, acta_url, curp_url, comprobante_url)
SELECT 
  n.id,
  CONCAT('https://storage.autismomochis.mx/actas/', n.id, '_acta.pdf'),
  CONCAT('https://storage.autismomochis.mx/curps/', n.id, '_curp.pdf'),
  CONCAT('https://storage.autismomochis.mx/comprobantes/', n.id, '_comprobante.pdf')
FROM ninos n;

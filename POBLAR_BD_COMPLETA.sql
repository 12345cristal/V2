-- ============================================================================
-- SCRIPT PARA POBLAR LA BASE DE DATOS CON DATOS COHERENTES Y RELACIONADOS
-- ============================================================================

-- Limpiar datos previos (opcional, comentar si no deseas eliminar)
-- DELETE FROM sesion;
-- DELETE FROM citas_calendario;
-- DELETE FROM terapias_nino;
-- DELETE FROM terapias_personal;

-- ============================================================================
-- 1. TIPOS DE TERAPIA
-- ============================================================================
INSERT INTO tipo_terapia (codigo, nombre) VALUES 
('LOGO', 'Logopedia'),
('OCUP', 'Terapia Ocupacional'),
('FISIO', 'Fisioterapia'),
('PSICO', 'Psicoterapia'),
('DESEN', 'Terapia del Desarrollo')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- ============================================================================
-- 2. TERAPIAS
-- ============================================================================
INSERT INTO terapias (nombre, descripcion, tipo_id, duracion_minutos, objetivo_general, categoria, tags, activo) VALUES
-- Logopedia
('Logopedia General', 'Terapia del lenguaje y comunicación', 1, 60, 'Mejorar habilidades del lenguaje', 'lenguaje', '["lenguaje","comunicación","dicción"]', 1),
('Dislexia - Lecto-escritura', 'Intervención en dificultades de lectura y escritura', 1, 60, 'Mejorar habilidades de lecto-escritura', 'lenguaje', '["lectura","escritura","dislexia"]', 1),
('Dyspraxia Verbal', 'Terapia para apraxia del habla', 1, 45, 'Mejorar coordinación motora del habla', 'lenguaje', '["habla","apraxia","motor"]', 1),

-- Terapia Ocupacional
('Terapia Ocupacional General', 'Desarrollo de habilidades motoras finas y gruesas', 2, 60, 'Desarrollar independencia en actividades cotidianas', 'motricidad', '["motricidad","independencia","actividades"]', 1),
('Integración Sensorial', 'Procesamiento sensorial y coordinación', 2, 50, 'Mejorar respuesta sensorial', 'sensorial', '["sensorial","coordinación","tactil"]', 1),
('Escritura y Motricidad Fina', 'Desarrollo de destreza escritora', 2, 45, 'Mejorar coordinación mano-ojo', 'motricidad', '["escritura","motricidad","destreza"]', 1),

-- Fisioterapia
('Fisioterapia General', 'Rehabilitación y fortalecimiento motor', 3, 60, 'Mejorar movilidad y fuerza', 'motor', '["movimiento","fortaleza","rehabilitación"]', 1),
('Marcha y Equilibrio', 'Terapia de marcha y equilibrio postural', 3, 50, 'Mejorar estabilidad y marcha', 'motor', '["equilibrio","marcha","postura"]', 1),

-- Psicoterapia
('Psicoterapia Infantil', 'Abordaje psicoterapéutico de problemas emocionales', 4, 60, 'Mejorar bienestar emocional', 'emocional', '["emoción","conducta","bienestar"]', 1),
('Terapia Cognitivo-Conductual', 'TCC aplicada a niños', 4, 60, 'Desarrollar estrategias de afrontamiento', 'cognitivo', '["cognición","conducta","pensamiento"]', 1),

-- Terapia del Desarrollo
('Atención Temprana', 'Intervención en primera infancia', 5, 45, 'Estimular desarrollo integral', 'desarrollo', '["estimulación","infantil","integral"]', 1),
('Desarrollo Cognitivo', 'Estimulación cognitiva y aprendizaje', 5, 50, 'Estimular habilidades cognitivas', 'cognitivo', '["cognitivo","aprendizaje","estimulación"]', 1);

-- ============================================================================
-- 3. PERSONAL (TERAPEUTAS) - Con especialidades coherentes
-- ============================================================================
INSERT INTO personal (nombres, apellido_paterno, apellido_materno, id_rol, rfc, curp, fecha_nacimiento, 
                      telefono_personal, correo_personal, especialidad_principal, especialidades, 
                      grado_academico, cedula_profesional, fecha_ingreso, estado_laboral, rating, total_pacientes) VALUES
-- Logopedas
('María', 'González', 'López', 3, 'MGO900815AAA', 'MGOL900815HDFNNN01', '1990-08-15', 
 '5551234001', 'maria.gonzalez@clinic.com', 'Logopedia', '["Logopedia","Dyspraxia","Dislexia"]', 
 'Licenciado en Logopedia', 'LOG-2015-001', '2018-01-15', 'ACTIVO', 5, 12),

('Carlos', 'Rodríguez', 'Martín', 3, 'CRM920510AAA', 'CRMD920510HDFNRN02', '1992-05-10', 
 '5551234002', 'carlos.rodriguez@clinic.com', 'Logopedia', '["Logopedia","Lecto-escritura"]', 
 'Licenciado en Logopedia', 'LOG-2016-002', '2018-06-01', 'ACTIVO', 4, 10),

-- Terapeutas Ocupacionales
('Alejandra', 'Ramírez', 'García', 3, 'ARA880320AAA', 'RAGA880320HDFRMN03', '1988-03-20', 
 '5551234003', 'alejandra.ramirez@clinic.com', 'Terapia Ocupacional', '["Terapia Ocupacional","Integración Sensorial","Motricidad Fina"]', 
 'Licenciado en Terapia Ocupacional', 'OCP-2014-003', '2017-02-15', 'ACTIVO', 5, 15),

('Diego', 'Hernández', 'Rojas', 3, 'DHR910705AAA', 'HERD910705HDFRNR04', '1991-07-05', 
 '5551234004', 'diego.hernandez@clinic.com', 'Terapia Ocupacional', '["Terapia Ocupacional","Escritura","Motricidad"]', 
 'Licenciado en Terapia Ocupacional', 'OCP-2017-004', '2019-03-01', 'ACTIVO', 4, 8),

-- Fisioterapeutas
('Elena', 'Martínez', 'Sánchez', 3, 'EMS850612AAA', 'MASE850612HDFSZN05', '1985-06-12', 
 '5551234005', 'elena.martinez@clinic.com', 'Fisioterapia', '["Fisioterapia","Marcha","Equilibrio"]', 
 'Licenciado en Fisioterapia', 'FIS-2013-005', '2016-08-15', 'ACTIVO', 5, 18),

('Fernando', 'López', 'Jiménez', 3, 'LJF930218AAA', 'LOJF930218HDFNRN06', '1993-02-18', 
 '5551234006', 'fernando.lopez@clinic.com', 'Fisioterapia', '["Fisioterapia","Rehabilitación","Fuerza"]', 
 'Licenciado en Fisioterapia', 'FIS-2018-006', '2020-01-15', 'ACTIVO', 4, 6),

-- Psicólogos/Psicoterapeuta
('Gabriela', 'Fernández', 'Cruz', 3, 'FCG880930AAA', 'FECG880930HDFNRR07', '1988-09-30', 
 '5551234007', 'gabriela.fernandez@clinic.com', 'Psicoterapia', '["Psicoterapia","TCC","Emocional"]', 
 'Licenciado en Psicología', 'PSI-2015-007', '2018-05-01', 'ACTIVO', 5, 14),

-- Especialista en Desarrollo
('Hugo', 'Torres', 'Domínguez', 3, 'TDH870411AAA', 'TODH870411HDFPRN08', '1987-04-11', 
 '5551234008', 'hugo.torres@clinic.com', 'Desarrollo Infantil', '["Atención Temprana","Estimulación","Cognitivo"]', 
 'Licenciado en Pedagogía Especial', 'PED-2014-008', '2017-09-15', 'ACTIVO', 5, 11);

-- ============================================================================
-- 4. NIÑOS (Pacientes)
-- ============================================================================
INSERT INTO ninos (nombres, apellido_paterno, apellido_materno, edad_actual, genero, fecha_nacimiento, 
                   estado, created_at, padres_tutores, diagnostico, derivado_por) VALUES
-- Grupo 1: Con necesidades de Logopedia
('Juan', 'Pérez', 'García', 6, 'M', '2019-09-15', 'ACTIVO', NOW(), 'Roberto Pérez, Ana García', 'Retraso en el lenguaje', 'Pediatra'),
('Lucía', 'Martínez', 'López', 7, 'F', '2018-10-22', 'ACTIVO', NOW(), 'Pedro Martínez, Rosa López', 'Dislexia', 'Escuela'),
('Manuel', 'González', 'Ruiz', 5, 'M', '2020-11-08', 'ACTIVO', NOW(), 'Miguel González, Laura Ruiz', 'Dislalia', 'Psicopedagogo'),

-- Grupo 2: Con necesidades de Terapia Ocupacional
('Sofia', 'Rodríguez', 'Fernández', 6, 'F', '2019-12-03', 'ACTIVO', NOW(), 'Francisco Rodríguez, Carmen Fernández', 'Dispraxia del desarrollo', 'Pediatra'),
('Pablo', 'García', 'Moreno', 7, 'M', '2018-08-14', 'ACTIVO', NOW(), 'Andrés García, Marta Moreno', 'Bajo tono muscular', 'Neuropediatra'),
('María', 'López', 'Hernández', 8, 'F', '2017-07-20', 'ACTIVO', NOW(), 'Carlos López, Susana Hernández', 'Dificultades motoras finas', 'Escuela'),

-- Grupo 3: Con necesidades de Fisioterapia
('David', 'Jiménez', 'Castro', 5, 'M', '2020-05-17', 'ACTIVO', NOW(), 'José Jiménez, Isabel Castro', 'Hipotonía', 'Fisioterapeuta'),
('Martina', 'Sánchez', 'Gómez', 6, 'F', '2019-06-28', 'ACTIVO', NOW(), 'Javier Sánchez, Elena Gómez', 'Espasticidad leve', 'Pediatra'),

-- Grupo 4: Con necesidades de Psicoterapia
('Alejandro', 'Díaz', 'Vega', 7, 'M', '2018-03-09', 'ACTIVO', NOW(), 'Rafael Díaz, Beatriz Vega', 'Ansiedad infantil', 'Psicólogo'),
('Natalia', 'Ramírez', 'Romero', 6, 'F', '2019-04-12', 'ACTIVO', NOW(), 'Raúl Ramírez, Patricia Romero', 'Déficit atencional', 'Escuela'),

-- Grupo 5: Con múltiples necesidades
('Jorge', 'Vargas', 'Núñez', 5, 'M', '2020-02-25', 'ACTIVO', NOW(), 'Enrique Vargas, Gabriela Núñez', 'TEA leve', 'Neuropediatra'),
('Cecilia', 'Flores', 'Delgado', 7, 'F', '2018-11-18', 'ACTIVO', NOW(), 'Eduardo Flores, Marcela Delgado', 'Desarrollo global atrasado', 'Pediatra');

-- ============================================================================
-- 5. ASIGNACIÓN DE TERAPIAS A PERSONAL (TerapiaPersonal)
-- ============================================================================
-- Logopedas con sus terapias
INSERT INTO terapias_personal (terapia_id, personal_id, activo) VALUES
(1, 1, 1), (2, 1, 1), (3, 1, 1),  -- María González -> Logopedia General, Dislexia, Dyspraxia
(1, 2, 1), (2, 2, 1),              -- Carlos Rodríguez -> Logopedia General, Dislexia

-- Terapeutas Ocupacionales con sus terapias
(4, 3, 1), (5, 3, 1), (6, 3, 1),  -- Alejandra Ramírez -> T.O. General, Integración Sensorial, Escritura
(4, 4, 1), (6, 4, 1),              -- Diego Hernández -> T.O. General, Escritura

-- Fisioterapeutas con sus terapias
(7, 5, 1), (8, 5, 1),              -- Elena Martínez -> Fisioterapia General, Marcha
(7, 6, 1), (8, 6, 1),              -- Fernando López -> Fisioterapia General, Marcha

-- Psicoterapeutas con sus terapias
(9, 7, 1), (10, 7, 1),             -- Gabriela Fernández -> Psicoterapia Infantil, TCC

-- Especialista en Desarrollo
(11, 8, 1), (12, 8, 1);            -- Hugo Torres -> Atención Temprana, Desarrollo Cognitivo

-- ============================================================================
-- 6. ASIGNACIÓN DE TERAPIAS A NIÑOS (TerapiaNino)
-- ============================================================================
-- Prioridad: 1=Urgente, 2=Normal, 3=Baja
-- Frecuencia en sesiones/semana

-- Juan Pérez: Logopedia General (Retraso del lenguaje)
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(1, 1, 1, 1, 2, NOW(), 1);  -- Con María González, 2 sesiones/semana

-- Lucía Martínez: Dislexia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(2, 2, 1, 2, 2, NOW(), 1);  -- Con María González, 2 sesiones/semana

-- Manuel González: Dislalia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(3, 1, 2, 2, 1, NOW(), 1);  -- Con Carlos Rodríguez, 1 sesión/semana

-- Sofía Rodríguez: Dispraxia -> T.O. General + Integración Sensorial
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(4, 4, 3, 1, 2, NOW(), 1),   -- T.O. General con Alejandra, 2 sesiones/semana
(4, 5, 3, 1, 1, NOW(), 1);   -- Integración Sensorial con Alejandra, 1 sesión/semana

-- Pablo García: Bajo tono muscular -> T.O. + Fisioterapia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(5, 4, 3, 1, 2, NOW(), 1),   -- T.O. General con Alejandra, 2 sesiones/semana
(5, 7, 5, 1, 2, NOW(), 1);   -- Fisioterapia General con Elena, 2 sesiones/semana

-- María López: Motricidad fina -> T.O. Escritura
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(6, 6, 4, 2, 1, NOW(), 1);   -- Escritura con Diego, 1 sesión/semana

-- David Jiménez: Hipotonía -> Fisioterapia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(7, 7, 5, 1, 2, NOW(), 1),   -- Fisioterapia General con Elena, 2 sesiones/semana
(7, 8, 5, 1, 1, NOW(), 1);   -- Marcha y Equilibrio con Elena, 1 sesión/semana

-- Martina Sánchez: Espasticidad leve -> Fisioterapia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(8, 8, 6, 2, 2, NOW(), 1);   -- Marcha y Equilibrio con Fernando, 2 sesiones/semana

-- Alejandro Díaz: Ansiedad infantil -> Psicoterapia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(9, 9, 7, 2, 1, NOW(), 1);   -- Psicoterapia Infantil con Gabriela, 1 sesión/semana

-- Natalia Ramírez: Déficit atencional -> TCC
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(10, 10, 7, 2, 2, NOW(), 1); -- TCC con Gabriela, 2 sesiones/semana

-- Jorge Vargas: TEA leve -> Desarrollo + Logopedia
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(11, 11, 8, 1, 2, NOW(), 1), -- Atención Temprana con Hugo, 2 sesiones/semana
(11, 1, 1, 1, 1, NOW(), 1);  -- Logopedia General con María, 1 sesión/semana

-- Cecilia Flores: Desarrollo atrasado -> Atención Temprana + Desarrollo Cognitivo
INSERT INTO terapias_nino (nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia_semana, fecha_asignacion, activo) VALUES
(12, 11, 8, 1, 2, NOW(), 1), -- Atención Temprana con Hugo, 2 sesiones/semana
(12, 12, 8, 1, 1, NOW(), 1); -- Desarrollo Cognitivo con Hugo, 1 sesión/semana

-- ============================================================================
-- RESUMEN
-- ============================================================================
-- ✓ 12 Niños con diagnósticos variados
-- ✓ 8 Terapeutas especializados
-- ✓ 12 Tipos de terapias coherentes
-- ✓ Asignaciones lógicas: cada terapeuta especializado en sus terapias
-- ✓ Niños asignados a terapeutas según especialidad
-- ✓ Datos listos para crear citas y sesiones desde el calendario

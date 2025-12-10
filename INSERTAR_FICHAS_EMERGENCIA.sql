-- ================================================================
-- INSERTAR FICHAS DE EMERGENCIA PARA TODOS LOS NIÑOS
-- ================================================================
-- INSTRUCCIONES:
-- 1. Abre http://localhost/phpmyadmin
-- 2. Selecciona la base de datos "autismo_mochis_ia"
-- 3. Haz clic en la pestaña "SQL"
-- 4. Copia TODO este contenido y pégalo
-- 5. Haz clic en "Continuar"
-- ================================================================

USE autismo_mochis_ia;

-- Ficha 1: Mateo García Rodríguez
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    1, 'O+', 'Penicilina, Polen', 'Asma leve controlado', 'Risperidona 0.5mg (1 vez al día)',
    'TEA Nivel 1 (Asperger)', 'Trastorno del Espectro Autista de soporte nivel 1. Dificultades en interacción social. Hipersensibilidad auditiva.',
    'María Rodríguez López', 'Madre', '6681234567', '6687654321',
    'Carlos García Pérez', 'Padre', '6681239999',
    'IMSS', '1234567890', 'Hospital General de Los Mochis', 'Dra. Ana Martínez', '6681112233',
    'En caso de crisis, hablar con voz calmada y suave. Evitar contacto físico. Llevar a espacio tranquilo sin ruidos fuertes.',
    'Sin lactosa. Evitar colorantes artificiales.',
    'Crisis por sobrecarga sensorial: ruidos fuertes, luces intermitentes, espacios muy concurridos',
    'Auriculares con cancelación de ruido, juguete fidget (spinner), contar hasta 10 respirando profundo',
    'Cambios bruscos de rutina, campanas/alarmas, gritos, multitudes',
    TRUE, 3
);

-- Ficha 2: Sofía López Martínez
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    2, 'A+', 'Ninguna conocida', 'Ninguna', 'Melatonina 3mg (antes de dormir)',
    'TEA Nivel 2', 'Trastorno del Espectro Autista de soporte nivel 2. Comunicación verbal limitada. Ecolalia frecuente.',
    'Laura Martínez Gómez', 'Madre', '6682345678', '6688765432',
    'Pedro López Sánchez', 'Padre', '6682340000',
    'Seguro Popular', '2345678901', 'Hospital Fátima', 'Dr. Roberto Flores', '6682223344',
    'Utilizar comunicación visual (PECS). Mantener contacto visual indirecto. Respetar su espacio personal de 1 metro.',
    'Dieta libre de gluten y caseína (GFCF). Evitar azúcares refinados.',
    'Crisis por frustración comunicativa: no poder expresar necesidades básicas (sed, hambre, baño)',
    'Tablero de comunicación con imágenes, abrazo de presión profunda (si lo acepta), música suave (canciones infantiles conocidas)',
    'No entender lo que quiere comunicar, presión para hablar, interrumpir sus rutinas',
    TRUE, 3
);

-- Ficha 3: Diego Hernández Castro
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    3, 'B+', 'Frutos secos (anafilaxia)', 'TDAH comórbido', 'Metilfenidato 10mg (desayuno), Risperidona 0.25mg (cena)',
    'TEA Nivel 1 + TDAH', 'TEA con TDAH. Alta impulsividad. Dificultad para seguir instrucciones secuenciales.',
    'Patricia Castro Morales', 'Madre', '6683456789', '6689876543',
    'Jorge Hernández Ruiz', 'Padre', '6683450001',
    'ISSSTE', '3456789012', 'Hospital del ISSSTE Los Mochis', 'Dr. Fernando Ríos', '6683334455',
    '¡IMPORTANTE! Porta EpiPen por alergia a frutos secos. En caso de contacto llamar inmediatamente al 911. Crisis de impulsividad: redirigir energía con actividad física.',
    'ALERGIA SEVERA: Nueces, almendras, cacahuates, avellanas. Verificar SIEMPRE etiquetas. Sin gluten.',
    'Crisis de frustración con conductas impulsivas: aventar objetos, golpear mesa, gritar',
    'Ejercicio físico (saltar, correr en círculos), pelota antiestrés, contar objetos de un color específico',
    'Esperas largas sin actividad, tareas muy largas, prohibiciones sin explicación',
    TRUE, 3
);

-- Ficha 4: Valentina Gómez Flores
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    4, 'AB+', 'Picadura de abeja (urticaria)', 'Hipotiroidismo controlado', 'Levotiroxina 25mcg (en ayunas)',
    'TEA Nivel 2', 'TEA nivel 2. Comunicación no verbal. Usa PECS. Hipersensibilidad táctil severa.',
    'Rosa Flores Delgado', 'Madre', '6684567890', '6680987654',
    'Manuel Gómez Torres', 'Padre', '6684560002',
    'Seguro Privado AXA', '4567890123', 'Hospital StarMédica', 'Dra. Carmen Vega', '6684445566',
    'NO tocar sin previo aviso. Usar contacto visual antes de acercarse. Evitar texturas ásperas. Permitir manipular objetos suaves.',
    'Texturas: evitar alimentos con grumos. Prefiere purés y líquidos. Sin picante.',
    'Crisis por sobrecarga táctil: roce accidental, etiquetas de ropa, texturas nuevas',
    'Manta de peso (5kg), masaje con presión profunda en brazos (solo si permite), burbuja de jabón para soplar',
    'Toques inesperados, ropa nueva sin lavar, texturas granuladas',
    TRUE, 3
);

-- Ficha 5: Santiago Pérez Ramírez
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    5, 'O-', 'Látex, Ibuprofeno', 'Epilepsia controlada (última crisis: 6 meses)', 'Ácido Valproico 250mg (cada 12 horas)',
    'TEA Nivel 3 + Epilepsia', 'TEA severo con epilepsia. Comunicación muy limitada. Movimientos estereotipados frecuentes.',
    'Elena Ramírez Ortiz', 'Madre', '6685678901', '6681098765',
    'Francisco Pérez Luna', 'Padre', '6685670003',
    'IMSS', '5678901234', 'Hospital General Los Mochis', 'Dr. Miguel Ángel Cota', '6685556677',
    '¡ALERTA EPILEPSIA! En caso de convulsión: acostar de lado, cronometrar, NO meter nada en boca. Llamar emergencia si dura >3min. Crisis autistas: NO restringir movimientos estereotipados.',
    'Dieta cetogénica supervisada. Sin azúcar. Horarios estrictos de comida.',
    'Crisis convulsivas (raras), crisis por restricción de estereotipias (aleteo de manos)',
    'Permitir aleteo libre, objeto giratorio (spinner grande), balanceo suave, música repetitiva',
    'Luces estroboscópicas, falta de sueño, impedir movimientos repetitivos',
    TRUE, 3
);

-- Ficha 6: Isabella Torres Mendoza
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    6, 'A-', 'Ácaros del polvo', 'Rinitis alérgica', 'Loratadina 5mg (1 vez al día)',
    'TEA Nivel 1', 'TEA leve. Intereses restrictivos intensos (dinosaurios). Memoria excepcional.',
    'Gabriela Mendoza Silva', 'Madre', '6686789012', '6682109876',
    'Alberto Torres Vargas', 'Padre', '6686780004',
    'Seguro Privado Monterrey', '6789012345', 'Hospital Ángeles Los Mochis', 'Dr. Luis Moreno', '6686667788',
    'Puede hablar extensamente sobre dinosaurios. No interrumpir abruptamente. Usar interés en dinosaurios para redirigir.',
    'Sin restricciones, pero prefiere alimentos beige (pan, pasta, pollo).',
    'Crisis por interrupción de monólogo especial, contradicción sobre hechos de dinosaurios',
    'Libro de dinosaurios, permitir hablar 5 minutos sobre tema favorito, dibujar dinosaurios',
    'Decir "ya cállate", corregir datos (aunque incorrectos), cambio de tema brusco',
    TRUE, 3
);

-- Ficha 7: Lucas Ramírez Vargas
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    7, 'B-', 'Ninguna', 'Estreñimiento crónico', 'Lactulosa 10ml (cada noche)',
    'TEA Nivel 2', 'TEA moderado. Ecolalia diferida. Rutinas rígidas. Ansiedad alta.',
    'Mariana Vargas Cruz', 'Madre', '6687890123', '6683210987',
    'Roberto Ramírez Díaz', 'Padre', '6687890005',
    'IMSS', '7890123456', 'Hospital IMSS Los Mochis', 'Dra. Sofía Gutiérrez', '6687778899',
    'Crisis de ansiedad: respirar en bolsa de papel, contar regresivo desde 20. Necesita predecir eventos: usar agenda visual.',
    'Dieta alta en fibra. Mucha agua. Evitar quesos y lácteos en exceso.',
    'Crisis de ansiedad por cambios no anticipados (maestro suplente, ruta diferente)',
    'Reloj visual de tiempo, agenda con pictogramas, frase repetitiva ("todo estará bien"), objeto de apego (peluche)',
    'Sorpresas, cambios sin aviso, promesas incumplidas',
    TRUE, 3
);

-- Ficha 8: Camila Fernández Ruiz
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    8, 'O+', 'Huevo (anafilaxia)', 'Dermatitis atópica', 'Hidrocortisona crema (aplicar 2 veces al día)',
    'TEA Nivel 1', 'TEA leve. Selectividad alimentaria extrema. Hipersensibilidad olfativa.',
    'Sandra Ruiz Morales', 'Madre', '6688901234', '6684321098',
    'Javier Fernández Castro', 'Padre', '6688900006',
    'Seguro Popular', '8901234567', 'Hospital General', 'Dr. Héctor Medina', '6688889900',
    '¡ALERGIA HUEVO! Porta EpiPen. Verificar TODOS los alimentos. Crisis olfativas: ventilar área, permitir salir del espacio.',
    'ALERGIA HUEVO (huevo, mayonesa, pastel, pan dulce). Solo acepta: arroz blanco, pollo hervido, manzana.',
    'Crisis por olores fuertes (perfumes, limpiadores, comida con ajo)',
    'Salir al aire libre, pañuelo con aroma familiar (vainilla), ventilador personal',
    'Perfumes, olores de cocina (cebolla, ajo), productos de limpieza',
    TRUE, 3
);

-- Ficha 9: Emiliano Castro Morales
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    9, 'A+', 'Ninguna', 'Trastorno del sueño', 'Ninguno actualmente',
    'TEA Nivel 2', 'TEA moderado. Comunicación gestual. Intereses sensoriales (luces, agua).',
    'Lorena Morales Gómez', 'Madre', '6689012345', '6685432109',
    'Eduardo Castro Pérez', 'Padre', '6689010007',
    'ISSSTE', '9012345678', 'Hospital ISSSTE', 'Dra. Patricia Herrera', '6689990011',
    'Fascinación por luces y agua. Supervisar cerca de fuentes. Crisis: ofrecer estímulo sensorial alternativo.',
    'Prefiere líquidos. Dificultad con sólidos. Dieta blanda.',
    'Crisis por falta de estímulo sensorial adecuado (aburrimiento sensorial)',
    'Lámpara de lava, botella sensorial con brillantina, juego de agua con colores',
    'Ambientes monótonos sin estímulos visuales',
    TRUE, 3
);

-- Ficha 10: Martina Díaz González
INSERT INTO fichas_emergencia (
    nino_id, tipo_sangre, alergias, condiciones_medicas, medicamentos_actuales,
    diagnostico_principal, diagnostico_detallado,
    contacto_principal_nombre, contacto_principal_relacion, contacto_principal_telefono, contacto_principal_telefono_alt,
    contacto_secundario_nombre, contacto_secundario_relacion, contacto_secundario_telefono,
    seguro_medico, numero_seguro, hospital_preferido, medico_tratante, telefono_medico,
    instrucciones_emergencia, restricciones_alimenticias,
    crisis_comunes, como_calmar, trigger_points,
    activa, creado_por_id
) VALUES (
    10, 'B+', 'Mariscos', 'Ninguna', 'Omega 3 (suplemento diario)',
    'TEA Nivel 1 (Asperger)', 'Síndrome de Asperger. Alto funcionamiento. Dificultad comprensión social.',
    'Claudia González Reyes', 'Madre', '6680123456', '6686543210',
    'Raúl Díaz Salazar', 'Padre', '6680120008',
    'Seguro Privado Mapfre', '0123456789', 'Hospital Privado Los Mochis', 'Dr. Arturo Beltrán', '6680001122',
    'Interpretación literal del lenguaje. Explicar sarcasmo/metáforas. Crisis por malentendidos sociales.',
    'Evitar mariscos (camarón, pulpo, pescado). Prefiere comida predecible.',
    'Crisis por no entender bromas, sarcasmo, o dobles sentidos',
    'Explicación clara y literal de la situación, lista escrita de reglas sociales, tiempo a solas',
    'Burlas, bromas sin explicación, exclusión social',
    TRUE, 3
);

-- Verificar inserción
SELECT COUNT(*) as total_fichas FROM fichas_emergencia WHERE activa = TRUE;
SELECT 
    fe.id,
    n.nombre,
    n.apellido_paterno,
    fe.tipo_sangre,
    fe.diagnostico_principal,
    fe.contacto_principal_nombre,
    fe.contacto_principal_telefono
FROM fichas_emergencia fe
INNER JOIN ninos n ON n.id = fe.nino_id
WHERE fe.activa = TRUE
ORDER BY fe.id;

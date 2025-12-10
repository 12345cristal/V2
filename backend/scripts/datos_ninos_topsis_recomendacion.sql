-- ============================================================
-- DATOS REALISTAS PARA SISTEMA TOPSIS Y RECOMENDACIÓN
-- Sistema: Autismo Mochis IA
-- 10 Niños con datos completos para análisis
-- ============================================================

USE autismo_mochis_ia;

-- ============================================================
-- INSERCIÓN DE 10 NIÑOS CON DATOS COMPLETOS
-- Incluye: datos personales + perfil_contenido para recomendaciones
-- ============================================================

INSERT INTO ninos (
    nombre, 
    apellido_paterno, 
    apellido_materno, 
    fecha_nacimiento, 
    sexo, 
    curp,
    direccion,
    diagnostico,
    alergias,
    medicamentos_actuales,
    escolar,
    padre,
    madre,
    contactos_emergencia,
    info_emocional,
    info_centro,
    perfil_contenido,
    estado,
    created_at
) VALUES 

-- ============================================================
-- NIÑO 1: Mateo Rodríguez García
-- Perfil: TEA Nivel 2, dificultades de comunicación verbal
-- ============================================================
(
    'Mateo',
    'Rodríguez',
    'García',
    '2018-03-15',
    'M',
    'ROGM180315HSLDRTA3',
    JSON_OBJECT(
        'calle', 'Av. Álvaro Obregón',
        'numero', '1234',
        'colonia', 'Centro',
        'municipio', 'Los Mochis',
        'codigoPostal', '81200'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 2',
        'fechaDiagnostico', '2020-05-10',
        'diagnosticosSecundarios', JSON_ARRAY('Trastorno del lenguaje expresivo'),
        'especialista', 'Dra. María Elena Soto',
        'institucion', 'Hospital Fátima'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Frutos secos',
        'ambiental', 'Polen'
    ),
    JSON_ARRAY(
        JSON_OBJECT('nombre', 'Risperidona', 'dosis', '0.5mg', 'horario', 'Cada 12 horas')
    ),
    JSON_OBJECT(
        'escuela', 'Jardín de Niños Mundo Feliz',
        'grado', 'Tercero de preescolar',
        'maestro', 'Profra. Claudia Hernández',
        'horarioClases', '8:00 AM - 12:00 PM',
        'adaptaciones', 'Apoyo de maestra sombra, tiempo extendido en actividades'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Jorge Luis Rodríguez Vega',
        'telefono', '6681234567',
        'correo', 'jorge.rodriguez@email.com',
        'ocupacion', 'Ingeniero Civil'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Patricia García Morales',
        'telefono', '6681234568',
        'correo', 'patricia.garcia@email.com',
        'ocupacion', 'Maestra de primaria'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Rosa María García Torres',
            'relacion', 'Abuela materna',
            'telefono', '6681234569'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Ruidos fuertes, cambios de rutina, espacios muy concurridos',
        'cosasQueCalman', 'Música suave, movimiento rítmico, abrazo firme',
        'preferenciasSensoriales', 'Texturas suaves, luces tenues, sonidos repetitivos',
        'cosasNoTolera', 'Etiquetas en la ropa, comidas con textura granulosa',
        'palabrasClave', 'pelota, dinosaurios, azul',
        'formaComunicacion', 'Gestos, palabras sueltas, PECS ocasional',
        'nivelComprension', 'MEDIO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-09-01',
        'terapias', JSON_OBJECT(
            'lenguaje', true,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', false
        ),
        'horariosTerapia', 'Lunes, Miércoles, Viernes 3:00-5:00 PM',
        'terapeutaAsignado', 'Lic. Carlos Méndez',
        'costoMensual', 4500.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 2 trastorno lenguaje expresivo',
        'areas_desarrollo', JSON_ARRAY('comunicacion', 'social', 'sensorial'),
        'preferencias', JSON_ARRAY('dinosaurios', 'pelota', 'musica', 'movimiento'),
        'dificultades', JSON_ARRAY('lenguaje verbal', 'cambios rutina', 'ruidos fuertes'),
        'nivel_funcional', 'medio',
        'edad', 6,
        'tags', JSON_ARRAY('TEA', 'comunicacion', 'lenguaje', 'sensorial', 'social', 'dinosaurios', 'pelota', 'ritmo')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 2: Sofía Martínez López
-- Perfil: TEA Nivel 1, alto funcionamiento, dificultad social
-- ============================================================
(
    'Sofía',
    'Martínez',
    'López',
    '2017-07-22',
    'F',
    'MALS170722MSLRPFA8',
    JSON_OBJECT(
        'calle', 'Blvd. Macario Gaxiola',
        'numero', '567',
        'colonia', 'Scally',
        'municipio', 'Los Mochis',
        'codigoPostal', '81223'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 1',
        'fechaDiagnostico', '2019-11-03',
        'diagnosticosSecundarios', JSON_ARRAY('Ansiedad social'),
        'especialista', 'Dr. Roberto Quintana',
        'institucion', 'Centro de Desarrollo Infantil'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Ninguna',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Miguel Hidalgo',
        'grado', 'Segundo de primaria',
        'maestro', 'Profra. Laura Sánchez',
        'horarioClases', '8:00 AM - 1:00 PM',
        'adaptaciones', 'Descansos sensoriales, trabajo en grupos pequeños'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Fernando Martínez Ruiz',
        'telefono', '6681345678',
        'correo', 'fernando.martinez@email.com',
        'ocupacion', 'Contador'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Ana López Pérez',
        'telefono', '6681345679',
        'correo', 'ana.lopez@email.com',
        'ocupacion', 'Psicóloga'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Carmen Ruiz de Martínez',
            'relacion', 'Abuela paterna',
            'telefono', '6681345680'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Interacción con desconocidos, trabajos en equipo, evaluaciones',
        'cosasQueCalman', 'Lectura, dibujo, tiempo a solas, naturaleza',
        'preferenciasSensoriales', 'Silencio, orden visual, colores pastel',
        'cosasNoTolera', 'Gritos, desorden, contacto físico no anticipado',
        'palabrasClave', 'libros, gatos, princesas, morado',
        'formaComunicacion', 'Lenguaje fluido pero formal, evita contacto visual',
        'nivelComprension', 'ALTO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-01-15',
        'terapias', JSON_OBJECT(
            'lenguaje', false,
            'conductual', true,
            'ocupacional', false,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Martes y Jueves 4:00-5:30 PM',
        'terapeutaAsignado', 'Lic. Sandra Flores',
        'costoMensual', 3500.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 1 alto funcionamiento ansiedad social',
        'areas_desarrollo', JSON_ARRAY('social', 'emocional', 'sensorial'),
        'preferencias', JSON_ARRAY('lectura', 'dibujo', 'gatos', 'princesas', 'naturaleza', 'orden'),
        'dificultades', JSON_ARRAY('interaccion social', 'trabajo equipo', 'contacto visual', 'ansiedad'),
        'nivel_funcional', 'alto',
        'edad', 7,
        'tags', JSON_ARRAY('TEA', 'alto funcionamiento', 'social', 'ansiedad', 'lectura', 'gatos', 'orden', 'emocional')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 3: Diego Ramírez Sánchez
-- Perfil: TEA Nivel 3, comunicación no verbal, alta sensibilidad
-- ============================================================
(
    'Diego',
    'Ramírez',
    'Sánchez',
    '2019-01-10',
    'M',
    'RASD190110HSLMNDA1',
    JSON_OBJECT(
        'calle', 'Calle Independencia',
        'numero', '890',
        'colonia', 'Flores Magón',
        'municipio', 'Los Mochis',
        'codigoPostal', '81210'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 3',
        'fechaDiagnostico', '2020-08-25',
        'diagnosticosSecundarios', JSON_ARRAY('Trastorno del procesamiento sensorial', 'Retraso del desarrollo motor'),
        'especialista', 'Dr. Javier Moreno',
        'institucion', 'CREE Los Mochis'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Gluten, lácteos',
        'ambiental', 'Perfumes fuertes'
    ),
    JSON_ARRAY(
        JSON_OBJECT('nombre', 'Melatonina', 'dosis', '3mg', 'horario', 'Antes de dormir')
    ),
    JSON_OBJECT(
        'escuela', 'CAM Los Mochis',
        'grado', 'Preescolar especial',
        'maestro', 'Profra. Mónica Castillo',
        'horarioClases', '9:00 AM - 12:30 PM',
        'adaptaciones', 'Programa individualizado, comunicación aumentativa, espacio sensorial'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Arturo Ramírez Beltrán',
        'telefono', '6681456789',
        'correo', 'arturo.ramirez@email.com',
        'ocupacion', 'Comerciante'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Gabriela Sánchez Villa',
        'telefono', '6681456790',
        'correo', 'gabriela.sanchez@email.com',
        'ocupacion', 'Ama de casa'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Sofía Ramírez Sánchez',
            'relacion', 'Hermana mayor',
            'telefono', '6681456791'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Luces brillantes, sonidos agudos, espacios nuevos, multitudes',
        'cosasQueCalman', 'Balanceo, objetos giratorios, agua, presión profunda',
        'preferenciasSensoriales', 'Movimiento vestibular, input propioceptivo, luz tenue',
        'cosasNoTolera', 'Cambios bruscos, espera, ropa ajustada',
        'palabrasClave', 'agua, gira, abrazo',
        'formaComunicacion', 'No verbal, gestos básicos, llanto cuando frustrado',
        'nivelComprension', 'BAJO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-02-20',
        'terapias', JSON_OBJECT(
            'lenguaje', true,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Lunes a Viernes 2:00-4:00 PM',
        'terapeutaAsignado', 'Lic. Miguel Ángel Torres',
        'costoMensual', 6500.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 3 no verbal trastorno procesamiento sensorial',
        'areas_desarrollo', JSON_ARRAY('comunicacion', 'sensorial', 'motricidad', 'conductual'),
        'preferencias', JSON_ARRAY('agua', 'balanceo', 'giro', 'presion', 'movimiento'),
        'dificultades', JSON_ARRAY('comunicacion verbal', 'sensibilidad sensorial', 'cambios', 'espera'),
        'nivel_funcional', 'bajo',
        'edad', 5,
        'tags', JSON_ARRAY('TEA', 'nivel 3', 'no verbal', 'sensorial', 'agua', 'movimiento', 'propioceptivo', 'vestibular')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 4: Valentina Flores Ortiz
-- Perfil: TEA Nivel 1, ecolalia, intereses restringidos intensos
-- ============================================================
(
    'Valentina',
    'Flores',
    'Ortiz',
    '2018-11-05',
    'F',
    'FOOV181105MSLRRL3',
    JSON_OBJECT(
        'calle', 'Av. Leyva Solano',
        'numero', '345',
        'colonia', 'Las Fuentes',
        'municipio', 'Los Mochis',
        'codigoPostal', '81249'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 1',
        'fechaDiagnostico', '2020-02-14',
        'diagnosticosSecundarios', JSON_ARRAY('Trastorno obsesivo-compulsivo'),
        'especialista', 'Dra. Carmen Leyva',
        'institucion', 'Clínica del Noroeste'
    ),
    JSON_OBJECT(
        'medicamentos', 'Penicilina',
        'alimentos', 'Ninguna',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Benito Juárez',
        'grado', 'Primero de primaria',
        'maestro', 'Prof. Luis González',
        'horarioClases', '8:00 AM - 12:30 PM',
        'adaptaciones', 'Pausas de regulación, incorporación de intereses especiales en tareas'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Ricardo Flores Medina',
        'telefono', '6681567890',
        'correo', 'ricardo.flores@email.com',
        'ocupacion', 'Médico'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Elena Ortiz Ramírez',
        'telefono', '6681567891',
        'correo', 'elena.ortiz@email.com',
        'ocupacion', 'Arquitecta'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'María Ortiz de Flores',
            'relacion', 'Abuela materna',
            'telefono', '6681567892'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Desviaciones de rutina, objetos fuera de lugar, número impar de cosas',
        'cosasQueCalman', 'Ordenar objetos por color/tamaño, contar, ver videos específicos',
        'preferenciasSensoriales', 'Simetría visual, patrones repetitivos, música clásica',
        'cosasNoTolera', 'Desorden, improvisación, alimentos mezclados',
        'palabrasClave', 'números, orden, colores, repetir',
        'formaComunicacion', 'Lenguaje fluido con ecolalia frecuente, repite frases de videos',
        'nivelComprension', 'ALTO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-08-10',
        'terapias', JSON_OBJECT(
            'lenguaje', true,
            'conductual', true,
            'ocupacional', false,
            'sensorial', false,
            'psicologia', true
        ),
        'horariosTerapia', 'Lunes, Miércoles, Viernes 3:30-5:00 PM',
        'terapeutaAsignado', 'Lic. Ana Beltrán',
        'costoMensual', 4000.00,
        'modalidadPago', 'Quincenal',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 1 ecolalia TOC intereses restringidos',
        'areas_desarrollo', JSON_ARRAY('comunicacion', 'conductual', 'emocional'),
        'preferencias', JSON_ARRAY('numeros', 'orden', 'colores', 'simetria', 'patrones', 'musica clasica'),
        'dificultades', JSON_ARRAY('rigidez rutinas', 'ecolalia', 'obsesiones', 'ansiedad cambios'),
        'nivel_funcional', 'alto',
        'edad', 6,
        'tags', JSON_ARRAY('TEA', 'ecolalia', 'TOC', 'numeros', 'orden', 'patrones', 'simetria', 'rigidez')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 5: Emiliano Castro Herrera
-- Perfil: TEA Nivel 2, hiperactividad, busca input sensorial
-- ============================================================
(
    'Emiliano',
    'Castro',
    'Herrera',
    '2017-04-18',
    'M',
    'CAHE170418HSLSRMA5',
    JSON_OBJECT(
        'calle', 'Calle Morelos',
        'numero', '678',
        'colonia', 'Centro',
        'municipio', 'Los Mochis',
        'codigoPostal', '81200'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 2',
        'fechaDiagnostico', '2019-06-30',
        'diagnosticosSecundarios', JSON_ARRAY('TDAH', 'Trastorno de integración sensorial'),
        'especialista', 'Dr. Héctor Villarreal',
        'institucion', 'Hospital General'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Colorantes artificiales',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(
        JSON_OBJECT('nombre', 'Metilfenidato', 'dosis', '10mg', 'horario', 'Por la mañana')
    ),
    JSON_OBJECT(
        'escuela', 'Primaria Revolución',
        'grado', 'Segundo de primaria',
        'maestro', 'Prof. Mario Ochoa',
        'horarioClases', '8:00 AM - 1:00 PM',
        'adaptaciones', 'Descansos motores frecuentes, escritorio con bandas elásticas, asiento dinámico'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Pablo Castro Núñez',
        'telefono', '6681678901',
        'correo', 'pablo.castro@email.com',
        'ocupacion', 'Electricista'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Diana Herrera Silva',
        'telefono', '6681678902',
        'correo', 'diana.herrera@email.com',
        'ocupacion', 'Enfermera'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Roberto Castro López',
            'relacion', 'Tío paterno',
            'telefono', '6681678903'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Actividades sedentarias prolongadas, espacios cerrados sin movimiento',
        'cosasQueCalman', 'Correr, saltar, trepar, apretar objetos, música con ritmo fuerte',
        'preferenciasSensoriales', 'Input propioceptivo intenso, movimiento constante, sabores fuertes',
        'cosasNoTolera', 'Estar sentado por mucho tiempo, actividades de precisión',
        'palabrasClave', 'corre, salta, fuerte, rápido',
        'formaComunicacion', 'Frases cortas, impetuoso, interrumpe frecuentemente',
        'nivelComprension', 'MEDIO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-03-05',
        'terapias', JSON_OBJECT(
            'lenguaje', false,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', false
        ),
        'horariosTerapia', 'Martes, Jueves, Sábado 3:00-4:30 PM',
        'terapeutaAsignado', 'Lic. Roberto Núñez',
        'costoMensual', 4200.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 2 TDAH trastorno integracion sensorial hiperactividad',
        'areas_desarrollo', JSON_ARRAY('conductual', 'sensorial', 'motricidad', 'atencion'),
        'preferencias', JSON_ARRAY('movimiento', 'correr', 'saltar', 'trepar', 'fuerza', 'ritmo'),
        'dificultades', JSON_ARRAY('atencion', 'hiperactividad', 'control impulsos', 'actividades sedentarias'),
        'nivel_funcional', 'medio',
        'edad', 7,
        'tags', JSON_ARRAY('TEA', 'TDAH', 'hiperactividad', 'movimiento', 'propioceptivo', 'sensorial', 'energia')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 6: Isabella Ruiz Medina
-- Perfil: TEA Nivel 1, hiperlexia, evita contacto físico
-- ============================================================
(
    'Isabella',
    'Ruiz',
    'Medina',
    '2018-09-12',
    'F',
    'RUMI180912MSLZDSB2',
    JSON_OBJECT(
        'calle', 'Blvd. Rosendo G. Castro',
        'numero', '1122',
        'colonia', 'Country',
        'municipio', 'Los Mochis',
        'codigoPostal', '81220'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 1',
        'fechaDiagnostico', '2020-10-05',
        'diagnosticosSecundarios', JSON_ARRAY('Hiperlexia'),
        'especialista', 'Dra. Verónica Salazar',
        'institucion', 'Centro Neurológico'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Ninguna',
        'ambiental', 'Pelo de animales'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Justo Sierra',
        'grado', 'Primero de primaria',
        'maestro', 'Profra. Beatriz Moreno',
        'horarioClases', '8:00 AM - 12:30 PM',
        'adaptaciones', 'Incorporación de lectura en todas las materias, respeto de espacio personal'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Manuel Ruiz Gutiérrez',
        'telefono', '6681789012',
        'correo', 'manuel.ruiz@email.com',
        'ocupacion', 'Abogado'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Lorena Medina Castro',
        'telefono', '6681789013',
        'correo', 'lorena.medina@email.com',
        'ocupacion', 'Diseñadora gráfica'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Andrea Ruiz Medina',
            'relacion', 'Hermana menor',
            'telefono', '6681789014'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Contacto físico no anticipado, ambientes ruidosos, juegos sin reglas claras',
        'cosasQueCalman', 'Leer en voz alta, escribir, escuchar audiolibros, estar sola',
        'preferenciasSensoriales', 'Espacio personal amplio, silencio, luz natural',
        'cosasNoTolera', 'Abrazos sorpresa, empujones, juegos físicos',
        'palabrasClave', 'lee, escribe, letras, historias',
        'formaComunicacion', 'Lenguaje avanzado para su edad, vocabulario extenso, tono formal',
        'nivelComprension', 'ALTO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-09-20',
        'terapias', JSON_OBJECT(
            'lenguaje', false,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Lunes y Jueves 4:00-5:30 PM',
        'terapeutaAsignado', 'Lic. Martha Villegas',
        'costoMensual', 3800.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 1 hiperlexia alto vocabulario',
        'areas_desarrollo', JSON_ARRAY('social', 'sensorial', 'emocional'),
        'preferencias', JSON_ARRAY('lectura', 'escritura', 'letras', 'historias', 'libros', 'silencio', 'soledad'),
        'dificultades', JSON_ARRAY('contacto fisico', 'juegos fisicos', 'ruido', 'interaccion no estructurada'),
        'nivel_funcional', 'alto',
        'edad', 6,
        'tags', JSON_ARRAY('TEA', 'hiperlexia', 'lectura', 'escritura', 'vocabulario', 'espacio personal', 'introversi')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 7: Santiago Vega Ramírez
-- Perfil: TEA Nivel 2, selectividad alimentaria severa
-- ============================================================
(
    'Santiago',
    'Vega',
    'Ramírez',
    '2019-06-20',
    'M',
    'VERS190620HSLGMNA9',
    JSON_OBJECT(
        'calle', 'Av. Gabriel Leyva',
        'numero', '2345',
        'colonia', 'Jardines del Country',
        'municipio', 'Los Mochis',
        'codigoPostal', '81223'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 2',
        'fechaDiagnostico', '2021-03-18',
        'diagnosticosSecundarios', JSON_ARRAY('Trastorno de la alimentación', 'Ansiedad generalizada'),
        'especialista', 'Dr. Alberto Mendoza',
        'institucion', 'Hospital Privado'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Mariscos',
        'ambiental', 'Ácaros del polvo'
    ),
    JSON_ARRAY(
        JSON_OBJECT('nombre', 'Sertralina', 'dosis', '25mg', 'horario', 'Por la mañana')
    ),
    JSON_OBJECT(
        'escuela', 'Jardín de Niños Gabriela Mistral',
        'grado', 'Tercero de preescolar',
        'maestro', 'Profra. Silvia Torres',
        'horarioClases', '8:30 AM - 12:00 PM',
        'adaptaciones', 'No presión para probar nuevos alimentos, permitir lunch traído de casa'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Rodrigo Vega Castillo',
        'telefono', '6681890123',
        'correo', 'rodrigo.vega@email.com',
        'ocupacion', 'Empresario'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Melissa Ramírez Acosta',
        'telefono', '6681890124',
        'correo', 'melissa.ramirez@email.com',
        'ocupacion', 'Nutrióloga'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Laura Vega Ramírez',
            'relacion', 'Hermana mayor',
            'telefono', '6681890125'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Nuevos alimentos, texturas desconocidas, olor a comida fuerte, hora de comer',
        'cosasQueCalman', 'Alimentos familiares color beige, rutina predecible, tablet durante comida',
        'preferenciasSensoriales', 'Texturas crujientes, temperaturas tibias, envases cerrados',
        'cosasNoTolera', 'Comidas mixtas, salsas, frutas con semillas',
        'palabrasClave', 'galletas, pan, nuggets, papas',
        'formaComunicacion', 'Frases cortas, palabra "no" muy frecuente con comida',
        'nivelComprension', 'MEDIO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-05-12',
        'terapias', JSON_OBJECT(
            'lenguaje', true,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Lunes, Miércoles, Viernes 2:30-4:30 PM',
        'terapeutaAsignado', 'Lic. Patricia Osuna',
        'costoMensual', 5000.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 2 trastorno alimentacion selectividad alimentaria ansiedad',
        'areas_desarrollo', JSON_ARRAY('sensorial', 'conductual', 'alimentacion', 'emocional'),
        'preferencias', JSON_ARRAY('galletas', 'pan', 'nuggets', 'papas', 'crujiente', 'beige'),
        'dificultades', JSON_ARRAY('alimentacion', 'texturas', 'nuevos alimentos', 'ansiedad comida'),
        'nivel_funcional', 'medio',
        'edad', 5,
        'tags', JSON_ARRAY('TEA', 'selectividad', 'alimentacion', 'sensorial', 'ansiedad', 'texturas', 'rutina')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 8: Camila Torres Jiménez
-- Perfil: TEA Nivel 1, masking social, agotamiento sensorial
-- ============================================================
(
    'Camila',
    'Torres',
    'Jiménez',
    '2016-12-03',
    'F',
    'TOJC161203MSLRRMA4',
    JSON_OBJECT(
        'calle', 'Calle Zaragoza',
        'numero', '456',
        'colonia', 'Solidaridad',
        'municipio', 'Los Mochis',
        'codigoPostal', '81208'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 1',
        'fechaDiagnostico', '2022-01-20',
        'diagnosticosSecundarios', JSON_ARRAY('Agotamiento autista', 'Depresión infantil'),
        'especialista', 'Dra. Claudia Ibarra',
        'institucion', 'Instituto de Salud Mental'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Ninguna',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Francisco I. Madero',
        'grado', 'Tercero de primaria',
        'maestro', 'Prof. Javier Ríos',
        'horarioClases', '7:30 AM - 1:30 PM',
        'adaptaciones', 'Espacio tranquilo disponible, reducción de trabajo en grupo, avisos anticipados'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Eduardo Torres Gómez',
        'telefono', '6681901234',
        'correo', 'eduardo.torres@email.com',
        'ocupacion', 'Gerente de ventas'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Daniela Jiménez Vargas',
        'telefono', '6681901235',
        'correo', 'daniela.jimenez@email.com',
        'ocupacion', 'Terapeuta ocupacional'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Mariana Torres Jiménez',
            'relacion', 'Hermana gemela',
            'telefono', '6681901236'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Expectativas sociales, días largos en escuela, eventos sociales grandes',
        'cosasQueCalman', 'Tiempo en su habitación, rutinas predecibles, naturaleza, animales',
        'preferenciasSensoriales', 'Mantas pesadas, luz tenue, aromas naturales',
        'cosasNoTolera', 'Cambios sin aviso, mentiras sociales, injusticias',
        'palabrasClave', 'descanso, sola, justa, animales',
        'formaComunicacion', 'Aparentemente típica en público, se derrumba en casa',
        'nivelComprension', 'ALTO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-10-08',
        'terapias', JSON_OBJECT(
            'lenguaje', false,
            'conductual', false,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Martes y Jueves 5:00-6:30 PM',
        'terapeutaAsignado', 'Psic. Andrea Morales',
        'costoMensual', 3200.00,
        'modalidadPago', 'Quincenal',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 1 masking agotamiento autista depresion',
        'areas_desarrollo', JSON_ARRAY('emocional', 'social', 'sensorial', 'autoestima'),
        'preferencias', JSON_ARRAY('soledad', 'naturaleza', 'animales', 'rutina', 'justicia', 'descanso'),
        'dificultades', JSON_ARRAY('masking social', 'agotamiento', 'sobrecarga sensorial', 'expectativas sociales'),
        'nivel_funcional', 'alto',
        'edad', 8,
        'tags', JSON_ARRAY('TEA', 'masking', 'agotamiento', 'sobrecarga', 'emocional', 'naturaleza', 'introspectiva')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 9: Lucas Pérez Salazar
-- Perfil: TEA Nivel 2, estereotipias motoras, ecolalia diferida
-- ============================================================
(
    'Lucas',
    'Pérez',
    'Salazar',
    '2018-05-25',
    'M',
    'PESL180525HSLRZCA7',
    JSON_OBJECT(
        'calle', 'Blvd. Antonio Rosales',
        'numero', '3456',
        'colonia', 'Las Palmas',
        'municipio', 'Los Mochis',
        'codigoPostal', '81240'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 2',
        'fechaDiagnostico', '2020-07-12',
        'diagnosticosSecundarios', JSON_ARRAY('Trastorno de movimientos estereotipados'),
        'especialista', 'Dr. Francisco Leyva',
        'institucion', 'Centro de Autismo del Noroeste'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Huevo',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Cristóbal Colón',
        'grado', 'Primero de primaria',
        'maestro', 'Profra. Rosa María López',
        'horarioClases', '8:00 AM - 12:30 PM',
        'adaptaciones', 'Permitir movimientos auto-regulatorios, breaks de movimiento, comunicación visual'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Miguel Pérez Ibarra',
        'telefono', '6682012345',
        'correo', 'miguel.perez@email.com',
        'ocupacion', 'Mecánico'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Karla Salazar Montes',
        'telefono', '6682012346',
        'correo', 'karla.salazar@email.com',
        'ocupacion', 'Secretaria'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'José Pérez Salazar',
            'relacion', 'Hermano menor',
            'telefono', '6682012347'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Transiciones, tiempos de espera, tareas con muchos pasos',
        'cosasQueCalman', 'Aleteo de manos, saltar, escuchar mismas frases, objetos brillantes',
        'preferenciasSensoriales', 'Movimientos repetitivos, estímulos visuales brillantes, input vestibular',
        'cosasNoTolera', 'Prohibición de estereotipias, silencio total, inmovilidad',
        'palabrasClave', 'salta, brilla, otra vez',
        'formaComunicacion', 'Ecolalia diferida de programas de TV, frases funcionales emergentes',
        'nivelComprension', 'MEDIO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-04-03',
        'terapias', JSON_OBJECT(
            'lenguaje', true,
            'conductual', true,
            'ocupacional', true,
            'sensorial', true,
            'psicologia', false
        ),
        'horariosTerapia', 'Lunes, Miércoles, Viernes 3:00-5:00 PM',
        'terapeutaAsignado', 'Lic. Fernando Osorio',
        'costoMensual', 4800.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 2 estereotipias motoras ecolalia diferida',
        'areas_desarrollo', JSON_ARRAY('comunicacion', 'motricidad', 'conductual', 'sensorial'),
        'preferencias', JSON_ARRAY('movimiento', 'saltar', 'aleteo', 'brillante', 'repeticion', 'TV'),
        'dificultades', JSON_ARRAY('transiciones', 'espera', 'comunicacion funcional', 'tareas complejas'),
        'nivel_funcional', 'medio',
        'edad', 6,
        'tags', JSON_ARRAY('TEA', 'estereotipias', 'ecolalia', 'movimiento', 'repeticion', 'vestibular', 'visual')
    ),
    'ACTIVO',
    NOW()
),

-- ============================================================
-- NIÑO 10: Renata Morales Cruz
-- Perfil: TEA Nivel 1, sinestesia, memoria visual excepcional
-- ============================================================
(
    'Renata',
    'Morales',
    'Cruz',
    '2017-10-08',
    'F',
    'MOCR171008MSLRRNA1',
    JSON_OBJECT(
        'calle', 'Av. Insurgentes',
        'numero', '789',
        'colonia', 'Primavera',
        'municipio', 'Los Mochis',
        'codigoPostal', '81215'
    ),
    JSON_OBJECT(
        'diagnosticoPrincipal', 'Trastorno del Espectro Autista Nivel 1',
        'fechaDiagnostico', '2020-09-15',
        'diagnosticosSecundarios', JSON_ARRAY('Sinestesia', 'Superdotación intelectual'),
        'especialista', 'Dra. Isabel Navarro',
        'institucion', 'Centro de Evaluación Neuropsicológica'
    ),
    JSON_OBJECT(
        'medicamentos', 'Ninguna',
        'alimentos', 'Ninguna',
        'ambiental', 'Ninguna'
    ),
    JSON_ARRAY(),
    JSON_OBJECT(
        'escuela', 'Primaria Octavio Paz',
        'grado', 'Segundo de primaria',
        'maestro', 'Profra. Gabriela Osuna',
        'horarioClases', '8:00 AM - 1:00 PM',
        'adaptaciones', 'Currículo enriquecido, proyectos independientes, uso de colores en materiales'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Alejandro Morales Vega',
        'telefono', '6682123456',
        'correo', 'alejandro.morales@email.com',
        'ocupacion', 'Ingeniero de sistemas'
    ),
    JSON_OBJECT(
        'nombreCompleto', 'Paulina Cruz Hernández',
        'telefono', '6682123457',
        'correo', 'paulina.cruz@email.com',
        'ocupacion', 'Artista plástica'
    ),
    JSON_ARRAY(
        JSON_OBJECT(
            'nombreCompleto', 'Valeria Morales Cruz',
            'relacion', 'Hermana mayor',
            'telefono', '6682123458'
        )
    ),
    JSON_OBJECT(
        'estimulosAnsiedad', 'Aburrimiento, tareas repetitivas, subestimación de capacidades',
        'cosasQueCalman', 'Pintar, resolver acertijos, asociar colores con conceptos, aprender cosas nuevas',
        'preferenciasSensoriales', 'Combinaciones específicas de colores, música armónica, simetría',
        'cosasNoTolera', 'Colores discordantes, monotonía, trabajos simples',
        'palabrasClave', 'colores, números tienen colores, aprendo, reto',
        'formaComunicacion', 'Lenguaje muy avanzado, conceptos abstractos, explica sus sinestesias',
        'nivelComprension', 'ALTO'
    ),
    JSON_OBJECT(
        'fechaIngreso', '2023-11-15',
        'terapias', JSON_OBJECT(
            'lenguaje', false,
            'conductual', false,
            'ocupacional', false,
            'sensorial', true,
            'psicologia', true
        ),
        'horariosTerapia', 'Jueves 4:30-6:00 PM',
        'terapeutaAsignado', 'Psic. Lucía Carrillo',
        'costoMensual', 2500.00,
        'modalidadPago', 'Mensual',
        'estado', 'ACTIVO'
    ),
    JSON_OBJECT(
        'diagnostico', 'TEA nivel 1 sinestesia superdotacion memoria visual excepcional',
        'areas_desarrollo', JSON_ARRAY('cognitivo', 'emocional', 'social', 'creatividad'),
        'preferencias', JSON_ARRAY('colores', 'pintura', 'acertijos', 'aprendizaje', 'retos', 'conceptos abstractos'),
        'dificultades', JSON_ARRAY('aburrimiento', 'tareas simples', 'frustracion con pares', 'expectativas sociales'),
        'nivel_funcional', 'alto',
        'edad', 7,
        'tags', JSON_ARRAY('TEA', 'sinestesia', 'superdotacion', 'colores', 'visual', 'creatividad', 'cognitivo')
    ),
    'ACTIVO',
    NOW()
);

-- ============================================================
-- VERIFICACIÓN DE INSERCIÓN
-- ============================================================
SELECT 
    COUNT(*) as total_ninos,
    SUM(CASE WHEN estado = 'ACTIVO' THEN 1 ELSE 0 END) as activos,
    MIN(fecha_nacimiento) as mas_grande,
    MAX(fecha_nacimiento) as mas_pequeno
FROM ninos;

-- ============================================================
-- VISTA DE PERFILES PARA RECOMENDACIONES
-- ============================================================
SELECT 
    id,
    nombre,
    apellido_paterno,
    TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) as edad,
    JSON_EXTRACT(diagnostico, '$.diagnosticoPrincipal') as diagnostico,
    JSON_EXTRACT(perfil_contenido, '$.nivel_funcional') as nivel_funcional,
    JSON_LENGTH(JSON_EXTRACT(perfil_contenido, '$.preferencias')) as num_preferencias,
    JSON_LENGTH(JSON_EXTRACT(perfil_contenido, '$.dificultades')) as num_dificultades
FROM ninos
WHERE estado = 'ACTIVO'
ORDER BY id;

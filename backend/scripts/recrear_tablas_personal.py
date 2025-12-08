# backend/scripts/recrear_tablas_personal.py
"""Script para eliminar y recrear las tablas personal y personal_horario"""
from sqlalchemy import text
from app.db.session import engine


def recrear_tablas():
    """Elimina y crea las tablas personal y personal_horario"""
    
    with engine.connect() as conn:
        print("Deshabilitando checks de foreign keys...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.commit()
        
        print("Eliminando tablas dependientes...")
        conn.execute(text("DROP TABLE IF EXISTS personal_perfil"))
        conn.execute(text("DROP TABLE IF EXISTS personal_horarios"))
        conn.execute(text("DROP TABLE IF EXISTS personal_horario"))
        conn.execute(text("DROP TABLE IF EXISTS personal"))
        conn.commit()
        print("✓ Tablas eliminadas")
        
        # SQL para crear tabla personal
        sql_personal = """
        CREATE TABLE personal (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombres VARCHAR(100) NOT NULL,
            apellido_paterno VARCHAR(100) NOT NULL,
            apellido_materno VARCHAR(100),
            id_usuario INT,
            id_rol INT NOT NULL,
            rfc VARCHAR(13) NOT NULL UNIQUE,
            curp VARCHAR(18) NOT NULL UNIQUE,
            fecha_nacimiento DATE NOT NULL,
            telefono_personal VARCHAR(10) NOT NULL,
            correo_personal VARCHAR(150) NOT NULL UNIQUE,
            calle VARCHAR(200),
            numero_exterior VARCHAR(10),
            numero_interior VARCHAR(10),
            colonia VARCHAR(100),
            ciudad VARCHAR(100),
            estado VARCHAR(100),
            codigo_postal VARCHAR(5),
            especialidad_principal VARCHAR(100),
            especialidades VARCHAR(500),
            grado_academico VARCHAR(100),
            cedula_profesional VARCHAR(20),
            fecha_ingreso DATE NOT NULL,
            estado_laboral ENUM('ACTIVO', 'VACACIONES', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
            experiencia INT DEFAULT 0,
            total_pacientes INT DEFAULT 0,
            sesiones_semana INT DEFAULT 0,
            rating INT DEFAULT 0,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_rol) REFERENCES roles(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # SQL para crear tabla personal_horario
        sql_horario = """
        CREATE TABLE personal_horario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_personal INT NOT NULL,
            dia_semana SMALLINT NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fin TIME NOT NULL,
            FOREIGN KEY (id_personal) REFERENCES personal(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        print("\nCreando tabla personal...")
        conn.execute(text(sql_personal))
        conn.commit()
        print("✓ Tabla personal creada")
        
        print("Creando tabla personal_horario...")
        conn.execute(text(sql_horario))
        conn.commit()
        print("✓ Tabla personal_horario creada")
        
        print("\nRehabilitando checks de foreign keys...")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
        
        # Insertar datos de prueba
        print("\nInsertando datos de prueba...")
        sql_datos = """
        INSERT INTO personal
          (id, id_usuario, id_rol, nombres, apellido_paterno, apellido_materno, 
           especialidad_principal, fecha_ingreso, estado_laboral, total_pacientes, 
           sesiones_semana, rating, rfc, curp, fecha_nacimiento, telefono_personal, 
           correo_personal, especialidades, grado_academico, experiencia)
        VALUES
          (1, 3, 2, 'María', 'González', 'López', 'Psicología', '2021-01-15', 'ACTIVO', 
           24, 18, 5, 'GONL900101AB3', 'GONL900101MDFNPR', '1990-01-01', '5551234567', 
           'maria.gonzalez@centro.com', 'Psicología Clínica, Terapia Cognitivo-Conductual', 
           'Maestría en Psicología Clínica', 8),
          
          (2, 4, 2, 'Juan', 'Ramírez', 'Sánchez', 'Psicopedagogía', '2021-03-10', 'ACTIVO', 
           20, 16, 5, 'RAMSJ850615DE', 'RAMSJ850615HDFRNN', '1985-06-15', '5552345678', 
           'juan.ramirez@centro.com', 'Psicopedagogía, Educación Especial', 
           'Licenciatura en Psicopedagogía', 12),
          
          (3, 5, 2, 'Ana', 'Martínez', 'Flores', 'Lenguaje', '2022-02-01', 'ACTIVO', 
           18, 14, 5, 'MARFA920320GH', 'MARFA920320MDFRLR', '1992-03-20', '5553456789', 
           'ana.martinez@centro.com', 'Terapia de Lenguaje, Comunicación', 
           'Licenciatura en Comunicación Humana', 6),
          
          (4, 6, 2, 'Carlos', 'Hernández', 'Pérez', 'Lenguaje', '2023-05-20', 'ACTIVO', 
           15, 12, 4, 'HERPC880710JK', 'HERPC880710HDFRRR', '1988-07-10', '5554567890', 
           'carlos.hernandez@centro.com', 'Audiología, Terapia de Lenguaje', 
           'Maestría en Audiología', 10),
          
          (5, 7, 2, 'Laura', 'López', 'García', 'Neuromotor', '2022-08-10', 'ACTIVO', 
           17, 15, 5, 'LOPL910525MN0', 'LOPL910525MDFRPR', '1991-05-25', '5555678901', 
           'laura.lopez@centro.com', 'Desarrollo Neuromotor, Integración Sensorial', 
           'Licenciatura en Terapia Física', 7),
          
          (6, 8, 2, 'Pedro', 'García', 'Morales', 'Neuromotor', '2023-01-05', 'ACTIVO', 
           16, 14, 4, 'GARP870412PQ5', 'GARP870412HDFRMR', '1987-04-12', '5556789012', 
           'pedro.garcia@centro.com', 'Terapia Ocupacional, Neuromotor', 
           'Licenciatura en Terapia Ocupacional', 9),
          
          (7, 9, 2, 'Sofia', 'Rodríguez', 'Vázquez', 'Fisioterapia', '2021-11-22', 'ACTIVO', 
           19, 16, 5, 'RODS930830ST9', 'RODS930830MDFDZF', '1993-08-30', '5557890123', 
           'sofia.rodriguez@centro.com', 'Fisioterapia Pediátrica, Rehabilitación', 
           'Licenciatura en Fisioterapia', 6),
          
          (8, 10, 2, 'Roberto', 'Sánchez', 'Torres', 'Fisioterapia', '2023-04-12', 'ACTIVO', 
           14, 12, 4, 'SANR860920VW1', 'SANR860920HDFRTR', '1986-09-20', '5558901234', 
           'roberto.sanchez@centro.com', 'Fisioterapia, Ortopedia', 
           'Maestría en Fisioterapia Pediátrica', 11),
          
          (9, 11, 2, 'Diana', 'Torres', 'Jiménez', 'Psicología', '2022-06-18', 'ACTIVO', 
           21, 17, 5, 'TORD940215YZ7', 'TORD940215MDFRRM', '1994-02-15', '5559012345', 
           'diana.torres@centro.com', 'Psicología Infantil, Terapia de Juego', 
           'Licenciatura en Psicología', 5),
          
          (10, 12, 2, 'Miguel', 'Jiménez', 'Castro', 'Psicopedagogía', '2022-09-30', 'ACTIVO', 
           18, 15, 5, 'JICM890605BC2', 'JICM890605HDFTGR', '1989-06-05', '5550123456', 
           'miguel.jimenez@centro.com', 'Psicopedagogía, Dificultades de Aprendizaje', 
           'Maestría en Psicopedagogía', 8)
        """
        
        conn.execute(text(sql_datos))
        conn.commit()
        print("✓ Datos de prueba insertados (10 terapeutas)")
        
        # Insertar horarios de ejemplo
        print("\nInsertando horarios de ejemplo...")
        sql_horarios = """
        INSERT INTO personal_horario (id_personal, dia_semana, hora_inicio, hora_fin)
        VALUES
          -- María González (id=1) - Lunes a Viernes 9:00-15:00
          (1, 1, '09:00:00', '15:00:00'),
          (1, 2, '09:00:00', '15:00:00'),
          (1, 3, '09:00:00', '15:00:00'),
          (1, 4, '09:00:00', '15:00:00'),
          (1, 5, '09:00:00', '15:00:00'),
          
          -- Juan Ramírez (id=2) - Lunes a Viernes 10:00-16:00
          (2, 1, '10:00:00', '16:00:00'),
          (2, 2, '10:00:00', '16:00:00'),
          (2, 3, '10:00:00', '16:00:00'),
          (2, 4, '10:00:00', '16:00:00'),
          (2, 5, '10:00:00', '16:00:00'),
          
          -- Ana Martínez (id=3) - Lunes, Miércoles, Viernes 8:00-14:00
          (3, 1, '08:00:00', '14:00:00'),
          (3, 3, '08:00:00', '14:00:00'),
          (3, 5, '08:00:00', '14:00:00'),
          
          -- Carlos Hernández (id=4) - Martes, Jueves 9:00-15:00
          (4, 2, '09:00:00', '15:00:00'),
          (4, 4, '09:00:00', '15:00:00'),
          
          -- Laura López (id=5) - Lunes a Viernes 7:00-13:00
          (5, 1, '07:00:00', '13:00:00'),
          (5, 2, '07:00:00', '13:00:00'),
          (5, 3, '07:00:00', '13:00:00'),
          (5, 4, '07:00:00', '13:00:00'),
          (5, 5, '07:00:00', '13:00:00')
        """
        
        conn.execute(text(sql_horarios))
        conn.commit()
        print("✓ Horarios de ejemplo insertados")
        
    print("\n¡Tablas recreadas exitosamente con datos de prueba!")


if __name__ == "__main__":
    recrear_tablas()

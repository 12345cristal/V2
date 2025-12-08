# backend/scripts/crear_tablas_personal.py
"""Script para crear las tablas personal y personal_horario"""
from sqlalchemy import text
from app.db.session import engine
from app.models import Personal, PersonalHorario


def crear_tablas():
    """Crea las tablas personal y personal_horario"""
    
    # SQL para crear tabla personal
    sql_personal = """
    CREATE TABLE IF NOT EXISTS personal (
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
    CREATE TABLE IF NOT EXISTS personal_horario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_personal INT NOT NULL,
        dia_semana SMALLINT NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        FOREIGN KEY (id_personal) REFERENCES personal(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    with engine.connect() as conn:
        print("Creando tabla personal...")
        conn.execute(text(sql_personal))
        conn.commit()
        print("✓ Tabla personal creada")
        
        print("Creando tabla personal_horario...")
        conn.execute(text(sql_horario))
        conn.commit()
        print("✓ Tabla personal_horario creada")
        
    print("\n¡Tablas creadas exitosamente!")


if __name__ == "__main__":
    crear_tablas()

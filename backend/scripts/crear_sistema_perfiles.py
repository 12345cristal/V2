"""
Script para crear la tabla personal_perfil y grado_academico
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import engine
from sqlalchemy import text


def crear_tablas_perfil():
    """Crea las tablas necesarias para el sistema de perfiles"""
    
    with engine.connect() as conn:
        print("🔄 Creando tablas para sistema de perfiles...")
        
        # 1. Crear tabla grado_academico
        try:
            print("\n   📚 Creando tabla grado_academico...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS grado_academico (
                    id TINYINT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL UNIQUE,
                    descripcion VARCHAR(255) NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            conn.commit()
            print("   ✅ Tabla grado_academico creada")
            
            # Insertar valores por defecto
            print("   📝 Insertando grados académicos por defecto...")
            conn.execute(text("""
                INSERT IGNORE INTO grado_academico (nombre, descripcion) VALUES
                ('Licenciatura', 'Título universitario de licenciatura'),
                ('Maestría', 'Título de posgrado maestría'),
                ('Doctorado', 'Título de posgrado doctorado'),
                ('Especialidad', 'Certificación de especialidad médica'),
                ('Técnico', 'Título técnico o TSU'),
                ('Preparatoria', 'Educación media superior')
            """))
            conn.commit()
            print("   ✅ Grados académicos insertados")
            
        except Exception as e:
            print(f"   ⚠️  Error con grado_academico: {e}")
        
        # 2. Crear tabla personal_perfil
        try:
            print("\n   👤 Creando tabla personal_perfil...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS personal_perfil (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    personal_id INT NOT NULL UNIQUE,
                    fecha_nacimiento DATE NULL,
                    grado_academico_id TINYINT NULL,
                    especialidades TEXT NULL,
                    rfc VARCHAR(13) NULL,
                    ine VARCHAR(18) NULL,
                    curp VARCHAR(18) NULL,
                    telefono_personal VARCHAR(20) NULL,
                    correo_personal VARCHAR(100) NULL,
                    domicilio_calle VARCHAR(100) NULL,
                    domicilio_colonia VARCHAR(100) NULL,
                    domicilio_cp VARCHAR(10) NULL,
                    domicilio_municipio VARCHAR(100) NULL,
                    domicilio_estado VARCHAR(100) NULL,
                    cv_url VARCHAR(255) NULL,
                    foto_url VARCHAR(255) NULL,
                    experiencia TEXT NULL,
                    FOREIGN KEY (personal_id) REFERENCES personal(id) ON DELETE CASCADE,
                    FOREIGN KEY (grado_academico_id) REFERENCES grado_academico(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            conn.commit()
            print("   ✅ Tabla personal_perfil creada")
            
        except Exception as e:
            print(f"   ⚠️  Error con personal_perfil: {e}")
        
        # 3. Crear directorios para archivos
        try:
            print("\n   📁 Creando directorios para archivos...")
            from pathlib import Path
            Path("static/fotos").mkdir(parents=True, exist_ok=True)
            Path("static/cv").mkdir(parents=True, exist_ok=True)
            print("   ✅ Directorios creados")
        except Exception as e:
            print(f"   ⚠️  Error creando directorios: {e}")
        
        print("\n✅ Configuración de perfiles completada exitosamente")


if __name__ == "__main__":
    print("=" * 70)
    print("CONFIGURACIÓN: Sistema de Perfiles de Personal")
    print("=" * 70)
    crear_tablas_perfil()

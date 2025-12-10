# backend/scripts/init_terapias_completo.py
"""
Script para poblar terapias y asignar terapeutas
Basado en las tuplas proporcionadas del sistema
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        print("=" * 60)
        print("INICIALIZACIÓN DE TERAPIAS Y ASIGNACIONES")
        print("=" * 60)
        
        # 1. CATÁLOGOS BÁSICOS - Tipos de Terapia
        print("\n[1/3] Insertando tipos de terapia...")
        
        # Verificar si ya existen
        result = conn.execute(text("SELECT COUNT(*) as total FROM tipo_terapia"))
        count = result.fetchone()[0]
        
        if count == 0:
            conn.execute(text("""
                INSERT INTO tipo_terapia (id, codigo, nombre) VALUES
                (1, 'LENGUAJE', 'Terapia de lenguaje'),
                (2, 'NEUROMOTOR', 'Terapia neuromotora'),
                (3, 'FISIOTERAPIA', 'Fisioterapia'),
                (4, 'PSICOLOGIA', 'Psicología'),
                (5, 'PSICOPEDAGOGIA', 'Psicopedagogía')
            """))
            conn.commit()
            print("   ✓ 5 tipos de terapia insertados")
        else:
            print(f"   ℹ Ya existen {count} tipos de terapia")
        
        # 2. TERAPIAS
        print("\n[2/3] Insertando terapias...")
        
        result = conn.execute(text("SELECT COUNT(*) as total FROM terapias"))
        count = result.fetchone()[0]
        
        if count == 0:
            conn.execute(text("""
                INSERT INTO terapias
                (id, nombre, descripcion, tipo_id, duracion_minutos, objetivo_general, activo)
                VALUES
                (1, 'Terapia de lenguaje individual', 
                 'Intervención en lenguaje y comunicación funcional para niñas y niños con TEA.', 
                 1, 45, 'Favorecer la comunicación funcional, comprensión y expresión oral.', 1),
                
                (2, 'Terapia neuromotora', 
                 'Sesiones orientadas al desarrollo de habilidades motoras gruesas y finas.', 
                 2, 45, 'Mejorar el control postural, coordinación y esquema corporal.', 1),
                
                (3, 'Fisioterapia infantil', 
                 'Trabajo fisioterapéutico enfocado en fortalecimiento y movilidad.', 
                 3, 45, 'Optimizar el movimiento y la independencia funcional.', 1),
                
                (4, 'Psicoterapia infantil', 
                 'Atención psicológica individual para niñas y niños.', 
                 4, 50, 'Favorecer la regulación emocional y el manejo de conducta.', 1),
                
                (5, 'Intervención psicopedagógica', 
                 'Apoyo psicopedagógico adaptado al estilo de aprendizaje.', 
                 5, 50, 'Acompañar el proceso académico y las habilidades de estudio.', 1)
            """))
            conn.commit()
            print("   ✓ 5 terapias insertadas")
        else:
            print(f"   ℹ Ya existen {count} terapias")
        
        # 3. ASIGNACIONES DE TERAPEUTAS A TERAPIAS
        print("\n[3/3] Asignando terapeutas a terapias...")
        
        result = conn.execute(text("SELECT COUNT(*) as total FROM terapias_personal"))
        count = result.fetchone()[0]
        
        if count == 0:
            conn.execute(text("""
                INSERT INTO terapias_personal (id, terapia_id, personal_id, activo)
                VALUES
                -- Terapia de lenguaje (ID 1) -> Personal IDs 3, 4
                (1, 1, 3, 1),
                (2, 1, 4, 1),
                
                -- Terapia neuromotora (ID 2) -> Personal IDs 5, 6
                (3, 2, 5, 1),
                (4, 2, 6, 1),
                
                -- Fisioterapia infantil (ID 3) -> Personal IDs 7, 8
                (5, 3, 7, 1),
                (6, 3, 8, 1),
                
                -- Psicoterapia infantil (ID 4) -> Personal IDs 1, 9
                (7, 4, 1, 1),
                (8, 4, 9, 1),
                
                -- Intervención psicopedagógica (ID 5) -> Personal IDs 2, 10
                (9, 5, 2, 1),
                (10, 5, 10, 1)
            """))
            conn.commit()
            print("   ✓ 10 asignaciones creadas (2 terapeutas por terapia)")
        else:
            print(f"   ℹ Ya existen {count} asignaciones")
        
        # RESUMEN
        print("\n" + "=" * 60)
        print("RESUMEN DE TERAPIAS Y ASIGNACIONES")
        print("=" * 60)
        
        result = conn.execute(text("""
            SELECT 
                t.id,
                t.nombre,
                tt.nombre as tipo,
                t.duracion_minutos,
                COUNT(tp.id) as total_terapeutas
            FROM terapias t
            LEFT JOIN tipo_terapia tt ON t.tipo_id = tt.id
            LEFT JOIN terapias_personal tp ON t.id = tp.terapia_id AND tp.activo = 1
            GROUP BY t.id, t.nombre, tt.nombre, t.duracion_minutos
            ORDER BY t.id
        """))
        
        terapias_info = result.fetchall()
        
        print(f"\n{'ID':<5} {'Terapia':<40} {'Tipo':<20} {'Duración':<10} {'Terapeutas'}")
        print("-" * 100)
        
        for terapia in terapias_info:
            print(f"{terapia[0]:<5} {terapia[1]:<40} {terapia[2]:<20} {terapia[3]:>3} min    {terapia[4]:>2}")
        
        # Detalle de asignaciones
        print("\n" + "=" * 60)
        print("DETALLE DE ASIGNACIONES")
        print("=" * 60)
        
        result = conn.execute(text("""
            SELECT 
                t.nombre as terapia,
                CONCAT(p.nombres, ' ', p.apellido_paterno, ' ', IFNULL(p.apellido_materno, '')) as terapeuta,
                p.especialidad_principal
            FROM terapias_personal tp
            JOIN terapias t ON tp.terapia_id = t.id
            JOIN personal p ON tp.personal_id = p.id
            WHERE tp.activo = 1
            ORDER BY t.id, p.id
        """))
        
        asignaciones = result.fetchall()
        
        terapia_actual = None
        for asig in asignaciones:
            if asig[0] != terapia_actual:
                print(f"\n📋 {asig[0]}")
                terapia_actual = asig[0]
            print(f"   👤 {asig[1]} - {asig[2]}")
        
        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)


if __name__ == "__main__":
    main()

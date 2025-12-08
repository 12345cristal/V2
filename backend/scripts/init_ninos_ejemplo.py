# scripts/init_ninos_ejemplo.py
"""
Script para crear niños de ejemplo en la base de datos
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from datetime import date, datetime
from app.db.session import SessionLocal
from app.models.nino import Nino
from app.models.tutor import Tutor


def crear_ninos_ejemplo():
    """Crea niños de ejemplo en la base de datos"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen niños
        ninos_existentes = db.query(Nino).count()
        if ninos_existentes > 0:
            print(f"✓ Ya existen {ninos_existentes} niños en la base de datos.")
            respuesta = input("¿Deseas agregar más niños de ejemplo? (s/n): ")
            if respuesta.lower() != 's':
                print("Operación cancelada.")
                return
        
        # Crear tutores de ejemplo si no existen
        tutores = []
        tutores_data = [
            {"nombre": "María", "apellido_paterno": "González", "apellido_materno": "López", 
             "telefono": "6681234567", "email": "maria.gonzalez@email.com"},
            {"nombre": "Juan", "apellido_paterno": "Pérez", "apellido_materno": "Martínez",
             "telefono": "6681234568", "email": "juan.perez@email.com"},
            {"nombre": "Ana", "apellido_paterno": "Ramírez", "apellido_materno": "Torres",
             "telefono": "6681234569", "email": "ana.ramirez@email.com"},
            {"nombre": "Carlos", "apellido_paterno": "Hernández", "apellido_materno": "Sánchez",
             "telefono": "6681234570", "email": "carlos.hernandez@email.com"},
            {"nombre": "Laura", "apellido_paterno": "Morales", "apellido_materno": "Castro",
             "telefono": "6681234571", "email": "laura.morales@email.com"},
        ]
        
        for tutor_data in tutores_data:
            # Verificar si el tutor ya existe por email
            tutor_existente = db.query(Tutor).filter(Tutor.email == tutor_data["email"]).first()
            if tutor_existente:
                tutores.append(tutor_existente)
            else:
                tutor = Tutor(**tutor_data)
                db.add(tutor)
                db.flush()
                tutores.append(tutor)
        
        db.commit()
        print(f"✓ Tutores creados/verificados: {len(tutores)}")
        
        # Crear niños de ejemplo
        ninos_data = [
            {
                "nombre": "Miguel Ángel",
                "apellido_paterno": "González",
                "apellido_materno": "López",
                "fecha_nacimiento": date(2018, 3, 15),
                "sexo": "M",
                "curp": "GOLM180315HSINPG01",
                "tutor_id": tutores[0].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Sofía",
                "apellido_paterno": "Pérez",
                "apellido_materno": "Martínez",
                "fecha_nacimiento": date(2017, 7, 22),
                "sexo": "F",
                "curp": "PEMS170722MSIRRF02",
                "tutor_id": tutores[1].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Diego",
                "apellido_paterno": "Ramírez",
                "apellido_materno": "Torres",
                "fecha_nacimiento": date(2019, 1, 10),
                "sexo": "M",
                "curp": "RATD190110HSIMRG03",
                "tutor_id": tutores[2].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Valeria",
                "apellido_paterno": "Hernández",
                "apellido_materno": "Sánchez",
                "fecha_nacimiento": date(2016, 11, 5),
                "sexo": "F",
                "curp": "HESV161105MSIRRL04",
                "tutor_id": tutores[3].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Emiliano",
                "apellido_paterno": "Morales",
                "apellido_materno": "Castro",
                "fecha_nacimiento": date(2020, 4, 18),
                "sexo": "M",
                "curp": "MOCE200418HSINMS05",
                "tutor_id": tutores[4].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Camila",
                "apellido_paterno": "González",
                "apellido_materno": "Ruiz",
                "fecha_nacimiento": date(2018, 9, 30),
                "sexo": "F",
                "curp": "GORC180930MSINMM06",
                "tutor_id": tutores[0].id,
                "estado": "BAJA_TEMPORAL"
            },
            {
                "nombre": "Mateo",
                "apellido_paterno": "López",
                "apellido_materno": "García",
                "fecha_nacimiento": date(2017, 2, 14),
                "sexo": "M",
                "curp": "LOGM170214HSINPT07",
                "tutor_id": tutores[1].id,
                "estado": "ACTIVO"
            },
            {
                "nombre": "Isabella",
                "apellido_paterno": "Martínez",
                "apellido_materno": "Flores",
                "fecha_nacimiento": date(2019, 6, 8),
                "sexo": "F",
                "curp": "MAFI190608MSIRTL08",
                "tutor_id": tutores[2].id,
                "estado": "ACTIVO"
            },
        ]
        
        ninos_creados = 0
        for nino_data in ninos_data:
            # Verificar si el niño ya existe por CURP
            nino_existente = db.query(Nino).filter(Nino.curp == nino_data["curp"]).first()
            if not nino_existente:
                nino = Nino(**nino_data)
                db.add(nino)
                ninos_creados += 1
        
        db.commit()
        print(f"✓ Niños creados: {ninos_creados}")
        print(f"✓ Total de niños en base de datos: {db.query(Nino).count()}")
        
        # Mostrar estadísticas
        activos = db.query(Nino).filter(Nino.estado == "ACTIVO").count()
        baja_temporal = db.query(Nino).filter(Nino.estado == "BAJA_TEMPORAL").count()
        inactivos = db.query(Nino).filter(Nino.estado == "INACTIVO").count()
        
        print("\n📊 Estadísticas:")
        print(f"   - Activos: {activos}")
        print(f"   - Baja temporal: {baja_temporal}")
        print(f"   - Inactivos: {inactivos}")
        print("\n✅ Datos de ejemplo creados exitosamente!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear niños de ejemplo: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 CREACIÓN DE NIÑOS DE EJEMPLO")
    print("=" * 60)
    crear_ninos_ejemplo()

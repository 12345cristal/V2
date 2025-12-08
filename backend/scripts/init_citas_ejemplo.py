"""
Script para crear citas de ejemplo en la base de datos

Ejecutar desde la carpeta backend:
    python -m scripts.init_citas_ejemplo
"""

from datetime import date, time, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.cita import Cita

# Crear engine y session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_citas_ejemplo():
    """Crea citas de ejemplo para diferentes fechas y estados"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existen citas
        citas_existentes = db.query(Cita).count()
        if citas_existentes > 0:
            print(f"⚠️  Ya existen {citas_existentes} citas en la base de datos")
            respuesta = input("¿Deseas agregar más citas de ejemplo? (s/n): ")
            if respuesta.lower() != 's':
                return
        
        # Fecha base: hoy
        fecha_base = date.today()
        
        citas_ejemplo = []
        
        # Citas PROGRAMADAS (estado_id=1) - fechas futuras
        for i in range(5):
            fecha = fecha_base + timedelta(days=i+1)
            cita = Cita(
                nino_id=1,  # Ajustar según tus datos
                terapeuta_id=1 + (i % 5),  # Rotar entre terapeutas 1-5
                terapia_id=1 + (i % 5),  # Rotar entre terapias 1-5
                fecha=fecha,
                hora_inicio=time(9, 0),
                hora_fin=time(10, 0),
                estado_id=1,  # PROGRAMADA
                motivo=f"Sesión de terapia programada {i+1}",
                observaciones="Cita de ejemplo",
                es_reposicion=0
            )
            citas_ejemplo.append(cita)
        
        # Citas REALIZADAS (estado_id=2) - fechas pasadas
        for i in range(5):
            fecha = fecha_base - timedelta(days=i+1)
            cita = Cita(
                nino_id=1,
                terapeuta_id=1 + (i % 5),
                terapia_id=1 + (i % 5),
                fecha=fecha,
                hora_inicio=time(10, 0),
                hora_fin=time(11, 0),
                estado_id=2,  # REALIZADA
                motivo=f"Sesión completada {i+1}",
                observaciones="Sesión realizada exitosamente",
                es_reposicion=0
            )
            citas_ejemplo.append(cita)
        
        # Citas CANCELADAS (estado_id=3)
        for i in range(3):
            fecha = fecha_base + timedelta(days=7+i)
            cita = Cita(
                nino_id=1,
                terapeuta_id=1 + (i % 5),
                terapia_id=1 + (i % 5),
                fecha=fecha,
                hora_inicio=time(11, 0),
                hora_fin=time(12, 0),
                estado_id=3,  # CANCELADA
                motivo=f"Cita cancelada {i+1}",
                observaciones="Cancelada por el tutor",
                es_reposicion=0
            )
            citas_ejemplo.append(cita)
        
        # Citas de REPOSICIÓN
        for i in range(2):
            fecha = fecha_base + timedelta(days=14+i)
            cita = Cita(
                nino_id=1,
                terapeuta_id=1,
                terapia_id=1,
                fecha=fecha,
                hora_inicio=time(14, 0),
                hora_fin=time(15, 0),
                estado_id=1,  # PROGRAMADA
                motivo="Reposición de sesión cancelada",
                observaciones="Cita de reposición",
                es_reposicion=1
            )
            citas_ejemplo.append(cita)
        
        # Insertar todas las citas
        db.add_all(citas_ejemplo)
        db.commit()
        
        print(f"✅ Se crearon {len(citas_ejemplo)} citas de ejemplo:")
        print(f"   - 5 citas PROGRAMADAS (futuras)")
        print(f"   - 5 citas REALIZADAS (pasadas)")
        print(f"   - 3 citas CANCELADAS")
        print(f"   - 2 citas de REPOSICIÓN")
        print(f"\n📊 Total de citas en BD: {db.query(Cita).count()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🏥 CREADOR DE CITAS DE EJEMPLO")
    print("=" * 60)
    print()
    
    crear_citas_ejemplo()
    
    print()
    print("=" * 60)
    print("✨ Proceso completado")
    print("=" * 60)

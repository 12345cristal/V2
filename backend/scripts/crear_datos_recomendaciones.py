# backend/scripts/crear_datos_recomendaciones.py
"""
Script para crear datos de prueba para el sistema de recomendaciones
Crea perfiles vectorizados ficticios para niños y actividades
"""
import sys
sys.path.insert(0, '.')

from app.db.session import SessionLocal
from app.models.recomendacion import PerfilNinoVectorizado, PerfilActividadVectorizada
from app.models.nino import Nino
from app.models.actividad import Actividad
from datetime import datetime
import random


def generar_embedding_ficticio(dimension=768):
    """Genera un embedding ficticio normalizado"""
    vector = [random.uniform(-1, 1) for _ in range(dimension)]
    # Normalizar
    norma = sum(x**2 for x in vector) ** 0.5
    return [x / norma for x in vector]


def crear_perfiles_ninos():
    """Crea perfiles vectorizados para los primeros 10 niños"""
    db = SessionLocal()
    
    try:
        # Obtener niños que no tienen perfil
        ninos = db.query(Nino).limit(10).all()
        
        perfiles_creados = 0
        for nino in ninos:
            # Verificar si ya tiene perfil
            perfil_existe = db.query(PerfilNinoVectorizado).filter(
                PerfilNinoVectorizado.nino_id == nino.id
            ).first()
            
            if perfil_existe:
                print(f"⏭️  Niño {nino.id} ya tiene perfil")
                continue
            
            # Determinar edad
            if nino.fecha_nacimiento:
                try:
                    if hasattr(nino.fecha_nacimiento, 'year'):
                        edad = datetime.now().year - nino.fecha_nacimiento.year
                    else:
                        edad = random.randint(3, 12)
                except:
                    edad = random.randint(3, 12)
            else:
                edad = random.randint(3, 12)
            
            # Crear perfil ficticio
            perfil = PerfilNinoVectorizado(
                nino_id=nino.id,
                embedding=generar_embedding_ficticio(),
                edad=edad,
                diagnosticos=['TEA', 'Retraso del lenguaje'] if random.random() > 0.5 else ['TEA'],
                dificultades=[
                    'Sensibilidad auditiva',
                    'Dificultad para seguir instrucciones',
                    'Hiperfoco visual'
                ][:random.randint(1, 3)],
                fortalezas=[
                    'Memoria visual excelente',
                    'Reconocimiento de patrones',
                    'Habilidad para clasificar objetos'
                ][:random.randint(1, 3)],
                texto_perfil=f"Perfil del niño {nino.nombre}: {edad} años, con características de TEA.",
                fecha_generacion=datetime.utcnow(),
                fecha_actualizacion=datetime.utcnow()
            )
            
            db.add(perfil)
            perfiles_creados += 1
            print(f"✅ Perfil creado para niño {nino.id}: {nino.nombre}")
        
        db.commit()
        print(f"\n🎉 Total perfiles de niños creados: {perfiles_creados}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


def crear_perfiles_actividades():
    """Crea perfiles vectorizados para actividades"""
    db = SessionLocal()
    
    try:
        # Obtener actividades activas
        actividades = db.query(Actividad).filter(Actividad.activo == 1).all()
        
        perfiles_creados = 0
        for actividad in actividades:
            # Verificar si ya tiene perfil
            perfil_existe = db.query(PerfilActividadVectorizada).filter(
                PerfilActividadVectorizada.actividad_id == actividad.id
            ).first()
            
            if perfil_existe:
                print(f"⏭️  Actividad {actividad.id} ya tiene perfil")
                continue
            
            # Crear perfil vectorizado
            perfil = PerfilActividadVectorizada(
                actividad_id=actividad.id,
                embedding=generar_embedding_ficticio(),
                tags=['terapia', 'desarrollo', 'sensorial'][:random.randint(1, 3)],
                areas_desarrollo=[actividad.area_desarrollo] if actividad.area_desarrollo else ['General'],
                nivel_dificultad=actividad.dificultad or random.randint(1, 3),
                texto_descripcion=actividad.descripcion or f"Actividad: {actividad.nombre}",
                fecha_generacion=datetime.utcnow(),
                fecha_actualizacion=datetime.utcnow()
            )
            
            db.add(perfil)
            perfiles_creados += 1
            print(f"✅ Perfil creado para actividad {actividad.id}: {actividad.nombre}")
        
        db.commit()
        print(f"\n🎉 Total perfiles de actividades creados: {perfiles_creados}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 CREANDO DATOS DE PRUEBA PARA RECOMENDACIONES")
    print("=" * 60)
    
    print("\n📝 Paso 1: Creando perfiles de niños...")
    crear_perfiles_ninos()
    
    print("\n📝 Paso 2: Creando perfiles de actividades...")
    crear_perfiles_actividades()
    
    print("\n" + "=" * 60)
    print("✨ PROCESO COMPLETADO")
    print("=" * 60)
    print("\n💡 Ahora puedes usar el sistema de recomendaciones en el frontend")

#!/usr/bin/env python3
# backend/migracion_mis_hijos.py
"""
Script para migrar la base de datos y crear las tablas de medicamentos y alergias.
Ejecutar desde la carpeta backend: python migracion_mis_hijos.py
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

from app.db.base_class import Base
from app.models.medicamentos import Medicamento, Alergia
from app.models.nino import Nino
from app.core.database import engine

def crear_tablas():
    """Crea las tablas necesarias en la base de datos"""
    try:
        print("🔄 Creando tablas de medicamentos y alergias...")
        
        # Crear las tablas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tablas creadas exitosamente!")
        print("\nTablas creadas:")
        print("  - medicamentos")
        print("  - alergias")
        
        # Verificar conexión
        from sqlalchemy import text
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES LIKE 'medicamentos'"))
            if result.fetchone():
                print("\n✅ Tabla 'medicamentos' verificada")
            
            result = connection.execute(text("SHOW TABLES LIKE 'alergias'"))
            if result.fetchone():
                print("✅ Tabla 'alergias' verificada")
        
        print("\n✅ Migración completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False


def insertar_datos_prueba():
    """Inserta datos de prueba (opcional)"""
    try:
        from sqlalchemy.orm import Session
        from datetime import date, datetime
        
        print("\n🔄 Insertando datos de prueba...")
        
        with Session(engine) as session:
            # Buscar un niño para agregar medicamentos y alergias de prueba
            nino = session.query(Nino).first()
            
            if not nino:
                print("⚠️  No hay niños en la base de datos. Cree un niño primero.")
                return False
            
            print(f"ℹ️  Usando niño: {nino.nombre} (ID: {nino.id})")
            
            # Crear medicamentos de prueba
            medicamentos_prueba = [
                Medicamento(
                    nino_id=nino.id,
                    nombre="Metilfenidato",
                    dosis="10 mg",
                    frecuencia="Dos veces al día",
                    razon="TDAH",
                    fecha_inicio=date.today(),
                    activo=True,
                    novedadReciente=True,
                    actualizado_por="Coordinador Sistema"
                ),
                Medicamento(
                    nino_id=nino.id,
                    nombre="Fluoxetina",
                    dosis="20 mg",
                    frecuencia="Una vez al día",
                    razon="Ansiedad",
                    fecha_inicio=date(2024, 1, 15),
                    activo=True,
                    novedadReciente=False,
                    actualizado_por="Coordinador Sistema"
                )
            ]
            
            # Crear alergias de prueba
            alergias_prueba = [
                Alergia(
                    nino_id=nino.id,
                    nombre="Penicilina",
                    severidad="severa",
                    reaccion="Anafilaxia",
                    tratamiento="Evitar completamente. Usar alternativas como cefalosporinas."
                ),
                Alergia(
                    nino_id=nino.id,
                    nombre="Maní",
                    severidad="moderada",
                    reaccion="Picazón en la boca, hinchazón de labios",
                    tratamiento="Evitar productos con maní"
                )
            ]
            
            # Agregar a la sesión
            for med in medicamentos_prueba:
                session.add(med)
            
            for alergia in alergias_prueba:
                session.add(alergia)
            
            # Confirmar cambios
            session.commit()
            
            print(f"✅ {len(medicamentos_prueba)} medicamentos agregados")
            print(f"✅ {len(alergias_prueba)} alergias agregadas")
            
            return True
            
    except Exception as e:
        print(f"❌ Error al insertar datos de prueba: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 MIGRACIÓN: MEDICAMENTOS Y ALERGIAS")
    print("=" * 60)
    
    # Crear tablas
    if crear_tablas():
        # Preguntar si agregar datos de prueba
        respuesta = input("\n¿Deseas agregar datos de prueba? (s/n): ").lower().strip()
        if respuesta == 's':
            insertar_datos_prueba()
    
    print("\n" + "=" * 60)
    print("Migración finalizada")
    print("=" * 60)

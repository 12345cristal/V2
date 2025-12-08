#!/usr/bin/env python3
"""
Script para inicializar catálogos de terapias en la base de datos
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.terapia import TipoTerapia, Prioridad, Terapia


def init_tipo_terapia(db: Session):
    """Inicializa el catálogo de tipos de terapia"""
    tipos = [
        {"codigo": "LENGUAJE", "nombre": "Terapia de Lenguaje"},
        {"codigo": "CONDUCTUAL", "nombre": "Terapia Conductual"},
        {"codigo": "OCUPACIONAL", "nombre": "Terapia Ocupacional"},
        {"codigo": "FISICA", "nombre": "Terapia Física"},
        {"codigo": "ABA", "nombre": "Análisis Conductual Aplicado (ABA)"},
        {"codigo": "SENSORIAL", "nombre": "Integración Sensorial"},
        {"codigo": "COGNITIVA", "nombre": "Terapia Cognitiva"},
        {"codigo": "SOCIAL", "nombre": "Habilidades Sociales"},
        {"codigo": "PSICOLOGICA", "nombre": "Apoyo Psicológico"},
        {"codigo": "ACADEMICA", "nombre": "Apoyo Académico"},
    ]
    
    for tipo_data in tipos:
        tipo = db.query(TipoTerapia).filter(TipoTerapia.codigo == tipo_data["codigo"]).first()
        if not tipo:
            tipo = TipoTerapia(**tipo_data)
            db.add(tipo)
            print(f"✓ Tipo de terapia creado: {tipo_data['nombre']}")
        else:
            print(f"• Tipo de terapia ya existe: {tipo_data['nombre']}")
    
    db.commit()


def init_prioridades(db: Session):
    """Inicializa el catálogo de prioridades"""
    prioridades = [
        {"codigo": "URGENTE", "nombre": "Urgente"},
        {"codigo": "ALTA", "nombre": "Alta"},
        {"codigo": "MEDIA", "nombre": "Media"},
        {"codigo": "BAJA", "nombre": "Baja"},
    ]
    
    for prio_data in prioridades:
        prio = db.query(Prioridad).filter(Prioridad.codigo == prio_data["codigo"]).first()
        if not prio:
            prio = Prioridad(**prio_data)
            db.add(prio)
            print(f"✓ Prioridad creada: {prio_data['nombre']}")
        else:
            print(f"• Prioridad ya existe: {prio_data['nombre']}")
    
    db.commit()


def init_terapias_ejemplo(db: Session):
    """Inicializa terapias de ejemplo"""
    # Obtener IDs de tipos de terapia
    tipo_lenguaje = db.query(TipoTerapia).filter(TipoTerapia.codigo == "LENGUAJE").first()
    tipo_aba = db.query(TipoTerapia).filter(TipoTerapia.codigo == "ABA").first()
    tipo_sensorial = db.query(TipoTerapia).filter(TipoTerapia.codigo == "SENSORIAL").first()
    tipo_social = db.query(TipoTerapia).filter(TipoTerapia.codigo == "SOCIAL").first()
    tipo_ocupacional = db.query(TipoTerapia).filter(TipoTerapia.codigo == "OCUPACIONAL").first()
    
    terapias = [
        {
            "nombre": "Terapia de Lenguaje Inicial",
            "descripcion": "Desarrollo de habilidades comunicativas básicas para niños con TEA",
            "tipo_id": tipo_lenguaje.id if tipo_lenguaje else 1,
            "duracion_minutos": 45,
            "objetivo_general": "Mejorar la comunicación verbal y no verbal, desarrollar vocabulario funcional",
            "activo": 1
        },
        {
            "nombre": "ABA Intensivo",
            "descripcion": "Intervención conductual intensiva basada en principios ABA",
            "tipo_id": tipo_aba.id if tipo_aba else 1,
            "duracion_minutos": 60,
            "objetivo_general": "Reducir conductas desafiantes y promover comportamientos adaptativos",
            "activo": 1
        },
        {
            "nombre": "Integración Sensorial",
            "descripcion": "Terapia para procesamiento sensorial y regulación",
            "tipo_id": tipo_sensorial.id if tipo_sensorial else 1,
            "duracion_minutos": 45,
            "objetivo_general": "Mejorar el procesamiento sensorial y la autorregulación",
            "activo": 1
        },
        {
            "nombre": "Habilidades Sociales Grupales",
            "descripcion": "Desarrollo de competencias sociales en grupo",
            "tipo_id": tipo_social.id if tipo_social else 1,
            "duracion_minutos": 60,
            "objetivo_general": "Fomentar interacción social apropiada y trabajo en equipo",
            "activo": 1
        },
        {
            "nombre": "Terapia Ocupacional",
            "descripcion": "Desarrollo de habilidades para la vida diaria",
            "tipo_id": tipo_ocupacional.id if tipo_ocupacional else 1,
            "duracion_minutos": 45,
            "objetivo_general": "Promover independencia en actividades cotidianas",
            "activo": 1
        },
    ]
    
    for terapia_data in terapias:
        terapia = db.query(Terapia).filter(Terapia.nombre == terapia_data["nombre"]).first()
        if not terapia:
            terapia = Terapia(**terapia_data)
            db.add(terapia)
            print(f"✓ Terapia creada: {terapia_data['nombre']}")
        else:
            print(f"• Terapia ya existe: {terapia_data['nombre']}")
    
    db.commit()


def main():
    """Función principal"""
    print("=" * 60)
    print("INICIALIZACIÓN DE CATÁLOGOS DE TERAPIAS")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        print("\n1. Inicializando tipos de terapia...")
        init_tipo_terapia(db)
        
        print("\n2. Inicializando prioridades...")
        init_prioridades(db)
        
        print("\n3. Creando terapias de ejemplo...")
        init_terapias_ejemplo(db)
        
        print("\n" + "=" * 60)
        print("✓ Catálogos inicializados correctamente")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error al inicializar catálogos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

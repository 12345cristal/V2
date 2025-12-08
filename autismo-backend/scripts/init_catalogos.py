"""
Script para inicializar tablas de catálogos con datos predeterminados.
"""

import sys
from pathlib import Path

# Agregar el directorio padre al path para imports
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.models.catalogos import (
    GradoAcademico,
    EstadoLaboral,
    TipoTerapia,
    Prioridad,
    EstadoCita,
    NivelDificultad,
    TipoRecurso,
    CategoriaRecurso,
    NivelRecurso,
)


# Datos iniciales para cada catálogo
GRADOS_ACADEMICOS = [
    "Sin estudios",
    "Primaria",
    "Secundaria",
    "Preparatoria",
    "Licenciatura",
    "Maestría",
    "Doctorado",
]

ESTADOS_LABORALES = [
    "Desempleado",
    "Empleado",
    "Independiente",
    "Jubilado",
    "Estudiante",
]

TIPOS_TERAPIA = [
    "Lenguaje",
    "Ocupacional",
    "Conductual",
    "Física",
    "Cognitiva",
    "Sensorial",
    "Emocional",
]

PRIORIDADES = [
    "Muy Baja",
    "Baja",
    "Media",
    "Alta",
    "Muy Alta",
    "Crítica",
]

ESTADOS_CITA = [
    "Pendiente",
    "Confirmada",
    "En Curso",
    "Completada",
    "Cancelada",
    "Reprogramada",
]

NIVELES_DIFICULTAD = [
    "Muy Fácil",
    "Fácil",
    "Moderado",
    "Difícil",
    "Muy Difícil",
]

TIPOS_RECURSO = [
    "Video",
    "Audio",
    "Documento",
    "Imagen",
    "Interactivo",
    "Juego",
    "Ejercicio",
]

CATEGORIAS_RECURSO = [
    "Comunicación",
    "Motricidad Fina",
    "Motricidad Gruesa",
    "Cognitivo",
    "Social",
    "Emocional",
    "Sensorial",
    "Autonomía",
]

NIVELES_RECURSO = [
    "Inicial",
    "Básico",
    "Intermedio",
    "Avanzado",
]


def insertar_catalogo(db, modelo, items, nombre_catalogo):
    """Insertar items en un catálogo si no existen"""
    print(f"  📋 {nombre_catalogo}...")
    insertados = 0
    
    for nombre in items:
        existe = db.query(modelo).filter(modelo.nombre == nombre).first()
        if not existe:
            db.add(modelo(nombre=nombre))
            insertados += 1
    
    if insertados > 0:
        print(f"     ✅ {insertados} nuevo(s)")
    else:
        print(f"     ⏭️  Ya existen todos")


def init_catalogos():
    """Inicializar todas las tablas de catálogos"""
    db = SessionLocal()
    try:
        print("🗂️  Inicializando catálogos...\n")
        
        insertar_catalogo(db, GradoAcademico, GRADOS_ACADEMICOS, "Grados Académicos")
        insertar_catalogo(db, EstadoLaboral, ESTADOS_LABORALES, "Estados Laborales")
        insertar_catalogo(db, TipoTerapia, TIPOS_TERAPIA, "Tipos de Terapia")
        insertar_catalogo(db, Prioridad, PRIORIDADES, "Prioridades")
        insertar_catalogo(db, EstadoCita, ESTADOS_CITA, "Estados de Cita")
        insertar_catalogo(db, NivelDificultad, NIVELES_DIFICULTAD, "Niveles de Dificultad")
        insertar_catalogo(db, TipoRecurso, TIPOS_RECURSO, "Tipos de Recurso")
        insertar_catalogo(db, CategoriaRecurso, CATEGORIAS_RECURSO, "Categorías de Recurso")
        insertar_catalogo(db, NivelRecurso, NIVELES_RECURSO, "Niveles de Recurso")
        
        db.commit()
        print("\n✅ Catálogos inicializados correctamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("INICIALIZAR CATÁLOGOS - Autismo Mochis IA")
    print("="*60 + "\n")
    init_catalogos()
    print("\n" + "="*60 + "\n")

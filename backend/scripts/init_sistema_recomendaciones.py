# backend/scripts/init_sistema_recomendaciones.py
"""
Script para inicializar el sistema de recomendaciones inteligentes
- Crea tablas necesarias
- Vectoriza actividades existentes
- Genera perfiles iniciales
"""
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.actividad import Actividad
from app.models.nino import Nino
from app.services.recomendacion_service import get_recomendacion_service


def ejecutar_sql(db: Session, archivo_sql: str):
    """Ejecuta un archivo SQL"""
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Dividir por ; para ejecutar cada statement
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        
        for statement in statements:
            if statement and not statement.startswith('--'):
                db.execute(statement)
        
        db.commit()
        print(f"✓ SQL ejecutado correctamente: {archivo_sql}")
        return True
    except Exception as e:
        print(f"✗ Error ejecutando SQL: {e}")
        db.rollback()
        return False


def vectorizar_actividades_existentes(db: Session):
    """Vectoriza todas las actividades existentes"""
    print("\n" + "="*60)
    print("VECTORIZANDO ACTIVIDADES EXISTENTES")
    print("="*60)
    
    try:
        servicio = get_recomendacion_service(db)
        
        # Obtener todas las actividades activas
        actividades = db.query(Actividad).filter(Actividad.activo == 1).all()
        
        if not actividades:
            print("⚠ No hay actividades para vectorizar")
            return
        
        print(f"Encontradas {len(actividades)} actividades activas")
        
        for i, actividad in enumerate(actividades, 1):
            try:
                perfil = servicio.crear_perfil_actividad(actividad.id)
                print(f"  [{i}/{len(actividades)}] ✓ {actividad.nombre}")
            except Exception as e:
                print(f"  [{i}/{len(actividades)}] ✗ Error en {actividad.nombre}: {e}")
        
        print("\n✓ Vectorización de actividades completada")
        
    except Exception as e:
        print(f"✗ Error vectorizando actividades: {e}")


def generar_perfiles_ninos_ejemplo(db: Session):
    """Genera perfiles vectorizados para algunos niños de ejemplo"""
    print("\n" + "="*60)
    print("GENERANDO PERFILES DE NIÑOS DE EJEMPLO")
    print("="*60)
    
    try:
        servicio = get_recomendacion_service(db)
        
        # Obtener los primeros 5 niños como ejemplo
        ninos = db.query(Nino).limit(5).all()
        
        if not ninos:
            print("⚠ No hay niños registrados")
            return
        
        print(f"Generando perfiles para {len(ninos)} niños")
        
        for i, nino in enumerate(ninos, 1):
            try:
                perfil = servicio.crear_perfil_nino(nino.id)
                print(f"  [{i}/{len(ninos)}] ✓ {nino.nombre} {nino.apellido_paterno}")
            except Exception as e:
                print(f"  [{i}/{len(ninos)}] ✗ Error: {e}")
        
        print("\n✓ Generación de perfiles completada")
        
    except Exception as e:
        print(f"✗ Error generando perfiles: {e}")


def verificar_instalacion(db: Session):
    """Verifica que todo esté correctamente instalado"""
    print("\n" + "="*60)
    print("VERIFICANDO INSTALACIÓN")
    print("="*60)
    
    tablas = [
        'perfil_nino_vectorizado',
        'perfil_actividad_vectorizada',
        'historial_progreso',
        'recomendaciones_actividades',
        'asignaciones_terapeuta_topsis'
    ]
    
    from app.models.recomendacion import (
        PerfilNinoVectorizado,
        PerfilActividadVectorizada,
        HistorialProgreso,
        RecomendacionActividad,
        AsignacionTerapeutaTOPSIS
    )
    
    resultados = []
    
    # Verificar perfiles de actividades
    count_actividades = db.query(PerfilActividadVectorizada).count()
    resultados.append(f"Actividades vectorizadas: {count_actividades}")
    
    # Verificar perfiles de niños
    count_ninos = db.query(PerfilNinoVectorizado).count()
    resultados.append(f"Niños con perfil vectorizado: {count_ninos}")
    
    # Verificar historial
    count_historial = db.query(HistorialProgreso).count()
    resultados.append(f"Registros de progreso: {count_historial}")
    
    # Verificar recomendaciones
    count_recomendaciones = db.query(RecomendacionActividad).count()
    resultados.append(f"Recomendaciones generadas: {count_recomendaciones}")
    
    # Verificar asignaciones TOPSIS
    count_topsis = db.query(AsignacionTerapeutaTOPSIS).count()
    resultados.append(f"Asignaciones TOPSIS: {count_topsis}")
    
    print("\nEstadísticas:")
    for resultado in resultados:
        print(f"  ✓ {resultado}")
    
    print("\n✓ Sistema de recomendaciones instalado correctamente")


def mostrar_ejemplo_uso():
    """Muestra ejemplos de cómo usar el sistema"""
    print("\n" + "="*60)
    print("EJEMPLOS DE USO")
    print("="*60)
    
    ejemplos = """
# 1. Recomendar actividades para un niño
GET /api/v1/recomendaciones/actividades/{nino_id}?top_n=5&incluir_explicacion=true

# 2. Seleccionar terapeuta óptimo con TOPSIS
POST /api/v1/recomendaciones/terapeuta/{nino_id}
{
    "terapia_tipo": "lenguaje",
    "criterios_pesos": {
        "experiencia": 0.30,
        "disponibilidad": 0.25,
        "carga_trabajo": 0.20,
        "evaluacion_desempeno": 0.15,
        "especializacion": 0.10
    }
}

# 3. Flujo completo (Actividades + Terapeuta + Explicaciones)
POST /api/v1/recomendaciones/completa/{nino_id}
{
    "terapia_tipo": "conductual"
}

# 4. Registrar progreso en actividad
POST /api/v1/recomendaciones/progreso/registrar
{
    "nino_id": 1,
    "actividad_id": 5,
    "terapeuta_id": 3,
    "calificacion": 4.5,
    "notas_progreso": "El niño mostró gran interés...",
    "duracion_minutos": 45
}

# 5. Generar sugerencias clínicas con Gemini
POST /api/v1/recomendaciones/sugerencias/{nino_id}
{
    "incluir_actividades_actuales": true,
    "incluir_progreso_reciente": true
}

# 6. Ver historial de recomendaciones
GET /api/v1/recomendaciones/historial/{nino_id}?limite=10
"""
    
    print(ejemplos)
    
    print("\n" + "="*60)
    print("CONFIGURACIÓN REQUERIDA")
    print("="*60)
    
    config = """
En el archivo .env, agregar:

GEMINI_API_KEY=tu_api_key_de_gemini

Obtén tu API key en: https://makersuite.google.com/app/apikey
"""
    
    print(config)


def main():
    """Función principal"""
    print("\n" + "="*60)
    print("INSTALACIÓN DEL SISTEMA DE RECOMENDACIONES INTELIGENTES")
    print("="*60)
    print("\nIntegra:")
    print("  • Recomendación basada en contenido (similitud vectorial)")
    print("  • TOPSIS para selección de terapeutas")
    print("  • Gemini para embeddings y explicaciones")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # 1. Crear tablas
        print("\n[1/4] Creando tablas...")
        archivo_sql = ROOT_DIR / "scripts" / "crear_tablas_recomendaciones.sql"
        if archivo_sql.exists():
            ejecutar_sql(db, str(archivo_sql))
        else:
            print(f"⚠ No se encontró: {archivo_sql}")
        
        # 2. Vectorizar actividades
        print("\n[2/4] Vectorizando actividades...")
        vectorizar_actividades_existentes(db)
        
        # 3. Generar perfiles de ejemplo
        print("\n[3/4] Generando perfiles de ejemplo...")
        generar_perfiles_ninos_ejemplo(db)
        
        # 4. Verificar instalación
        print("\n[4/4] Verificando instalación...")
        verificar_instalacion(db)
        
        # Mostrar ejemplos de uso
        mostrar_ejemplo_uso()
        
        print("\n" + "="*60)
        print("✓ INSTALACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error durante la instalación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()

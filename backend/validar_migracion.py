"""
SCRIPT DE VALIDACIÓN POST-MIGRACIÓN
Verifica que la tabla 'citas' esté sincronizada con el modelo ORM
"""
import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import inspect, text
from app.db.session import engine
from app.models.cita import Cita


def validar_columnas_google_calendar():
    """
    Valida que las 4 columnas de Google Calendar existan en la BD
    """
    print("=" * 60)
    print("🔍 VALIDACIÓN: Columnas Google Calendar en tabla 'citas'")
    print("=" * 60)
    
    inspector = inspect(engine)
    columnas_bd = {col['name']: col for col in inspector.get_columns('citas')}
    
    # Columnas requeridas según modelo ORM
    columnas_requeridas = {
        'google_event_id': {
            'tipo_esperado': 'VARCHAR',
            'nullable': True,
            'descripcion': 'ID del evento en Google Calendar'
        },
        'google_calendar_link': {
            'tipo_esperado': 'VARCHAR',
            'nullable': True,
            'descripcion': 'URL del evento en Google Calendar'
        },
        'sincronizado_calendar': {
            'tipo_esperado': 'TINYINT',
            'nullable': False,
            'descripcion': 'Indica si está sincronizado'
        },
        'fecha_sincronizacion': {
            'tipo_esperado': 'DATETIME',
            'nullable': True,
            'descripcion': 'Última fecha de sincronización'
        }
    }
    
    errores = []
    exitos = []
    
    for col_nombre, col_info in columnas_requeridas.items():
        if col_nombre not in columnas_bd:
            errores.append(f"❌ Columna '{col_nombre}' NO EXISTE en la tabla")
        else:
            col_bd = columnas_bd[col_nombre]
            tipo_bd = str(col_bd['type']).upper()
            
            # Validar tipo
            if col_info['tipo_esperado'] not in tipo_bd:
                errores.append(
                    f"⚠️  Columna '{col_nombre}': tipo '{tipo_bd}' "
                    f"(esperado: {col_info['tipo_esperado']})"
                )
            else:
                exitos.append(
                    f"✅ {col_nombre}: {tipo_bd} "
                    f"(nullable={col_bd['nullable']}) - OK"
                )
    
    print("\n📋 Resultados:\n")
    for exito in exitos:
        print(exito)
    
    if errores:
        print("\n❌ ERRORES ENCONTRADOS:\n")
        for error in errores:
            print(error)
        print("\n🔧 ACCIÓN REQUERIDA:")
        print("   Ejecutar: backend/MIGRACION_GOOGLE_CALENDAR.sql")
        return False
    else:
        print("\n✅ TODAS LAS COLUMNAS ESTÁN SINCRONIZADAS")
        return True


def probar_query_simple():
    """
    Prueba que queries simples funcionen sin error de columnas
    """
    print("\n" + "=" * 60)
    print("🧪 PRUEBA: Query simple COUNT(*)")
    print("=" * 60)
    
    try:
        from app.db.session import SessionLocal
        db = SessionLocal()
        
        # Esta query fallaba antes de la migración
        count = db.query(Cita).count()
        print(f"✅ Query COUNT ejecutada exitosamente: {count} citas")
        
        # Intentar acceder a las columnas de Google Calendar
        primera_cita = db.query(Cita).first()
        if primera_cita:
            print(f"✅ Acceso a google_event_id: {primera_cita.google_event_id}")
            print(f"✅ Acceso a sincronizado_calendar: {primera_cita.sincronizado_calendar}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        if "Unknown column" in str(e):
            print("\n🔧 La migración SQL AÚN NO se ha ejecutado")
        return False


def verificar_indices():
    """
    Verifica que los índices estén creados
    """
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN: Índices en tabla 'citas'")
    print("=" * 60)
    
    inspector = inspect(engine)
    indices = inspector.get_indexes('citas')
    
    indices_google = [idx for idx in indices 
                     if 'google_event_id' in str(idx.get('column_names', []))]
    
    if indices_google:
        print(f"✅ Índice en google_event_id encontrado: {len(indices_google)}")
    else:
        print("⚠️  No se encontró índice específico en google_event_id")
    
    return True


if __name__ == "__main__":
    print("\n🚀 INICIANDO VALIDACIÓN POST-MIGRACIÓN\n")
    
    # Paso 1: Verificar columnas
    columnas_ok = validar_columnas_google_calendar()
    
    if columnas_ok:
        # Paso 2: Probar queries
        query_ok = probar_query_simple()
        
        # Paso 3: Verificar índices
        verificar_indices()
        
        if query_ok:
            print("\n" + "=" * 60)
            print("✅ ¡MIGRACIÓN EXITOSA! Backend listo para Google Calendar")
            print("=" * 60)
            print("\n📌 Próximos pasos:")
            print("   1. Reiniciar backend: python run_server.py")
            print("   2. Probar endpoints:")
            print("      - GET /api/v1/coordinador/dashboard")
            print("      - GET /api/v1/citas")
            print("      - GET /api/v1/estados-cita")
            print("\n")
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("❌ MIGRACIÓN PENDIENTE")
        print("=" * 60)
        print("\n📌 Ejecutar en MySQL:")
        print("   mysql -u root -p < backend/MIGRACION_GOOGLE_CALENDAR.sql")
        print("\n")
        sys.exit(1)

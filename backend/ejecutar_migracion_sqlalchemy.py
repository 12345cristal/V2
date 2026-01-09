"""
EJECUTAR MIGRACIÓN VÍA SQLALCHEMY
Alternativa cuando MySQL CLI falla por problemas de autenticación
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.db.session import engine

def ejecutar_migracion():
    """
    Ejecuta la migración directamente usando SQLAlchemy
    """
    print("=" * 70)
    print("🔧 MIGRACIÓN: Agregar columnas Google Calendar")
    print("=" * 70)
    
    migracion_queries = [
        # Paso 1: Agregar columnas
        """
        ALTER TABLE citas 
            ADD COLUMN google_event_id VARCHAR(255) NULL UNIQUE 
                COMMENT 'ID del evento en Google Calendar',
            ADD COLUMN google_calendar_link VARCHAR(500) NULL 
                COMMENT 'URL del evento en Google Calendar',
            ADD COLUMN sincronizado_calendar TINYINT(1) NOT NULL DEFAULT 0 
                COMMENT 'Indica si está sincronizado con Google Calendar',
            ADD COLUMN fecha_sincronizacion DATETIME NULL 
                COMMENT 'Última fecha de sincronización con Google Calendar'
        """,
        
        # Paso 2: Agregar índices
        """
        ALTER TABLE citas 
            ADD INDEX idx_google_event_id (google_event_id)
        """,
        
        """
        ALTER TABLE citas 
            ADD INDEX idx_sincronizado_calendar (sincronizado_calendar)
        """
    ]
    
    try:
        with engine.connect() as conn:
            print("\n📊 Ejecutando cambios en la base de datos...\n")
            
            # Ejecutar cada query
            for i, query in enumerate(migracion_queries, 1):
                try:
                    print(f"[{i}/{len(migracion_queries)}] Ejecutando...", end=" ")
                    conn.execute(text(query))
                    conn.commit()
                    print("✅ OK")
                except Exception as e:
                    error_msg = str(e)
                    
                    # Ignorar errores de columnas/índices duplicados
                    if "Duplicate column name" in error_msg:
                        print("⚠️  Columna ya existe (OK)")
                    elif "Duplicate key name" in error_msg:
                        print("⚠️  Índice ya existe (OK)")
                    else:
                        print(f"❌ ERROR")
                        raise
            
            print("\n" + "=" * 70)
            print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("=" * 70)
            
            # Verificar estructura
            print("\n📋 Verificando estructura de tabla 'citas':")
            result = conn.execute(text("DESC citas"))
            
            columnas_google = []
            for row in result:
                if 'google' in row[0] or 'sincronizado' in row[0]:
                    columnas_google.append(f"   ✅ {row[0]} ({row[1]})")
            
            if columnas_google:
                print("\n🎯 Columnas Google Calendar encontradas:")
                for col in columnas_google:
                    print(col)
            
            print("\n" + "=" * 70)
            print("📌 Próximos pasos:")
            print("   1. Ejecutar validación: python validar_migracion.py")
            print("   2. Reiniciar backend: python run_server.py")
            print("   3. Probar endpoints:")
            print("      - GET /api/v1/coordinador/dashboard")
            print("      - GET /api/v1/citas")
            print("=" * 70)
            
            return True
            
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ ERROR al ejecutar migración:")
        print("=" * 70)
        print(f"   {str(e)}")
        print("\n💡 Alternativa:")
        print("   Ejecutar manualmente en phpMyAdmin:")
        print("   1. Abrir: http://localhost/phpmyadmin")
        print("   2. Seleccionar base de datos 'autismo'")
        print("   3. Ir a pestaña SQL")
        print("   4. Copiar contenido de: MIGRACION_GOOGLE_CALENDAR.sql")
        print("   5. Ejecutar")
        print("=" * 70)
        return False


if __name__ == "__main__":
    try:
        exito = ejecutar_migracion()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Migración cancelada por el usuario")
        sys.exit(1)

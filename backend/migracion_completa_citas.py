"""
MIGRACIÓN COMPLETA: Sincronizar TODAS las columnas del modelo Cita
Incluye Google Calendar + Gestión + Auditoría
"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from sqlalchemy import text
from app.db.session import engine

def ejecutar_migracion_completa():
    """
    Agrega TODAS las columnas faltantes del modelo Cita
    """
    print("=" * 80)
    print("🔧 MIGRACIÓN COMPLETA: Sincronizar modelo Cita con base de datos")
    print("=" * 80)
    
    migraciones = [
        # Google Calendar (ya ejecutadas pero por si acaso)
        {
            "nombre": "Google Calendar: google_event_id",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN IF NOT EXISTS google_event_id VARCHAR(255) NULL UNIQUE 
                COMMENT 'ID del evento en Google Calendar'
            """
        },
        {
            "nombre": "Google Calendar: google_calendar_link",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN IF NOT EXISTS google_calendar_link VARCHAR(500) NULL 
                COMMENT 'URL del evento en Google Calendar'
            """
        },
        {
            "nombre": "Google Calendar: sincronizado_calendar",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN IF NOT EXISTS sincronizado_calendar TINYINT(1) NOT NULL DEFAULT 0 
                COMMENT 'Indica si está sincronizado con Google Calendar'
            """
        },
        {
            "nombre": "Google Calendar: fecha_sincronizacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN IF NOT EXISTS fecha_sincronizacion DATETIME NULL 
                COMMENT 'Última fecha de sincronización con Google Calendar'
            """
        },
        
        # Campos de Gestión
        {
            "nombre": "Gestión: confirmada",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN confirmada TINYINT(1) NOT NULL DEFAULT 0 
                COMMENT 'Confirmada por el padre/tutor'
            """
        },
        {
            "nombre": "Gestión: fecha_confirmacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN fecha_confirmacion DATETIME NULL
            """
        },
        {
            "nombre": "Gestión: cancelado_por",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN cancelado_por INT NULL,
                ADD CONSTRAINT fk_citas_cancelado_por 
                FOREIGN KEY (cancelado_por) REFERENCES usuarios(id) ON DELETE SET NULL
            """
        },
        {
            "nombre": "Gestión: fecha_cancelacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN fecha_cancelacion DATETIME NULL
            """
        },
        {
            "nombre": "Gestión: motivo_cancelacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN motivo_cancelacion TEXT NULL
            """
        },
        
        # Auditoría
        {
            "nombre": "Auditoría: creado_por",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN creado_por INT NULL,
                ADD CONSTRAINT fk_citas_creado_por 
                FOREIGN KEY (creado_por) REFERENCES usuarios(id) ON DELETE SET NULL
            """
        },
        {
            "nombre": "Auditoría: fecha_creacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            """
        },
        {
            "nombre": "Auditoría: actualizado_por",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN actualizado_por INT NULL,
                ADD CONSTRAINT fk_citas_actualizado_por 
                FOREIGN KEY (actualizado_por) REFERENCES usuarios(id) ON DELETE SET NULL
            """
        },
        {
            "nombre": "Auditoría: fecha_actualizacion",
            "query": """
                ALTER TABLE citas 
                ADD COLUMN fecha_actualizacion DATETIME 
                DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """
        },
        
        # Índices
        {
            "nombre": "Índice: idx_google_event_id",
            "query": """
                ALTER TABLE citas 
                ADD INDEX idx_google_event_id (google_event_id)
            """
        },
        {
            "nombre": "Índice: idx_sincronizado_calendar",
            "query": """
                ALTER TABLE citas 
                ADD INDEX idx_sincronizado_calendar (sincronizado_calendar)
            """
        },
        {
            "nombre": "Índice: idx_confirmada",
            "query": """
                ALTER TABLE citas 
                ADD INDEX idx_confirmada (confirmada)
            """
        },
        {
            "nombre": "Índice: idx_fecha_creacion",
            "query": """
                ALTER TABLE citas 
                ADD INDEX idx_fecha_creacion (fecha_creacion)
            """
        }
    ]
    
    exitosas = 0
    ya_existentes = 0
    errores = 0
    
    try:
        with engine.connect() as conn:
            print(f"\n📊 Ejecutando {len(migraciones)} migraciones...\n")
            
            for i, migracion in enumerate(migraciones, 1):
                try:
                    nombre = migracion['nombre']
                    query = migracion['query']
                    
                    print(f"[{i:02d}/{len(migraciones)}] {nombre:<50}", end=" ")
                    conn.execute(text(query))
                    conn.commit()
                    print("✅")
                    exitosas += 1
                    
                except Exception as e:
                    error_msg = str(e)
                    
                    # Errores que indican que ya existe (no son problemas)
                    if any(x in error_msg for x in [
                        "Duplicate column name",
                        "Duplicate key name",
                        "duplicate key name"
                    ]):
                        print("⚠️  Ya existe")
                        ya_existentes += 1
                    else:
                        print(f"❌ ERROR")
                        print(f"    └─ {error_msg[:100]}")
                        errores += 1
            
            print("\n" + "=" * 80)
            print("📊 RESUMEN DE MIGRACIÓN")
            print("=" * 80)
            print(f"   ✅ Exitosas:      {exitosas}")
            print(f"   ⚠️  Ya existían:   {ya_existentes}")
            print(f"   ❌ Errores:       {errores}")
            print("=" * 80)
            
            if errores == 0:
                print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE\n")
                
                # Verificar estructura final
                print("📋 Verificando estructura final...")
                result = conn.execute(text("SHOW COLUMNS FROM citas"))
                
                columnas_nuevas = [
                    'google_event_id', 'google_calendar_link', 'sincronizado_calendar',
                    'fecha_sincronizacion', 'confirmada', 'fecha_confirmacion',
                    'cancelado_por', 'fecha_cancelacion', 'motivo_cancelacion',
                    'creado_por', 'fecha_creacion', 'actualizado_por', 'fecha_actualizacion'
                ]
                
                columnas_encontradas = []
                for row in result:
                    if row[0] in columnas_nuevas:
                        columnas_encontradas.append(row[0])
                
                print(f"\n🎯 Columnas nuevas encontradas: {len(columnas_encontradas)}/{len(columnas_nuevas)}")
                
                if len(columnas_encontradas) == len(columnas_nuevas):
                    print("✅ TODAS las columnas están presentes")
                else:
                    faltantes = set(columnas_nuevas) - set(columnas_encontradas)
                    print(f"⚠️  Faltan: {', '.join(faltantes)}")
                
                return True
            else:
                return False
                
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERROR CRÍTICO:")
        print("=" * 80)
        print(f"   {str(e)}")
        return False


if __name__ == "__main__":
    try:
        exito = ejecutar_migracion_completa()
        
        if exito:
            print("\n" + "=" * 80)
            print("📌 PRÓXIMOS PASOS:")
            print("=" * 80)
            print("   1. Validar: python validar_migracion.py")
            print("   2. Reiniciar backend: python run_server.py")
            print("   3. Probar endpoints:")
            print("      - GET /api/v1/coordinador/dashboard")
            print("      - GET /api/v1/citas")
            print("=" * 80)
            print("")
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Migración cancelada por el usuario")
        sys.exit(1)

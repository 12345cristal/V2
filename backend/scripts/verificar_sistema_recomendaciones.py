# backend/scripts/verificar_sistema_recomendaciones.py
"""
Script de verificación del sistema de recomendaciones
Verifica integridad de código, importaciones y configuración
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

def verificar_importaciones():
    """Verifica que todas las importaciones funcionen"""
    print("="*60)
    print("VERIFICANDO IMPORTACIONES")
    print("="*60)
    
    errores = []
    
    # 1. Modelos
    try:
        from app.models.recomendacion import (
            PerfilNinoVectorizado,
            PerfilActividadVectorizada,
            HistorialProgreso,
            RecomendacionActividad,
            AsignacionTerapeutaTOPSIS
        )
        print("✓ Modelos de recomendación importados correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando modelos: {e}")
    
    # 2. Servicio Gemini
    try:
        from app.services.gemini_service import gemini_service
        print("✓ Servicio Gemini importado correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando Gemini service: {e}")
    
    # 3. Servicio TOPSIS
    try:
        from app.services import topsis_service
        print("✓ Servicio TOPSIS importado correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando TOPSIS service: {e}")
    
    # 4. Servicio de Recomendación
    try:
        from app.services.recomendacion_service import RecomendacionService
        print("✓ Servicio de Recomendación importado correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando Recomendación service: {e}")
    
    # 5. Schemas
    try:
        from app.schemas.recomendacion import (
            RecomendacionActividadesResponse,
            SeleccionTerapeutaResponse,
            RecomendacionCompletaResponse
        )
        print("✓ Schemas de recomendación importados correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando schemas: {e}")
    
    # 6. API Router
    try:
        from app.api.v1 import recomendaciones
        print("✓ Router de API importado correctamente")
    except Exception as e:
        errores.append(f"✗ Error importando API router: {e}")
    
    return errores


def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("\n" + "="*60)
    print("VERIFICANDO DEPENDENCIAS")
    print("="*60)
    
    errores = []
    
    # Google Generative AI
    try:
        import google.generativeai as genai
        print("✓ google-generativeai instalado")
    except ImportError:
        errores.append("✗ google-generativeai NO instalado. Ejecutar: pip install google-generativeai")
    
    # NumPy
    try:
        import numpy as np
        print("✓ numpy instalado")
    except ImportError:
        errores.append("✗ numpy NO instalado. Ejecutar: pip install numpy")
    
    # SQLAlchemy
    try:
        from sqlalchemy.orm import Session
        print("✓ SQLAlchemy instalado")
    except ImportError:
        errores.append("✗ SQLAlchemy NO instalado")
    
    # FastAPI
    try:
        from fastapi import APIRouter
        print("✓ FastAPI instalado")
    except ImportError:
        errores.append("✗ FastAPI NO instalado")
    
    return errores


def verificar_configuracion():
    """Verifica la configuración"""
    print("\n" + "="*60)
    print("VERIFICANDO CONFIGURACIÓN")
    print("="*60)
    
    import os
    from dotenv import load_dotenv
    
    # Cargar .env
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print("✓ Archivo .env encontrado")
    else:
        print("⚠ Archivo .env no encontrado")
    
    # Verificar GEMINI_API_KEY
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✓ GEMINI_API_KEY configurada")
    else:
        print("⚠ GEMINI_API_KEY NO configurada")
        print("  Agregar en .env: GEMINI_API_KEY=tu_api_key")
    
    # Verificar DATABASE_URL
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        print("✓ DATABASE_URL configurada")
    else:
        print("⚠ DATABASE_URL NO configurada")


def verificar_estructura_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("\n" + "="*60)
    print("VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    print("="*60)
    
    archivos_requeridos = [
        "app/models/recomendacion.py",
        "app/services/gemini_service.py",
        "app/services/recomendacion_service.py",
        "app/api/v1/recomendaciones.py",
        "app/schemas/recomendacion.py",
        "scripts/crear_tablas_recomendaciones.sql",
        "scripts/init_sistema_recomendaciones.py"
    ]
    
    faltantes = []
    
    for archivo in archivos_requeridos:
        ruta = ROOT_DIR / archivo
        if ruta.exists():
            print(f"✓ {archivo}")
        else:
            print(f"✗ {archivo} - NO ENCONTRADO")
            faltantes.append(archivo)
    
    return faltantes


def verificar_funciones_topsis():
    """Verifica que las funciones de TOPSIS existan"""
    print("\n" + "="*60)
    print("VERIFICANDO FUNCIONES TOPSIS")
    print("="*60)
    
    try:
        from app.services import topsis_service
        
        # Verificar que exista la función calcular_ranking_terapeutas
        if hasattr(topsis_service, 'calcular_ranking_terapeutas'):
            print("✓ Función calcular_ranking_terapeutas existe")
        else:
            print("✗ Función calcular_ranking_terapeutas NO encontrada")
            return False
        
        # Verificar función aplicar_topsis
        if hasattr(topsis_service, 'aplicar_topsis'):
            print("✓ Función aplicar_topsis existe")
        else:
            print("✗ Función aplicar_topsis NO encontrada")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Error verificando TOPSIS: {e}")
        return False


def main():
    """Función principal"""
    print("\n" + "="*70)
    print(" "*10 + "VERIFICACIÓN DEL SISTEMA DE RECOMENDACIONES")
    print("="*70)
    
    errores_totales = []
    
    # 1. Verificar dependencias
    errores_deps = verificar_dependencias()
    errores_totales.extend(errores_deps)
    
    # 2. Verificar estructura de archivos
    archivos_faltantes = verificar_estructura_archivos()
    if archivos_faltantes:
        errores_totales.append(f"Archivos faltantes: {len(archivos_faltantes)}")
    
    # 3. Verificar importaciones
    errores_imports = verificar_importaciones()
    errores_totales.extend(errores_imports)
    
    # 4. Verificar funciones TOPSIS
    if not verificar_funciones_topsis():
        errores_totales.append("Funciones TOPSIS incompletas")
    
    # 5. Verificar configuración
    verificar_configuracion()
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    if errores_totales:
        print(f"\n⚠ Se encontraron {len(errores_totales)} problemas:\n")
        for error in errores_totales:
            print(f"  • {error}")
        print("\n" + "="*70)
        print("Estado: REQUIERE ATENCIÓN")
        print("="*70)
        return False
    else:
        print("\n✅ Todas las verificaciones pasaron correctamente")
        print("\n" + "="*70)
        print("Estado: SISTEMA LISTO PARA USAR")
        print("="*70)
        print("\nPróximos pasos:")
        print("  1. Configurar GEMINI_API_KEY en .env (si aún no está)")
        print("  2. Ejecutar: python scripts/init_sistema_recomendaciones.py")
        print("  3. Iniciar servidor: uvicorn app.main:app --reload")
        print("  4. Acceder a Swagger: http://localhost:8000/docs")
        return True


if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)

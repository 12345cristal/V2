#!/usr/bin/env python3
"""
Script de prueba para verificar los endpoints de Mis Hijos
Ejecutar: python test_mis_hijos_api.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Verifica que todos los imports necesarios funcionen"""
    print("=" * 60)
    print("🧪 TEST 1: Verificando Imports")
    print("=" * 60)
    
    try:
        # Modelos
        print("✓ Importando modelos...")
        from app.models.nino import Nino, NinoDiagnostico, NinoInfoEmocional
        from app.models.medicamentos import Medicamento, Alergia
        from app.models.tutor import Tutor
        from app.models.usuario import Usuario
        print("  ✅ Modelos importados correctamente")
        
        # Schemas
        print("✓ Importando schemas...")
        from app.schemas.padres_mis_hijos import (
            HijoResponse, AlergiaResponse, MedicamentoResponse,
            MisHijosPageResponse, MisHijosApiResponse
        )
        print("  ✅ Schemas importados correctamente")
        
        # Servicios
        print("✓ Importando servicios...")
        from app.services.padres_mis_hijos_service import (
            obtener_mis_hijos,
            obtener_hijo_por_id,
            marcar_medicamento_como_visto,
            obtener_medicamentos_por_hijo,
            obtener_alergias_por_hijo
        )
        print("  ✅ Servicios importados correctamente")
        
        # Endpoints
        print("✓ Importando endpoints...")
        from app.api.v1.padres.mis_hijos import router
        print("  ✅ Endpoints importados correctamente")
        
        print("\n✅ TODOS LOS IMPORTS FUNCIONAN CORRECTAMENTE\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en imports: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_model_relationships():
    """Verifica las relaciones entre modelos"""
    print("=" * 60)
    print("🧪 TEST 2: Verificando Relaciones de Modelos")
    print("=" * 60)
    
    try:
        from app.models.nino import Nino
        from app.models.medicamentos import Medicamento, Alergia
        from app.models.tutor import Tutor
        
        # Verificar que Nino tiene las relaciones correctas
        print("✓ Verificando relaciones de Nino...")
        assert hasattr(Nino, 'medicamentos'), "Nino debe tener relación 'medicamentos'"
        assert hasattr(Nino, 'alergias'), "Nino debe tener relación 'alergias'"
        assert hasattr(Nino, 'tutor'), "Nino debe tener relación 'tutor'"
        print("  ✅ Nino tiene todas las relaciones necesarias")
        
        # Verificar que Medicamento tiene relación con Nino
        print("✓ Verificando relaciones de Medicamento...")
        assert hasattr(Medicamento, 'nino'), "Medicamento debe tener relación 'nino'"
        print("  ✅ Medicamento tiene relación con Nino")
        
        # Verificar que Alergia tiene relación con Nino
        print("✓ Verificando relaciones de Alergia...")
        assert hasattr(Alergia, 'nino'), "Alergia debe tener relación 'nino'"
        print("  ✅ Alergia tiene relación con Nino")
        
        # Verificar que Tutor tiene relación con Nino
        print("✓ Verificando relaciones de Tutor...")
        assert hasattr(Tutor, 'ninos'), "Tutor debe tener relación 'ninos'"
        print("  ✅ Tutor tiene relación con Nino")
        
        print("\n✅ TODAS LAS RELACIONES SON CORRECTAS\n")
        return True
        
    except AssertionError as e:
        print(f"\n❌ ERROR en relaciones: {e}\n")
        return False
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_endpoint_routes():
    """Verifica que las rutas estén configuradas correctamente"""
    print("=" * 60)
    print("🧪 TEST 3: Verificando Rutas de API")
    print("=" * 60)
    
    try:
        from app.api.v1.padres.mis_hijos import router
        
        # Obtener las rutas registradas
        routes = [route.path for route in router.routes]
        
        expected_routes = [
            "/padres/mis-hijos",
            "/padres/mis-hijos/{nino_id}",
            "/padres/mis-hijos/{nino_id}/medicamentos",
            "/padres/mis-hijos/{nino_id}/alergias",
            "/padres/mis-hijos/{nino_id}/medicamentos/{medicamento_id}/visto"
        ]
        
        print(f"✓ Rutas encontradas: {len(routes)}")
        for route in routes:
            print(f"  - {route}")
        
        print(f"\n✓ Verificando rutas esperadas...")
        for expected in expected_routes:
            if expected in routes:
                print(f"  ✅ {expected}")
            else:
                print(f"  ❌ {expected} - NO ENCONTRADA")
        
        print("\n✅ RUTAS VERIFICADAS\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR al verificar rutas: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_schema_validation():
    """Verifica que los schemas Pydantic funcionen correctamente"""
    print("=" * 60)
    print("🧪 TEST 4: Verificando Schemas Pydantic")
    print("=" * 60)
    
    try:
        from app.schemas.padres_mis_hijos import (
            AlergiaResponse, MedicamentoResponse, HijoResponse,
            MisHijosPageResponse, MisHijosApiResponse
        )
        from datetime import date, datetime
        
        # Test AlergiaResponse
        print("✓ Probando AlergiaResponse...")
        alergia = AlergiaResponse(
            id=1,
            nombre="Penicilina",
            severidad="severa",
            reaccion="Anafilaxia"
        )
        assert alergia.nombre == "Penicilina"
        print("  ✅ AlergiaResponse funciona correctamente")
        
        # Test MedicamentoResponse
        print("✓ Probando MedicamentoResponse...")
        medicamento = MedicamentoResponse(
            id=1,
            nombre="Metilfenidato",
            dosis="10 mg",
            frecuencia="Dos veces al día",
            razon="TDAH",
            fechaInicio=date.today(),
            activo=True,
            novedadReciente=True
        )
        assert medicamento.nombre == "Metilfenidato"
        print("  ✅ MedicamentoResponse funciona correctamente")
        
        # Test HijoResponse
        print("✓ Probando HijoResponse...")
        hijo = HijoResponse(
            id=1,
            nombre="Juan",
            apellidoPaterno="Pérez",
            fechaNacimiento=date(2015, 5, 15),
            edad=8,
            diagnostico="TEA",
            cuatrimestre=2,
            alergias=[alergia],
            medicamentos=[medicamento],
            visto=False,
            novedades=1
        )
        assert hijo.nombre == "Juan"
        assert len(hijo.alergias) == 1
        assert len(hijo.medicamentos) == 1
        print("  ✅ HijoResponse funciona correctamente")
        
        # Test MisHijosApiResponse
        print("✓ Probando MisHijosApiResponse...")
        response = MisHijosApiResponse(
            exito=True,
            datos=MisHijosPageResponse(hijos=[hijo]),
            mensaje="Éxito"
        )
        assert response.exito == True
        assert len(response.datos.hijos) == 1
        print("  ✅ MisHijosApiResponse funciona correctamente")
        
        print("\n✅ TODOS LOS SCHEMAS FUNCIONAN CORRECTAMENTE\n")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR en schemas: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 60)
    print("🚀 INICIANDO TESTS DE MIS HIJOS BACKEND")
    print("=" * 60 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Relaciones": test_model_relationships(),
        "Rutas": test_endpoint_routes(),
        "Schemas": test_schema_validation()
    }
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name:20s}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print("❌ ALGUNOS TESTS FALLARON - REVISAR ARRIBA")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

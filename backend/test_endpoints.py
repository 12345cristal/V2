#!/usr/bin/env python3
"""
Script de prueba de endpoints del backend
Sin autenticación para validar estructura básica
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Probar endpoint de salud"""
    print("\n[TEST] GET /health")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Body: {json.dumps(resp.json(), indent=2)}")
        return resp.status_code == 200
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_docs():
    """Probar que Swagger está disponible"""
    print("\n[TEST] GET /docs (Swagger)")
    try:
        resp = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"  Status: {resp.status_code}")
        print(f"  Swagger disponible: {resp.status_code == 200}")
        return resp.status_code == 200
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_openapi():
    """Probar schema OpenAPI"""
    print("\n[TEST] GET /openapi.json")
    try:
        resp = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"  Status: {resp.status_code}")
            print(f"  Rutas disponibles: {len(data.get('paths', {}))}")
            
            # Mostrar rutas de terapeuta
            terapeuta_routes = [k for k in data.get('paths', {}).keys() if '/terapeuta' in k]
            print(f"  Rutas de Terapeuta ({len(terapeuta_routes)}):")
            for route in sorted(terapeuta_routes):
                print(f"    - {route}")
            return True
        else:
            print(f"  Status: {resp.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE BACKEND - AUTISMO MOCHIS IA")
    print("=" * 60)
    
    tests = [
        test_health(),
        test_docs(),
        test_openapi(),
    ]
    
    print("\n" + "=" * 60)
    print(f"Resultados: {sum(tests)}/{len(tests)} pasaron")
    print("=" * 60)
    
    if all(tests):
        print("\n✅ Backend está corriendo correctamente")
        exit(0)
    else:
        print("\n❌ Hay errores en el backend")
        exit(1)

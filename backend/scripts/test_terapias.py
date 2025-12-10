"""
Script de prueba para el módulo de terapias
Ejecutar después de inicializar los catálogos
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# ⚠️ IMPORTANTE: Reemplaza con tu token de autenticación
TOKEN = "tu_token_aqui"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def test_listar_terapias():
    """Prueba: Listar todas las terapias"""
    print("\n" + "="*60)
    print("TEST: Listar Terapias")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/terapias", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        terapias = response.json()
        print(f"✓ Terapias encontradas: {len(terapias)}")
        for t in terapias:
            print(f"  - {t['nombre']} ({t['estado']})")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_crear_terapia():
    """Prueba: Crear una nueva terapia"""
    print("\n" + "="*60)
    print("TEST: Crear Terapia")
    print("="*60)
    
    data = {
        "nombre": "Terapia de Prueba",
        "descripcion": "Esta es una terapia de prueba",
        "tipo_id": 1,
        "duracion_minutos": 45,
        "objetivo_general": "Objetivo de prueba"
    }
    
    response = requests.post(f"{BASE_URL}/terapias", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        terapia = response.json()
        print(f"✓ Terapia creada: {terapia['nombre']} (ID: {terapia['id_terapia']})")
        return terapia['id_terapia']
    else:
        print(f"✗ Error: {response.text}")
        return None

def test_obtener_terapia(terapia_id):
    """Prueba: Obtener una terapia específica"""
    print("\n" + "="*60)
    print(f"TEST: Obtener Terapia ID {terapia_id}")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/terapias/{terapia_id}", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        terapia = response.json()
        print(f"✓ Terapia: {terapia['nombre']}")
        print(f"  Descripción: {terapia['descripcion']}")
        print(f"  Duración: {terapia['duracion_minutos']} min")
        print(f"  Estado: {terapia['estado']}")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_actualizar_terapia(terapia_id):
    """Prueba: Actualizar una terapia"""
    print("\n" + "="*60)
    print(f"TEST: Actualizar Terapia ID {terapia_id}")
    print("="*60)
    
    data = {
        "nombre": "Terapia de Prueba Actualizada",
        "descripcion": "Descripción actualizada",
        "duracion_minutos": 60
    }
    
    response = requests.put(f"{BASE_URL}/terapias/{terapia_id}", headers=headers, json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        terapia = response.json()
        print(f"✓ Terapia actualizada: {terapia['nombre']}")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_cambiar_estado(terapia_id):
    """Prueba: Cambiar estado de una terapia"""
    print("\n" + "="*60)
    print(f"TEST: Cambiar Estado Terapia ID {terapia_id}")
    print("="*60)
    
    response = requests.patch(f"{BASE_URL}/terapias/{terapia_id}/estado", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        terapia = response.json()
        print(f"✓ Estado cambiado a: {terapia['estado']}")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_personal_sin_terapia():
    """Prueba: Listar personal sin terapia asignada"""
    print("\n" + "="*60)
    print("TEST: Personal Sin Terapia")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/personal/sin-terapia", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        personal = response.json()
        print(f"✓ Personal sin terapia: {len(personal)}")
        for p in personal[:5]:  # Mostrar solo los primeros 5
            print(f"  - {p['nombre_completo']} ({p['especialidad']})")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_personal_asignado():
    """Prueba: Listar personal con terapias asignadas"""
    print("\n" + "="*60)
    print("TEST: Personal Asignado")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/terapias/personal-asignado", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        personal = response.json()
        print(f"✓ Personal con terapia asignada: {len(personal)}")
        for p in personal[:5]:  # Mostrar solo los primeros 5
            print(f"  - {p['nombre_completo']} → {p['terapia']}")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def test_tipos_terapia():
    """Prueba: Listar tipos de terapia"""
    print("\n" + "="*60)
    print("TEST: Tipos de Terapia")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/terapias/catalogos/tipos", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        tipos = response.json()
        print(f"✓ Tipos de terapia: {len(tipos)}")
        for t in tipos:
            print(f"  - {t['codigo']}: {t['nombre']}")
    else:
        print(f"✗ Error: {response.text}")
    
    return response.status_code == 200

def main():
    """Función principal"""
    print("\n" + "🚀"*30)
    print("PRUEBAS DEL MÓDULO DE TERAPIAS")
    print("🚀"*30)
    
    if TOKEN == "tu_token_aqui":
        print("\n⚠️  ERROR: Debes configurar tu TOKEN en el script")
        print("   1. Inicia sesión en la API")
        print("   2. Copia el token")
        print("   3. Reemplaza 'tu_token_aqui' con tu token")
        return
    
    resultados = []
    
    # Tests de lectura
    resultados.append(("Listar Terapias", test_listar_terapias()))
    resultados.append(("Tipos de Terapia", test_tipos_terapia()))
    resultados.append(("Personal Sin Terapia", test_personal_sin_terapia()))
    resultados.append(("Personal Asignado", test_personal_asignado()))
    
    # Tests de escritura
    terapia_id = test_crear_terapia()
    if terapia_id:
        resultados.append(("Crear Terapia", True))
        resultados.append(("Obtener Terapia", test_obtener_terapia(terapia_id)))
        resultados.append(("Actualizar Terapia", test_actualizar_terapia(terapia_id)))
        resultados.append(("Cambiar Estado", test_cambiar_estado(terapia_id)))
    else:
        resultados.append(("Crear Terapia", False))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    
    exitosos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✓ PASS" if resultado else "✗ FAIL"
        print(f"{estado} - {nombre}")
    
    print("\n" + "="*60)
    print(f"Resultado: {exitosos}/{total} pruebas exitosas")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error en las pruebas: {e}")

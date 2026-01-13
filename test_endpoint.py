#!/usr/bin/env python3
import requests
import json

# Probar el endpoint de terapeutas por terapia
# Por ejemplo, Terapia ID 1 (Logopedia General)
try:
    response = requests.get('http://localhost:8000/api/v1/personal/por-terapia/1')
    
    if response.status_code == 200:
        terapeutas = response.json()
        print("✓ Endpoint funcionando")
        print(f"✓ Terapeutas especializados en Terapia ID 1 (Logopedia General):")
        for t in terapeutas:
            print(f"  - {t.get('nombres', 'N/A')} ({t.get('especialidad_principal', 'N/A')})")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"✗ Error: {str(e)}")

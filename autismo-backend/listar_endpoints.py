"""
Script para listar todos los endpoints disponibles en el backend
"""

from app.main import app
from fastapi.routing import APIRoute

print("\n" + "="*80)
print("ENDPOINTS DISPONIBLES EN EL BACKEND")
print("="*80 + "\n")

endpoints = []

for route in app.routes:
    if isinstance(route, APIRoute):
        methods = ", ".join(route.methods)
        path = route.path
        name = route.name
        endpoints.append({
            "methods": methods,
            "path": path,
            "name": name
        })

# Agrupar por método
for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
    method_endpoints = [e for e in endpoints if method in e["methods"]]
    if method_endpoints:
        print(f"\n[{method}] ENDPOINTS ({len(method_endpoints)}):")
        print("-" * 80)
        for ep in method_endpoints:
            print(f"  {ep['methods']:12} {ep['path']:50} ({ep['name']})")

print("\n" + "="*80)
print(f"TOTAL DE ENDPOINTS: {len(endpoints)}")
print("="*80 + "\n")

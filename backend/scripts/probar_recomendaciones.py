"""
Script para probar el sistema de recomendaciones completo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.recomendacion_actividades_service import RecomendacionActividadesService
from app.db.session import SessionLocal

print("=" * 80)
print("PRUEBA DEL SISTEMA DE RECOMENDACIONES")
print("=" * 80)

db = SessionLocal()
service = RecomendacionActividadesService(db)

try:
    # Probar con el niño ID 1
    nino_id = 1
    
    print(f"\n[1/3] Generando recomendaciones para niño {nino_id}...")
    
    resultado = service.generar_recomendaciones(
        nino_id=nino_id,
        top_n=5,
        filtrar_por_area="motor",
        nivel_dificultad_max=2
    )
    
    print(f"\n✓ Recomendaciones generadas exitosamente")
    print(f"  Niño: {resultado.nombre_nino}")
    print(f"  Total recomendaciones: {resultado.total_recomendaciones}")
    print(f"  Fecha: {resultado.fecha_generacion}")
    
    print("\n[2/3] Actividades recomendadas:")
    for i, rec in enumerate(resultado.recomendaciones, 1):
        print(f"\n  {i}. {rec.nombre}")
        print(f"     Área: {rec.area_desarrollo} | Dificultad: {rec.dificultad} | Score: {rec.score_similitud:.2%}")
        print(f"     Razón: {rec.razon_recomendacion}")
        print(f"     Duración: {rec.duracion_minutos} min")
    
    # Probar sin filtros
    print(f"\n[3/3] Generando recomendaciones sin filtros...")
    
    resultado2 = service.generar_recomendaciones(
        nino_id=nino_id,
        top_n=10
    )
    
    print(f"\n✓ Recomendaciones generales:")
    print(f"  Total: {resultado2.total_recomendaciones}")
    
    print("\n  Top 5 mejores scores:")
    for i, rec in enumerate(resultado2.recomendaciones[:5], 1):
        print(f"    {i}. {rec.nombre} - {rec.score_similitud:.2%} ({rec.area_desarrollo})")
    
    print("\n" + "=" * 80)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()

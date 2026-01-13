#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para conectar terapeutas, terapias y niños de forma realista
"""

import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

from app.db.session import SessionLocal
from app.models.personal import Personal
from app.models.terapia import Terapia, TipoTerapia, TerapiaPersonal, TerapiaNino
from app.models.nino import Nino

db = SessionLocal()

try:
    print("=" * 60)
    print("CONECTANDO DATOS DE FORMA REALISTA")
    print("=" * 60)
    
    # Obtener datos
    terapeutas = db.query(Personal).filter(Personal.estado_laboral == "ACTIVO").all()
    terapias = db.query(Terapia).all()
    ninos = db.query(Nino).all()
    
    print(f"\nDatos actuales:")
    print(f"  Terapeutas activos: {len(terapeutas)}")
    print(f"  Terapias: {len(terapias)}")
    print(f"  Ninos: {len(ninos)}")
    
    if not terapeutas or not terapias or not ninos:
        print("\n[ERROR] No hay datos suficientes")
        sys.exit(1)
    
    # PASO 1: Conectar terapeutas con terapias
    print("\n" + "-" * 60)
    print("PASO 1: CONECTANDO TERAPEUTAS CON TERAPIAS")
    print("-" * 60)
    
    # Limpiar relaciones anteriores
    db.query(TerapiaPersonal).delete()
    db.commit()
    
    # Crear nuevas relaciones: cada terapeuta con 2-3 terapias
    asignaciones_creadas = 0
    for idx, terapeuta in enumerate(terapeutas):
        nombre = f"{terapeuta.nombres} {terapeuta.apellido_paterno}".strip()
        
        # Asignar 2-3 terapias a cada terapeuta
        num_terapias = 2 if idx % 3 == 0 else 3
        terapias_asignadas = terapias[idx % len(terapias): (idx % len(terapias)) + num_terapias]
        if not terapias_asignadas:
            terapias_asignadas = terapias[:num_terapias]
        
        for terapia in terapias_asignadas:
            tp = TerapiaPersonal(
                personal_id=terapeuta.id,
                terapia_id=terapia.id,
                activo=1
            )
            db.add(tp)
            asignaciones_creadas += 1
        
        print(f"[+] {nombre}: {len(terapias_asignadas)} terapias")
    
    db.commit()
    print(f"\n[OK] Creadas {asignaciones_creadas} conexiones terapeuta-terapia")
    
    # PASO 2: Conectar niños con terapeutas y terapias
    print("\n" + "-" * 60)
    print("PASO 2: CONECTANDO NINOS CON TERAPIAS Y TERAPEUTAS")
    print("-" * 60)
    
    # Limpiar relaciones anteriores
    db.query(TerapiaNino).delete()
    db.commit()
    
    # Crear nuevas relaciones: cada niño con 1-2 terapias y un terapeuta
    asignaciones_nino_creadas = 0
    for idx, nino in enumerate(ninos):
        nombre = f"{nino.nombre} {nino.apellido_paterno}".strip()
        
        # Asignar 1-2 terapias a cada niño
        num_terapias = 1 if idx % 3 == 0 else 2
        terapias_nino = terapias[idx % len(terapias): (idx % len(terapias)) + num_terapias]
        if not terapias_nino:
            terapias_nino = [terapias[0]]
        
        # Asignar un terapeuta (cualquiera activo)
        terapeuta = terapeutas[idx % len(terapeutas)]
        
        for terapia in terapias_nino:
            tn = TerapiaNino(
                nino_id=nino.id,
                terapia_id=terapia.id,
                terapeuta_id=terapeuta.id,
                activo=1
            )
            db.add(tn)
            asignaciones_nino_creadas += 1
        
        terapeuta_nombre = f"{terapeuta.nombres} {terapeuta.apellido_paterno}".strip()
        print(f"[+] {nombre}: {len(terapias_nino)} terapias con {terapeuta_nombre}")
    
    db.commit()
    print(f"\n[OK] Creadas {asignaciones_nino_creadas} asignaciones nino-terapia-terapeuta")
    
    # RESUMEN FINAL
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    final_tp = db.query(TerapiaPersonal).count()
    final_tn = db.query(TerapiaNino).count()
    
    print(f"\nEspecialidades de terapeutas: {final_tp}")
    print(f"Asignaciones de ninos: {final_tn}")
    print(f"\n[SUCCESS] Base de datos conectada exitosamente")
    
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    db.rollback()
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

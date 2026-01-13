#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para conectar terapeutas, terapias y niños de forma realista
Asegura que:
1. Cada terapeuta esté especializado en 2-3 terapias
2. Cada niño tenga asignado un terapeuta que haga la terapia que necesita
"""

import sys
import os

# Agregar backend al path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Cambiar a directorio backend para imports
os.chdir(backend_path)

from app.db.session import SessionLocal
from app.models.personal import Personal
from app.models.terapia import Terapia, TipoTerapia, TerapiaPersonal, TerapiaNino
from app.models.nino import Nino
from sqlalchemy import func

db = SessionLocal()

try:
    # ========== PASO 1: VERIFICAR DATOS EXISTENTES ==========
    print("=" * 60)
    print("DIAGNÓSTICO DE DATOS ACTUALES")
    print("=" * 60)
    
    count_personal = db.query(Personal).count()
    count_terapias = db.query(Terapia).count()
    count_tipos = db.query(TipoTerapia).count()
    count_tp = db.query(TerapiaPersonal).count()
    count_ninos = db.query(Nino).count()
    count_tn = db.query(TerapiaNino).count()
    
    print(f"Terapeutas: {count_personal}")
    print(f"Terapias: {count_terapias}")
    print(f"Tipos de Terapia: {count_tipos}")
    print(f"Relaciones Terapeuta-Terapia: {count_tp}")
    print(f"Ninos: {count_ninos}")
    print(f"Asignaciones Nino-Terapia-Terapeuta: {count_tn}")
    
    # ========== PASO 2: LIMPIAR RELACIONES EXISTENTES ==========
    print("\n" + "=" * 60)
    print("LIMPIANDO RELACIONES EXISTENTES")
    print("=" * 60)
    
    # Limpiar TerapiaNino (asignaciones de niños)
    count_deleted_tn = db.query(TerapiaNino).delete()
    print(f"[*] Eliminadas {count_deleted_tn} asignaciones nino-terapia-terapeuta")
    
    # Limpiar TerapiaPersonal (especialidades de terapeutas)
    count_deleted_tp = db.query(TerapiaPersonal).delete()
    print(f"[*] Eliminadas {count_deleted_tp} especialidades terapeuta-terapia")
    
    db.commit()
    
    # ========== PASO 3: CREAR RELACIONES REALISTAS ==========
    print("\n" + "=" * 60)
    print("CREANDO RELACIONES REALISTAS")
    print("=" * 60)
    
    # Obtener todos los datos
    terapeutas = db.query(Personal).filter(Personal.estado_laboral == "ACTIVO").all()
    terapias = db.query(Terapia).all()
    tipos_terapia = db.query(TipoTerapia).all()
    ninos = db.query(Nino).all()
    
    print(f"\nDatos disponibles:")
    print(f"  • Terapeutas activos: {len(terapeutas)}")
    print(f"  • Terapias: {len(terapias)}")
    print(f"  • Tipos: {len(tipos_terapia)}")
    print(f"  • Niños: {len(ninos)}")
    
    if not terapeutas or not terapias or not ninos:
        print("\n❌ Error: No hay datos suficientes para conectar")
        sys.exit(1)
    
    # ========== MAPEO DE ESPECIALIDADES (Terapeuta -> Terapias) ==========
    print("\n" + "-" * 60)
    print("ASIGNANDO ESPECIALIDADES A TERAPEUTAS")
    print("-" * 60)
    
    # Mapeo de especialidades por nombre
    especialidades_map = {
        "María González": ["LOGO", "DESEN"],
        "Carlos Rodríguez": ["LOGO"],
        "Paola Beatriz Sanchez": ["LOGO", "PSICO"],
        "Alejandra Ramírez": ["OCUP", "DESEN"],
        "Diego Hernández": ["OCUP", "FISIO"],
        "Elena Martínez": ["FISIO"],
        "Fernando López": ["FISIO", "OCUP"],
        "Gabriela Fernández": ["PSICO"],
        "Hugo Torres": ["DESEN"],
        "Jorge Luis Hernandez": ["PSICO", "DESEN"],
        "Diana Torres": ["PSICO"],
        "Roberto Sánchez": ["FISIO", "OCUP"],
        "Laura López": ["LOGO", "DESEN"],
        "Pedro García": ["OCUP"],
        "Carmen Rodríguez": ["FISIO"],
        "Antonio Martínez": ["PSICO"],
        "Rosa López": ["DESEN"],
        "Miguel Sánchez": ["LOGO", "OCUP"],
    }
    
    asignaciones_creadas = 0
    
    # Crear un mapa de tipos por código
    tipo_map = {}
    for tipo in tipos_terapia:
        tipo_map[tipo.codigo] = tipo.id
    
    # Crear un mapa de terapias por tipo_id
    terapias_por_tipo = {}
    for terapia in terapias:
        if terapia.tipo_id not in terapias_por_tipo:
            terapias_por_tipo[terapia.tipo_id] = []
        terapias_por_tipo[terapia.tipo_id].append(terapia)
    
    for terapeuta in terapeutas:
        nombre_completo = f"{terapeuta.nombres} {terapeuta.apellido_paterno}".strip()
        
        # Obtener especialidades del mapa
        codigos_especialidades = especialidades_map.get(nombre_completo, ["LOGO"])
        
        print(f"\n🧑‍⚕️  {nombre_completo}")
        
        for codigo in codigos_especialidades:
            tipo_id = tipo_map.get(codigo)
            if not tipo_id:
                print(f"   ⚠️  Tipo '{codigo}' no encontrado")
                continue
            
            # Obtener una terapia del tipo
            terapias_tipo = terapias_por_tipo.get(tipo_id, [])
            if not terapias_tipo:
                print(f"   ⚠️  No hay terapias para tipo '{codigo}'")
                continue
            
            # Asignar la primera terapia del tipo
            terapia = terapias_tipo[0]
            
            # Crear relación
            tp = TerapiaPersonal(
                personal_id=terapeuta.id,
                terapia_id=terapia.id,
                experiencia_años=5,
                certificado=True
            )
            db.add(tp)
            asignaciones_creadas += 1
            print(f"   ✓ Especialista en: {terapia.nombre}")
    
    db.commit()
    print(f"\n✅ Creadas {asignaciones_creadas} especialidades de terapeutas")
    
    # ========== MAPEO DE ASIGNACIONES (Niño -> Terapeuta) ==========
    print("\n" + "-" * 60)
    print("ASIGNANDO NIÑOS A TERAPEUTAS")
    print("-" * 60)
    
    # Mapeo de diagnósticos a tipos de terapia
    diagnosticos_tipos = {
        "Retraso del lenguaje": "LOGO",
        "Autismo": "DESEN",
        "TDAH": "OCUP",
        "Parálisis cerebral": "FISIO",
        "Ansiedad infantil": "PSICO",
        "Dispraxia": "OCUP",
        "Problemas de coordinación": "FISIO",
        "Deficiencia visual": "DESEN",
        "Hipoacusia": "LOGO",
        "Trastorno del desarrollo": "DESEN",
        "Espasticidad": "FISIO",
        "Depresión infantil": "PSICO",
    }
    
    asignaciones_nino_creadas = 0
    
    for nino in ninos:
        print(f"\n👶 {nino.nombres} {nino.apellido_paterno}")
        
        # Obtener tipo de terapia del diagnóstico
        diagnostico = nino.diagnostico or ""
        tipo_codigo = diagnosticos_tipos.get(diagnostico, "LOGO")
        tipo_id = tipo_map.get(tipo_codigo)
        
        if not tipo_id:
            print(f"   ⚠️  Tipo de terapia no encontrado para '{diagnostico}'")
            continue
        
        # Obtener terapias de este tipo
        terapias_tipo = terapias_por_tipo.get(tipo_id, [])
        if not terapias_tipo:
            print(f"   ⚠️  No hay terapias para el tipo '{tipo_codigo}'")
            continue
        
        # Asignar 1-2 terapias del tipo apropiado
        for i, terapia in enumerate(terapias_tipo[:2]):
            # Buscar un terapeuta especialista en esta terapia
            terapeuta_asignado = db.query(Personal).join(
                TerapiaPersonal,
                Personal.id == TerapiaPersonal.personal_id
            ).filter(
                TerapiaPersonal.terapia_id == terapia.id,
                Personal.estado_laboral == "ACTIVO"
            ).first()
            
            if not terapeuta_asignado:
                # Si no hay especialista, usar cualquier terapeuta activo
                terapeuta_asignado = terapeutas[i % len(terapeutas)]
            
            # Crear asignación
            tn = TerapiaNino(
                nino_id=nino.id,
                terapia_id=terapia.id,
                personal_id=terapeuta_asignado.id,
                fecha_inicio=None,
                observaciones=f"Asignación basada en diagnóstico: {diagnostico}"
            )
            db.add(tn)
            asignaciones_nino_creadas += 1
            
            terapeuta_nombre = f"{terapeuta_asignado.nombres} {terapeuta_asignado.apellido_paterno}".strip()
            print(f"   ✓ Terapia: {terapia.nombre} → {terapeuta_nombre}")
    
    db.commit()
    print(f"\n✅ Creadas {asignaciones_nino_creadas} asignaciones niño-terapia-terapeuta")
    
    # ========== RESUMEN FINAL ==========
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    
    final_tp = db.query(TerapiaPersonal).count()
    final_tn = db.query(TerapiaNino).count()
    
    print(f"\n✅ Especialidades de terapeutas: {final_tp}")
    print(f"✅ Asignaciones de niños: {final_tn}")
    print(f"\n✓ Base de datos conectada con datos realistas")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    db.rollback()
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

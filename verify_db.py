#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.terapia import Terapia, TerapiaPersonal
from app.models.personal import Personal
from app.db.session import SessionLocal

# Verificar datos en la base de datos
db = SessionLocal()

print("=" * 60)
print("VERIFICACIÓN DE DATOS EN BASE DE DATOS")
print("=" * 60)

# Contar registros
print("\n1. CONTEO DE REGISTROS:")
print(f"   Terapeutas: {db.query(Personal).count()}")
print(f"   Terapias: {db.query(Terapia).count()}")
print(f"   Asignaciones Terapeuta-Terapia: {db.query(TerapiaPersonal).count()}")

# Mostrar asignaciones por terapia
print("\n2. TERAPEUTAS POR TERAPIA:")
terapias = db.query(Terapia).all()
for terapia in terapias:
    terapeutas = db.query(Personal).join(
        TerapiaPersonal, TerapiaPersonal.personal_id == Personal.id
    ).filter(TerapiaPersonal.terapia_id == terapia.id).all()
    
    print(f"\n   {terapia.nombre}:")
    if terapeutas:
        for t in terapeutas:
            print(f"     - {t.nombres} {t.apellido_paterno} ({t.especialidad_principal})")
    else:
        print(f"     - Sin asignaciones")

print("\n" + "=" * 60)
db.close()

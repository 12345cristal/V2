#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos coherentes
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.db.session import SessionLocal
from app.models.terapia import Terapia, TerapiaPersonal, TerapiaNino, TipoTerapia
from app.models.personal import Personal
from app.models.nino import Nino
from app.models.rol import Rol
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

db = SessionLocal()

def poblar_tipos_terapia():
    """Inserta los tipos de terapia"""
    tipos = [
        {'codigo': 'LOGO', 'nombre': 'Logopedia'},
        {'codigo': 'OCUP', 'nombre': 'Terapia Ocupacional'},
        {'codigo': 'FISIO', 'nombre': 'Fisioterapia'},
        {'codigo': 'PSICO', 'nombre': 'Psicoterapia'},
        {'codigo': 'DESEN', 'nombre': 'Terapia del Desarrollo'}
    ]
    
    for tipo in tipos:
        existe = db.query(TipoTerapia).filter(TipoTerapia.codigo == tipo['codigo']).first()
        if not existe:
            tt = TipoTerapia(codigo=tipo['codigo'], nombre=tipo['nombre'])
            db.add(tt)
    
    db.commit()
    print("✓ Tipos de terapia insertados")

def poblar_terapias():
    """Inserta las terapias"""
    terapias = [
        # Logopedia
        {
            'nombre': 'Logopedia General',
            'descripcion': 'Terapia del lenguaje y comunicación',
            'tipo_id': 1,
            'duracion_minutos': 60,
            'objetivo_general': 'Mejorar habilidades del lenguaje',
            'categoria': 'lenguaje',
            'tags': '["lenguaje","comunicación","dicción"]'
        },
        {
            'nombre': 'Dislexia - Lecto-escritura',
            'descripcion': 'Intervención en dificultades de lectura y escritura',
            'tipo_id': 1,
            'duracion_minutos': 60,
            'objetivo_general': 'Mejorar habilidades de lecto-escritura',
            'categoria': 'lenguaje',
            'tags': '["lectura","escritura","dislexia"]'
        },
        {
            'nombre': 'Dyspraxia Verbal',
            'descripcion': 'Terapia para apraxia del habla',
            'tipo_id': 1,
            'duracion_minutos': 45,
            'objetivo_general': 'Mejorar coordinación motora del habla',
            'categoria': 'lenguaje',
            'tags': '["habla","apraxia","motor"]'
        },
        # Terapia Ocupacional
        {
            'nombre': 'Terapia Ocupacional General',
            'descripcion': 'Desarrollo de habilidades motoras finas y gruesas',
            'tipo_id': 2,
            'duracion_minutos': 60,
            'objetivo_general': 'Desarrollar independencia en actividades cotidianas',
            'categoria': 'motricidad',
            'tags': '["motricidad","independencia","actividades"]'
        },
        {
            'nombre': 'Integración Sensorial',
            'descripcion': 'Procesamiento sensorial y coordinación',
            'tipo_id': 2,
            'duracion_minutos': 50,
            'objetivo_general': 'Mejorar respuesta sensorial',
            'categoria': 'sensorial',
            'tags': '["sensorial","coordinación","tactil"]'
        },
        {
            'nombre': 'Escritura y Motricidad Fina',
            'descripcion': 'Desarrollo de destreza escritora',
            'tipo_id': 2,
            'duracion_minutos': 45,
            'objetivo_general': 'Mejorar coordinación mano-ojo',
            'categoria': 'motricidad',
            'tags': '["escritura","motricidad","destreza"]'
        },
        # Fisioterapia
        {
            'nombre': 'Fisioterapia General',
            'descripcion': 'Rehabilitación y fortalecimiento motor',
            'tipo_id': 3,
            'duracion_minutos': 60,
            'objetivo_general': 'Mejorar movilidad y fuerza',
            'categoria': 'motor',
            'tags': '["movimiento","fortaleza","rehabilitación"]'
        },
        {
            'nombre': 'Marcha y Equilibrio',
            'descripcion': 'Terapia de marcha y equilibrio postural',
            'tipo_id': 3,
            'duracion_minutos': 50,
            'objetivo_general': 'Mejorar estabilidad y marcha',
            'categoria': 'motor',
            'tags': '["equilibrio","marcha","postura"]'
        },
        # Psicoterapia
        {
            'nombre': 'Psicoterapia Infantil',
            'descripcion': 'Abordaje psicoterapéutico de problemas emocionales',
            'tipo_id': 4,
            'duracion_minutos': 60,
            'objetivo_general': 'Mejorar bienestar emocional',
            'categoria': 'emocional',
            'tags': '["emoción","conducta","bienestar"]'
        },
        {
            'nombre': 'Terapia Cognitivo-Conductual',
            'descripcion': 'TCC aplicada a niños',
            'tipo_id': 4,
            'duracion_minutos': 60,
            'objetivo_general': 'Desarrollar estrategias de afrontamiento',
            'categoria': 'cognitivo',
            'tags': '["cognición","conducta","pensamiento"]'
        },
        # Desarrollo
        {
            'nombre': 'Atención Temprana',
            'descripcion': 'Intervención en primera infancia',
            'tipo_id': 5,
            'duracion_minutos': 45,
            'objetivo_general': 'Estimular desarrollo integral',
            'categoria': 'desarrollo',
            'tags': '["estimulación","infantil","integral"]'
        },
        {
            'nombre': 'Desarrollo Cognitivo',
            'descripcion': 'Estimulación cognitiva y aprendizaje',
            'tipo_id': 5,
            'duracion_minutos': 50,
            'objetivo_general': 'Estimular habilidades cognitivas',
            'categoria': 'cognitivo',
            'tags': '["cognitivo","aprendizaje","estimulación"]'
        }
    ]
    
    for terapia_data in terapias:
        existe = db.query(Terapia).filter(Terapia.nombre == terapia_data['nombre']).first()
        if not existe:
            t = Terapia(**terapia_data, activo=1)
            db.add(t)
    
    db.commit()
    print("✓ Terapias insertadas")

def poblar_terapeutas():
    """Inserta los terapeutas"""
    # Primero obtener el rol de terapeuta (id_rol = 3)
    rol_terapeuta = db.query(Rol).filter(Rol.id == 3).first()
    if not rol_terapeuta:
        print("⚠ Rol terapeuta no encontrado")
        return
    
    terapeutas = [
        {
            'nombres': 'María', 'apellido_paterno': 'González', 'apellido_materno': 'López',
            'rfc': 'MGO900815AAA', 'curp': 'MGOL900815HDFNNN01',
            'fecha_nacimiento': date(1990, 8, 15),
            'telefono_personal': '5551234001', 'correo_personal': 'maria.gonzalez@clinic.com',
            'especialidad_principal': 'Logopedia', 'especialidades': '["Logopedia","Dyspraxia","Dislexia"]',
            'grado_academico': 'Licenciado en Logopedia', 'cedula_profesional': 'LOG-2015-001',
            'fecha_ingreso': date(2018, 1, 15), 'rating': 5, 'total_pacientes': 12
        },
        {
            'nombres': 'Carlos', 'apellido_paterno': 'Rodríguez', 'apellido_materno': 'Martín',
            'rfc': 'CRM920510AAA', 'curp': 'CRMD920510HDFNRN02',
            'fecha_nacimiento': date(1992, 5, 10),
            'telefono_personal': '5551234002', 'correo_personal': 'carlos.rodriguez@clinic.com',
            'especialidad_principal': 'Logopedia', 'especialidades': '["Logopedia","Lecto-escritura"]',
            'grado_academico': 'Licenciado en Logopedia', 'cedula_profesional': 'LOG-2016-002',
            'fecha_ingreso': date(2018, 6, 1), 'rating': 4, 'total_pacientes': 10
        },
        {
            'nombres': 'Alejandra', 'apellido_paterno': 'Ramírez', 'apellido_materno': 'García',
            'rfc': 'ARA880320AAA', 'curp': 'RAGA880320HDFRMN03',
            'fecha_nacimiento': date(1988, 3, 20),
            'telefono_personal': '5551234003', 'correo_personal': 'alejandra.ramirez@clinic.com',
            'especialidad_principal': 'Terapia Ocupacional', 'especialidades': '["Terapia Ocupacional","Integración Sensorial","Motricidad Fina"]',
            'grado_academico': 'Licenciado en Terapia Ocupacional', 'cedula_profesional': 'OCP-2014-003',
            'fecha_ingreso': date(2017, 2, 15), 'rating': 5, 'total_pacientes': 15
        },
        {
            'nombres': 'Diego', 'apellido_paterno': 'Hernández', 'apellido_materno': 'Rojas',
            'rfc': 'DHR910705AAA', 'curp': 'HERD910705HDFRNR04',
            'fecha_nacimiento': date(1991, 7, 5),
            'telefono_personal': '5551234004', 'correo_personal': 'diego.hernandez@clinic.com',
            'especialidad_principal': 'Terapia Ocupacional', 'especialidades': '["Terapia Ocupacional","Escritura","Motricidad"]',
            'grado_academico': 'Licenciado en Terapia Ocupacional', 'cedula_profesional': 'OCP-2017-004',
            'fecha_ingreso': date(2019, 3, 1), 'rating': 4, 'total_pacientes': 8
        },
        {
            'nombres': 'Elena', 'apellido_paterno': 'Martínez', 'apellido_materno': 'Sánchez',
            'rfc': 'EMS850612AAA', 'curp': 'MASE850612HDFSZN05',
            'fecha_nacimiento': date(1985, 6, 12),
            'telefono_personal': '5551234005', 'correo_personal': 'elena.martinez@clinic.com',
            'especialidad_principal': 'Fisioterapia', 'especialidades': '["Fisioterapia","Marcha","Equilibrio"]',
            'grado_academico': 'Licenciado en Fisioterapia', 'cedula_profesional': 'FIS-2013-005',
            'fecha_ingreso': date(2016, 8, 15), 'rating': 5, 'total_pacientes': 18
        },
        {
            'nombres': 'Fernando', 'apellido_paterno': 'López', 'apellido_materno': 'Jiménez',
            'rfc': 'LJF930218AAA', 'curp': 'LOJF930218HDFNRN06',
            'fecha_nacimiento': date(1993, 2, 18),
            'telefono_personal': '5551234006', 'correo_personal': 'fernando.lopez@clinic.com',
            'especialidad_principal': 'Fisioterapia', 'especialidades': '["Fisioterapia","Rehabilitación","Fuerza"]',
            'grado_academico': 'Licenciado en Fisioterapia', 'cedula_profesional': 'FIS-2018-006',
            'fecha_ingreso': date(2020, 1, 15), 'rating': 4, 'total_pacientes': 6
        },
        {
            'nombres': 'Gabriela', 'apellido_paterno': 'Fernández', 'apellido_materno': 'Cruz',
            'rfc': 'FCG880930AAA', 'curp': 'FECG880930HDFNRR07',
            'fecha_nacimiento': date(1988, 9, 30),
            'telefono_personal': '5551234007', 'correo_personal': 'gabriela.fernandez@clinic.com',
            'especialidad_principal': 'Psicoterapia', 'especialidades': '["Psicoterapia","TCC","Emocional"]',
            'grado_academico': 'Licenciado en Psicología', 'cedula_profesional': 'PSI-2015-007',
            'fecha_ingreso': date(2018, 5, 1), 'rating': 5, 'total_pacientes': 14
        },
        {
            'nombres': 'Hugo', 'apellido_paterno': 'Torres', 'apellido_materno': 'Domínguez',
            'rfc': 'TDH870411AAA', 'curp': 'TODH870411HDFPRN08',
            'fecha_nacimiento': date(1987, 4, 11),
            'telefono_personal': '5551234008', 'correo_personal': 'hugo.torres@clinic.com',
            'especialidad_principal': 'Desarrollo Infantil', 'especialidades': '["Atención Temprana","Estimulación","Cognitivo"]',
            'grado_academico': 'Licenciado en Pedagogía Especial', 'cedula_profesional': 'PED-2014-008',
            'fecha_ingreso': date(2017, 9, 15), 'rating': 5, 'total_pacientes': 11
        }
    ]
    
    for terapeuta_data in terapeutas:
        existe = db.query(Personal).filter(Personal.rfc == terapeuta_data['rfc']).first()
        if not existe:
            p = Personal(**terapeuta_data, id_rol=3, estado_laboral='ACTIVO')
            db.add(p)
    
    db.commit()
    print("✓ Terapeutas insertados")

def poblar_ninos():
    """Inserta los niños"""
    ninos = [
        {
            'nombre': 'Juan', 'apellido_paterno': 'Pérez', 'apellido_materno': 'García',
            'fecha_nacimiento': date(2019, 9, 15), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'PEGJ190915HDFNRN01'
        },
        {
            'nombre': 'Lucía', 'apellido_paterno': 'Martínez', 'apellido_materno': 'López',
            'fecha_nacimiento': date(2018, 10, 22), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'MAML181022HDFNRR02'
        },
        {
            'nombre': 'Manuel', 'apellido_paterno': 'González', 'apellido_materno': 'Ruiz',
            'fecha_nacimiento': date(2020, 11, 8), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'GORM201108HDFNZN03'
        },
        {
            'nombre': 'Sofía', 'apellido_paterno': 'Rodríguez', 'apellido_materno': 'Fernández',
            'fecha_nacimiento': date(2019, 12, 3), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'ROFS191203HDFNRR04'
        },
        {
            'nombre': 'Pablo', 'apellido_paterno': 'García', 'apellido_materno': 'Moreno',
            'fecha_nacimiento': date(2018, 8, 14), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'GAMP180814HDFNRR05'
        },
        {
            'nombre': 'María', 'apellido_paterno': 'López', 'apellido_materno': 'Hernández',
            'fecha_nacimiento': date(2017, 7, 20), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'LOHM170720HDFNRR06'
        },
        {
            'nombre': 'David', 'apellido_paterno': 'Jiménez', 'apellido_materno': 'Castro',
            'fecha_nacimiento': date(2020, 5, 17), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'JICD200517HDFNSS07'
        },
        {
            'nombre': 'Martina', 'apellido_paterno': 'Sánchez', 'apellido_materno': 'Gómez',
            'fecha_nacimiento': date(2019, 6, 28), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'SAGM190628HDFNMR08'
        },
        {
            'nombre': 'Alejandro', 'apellido_paterno': 'Díaz', 'apellido_materno': 'Vega',
            'fecha_nacimiento': date(2018, 3, 9), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'DIVA180309HDFNGN09'
        },
        {
            'nombre': 'Natalia', 'apellido_paterno': 'Ramírez', 'apellido_materno': 'Romero',
            'fecha_nacimiento': date(2019, 4, 12), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'RARN190412HDFNMR10'
        },
        {
            'nombre': 'Jorge', 'apellido_paterno': 'Vargas', 'apellido_materno': 'Núñez',
            'fecha_nacimiento': date(2020, 2, 25), 'sexo': 'M',
            'estado': 'ACTIVO', 'curp': 'VARN200225HDFNLL11'
        },
        {
            'nombre': 'Cecilia', 'apellido_paterno': 'Flores', 'apellido_materno': 'Delgado',
            'fecha_nacimiento': date(2018, 11, 18), 'sexo': 'F',
            'estado': 'ACTIVO', 'curp': 'FODC181118HDFNLL12'
        }
    ]
    
    for nino_data in ninos:
        existe = db.query(Nino).filter(
            Nino.nombre == nino_data['nombre'],
            Nino.apellido_paterno == nino_data['apellido_paterno']
        ).first()
        if not existe:
            n = Nino(**nino_data)
            db.add(n)
    
    db.commit()
    print("✓ Niños insertados")

def poblar_asignaciones():
    """Asigna terapias a terapeutas y niños"""
    # Asignaciones terapeutas - terapias
    asignaciones_tp = [
        (1, 1, 1), (1, 2, 1), (1, 3, 1),  # María
        (2, 1, 1), (2, 2, 1),              # Carlos
        (3, 4, 1), (3, 5, 1), (3, 6, 1),  # Alejandra
        (4, 4, 1), (4, 6, 1),              # Diego
        (5, 7, 1), (5, 8, 1),              # Elena
        (6, 7, 1), (6, 8, 1),              # Fernando
        (7, 9, 1), (7, 10, 1),             # Gabriela
        (8, 11, 1), (8, 12, 1)             # Hugo
    ]
    
    for terapeuta_id, terapia_id, activo in asignaciones_tp:
        existe = db.query(TerapiaPersonal).filter(
            TerapiaPersonal.terapia_id == terapia_id,
            TerapiaPersonal.personal_id == terapeuta_id
        ).first()
        if not existe:
            tp = TerapiaPersonal(terapia_id=terapia_id, personal_id=terapeuta_id, activo=activo)
            db.add(tp)
    
    # Asignaciones niños - terapias - terapeutas
    asignaciones_tn = [
        (1, 1, 1, 1, 2),      # Juan - Logopedia General con María
        (2, 2, 1, 2, 2),      # Lucía - Dislexia con María
        (3, 1, 2, 2, 1),      # Manuel - Logopedia General con Carlos
        (4, 4, 3, 1, 2),      # Sofía - T.O. General con Alejandra
        (4, 5, 3, 1, 1),      # Sofía - Integración Sensorial con Alejandra
        (5, 4, 3, 1, 2),      # Pablo - T.O. General con Alejandra
        (5, 7, 5, 1, 2),      # Pablo - Fisioterapia General con Elena
        (6, 6, 4, 2, 1),      # María L - Escritura con Diego
        (7, 7, 5, 1, 2),      # David - Fisioterapia General con Elena
        (7, 8, 5, 1, 1),      # David - Marcha con Elena
        (8, 8, 6, 2, 2),      # Martina - Marcha con Fernando
        (9, 9, 7, 2, 1),      # Alejandro - Psicoterapia con Gabriela
        (10, 10, 7, 2, 2),    # Natalia - TCC con Gabriela
        (11, 11, 8, 1, 2),    # Jorge - Atención Temprana con Hugo
        (11, 1, 1, 1, 1),     # Jorge - Logopedia General con María
        (12, 11, 8, 1, 2),    # Cecilia - Atención Temprana con Hugo
        (12, 12, 8, 1, 1)     # Cecilia - Desarrollo Cognitivo con Hugo
    ]
    
    for nino_id, terapia_id, terapeuta_id, prioridad_id, frecuencia in asignaciones_tn:
        existe = db.query(TerapiaNino).filter(
            TerapiaNino.nino_id == nino_id,
            TerapiaNino.terapia_id == terapia_id
        ).first()
        if not existe:
            tn = TerapiaNino(
                nino_id=nino_id,
                terapia_id=terapia_id,
                terapeuta_id=terapeuta_id,
                prioridad_id=prioridad_id,
                frecuencia_semana=frecuencia,
                fecha_asignacion=datetime.now().strftime("%Y-%m-%d"),
                activo=1
            )
            db.add(tn)
    
    db.commit()
    print("✓ Asignaciones realizadas")

def main():
    try:
        print("🔧 Poblando base de datos...")
        poblar_tipos_terapia()
        poblar_terapias()
        poblar_terapeutas()
        poblar_ninos()
        poblar_asignaciones()
        print("\n✓ Base de datos poblada exitosamente")
        print("  - 12 Niños con diagnósticos variados")
        print("  - 8 Terapeutas especializados")
        print("  - 12 Tipos de terapias coherentes")
        print("  - Asignaciones lógicas por especialidad")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()

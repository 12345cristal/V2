# backend/scripts/agregar_terapeutas_ejemplo.py
"""
Script para agregar 10 terapeutas adicionales con datos variados
para mejorar la evaluación TOPSIS
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.personal import Personal, EstadoLaboral
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random


def crear_terapeutas_ejemplo():
    """Crea 10 terapeutas adicionales con datos variados"""
    
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("🏥 AGREGANDO TERAPEUTAS ADICIONALES PARA TOPSIS")
        print("="*60 + "\n")
        
        # Verificar que existe el rol de terapeuta
        rol_terapeuta = db.query(Rol).filter(Rol.id == 3).first()
        if not rol_terapeuta:
            print("❌ ERROR: No existe el rol de terapeuta (ID=3)")
            return
        
        # Datos de terapeutas variados
        terapeutas_data = [
            {
                "nombres": "Roberto",
                "apellido_paterno": "Hernández",
                "apellido_materno": "Silva",
                "especialidad_principal": "Terapia Ocupacional",
                "especialidades": "Terapia Ocupacional, Integración Sensorial",
                "experiencia": "8 años",
                "grado_academico": "Licenciatura",
                "rating": 4.8,
                "total_pacientes": 35
            },
            {
                "nombres": "Laura",
                "apellido_paterno": "Mendoza",
                "apellido_materno": "Reyes",
                "especialidad_principal": "Psicología Infantil",
                "especialidades": "Psicología Infantil, Terapia Cognitivo-Conductual",
                "experiencia": "6 años",
                "grado_academico": "Maestría",
                "rating": 4.7,
                "total_pacientes": 28
            },
            {
                "nombres": "Fernando",
                "apellido_paterno": "Castro",
                "apellido_materno": "López",
                "especialidad_principal": "Lenguaje y Comunicación",
                "especialidades": "Lenguaje y Comunicación, Articulación",
                "experiencia": "12 años",
                "grado_academico": "Maestría",
                "rating": 4.9,
                "total_pacientes": 42
            },
            {
                "nombres": "Gabriela",
                "apellido_paterno": "Morales",
                "apellido_materno": "Díaz",
                "especialidad_principal": "Terapia Conductual ABA",
                "especialidades": "Terapia Conductual ABA, Análisis Funcional",
                "experiencia": "5 años",
                "grado_academico": "Licenciatura",
                "rating": 4.5,
                "total_pacientes": 22
            },
            {
                "nombres": "Diego",
                "apellido_paterno": "Ruiz",
                "apellido_materno": "Sánchez",
                "especialidad_principal": "Musicoterapia",
                "especialidades": "Musicoterapia, Expresión Artística",
                "experiencia": "4 años",
                "grado_academico": "Licenciatura",
                "rating": 4.4,
                "total_pacientes": 18
            },
            {
                "nombres": "Patricia",
                "apellido_paterno": "Guzmán",
                "apellido_materno": "Torres",
                "especialidad_principal": "Terapia Física",
                "especialidades": "Terapia Física, Desarrollo Motor",
                "experiencia": "10 años",
                "grado_academico": "Licenciatura",
                "rating": 4.8,
                "total_pacientes": 38
            },
            {
                "nombres": "Miguel",
                "apellido_paterno": "Ortiz",
                "apellido_materno": "Ramírez",
                "especialidad_principal": "Integración Sensorial",
                "especialidades": "Integración Sensorial, Terapia Ocupacional",
                "experiencia": "7 años",
                "grado_academico": "Maestría",
                "rating": 4.6,
                "total_pacientes": 30
            },
            {
                "nombres": "Sofía",
                "apellido_paterno": "Vargas",
                "apellido_materno": "Medina",
                "especialidad_principal": "Lenguaje y Comunicación",
                "especialidades": "Lenguaje y Comunicación, Comunicación Aumentativa",
                "experiencia": "9 años",
                "grado_academico": "Maestría",
                "rating": 4.9,
                "total_pacientes": 36
            },
            {
                "nombres": "Alberto",
                "apellido_paterno": "Flores",
                "apellido_materno": "Guerrero",
                "especialidad_principal": "Terapia Conductual ABA",
                "especialidades": "Terapia Conductual ABA, TEACCH",
                "experiencia": "11 años",
                "grado_academico": "Doctorado",
                "rating": 5.0,
                "total_pacientes": 45
            },
            {
                "nombres": "Valeria",
                "apellido_paterno": "Romero",
                "apellido_materno": "Jiménez",
                "especialidad_principal": "Psicopedagogía",
                "especialidades": "Psicopedagogía, Educación Especial",
                "experiencia": "3 años",
                "grado_academico": "Licenciatura",
                "rating": 4.3,
                "total_pacientes": 15
            }
        ]
        
        terapeutas_creados = 0
        
        for idx, data in enumerate(terapeutas_data, start=1):
            try:
                # Crear usuario
                email = f"{data['nombres'].lower()}.{data['apellido_paterno'].lower()}@autismo.com"
                
                # Verificar si ya existe
                existe = db.query(Usuario).filter(Usuario.email == email).first()
                if existe:
                    print(f"⚠️  Terapeuta {idx}: {data['nombres']} {data['apellido_paterno']} ya existe")
                    continue
                
                usuario = Usuario(
                    nombres=data['nombres'],
                    apellido_paterno=data['apellido_paterno'],
                    apellido_materno=data['apellido_materno'],
                    email=email,
                    hashed_password=get_password_hash("terapeuta123"),
                    rol_id=3,  # Terapeuta
                    activo=True
                )
                db.add(usuario)
                db.flush()
                
                # Crear personal/terapeuta
                fecha_ingreso = datetime.now() - timedelta(days=random.randint(365, 3650))
                
                terapeuta = Personal(
                    nombres=data['nombres'],
                    apellido_paterno=data['apellido_paterno'],
                    apellido_materno=data['apellido_materno'],
                    id_usuario=usuario.id,
                    id_rol=3,
                    rfc=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=13))}",
                    curp=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=18))}",
                    fecha_nacimiento=datetime.now() - timedelta(days=random.randint(9125, 14600)),  # 25-40 años
                    telefono_personal=f"668{''.join(random.choices('0123456789', k=7))}",
                    correo_personal=email,
                    calle=f"Calle {random.choice(['Juárez', 'Hidalgo', 'Morelos', 'Reforma'])}",
                    numero_exterior=str(random.randint(100, 999)),
                    colonia=f"Colonia {random.choice(['Centro', 'Norte', 'Sur', 'Este'])}",
                    ciudad="Los Mochis",
                    estado="Sinaloa",
                    codigo_postal=f"8180{random.randint(0, 9)}",
                    especialidad_principal=data['especialidad_principal'],
                    especialidades=data['especialidades'],
                    grado_academico=data['grado_academico'],
                    cedula_profesional=f"{''.join(random.choices('0123456789', k=8))}",
                    fecha_ingreso=fecha_ingreso,
                    estado_laboral=EstadoLaboral.ACTIVO,
                    experiencia=data['experiencia'],
                    total_pacientes=data['total_pacientes'],
                    sesiones_semana=random.randint(15, 35),
                    rating=data['rating']
                )
                db.add(terapeuta)
                
                terapeutas_creados += 1
                print(f"✅ Terapeuta {idx}: {data['nombres']} {data['apellido_paterno']} - {data['especialidad_principal']}")
                
            except Exception as e:
                print(f"❌ Error al crear terapeuta {idx}: {str(e)}")
                db.rollback()
                continue
        
        # Guardar cambios
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ COMPLETADO: {terapeutas_creados} terapeutas agregados exitosamente")
        print(f"{'='*60}\n")
        
        # Resumen
        total_terapeutas = db.query(Personal).filter(Personal.id_rol == 3).count()
        print(f"📊 Total de terapeutas en el sistema: {total_terapeutas}")
        print(f"📊 Terapeutas activos: {db.query(Personal).filter(Personal.id_rol == 3, Personal.estado_laboral == EstadoLaboral.ACTIVO).count()}")
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("\n🚀 Iniciando script de creación de terapeutas...\n")
    crear_terapeutas_ejemplo()
    print("\n✅ Script finalizado\n")

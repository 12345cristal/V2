"""
Script para poblar completamente el sistema de recomendaciones
Genera perfiles vectorizados para todos los niños y crea actividades variadas
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.nino import Nino
from sqlalchemy import text
import numpy as np
import json
from datetime import datetime, date

def calcular_edad(fecha_nacimiento):
    """Calcula la edad a partir de la fecha de nacimiento"""
    if not fecha_nacimiento:
        return 5  # Edad por defecto
    
    if isinstance(fecha_nacimiento, str):
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
    
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year
    if hoy.month < fecha_nacimiento.month or (hoy.month == fecha_nacimiento.month and hoy.day < fecha_nacimiento.day):
        edad -= 1
    return edad

# Datos para generar perfiles variados de niños
DIAGNOSTICOS_VARIADOS = [
    ["TEA Nivel 1", "Hiperlexia"],
    ["TEA Nivel 2", "Dificultad en comunicación social"],
    ["TEA Nivel 3", "Comportamientos repetitivos severos"],
    ["Asperger", "Alta funcionalidad"],
    ["TEA con hipersensibilidad sensorial"],
    ["TEA con hiposensibilidad sensorial"],
    ["TEA con trastorno de ansiedad"],
    ["TEA con TDAH"],
    ["TEA no verbal"],
    ["TEA verbal con ecolalia"],
]

DIFICULTADES_VARIADAS = [
    ["Contacto visual limitado", "Dificultad en turnos conversacionales"],
    ["Rigidez en rutinas", "Malestar ante cambios"],
    ["Procesamiento sensorial auditivo", "Hipersensibilidad a sonidos"],
    ["Coordinación motora fina", "Dificultad en escritura"],
    ["Regulación emocional", "Berrinches frecuentes"],
    ["Comunicación no verbal", "Dificultad para señalar"],
    ["Interacción con pares", "Juego solitario preferido"],
    ["Atención sostenida", "Distracción frecuente"],
    ["Comprensión de instrucciones complejas"],
    ["Expresión de necesidades básicas"],
]

FORTALEZAS_VARIADAS = [
    ["Excelente memoria visual", "Reconocimiento de patrones"],
    ["Interés intenso en números", "Habilidad matemática"],
    ["Vocabulario avanzado", "Lectura fluida"],
    ["Creatividad artística", "Atención al detalle"],
    ["Honestidad", "Pensamiento lógico"],
    ["Memoria auditiva excepcional", "Aprendizaje por repetición"],
    ["Habilidad musical", "Reconocimiento de melodías"],
    ["Conocimiento enciclopédico en temas específicos"],
    ["Persistencia en tareas de interés", "Dedicación"],
    ["Capacidad de concentración en actividades preferidas"],
]

# Actividades variadas por áreas de desarrollo
ACTIVIDADES_MOTOR = [
    {
        "nombre": "Circuito de Obstáculos Sensorial",
        "descripcion": "Recorrido con diferentes texturas y niveles para estimular coordinación y procesamiento sensorial",
        "objetivo": "Desarrollar coordinación motora gruesa y adaptación sensorial",
        "materiales": "Colchonetas, túnel de tela, cojines, cuerdas, conos",
        "duracion_minutos": 30,
        "tags": ["motricidad gruesa", "sensorial", "coordinación", "equilibrio"],
        "dificultad": 2
    },
    {
        "nombre": "Yoga para Niños Adaptado",
        "descripcion": "Posturas de yoga simples con apoyo visual y narrativa",
        "objetivo": "Mejorar flexibilidad, equilibrio y autorregulación",
        "materiales": "Tapete de yoga, tarjetas visuales de posturas, música relajante",
        "duracion_minutos": 25,
        "tags": ["yoga", "relajación", "equilibrio", "autorregulación"],
        "dificultad": 1
    },
    {
        "nombre": "Juego de Lanzamiento con Objetivos",
        "descripcion": "Lanzar pelotas de diferentes tamaños a objetivos marcados",
        "objetivo": "Desarrollar coordinación ojo-mano y control motor",
        "materiales": "Pelotas variadas, cestas, objetivos visuales",
        "duracion_minutos": 20,
        "tags": ["lanzamiento", "coordinación", "puntería"],
        "dificultad": 1
    },
    {
        "nombre": "Ensartado de Cuentas Grandes",
        "descripcion": "Enhebrar cuentas grandes en cordón siguiendo patrones",
        "objetivo": "Desarrollar motricidad fina y seguimiento de secuencias",
        "materiales": "Cuentas grandes de colores, cordones gruesos, tarjetas de patrones",
        "duracion_minutos": 15,
        "tags": ["motricidad fina", "patrones", "coordinación"],
        "dificultad": 1
    },
    {
        "nombre": "Recortar con Tijeras Adaptadas",
        "descripcion": "Práctica de corte con tijeras especiales siguiendo líneas",
        "objetivo": "Fortalecer músculos de la mano y coordinación para escritura",
        "materiales": "Tijeras adaptadas, papel con líneas guía, diferentes texturas",
        "duracion_minutos": 20,
        "tags": ["motricidad fina", "tijeras", "preescritura"],
        "dificultad": 2
    },
    {
        "nombre": "Pintura con Diferentes Herramientas",
        "descripcion": "Explorar pintura con pinceles, esponjas, rodillos y dedos",
        "objetivo": "Estimular creatividad y exploración sensorial táctil",
        "materiales": "Pinturas lavables, papel grande, herramientas variadas",
        "duracion_minutos": 30,
        "tags": ["arte", "sensorial", "creatividad", "motricidad fina"],
        "dificultad": 1
    },
]

ACTIVIDADES_COGNITIVO = [
    {
        "nombre": "Clasificación por Categorías",
        "descripcion": "Agrupar objetos por color, forma, tamaño o función",
        "objetivo": "Desarrollar pensamiento categorial y habilidades de clasificación",
        "materiales": "Objetos variados, cajas de clasificación, tarjetas de categorías",
        "duracion_minutos": 20,
        "tags": ["clasificación", "categorías", "pensamiento lógico"],
        "dificultad": 1
    },
    {
        "nombre": "Rompecabezas Progresivos",
        "descripcion": "Completar rompecabezas de 4 a 24 piezas con aumento gradual",
        "objetivo": "Desarrollar resolución de problemas y percepción espacial",
        "materiales": "Rompecabezas de diferentes niveles, soporte visual",
        "duracion_minutos": 25,
        "tags": ["rompecabezas", "espacial", "resolución problemas"],
        "dificultad": 2
    },
    {
        "nombre": "Juego de Memoria Visual",
        "descripcion": "Encontrar parejas de tarjetas con imágenes",
        "objetivo": "Fortalecer memoria de trabajo y atención",
        "materiales": "Tarjetas de memoria con imágenes atractivas",
        "duracion_minutos": 15,
        "tags": ["memoria", "atención", "concentración"],
        "dificultad": 1
    },
    {
        "nombre": "Secuencias Temporales",
        "descripcion": "Ordenar tarjetas de una historia en secuencia lógica",
        "objetivo": "Desarrollar comprensión de causa-efecto y secuenciación",
        "materiales": "Tarjetas de secuencias de 3-6 pasos",
        "duracion_minutos": 20,
        "tags": ["secuencias", "lógica", "comprensión"],
        "dificultad": 2
    },
    {
        "nombre": "Construcción con Bloques Siguiendo Modelo",
        "descripcion": "Reproducir construcciones mostradas en tarjetas",
        "objetivo": "Desarrollar habilidades visuoespaciales y planificación",
        "materiales": "Bloques de construcción, tarjetas modelo",
        "duracion_minutos": 25,
        "tags": ["construcción", "espacial", "imitación"],
        "dificultad": 2
    },
    {
        "nombre": "Emparejamiento de Sonidos con Imágenes",
        "descripcion": "Asociar sonidos grabados con tarjetas de imágenes correspondientes",
        "objetivo": "Desarrollar discriminación auditiva y asociación",
        "materiales": "Grabadora de sonidos, tarjetas visuales",
        "duracion_minutos": 20,
        "tags": ["auditivo", "asociación", "discriminación"],
        "dificultad": 1
    },
]

ACTIVIDADES_SOCIAL = [
    {
        "nombre": "Juego de Turnos con Dado Gigante",
        "descripcion": "Juego de mesa simple donde cada niño espera su turno",
        "objetivo": "Practicar espera de turnos y seguimiento de reglas",
        "materiales": "Dado grande, fichas de colores, tablero simple",
        "duracion_minutos": 20,
        "tags": ["turnos", "reglas", "interacción"],
        "dificultad": 1
    },
    {
        "nombre": "Reconocimiento de Emociones con Espejo",
        "descripcion": "Imitar y nombrar emociones frente al espejo",
        "objetivo": "Identificar y expresar emociones básicas",
        "materiales": "Espejo grande, tarjetas de emociones, apoyo visual",
        "duracion_minutos": 15,
        "tags": ["emociones", "expresión", "reconocimiento"],
        "dificultad": 1
    },
    {
        "nombre": "Teatro de Títeres Social",
        "descripcion": "Representar situaciones sociales con títeres",
        "objetivo": "Practicar habilidades sociales en contexto lúdico",
        "materiales": "Títeres variados, escenario pequeño, guiones visuales",
        "duracion_minutos": 25,
        "tags": ["social", "rol", "comunicación", "juego simbólico"],
        "dificultad": 2
    },
    {
        "nombre": "Juego Cooperativo de Construcción",
        "descripcion": "Construir algo en conjunto con otro niño o adulto",
        "objetivo": "Fomentar colaboración y comunicación",
        "materiales": "Bloques grandes, plan visual compartido",
        "duracion_minutos": 20,
        "tags": ["cooperación", "trabajo equipo", "comunicación"],
        "dificultad": 2
    },
    {
        "nombre": "Historias Sociales Personalizadas",
        "descripcion": "Leer y discutir historias sobre situaciones sociales",
        "objetivo": "Comprender expectativas y comportamientos sociales",
        "materiales": "Libros de historias sociales, imágenes del niño en situaciones",
        "duracion_minutos": 15,
        "tags": ["historias sociales", "comprensión", "comportamiento"],
        "dificultad": 1
    },
    {
        "nombre": "Juego de Imitación de Acciones",
        "descripcion": "Seguir al líder imitando acciones motoras y gestos",
        "objetivo": "Desarrollar imitación y atención compartida",
        "materiales": "Música, tarjetas de acciones opcionales",
        "duracion_minutos": 15,
        "tags": ["imitación", "atención", "motricidad"],
        "dificultad": 1
    },
]

ACTIVIDADES_COMUNICACION = [
    {
        "nombre": "Tablero de Comunicación PECS Básico",
        "descripcion": "Usar sistema de intercambio de imágenes para comunicar deseos",
        "objetivo": "Desarrollar comunicación funcional mediante imágenes",
        "materiales": "Tablero PECS, tarjetas laminadas, velcro",
        "duracion_minutos": 20,
        "tags": ["PECS", "comunicación aumentativa", "peticiones"],
        "dificultad": 1
    },
    {
        "nombre": "Caja de Sorpresas Comunicativa",
        "descripcion": "Pedir ayuda para abrir caja con objeto deseado dentro",
        "objetivo": "Fomentar iniciación comunicativa y peticiones",
        "materiales": "Cajas con cierres variados, objetos motivadores",
        "duracion_minutos": 15,
        "tags": ["iniciativa", "petición", "comunicación"],
        "dificultad": 1
    },
    {
        "nombre": "Canciones con Gestos",
        "descripcion": "Aprender canciones simples con gestos asociados",
        "objetivo": "Combinar lenguaje verbal con gestos comunicativos",
        "materiales": "Reproductor de música, tarjetas de gestos",
        "duracion_minutos": 20,
        "tags": ["canciones", "gestos", "lenguaje"],
        "dificultad": 1
    },
    {
        "nombre": "Libro de Comunicación Personalizado",
        "descripcion": "Usar libro con fotos del niño y su entorno para comunicar",
        "objetivo": "Expandir vocabulario funcional personalizado",
        "materiales": "Álbum con fotos familiares, objetos, lugares conocidos",
        "duracion_minutos": 20,
        "tags": ["vocabulario", "personalizado", "comunicación"],
        "dificultad": 1
    },
    {
        "nombre": "Juego de Preguntas con Apoyo Visual",
        "descripcion": "Responder preguntas simples con ayuda de imágenes",
        "objetivo": "Desarrollar comprensión y respuesta a preguntas",
        "materiales": "Tarjetas de preguntas visuales, opciones de respuesta",
        "duracion_minutos": 15,
        "tags": ["preguntas", "comprensión", "respuestas"],
        "dificultad": 2
    },
    {
        "nombre": "Descripción de Objetos con Pistas",
        "descripcion": "Adivinar objeto mediante descripción de características",
        "objetivo": "Desarrollar vocabulario descriptivo y comprensión",
        "materiales": "Objetos variados, tarjetas de características",
        "duracion_minutos": 20,
        "tags": ["vocabulario", "descripción", "adivinanzas"],
        "dificultad": 2
    },
]

ACTIVIDADES_SENSORIAL = [
    {
        "nombre": "Mesa de Luz con Materiales Translúcidos",
        "descripcion": "Explorar objetos de colores sobre mesa de luz",
        "objetivo": "Estimular percepción visual y exploración táctil",
        "materiales": "Mesa de luz, objetos translúcidos, figuras de colores",
        "duracion_minutos": 20,
        "tags": ["visual", "sensorial", "exploración"],
        "dificultad": 1
    },
    {
        "nombre": "Caja Sensorial de Texturas",
        "descripcion": "Buscar objetos escondidos en materiales de diferentes texturas",
        "objetivo": "Desensibilización táctil y exploración sensorial",
        "materiales": "Cajas con arroz, frijoles, arena, objetos escondidos",
        "duracion_minutos": 15,
        "tags": ["táctil", "texturas", "exploración"],
        "dificultad": 1
    },
    {
        "nombre": "Botella de Calma Sensorial",
        "descripcion": "Observar botella con purpurina y líquido para autorregulación",
        "objetivo": "Proveer herramienta de calma y enfoque visual",
        "materiales": "Botella sensorial, silla cómoda, espacio tranquilo",
        "duracion_minutos": 10,
        "tags": ["calma", "autorregulación", "visual"],
        "dificultad": 1
    },
    {
        "nombre": "Masaje con Pelotas Texturizadas",
        "descripcion": "Rodar pelotas de diferentes texturas sobre cuerpo",
        "objetivo": "Proveer input propioceptivo calmante",
        "materiales": "Pelotas texturizadas de varios tamaños",
        "duracion_minutos": 15,
        "tags": ["propioceptivo", "masaje", "calma"],
        "dificultad": 1
    },
    {
        "nombre": "Columpio y Movimiento Vestibular",
        "descripcion": "Uso controlado de columpio para estimulación vestibular",
        "objetivo": "Regular sistema vestibular y proveer input sensorial",
        "materiales": "Columpio terapéutico, espacio seguro",
        "duracion_minutos": 20,
        "tags": ["vestibular", "movimiento", "regulación"],
        "dificultad": 2
    },
    {
        "nombre": "Plastilina y Masas Sensoriales",
        "descripcion": "Manipular plastilina, slime y otras masas",
        "objetivo": "Fortalecer manos y proveer input táctil",
        "materiales": "Plastilina de diferentes resistencias, moldes, herramientas",
        "duracion_minutos": 25,
        "tags": ["táctil", "motricidad fina", "manipulación"],
        "dificultad": 1
    },
]

def generar_embedding_aleatorio():
    """Genera un vector de 768 dimensiones aleatorio normalizado"""
    embedding = np.random.randn(768)
    embedding = embedding / np.linalg.norm(embedding)
    return embedding.tolist()

def crear_perfil_nino(nino_id: int, nino_data: dict, db: SessionLocal):
    """Crea perfil vectorizado para un niño"""
    
    # Usar datos variados según el ID del niño
    idx = nino_id % len(DIAGNOSTICOS_VARIADOS)
    
    diagnosticos = DIAGNOSTICOS_VARIADOS[idx]
    dificultades = DIFICULTADES_VARIADAS[idx]
    fortalezas = FORTALEZAS_VARIADAS[idx]
    
    # Calcular edad
    edad = calcular_edad(nino_data.get('fecha_nacimiento'))
    
    # Generar texto del perfil
    texto_perfil = f"""
    Niño: {nino_data.get('nombre', '')} {nino_data.get('apellido_paterno', '')}
    Edad: {edad} años
    Diagnósticos: {', '.join(diagnosticos)}
    Dificultades principales: {', '.join(dificultades)}
    Fortalezas: {', '.join(fortalezas)}
    """
    
    # Generar embedding
    embedding = generar_embedding_aleatorio()
    
    # Insertar perfil
    query = text("""
        INSERT INTO perfil_nino_vectorizado 
        (nino_id, embedding, edad, diagnosticos, dificultades, fortalezas, texto_perfil, fecha_generacion, fecha_actualizacion)
        VALUES 
        (:nino_id, :embedding, :edad, :diagnosticos, :dificultades, :fortalezas, :texto_perfil, NOW(), NOW())
        ON DUPLICATE KEY UPDATE
        embedding = :embedding,
        edad = :edad,
        diagnosticos = :diagnosticos,
        dificultades = :dificultades,
        fortalezas = :fortalezas,
        texto_perfil = :texto_perfil,
        fecha_actualizacion = NOW()
    """)
    
    db.execute(query, {
        'nino_id': nino_id,
        'embedding': json.dumps(embedding),
        'edad': edad,
        'diagnosticos': json.dumps(diagnosticos),
        'dificultades': json.dumps(dificultades),
        'fortalezas': json.dumps(fortalezas),
        'texto_perfil': texto_perfil.strip()
    })
    
    return True

def crear_actividad(actividad_data: dict, area: str, db: SessionLocal):
    """Crea una actividad y su perfil vectorizado"""
    
    # Insertar actividad
    query_actividad = text("""
        INSERT INTO actividades 
        (nombre, descripcion, objetivo, materiales, duracion_minutos, tags, dificultad, area_desarrollo, activo)
        VALUES 
        (:nombre, :descripcion, :objetivo, :materiales, :duracion_minutos, :tags, :dificultad, :area_desarrollo, 1)
    """)
    
    result = db.execute(query_actividad, {
        'nombre': actividad_data['nombre'],
        'descripcion': actividad_data['descripcion'],
        'objetivo': actividad_data['objetivo'],
        'materiales': actividad_data['materiales'],
        'duracion_minutos': actividad_data['duracion_minutos'],
        'tags': json.dumps(actividad_data['tags']),
        'dificultad': actividad_data['dificultad'],
        'area_desarrollo': area
    })
    
    actividad_id = result.lastrowid
    
    # Crear perfil vectorizado de la actividad
    embedding = generar_embedding_aleatorio()
    
    texto_descripcion = f"""
    Actividad: {actividad_data['nombre']}
    Área: {area}
    Descripción: {actividad_data['descripcion']}
    Objetivo: {actividad_data['objetivo']}
    Dificultad: {actividad_data['dificultad']}
    Tags: {', '.join(actividad_data['tags'])}
    """
    
    query_perfil = text("""
        INSERT INTO perfil_actividad_vectorizada
        (actividad_id, embedding, areas_desarrollo, tags, nivel_dificultad, texto_descripcion, fecha_generacion, fecha_actualizacion)
        VALUES
        (:actividad_id, :embedding, :areas_desarrollo, :tags, :nivel_dificultad, :texto_descripcion, NOW(), NOW())
    """)
    
    db.execute(query_perfil, {
        'actividad_id': actividad_id,
        'embedding': json.dumps(embedding),
        'areas_desarrollo': json.dumps([area]),
        'tags': json.dumps(actividad_data['tags']),
        'nivel_dificultad': actividad_data['dificultad'],
        'texto_descripcion': texto_descripcion.strip()
    })
    
    return actividad_id

def main():
    print("=" * 80)
    print("POBLANDO SISTEMA COMPLETO DE RECOMENDACIONES")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 1. Obtener todos los niños
        print("\n[1/3] Obteniendo todos los niños...")
        ninos = db.query(Nino).all()
        print(f"   ✓ Encontrados {len(ninos)} niños")
        
        # 2. Crear perfiles para todos los niños
        print("\n[2/3] Generando perfiles vectorizados para niños...")
        perfiles_creados = 0
        for nino in ninos:
            try:
                nino_data = {
                    'nombre': nino.nombre,
                    'apellido_paterno': nino.apellido_paterno,
                    'fecha_nacimiento': nino.fecha_nacimiento
                }
                crear_perfil_nino(nino.id, nino_data, db)
                perfiles_creados += 1
                
                if perfiles_creados % 10 == 0:
                    print(f"   ✓ Perfiles creados: {perfiles_creados}/{len(ninos)}")
                    db.commit()
            except Exception as e:
                print(f"   ✗ Error con niño {nino.id}: {str(e)}")
                continue
        
        db.commit()
        print(f"   ✓ Total perfiles de niños: {perfiles_creados}")
        
        # 3. Crear actividades variadas
        print("\n[3/3] Creando actividades variadas...")
        
        actividades_creadas = 0
        
        # Motor
        print("   → Creando actividades MOTOR...")
        for act in ACTIVIDADES_MOTOR:
            try:
                crear_actividad(act, 'motor', db)
                actividades_creadas += 1
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        # Cognitivo
        print("   → Creando actividades COGNITIVO...")
        for act in ACTIVIDADES_COGNITIVO:
            try:
                crear_actividad(act, 'cognitivo', db)
                actividades_creadas += 1
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        # Social
        print("   → Creando actividades SOCIAL...")
        for act in ACTIVIDADES_SOCIAL:
            try:
                crear_actividad(act, 'social', db)
                actividades_creadas += 1
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        # Comunicación
        print("   → Creando actividades COMUNICACIÓN...")
        for act in ACTIVIDADES_COMUNICACION:
            try:
                crear_actividad(act, 'comunicacion', db)
                actividades_creadas += 1
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        # Sensorial
        print("   → Creando actividades SENSORIAL...")
        for act in ACTIVIDADES_SENSORIAL:
            try:
                crear_actividad(act, 'sensorial', db)
                actividades_creadas += 1
            except Exception as e:
                print(f"   ✗ Error: {str(e)}")
        
        db.commit()
        print(f"   ✓ Total actividades creadas: {actividades_creadas}")
        
        # Resumen final
        print("\n" + "=" * 80)
        print("RESUMEN FINAL")
        print("=" * 80)
        
        total_ninos = db.execute(text("SELECT COUNT(*) FROM ninos")).scalar()
        total_perfiles_ninos = db.execute(text("SELECT COUNT(*) FROM perfil_nino_vectorizado")).scalar()
        total_actividades = db.execute(text("SELECT COUNT(*) FROM actividades")).scalar()
        total_perfiles_act = db.execute(text("SELECT COUNT(*) FROM perfil_actividad_vectorizada")).scalar()
        
        print(f"Niños totales: {total_ninos}")
        print(f"Perfiles de niños: {total_perfiles_ninos}")
        print(f"Actividades totales: {total_actividades}")
        print(f"Perfiles de actividades: {total_perfiles_act}")
        
        print("\n✓ Sistema completamente poblado")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ ERROR GENERAL: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

# Módulo TOPSIS y Recomendación - Autismo Mochis IA

Sistema completo de análisis de decisiones multiccriterio (TOPSIS) y recomendaciones basadas en contenido para el sistema "Autismo Mochis IA".

## 📋 Características

### Backend (FastAPI)

#### Módulo TOPSIS
- **Gestión de criterios**: CRUD completo para configurar criterios de evaluación
- **Cálculo de prioridad**: Algoritmo TOPSIS para priorizar niños según múltiples criterios
- **Pesos configurables**: Permite ajustar la importancia de cada criterio
- **Tipos de criterio**: Soporte para criterios de beneficio (mayor es mejor) y costo (menor es mejor)

#### Módulo Recomendación
- **Recomendación de actividades**: Basada en similitud de contenido entre perfil del niño y actividades
- **Recomendación de terapias**: Basada en similitud de contenido entre perfil del niño y terapias
- **Vectorización TF-IDF**: Procesamiento de texto para calcular similitudes
- **Top-N recomendaciones**: Configurable el número de recomendaciones a retornar

### Frontend (Angular)

#### Para COORDINADOR
- **Análisis TOPSIS**: Página para gestionar criterios y calcular prioridad de niños
- **Recomendaciones por niño**: Vista de actividades y terapias recomendadas para cada niño

#### Para TERAPEUTA
- **Panel de recomendaciones**: Vista de recomendaciones para todos sus pacientes asignados

## 🛠️ Instalación

### 1. Backend - Dependencias Python

Instalar las librerías necesarias:

```bash
cd backend
pip install numpy scikit-learn
```

### 2. Backend - Crear tablas en base de datos

Ejecutar el script de instalación:

```bash
cd backend
python scripts/setup_topsis_recomendacion.py
```

Este script creará:
- Tabla `criterio_topsis` con 5 criterios de ejemplo
- Tabla `actividades` con 5 actividades de ejemplo
- Campo `perfil_contenido` en tabla `ninos`
- Campos `categoria` y `tags` en tabla `terapias`

### 3. Backend - Verificar endpoints

El backend debería iniciarse sin errores:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Endpoints disponibles:
- `GET /api/v1/topsis/criterios` - Listar criterios
- `POST /api/v1/topsis/criterios` - Crear criterio
- `PUT /api/v1/topsis/criterios/{id}` - Actualizar criterio
- `DELETE /api/v1/topsis/criterios/{id}` - Eliminar criterio
- `POST /api/v1/topsis/prioridad-ninos` - Calcular prioridad TOPSIS
- `GET /api/v1/recomendacion/actividades/{nino_id}` - Recomendaciones de actividades
- `GET /api/v1/recomendacion/terapias/{nino_id}` - Recomendaciones de terapias

### 4. Frontend - Verificar rutas

Las rutas ya están configuradas:

**Coordinador:**
- `/coordinador/topsis-prioridad` - Análisis TOPSIS
- `/coordinador/recomendacion-nino` - Recomendaciones por niño

**Terapeuta:**
- `/terapeuta/recomendaciones` - Panel de recomendaciones

## 📊 Uso del Módulo TOPSIS

### Para Coordinadores

1. **Configurar criterios**
   - Ir a `/coordinador/topsis-prioridad`
   - Crear/editar criterios de evaluación
   - Asignar pesos (suma debe ser cercana a 1.0)
   - Definir tipo: beneficio o costo

2. **Evaluar niños**
   - Llenar la matriz de decisión con valores para cada niño/criterio
   - Ejemplo: severidad (1-10), faltas (número), progreso (1-10)
   - Hacer clic en "Calcular Prioridad"

3. **Revisar resultados**
   - Los niños se ordenan por score TOPSIS (0-1)
   - El ranking indica la prioridad (1 = mayor prioridad)
   - Usar esta información para tomar decisiones de asignación

### Ejemplo de criterios

```json
{
  "nombre": "Severidad del diagnóstico",
  "peso": 0.30,
  "tipo": "beneficio",  // Mayor severidad = mayor prioridad
  "descripcion": "Nivel de gravedad según especialista"
}
```

## 🎯 Uso del Módulo Recomendación

### Para Coordinadores

1. **Seleccionar niño**
   - Ir a `/coordinador/recomendacion-nino`
   - Seleccionar un niño del dropdown

2. **Revisar recomendaciones**
   - Ver actividades sugeridas con score de similitud
   - Ver terapias sugeridas con score de similitud
   - Usar esta información para planificar intervenciones

### Para Terapeutas

1. **Ver panel de recomendaciones**
   - Ir a `/terapeuta/recomendaciones`
   - Expandir cada paciente para ver sus recomendaciones
   - Las actividades están personalizadas según el perfil del niño

### Cómo funciona la recomendación

El sistema compara:
- **Perfil del niño**: diagnóstico, preferencias, dificultades, palabras clave
- **Características de actividades**: nombre, descripción, objetivo, tags, área de desarrollo
- **Características de terapias**: nombre, descripción, objetivo, categoría, tags

Usa TF-IDF + Similitud de Coseno para calcular qué actividades/terapias son más relevantes para cada niño.

## 📁 Estructura de archivos creados

### Backend

```
backend/
├── app/
│   ├── models/
│   │   ├── criterio_topsis.py          # Modelo de criterios TOPSIS
│   │   ├── actividad.py                # Modelo de actividades
│   │   ├── nino.py                     # Actualizado con perfil_contenido
│   │   └── terapia.py                  # Actualizado con categoria y tags
│   ├── schemas/
│   │   ├── topsis.py                   # Schemas Pydantic TOPSIS
│   │   └── recomendacion.py            # Schemas Pydantic Recomendación
│   ├── services/
│   │   ├── topsis_service.py           # Lógica TOPSIS (NumPy)
│   │   ├── vectorizer.py               # TF-IDF y similitud
│   │   └── recommend_service.py        # Lógica de recomendación
│   └── api/v1/endpoints/
│       ├── topsis.py                   # Endpoints TOPSIS
│       └── recomendacion.py            # Endpoints Recomendación
└── scripts/
    ├── crear_tablas_topsis_recomendacion.sql
    └── setup_topsis_recomendacion.py
```

### Frontend

```
src/app/
├── interfaces/
│   ├── topsis.interface.ts             # Interfaces TypeScript TOPSIS
│   └── recomendacion.interface.ts      # Interfaces TypeScript Recomendación
├── service/
│   ├── topsis.service.ts               # Servicio Angular TOPSIS
│   └── recomendacion.service.ts        # Servicio Angular Recomendación
├── coordinador/
│   ├── prioridad-ninos/                # Componente TOPSIS
│   │   ├── prioridad-ninos.ts
│   │   ├── prioridad-ninos.html
│   │   └── prioridad-ninos.scss
│   └── recomendacion-nino/             # Componente Recomendaciones
│       ├── recomendacion-nino.ts
│       ├── recomendacion-nino.html
│       └── recomendacion-nino.scss
└── terapeuta/
    └── recomendacion-panel/             # Panel terapeuta
        ├── recomendacion-panel.ts
        ├── recomendacion-panel.html
        └── recomendacion-panel.scss
```

## 🔧 Configuración avanzada

### Ajustar perfiles de niños

Para mejorar las recomendaciones, actualizar el campo `perfil_contenido` en la tabla `ninos`:

```json
{
  "tags": ["autismo", "lenguaje", "social"],
  "intereses": "Construcción, música, animales",
  "dificultades": "Comunicación verbal, interacción social",
  "diagnostico": "TEA nivel 2"
}
```

### Agregar actividades personalizadas

```sql
INSERT INTO actividades (nombre, descripcion, tags, dificultad, area_desarrollo) 
VALUES (
  'Mi actividad',
  'Descripción...',
  JSON_ARRAY('tag1', 'tag2'),
  2,
  'motor'
);
```

### Ajustar tags de terapias

```sql
UPDATE terapias 
SET tags = JSON_ARRAY('lenguaje', 'expresión', 'comunicación'),
    categoria = 'Lenguaje y comunicación'
WHERE id = 1;
```

## 🐛 Solución de problemas

### Error: No hay criterios TOPSIS
- Verificar que se ejecutó `setup_topsis_recomendacion.py`
- Crear criterios manualmente desde la interfaz

### Error: Recomendaciones vacías
- Verificar que existan actividades en la BD
- Verificar que el niño tenga datos en `perfil_contenido`
- Revisar que las terapias tengan `tags` y `categoria`

### Error de importación en Python
- Instalar dependencias: `pip install numpy scikit-learn`

## 📚 Referencias

- **TOPSIS**: Technique for Order of Preference by Similarity to Ideal Solution
- **TF-IDF**: Term Frequency-Inverse Document Frequency
- **Similitud de Coseno**: Medida de similitud entre vectores

## 👥 Roles y permisos

- **COORDINADOR**: Acceso completo a TOPSIS y recomendaciones de todos los niños
- **TERAPEUTA**: Acceso a recomendaciones solo de sus pacientes asignados

## 🎉 ¡Sistema listo!

El módulo está completamente integrado y listo para usar. Los coordinadores pueden comenzar a crear criterios TOPSIS y los terapeutas verán recomendaciones personalizadas para sus pacientes.

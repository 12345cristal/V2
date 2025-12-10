# 🎯 Sistema de Recomendaciones Inteligentes

## 📋 Descripción General

Sistema completo de recomendaciones que integra tres tecnologías complementarias:

1. **Recomendación basada en contenido** → Sugiere qué terapias y actividades
2. **TOPSIS** → Selecciona el mejor terapeuta
3. **Gemini AI** → Genera explicaciones en lenguaje natural

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1️⃣ PERFIL DEL NIÑO                                     │
│     ├─ Gemini genera embedding vectorial                │
│     ├─ Edad, diagnósticos, dificultades                 │
│     └─ Notas clínicas vectorizadas                      │
│                                                          │
│  2️⃣ RECOMENDACIÓN DE ACTIVIDADES                        │
│     ├─ Similitud coseno con actividades vectorizadas    │
│     ├─ Ranking por score de similitud                   │
│     └─ Gemini explica por qué son adecuadas             │
│                                                          │
│  3️⃣ SELECCIÓN DE TERAPEUTA (TOPSIS)                     │
│     ├─ Matriz de criterios (experiencia, carga, etc.)   │
│     ├─ Cálculo de score TOPSIS                          │
│     ├─ Ranking de terapeutas                            │
│     └─ Gemini justifica la selección                    │
│                                                          │
│  4️⃣ RESULTADO INTEGRADO                                 │
│     └─ Recomendación completa + Explicación clínica     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🗄️ Estructura de Base de Datos

### Tablas Creadas

#### 1. `perfil_nino_vectorizado`
Almacena embeddings del perfil completo del niño.

```sql
- id: INT (PK)
- nino_id: INT (FK → ninos.id) UNIQUE
- embedding: JSON (vector de floats)
- edad: INT
- diagnosticos: JSON ['TEA', 'TDAH']
- dificultades: JSON
- fortalezas: JSON
- texto_perfil: TEXT
- fecha_generacion: DATETIME
- fecha_actualizacion: DATETIME
```

#### 2. `perfil_actividad_vectorizada`
Embeddings de actividades terapéuticas.

```sql
- id: INT (PK)
- actividad_id: INT (FK → actividades.id) UNIQUE
- embedding: JSON
- areas_desarrollo: JSON
- tags: JSON
- nivel_dificultad: SMALLINT
- texto_descripcion: TEXT
- fecha_generacion: DATETIME
```

#### 3. `historial_progreso`
Registro de progreso para aprendizaje colaborativo.

```sql
- id: INT (PK)
- nino_id: INT (FK)
- actividad_id: INT (FK)
- terapeuta_id: INT (FK)
- calificacion: DECIMAL(3,2) [1.0-5.0]
- notas_progreso: TEXT
- fecha_sesion: DATETIME
- embedding_notas: JSON
```

#### 4. `recomendaciones_actividades`
Recomendaciones generadas.

```sql
- id: INT (PK)
- nino_id: INT (FK)
- actividades_recomendadas: JSON
- explicacion_humana: TEXT
- metodo: VARCHAR(50) [contenido|colaborativo|hibrido]
- fecha_generacion: DATETIME
- aplicada: TINYINT
```

#### 5. `asignaciones_terapeuta_topsis`
Resultados de selección con TOPSIS.

```sql
- id: INT (PK)
- nino_id: INT (FK)
- terapia_tipo: VARCHAR(100)
- ranking_terapeutas: JSON
- terapeuta_seleccionado_id: INT (FK)
- explicacion_seleccion: TEXT
- criterios_usados: JSON
- fecha_calculo: DATETIME
```

## 🚀 Instalación

### 1. Requisitos Previos

```bash
# Instalar dependencias de Python
pip install google-generativeai numpy

# O agregar a requirements.txt
google-generativeai>=0.3.0
numpy>=1.24.0
```

### 2. Configuración de Gemini API

Agregar en `.env`:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

**Obtener API Key:**
1. Visita: https://makersuite.google.com/app/apikey
2. Crea un proyecto en Google AI Studio
3. Genera una API key
4. Copia la key al archivo `.env`

### 3. Ejecutar Script de Instalación

```bash
cd backend
python scripts/init_sistema_recomendaciones.py
```

Este script:
- ✓ Crea todas las tablas necesarias
- ✓ Vectoriza actividades existentes
- ✓ Genera perfiles de niños de ejemplo
- ✓ Verifica la instalación

## 📡 API Endpoints

### 1. Recomendar Actividades

**Endpoint:** `POST /api/v1/recomendaciones/actividades/{nino_id}`

**Query Params:**
- `top_n`: Número de actividades (default: 5)
- `incluir_explicacion`: Boolean (default: true)

**Respuesta:**
```json
{
  "nino_id": 1,
  "recomendaciones": [
    {
      "actividad_id": 5,
      "nombre": "Juegos de turn-taking con imágenes",
      "descripcion": "...",
      "score": 0.95,
      "area_desarrollo": "lenguaje",
      "tags": ["comunicación", "visual"]
    }
  ],
  "explicacion": "Estas actividades son ideales porque...",
  "fecha_generacion": "2025-12-09T10:30:00"
}
```

### 2. Seleccionar Terapeuta Óptimo

**Endpoint:** `POST /api/v1/recomendaciones/terapeuta/{nino_id}`

**Body:**
```json
{
  "terapia_tipo": "lenguaje",
  "criterios_pesos": {
    "experiencia": 0.30,
    "disponibilidad": 0.25,
    "carga_trabajo": 0.20,
    "evaluacion_desempeno": 0.15,
    "especializacion": 0.10
  }
}
```

**Respuesta:**
```json
{
  "nino_id": 1,
  "terapia_tipo": "lenguaje",
  "terapeuta_seleccionado": {
    "id": 5,
    "nombre": "Dra. María López",
    "score": 0.98,
    "posicion": 1,
    "experiencia_anos": 8,
    "especialidad": "Lenguaje y comunicación"
  },
  "ranking_completo": [...],
  "explicacion": "La Dra. López es la opción óptima porque...",
  "criterios_usados": {...}
}
```

### 3. Flujo Completo (TODO EN UNO)

**Endpoint:** `POST /api/v1/recomendaciones/completa/{nino_id}`

**Body:**
```json
{
  "terapia_tipo": "conductual"
}
```

**Respuesta:**
```json
{
  "nino": {
    "id": 1,
    "nombre": "Marco Pérez"
  },
  "actividades_recomendadas": {
    "recomendaciones": [...],
    "explicacion": "..."
  },
  "terapeuta_asignado": {
    "terapeuta_seleccionado": {...},
    "explicacion": "..."
  },
  "fecha_generacion": "2025-12-09T10:30:00"
}
```

### 4. Registrar Progreso

**Endpoint:** `POST /api/v1/recomendaciones/progreso/registrar`

**Body:**
```json
{
  "nino_id": 1,
  "actividad_id": 5,
  "terapeuta_id": 3,
  "calificacion": 4.5,
  "notas_progreso": "El niño mostró gran interés en las tarjetas PECS...",
  "duracion_minutos": 45
}
```

### 5. Generar Sugerencias Clínicas

**Endpoint:** `POST /api/v1/recomendaciones/sugerencias/{nino_id}`

**Body:**
```json
{
  "incluir_actividades_actuales": true,
  "incluir_progreso_reciente": true
}
```

**Respuesta:**
```json
{
  "nino_id": 1,
  "sugerencias": "Basado en el progreso reciente, recomiendo:\n1. Intensificar ejercicios de imitación bucofacial...\n2. Incorporar música suave de fondo...",
  "contexto_usado": {
    "actividades_actuales": ["PECS Nivel 2", "Imitación"],
    "progreso_incluido": true
  }
}
```

### 6. Historial de Recomendaciones

**Endpoint:** `GET /api/v1/recomendaciones/historial/{nino_id}?limite=10`

## 🧠 Cómo Funciona

### Similitud de Contenido (Vector Embeddings)

1. **Gemini genera embeddings** del perfil del niño:
   - Diagnósticos
   - Dificultades
   - Fortalezas
   - Notas clínicas

2. **Cada actividad también tiene embedding**

3. **Similitud coseno** mide qué tan "cercanas" son:
   ```
   similitud = (A · B) / (||A|| × ||B||)
   ```

4. **Actividades con mayor similitud** = más adecuadas

### TOPSIS (Selección de Terapeuta)

**Criterios evaluados:**

| Criterio | Peso | Tipo | Descripción |
|----------|------|------|-------------|
| Experiencia | 30% | Beneficio | Años de práctica |
| Disponibilidad | 25% | Beneficio | Horarios libres |
| Carga de trabajo | 20% | Costo | Número de pacientes |
| Evaluación | 15% | Beneficio | Desempeño promedio |
| Especialización | 10% | Beneficio | Nivel en el área |

**Proceso:**
1. Normalización vectorial
2. Aplicación de pesos
3. Cálculo de ideales (mejor y peor)
4. Distancias euclidianas
5. Score de proximidad relativa

### Gemini AI (Explicaciones)

Gemini se usa para:

1. **Generar embeddings** de texto libre
2. **Explicar recomendaciones** en lenguaje natural
3. **Justificar selecciones** de terapeutas
4. **Generar sugerencias** clínicas personalizadas

## 💡 Casos de Uso

### Caso 1: Planificación de Sesión

**Terapeuta quiere planificar sesión para Marco:**

```bash
POST /api/v1/recomendaciones/actividades/1?top_n=5
```

**Sistema responde:**
- Top 5 actividades más adecuadas
- Explicación de por qué son buenas
- Score de similitud para cada una

### Caso 2: Asignación de Terapeuta

**Coordinador necesita asignar terapeuta de lenguaje:**

```bash
POST /api/v1/recomendaciones/terapeuta/1
{
  "terapia_tipo": "lenguaje"
}
```

**Sistema responde:**
- Ranking completo de terapeutas
- Score TOPSIS para cada uno
- Explicación clínica de la mejor opción

### Caso 3: Decisión Integral

**Coordinador quiere plan completo:**

```bash
POST /api/v1/recomendaciones/completa/1
{
  "terapia_tipo": "lenguaje"
}
```

**Sistema responde:**
- Actividades recomendadas
- Terapeuta óptimo
- Justificación completa generada por Gemini

## 🔧 Configuración Avanzada

### Personalizar Pesos de TOPSIS

```python
criterios_custom = {
    "experiencia": 0.40,      # Más peso a experiencia
    "disponibilidad": 0.15,
    "carga_trabajo": 0.25,    # Más peso a carga
    "evaluacion_desempeno": 0.10,
    "especializacion": 0.10
}
```

### Ajustar Número de Recomendaciones

```python
# En el servicio
resultado = servicio.recomendar_actividades(
    nino_id=1,
    top_n=10,  # Más actividades
    incluir_explicacion=True
)
```

## 📊 Monitoreo y Análisis

### Estadísticas Disponibles

```sql
-- Actividades más recomendadas
SELECT 
    a.nombre,
    COUNT(*) as veces_recomendada
FROM recomendaciones_actividades ra
JOIN actividades a ON JSON_CONTAINS(ra.actividades_recomendadas, JSON_OBJECT('actividad_id', a.id))
GROUP BY a.id
ORDER BY veces_recomendada DESC
LIMIT 10;

-- Terapeutas más seleccionados
SELECT 
    p.nombres,
    COUNT(*) as veces_seleccionado,
    AVG(JSON_EXTRACT(ranking_terapeutas, '$[0].score')) as score_promedio
FROM asignaciones_terapeuta_topsis at
JOIN personal p ON at.terapeuta_seleccionado_id = p.id
GROUP BY p.id
ORDER BY veces_seleccionado DESC;

-- Efectividad de actividades
SELECT 
    a.nombre,
    AVG(hp.calificacion) as calificacion_promedio,
    COUNT(*) as sesiones_realizadas
FROM historial_progreso hp
JOIN actividades a ON hp.actividad_id = a.id
GROUP BY a.id
ORDER BY calificacion_promedio DESC;
```

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY no configurada"

**Solución:**
```bash
# Verificar que existe en .env
cat .env | grep GEMINI_API_KEY

# Si no existe, agregar:
echo "GEMINI_API_KEY=tu_key_aqui" >> .env
```

### Error: "No hay actividades vectorizadas"

**Solución:**
```bash
# Re-ejecutar vectorización
python scripts/init_sistema_recomendaciones.py
```

### Gemini retorna embeddings vacíos

**Solución:**
1. Verificar que la API key es válida
2. Verificar conectividad a internet
3. Revisar límites de cuota de Google AI

## 📈 Mejoras Futuras

- [ ] Aprendizaje colaborativo (filtrado híbrido)
- [ ] Clustering de niños similares
- [ ] Predicción de progreso con ML
- [ ] Dashboard de analytics
- [ ] Integración con calendario de sesiones

## 📞 Soporte

Para problemas o preguntas, consultar:
- Documentación de Gemini: https://ai.google.dev/docs
- Documentación de TOPSIS: [Ver archivo TOPSIS_PROFESIONAL.md]

---

**Última actualización:** 9 de diciembre de 2025  
**Versión:** 1.0.0

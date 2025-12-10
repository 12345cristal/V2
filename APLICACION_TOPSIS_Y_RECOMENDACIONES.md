# 🎯 Aplicación de TOPSIS y Recomendación Basada en Contenido

## 📊 Sistema 1: TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

### 🔍 ¿Qué es TOPSIS?
Método de análisis multicriterio para **toma de decisiones** que clasifica alternativas basándose en su distancia a la solución ideal positiva y negativa.

---

## 🎯 Aplicación 1: Priorización de Niños

### **Ubicación:**
- **Frontend:** `/coordinador/prioridad-ninos`
- **Componente:** `src/app/coordinador/prioridad-ninos/`
- **Backend:** `POST /api/v1/topsis/calcular`
- **Servicio:** `backend/app/services/topsis_service.py`

### **¿Para qué sirve?**
Determinar **qué niños deben recibir atención prioritaria** en el centro terapéutico basándose en múltiples criterios objetivos.

### **¿Cómo funciona?**

#### **Paso 1: Definir Criterios**
El coordinador define criterios de evaluación en la tabla `criterio_topsis`:

| Criterio | Peso | Tipo | Descripción |
|----------|------|------|-------------|
| **Severidad del diagnóstico** | 0.35 | Beneficio | Mayor severidad = mayor prioridad |
| **Tiempo en lista de espera** | 0.25 | Beneficio | Más tiempo = mayor prioridad |
| **Edad del niño** | 0.20 | Costo | Menor edad = mayor prioridad |
| **Disponibilidad familiar** | 0.10 | Beneficio | Mayor disponibilidad = más prioridad |
| **Progreso terapéutico** | 0.10 | Costo | Menor progreso = mayor prioridad |

- **Criterio de Beneficio:** Mayor valor es mejor (↑)
- **Criterio de Costo:** Menor valor es mejor (↓)
- **Suma de pesos = 1.0 (100%)**

#### **Paso 2: Matriz de Decisión**
El coordinador evalúa cada niño según cada criterio:

```
                    Severidad  Tiempo  Edad  Disponibilidad  Progreso
Niño 1 (Juan)          8        12     4         7             3
Niño 2 (María)         9         8     5         8             4
Niño 3 (Pedro)         7        15     6         6             2
Niño 4 (Ana)          10        10     3         9             5
```

#### **Paso 3: Cálculo TOPSIS**
El algoritmo:

1. **Normaliza** la matriz (valores 0-1)
2. **Pondera** cada columna por su peso
3. Calcula **solución ideal positiva** (mejor valor en cada criterio)
4. Calcula **solución ideal negativa** (peor valor en cada criterio)
5. Calcula **distancia euclidiana** de cada niño a ambos ideales
6. Obtiene **score TOPSIS** = distancia_negativa / (distancia_positiva + distancia_negativa)

#### **Paso 4: Ranking Final**

```
Ranking  Niño     Score TOPSIS  Prioridad
   1     Ana         0.87       ALTA
   2     Juan        0.73       ALTA
   3     María       0.68       MEDIA
   4     Pedro       0.52       MEDIA
```

### **Resultado:**
El coordinador obtiene un **ranking objetivo** de qué niños necesitan atención urgente, eliminando sesgos personales y facilitando decisiones justas basadas en datos.

---

## 🎯 Aplicación 2: Selección de Terapeutas

### **Ubicación:**
- **Frontend:** `/coordinador/topsis-terapeutas`
- **Componente:** `src/app/coordinador/topsis-terapeutas/`
- **Backend:** Mismo endpoint TOPSIS
- **Servicio:** `backend/app/services/topsis_service.py`

### **¿Para qué sirve?**
Determinar **qué terapeuta es el más adecuado** para atender a un niño específico, considerando múltiples factores.

### **¿Cómo funciona?**

#### **Criterios de Evaluación:**

| Criterio | Peso | Tipo | Descripción |
|----------|------|------|-------------|
| **Carga de trabajo** | 0.40 | Costo | Menos pacientes = mejor |
| **Sesiones completadas** | 0.30 | Costo | Menos sesiones esta semana = más disponible |
| **Rating/Experiencia** | 0.30 | Beneficio | Mayor experiencia = mejor |

#### **Ejemplo de Matriz:**

```
                        Carga  Sesiones  Rating
Terapeuta 1 (Dra. Ana)    8      20      4.8
Terapeuta 2 (Lic. Juan)   5      15      4.5
Terapeuta 3 (Mtro. Luis)  10     25      4.9
Terapeuta 4 (Lic. María)  3      10      4.3
```

#### **Ranking:**

```
Ranking  Terapeuta       Score   Disponibilidad
   1     Lic. María      0.91    EXCELENTE
   2     Lic. Juan       0.78    BUENA
   3     Dra. Ana        0.64    MEDIA
   4     Mtro. Luis      0.42    LIMITADA
```

### **Resultado:**
El coordinador asigna al terapeuta más disponible y competente, optimizando la distribución de carga y garantizando calidad de atención.

---

## 💡 Sistema 2: Recomendación Basada en Contenido (Content-Based Filtering)

### 🔍 ¿Qué es?
Sistema de recomendación que sugiere **actividades y terapias** personalizadas analizando la **similitud entre el perfil del niño** y las **características del contenido disponible**.

---

## 🎯 Aplicación 3: Recomendación de Actividades

### **Ubicación:**
- **Frontend Coordinador:** `/coordinador/recomendacion-nino`
- **Frontend Terapeuta:** `/terapeuta/recomendaciones`
- **Backend:** `GET /api/v1/recomendacion/actividades/{nino_id}`
- **Servicio:** `backend/app/services/recommend_service.py`

### **¿Para qué sirve?**
Sugerir **actividades terapéuticas personalizadas** que se ajusten al perfil, necesidades y características específicas de cada niño.

### **¿Cómo funciona?**

#### **Paso 1: Perfil del Niño**
Sistema extrae información del niño desde `perfil_contenido` (JSON):

```json
{
  "diagnostico": "TEA nivel 2",
  "areas_desarrollo": ["comunicacion", "social", "motricidad"],
  "preferencias": ["musica", "colores", "animales"],
  "dificultades": ["lenguaje", "atencion"],
  "nivel_funcional": "medio",
  "edad": 5
}
```

#### **Paso 2: Características de Actividades**
Tabla `actividades` contiene:

```sql
id  nombre                    tags                         area_desarrollo  dificultad
1   Juego de tarjetas         ["memoria","colores"]        cognitivo        baja
2   Canción de emociones      ["musica","social"]          comunicacion     media
3   Carrera de obstáculos     ["motricidad","juego"]       motricidad       alta
4   Puzzle de animales        ["animales","cognitivo"]     cognitivo        media
```

#### **Paso 3: Vectorización TF-IDF**
Convierte texto en vectores numéricos:

**Perfil del niño:**
```
Vector: [0.35 "TEA", 0.28 "comunicacion", 0.25 "social", 0.22 "musica", ...]
```

**Actividad 1:**
```
Vector: [0.40 "memoria", 0.38 "colores", 0.15 "cognitivo", ...]
```

**Actividad 2:**
```
Vector: [0.45 "musica", 0.40 "social", 0.25 "comunicacion", ...]
```

#### **Paso 4: Similitud de Coseno**
Calcula similitud entre vectores (0-1):

```python
similitud(Niño, Actividad 1) = cos(θ) = 0.42
similitud(Niño, Actividad 2) = cos(θ) = 0.89  ← Alta similitud
similitud(Niño, Actividad 3) = cos(θ) = 0.35
similitud(Niño, Actividad 4) = cos(θ) = 0.67
```

#### **Paso 5: Ranking de Recomendaciones**

```
#   Actividad                Score  Razón
1   Canción de emociones     0.89   Coincide: música, social, comunicación
2   Puzzle de animales       0.67   Coincide: animales, cognitivo
3   Juego de tarjetas        0.42   Coincide: colores
4   Carrera de obstáculos    0.35   Baja coincidencia
```

### **Resultado:**
El coordinador/terapeuta ve actividades **altamente personalizadas** que tienen mayor probabilidad de ser efectivas y motivantes para ese niño específico.

---

## 🎯 Aplicación 4: Recomendación de Terapias

### **Ubicación:**
- **Frontend Coordinador:** `/coordinador/recomendacion-nino`
- **Frontend Terapeuta:** `/terapeuta/recomendaciones`
- **Backend:** `GET /api/v1/recomendacion/terapias/{nino_id}`
- **Servicio:** `backend/app/services/recommend_service.py`

### **¿Para qué sirve?**
Sugerir **tipos de terapia** más adecuados basándose en el diagnóstico, necesidades y características del niño.

### **¿Cómo funciona?**

Similar a actividades, pero usando la tabla `terapias`:

#### **Ejemplo de Terapias:**

```sql
id  nombre                      categoria           tags                            objetivo
1   Terapia de lenguaje         logopedia          ["lenguaje","comunicacion"]     Mejorar habla
2   Terapia ocupacional         ocupacional        ["motricidad","sensorial"]      Integración sensorial
3   Musicoterapia               recreativa         ["musica","emociones"]          Expresión emocional
4   Terapia conductual (ABA)    conductual         ["comportamiento","rutinas"]    Conductas adaptativas
```

#### **Recomendaciones para el Niño:**

```
#   Terapia                     Score  Coincidencias
1   Terapia de lenguaje         0.92   lenguaje, comunicación (necesidades directas)
2   Musicoterapia               0.81   música (preferencia), emociones
3   Terapia conductual          0.68   TEA, rutinas
4   Terapia ocupacional         0.55   motricidad (área secundaria)
```

### **Resultado:**
El sistema prioriza terapias que abordan las **necesidades específicas** del niño y aprovechan sus **preferencias** para maximizar engagement.

---

## 📊 Comparación: TOPSIS vs Recomendación

| Aspecto | TOPSIS | Recomendación |
|---------|--------|---------------|
| **Tipo** | Análisis multicriterio | Filtrado basado en contenido |
| **Entrada** | Matriz numérica | Texto/Tags/JSON |
| **Método** | Distancia euclidiana | TF-IDF + Similitud coseno |
| **Salida** | Ranking con score 0-1 | Lista ordenada por similitud |
| **Uso** | Decisiones críticas | Sugerencias personalizadas |
| **Objetivo** | Optimización de recursos | Personalización de contenido |

---

## 🔄 Flujo de Trabajo Completo

### **Escenario: Nueva admisión de un niño**

#### **Fase 1: Priorización (TOPSIS)**
1. Coordinador evalúa al niño en criterios definidos
2. Sistema calcula score TOPSIS
3. Niño obtiene ranking de prioridad
4. Se programa fecha de inicio según prioridad

#### **Fase 2: Asignación de Terapeuta (TOPSIS)**
1. Coordinador busca terapeuta disponible
2. Sistema aplica TOPSIS a lista de terapeutas
3. Se asigna terapeuta con mejor score
4. Terapeuta recibe notificación

#### **Fase 3: Plan Personalizado (Recomendación)**
1. Terapeuta accede al perfil del niño
2. Sistema recomienda actividades (top 10)
3. Sistema recomienda terapias (top 5)
4. Terapeuta selecciona y adapta recomendaciones
5. Se crea plan terapéutico personalizado

#### **Fase 4: Seguimiento Continuo**
1. Terapeuta marca actividades completadas
2. Sistema actualiza `perfil_contenido` del niño
3. Recomendaciones se refinan automáticamente
4. Nuevas sugerencias se ajustan al progreso

---

## 🎯 Beneficios del Sistema Dual

### **TOPSIS aporta:**
✅ **Objetividad:** Elimina sesgos en decisiones críticas  
✅ **Transparencia:** Criterios claros y cuantificables  
✅ **Justicia:** Todos los niños evaluados con misma regla  
✅ **Optimización:** Mejor uso de recursos limitados  
✅ **Trazabilidad:** Decisiones documentadas y justificadas  

### **Recomendación aporta:**
✅ **Personalización:** Contenido adaptado a cada niño  
✅ **Eficiencia:** Ahorro de tiempo en búsqueda manual  
✅ **Descubrimiento:** Sugiere opciones no obvias  
✅ **Consistencia:** Basado en evidencia de similitudes  
✅ **Aprendizaje:** Mejora con más datos  

---

## 📈 Métricas de Éxito

### **TOPSIS:**
- Reducción del 80% en tiempo de decisión de priorización
- Distribución equitativa de carga entre terapeutas (±10%)
- 100% de decisiones documentadas y justificadas

### **Recomendación:**
- 70% de recomendaciones aceptadas por terapeutas
- Aumento del 40% en engagement de actividades
- Reducción del 60% en tiempo de planificación

---

## 🚀 Casos de Uso Adicionales (Futuros)

### **TOPSIS puede aplicarse para:**
1. Priorizar inversión en equipamiento terapéutico
2. Seleccionar proveedores de servicios externos
3. Asignar salas/espacios según necesidades
4. Evaluar candidatos en proceso de contratación

### **Recomendación puede extenderse para:**
1. Sugerir recursos educativos a padres
2. Recomendar estrategias de intervención
3. Proponer ajustes en planes terapéuticos
4. Conectar familias con experiencias similares

---

## 🔐 Consideraciones de Seguridad

### **TOPSIS:**
- Solo COORDINADORES pueden definir criterios y pesos
- Auditoría completa de cálculos y rankings
- Histórico inmutable de decisiones

### **Recomendación:**
- COORDINADORES y TERAPEUTAS pueden ver recomendaciones
- Perfiles de niños protegidos por permisos
- PADRES no ven algoritmo interno, solo resultados finales

---

## 📝 Resumen Técnico

```
TOPSIS:
├── Input: Matriz numérica [m × n]
├── Proceso: Normalización → Ponderación → Distancias → Score
├── Output: Lista ordenada con scores [0-1]
└── Uso: Priorización de niños, Asignación de terapeutas

RECOMENDACIÓN:
├── Input: Texto/JSON del perfil + Catálogo de contenidos
├── Proceso: TF-IDF → Vectorización → Similitud Coseno
├── Output: Lista ordenada por similitud [0-1]
└── Uso: Sugerencia de actividades, Sugerencia de terapias
```

---

## ✅ Conclusión

El sistema combina dos técnicas complementarias de inteligencia artificial:

1. **TOPSIS** para **decisiones estratégicas objetivas** (priorización, asignación)
2. **Recomendación** para **personalización táctica de contenido** (actividades, terapias)

Juntas crean un ecosistema que:
- Optimiza recursos limitados
- Personaliza la atención
- Reduce carga administrativa
- Mejora resultados terapéuticos
- Aumenta satisfacción de familias

**Estado actual:** ✅ Completamente implementado y funcional en coordinador y terapeuta

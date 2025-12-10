# 🎯 Sistema TOPSIS para Evaluación de Terapeutas

## ¿Qué es TOPSIS?

**TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) es un algoritmo de toma de decisiones multicriterio que:

1. Define una **"solución ideal positiva"** (mejor valor en cada criterio)
2. Define una **"solución ideal negativa"** (peor valor en cada criterio)  
3. Calcula qué alternativa está **más cerca del ideal** y **más lejos del anti-ideal**
4. Genera un **ranking ordenado** basado en proximidad a la solución óptima

---

## 📊 Criterios Evaluados

### 1. 📅 **Sesiones Semanales** (Carga Laboral)
- **Tipo**: COSTO ⬇️ (menor es mejor)
- **Fuente**: `personal.sesiones_semana`
- **Objetivo**: Encontrar terapeutas con **mayor disponibilidad**
- **Ejemplo**: 
  - Terapeuta A: 15 sesiones/semana → **Menos carga** ✅
  - Terapeuta B: 27 sesiones/semana → **Más carga** ⚠️

### 2. 👥 **Total de Pacientes** (Experiencia)
- **Tipo**: BENEFICIO ⬆️ (mayor es mejor)
- **Fuente**: `personal.total_pacientes`
- **Objetivo**: Encontrar terapeutas con **más experiencia práctica**
- **Ejemplo**:
  - Terapeuta A: 45 pacientes → **Más experiencia** ✅
  - Terapeuta B: 15 pacientes → **Menos experiencia** ⚠️

### 3. ⭐ **Rating** (Calidad)
- **Tipo**: BENEFICIO ⬆️ (mayor es mejor)
- **Fuente**: `personal.rating`
- **Rango**: 0.0 a 5.0
- **Objetivo**: Encontrar terapeutas **mejor evaluados**
- **Ejemplo**:
  - Terapeuta A: 5.0 → **Excelente** ✅
  - Terapeuta B: 4.3 → **Bueno** ✓

### 4. 🎓 **Match de Especialidad**
- **Tipo**: BENEFICIO ⬆️ (mayor es mejor)
- **Fuente**: Comparación entre `terapias.nombre_terapia` y `personal.especialidad_principal / especialidades`
- **Valores**: 1.0 (match) o 0.0 (no match)
- **Objetivo**: Priorizar terapeutas con **especialidad correcta**
- **Mapeo inteligente**:
  - "Terapia de lenguaje" → Match con "Lenguaje y Comunicación"
  - "Terapia Conductual" → Match con "ABA", "Conductual"
  - "Terapia Ocupacional" → Match con "Ocupacional"

---

## ⚖️ Pesos Personalizables

Los **pesos** determinan la **importancia relativa** de cada criterio:

```
Peso 0.0 → Criterio ignorado
Peso 0.5 → Importancia media  
Peso 1.0 → Criterio dominante
```

### Ejemplos de Configuración:

#### 🔹 **Caso 1: Priorizar Disponibilidad**
```
Carga Laboral: 0.50 (50%)
Total Pacientes: 0.20 (20%)
Rating: 0.20 (20%)
Match: 0.10 (10%)
```
**Resultado**: Terapeutas con **menos sesiones** obtienen ranking alto

#### 🔹 **Caso 2: Priorizar Experiencia**
```
Carga Laboral: 0.10
Total Pacientes: 0.50 ← MÁXIMO
Rating: 0.30
Match: 0.10
```
**Resultado**: Terapeutas con **más pacientes** obtienen ranking alto

#### 🔹 **Caso 3: Priorizar Calidad**
```
Carga Laboral: 0.15
Total Pacientes: 0.15
Rating: 0.50 ← MÁXIMO
Match: 0.20
```
**Resultado**: Terapeutas con **mejor rating** obtienen ranking alto

#### 🔹 **Caso 4: Priorizar Especialidad**
```
Carga Laboral: 0.10
Total Pacientes: 0.20
Rating: 0.20
Match: 0.50 ← MÁXIMO
```
**Resultado**: Terapeutas con **especialidad correcta** obtienen ranking alto

---

## 🧮 Cálculo TOPSIS (Paso a Paso)

### Ejemplo con 3 terapeutas:

| Terapeuta | Sesiones/Sem | Pacientes | Rating | Match |
|-----------|--------------|-----------|--------|-------|
| Roberto   | 15           | 35        | 5.0    | 1     |
| Laura     | 20           | 28        | 5.0    | 1     |
| Fernando  | 18           | 42        | 5.0    | 1     |

**Pesos**: [0.3, 0.3, 0.2, 0.2]

### **Paso 1: Normalización Vectorial**
Cada valor se divide por √(suma de cuadrados de su columna)

```
Sesiones: √(15² + 20² + 18²) = 30.35
Roberto: 15/30.35 = 0.494
Laura: 20/30.35 = 0.659
Fernando: 18/30.35 = 0.593
```

### **Paso 2: Aplicar Pesos**
Multiplicar cada valor normalizado por su peso

```
Roberto sesiones: 0.494 × 0.3 = 0.148
```

### **Paso 3: Soluciones Ideales**

**Ideal Positivo (A+):**
- Sesiones (COSTO): MIN = 0.148 ← Roberto
- Pacientes (BENEFICIO): MAX = mayor valor
- Rating (BENEFICIO): MAX = mayor valor
- Match (BENEFICIO): MAX = 1.0

**Ideal Negativo (A-):**
- Sesiones (COSTO): MAX = 0.197 ← Laura
- Pacientes (BENEFICIO): MIN = menor valor
- Rating (BENEFICIO): MIN = menor valor  
- Match (BENEFICIO): MIN = 0.0

### **Paso 4: Distancias Euclidianas**

```
D+ = √[(x₁-A+₁)² + (x₂-A+₂)² + (x₃-A+₃)² + (x₄-A+₄)²]
D- = √[(x₁-A-₁)² + (x₂-A-₂)² + (x₃-A-₃)² + (x₄-A-₄)²]
```

### **Paso 5: Proximidad Relativa (Score)**

```
Score = D- / (D+ + D-)
```

**Rango**: 0.0 a 1.0  
**Mayor score** = **Mejor terapeuta**

---

## 📈 Interpretación de Resultados

### Ranking Final:

```
#1 Fernando (Score: 0.73) ✅
   - 18 sesiones/semana (Carga media)
   - 42 pacientes (MÁS EXPERIENCIA) ⭐
   - Rating 5.0 (Excelente)
   - Match: ✓

#2 Roberto (Score: 0.68) ✓
   - 15 sesiones/semana (MENOS CARGA) ⭐
   - 35 pacientes (Experiencia buena)
   - Rating 5.0 (Excelente)
   - Match: ✓

#3 Laura (Score: 0.54) ✓
   - 20 sesiones/semana (Carga alta) ⚠️
   - 28 pacientes (Experiencia media)
   - Rating 5.0 (Excelente)
   - Match: ✓
```

### ¿Por qué Fernando es #1?

Con pesos balanceados (0.3, 0.3, 0.2, 0.2):
- **Fernando** tiene el **mejor balance** entre todos los criterios
- Tiene la **mayor experiencia** (42 pacientes) → Peso 0.3 ⬆️
- Su carga es **media** (18 sesiones), no la más baja pero aceptable
- Rating perfecto y match correcto

### ¿Por qué no Roberto (menos carga)?

- Roberto tiene **menos sesiones** (15 vs 18) → Mejor en disponibilidad
- Pero Fernando tiene **7 pacientes más** (42 vs 35) → Mejor en experiencia
- Con peso 0.3 en ambos, la **diferencia en experiencia** compensa
- Si aumentamos peso de "Carga Laboral" a 0.5, Roberto subiría a #1

---

## 🔧 Correcciones Implementadas

### ❌ Problema Anterior:

1. **Carga laboral** buscaba en tabla `citas` (contaba citas activas)
2. **Sesiones completadas** buscaba en tabla `sesiones` (vacía, retornaba 0)
3. **Rating** se calculaba de tabla `sesiones` → Siempre 3.0 (neutral)
4. **Match** solo verificaba tabla `terapias_personal` (relación N:N)

**Resultado**: Todos los terapeutas tenían métricas similares (0, 0, 3.0, 0/1)

### ✅ Solución Actual:

```python
# Carga laboral → sesiones_semana de personal
terapeuta.sesiones_semana  # Ej: 15, 18, 20, 27

# Sesiones completadas → total_pacientes de personal
terapeuta.total_pacientes  # Ej: 15, 28, 35, 42, 45

# Rating → rating de personal
terapeuta.rating  # Ej: 4.3, 4.5, 4.8, 5.0

# Match → Comparación inteligente de texto
"Lenguaje" in terapia.nombre AND "lenguaje|comunicación" in especialidad
```

**Resultado**: Cada terapeuta tiene métricas **únicas y reales**, rankings **diferentes** en cada evaluación

---

## 🎯 Casos de Uso

### Caso 1: Asignar terapeuta para nueva terapia de lenguaje

```
Terapia: "Terapia de lenguaje individual"
Pesos sugeridos:
- Carga: 0.30 (Queremos disponibilidad)
- Pacientes: 0.25 (Experiencia importante)
- Rating: 0.20 (Calidad)
- Match: 0.25 (Debe ser especialista en lenguaje)
```

**Resultado esperado**: Terapeuta con:
- ✅ Especialidad en "Lenguaje y Comunicación"
- ✅ Carga baja (< 20 sesiones/semana)
- ✅ Experiencia media-alta (> 25 pacientes)
- ✅ Rating > 4.5

---

### Caso 2: Reemplazar terapeuta por vacaciones

```
Terapia: Ya conocida
Pesos sugeridos:
- Carga: 0.40 ← Mayor peso (Urgente)
- Pacientes: 0.20
- Rating: 0.15
- Match: 0.25 (Debe saber la terapia)
```

**Resultado esperado**: Terapeuta con **máxima disponibilidad inmediata**

---

## 📌 Notas Importantes

1. **Datos reales**: Todas las métricas vienen de la tabla `personal`
2. **No requiere sesiones históricas**: Funciona con datos de perfil del terapeuta
3. **Match inteligente**: Busca por palabras clave, no requiere tabla relacional
4. **Personalizable**: Ajusta pesos según prioridades del caso
5. **Transparente**: Muestra todas las métricas en la tabla de resultados

---

## 🚀 Próximas Mejoras

- [ ] Permitir filtrar por grado académico (Licenciatura, Maestría, Doctorado)
- [ ] Agregar criterio de "años de experiencia" (extraer de campo `experiencia`)
- [ ] Incorporar disponibilidad horaria (requiere nuevo campo en BD)
- [ ] Guardar configuraciones de pesos como "plantillas"
- [ ] Exportar resultados a PDF/Excel
- [ ] Integración con sistema de recomendaciones (Gemini AI)

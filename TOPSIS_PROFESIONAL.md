# 🎯 MÓDULO TOPSIS PROFESIONAL - DOCUMENTACIÓN COMPLETA

## 📋 Resumen de Implementación

Se ha completado la profesionalización del módulo TOPSIS de evaluación de terapeutas con **Clean Architecture**, **validación robusta** y **cálculos basados en datos reales de MySQL**.

---

## 🏗️ Arquitectura Implementada

### Backend: Clean Architecture en 3 Capas

```
backend/app/
├── schemas/topsis_terapeutas.py      # Capa de Validación (Pydantic)
├── services/topsis_terapeutas_service.py  # Capa de Lógica de Negocio
└── api/v1/endpoints/topsis_terapeutas.py  # Capa de Presentación (REST)
```

### Frontend: Angular 17+ con Best Practices

```
src/app/
├── interfaces/topsis-terapeutas.interface.ts  # Tipado TypeScript
├── service/topsis.service.ts                   # HTTP Client Service
└── coordinador/topsis-terapeutas/
    ├── topsis-terapeutas.ts                    # Componente con Signals
    ├── topsis-terapeutas.html                  # Template con @if/@for
    └── topsis-terapeutas.scss                  # Estilos profesionales
```

---

## 🔧 Componentes Backend

### 1. **Schemas (Pydantic Validation)**

**Archivo:** `backend/app/schemas/topsis_terapeutas.py`

#### Características:
- ✅ **PesosCriterios**: Validación de pesos (0-1, suma = 1.0 ±0.01)
- ✅ **@model_validator**: Validación automática de suma de pesos
- ✅ **TopsisEvaluacionRequest**: Request con filtros opcionales
- ✅ **MetricasTerapeuta**: Métricas calculadas de DB
- ✅ **TerapeutaRanking**: Resultado individual con score
- ✅ **TopsisResultado**: Response completo con ranking

#### Ejemplo de Request:
```python
{
  "terapia_id": 1,  # Opcional
  "pesos": {
    "carga_laboral": 0.30,
    "sesiones_completadas": 0.25,
    "rating": 0.30,
    "especialidad": 0.15
  },
  "incluir_inactivos": false
}
```

---

### 2. **Services (Business Logic)**

**Archivo:** `backend/app/services/topsis_terapeutas_service.py`

#### Clase 1: **TopsisCalculator** (Algoritmo Puro)
Implementa el algoritmo TOPSIS matemático puro:

```python
normalizar_matriz()          # Normalización vectorial
aplicar_pesos()              # Aplicación de ponderaciones
calcular_ideales()           # Soluciones ideales A+ y A-
calcular_distancias()        # Distancias euclidianas
calcular_scores()            # Coeficientes de proximidad (0-1)
```

#### Clase 2: **MetricasService** (Consultas DB)
Calcula métricas reales desde MySQL:

```python
obtener_carga_laboral()          # COUNT(citas WHERE terapeuta_id)
obtener_sesiones_completadas()   # COUNT(sesiones WHERE creado_por)
obtener_rating_promedio()        # AVG(valoraciones.puntuacion)
verifica_especialidad_match()    # EXISTS(terapias_personal)
```

**⚠️ CORRECCIÓN CRÍTICA IMPLEMENTADA:**
- ✅ `Cita.terapeuta_id` (NO `id_personal`)
- ✅ `Sesion.creado_por` para identificar terapeuta
- ✅ `Valoracion.evaluado_id` para rating del terapeuta

#### Clase 3: **TopsisEvaluacionService** (Orquestador)
Coordina el flujo completo:

```python
obtener_terapeutas_activos()     # Filtrar por EstadoLaboral.ACTIVO
calcular_metricas_terapeuta()    # Agregar 4 métricas por terapeuta
construir_matriz_decision()      # Crear matriz NumPy
evaluar_terapeutas()             # Workflow completo: DB → TOPSIS → Ranking
```

---

### 3. **Endpoints (REST API)**

**Archivo:** `backend/app/api/v1/endpoints/topsis_terapeutas.py`

#### Endpoint Principal: `POST /api/v1/topsis/terapeutas`

**Request Body:**
```json
{
  "terapia_id": 1,
  "pesos": {
    "carga_laboral": 0.30,
    "sesiones_completadas": 0.25,
    "rating": 0.30,
    "especialidad": 0.15
  },
  "incluir_inactivos": false
}
```

**Response (200 OK):**
```json
{
  "total_evaluados": 5,
  "terapia_solicitada": 1,
  "pesos_aplicados": { ... },
  "ranking": [
    {
      "terapeuta_id": 42,
      "nombre": "Dr. Juan Pérez",
      "especialidad_principal": "Lenguaje",
      "score": 0.856,
      "ranking": 1,
      "metricas": {
        "carga_laboral": 8,
        "sesiones_completadas": 45,
        "rating": 4.7,
        "especialidad_match": true
      }
    },
    ...
  ]
}
```

**Errores:**
- `400 Bad Request`: Pesos no suman 1.0 o validación fallida
- `500 Internal Server Error`: Error de servidor

#### Endpoint Helper: `GET /api/v1/topsis/terapeutas/pesos-default`

Retorna pesos por defecto y descripciones de criterios.

---

## 🎨 Componentes Frontend

### 1. **Interfaces TypeScript**

**Archivo:** `src/app/interfaces/topsis-terapeutas.interface.ts`

```typescript
export interface PesosCriterios {
  carga_laboral: number;
  sesiones_completadas: number;
  rating: number;
  especialidad: number;
}

export interface TopsisEvaluacionRequest { ... }
export interface TerapeutaRanking { ... }
export interface TopsisResultado { ... }
```

---

### 2. **Service Angular**

**Archivo:** `src/app/service/topsis.service.ts`

#### Métodos Profesionales:

```typescript
// Evaluación con pesos configurables
evaluarTerapeutasProfesional(request: TopsisEvaluacionRequest): Observable<TopsisResultado>

// Pesos por defecto
obtenerPesosDefault(): Observable<PesosDefault>
```

---

### 3. **Componente Angular**

**Archivo:** `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.ts`

#### Características Implementadas:

✅ **Configuración de Pesos:**
- Sliders interactivos para cada criterio (0-1)
- Validación en tiempo real de suma = 1.0
- Botón "Normalizar" para ajustar automáticamente

✅ **Filtros Opcionales:**
- ID de terapia específica (verifica especialidad)
- Incluir terapeutas inactivos

✅ **Validaciones:**
```typescript
validarPesos(): boolean        // Suma == 1.0 ±0.01
getSumaPesos(): number         // Suma actual
normalizarPesos(): void        // Ajuste proporcional
```

✅ **Estados de UI:**
- `cargando`: Spinner durante evaluación
- `mensajeError`: Alertas de error
- `mensajeInfo`: Mensajes informativos
- `mostrarConfiguracion`: Toggle config/resultados

---

### 4. **Template HTML**

**Archivo:** `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.html`

#### Secciones:

1. **Header Gradient:** Título y descripción
2. **Alertas:** Error, info, cargando
3. **Configuración:**
   - Filtros opcionales (terapia_id, incluir_inactivos)
   - 4 sliders para pesos con valores en tiempo real
   - Indicador de suma válida/inválida
   - Botones: "Normalizar Pesos" y "Calcular"
4. **Resultados:**
   - Resumen (total evaluados, terapia solicitada)
   - Tabla con ranking, nombre, especialidad, score, métricas
   - Badges dorado/plata/bronce para top 3
   - Progress bars por score
   - Pesos aplicados en grid

---

### 5. **Estilos SCSS**

**Archivo:** `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.scss`

#### Características:
- ✨ Gradientes modernos (purple-blue)
- 🎨 Paleta de colores profesional (Tailwind-inspired)
- 📱 Diseño responsivo (mobile-first)
- 🎭 Animaciones suaves (slideDown, fadeIn)
- 🏅 Badges especiales (gold, silver, bronze)
- 📊 Progress bars personalizados
- 🎯 Focus states accesibles

---

## 📊 Criterios TOPSIS Implementados

| Criterio | Tipo | Descripción | Peso Default |
|----------|------|-------------|--------------|
| **Carga Laboral** | Costo (menor mejor) | Número de citas activas (PROGRAMADA, EN_PROGRESO) | 0.30 |
| **Sesiones Completadas** | Beneficio (mayor mejor) | Total de sesiones finalizadas exitosamente | 0.25 |
| **Rating Promedio** | Beneficio (mayor mejor) | Valoración promedio (1-5, default 3.0) | 0.30 |
| **Especialidad Match** | Beneficio (mayor mejor) | Coincidencia con terapia solicitada (boolean) | 0.15 |

---

## 🔄 Flujo de Ejecución

### Backend Flow:
```
1. Recibir TopsisEvaluacionRequest
2. Validar pesos (suma = 1.0 ±0.01)
3. Obtener terapeutas activos de DB
4. Calcular métricas para cada terapeuta:
   - Carga laboral (COUNT citas)
   - Sesiones completadas (COUNT sesiones)
   - Rating promedio (AVG valoraciones)
   - Especialidad match (EXISTS terapias_personal)
5. Construir matriz de decisión NumPy
6. Aplicar algoritmo TOPSIS:
   - Normalizar matriz
   - Aplicar pesos
   - Calcular ideales A+ y A-
   - Calcular distancias euclidianas
   - Calcular scores (proximidad)
7. Ordenar por score descendente
8. Asignar rankings (1, 2, 3, ...)
9. Retornar TopsisResultado
```

### Frontend Flow:
```
1. ngOnInit: Cargar pesos default
2. Usuario ajusta pesos con sliders
3. Validación en tiempo real (suma = 1.0)
4. Usuario hace clic en "Calcular"
5. Enviar POST /api/v1/topsis/terapeutas
6. Mostrar spinner (cargando = true)
7. Recibir ranking de terapeutas
8. Mostrar resultados en tabla:
   - Badges por ranking
   - Progress bars por score
   - Métricas detalladas
9. Opción "Nueva Evaluación" para reiniciar
```

---

## ✅ Validaciones Implementadas

### Backend (Pydantic):
- ✅ Pesos entre 0 y 1 (`ge=0`, `le=1`)
- ✅ Suma de pesos = 1.0 ±0.01 (`@model_validator`)
- ✅ terapia_id opcional (`Optional[int]`)
- ✅ incluir_inactivos default False

### Frontend (TypeScript):
- ✅ Validación antes de enviar request
- ✅ Botón "Calcular" deshabilitado si suma != 1.0
- ✅ Indicador visual de suma válida/inválida
- ✅ Mensajes de error descriptivos

---

## 🐛 Correcciones Críticas Aplicadas

### Error Original:
```
AttributeError: type object 'Cita' has no attribute 'id_personal'
```

### Solución Implementada:
```python
# ❌ INCORRECTO (antes)
Cita.id_personal

# ✅ CORRECTO (ahora)
Cita.terapeuta_id           # Campo correcto en modelo Cita
Sesion.creado_por           # Campo para identificar terapeuta
Valoracion.evaluado_id      # Campo para rating del terapeuta
```

Todos los servicios y endpoints ahora usan los campos correctos:
- `MetricasService.obtener_carga_laboral()` → `Cita.terapeuta_id`
- `MetricasService.obtener_sesiones_completadas()` → `Sesion.creado_por`
- `MetricasService.obtener_rating_promedio()` → `Valoracion.evaluado_id`

---

## 📦 Archivos Creados/Modificados

### ✨ Nuevos Archivos:
1. `backend/app/schemas/topsis_terapeutas.py` (NEW)
2. `backend/app/services/topsis_terapeutas_service.py` (NEW)
3. `backend/app/api/v1/endpoints/topsis_terapeutas.py` (NEW)
4. `src/app/interfaces/topsis-terapeutas.interface.ts` (NEW)

### 🔧 Archivos Modificados:
1. `backend/app/api/v1/__init__.py` (router registration)
2. `src/app/service/topsis.service.ts` (nuevos métodos)
3. `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.ts` (reescrito)
4. `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.html` (rediseñado)
5. `src/app/coordinador/topsis-terapeutas/topsis-terapeutas.scss` (estilos profesionales)

---

## 🚀 Cómo Usar

### 1. Iniciar Backend:
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Iniciar Frontend:
```powershell
npm start
```

### 3. Acceder al Módulo:
```
http://localhost:4200/coordinador/topsis-terapeutas
```

### 4. Usar la Interfaz:

#### Paso 1: Configurar Pesos
- Ajusta los sliders de cada criterio según prioridades
- Verifica que la suma sea 1.0 (indicador verde)
- Usa "Normalizar" si la suma no es exacta

#### Paso 2: Filtros Opcionales
- **Terapia Específica**: Ingresa ID para verificar especialidad
- **Incluir Inactivos**: Marca checkbox para incluir terapeutas inactivos

#### Paso 3: Calcular
- Haz clic en "Calcular Evaluación TOPSIS"
- Espera el procesamiento (spinner)
- Revisa resultados en tabla

#### Paso 4: Interpretar Resultados
- **Ranking**: Posición en lista ordenada (1 = mejor)
- **Score**: Coeficiente de proximidad (0-1, mayor = mejor)
- **Métricas**: Datos reales de la base de datos
- **Badges**: Oro/Plata/Bronce para top 3

---

## 🧪 Testing

### Datos de Prueba:
Si no tienes terapeutas reales, inserta datos de prueba:

```sql
-- Archivo: backend/scripts/datos_ninos_topsis_recomendacion.sql
-- Contiene 10 niños realistas con perfiles completos
```

**Ejecutar:**
```powershell
# Usando MySQL Workbench (recomendado)
# O desde línea de comandos:
mysql -u root -p autismo_db < backend\scripts\datos_ninos_topsis_recomendacion.sql
```

### Casos de Prueba:

#### Test 1: Evaluar Todos los Terapeutas
- Pesos: Default (0.30, 0.25, 0.30, 0.15)
- Filtros: Ninguno
- Resultado: Lista completa de terapeutas activos

#### Test 2: Evaluar para Terapia Específica
- Pesos: Default
- Terapia ID: 1 (ej. Lenguaje)
- Resultado: Solo terapeutas con especialidad en Lenguaje tendrán especialidad_match = true

#### Test 3: Priorizar Disponibilidad
- Pesos: carga=0.60, sesiones=0.10, rating=0.20, especialidad=0.10
- Resultado: Terapeutas con menor carga laboral en top

#### Test 4: Priorizar Calidad
- Pesos: carga=0.10, sesiones=0.20, rating=0.60, especialidad=0.10
- Resultado: Terapeutas con mejor rating en top

---

## 📚 Referencias Técnicas

### Algoritmo TOPSIS:
- **Paper Original**: Hwang & Yoon (1981)
- **Normalización**: Vectorial (element / √Σ(elements²))
- **Distancias**: Euclidianas
- **Score**: C = D⁻ / (D⁺ + D⁻), donde 0 ≤ C ≤ 1

### Bibliotecas Utilizadas:
- **NumPy**: Operaciones matriciales
- **Pydantic**: Validación de datos
- **SQLAlchemy**: ORM para MySQL
- **FastAPI**: REST API framework
- **Angular 17+**: Frontend con Signals y Control Flow

---

## 🎯 Próximos Pasos Sugeridos

### Mejoras Futuras:

1. **Dashboard de Análisis:**
   - Gráficos de distribución de scores
   - Comparación de métricas entre terapeutas
   - Tendencias históricas

2. **Recomendaciones Automáticas:**
   - Sugerir terapeutas óptimos por niño
   - Machine Learning para ajustar pesos automáticamente

3. **Export de Resultados:**
   - PDF con ranking detallado
   - Excel con métricas completas

4. **Notificaciones:**
   - Alertar terapeutas con carga laboral alta
   - Notificar cuando un terapeuta suba en ranking

5. **Auditoría:**
   - Registrar evaluaciones TOPSIS en tabla de auditoría
   - Historial de configuraciones de pesos

---

## 🐛 Troubleshooting

### Error: "Los pesos deben sumar 1.0"
**Solución:** Haz clic en "Normalizar Pesos" para ajustar automáticamente.

### Error: "No se encontraron terapeutas"
**Causa:** No hay terapeutas activos o todos fueron filtrados.
**Solución:** 
- Verifica que existan registros en `personal` con `estado_laboral = 'ACTIVO'`
- Marca "Incluir inactivos" si necesario

### Error: "AttributeError: 'Cita' has no attribute..."
**Causa:** Usando código antiguo sin correcciones.
**Solución:** Verifica que estés usando:
- `backend/app/services/topsis_terapeutas_service.py` (NUEVO)
- `backend/app/api/v1/endpoints/topsis_terapeutas.py` (NUEVO)

### Spinner infinito al calcular
**Causa:** Backend no responde o hay error en endpoint.
**Solución:** 
- Revisa logs de FastAPI: `uvicorn app.main:app --reload`
- Verifica que el router esté registrado en `__init__.py`
- Comprueba la consola del navegador (F12)

---

## ✨ Resumen de Mejoras

### Antes:
- ❌ Error `id_personal` no existe
- ❌ Endpoints hardcodeados sin validación
- ❌ Datos ficticios en frontend
- ❌ Sin configuración de pesos
- ❌ Código acoplado sin arquitectura clara

### Después:
- ✅ Clean Architecture con separación de capas
- ✅ Validación robusta con Pydantic
- ✅ Cálculos con datos reales de MySQL
- ✅ Configuración flexible de pesos
- ✅ UI profesional con validaciones en tiempo real
- ✅ Documentación completa con OpenAPI
- ✅ Código mantenible y escalable
- ✅ Tipado completo (TypeScript + Python)
- ✅ Manejo de errores en todos los niveles

---

## 📧 Soporte

Para dudas o problemas, revisar:
1. Este documento (TOPSIS_PROFESIONAL.md)
2. Logs de backend: Terminal de `uvicorn`
3. Consola del navegador (F12 → Console/Network)
4. Documentación interactiva: `http://localhost:8000/docs`

---

**Versión:** 1.0.0  
**Fecha:** 2024  
**Autor:** Sistema de IA con Clean Architecture y Best Practices  
**Estado:** ✅ Producción Ready

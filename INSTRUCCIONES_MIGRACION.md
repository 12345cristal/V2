# INSTRUCCIONES PARA EJECUTAR MIGRACIONES
# ==========================================

## OPCIÓN 1: Usando MySQL Workbench o phpMyAdmin (RECOMENDADO)

1. Abre MySQL Workbench o phpMyAdmin
2. Conéctate a la base de datos `autismo_mochis_ia`
3. Ejecuta los siguientes scripts en orden:

### Script 1: migrar_estados_y_tipo_sangre.sql
```sql
-- Abrir archivo: backend/scripts/migrar_estados_y_tipo_sangre.sql
-- Copiar y pegar el contenido completo en MySQL Workbench
-- Ejecutar
```

### Script 2: crear_tabla_fichas_emergencia.sql
```sql
-- Abrir archivo: backend/scripts/crear_tabla_fichas_emergencia.sql
-- Copiar y pegar el contenido completo en MySQL Workbench
-- Ejecutar
```

## OPCIÓN 2: Usando Python (si tienes mysql-connector-python instalado)

1. Abre el archivo: `backend/scripts/ejecutar_migraciones.py`
2. Modifica la línea 23-27 con tus credenciales:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',  # Tu usuario de MySQL
       'password': 'TU_CONTRASEÑA_AQUI',  # Tu contraseña
       'database': 'autismo_mochis_ia'
   }
   ```
3. Ejecuta:
   ```bash
   cd backend/scripts
   python ejecutar_migraciones.py
   ```

## OPCIÓN 3: Ejecutar SQL manualmente

### Paso 1: Actualizar estados y agregar tipo_sangre
```sql
USE autismo_mochis_ia;

-- Agregar columna tipo_sangre
ALTER TABLE ninos 
ADD COLUMN IF NOT EXISTS tipo_sangre VARCHAR(10) NULL 
COMMENT 'Tipo de sangre: A+, B+, AB+, O+, A-, B-, AB-, O-'
AFTER curp;

-- Convertir BAJA_TEMPORAL a INACTIVO
UPDATE ninos 
SET estado = 'INACTIVO' 
WHERE estado = 'BAJA_TEMPORAL';

-- Modificar ENUM para eliminar BAJA_TEMPORAL
ALTER TABLE ninos 
MODIFY COLUMN estado ENUM('ACTIVO', 'INACTIVO') 
DEFAULT 'ACTIVO' 
NOT NULL;
```

### Paso 2: Crear tabla fichas_emergencia
```sql
USE autismo_mochis_ia;

CREATE TABLE IF NOT EXISTS fichas_emergencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nino_id INT NOT NULL UNIQUE,
    
    -- Información médica crítica
    tipo_sangre VARCHAR(10),
    alergias TEXT,
    condiciones_medicas TEXT,
    medicamentos_actuales TEXT,
    
    -- Información de diagnóstico
    diagnostico_principal VARCHAR(255),
    diagnostico_detallado TEXT,
    
    -- Contactos de emergencia
    contacto_principal_nombre VARCHAR(200) NOT NULL,
    contacto_principal_relacion VARCHAR(100),
    contacto_principal_telefono VARCHAR(20) NOT NULL,
    contacto_principal_telefono_alt VARCHAR(20),
    
    contacto_secundario_nombre VARCHAR(200),
    contacto_secundario_relacion VARCHAR(100),
    contacto_secundario_telefono VARCHAR(20),
    
    -- Información médica adicional
    seguro_medico VARCHAR(200),
    numero_seguro VARCHAR(100),
    hospital_preferido VARCHAR(255),
    medico_tratante VARCHAR(200),
    telefono_medico VARCHAR(20),
    
    -- Instrucciones especiales
    instrucciones_emergencia TEXT,
    restricciones_alimenticias TEXT,
    
    -- Información de comportamiento crítica
    crisis_comunes TEXT,
    como_calmar TEXT,
    trigger_points TEXT,
    
    -- Control
    activa BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    creado_por_id INT,
    
    FOREIGN KEY (nino_id) REFERENCES ninos(id) ON DELETE CASCADE,
    FOREIGN KEY (creado_por_id) REFERENCES usuarios(id),
    
    INDEX idx_nino_id (nino_id),
    INDEX idx_activa (activa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Crear fichas de emergencia para niños existentes
INSERT INTO fichas_emergencia (
    nino_id,
    tipo_sangre,
    diagnostico_principal,
    contacto_principal_nombre,
    contacto_principal_relacion,
    contacto_principal_telefono,
    activa
)
SELECT 
    n.id,
    n.tipo_sangre,
    nd.diagnostico_principal,
    COALESCE(t.nombre_completo, 'Sin especificar'),
    'Tutor',
    COALESCE(t.telefono, 'Sin teléfono'),
    TRUE
FROM ninos n
LEFT JOIN ninos_diagnostico nd ON n.id = nd.nino_id
LEFT JOIN tutores t ON n.tutor_id = t.id
WHERE NOT EXISTS (
    SELECT 1 FROM fichas_emergencia fe WHERE fe.nino_id = n.id
);
```

## Verificación
Después de ejecutar ambos scripts, verifica:
```sql
-- Verificar estados
SELECT estado, COUNT(*) as total 
FROM ninos 
GROUP BY estado;

-- Verificar fichas de emergencia
SELECT COUNT(*) as total_fichas FROM fichas_emergencia;

-- Ver estructura de fichas
DESCRIBE fichas_emergencia;
```

## Notas Importantes
- ✅ Los scripts son seguros y NO borran datos
- ✅ BAJA_TEMPORAL se convierte automáticamente a INACTIVO
- ✅ Se crean fichas de emergencia para todos los niños existentes
- ✅ El campo tipo_sangre se agrega sin afectar datos existentes

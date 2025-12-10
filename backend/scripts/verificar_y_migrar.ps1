# Script de verificacion y migracion automatica
# Ejecutar desde: backend/scripts/

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICACION DE MIGRACIONES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuracion de la base de datos
$DB_HOST = "localhost"
$DB_USER = "root"
$DB_PASS = ""  # Actualiza si tienes contrasena
$DB_NAME = "autismo_mochis_ia"

# Verificar si MySQL esta instalado
$mysqlCmd = Get-Command mysql -ErrorAction SilentlyContinue
if (-not $mysqlCmd) {
    Write-Host "ERROR: MySQL no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Yellow
    Write-Host "1. Instalar MySQL: https://dev.mysql.com/downloads/installer/" -ForegroundColor Yellow
    Write-Host "2. Usar XAMPP/WAMP y agregar MySQL al PATH" -ForegroundColor Yellow
    Write-Host "3. Ejecutar las migraciones manualmente desde phpMyAdmin" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK: MySQL encontrado" -ForegroundColor Green

# Verificar si la base de datos existe
Write-Host "Verificando base de datos..." -ForegroundColor Cyan
$checkDB = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DB_NAME';"
$result = & mysql -u $DB_USER -h $DB_HOST -e $checkDB 2>$null

if (-not $result -or $result -notmatch $DB_NAME) {
    Write-Host "ERROR: Base de datos '$DB_NAME' no encontrada" -ForegroundColor Red
    Write-Host "Por favor, crea la base de datos primero." -ForegroundColor Yellow
    exit 1
}

Write-Host "OK: Base de datos encontrada" -ForegroundColor Green

# Verificar si ya se migro el estado
Write-Host "Verificando estado de la columna 'estado'..." -ForegroundColor Cyan
$checkEstado = "SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = 'ninos' AND COLUMN_NAME = 'estado';"
$estadoType = & mysql -u $DB_USER -h $DB_HOST -e $checkEstado -s -N 2>$null

if ($estadoType -match "BAJA_TEMPORAL") {
    Write-Host "ATENCION: La columna 'estado' todavia contiene BAJA_TEMPORAL" -ForegroundColor Yellow
    Write-Host "Ejecutando migracion de estados..." -ForegroundColor Cyan
    
    $migracionEstados = Join-Path $PSScriptRoot "migrar_estados_y_tipo_sangre.sql"
    if (Test-Path $migracionEstados) {
        Get-Content $migracionEstados | & mysql -u $DB_USER -h $DB_HOST $DB_NAME
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Migracion de estados completada" -ForegroundColor Green
        } else {
            Write-Host "ERROR al ejecutar migracion de estados" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "ERROR: Archivo de migracion no encontrado: $migracionEstados" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "OK: La columna 'estado' ya esta actualizada (ACTIVO, INACTIVO)" -ForegroundColor Green
}

# Verificar si existe la tabla fichas_emergencia
Write-Host "Verificando tabla 'fichas_emergencia'..." -ForegroundColor Cyan
$checkTable = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = 'fichas_emergencia';"
$tableExists = & mysql -u $DB_USER -h $DB_HOST -e $checkTable -s -N 2>$null

if ($tableExists -eq "0") {
    Write-Host "ATENCION: Tabla 'fichas_emergencia' no existe" -ForegroundColor Yellow
    Write-Host "Creando tabla fichas_emergencia..." -ForegroundColor Cyan
    
    $crearTablaFichas = Join-Path $PSScriptRoot "crear_tabla_fichas_emergencia.sql"
    if (Test-Path $crearTablaFichas) {
        Get-Content $crearTablaFichas | & mysql -u $DB_USER -h $DB_HOST $DB_NAME
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Tabla fichas_emergencia creada" -ForegroundColor Green
        } else {
            Write-Host "ERROR al crear tabla fichas_emergencia" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "ERROR: Archivo SQL no encontrado: $crearTablaFichas" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "OK: Tabla 'fichas_emergencia' ya existe" -ForegroundColor Green
}

# Verificar si existe la columna tipo_sangre
Write-Host "Verificando columna 'tipo_sangre'..." -ForegroundColor Cyan
$checkTipoSangre = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = 'ninos' AND COLUMN_NAME = 'tipo_sangre';"
$tipoSangreExists = & mysql -u $DB_USER -h $DB_HOST -e $checkTipoSangre -s -N 2>$null

if ($tipoSangreExists -eq "1") {
    Write-Host "OK: Columna 'tipo_sangre' ya existe" -ForegroundColor Green
} else {
    Write-Host "ATENCION: Columna 'tipo_sangre' no encontrada" -ForegroundColor Yellow
}

# Mostrar resumen
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  RESUMEN DE ESTADISTICAS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$queryTotal = "SELECT COUNT(*) FROM ninos;"
$queryActivos = "SELECT COUNT(*) FROM ninos WHERE estado = 'ACTIVO';"
$queryInactivos = "SELECT COUNT(*) FROM ninos WHERE estado = 'INACTIVO';"
$queryFichas = "SELECT COUNT(*) FROM fichas_emergencia;"

$total = & mysql -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e $queryTotal
$activos = & mysql -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e $queryActivos
$inactivos = & mysql -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e $queryInactivos
$fichas = & mysql -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e $queryFichas

Write-Host "Total de ninos: $total"
Write-Host "Ninos activos: $activos" -ForegroundColor Green
Write-Host "Ninos inactivos: $inactivos" -ForegroundColor Yellow
Write-Host "Fichas de emergencia: $fichas" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  MIGRACIONES COMPLETADAS" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora puedes:" -ForegroundColor Cyan
Write-Host "1. Iniciar el backend: cd backend; python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host "2. Iniciar el frontend: ng serve" -ForegroundColor Yellow
Write-Host "3. Probar el filtro de ninos activos en el navegador" -ForegroundColor Yellow
Write-Host ""

# Script de verificacion usando XAMPP MySQL
# Ejecutar desde: backend/scripts/

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  VERIFICACION DE MIGRACIONES (XAMPP)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Configuracion
$MYSQL_PATH = "C:\xampp\mysql\bin\mysql.exe"
$DB_HOST = "localhost"
$DB_USER = "root"
$DB_PASS = ""
$DB_NAME = "autismo_mochis_ia"

# Verificar MySQL
if (-not (Test-Path $MYSQL_PATH)) {
    Write-Host "ERROR: MySQL no encontrado en $MYSQL_PATH" -ForegroundColor Red
    exit 1
}

Write-Host "OK: MySQL encontrado en XAMPP" -ForegroundColor Green

# Verificar BD
Write-Host "Verificando base de datos..." -ForegroundColor Cyan
$checkDB = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DB_NAME';"
$result = & $MYSQL_PATH -u $DB_USER -h $DB_HOST -e $checkDB 2>$null

if (-not $result -or $result -notmatch $DB_NAME) {
    Write-Host "ERROR: Base de datos '$DB_NAME' no encontrada" -ForegroundColor Red
    Write-Host "Creala primero en phpMyAdmin" -ForegroundColor Yellow
    exit 1
}

Write-Host "OK: Base de datos encontrada" -ForegroundColor Green

# Verificar estado
Write-Host "Verificando columna 'estado'..." -ForegroundColor Cyan
$checkEstado = "SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = 'ninos' AND COLUMN_NAME = 'estado';"
$estadoType = & $MYSQL_PATH -u $DB_USER -h $DB_HOST -e $checkEstado -s -N 2>$null

if ($estadoType -match "BAJA_TEMPORAL") {
    Write-Host "ATENCION: Migrando estados (BAJA_TEMPORAL -> INACTIVO)..." -ForegroundColor Yellow
    
    $migracionEstados = Join-Path $PSScriptRoot "migrar_estados_y_tipo_sangre.sql"
    if (Test-Path $migracionEstados) {
        Get-Content $migracionEstados | & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Migracion de estados completada" -ForegroundColor Green
        } else {
            Write-Host "ERROR al migrar estados" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "OK: Estados actualizados (solo ACTIVO/INACTIVO)" -ForegroundColor Green
}

# Verificar tabla fichas_emergencia
Write-Host "Verificando tabla 'fichas_emergencia'..." -ForegroundColor Cyan
$checkTable = "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '$DB_NAME' AND TABLE_NAME = 'fichas_emergencia';"
$tableExists = & $MYSQL_PATH -u $DB_USER -h $DB_HOST -e $checkTable -s -N 2>$null

if ($tableExists -eq "0") {
    Write-Host "ATENCION: Creando tabla fichas_emergencia..." -ForegroundColor Yellow
    
    $crearTablaFichas = Join-Path $PSScriptRoot "crear_tabla_fichas_emergencia.sql"
    if (Test-Path $crearTablaFichas) {
        Get-Content $crearTablaFichas | & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK: Tabla fichas_emergencia creada" -ForegroundColor Green
        } else {
            Write-Host "ERROR al crear tabla" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "OK: Tabla fichas_emergencia existe" -ForegroundColor Green
}

# Estadisticas
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ESTADISTICAS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$total = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM ninos;"
$activos = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM ninos WHERE estado = 'ACTIVO';"
$inactivos = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM ninos WHERE estado = 'INACTIVO';"
$fichas = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM fichas_emergencia;"

Write-Host "Total de ninos: $total"
Write-Host "Activos: $activos" -ForegroundColor Green
Write-Host "Inactivos: $inactivos" -ForegroundColor Yellow
Write-Host "Fichas de emergencia: $fichas" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  LISTO PARA USAR" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Siguiente paso:" -ForegroundColor Cyan
Write-Host "1. Iniciar backend: cd backend; python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host "2. Iniciar frontend: ng serve" -ForegroundColor Yellow
Write-Host "3. Probar filtro de activos en el navegador" -ForegroundColor Yellow
Write-Host ""

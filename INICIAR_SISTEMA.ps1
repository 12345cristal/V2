# Script para inicializar el sistema completo
# Crea la BD si no existe, ejecuta migraciones, e inicia backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIALIZACION DEL SISTEMA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$MYSQL_PATH = "C:\xampp\mysql\bin\mysql.exe"
$DB_HOST = "localhost"
$DB_USER = "root"
$DB_PASS = ""
$DB_NAME = "autismo_mochis_ia"

# 1. Verificar MySQL
Write-Host "1. Verificando MySQL..." -ForegroundColor Cyan
if (-not (Test-Path $MYSQL_PATH)) {
    Write-Host "ERROR: MySQL no encontrado. Inicia XAMPP primero" -ForegroundColor Red
    exit 1
}

$mysqlProcess = Get-Process -Name "mysqld" -ErrorAction SilentlyContinue
if (-not $mysqlProcess) {
    Write-Host "ERROR: MySQL no esta corriendo" -ForegroundColor Red
    Write-Host "Por favor:" -ForegroundColor Yellow
    Write-Host "1. Abre XAMPP Control Panel" -ForegroundColor Yellow
    Write-Host "2. Click en 'Start' para MySQL" -ForegroundColor Yellow
    Write-Host "3. Ejecuta este script nuevamente" -ForegroundColor Yellow
    exit 1
}

Write-Host "   OK: MySQL corriendo" -ForegroundColor Green

# 2. Crear base de datos si no existe
Write-Host "2. Verificando base de datos..." -ForegroundColor Cyan
$checkDB = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '$DB_NAME';"
$result = & $MYSQL_PATH -u $DB_USER -h $DB_HOST -e $checkDB 2>$null

if (-not $result -or $result -notmatch $DB_NAME) {
    Write-Host "   Base de datos no existe. Creando..." -ForegroundColor Yellow
    $createDB = "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
    & $MYSQL_PATH -u $DB_USER -h $DB_HOST -e $createDB
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK: Base de datos creada" -ForegroundColor Green
    } else {
        Write-Host "   ERROR: No se pudo crear la BD" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   OK: Base de datos existe" -ForegroundColor Green
}

# 3. Ejecutar migraciones
Write-Host "3. Ejecutando migraciones..." -ForegroundColor Cyan

# Migración de estados
$migracionEstados = Join-Path $PSScriptRoot "backend\scripts\migrar_estados_y_tipo_sangre.sql"
if (Test-Path $migracionEstados) {
    Write-Host "   Migrando estados y tipo_sangre..." -ForegroundColor Yellow
    Get-Content $migracionEstados | & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME 2>$null
    Write-Host "   OK: Estados migrados" -ForegroundColor Green
}

# Crear tabla fichas_emergencia
$crearFichas = Join-Path $PSScriptRoot "backend\scripts\crear_tabla_fichas_emergencia.sql"
if (Test-Path $crearFichas) {
    Write-Host "   Creando tabla fichas_emergencia..." -ForegroundColor Yellow
    Get-Content $crearFichas | & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME 2>$null
    Write-Host "   OK: Tabla creada" -ForegroundColor Green
}

# Crear tablas base del sistema (usuarios, roles, ninos, etc)
$crearTablas = Join-Path $PSScriptRoot "backend\scripts\crear_tablas_personal.py"
if (Test-Path $crearTablas) {
    Write-Host "   Creando tablas base del sistema..." -ForegroundColor Yellow
    cd backend
    python scripts\crear_tablas_personal.py 2>$null
    cd ..
    Write-Host "   OK: Tablas base creadas" -ForegroundColor Green
}

# Poblar datos iniciales
Write-Host "4. Poblando datos iniciales..." -ForegroundColor Cyan
$poblarSistema = Join-Path $PSScriptRoot "backend\scripts\poblar_sistema_completo.py"
if (Test-Path $poblarSistema) {
    Write-Host "   Insertando datos de ejemplo..." -ForegroundColor Yellow
    cd backend
    python scripts\poblar_sistema_completo.py 2>$null
    cd ..
    Write-Host "   OK: Datos insertados" -ForegroundColor Green
}

# 5. Mostrar estadísticas
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ESTADISTICAS DEL SISTEMA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$total = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM ninos;" 2>$null
$activos = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM ninos WHERE estado = 'ACTIVO';" 2>$null
$usuarios = & $MYSQL_PATH -u $DB_USER -h $DB_HOST $DB_NAME -s -N -e "SELECT COUNT(*) FROM usuarios;" 2>$null

if ($total) {
    Write-Host "Total de ninos: $total" -ForegroundColor White
    Write-Host "Ninos activos: $activos" -ForegroundColor Green
    Write-Host "Usuarios: $usuarios" -ForegroundColor Cyan
} else {
    Write-Host "Sistema inicializado (sin datos aun)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SISTEMA LISTO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ahora ejecuta en terminales separadas:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Terminal 1 - Backend:" -ForegroundColor Yellow
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 - Frontend:" -ForegroundColor Yellow
Write-Host "  ng serve" -ForegroundColor White
Write-Host ""
Write-Host "Luego abre: http://localhost:4200" -ForegroundColor Cyan
Write-Host ""

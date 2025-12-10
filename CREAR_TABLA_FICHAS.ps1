# Script para crear tabla fichas_emergencia en MySQL
# Ejecutar este script en PowerShell

Write-Host "================================" -ForegroundColor Cyan
Write-Host "CREAR TABLA FICHAS_EMERGENCIA" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Ruta del script SQL
$SCRIPT_SQL = "C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend\scripts\crear_tabla_fichas_emergencia.sql"

# Verificar que existe el archivo
if (-Not (Test-Path $SCRIPT_SQL)) {
    Write-Host "ERROR: No se encuentra el archivo $SCRIPT_SQL" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "Archivo SQL encontrado: $SCRIPT_SQL" -ForegroundColor Green
Write-Host ""

# Leer el contenido del SQL
$contenidoSQL = Get-Content $SCRIPT_SQL -Raw

# Ejecutar el SQL
Write-Host "Ejecutando SQL en MySQL..." -ForegroundColor Yellow

# Ejecutar directamente
$contenidoSQL | & "C:\xampp\mysql\bin\mysql.exe" -u root autismo_mochis_ia

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Tabla fichas_emergencia creada exitosamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Puedes verificar en phpMyAdmin: http://localhost/phpmyadmin" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "ERROR al ejecutar SQL (codigo: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUCION MANUAL:" -ForegroundColor Yellow
    Write-Host "1. Abre phpMyAdmin: http://localhost/phpmyadmin" -ForegroundColor White
    Write-Host "2. Selecciona la base de datos: autismo_mochis_ia" -ForegroundColor White
    Write-Host "3. Ve a la pestania SQL" -ForegroundColor White
    Write-Host "4. Copia y pega el contenido del archivo:" -ForegroundColor White
    Write-Host "   $SCRIPT_SQL" -ForegroundColor Cyan
    Write-Host "5. Haz clic en Continuar" -ForegroundColor White
}

Write-Host ""
pause

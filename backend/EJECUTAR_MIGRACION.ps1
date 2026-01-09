# ==========================================
# SCRIPT: Ejecutar migración Google Calendar
# Fecha: 9 de enero de 2026
# ==========================================

Write-Host "`n===========================================================" -ForegroundColor Cyan
Write-Host "🔧 MIGRACIÓN: Agregar columnas Google Calendar a tabla citas" -ForegroundColor Cyan
Write-Host "===========================================================" -ForegroundColor Cyan

# Variables de conexión MySQL (AJUSTAR según tu configuración)
$MYSQL_USER = "root"
$MYSQL_HOST = "localhost"
$MYSQL_PORT = "3306"
$MYSQL_DB = "autismo"
$SQL_FILE = "MIGRACION_GOOGLE_CALENDAR.sql"

# Verificar que el archivo SQL existe
if (-Not (Test-Path $SQL_FILE)) {
    Write-Host "`n❌ ERROR: No se encuentra $SQL_FILE" -ForegroundColor Red
    exit 1
}

Write-Host "`n📋 Configuración:" -ForegroundColor Yellow
Write-Host "   Usuario MySQL: $MYSQL_USER" -ForegroundColor Gray
Write-Host "   Host: $MYSQL_HOST" -ForegroundColor Gray
Write-Host "   Puerto: $MYSQL_PORT" -ForegroundColor Gray
Write-Host "   Base de datos: $MYSQL_DB" -ForegroundColor Gray
Write-Host "   Archivo SQL: $SQL_FILE" -ForegroundColor Gray

Write-Host "`n⚠️  ADVERTENCIA:" -ForegroundColor Yellow
Write-Host "   Esta migración agregará 4 columnas nuevas a la tabla 'citas'" -ForegroundColor Yellow
Write-Host "   Los datos existentes NO se perderán" -ForegroundColor Yellow

$confirmacion = Read-Host "`n¿Deseas continuar? (S/N)"

if ($confirmacion -ne "S" -and $confirmacion -ne "s") {
    Write-Host "`n❌ Migración cancelada por el usuario" -ForegroundColor Red
    exit 0
}

Write-Host "`n🚀 Ejecutando migración..." -ForegroundColor Cyan

# Ejecutar migración
try {
    # Opción 1: Si mysql.exe está en PATH
    $mysqlCmd = "mysql -u $MYSQL_USER -p -h $MYSQL_HOST -P $MYSQL_PORT $MYSQL_DB"
    
    Write-Host "`n💡 Comando a ejecutar:" -ForegroundColor Gray
    Write-Host "   $mysqlCmd < $SQL_FILE" -ForegroundColor Gray
    Write-Host "`n🔑 Ingresa tu contraseña de MySQL cuando se solicite:" -ForegroundColor Yellow
    
    Get-Content $SQL_FILE | & mysql -u $MYSQL_USER -p -h $MYSQL_HOST -P $MYSQL_PORT $MYSQL_DB
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ ¡MIGRACIÓN EJECUTADA EXITOSAMENTE!" -ForegroundColor Green
        
        Write-Host "`n📊 Verificando cambios..." -ForegroundColor Cyan
        Start-Sleep -Seconds 2
        
        # Ejecutar validación
        if (Test-Path "validar_migracion.py") {
            Write-Host "`n🧪 Ejecutando script de validación..." -ForegroundColor Cyan
            python validar_migracion.py
        } else {
            Write-Host "`n⚠️  Script de validación no encontrado (validar_migracion.py)" -ForegroundColor Yellow
        }
        
        Write-Host "`n===========================================================" -ForegroundColor Green
        Write-Host "✅ PROCESO COMPLETADO" -ForegroundColor Green
        Write-Host "===========================================================" -ForegroundColor Green
        
        Write-Host "`n📌 Próximos pasos:" -ForegroundColor Cyan
        Write-Host "   1. Reiniciar el backend:" -ForegroundColor Gray
        Write-Host "      cd backend" -ForegroundColor Gray
        Write-Host "      python run_server.py" -ForegroundColor Gray
        Write-Host "`n   2. Probar endpoints:" -ForegroundColor Gray
        Write-Host "      GET http://localhost:8000/api/v1/coordinador/dashboard" -ForegroundColor Gray
        Write-Host "      GET http://localhost:8000/api/v1/citas" -ForegroundColor Gray
        Write-Host "      GET http://localhost:8000/api/v1/estados-cita" -ForegroundColor Gray
        Write-Host ""
        
    } else {
        throw "Error al ejecutar migración"
    }
    
} catch {
    Write-Host "`n❌ ERROR al ejecutar migración:" -ForegroundColor Red
    Write-Host "   $_" -ForegroundColor Red
    
    Write-Host "`n💡 Alternativa manual:" -ForegroundColor Yellow
    Write-Host "   1. Abre MySQL Workbench o phpMyAdmin" -ForegroundColor Gray
    Write-Host "   2. Conecta a la base de datos '$MYSQL_DB'" -ForegroundColor Gray
    Write-Host "   3. Abre y ejecuta el archivo: $SQL_FILE" -ForegroundColor Gray
    Write-Host ""
    
    exit 1
}

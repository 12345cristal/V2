# Ejecutar migraciones SQL para actualizar base de datos
# PowerShell script

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "MIGRACIONES DE BASE DE DATOS" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Configuración
$DB_NAME = "autismo_mochis_ia"
$DB_USER = "root"
$DB_PASSWORD = ""  # Dejar vacío si no tiene contraseña

# Rutas de scripts
$SCRIPT_PATH = Split-Path -Parent $MyInvocation.MyCommand.Path
$MIGRATION1 = Join-Path $SCRIPT_PATH "migrar_estados_y_tipo_sangre.sql"
$MIGRATION2 = Join-Path $SCRIPT_PATH "crear_tabla_fichas_emergencia.sql"

Write-Host "📁 Directorio de scripts: $SCRIPT_PATH" -ForegroundColor Yellow
Write-Host ""

# Función para ejecutar SQL
function Invoke-SqlScript {
    param(
        [string]$ScriptPath,
        [string]$Description
    )
    
    Write-Host "🔧 $Description..." -ForegroundColor Green
    Write-Host "   Archivo: $(Split-Path -Leaf $ScriptPath)" -ForegroundColor Gray
    
    if (-not (Test-Path $ScriptPath)) {
        Write-Host "   ❌ ERROR: Archivo no encontrado" -ForegroundColor Red
        return $false
    }
    
    # Leer contenido del archivo
    $sqlContent = Get-Content $ScriptPath -Raw -Encoding UTF8
    
    # Ejecutar usando Python y MySQLdb o pymysql
    $pythonScript = @"
import mysql.connector
import sys

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='$DB_USER',
        password='$DB_PASSWORD',
        database='$DB_NAME'
    )
    cursor = conn.cursor()
    
    # Ejecutar script SQL
    sql_content = '''$sqlContent'''
    
    # Dividir por punto y coma y ejecutar cada statement
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    for statement in statements:
        if statement:
            cursor.execute(statement)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print('   ✅ Completado exitosamente')
    sys.exit(0)
    
except Exception as e:
    print(f'   ❌ ERROR: {str(e)}')
    sys.exit(1)
"@
    
    # Guardar script temporal
    $tempPyScript = Join-Path $env:TEMP "execute_sql.py"
    Set-Content -Path $tempPyScript -Value $pythonScript -Encoding UTF8
    
    # Ejecutar
    python $tempPyScript
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        return $true
    } else {
        Write-Host ""
        return $false
    }
}

# Ejecutar migraciones
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PASO 1: Migrar estados y tipo de sangre" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$result1 = Invoke-SqlScript -ScriptPath $MIGRATION1 -Description "Eliminando BAJA_TEMPORAL y agregando tipo_sangre"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PASO 2: Crear tabla fichas_emergencia" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$result2 = Invoke-SqlScript -ScriptPath $MIGRATION2 -Description "Creando tabla fichas_emergencia"

# Resumen
Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "RESUMEN DE MIGRACIONES" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Paso 1 (Estados): $(if ($result1) {'✅ OK'} else {'❌ FALLO'})" -ForegroundColor $(if ($result1) {'Green'} else {'Red'})
Write-Host "Paso 2 (Fichas):  $(if ($result2) {'✅ OK'} else {'❌ FALLO'})" -ForegroundColor $(if ($result2) {'Green'} else {'Red'})
Write-Host ""

if ($result1 -and $result2) {
    Write-Host "✅ Todas las migraciones completadas exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Algunas migraciones fallaron. Revise los errores arriba." -ForegroundColor Red
}

Write-Host ""
Write-Host "Presione cualquier tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

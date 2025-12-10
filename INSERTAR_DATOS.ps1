# ============================================================
# SCRIPT PARA INSERTAR DATOS DE PRUEBA EN LA BASE DE DATOS
# ============================================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  INSERTAR DATOS DE PRUEBA" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Ruta al archivo SQL
$sqlFile = "backend\scripts\datos_ninos_topsis_recomendacion.sql"

if (-not (Test-Path $sqlFile)) {
    Write-Host "ERROR: No se encontro el archivo SQL en:" -ForegroundColor Red
    Write-Host "   $sqlFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Archivo SQL encontrado" -ForegroundColor Green
Write-Host ""

# Solicitar credenciales de MySQL
Write-Host "Ingresa las credenciales de MySQL:" -ForegroundColor Yellow
$usuario = Read-Host "   Usuario (por defecto: root)"
if ([string]::IsNullOrWhiteSpace($usuario)) {
    $usuario = "root"
}

$contrasena = Read-Host "   Contraseña" -AsSecureString
$contrasenaPlainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($contrasena))

$baseDatos = Read-Host "   Base de datos (por defecto: autismo_mochis_ia)"
if ([string]::IsNullOrWhiteSpace($baseDatos)) {
    $baseDatos = "autismo_mochis_ia"
}

Write-Host ""
Write-Host "Insertando datos..." -ForegroundColor Cyan

# Ejecutar MySQL
Get-Content $sqlFile | & mysql -u $usuario "-p$contrasenaPlainText" $baseDatos

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "DATOS INSERTADOS EXITOSAMENTE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Datos insertados:" -ForegroundColor Cyan
    Write-Host "   - 10 ninos con perfiles completos" -ForegroundColor White
    Write-Host "   - Datos para TOPSIS (diagnosticos, niveles de TEA)" -ForegroundColor White
    Write-Host "   - Datos para recomendaciones (perfiles de contenido)" -ForegroundColor White
    Write-Host ""
    Write-Host "Ahora puedes usar:" -ForegroundColor Cyan
    Write-Host "   - /coordinador/prioridad-ninos" -ForegroundColor White
    Write-Host "   - /coordinador/recomendacion-nino" -ForegroundColor White
    Write-Host "   - /coordinador/topsis-terapeutas" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "ERROR al insertar datos. Codigo de salida: $LASTEXITCODE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifica que:" -ForegroundColor Yellow
    Write-Host "   1. MySQL este corriendo" -ForegroundColor White
    Write-Host "   2. Las credenciales sean correctas" -ForegroundColor White
    Write-Host "   3. La base de datos '$baseDatos' exista" -ForegroundColor White
}

Write-Host ""
Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

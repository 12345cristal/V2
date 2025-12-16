# ================================================================
# SCRIPT DE CONFIGURACIÓN RÁPIDA - GOOGLE CALENDAR
# Ejecutar desde: backend/
# ================================================================

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  CONFIGURACIÓN GOOGLE CALENDAR API  " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar entorno virtual
Write-Host "[1/6] Verificando entorno virtual..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "  ⚠️  No se encontró entorno virtual." -ForegroundColor Red
    Write-Host "  Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "  ✅ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "  Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# 2. Instalar dependencias
Write-Host ""
Write-Host "[2/6] Instalando dependencias de Google Calendar..." -ForegroundColor Yellow
pip install google-api-python-client==2.110.0
pip install google-auth==2.25.2
pip install google-auth-oauthlib==1.2.0
pip install google-auth-httplib2==0.2.0
Write-Host "  ✅ Dependencias instaladas" -ForegroundColor Green

# 3. Crear carpeta de credenciales
Write-Host ""
Write-Host "[3/6] Creando carpeta para credenciales..." -ForegroundColor Yellow
if (-not (Test-Path "credentials")) {
    New-Item -ItemType Directory -Path "credentials" | Out-Null
    Write-Host "  ✅ Carpeta 'credentials' creada" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Carpeta 'credentials' ya existe" -ForegroundColor Cyan
}

# 4. Crear .gitignore para credenciales
Write-Host ""
Write-Host "[4/6] Configurando .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# Google Calendar Credentials
credentials/*.json
!credentials/.gitkeep
"@

if (Test-Path "credentials/.gitignore") {
    Write-Host "  ℹ️  .gitignore ya existe" -ForegroundColor Cyan
} else {
    $gitignoreContent | Out-File -FilePath "credentials/.gitignore" -Encoding UTF8
    "" | Out-File -FilePath "credentials/.gitkeep" -Encoding UTF8
    Write-Host "  ✅ .gitignore creado (credenciales protegidas)" -ForegroundColor Green
}

# 5. Agregar variables de entorno
Write-Host ""
Write-Host "[5/6] Configurando variables de entorno..." -ForegroundColor Yellow
$envFile = ".env"
$envLines = @"

# === GOOGLE CALENDAR API ===
GOOGLE_CALENDAR_CREDENTIALS=credentials/google-calendar-service-account.json
GOOGLE_CALENDAR_ID=primary
"@

if (Test-Path $envFile) {
    $currentEnv = Get-Content $envFile -Raw
    if ($currentEnv -notmatch "GOOGLE_CALENDAR_CREDENTIALS") {
        Add-Content $envFile $envLines
        Write-Host "  ✅ Variables agregadas a .env" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Variables ya existen en .env" -ForegroundColor Cyan
    }
} else {
    $envLines | Out-File -FilePath $envFile -Encoding UTF8
    Write-Host "  ✅ Archivo .env creado" -ForegroundColor Green
}

# 6. Ejecutar migración SQL
Write-Host ""
Write-Host "[6/6] Migración de base de datos..." -ForegroundColor Yellow
Write-Host "  📋 Archivo SQL generado: scripts/migrar_citas_google_calendar.sql" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Para aplicar la migración:" -ForegroundColor Yellow
Write-Host "    1. Abre phpMyAdmin: http://localhost/phpmyadmin" -ForegroundColor White
Write-Host "    2. Selecciona la BD: autismo_mochis_ia" -ForegroundColor White
Write-Host "    3. Pestaña 'SQL'" -ForegroundColor White
Write-Host "    4. Pega el contenido de: scripts/migrar_citas_google_calendar.sql" -ForegroundColor White
Write-Host "    5. Ejecuta" -ForegroundColor White
Write-Host ""

# Resumen
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  ✅ CONFIGURACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 PRÓXIMOS PASOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. GOOGLE CLOUD CONSOLE:" -ForegroundColor Cyan
Write-Host "     a. Ir a: https://console.cloud.google.com" -ForegroundColor White
Write-Host "     b. Crear Service Account" -ForegroundColor White
Write-Host "     c. Habilitar Calendar API" -ForegroundColor White
Write-Host "     d. Descargar JSON de credenciales" -ForegroundColor White
Write-Host ""
Write-Host "  2. GUARDAR CREDENCIALES:" -ForegroundColor Cyan
Write-Host "     Mover el archivo JSON a:" -ForegroundColor White
Write-Host "     backend/credentials/google-calendar-service-account.json" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. COMPARTIR CALENDARIO:" -ForegroundColor Cyan
Write-Host "     En Google Calendar, compartir con el email del Service Account" -ForegroundColor White
Write-Host ""
Write-Host "  4. EJECUTAR MIGRACIÓN SQL:" -ForegroundColor Cyan
Write-Host "     Ver instrucciones arriba ↑" -ForegroundColor White
Write-Host ""
Write-Host "  5. REGISTRAR ENDPOINTS:" -ForegroundColor Cyan
Write-Host "     Agregar en backend/app/main.py:" -ForegroundColor White
Write-Host @"
     from app.api.v1.endpoints import citas_calendario
     
     app.include_router(
         citas_calendario.router,
         prefix=f"{settings.API_V1_PREFIX}/citas-calendario",
         tags=["Citas y Calendario"]
     )
"@ -ForegroundColor Yellow
Write-Host ""
Write-Host "  6. REINICIAR BACKEND:" -ForegroundColor Cyan
Write-Host "     uvicorn app.main:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "📚 DOCUMENTACIÓN COMPLETA:" -ForegroundColor Yellow
Write-Host "   Ver: SISTEMA_CITAS_GOOGLE_CALENDAR.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan

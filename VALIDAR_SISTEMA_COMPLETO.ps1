# =======================================================
# SCRIPT DE VALIDACIÓN COMPLETA
# Verifica que el backend esté funcionando correctamente
# después de todas las correcciones
# =======================================================

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "🧪 VALIDACIÓN COMPLETA: Backend + Migraciones + Endpoints" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

$errores = 0
$exitos = 0

# 1. Verificar que el backend esté corriendo
Write-Host "📡 [1/5] Verificando que el backend esté corriendo..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/ia/estado" -Method GET -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        if ($data.estado -eq "ok") {
            Write-Host "   ✅ Backend corriendo - Estado: $($data.estado)" -ForegroundColor Green
            $exitos++
        } else {
            Write-Host "   ❌ Backend responde pero estado incorrecto: $($data.estado)" -ForegroundColor Red
            $errores++
        }
    }
} catch {
    Write-Host "   ❌ Backend NO está corriendo en puerto 8000" -ForegroundColor Red
    Write-Host "      Ejecutar: cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Gray
    $errores++
}

# 2. Verificar endpoints públicos (catálogos)
Write-Host "`n📚 [2/5] Verificando endpoints públicos (sin autenticación)..." -ForegroundColor Yellow

$endpoints_publicos = @(
    @{ url = "http://localhost:8000/api/v1/estados-cita"; nombre = "Estados Cita" },
    @{ url = "http://localhost:8000/api/v1/especialidades"; nombre = "Especialidades" },
    @{ url = "http://localhost:8000/api/v1/roles"; nombre = "Roles" }
)

foreach ($ep in $endpoints_publicos) {
    try {
        $response = Invoke-WebRequest -Uri $ep.url -Method GET -UseBasicParsing -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            $items = ($response.Content | ConvertFrom-Json).Count
            Write-Host "   ✅ $($ep.nombre): $items items" -ForegroundColor Green
            $exitos++
        }
    } catch {
        Write-Host "   ❌ $($ep.nombre): Error $($_.Exception.Message)" -ForegroundColor Red
        $errores++
    }
}

# 3. Verificar base de datos (migración de columnas)
Write-Host "`n🗄️  [3/5] Verificando migración de base de datos..." -ForegroundColor Yellow
Push-Location backend
try {
    $validacion = python validar_migracion.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Todas las columnas de Google Calendar presentes" -ForegroundColor Green
        $exitos++
    } else {
        Write-Host "   ❌ Faltan columnas en la base de datos" -ForegroundColor Red
        Write-Host "      Ejecutar: python migracion_completa_citas.py" -ForegroundColor Gray
        $errores++
    }
} catch {
    Write-Host "   ⚠️  No se pudo ejecutar validación de BD" -ForegroundColor Yellow
}
Pop-Location

# 4. Verificar endpoint que requiere autenticación (debe dar 401)
Write-Host "`n🔐 [4/5] Verificando endpoints protegidos (autenticación)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/coordinador/dashboard" -Method GET -UseBasicParsing -TimeoutSec 5 -SkipHttpErrorCheck
    if ($response.StatusCode -eq 401) {
        Write-Host "   ✅ Coordinador Dashboard: 401 Unauthorized (correcto sin token)" -ForegroundColor Green
        $exitos++
    } elseif ($response.StatusCode -eq 200) {
        Write-Host "   ⚠️  Dashboard responde 200 sin token (problema de seguridad)" -ForegroundColor Yellow
        $errores++
    } else {
        Write-Host "   ❌ Dashboard: Status inesperado $($response.StatusCode)" -ForegroundColor Red
        $errores++
    }
} catch {
    Write-Host "   ❌ Error al verificar dashboard: $($_.Exception.Message)" -ForegroundColor Red
    $errores++
}

# 5. Verificar archivos frontend
Write-Host "`n🎨 [5/5] Verificando archivos frontend Angular..." -ForegroundColor Yellow

$archivos_frontend = @(
    "src/app/service/health-check.service.ts",
    "src/app/pages/login/login.ts",
    "src/app/pages/login/login.html",
    "src/app/coordinador/inicio/inicio.ts",
    "src/app/coordinador/inicio/inicio.html"
)

foreach ($archivo in $archivos_frontend) {
    if (Test-Path $archivo) {
        Write-Host "   ✅ $archivo" -ForegroundColor Green
        $exitos++
    } else {
        Write-Host "   ❌ $archivo NO EXISTE" -ForegroundColor Red
        $errores++
    }
}

# Resumen final
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "📊 RESUMEN DE VALIDACIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ✅ Exitos:  $exitos" -ForegroundColor Green
Write-Host "   ❌ Errores: $errores" -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($errores -eq 0) {
    Write-Host "🎉 ¡TODAS LAS VALIDACIONES PASARON!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📌 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "   1. Frontend: ng serve --port 4200" -ForegroundColor Gray
    Write-Host "   2. Abrir: http://localhost:4200/login" -ForegroundColor Gray
    Write-Host "   3. Verificar banner de estado del backend" -ForegroundColor Gray
    Write-Host "   4. Intentar login (debe funcionar sin ERR_CONNECTION_REFUSED)" -ForegroundColor Gray
    Write-Host ""
    exit 0
} else {
    Write-Host "⚠️  HAY ERRORES QUE CORREGIR" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📌 Acciones recomendadas:" -ForegroundColor Cyan
    Write-Host "   1. Backend: cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Gray
    Write-Host "   2. Migración BD: cd backend; python migracion_completa_citas.py" -ForegroundColor Gray
    Write-Host "   3. Re-ejecutar: .\VALIDAR_SISTEMA_COMPLETO.ps1" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

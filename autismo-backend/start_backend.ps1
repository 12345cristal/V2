# Script para iniciar el backend de Autismo Mochis IA
# Ejecutar con: .\start_backend.ps1

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "🚀 AUTISMO MOCHIS IA - BACKEND SERVER" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app\main.py")) {
    Write-Host "❌ Error: No se encuentra app\main.py" -ForegroundColor Red
    Write-Host "Por favor ejecuta este script desde el directorio autismo-backend`n" -ForegroundColor Yellow
    exit 1
}

# Verificar que existe .env
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Advertencia: No se encuentra archivo .env" -ForegroundColor Yellow
    Write-Host "Copia .env.example a .env y configura tus variables`n" -ForegroundColor Yellow
    
    $response = Read-Host "¿Deseas continuar de todos modos? (s/n)"
    if ($response -ne "s" -and $response -ne "S") {
        exit 0
    }
}

# Verificar Python
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion detectado`n" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Instala Python 3.12+ primero`n" -ForegroundColor Red
    exit 1
}

# Verificar uvicorn
Write-Host "📦 Verificando uvicorn..." -ForegroundColor Yellow
try {
    $uvicornCheck = pip show uvicorn 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ uvicorn instalado`n" -ForegroundColor Green
    } else {
        throw
    }
} catch {
    Write-Host "⚠️  uvicorn no encontrado" -ForegroundColor Yellow
    Write-Host "Instalando dependencias...`n" -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🌐 INICIANDO SERVIDOR FASTAPI" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

Write-Host "📍 API URL: http://localhost:8000" -ForegroundColor Green
Write-Host "📚 Documentación: http://localhost:8000/api/docs" -ForegroundColor Green
Write-Host "📖 ReDoc: http://localhost:8000/api/redoc`n" -ForegroundColor Green

Write-Host "💡 Presiona Ctrl+C para detener el servidor`n" -ForegroundColor Yellow

# Iniciar uvicorn con recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

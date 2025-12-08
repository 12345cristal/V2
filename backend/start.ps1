# ==================================================
# Script de inicio del backend - PowerShell
# ==================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend - Autismo Mochis IA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "[ERROR] No existe el entorno virtual 'venv'" -ForegroundColor Red
    Write-Host "[INFO] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[OK] Entorno virtual creado" -ForegroundColor Green
    Write-Host ""
}

# Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Instalar dependencias
Write-Host "[INFO] Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Iniciando servidor con Uvicorn..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Servidor corriendo en: http://localhost:8000" -ForegroundColor Green
Write-Host "Documentacion API: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

# Iniciar servidor
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

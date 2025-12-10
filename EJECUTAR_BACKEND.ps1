# Script para iniciar el backend
# Ejecuta este script desde una terminal SEPARADA de VS Code

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO BACKEND - AUTISMO MOCHIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navegar al directorio backend
Set-Location -Path "$PSScriptRoot\backend"

Write-Host "[INFO] Directorio actual: $PWD" -ForegroundColor Yellow
Write-Host "[INFO] Iniciando servidor en puerto 8000..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  NO CIERRES ESTA VENTANA" -ForegroundColor Green
Write-Host "  El backend debe estar corriendo" -ForegroundColor Green
Write-Host "  mientras uses el sistema" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Iniciar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

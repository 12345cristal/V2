# Script simple para iniciar el backend
Write-Host "Iniciando Backend..." -ForegroundColor Green
Write-Host "Backend corriendo en: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Documentacion: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend"

& ".\venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

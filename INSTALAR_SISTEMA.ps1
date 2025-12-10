# INSTALACIÓN Y ACTIVACIÓN DEL SISTEMA - Windows PowerShell
# Script automatizado para poner en marcha el sistema de recomendaciones

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SISTEMA DE RECOMENDACIONES INTELIGENTES" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1. Instalar dependencias Python
Write-Host "[1/4] Instalando dependencias de Python..." -ForegroundColor Yellow
Set-Location backend
pip install google-generativeai numpy --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencias instaladas correctamente`n" -ForegroundColor Green
} else {
    Write-Host "✗ Error instalando dependencias`n" -ForegroundColor Red
    exit 1
}

# 2. Verificar sistema
Write-Host "[2/4] Verificando integridad del sistema..." -ForegroundColor Yellow
python -c "from app.services.recomendacion_service import RecomendacionService; from app.api.v1.recomendaciones import router; print('OK')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Sistema verificado correctamente`n" -ForegroundColor Green
} else {
    Write-Host "✗ Error en verificación`n" -ForegroundColor Red
    exit 1
}

# 3. Crear tablas (opcional - comentado por seguridad)
Write-Host "[3/4] Creación de tablas en base de datos..." -ForegroundColor Yellow
Write-Host "⚠  Para crear las tablas, ejecuta manualmente:" -ForegroundColor Yellow
Write-Host "   python scripts\init_sistema_recomendaciones.py`n" -ForegroundColor White

# 4. Mostrar próximos pasos
Write-Host "[4/4] Sistema listo para usar`n" -ForegroundColor Yellow

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📋 PRÓXIMOS PASOS:`n" -ForegroundColor White

Write-Host "1. Configurar Gemini (opcional):" -ForegroundColor Yellow
Write-Host "   Agregar en .env: GEMINI_API_KEY=tu_key`n" -ForegroundColor White

Write-Host "2. Crear tablas en base de datos:" -ForegroundColor Yellow
Write-Host "   python scripts\init_sistema_recomendaciones.py`n" -ForegroundColor White

Write-Host "3. Iniciar servidor backend:" -ForegroundColor Yellow
Write-Host "   uvicorn app.main:app --reload`n" -ForegroundColor White

Write-Host "4. Verificar en Swagger:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs`n" -ForegroundColor White

Write-Host "5. Iniciar frontend Angular:" -ForegroundColor Yellow
Write-Host "   cd ..\src" -ForegroundColor White
Write-Host "   ng serve`n" -ForegroundColor White

Write-Host "📚 DOCUMENTACIÓN:`n" -ForegroundColor White
Write-Host "   • SISTEMA_RECOMENDACIONES_COMPLETO.md - Guía completa" -ForegroundColor Gray
Write-Host "   • GUIA_RAPIDA_RECOMENDACIONES.md - Inicio rápido" -ForegroundColor Gray
Write-Host "   • VERIFICACION_SISTEMA_COMPLETO.md - Estado del sistema`n" -ForegroundColor Gray

Write-Host "🎯 ENDPOINTS DISPONIBLES:`n" -ForegroundColor White
Write-Host "   POST /api/v1/recomendaciones/actividades/{nino_id}" -ForegroundColor Gray
Write-Host "   POST /api/v1/recomendaciones/terapeuta/{nino_id}" -ForegroundColor Gray
Write-Host "   POST /api/v1/recomendaciones/completa/{nino_id}" -ForegroundColor Gray
Write-Host "   POST /api/v1/recomendaciones/sugerencias/{nino_id}" -ForegroundColor Gray
Write-Host "   GET  /api/v1/recomendaciones/historial/{nino_id}`n" -ForegroundColor Gray

Set-Location ..
Write-Host "✨ ¡Listo para usar! ✨`n" -ForegroundColor Green

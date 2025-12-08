@echo off
REM ==================================================
REM Script de inicio del backend - Windows
REM ==================================================

echo ========================================
echo Backend - Autismo Mochis IA
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [ERROR] No existe el entorno virtual 'venv'
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    echo [OK] Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo Iniciando servidor con Uvicorn...
echo ========================================
echo.
echo Servidor corriendo en: http://localhost:8000
echo Documentacion API: http://localhost:8000/docs
echo.

REM Iniciar servidor
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause

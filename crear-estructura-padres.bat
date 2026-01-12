@echo off
REM Crear estructura de carpetas para el módulo padres

setlocal enabledelayedexpansion

set "basePath=C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\src\app\padres\pages"

REM Crear carpetas principales
mkdir "%basePath%\inicio" 2>nul
mkdir "%basePath%\mis-hijos" 2>nul
mkdir "%basePath%\mis-hijos\detalle-hijo" 2>nul
mkdir "%basePath%\sesiones" 2>nul
mkdir "%basePath%\sesiones\detalle-sesion" 2>nul
mkdir "%basePath%\historial-terapeutico" 2>nul
mkdir "%basePath%\tareas" 2>nul
mkdir "%basePath%\tareas\detalle-tarea" 2>nul
mkdir "%basePath%\pagos" 2>nul
mkdir "%basePath%\pagos\historial-pagos" 2>nul
mkdir "%basePath%\documentos" 2>nul
mkdir "%basePath%\documentos\detalle-documento" 2>nul
mkdir "%basePath%\recursos" 2>nul
mkdir "%basePath%\mensajes" 2>nul
mkdir "%basePath%\mensajes\chat" 2>nul
mkdir "%basePath%\notificaciones" 2>nul

echo Estructura de carpetas creada exitosamente!
echo.
echo Carpetas creadas en: %basePath%
dir "%basePath%" /s /b

pause

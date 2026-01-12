@echo off
REM Script para crear la estructura completa del módulo Padre
REM Ejecutar desde: src\app\padre

cd /d %~dp0

REM Crear todas las carpetas necesarias
mkdir mis-hijos
mkdir sesiones
mkdir historial-terapeutico
mkdir tareas
mkdir pagos-section
mkdir documentos-section
mkdir recursos
mkdir mensajes
mkdir notificaciones
mkdir perfil-accesibilidad

echo Estructura de carpetas creada exitosamente
pause

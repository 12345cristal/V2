@echo off
echo =====================================
echo   INSERTAR DATOS DE PRUEBA
echo =====================================
echo.

set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 9.2\bin\mysql.exe"
set SQL_FILE=backend\scripts\datos_ninos_topsis_recomendacion.sql

if not exist %SQL_FILE% (
    echo ERROR: No se encontro el archivo SQL
    echo Buscando en: %SQL_FILE%
    pause
    exit /b 1
)

echo Archivo SQL encontrado
echo.

set /p USUARIO="Usuario MySQL (por defecto: root): "
if "%USUARIO%"=="" set USUARIO=root

set /p PASSWORD="Contrasena MySQL: "

set /p BD="Base de datos (por defecto: autismo_mochis_ia): "
if "%BD%"=="" set BD=autismo_mochis_ia

echo.
echo Insertando datos en la base de datos...
echo.

%MYSQL_PATH% -u %USUARIO% -p%PASSWORD% %BD% < %SQL_FILE%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =====================================
    echo   DATOS INSERTADOS EXITOSAMENTE!
    echo =====================================
    echo.
    echo Datos insertados:
    echo   - 10 ninos con perfiles completos
    echo   - Datos para TOPSIS
    echo   - Datos para recomendaciones
    echo.
    echo Ahora puedes usar:
    echo   - /coordinador/prioridad-ninos
    echo   - /coordinador/recomendacion-nino
    echo   - /coordinador/topsis-terapeutas
    echo.
) else (
    echo.
    echo ERROR al insertar datos
    echo.
    echo Verifica que:
    echo   1. MySQL este corriendo
    echo   2. Las credenciales sean correctas
    echo   3. La base de datos '%BD%' exista
    echo.
)

pause

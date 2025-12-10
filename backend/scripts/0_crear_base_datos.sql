-- Script SQL para crear la base de datos e inicializar el sistema
-- Ejecutar este archivo desde phpMyAdmin (http://localhost/phpmyadmin)

-- 1. CREAR BASE DE DATOS
CREATE DATABASE IF NOT EXISTS autismo_mochis_ia 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

USE autismo_mochis_ia;

-- 2. MENSAJE DE CONFIRMACIÓN
SELECT 'Base de datos creada exitosamente' AS resultado;
SELECT 'Ahora ejecuta los siguientes scripts en orden:' AS siguiente_paso;
SELECT '1. migrar_estados_y_tipo_sangre.sql' AS paso_1;
SELECT '2. crear_tabla_fichas_emergencia.sql' AS paso_2;
SELECT 'O usa el script Python: poblar_sistema_completo.py' AS alternativa;

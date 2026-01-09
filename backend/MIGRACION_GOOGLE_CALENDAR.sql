-- ==========================================
-- MIGRACIÓN: Agregar campos de Google Calendar a tabla citas
-- Fecha: 9 de enero de 2026
-- Problema resuelto: sqlalchemy.exc.OperationalError (1054, "Unknown column 'citas.google_event_id'")
-- ==========================================

-- 📋 CONTEXTO:
-- El modelo ORM SQLAlchemy define 4 columnas para integración con Google Calendar
-- que NO existen en la tabla MySQL, causando errores incluso en queries .count()

-- 🔧 SOLUCIÓN: ALTER TABLE para sincronizar base de datos con modelo ORM

USE autismo;  -- Ajusta el nombre de tu base de datos si es diferente

-- ✅ Paso 1: Agregar columnas de Google Calendar
ALTER TABLE citas 
    ADD COLUMN google_event_id VARCHAR(255) NULL UNIQUE COMMENT 'ID del evento en Google Calendar',
    ADD COLUMN google_calendar_link VARCHAR(500) NULL COMMENT 'URL del evento en Google Calendar',
    ADD COLUMN sincronizado_calendar TINYINT(1) NOT NULL DEFAULT 0 COMMENT 'Indica si está sincronizado con Google Calendar',
    ADD COLUMN fecha_sincronizacion DATETIME NULL COMMENT 'Última fecha de sincronización con Google Calendar';

-- ✅ Paso 2: Agregar índices para optimizar búsquedas
ALTER TABLE citas 
    ADD INDEX idx_google_event_id (google_event_id),
    ADD INDEX idx_sincronizado_calendar (sincronizado_calendar);

-- ✅ Paso 3: Verificar estructura final
DESC citas;

-- ✅ Paso 4: Verificar que no hay datos corruptos (debe retornar 0)
SELECT COUNT(*) as registros_con_datos_google 
FROM citas 
WHERE google_event_id IS NOT NULL;

-- ==========================================
-- 📊 RESULTADOS ESPERADOS:
-- ==========================================
-- - 4 columnas nuevas agregadas exitosamente
-- - Datos existentes preservados (valores NULL en nuevas columnas)
-- - Índices creados para mejorar performance
-- - Modelo ORM y BD ahora sincronizados
-- - Endpoints /coordinador/dashboard y /citas funcionarán correctamente

-- ==========================================
-- 🔄 SIGUIENTES PASOS (Recomendado para producción):
-- ==========================================
-- 1. Implementar Alembic para migraciones versionadas
-- 2. Crear backup antes de ejecutar en producción:
--    mysqldump -u root -p autismo > backup_pre_google_calendar.sql
-- 3. Ejecutar esta migración en entorno de desarrollo primero
-- 4. Validar endpoints funcionan correctamente
-- 5. Ejecutar en producción durante ventana de mantenimiento

-- ==========================================
-- 🐛 EXPLICACIÓN DEL ERROR ORIGINAL:
-- ==========================================
-- SQLAlchemy construye queries SQL basándose en la metadata del modelo ORM.
-- Aunque se ejecute solo `.count()`, SQLAlchemy genera un SELECT que incluye
-- todas las columnas definidas en el modelo. MySQL rechaza la query porque
-- `citas.google_event_id` no existe físicamente en la tabla.
--
-- La única solución profesional es sincronizar la BD con el modelo ORM.
-- NO usar try/except para ocultar el error.
-- NO eliminar las columnas del modelo (se necesitan para Google Calendar).
-- ==========================================

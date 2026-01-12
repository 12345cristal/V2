-- Agregar columnas faltantes a personal_perfil
ALTER TABLE personal_perfil ADD COLUMN foto_perfil VARCHAR(255) NULL DEFAULT NULL;
ALTER TABLE personal_perfil ADD COLUMN cv_archivo VARCHAR(255) NULL DEFAULT NULL;
ALTER TABLE personal_perfil ADD COLUMN documentos_extra TEXT NULL DEFAULT NULL;

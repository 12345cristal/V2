-- Add missing columns to personal_perfil table
USE autismo_mochis_ia;

ALTER TABLE personal_perfil 
ADD COLUMN IF NOT EXISTS foto_perfil VARCHAR(255),
ADD COLUMN IF NOT EXISTS cv_archivo VARCHAR(255),
ADD COLUMN IF NOT EXISTS documentos_extra TEXT;

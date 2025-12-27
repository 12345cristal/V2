-- -----------------------------------------------------
-- Tablas de Chatbot (MySQL) - Autismo Mochis IA
-- Compatible con MySQL 8.x y PyMySQL
-- -----------------------------------------------------

-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS `autismo_mochis_ia`
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE `autismo_mochis_ia`;

-- -----------------------------------------------------
-- Tabla: chat_sessions
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` CHAR(32) NOT NULL,
  `nino_id` INT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `active` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_chat_sessions_session_id` (`session_id`),
  KEY `ix_chat_sessions_nino_id` (`nino_id`),
  KEY `ix_chat_sessions_session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------
-- Tabla: chat_messages
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chat_messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `session_id` CHAR(32) NOT NULL,
  `role` ENUM('usuario','asistente') NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_chat_messages_session_id` (`session_id`),
  CONSTRAINT `fk_chat_messages_session_id`
    FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`session_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

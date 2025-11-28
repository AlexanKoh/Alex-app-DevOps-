-- Создаем базу данных если не существует (на всякий случай)
CREATE DATABASE IF NOT EXISTS users_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Используем нашу базу
USE users_db;

-- Таблица создастся автоматически в приложении, но можно и здесь
-- CREATE TABLE IF NOT EXISTS users (...);

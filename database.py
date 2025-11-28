import pymysql
import os
from typing import List, Dict, Optional

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'users_db')
        self.port = int(os.getenv('DB_PORT', '3306'))
        
    def get_connection(self):
        """Создает и возвращает соединение с базой данных"""
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def init_db(self):
        """Инициализирует базу данных и создает таблицу пользователей"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            conn.commit()
            print("✅ Таблица users создана или уже существует")
        except Exception as e:
            print(f"❌ Ошибка при создании таблицы: {e}")
            raise
        finally:
            conn.close()
    
    def get_all_users(self) -> List[Dict]:
        """Возвращает всех пользователей"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id, name, email, created_at FROM users')
                return cursor.fetchall()
        finally:
            conn.close()
    
    def create_user(self, name: str, email: str) -> Optional[int]:
        """Создает нового пользователя и возвращает его ID"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (name, email) VALUES (%s, %s)',
                    (name, email)
                )
                conn.commit()
                return cursor.lastrowid
        except pymysql.IntegrityError:
            # Обработка дублирующихся email
            return None
        finally:
            conn.close()
    
    def get_db_info(self) -> Dict:
        """Возвращает информацию о подключении к БД"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT VERSION() as version')
                version = cursor.fetchone()
                
                return {
                    'host': self.host,
                    'port': self.port,
                    'database': self.database,
                    'user': self.user,
                    'mysql_version': version['version'] if version else 'Unknown'
                }
        finally:
            conn.close()

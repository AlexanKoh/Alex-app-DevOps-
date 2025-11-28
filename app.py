from flask import Flask, request, jsonify
from database import Database
import os
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
db = Database()

def wait_for_db(max_retries=30, delay_seconds=2):
    """Ожидает пока база данных станет доступной"""
    for i in range(max_retries):
        try:
            conn = db.get_connection()
            conn.close()
            logger.info("Database connection established successfully")
            return True
        except Exception as e:
            logger.warning(f"Database connection failed (attempt {i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                time.sleep(delay_seconds)
    
    logger.error("Could not establish database connection after all retries")
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка жизнеспособности приложения и БД"""
    try:
        conn = db.get_connection()
        conn.close()
        return jsonify({
            "status": "ok", 
            "database": "connected",
            "timestamp": time.time()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "database": "disconnected",
            "error": str(e)
        }), 503

@app.route('/users', methods=['GET'])
def get_users():
    """Возвращает список всех пользователей"""
    try:
        users = db.get_all_users()
        return jsonify({
            "users": users,
            "count": len(users)
        })
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    """Создает нового пользователя"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        name = data.get('name')
        email = data.get('email')
        
        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400
        
        user_id = db.create_user(name, email)
        
        if user_id is None:
            return jsonify({"error": "User with this email already exists"}), 409
        
        logger.info(f"User created: {name} ({email})")
        return jsonify({
            "id": user_id,
            "name": name,
            "email": email,
            "message": "User created successfully"
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/db', methods=['GET'])
def db_info():
    """Возвращает информацию о подключении к БД"""
    try:
        info = db.get_db_info()
        info['user'] = info['user']
        return jsonify(info)
    except Exception as e:
        logger.error(f"Error getting DB info: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting application initialization...")
    if wait_for_db():
        db.init_db()
        logger.info("Database initialized successfully")
        port = int(os.getenv('PORT', '5000'))
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        logger.info(f"Starting Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        logger.error("Failed to initialize application due to database connection issues")
        exit(1)

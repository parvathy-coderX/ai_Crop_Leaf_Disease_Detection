"""
Configuration file for SmartAgriAI
Contains API keys, database URIs, and model paths
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'your_api_key_here')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'your_api_key_here')
    
    # Model Paths
    DISEASE_MODEL_PATH = 'models/disease_model.h5'
    WEATHER_MODEL_PATH = 'models/weather_model.pkl'
    
    # Database Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = 'smartagriai_db'
    
    # Upload Settings
    UPLOAD_FOLDER = 'static/uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Weather API Settings
    WEATHER_API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    
    # Risk thresholds
    TEMP_HIGH_THRESHOLD = 35  # Celsius
    HUMIDITY_HIGH_THRESHOLD = 80  # Percentage
    RAIN_HEAVY_THRESHOLD = 20  # mm
    
    # ===== ADD THESE NEW CONFIGURATIONS =====
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    TESTING = False
    
    # JWT Settings (for authentication)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60  # 24 hours
    
    # File Upload Settings
    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB max image size
    ALLOWED_IMAGE_FORMATS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    UPLOAD_IMAGE_QUALITY = 85  # JPEG compression quality (1-100)
    
    # Model Settings
    MODEL_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for predictions
    MODEL_INPUT_SIZE = (224, 224)  # Default input size for models
    ENABLE_FALLBACK_MODEL = True  # Use fallback if main model fails
    
    # Cache Settings
    CACHE_TYPE = 'simple'  # redis, simple, filesystem
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = 'smartagriai_'
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per day, 10 per hour"
    RATELIMIT_STRATEGY = 'fixed-window'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/app.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # API Settings
    API_TITLE = 'SmartAgriAI API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'AI-powered agricultural assistant API'
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Date/Time Settings
    TIMEZONE = 'Asia/Kolkata'
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Email Settings (for future use)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@smartagriai.com')
    
    # SMS Settings (for future use)
    SMS_API_KEY = os.getenv('SMS_API_KEY')
    SMS_SENDER_ID = os.getenv('SMS_SENDER_ID', 'SMARTAG')
    
    # Feature Flags
    ENABLE_DISEASE_DETECTION = True
    ENABLE_WEATHER_PREDICTION = True
    ENABLE_SCHEME_RECOMMENDATION = True
    ENABLE_USER_HISTORY = True
    ENABLE_NOTIFICATIONS = False
    
    # Prediction Settings
    SAVE_PREDICTION_IMAGES = True  # Save uploaded images for analysis
    PREDICTION_HISTORY_DAYS = 90  # Keep history for 90 days
    
    # Weather Settings
    WEATHER_UPDATE_INTERVAL = 30 * 60  # Update weather every 30 minutes (seconds)
    WEATHER_CACHE_TIMEOUT = 15 * 60  # Cache weather for 15 minutes
    
    # Scheme Settings
    SCHEMES_CACHE_TIMEOUT = 24 * 60 * 60  # Cache schemes for 24 hours
    MAX_SCHEME_RECOMMENDATIONS = 10
    
    # Map Settings
    MAP_DEFAULT_ZOOM = 10
    MAP_MAX_ZOOM = 18
    MAP_SEARCH_RADIUS = 20  # km
    
    # Performance Settings
    MODEL_PREDICTION_TIMEOUT = 10  # seconds
    API_REQUEST_TIMEOUT = 30  # seconds
    MAX_WORKERS = 4  # Thread pool size for parallel processing
    
    # Security Settings
    BCRYPT_ROUNDS = 12  # Password hashing rounds
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 30 * 24 * 60 * 60  # 30 days
    
    # Development vs Production
    @classmethod
    def is_production(cls):
        return os.getenv('FLASK_ENV') == 'production'
    
    @classmethod
    def is_development(cls):
        return os.getenv('FLASK_ENV') == 'development'
    
    @classmethod
    def is_testing(cls):
        return os.getenv('FLASK_ENV') == 'testing'

# You can also create different config classes for different environments
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    CACHE_TYPE = 'simple'
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    CACHE_TYPE = 'redis'
    RATELIMIT_ENABLED = True
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    CACHE_TYPE = 'simple'
    RATELIMIT_ENABLED = False
    MONGO_URI = 'mongodb://localhost:27017/smartagriai_test'
    UPLOAD_FOLDER = 'tests/uploads/'

# Select config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

# Default config
config = DevelopmentConfig  # Default to development
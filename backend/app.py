"""
Main Flask application for SmartAgriAI
"""

from flask import Flask, jsonify, request  # ✅ Add 'request' here
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import Config
import os
import logging

# Initialize extensions
mongo = PyMongo()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS with specific settings for file uploads
    CORS(app, 
         origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Your React app URL
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         supports_credentials=True,
         expose_headers=["Content-Range", "X-Content-Range"])
    
    # Initialize MongoDB
    app.config["MONGO_URI"] = Config.MONGO_URI + Config.DATABASE_NAME
    mongo.init_app(app)
    
    # Create upload folder if it doesn't exist
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    print(f"✅ Upload folder configured: {os.path.abspath(upload_folder)}")
    
    # Set maximum file size
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Register blueprints (routes)
    try:
        from routes.disease_routes import disease_bp
        from routes.weather_routes import weather_bp
        from routes.scheme_routes import scheme_bp
        from routes.user_routes import user_bp
        
        app.register_blueprint(disease_bp, url_prefix='/api/disease')
        app.register_blueprint(weather_bp, url_prefix='/api/weather')
        app.register_blueprint(scheme_bp, url_prefix='/api/schemes')
        app.register_blueprint(user_bp, url_prefix='/api/user')
        
        print("✅ Blueprints registered successfully")
    except Exception as e:
        print(f"❌ Error registering blueprints: {e}")
    
    @app.route('/')
    def home():
        """Home endpoint with API information"""
        return jsonify({
            'message': 'Welcome to SmartAgriAI API',
            'version': '1.0',
            'status': 'running',
            'upload_folder': os.path.basename(app.config['UPLOAD_FOLDER']),
            'endpoints': [
                '/api/disease/predict',
                '/api/disease/health',
                '/api/disease/diseases/list',
                '/api/weather/risk',
                '/api/weather/current',
                '/api/weather/forecast',
                '/api/schemes/recommend',
                '/api/schemes/search',
                '/api/user/register',
                '/api/user/login',
                '/api/user/<user_id>/history'
            ]
        })
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for debugging"""
        return jsonify({
            'status': 'healthy',
            'service': 'SmartAgriAI API',
            'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
            'cors_enabled': True
        }), 200
    
    # Add error handler for large files
    @app.errorhandler(413)
    def too_large(e):
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413
    
    # Add error handler for CORS preflight
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = jsonify({'status': 'ok'})
            response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
            return response
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*50)
    print("🚀 SmartAgriAI API Server Starting...")
    print("="*50)
    print(f"📍 Backend URL: http://localhost:5000")
    print(f"📍 Frontend URL: http://localhost:3000")
    print(f"📍 Upload folder: {os.path.abspath(app.config['UPLOAD_FOLDER'])}")
    print(f"📍 Debug mode: {app.debug}")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
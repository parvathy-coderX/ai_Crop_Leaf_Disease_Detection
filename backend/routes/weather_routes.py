"""
Weather-based disease risk prediction API routes for SmartAgriAI
Handles weather data fetching, risk assessment, and forecasting
"""

from flask import Blueprint, request, jsonify
from services.weather_service import WeatherService
from config import Config
from datetime import datetime
import logging
import traceback

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
weather_bp = Blueprint('weather', __name__)

# Initialize service
weather_service = WeatherService(Config.WEATHER_MODEL_PATH)

# Crop database
CROP_DATABASE = {
    'rice': {'name': 'Rice', 'optimal_temp': (20, 35), 'optimal_humidity': (60, 80)},
    'wheat': {'name': 'Wheat', 'optimal_temp': (15, 25), 'optimal_humidity': (40, 60)},
    'cotton': {'name': 'Cotton', 'optimal_temp': (25, 35), 'optimal_humidity': (50, 70)},
    'sugarcane': {'name': 'Sugarcane', 'optimal_temp': (25, 35), 'optimal_humidity': (60, 80)},
    'banana': {'name': 'Banana', 'optimal_temp': (25, 30), 'optimal_humidity': (70, 85)},
    'coconut': {'name': 'Coconut', 'optimal_temp': (27, 32), 'optimal_humidity': (70, 85)},
    'tomato': {'name': 'Tomato', 'optimal_temp': (20, 27), 'optimal_humidity': (60, 70)},
    'potato': {'name': 'Potato', 'optimal_temp': (15, 20), 'optimal_humidity': (70, 80)},
    'pepper': {'name': 'Bell Pepper', 'optimal_temp': (20, 25), 'optimal_humidity': (60, 70)}
}

@weather_bp.route('/risk', methods=['POST'])
def get_weather_risk():
    """Get weather-based disease risk assessment"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['lat', 'lon', 'crop_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        lat = float(data['lat'])
        lon = float(data['lon'])
        crop_type = data['crop_type'].lower()
        
        # Validate crop type
        if crop_type not in CROP_DATABASE:
            return jsonify({
                'success': False,
                'error': f'Unsupported crop: {crop_type}',
                'supported_crops': list(CROP_DATABASE.keys())
            }), 400
        
        # Get risk assessment
        risk_assessment = weather_service.predict_disease_risk(lat, lon, crop_type)
        risk_assessment['crop_info'] = CROP_DATABASE[crop_type]
        risk_assessment['timestamp'] = datetime.now().isoformat()
        
        return jsonify({'success': True, 'data': risk_assessment}), 200
        
    except Exception as e:
        logger.error(f"Error in weather risk: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    """Get current weather for location"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        if not lat or not lon:
            return jsonify({'success': False, 'error': 'Latitude and longitude required'}), 400
        
        weather_data = weather_service.get_current_weather(float(lat), float(lon))
        
        return jsonify({'success': True, 'data': weather_data}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@weather_bp.route('/forecast', methods=['GET'])
def get_weather_forecast():
    """Get weather forecast"""
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        days = int(request.args.get('days', 5))
        
        if not lat or not lon:
            return jsonify({'success': False, 'error': 'Latitude and longitude required'}), 400
        
        days = min(days, 7)
        forecast = weather_service.get_forecast(float(lat), float(lon), days)
        
        return jsonify({'success': True, 'data': {'forecast': forecast, 'days': days}}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@weather_bp.route('/crops', methods=['GET'])
def get_supported_crops():
    """List supported crops"""
    crops = []
    for crop_id, info in CROP_DATABASE.items():
        crops.append({
            'id': crop_id,
            'name': info['name'],
            'optimal_temp': f"{info['optimal_temp'][0]}-{info['optimal_temp'][1]}°C",
            'optimal_humidity': f"{info['optimal_humidity'][0]}-{info['optimal_humidity'][1]}%"
        })
    
    return jsonify({'success': True, 'count': len(crops), 'crops': crops}), 200

@weather_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'weather_service',
        'status': 'healthy',
        'supported_crops': list(CROP_DATABASE.keys())
    }), 200
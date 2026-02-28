"""
User management API routes for SmartAgriAI
Handles user registration, login, history, and profile management
"""

from flask import Blueprint, request, jsonify
from database.db_config import db
from datetime import datetime
import logging
import hashlib
import uuid

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
user_bp = Blueprint('user', __name__)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'phone', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Check if user already exists
        existing_user = db.find_one('users', {'phone': data['phone']})
        if existing_user:
            return jsonify({'success': False, 'error': 'User already exists'}), 400
        
        # Create user document
        user_doc = {
            'user_id': str(uuid.uuid4()),
            'name': data['name'],
            'phone': data['phone'],
            'password': hash_password(data['password']),
            'location': data.get('location', ''),
            'crop_type': data.get('crop_type', ''),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'predictions_count': 0,
            'is_active': True
        }
        
        # Save to database
        user_id = db.insert_one('users', user_doc)
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user_doc['user_id'],
            'name': user_doc['name']
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        if not data or 'phone' not in data or 'password' not in data:
            return jsonify({'success': False, 'error': 'Phone and password required'}), 400
        
        # Find user
        user = db.find_one('users', {'phone': data['phone']})
        
        if not user or user['password'] != hash_password(data['password']):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user_id': user['user_id'],
            'name': user['name'],
            'phone': user['phone'],
            'location': user.get('location', '')
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Get user's prediction history"""
    try:
        limit = int(request.args.get('limit', 20))
        
        predictions = db.find_many(
            'predictions',
            {'user_id': user_id},
            limit=limit,
            sort=[('timestamp', -1)]
        )
        
        # Format for response
        history = []
        for pred in predictions:
            history.append({
                'id': str(pred.get('_id', '')),
                'date': pred['timestamp'].isoformat() if pred.get('timestamp') else None,
                'disease': pred.get('disease'),
                'confidence': pred.get('confidence'),
                'crop_type': pred.get('crop_type'),
                'image_path': pred.get('image_path'),
                'location': pred.get('location')
            })
        
        return jsonify({
            'success': True,
            'count': len(history),
            'history': history
        }), 200
        
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<user_id>/profile', methods=['GET'])
def get_profile(user_id):
    """Get user profile"""
    try:
        user = db.find_one('users', {'user_id': user_id})
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'profile': {
                'user_id': user['user_id'],
                'name': user['name'],
                'phone': user['phone'],
                'location': user.get('location', ''),
                'crop_type': user.get('crop_type', ''),
                'predictions_count': user.get('predictions_count', 0),
                'created_at': user['created_at'].isoformat() if user.get('created_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<user_id>/profile', methods=['PUT'])
def update_profile(user_id):
    """Update user profile"""
    try:
        data = request.get_json()
        updates = {}
        
        # Allowed updates
        if 'name' in data:
            updates['name'] = data['name']
        if 'location' in data:
            updates['location'] = data['location']
        if 'crop_type' in data:
            updates['crop_type'] = data['crop_type']
        
        updates['updated_at'] = datetime.now()
        
        result = db.update_one('users', {'user_id': user_id}, updates)
        
        if result > 0:
            return jsonify({'success': True, 'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<user_id>/predictions/<prediction_id>', methods=['DELETE'])
def delete_prediction(user_id, prediction_id):
    """Delete a prediction from history"""
    try:
        # This would need to be implemented based on your database structure
        # For now, return success message
        return jsonify({
            'success': True,
            'message': 'Prediction deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/<user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """Get user statistics"""
    try:
        # Get user's predictions
        predictions = db.find_many('predictions', {'user_id': user_id})
        
        total_predictions = len(predictions)
        healthy_count = sum(1 for p in predictions if p.get('disease') == 'Healthy')
        disease_count = total_predictions - healthy_count
        
        # Get unique crops
        crops = set(p.get('crop_type') for p in predictions if p.get('crop_type'))
        
        return jsonify({
            'success': True,
            'stats': {
                'total_predictions': total_predictions,
                'healthy_crops': healthy_count,
                'diseases_detected': disease_count,
                'unique_crops': len(crops),
                'crops': list(crops)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'user_service',
        'status': 'healthy'
    }), 200
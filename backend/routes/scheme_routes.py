"""
Government scheme recommendation API routes for SmartAgriAI
Handles fetching and filtering government agricultural schemes
"""

from flask import Blueprint, request, jsonify
from services.scheme_service import SchemeService
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
scheme_bp = Blueprint('scheme', __name__)

# Initialize service
scheme_service = SchemeService()

@scheme_bp.route('/recommend', methods=['POST'])
def recommend_schemes():
    """Get government scheme recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        if 'state' not in data:
            return jsonify({'success': False, 'error': 'State is required'}), 400
        
        # Get recommendations
        recommendations = scheme_service.recommend_schemes(
            data['state'],
            data.get('crop_type'),
            data.get('disease')
        )
        
        return jsonify({
            'success': True,
            'count': len(recommendations),
            'schemes': recommendations,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in scheme recommendation: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@scheme_bp.route('/search', methods=['GET'])
def search_schemes():
    """Search schemes by keyword"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        results = scheme_service.search_schemes(query)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'schemes': results
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@scheme_bp.route('/<scheme_id>', methods=['GET'])
def get_scheme_by_id(scheme_id):
    """Get scheme details by ID"""
    try:
        scheme = scheme_service.get_scheme_by_id(scheme_id)
        
        if scheme:
            return jsonify({'success': True, 'scheme': scheme}), 200
        else:
            return jsonify({'success': False, 'error': 'Scheme not found'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@scheme_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get scheme categories"""
    try:
        categories = scheme_service.get_scheme_categories()
        return jsonify({'success': True, 'categories': categories}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@scheme_bp.route('/stats', methods=['GET'])
def get_statistics():
    """Get scheme statistics"""
    try:
        stats = scheme_service.get_statistics()
        return jsonify({'success': True, 'statistics': stats}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@scheme_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    stats = scheme_service.get_statistics()
    return jsonify({
        'success': True,
        'service': 'scheme_service',
        'status': 'healthy',
        'statistics': stats
    }), 200
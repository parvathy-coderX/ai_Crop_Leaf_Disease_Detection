"""
Disease detection API routes for SmartAgriAI
Handles image upload and disease prediction
"""

from flask import Blueprint, request, jsonify
from services.disease_service import DiseaseDetectionService
from config import Config
from utils.preprocess import allowed_file
from utils.image_helper import save_uploaded_image, validate_image
import os

# Create blueprint
disease_bp = Blueprint('disease', __name__)

# Initialize disease detection service
disease_service = DiseaseDetectionService(Config.DISEASE_MODEL_PATH)

@disease_bp.route('/predict', methods=['POST'])
def predict_disease():
    """
    Endpoint to predict disease from leaf image.
    Expects: image file in form-data
    Returns: disease prediction with confidence
    """
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        return jsonify({
            'success': False,
            'error': f'File type not allowed. Allowed types: {", ".join(Config.ALLOWED_EXTENSIONS)}'
        }), 400

    # Validate image integrity
    image_bytes = file.read()
    is_valid, validation_msg = validate_image(image_bytes)
    if not is_valid:
        return jsonify({'success': False, 'error': validation_msg}), 400

    # Save uploaded image (optional)
    file.seek(0)
    saved_path = save_uploaded_image(file, Config.UPLOAD_FOLDER)

    # Predict disease
    result = disease_service.predict(image_bytes)

    if result['success']:
        # Add image path and return
        result['image_path'] = os.path.basename(saved_path)
        return jsonify(result), 200
    else:
        return jsonify(result), 500
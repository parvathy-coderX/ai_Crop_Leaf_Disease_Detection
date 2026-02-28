"""
Image preprocessing utilities for disease detection
"""

import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image(image_bytes, target_size=(224, 224)):
    """
    Preprocess image for CNN model
    Args:
        image_bytes: Raw image bytes
        target_size: Target size for model input
    Returns:
        Preprocessed image array
    """
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to numpy array
        image_array = np.array(image)
        
        # Normalize pixel values
        image_array = image_array / 255.0
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
        
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

def allowed_file(filename, allowed_extensions):
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
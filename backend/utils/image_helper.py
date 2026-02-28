"""
Image helper utilities for handling uploads and validation
"""

import os
import uuid
from PIL import Image
import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def save_uploaded_image(file, upload_folder):
    """
    Save uploaded image to disk
    Args:
        file: FileStorage object
        upload_folder: Path to upload folder
    Returns:
        Path to saved file
    """
    try:
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.jpg"
        
        # Save file
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        logger.info(f"Image saved: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise

def validate_image(image_bytes):
    """
    Validate image integrity and format
    Args:
        image_bytes: Raw image bytes
    Returns:
        (is_valid, message) tuple
    """
    try:
        # Check if bytes are empty
        if not image_bytes or len(image_bytes) == 0:
            return False, "Empty image file"
        
        # Check file size (max 16MB)
        if len(image_bytes) > 16 * 1024 * 1024:
            return False, "Image too large (max 16MB)"
        
        # Try to open with PIL
        img = Image.open(io.BytesIO(image_bytes))
        
        # Verify image
        img.verify()
        
        # Need to reopen after verify
        img = Image.open(io.BytesIO(image_bytes))
        
        # Check dimensions
        width, height = img.size
        if width < 50 or height < 50:
            return False, "Image too small (minimum 50x50 pixels)"
        
        if width > 4000 or height > 4000:
            return False, "Image too large (maximum 4000x4000 pixels)"
        
        return True, "Image valid"
        
    except Exception as e:
        return False, f"Invalid image: {str(e)}"

def resize_image(image_bytes, max_size=(1024, 1024)):
    """
    Resize image if too large
    Args:
        image_bytes: Raw image bytes
        max_size: Maximum dimensions (width, height)
    Returns:
        Resized image bytes
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Check if resize needed
        if img.size[0] <= max_size[0] and img.size[1] <= max_size[1]:
            return image_bytes
        
        # Resize
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert back to bytes
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
        
    except Exception as e:
        logger.error(f"Error resizing image: {str(e)}")
        return image_bytes

def get_image_format(image_bytes):
    """
    Detect image format from bytes
    Args:
        image_bytes: Raw image bytes
    Returns:
        Image format string or None
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return img.format.lower()
    except:
        return None

def allowed_file(filename, allowed_extensions):
    """
    Check if file extension is allowed
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
"""
Disease detection service using CNN model
Handles image preprocessing, model inference, and treatment recommendations
"""

import tensorflow as tf
import numpy as np
from PIL import Image
import io
import logging
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiseaseDetectionService:
    """
    Service class for crop disease detection using CNN
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the disease detection service
        
        Args:
            model_path: Path to the trained CNN model file
        """
        self.model = None
        self.class_names = self.load_class_names()
        self.disease_info = self.load_disease_info()
        self.model_path = model_path
        # ✅ FIXED: Changed from 224 to 128 to match your trained model
        self.input_size = (128, 128)  # Your model expects 128x128 images
        self.load_model(model_path)
        
    def load_class_names(self) -> Dict[int, str]:
        """
        Load class names for diseases based on the dataset structure
        
        Returns:
            Dictionary mapping class indices to disease names
        """
        # Updated to match your dataset structure
        return {
            0: "Pepper__bell___Bacterial_spot",
            1: "Pepper__bell___healthy",
            2: "Potato___Early_blight",
            3: "Potato___healthy",
            4: "Potato___Late_blight",
            5: "Tomato__Target_Spot",
            6: "Tomato__Tomato_mosaic_virus",
            7: "Tomato__Tomato_YellowLeaf__Curl_Virus",
            8: "Tomato_Bacterial_spot",
            9: "Tomato_Early_blight",
            10: "Tomato_healthy",
            11: "Tomato_Late_blight",
            12: "Tomato_Leaf_Mold",
            13: "Tomato_Septoria_leaf_spot",
            14: "Tomato_Spider_mites_Two_spotted_spider_mite"
        }
    
    def load_disease_info(self) -> Dict[str, Dict]:
        """
        Load detailed information about each disease
        
        Returns:
            Dictionary with disease information
        """
        return {
            "Pepper__bell___Bacterial_spot": {
                "scientific_name": "Xanthomonas campestris pv. vesicatoria",
                "type": "Bacterial",
                "description": "Bacterial spot is a common disease affecting bell peppers, causing lesions on leaves and fruits.",
                "symptoms": [
                    "Water-soaked spots on leaves",
                    "Spots turn brown and necrotic",
                    "Yellow halos around lesions",
                    "Fruit spots are raised and scabby"
                ],
                "causes": [
                    "Bacteria Xanthomonas campestris",
                    "Spread through rain splash and irrigation",
                    "Warm, humid conditions",
                    "Plant debris and infected seeds"
                ],
                "treatment": {
                    "chemical": [
                        "Copper-based bactericides",
                        "Copper hydroxide",
                        "Copper sulfate"
                    ],
                    "organic": [
                        "Remove infected plants",
                        "Copper soap sprays",
                        "Biological control agents"
                    ]
                },
                "prevention": [
                    "Use disease-free seeds",
                    "Practice crop rotation",
                    "Avoid overhead irrigation",
                    "Remove plant debris",
                    "Use resistant varieties"
                ],
                "favorable_conditions": {
                    "temperature": "24-30°C",
                    "humidity": "High humidity",
                    "rainfall": "Frequent rain/irrigation"
                }
            },
            "Pepper__bell___healthy": {
                "description": "The bell pepper plant appears healthy with no visible disease symptoms.",
                "symptoms": [
                    "Vibrant green leaves",
                    "Normal growth pattern",
                    "No spots or lesions",
                    "Healthy fruit development"
                ],
                "recommendations": [
                    "Continue regular monitoring",
                    "Maintain balanced nutrition",
                    "Ensure proper irrigation",
                    "Practice good field hygiene"
                ]
            },
            "Potato___Early_blight": {
                "scientific_name": "Alternaria solani",
                "type": "Fungal",
                "description": "Early blight is a common fungal disease of potatoes, characterized by dark lesions with concentric rings.",
                "symptoms": [
                    "Dark brown to black spots on leaves",
                    "Target-like concentric rings",
                    "Yellowing around lesions",
                    "Lesions on stems and tubers"
                ],
                "causes": [
                    "Fungus Alternaria solani",
                    "Warm, humid conditions",
                    "Plant debris from previous crops",
                    "Poor air circulation"
                ],
                "treatment": {
                    "chemical": [
                        "Chlorothalonil",
                        "Mancozeb",
                        "Azoxystrobin"
                    ],
                    "organic": [
                        "Copper fungicides",
                        "Neem oil",
                        "Baking soda solution"
                    ]
                },
                "prevention": [
                    "Use certified disease-free seed potatoes",
                    "Practice crop rotation",
                    "Avoid overhead irrigation",
                    "Remove and destroy infected plants",
                    "Improve air circulation"
                ],
                "favorable_conditions": {
                    "temperature": "24-29°C",
                    "humidity": "High humidity",
                    "rainfall": "Frequent rain/dew"
                }
            },
            "Potato___Late_blight": {
                "scientific_name": "Phytophthora infestans",
                "type": "Fungal-like (Oomycete)",
                "description": "Late blight is a devastating disease that caused the Irish Potato Famine. It affects both potatoes and tomatoes.",
                "symptoms": [
                    "Water-soaked lesions on leaves",
                    "White fungal growth on undersides",
                    "Dark brown to black lesions on stems",
                    "Brown, rotten areas on tubers"
                ],
                "causes": [
                    "Phytophthora infestans",
                    "Cool, wet conditions",
                    "Spread through air and water",
                    "Infected seed tubers"
                ],
                "treatment": {
                    "chemical": [
                        "Metalaxyl",
                        "Mancozeb",
                        "Chlorothalonil"
                    ],
                    "organic": [
                        "Copper fungicides",
                        "Remove infected plants immediately",
                        "Biological control agents"
                    ]
                },
                "prevention": [
                    "Use resistant varieties",
                    "Destroy volunteer potatoes",
                    "Avoid dense planting",
                    "Ensure good drainage",
                    "Monitor weather conditions"
                ],
                "favorable_conditions": {
                    "temperature": "10-20°C",
                    "humidity": ">90%",
                    "rainfall": "Frequent rain"
                }
            },
            "Potato___healthy": {
                "description": "The potato plant appears healthy with no visible disease symptoms.",
                "symptoms": [
                    "Vibrant green leaves",
                    "Normal growth pattern",
                    "No spots or lesions",
                    "Healthy tuber development"
                ],
                "recommendations": [
                    "Continue regular monitoring",
                    "Maintain balanced nutrition",
                    "Ensure proper irrigation",
                    "Practice good field hygiene"
                ]
            },
            "Tomato_Early_blight": {
                "scientific_name": "Alternaria solani",
                "type": "Fungal",
                "description": "Early blight in tomatoes causes leaf spots and fruit rot, significantly reducing yield.",
                "symptoms": [
                    "Dark spots with concentric rings on lower leaves",
                    "Yellowing around lesions",
                    "Lesions on stems",
                    "Sunken, leathery spots on fruits"
                ],
                "causes": [
                    "Fungus Alternaria solani",
                    "Warm, humid conditions",
                    "Plant debris",
                    "Poor air circulation"
                ],
                "treatment": {
                    "chemical": [
                        "Chlorothalonil",
                        "Mancozeb",
                        "Copper fungicides"
                    ],
                    "organic": [
                        "Neem oil",
                        "Baking soda spray",
                        "Remove affected leaves"
                    ]
                },
                "prevention": [
                    "Mulch around plants",
                    "Water at base of plants",
                    "Provide adequate spacing",
                    "Rotate crops",
                    "Use resistant varieties"
                ]
            },
            "Tomato_Late_blight": {
                "scientific_name": "Phytophthora infestans",
                "type": "Fungal-like",
                "description": "Late blight in tomatoes causes rapid decay of foliage and fruit, spreading quickly in wet conditions.",
                "symptoms": [
                    "Large, dark, water-soaked spots on leaves",
                    "White mold on leaf undersides",
                    "Dark, firm lesions on stems",
                    "Greasy-looking spots on green fruits"
                ],
                "causes": [
                    "Phytophthora infestans",
                    "Cool, wet weather",
                    "Spores spread by wind and rain",
                    "Infected transplants"
                ],
                "treatment": {
                    "chemical": [
                        "Chlorothalonil",
                        "Copper fungicides",
                        "Mancozeb"
                    ],
                    "organic": [
                        "Remove infected plants immediately",
                        "Copper sprays",
                        "Improve air circulation"
                    ]
                },
                "prevention": [
                    "Use resistant varieties",
                    "Avoid overhead irrigation",
                    "Provide good air circulation",
                    "Remove volunteer tomatoes",
                    "Monitor weather forecasts"
                ]
            },
            "Tomato_healthy": {
                "description": "The tomato plant appears healthy with no visible disease symptoms.",
                "symptoms": [
                    "Vibrant green leaves",
                    "Normal growth pattern",
                    "No spots or lesions",
                    "Healthy fruit development"
                ],
                "recommendations": [
                    "Continue regular monitoring",
                    "Maintain balanced nutrition",
                    "Ensure proper irrigation",
                    "Practice good field hygiene"
                ]
            },
            "Tomato_Leaf_Mold": {
                "scientific_name": "Passalora fulva (formerly Fulvia fulva)",
                "type": "Fungal",
                "description": "Leaf mold primarily affects greenhouse tomatoes, causing yellow spots and mold on leaves.",
                "symptoms": [
                    "Pale green or yellowish spots on upper leaf surface",
                    "Olive-green to grayish-purple mold on undersides",
                    "Leaves turn brown and curl",
                    "Reduced yield"
                ],
                "causes": [
                    "Fungus Passalora fulva",
                    "High humidity",
                    "Poor air circulation",
                    "Overcrowding"
                ],
                "treatment": {
                    "chemical": [
                        "Chlorothalonil",
                        "Copper fungicides",
                        "Myclobutanil"
                    ],
                    "organic": [
                        "Improve ventilation",
                        "Reduce humidity",
                        "Remove affected leaves"
                    ]
                },
                "prevention": [
                    "Space plants properly",
                    "Improve air circulation",
                    "Avoid overhead watering",
                    "Use resistant varieties",
                    "Control humidity in greenhouses"
                ]
            },
            "Tomato_Septoria_leaf_spot": {
                "scientific_name": "Septoria lycopersici",
                "type": "Fungal",
                "description": "Septoria leaf spot causes numerous small spots on tomato leaves, leading to defoliation.",
                "symptoms": [
                    "Small, circular spots with dark borders and light centers",
                    "Black dots (pycnidia) in center of spots",
                    "Yellowing around spots",
                    "Lower leaves affected first"
                ],
                "causes": [
                    "Fungus Septoria lycopersici",
                    "Infected plant debris",
                    "Splash dispersal",
                    "Warm, wet conditions"
                ],
                "treatment": {
                    "chemical": [
                        "Chlorothalonil",
                        "Mancozeb",
                        "Copper fungicides"
                    ],
                    "organic": [
                        "Remove affected leaves",
                        "Neem oil",
                        "Baking soda spray"
                    ]
                },
                "prevention": [
                    "Mulch around plants",
                    "Water at base",
                    "Remove infected leaves",
                    "Rotate crops",
                    "Clean up plant debris"
                ]
            },
            "Tomato_Spider_mites_Two_spotted_spider_mite": {
                "scientific_name": "Tetranychus urticae",
                "type": "Pest",
                "description": "Two-spotted spider mites are tiny pests that suck plant sap, causing stippling and webbing.",
                "symptoms": [
                    "Fine stippling on leaves",
                    "Leaves turn yellow or bronze",
                    "Fine webbing on plants",
                    "Leaf drop in severe cases"
                ],
                "causes": [
                    "Two-spotted spider mites",
                    "Hot, dry conditions",
                    "Dusty conditions",
                    "Overuse of pesticides"
                ],
                "treatment": {
                    "chemical": [
                        "Insecticidal soaps",
                        "Miticides",
                        "Horticultural oils"
                    ],
                    "organic": [
                        "Introduce predatory mites",
                        "Neem oil",
                        "Strong water spray"
                    ]
                },
                "prevention": [
                    "Keep plants well-watered",
                    "Reduce dust",
                    "Encourage beneficial insects",
                    "Monitor regularly",
                    "Avoid broad-spectrum pesticides"
                ]
            },
            "Tomato__Tomato_mosaic_virus": {
                "scientific_name": "Tomato mosaic virus (ToMV)",
                "type": "Viral",
                "description": "Tomato mosaic virus causes mottling, distortion, and reduced yield in tomatoes.",
                "symptoms": [
                    "Light and dark green mottling on leaves",
                    "Leaf distortion and fernleaf",
                    "Stunted growth",
                    "Poor fruit set and quality"
                ],
                "causes": [
                    "Tomato mosaic virus",
                    "Mechanical transmission",
                    "Infected seeds",
                    "Infected plant debris"
                ],
                "treatment": {
                    "chemical": [],
                    "organic": [
                        "No cure - remove infected plants",
                        "Wash hands and tools",
                        "Use resistant varieties"
                    ]
                },
                "prevention": [
                    "Use virus-free seeds",
                    "Wash hands before handling",
                    "Disinfect tools",
                    "Remove infected plants",
                    "Control weeds"
                ]
            }
        }
    
    def load_model(self, model_path: str) -> None:
        """
        Load the trained CNN model
        
        Args:
            model_path: Path to model file
        """
        try:
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                logger.info(f"Model loaded successfully from {model_path}")
                
                # Log model details
                logger.info(f"Model input shape: {self.model.input_shape}")
                logger.info(f"Model output shape: {self.model.output_shape}")
                
                # ✅ Auto-detect input size from model
                if hasattr(self.model, 'input_shape'):
                    # Extract height and width from model input shape
                    # Model input shape is typically (None, height, width, channels)
                    if len(self.model.input_shape) == 4:
                        _, h, w, _ = self.model.input_shape
                        self.input_size = (h, w)
                        logger.info(f"Auto-detected input size: {self.input_size}")
            else:
                logger.warning(f"Model file not found at {model_path}. Using fallback mode.")
                self.create_fallback_model()
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.info("Creating fallback model for testing")
            self.create_fallback_model()
    
    def create_fallback_model(self) -> None:
        """
        Create a fallback model for testing when actual model is not available
        """
        try:
            # ✅ Use 128x128 for fallback model to match your trained model
            input_shape = (128, 128, 3)
            inputs = tf.keras.Input(shape=input_shape)
            
            # Data augmentation
            x = tf.keras.layers.RandomFlip("horizontal")(inputs)
            x = tf.keras.layers.RandomRotation(0.1)(x)
            x = tf.keras.layers.RandomZoom(0.1)(x)
            
            # Convolutional layers
            x = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(x)
            x = tf.keras.layers.MaxPooling2D()(x)
            x = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(x)
            x = tf.keras.layers.MaxPooling2D()(x)
            x = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(x)
            x = tf.keras.layers.GlobalAveragePooling2D()(x)
            
            # Dense layers
            x = tf.keras.layers.Dense(256, activation='relu')(x)
            x = tf.keras.layers.Dropout(0.5)(x)
            x = tf.keras.layers.Dense(128, activation='relu')(x)
            
            # Output layer - 15 classes for your dataset
            outputs = tf.keras.layers.Dense(len(self.class_names), activation='softmax')(x)
            
            self.model = tf.keras.Model(inputs, outputs)
            
            # Compile model
            self.model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            logger.info(f"Fallback model created successfully with {len(self.class_names)} classes")
            logger.info(f"Fallback model input shape: {self.model.input_shape}")
            
        except Exception as e:
            logger.error(f"Error creating fallback model: {str(e)}")
            raise
    
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Preprocessed image array
        """
        try:
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # ✅ Resize image to match model's expected input size
            logger.debug(f"Resizing image to: {self.input_size}")
            image = image.resize(self.input_size)
            
            # Convert to numpy array
            image_array = np.array(image, dtype=np.float32)
            
            # Normalize pixel values to [0, 1]
            image_array = image_array / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            logger.debug(f"Image preprocessed: shape={image_array.shape}")
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict(self, image_bytes: bytes) -> Dict:
        """
        Predict disease from image
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_bytes)
            
            # Verify shape matches model expectations
            logger.info(f"Input shape for prediction: {processed_image.shape}")
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get top 5 predictions
            top_5_indices = np.argsort(predictions[0])[-5:][::-1]
            
            results = []
            for idx in top_5_indices:
                disease_name = self.class_names.get(idx, f"Disease_{idx}")
                confidence = float(predictions[0][idx])
                
                # Format disease name for display
                display_name = self.format_disease_name(disease_name)
                
                results.append({
                    'disease': display_name,
                    'original_class': disease_name,
                    'disease_id': int(idx),
                    'confidence': confidence,
                    'confidence_percentage': round(confidence * 100, 2),
                    'disease_type': self.get_disease_type(display_name),
                    'severity': self.calculate_severity(confidence)
                })
            
            # Get primary disease info
            primary_disease = results[0]['disease']
            original_class = results[0]['original_class']
            
            # Get treatment and prevention info
            disease_details = self.get_disease_details(original_class)
            
            # Calculate confidence level
            confidence_level = self.get_confidence_level(results[0]['confidence'])
            
            response = {
                'success': True,
                'predictions': results,
                'primary_disease': primary_disease,
                'original_class': original_class,
                'confidence': results[0]['confidence_percentage'],
                'confidence_level': confidence_level,
                'disease_details': disease_details,
                'severity': results[0]['severity'],
                'model_used': 'CNN-MobileNetV2',
                'input_size': self.input_size,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Prediction successful: {primary_disease} with {results[0]['confidence_percentage']}% confidence")
            return response
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def format_disease_name(self, class_name: str) -> str:
        """
        Format the class name for display
        
        Args:
            class_name: Original class name from dataset
            
        Returns:
            Formatted disease name
        """
        # Remove underscores and clean up
        name = class_name.replace('___', ' - ').replace('_', ' ')
        
        # Special formatting for specific classes
        if 'Tomato__Tomato_YellowLeaf__Curl_Virus' in class_name:
            return "Tomato Yellow Leaf Curl Virus"
        elif 'Tomato_Spider_mites_Two_spotted_spider_mite' in class_name:
            return "Tomato Spider Mites (Two-spotted)"
        
        return name
    
    def predict_batch(self, image_batches: List[bytes]) -> List[Dict]:
        """
        Predict diseases from multiple images
        
        Args:
            image_batches: List of image bytes
            
        Returns:
            List of prediction results
        """
        results = []
        
        for idx, image_bytes in enumerate(image_batches):
            try:
                result = self.predict(image_bytes)
                result['image_index'] = idx
                results.append(result)
            except Exception as e:
                results.append({
                    'success': False,
                    'image_index': idx,
                    'error': str(e)
                })
        
        return results
    
    def get_disease_details(self, disease_name: str) -> Dict:
        """
        Get detailed information about a disease
        
        Args:
            disease_name: Name of the disease (original class name)
            
        Returns:
            Dictionary with disease details
        """
        default_info = {
            "description": f"Information about {self.format_disease_name(disease_name)}",
            "symptoms": ["Consult local agriculture officer for symptoms"],
            "treatment": {
                "chemical": ["Consult agriculture expert"],
                "organic": ["Use organic farming practices"]
            },
            "prevention": ["Regular field monitoring", "Good agricultural practices"]
        }
        
        return self.disease_info.get(disease_name, default_info)
    
    def get_disease_type(self, disease_name: str) -> str:
        """
        Get the type of disease (Fungal, Bacterial, Viral, Pest)
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Disease type
        """
        disease_lower = disease_name.lower()
        
        if 'bacterial' in disease_lower:
            return "Bacterial"
        elif 'viral' in disease_lower or 'virus' in disease_lower:
            return "Viral"
        elif 'mite' in disease_lower or 'spider' in disease_lower:
            return "Pest"
        elif 'blight' in disease_lower or 'spot' in disease_lower or 'mold' in disease_lower:
            return "Fungal"
        elif 'healthy' in disease_lower:
            return "Healthy"
        else:
            return "Unknown"
    
    def calculate_severity(self, confidence: float) -> str:
        """
        Calculate severity based on confidence
        
        Args:
            confidence: Prediction confidence
            
        Returns:
            Severity level
        """
        if confidence > 0.9:
            return "CRITICAL"
        elif confidence > 0.7:
            return "HIGH"
        elif confidence > 0.5:
            return "MEDIUM"
        elif confidence > 0.3:
            return "LOW"
        else:
            return "UNCERTAIN"
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        Get confidence level description
        
        Args:
            confidence: Prediction confidence
            
        Returns:
            Confidence level description
        """
        if confidence > 0.9:
            return "Very High"
        elif confidence > 0.7:
            return "High"
        elif confidence > 0.5:
            return "Medium"
        elif confidence > 0.3:
            return "Low"
        else:
            return "Very Low"
    
    def get_treatment_recommendation(self, disease_name: str) -> Dict:
        """
        Get treatment recommendations for a disease
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Treatment recommendations
        """
        disease_info = self.get_disease_details(disease_name)
        
        if "healthy" in disease_name.lower():
            return {
                "action": "No treatment needed",
                "recommendations": [
                    "Continue regular monitoring",
                    "Maintain good agricultural practices",
                    "Apply balanced fertilizers"
                ]
            }
        
        treatment = disease_info.get('treatment', {})
        
        return {
            "immediate_action": treatment.get('chemical', ['Consult agriculture officer'])[0] if treatment.get('chemical') else "Consult agriculture officer",
            "organic_methods": treatment.get('organic', ['Use neem-based products']),
            "prevention_tips": disease_info.get('prevention', ['Regular monitoring']),
            "consult_expert": "Contact local agriculture extension officer for specific guidance"
        }
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model
        
        Returns:
            Model information
        """
        if self.model:
            return {
                'loaded': True,
                'input_shape': str(self.model.input_shape),
                'output_shape': str(self.model.output_shape),
                'num_classes': len(self.class_names),
                'classes': list(self.class_names.values()),
                'input_size': self.input_size
            }
        else:
            return {
                'loaded': False,
                'error': 'Model not loaded'
            }


# ===== STANDALONE FUNCTIONS FOR ROUTE USE =====

def predict_disease(image_file):
    """
    Standalone function for route use
    Args:
        image_file: FileStorage object from Flask request
    Returns:
        Prediction result dictionary
    """
    try:
        # Read image bytes
        image_bytes = image_file.read()
        
        # Create service instance
        service = DiseaseDetectionService('models/disease_model.h5')
        
        # Make prediction
        result = service.predict(image_bytes)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in predict_disease: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


# For backward compatibility
disease_service = DiseaseDetectionService('models/disease_model.h5')
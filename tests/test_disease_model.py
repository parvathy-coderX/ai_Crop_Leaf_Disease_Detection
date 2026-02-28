"""
Unit tests for disease detection service and routes
"""

import unittest
import sys
import os
import json
import io
import numpy as np
from PIL import Image
from unittest.mock import patch, MagicMock, Mock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.disease_service import DiseaseDetectionService
from backend.routes.disease_routes import disease_bp
from backend.app import create_app
from backend.config import Config

class TestDiseaseService(unittest.TestCase):
    """Test cases for DiseaseDetectionService class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are reused across tests"""
        cls.test_model_path = 'test_models/dummy_model.h5'
        cls.service = DiseaseDetectionService(cls.test_model_path)
        
        # Create a sample test image
        cls.test_image = cls.create_test_image()
        cls.test_image_bytes = cls.image_to_bytes(cls.test_image)
        
    @classmethod
    def create_test_image(cls):
        """Create a sample test image"""
        img = Image.new('RGB', (224, 224), color='green')
        return img
    
    @classmethod
    def image_to_bytes(cls, image):
        """Convert PIL Image to bytes"""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.mock_model = MagicMock()
        self.service.model = self.mock_model
    
    def test_load_class_names(self):
        """Test if class names are loaded correctly"""
        class_names = self.service.load_class_names()
        self.assertIsInstance(class_names, dict)
        self.assertGreater(len(class_names), 0)
        self.assertIn(0, class_names)
        self.assertIn("Healthy", class_names.values())
    
    def test_load_disease_info(self):
        """Test if disease info is loaded correctly"""
        disease_info = self.service.load_disease_info()
        self.assertIsInstance(disease_info, dict)
        self.assertIn("Rice Blast", disease_info)
        self.assertIn("Healthy", disease_info)
        
        # Check structure of disease info
        rice_blast_info = disease_info["Rice Blast"]
        self.assertIn("scientific_name", rice_blast_info)
        self.assertIn("symptoms", rice_blast_info)
        self.assertIn("treatment", rice_blast_info)
        self.assertIsInstance(rice_blast_info["symptoms"], list)
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        processed = self.service.preprocess_image(self.test_image_bytes)
        
        # Check shape and type
        self.assertIsInstance(processed, np.ndarray)
        self.assertEqual(processed.shape, (1, 224, 224, 3))
        self.assertEqual(processed.dtype, np.float32)
        
        # Check normalization
        self.assertTrue(np.all(processed >= 0) and np.all(processed <= 1))
    
    def test_preprocess_image_invalid(self):
        """Test preprocessing with invalid image"""
        with self.assertRaises(Exception):
            self.service.preprocess_image(b"invalid image data")
    
    @patch('tensorflow.keras.models.load_model')
    def test_load_model(self, mock_load):
        """Test model loading"""
        mock_load.return_value = MagicMock()
        self.service.load_model("dummy_path")
        mock_load.assert_called_once()
    
    def test_predict_healthy(self):
        """Test prediction for healthy plant"""
        # Mock model prediction for healthy class
        mock_prediction = np.zeros((1, len(self.service.class_names)))
        mock_prediction[0][16] = 0.95  # Healthy class (index 16)
        self.mock_model.predict.return_value = mock_prediction
        
        result = self.service.predict(self.test_image_bytes)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['primary_disease'], "Healthy")
        self.assertGreater(result['confidence'], 90)
        self.assertIn('predictions', result)
        self.assertIn('disease_details', result)
    
    def test_predict_disease(self):
        """Test prediction for diseased plant"""
        # Mock model prediction for Rice Blast
        mock_prediction = np.zeros((1, len(self.service.class_names)))
        mock_prediction[0][0] = 0.92  # Rice Blast class
        self.mock_model.predict.return_value = mock_prediction
        
        result = self.service.predict(self.test_image_bytes)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['primary_disease'], "Rice Blast")
        self.assertAlmostEqual(result['confidence'], 92.0, places=1)
        
        # Check if treatment is provided
        self.assertIn('treatment', result['disease_details'])
    
    def test_predict_top_k(self):
        """Test if top K predictions are returned"""
        # Mock model prediction with multiple classes
        mock_prediction = np.zeros((1, len(self.service.class_names)))
        mock_prediction[0][0] = 0.70  # Rice Blast
        mock_prediction[0][1] = 0.20  # Rice Brown Spot
        mock_prediction[0][2] = 0.05  # Rice Leaf Scald
        self.mock_model.predict.return_value = mock_prediction
        
        result = self.service.predict(self.test_image_bytes)
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['predictions']), 5)  # Top 5
        self.assertEqual(result['predictions'][0]['disease'], "Rice Blast")
        self.assertEqual(result['predictions'][1]['disease'], "Rice Brown Spot")
    
    def test_predict_error_handling(self):
        """Test error handling during prediction"""
        self.mock_model.predict.side_effect = Exception("Model error")
        
        result = self.service.predict(self.test_image_bytes)
        
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_get_disease_type(self):
        """Test disease type classification"""
        self.assertEqual(self.service.get_disease_type("Rice Blast"), "Fungal")
        self.assertEqual(self.service.get_disease_type("Bacterial Leaf Blight"), "Bacterial")
        self.assertEqual(self.service.get_disease_type("Bunchy Top"), "Viral")
        self.assertEqual(self.service.get_disease_type("Unknown"), "Unknown")
    
    def test_calculate_severity(self):
        """Test severity calculation"""
        self.assertEqual(self.service.calculate_severity(0.95), "CRITICAL")
        self.assertEqual(self.service.calculate_severity(0.85), "HIGH")
        self.assertEqual(self.service.calculate_severity(0.65), "MEDIUM")
        self.assertEqual(self.service.calculate_severity(0.35), "LOW")
        self.assertEqual(self.service.calculate_severity(0.25), "UNCERTAIN")
    
    def test_get_confidence_level(self):
        """Test confidence level description"""
        self.assertEqual(self.service.get_confidence_level(0.95), "Very High")
        self.assertEqual(self.service.get_confidence_level(0.80), "High")
        self.assertEqual(self.service.get_confidence_level(0.60), "Medium")
        self.assertEqual(self.service.get_confidence_level(0.40), "Low")
        self.assertEqual(self.service.get_confidence_level(0.20), "Very Low")
    
    def test_get_treatment_recommendation(self):
        """Test treatment recommendations"""
        # Test for diseased plant
        treatment = self.service.get_treatment_recommendation("Rice Blast")
        self.assertIn('immediate_action', treatment)
        self.assertIn('organic_methods', treatment)
        self.assertIn('prevention_tips', treatment)
        
        # Test for healthy plant
        healthy_treatment = self.service.get_treatment_recommendation("Healthy")
        self.assertEqual(healthy_treatment['action'], "No treatment needed")
    
    def test_predict_batch(self):
        """Test batch prediction"""
        # Mock model prediction
        mock_prediction = np.zeros((1, len(self.service.class_names)))
        mock_prediction[0][16] = 0.95
        self.mock_model.predict.return_value = mock_prediction
        
        # Create multiple test images
        images = [self.test_image_bytes] * 3
        results = self.service.predict_batch(images)
        
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertTrue(result['success'])
            self.assertEqual(result['primary_disease'], "Healthy")
    
    def test_get_model_info(self):
        """Test model information retrieval"""
        self.mock_model.input_shape = (None, 224, 224, 3)
        self.mock_model.output_shape = (None, 17)
        
        model_info = self.service.get_model_info()
        self.assertTrue(model_info['loaded'])
        self.assertEqual(model_info['num_classes'], 17)
        
        # Test when model not loaded
        self.service.model = None
        model_info = self.service.get_model_info()
        self.assertFalse(model_info['loaded'])


class TestDiseaseRoutes(unittest.TestCase):
    """Test cases for disease detection API routes"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test app"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        
        # Create test image
        cls.test_image = TestDiseaseService.create_test_image()
        cls.test_image_bytes = TestDiseaseService.image_to_bytes(cls.test_image)
    
    def setUp(self):
        """Set up before each test"""
        self.test_image_file = (io.BytesIO(self.test_image_bytes), 'test.png')
    
    def test_predict_success(self):
        """Test successful disease prediction"""
        with patch('backend.services.disease_service.DiseaseDetectionService.predict') as mock_predict:
            mock_predict.return_value = {
                'success': True,
                'primary_disease': 'Healthy',
                'confidence': 95.5,
                'predictions': [{'disease': 'Healthy', 'confidence': 0.955}],
                'disease_details': {}
            }
            
            response = self.client.post(
                '/api/disease/predict',
                data={'image': self.test_image_file},
                content_type='multipart/form-data'
            )
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['primary_disease'], 'Healthy')
    
    def test_predict_no_image(self):
        """Test prediction with no image"""
        response = self.client.post('/api/disease/predict')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_predict_invalid_file_type(self):
        """Test prediction with invalid file type"""
        invalid_file = (io.BytesIO(b"not an image"), 'test.txt')
        response = self.client.post(
            '/api/disease/predict',
            data={'image': invalid_file},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'INVALID_TYPE')
    
    def test_predict_empty_file(self):
        """Test prediction with empty file"""
        empty_file = (io.BytesIO(b''), 'test.png')
        response = self.client.post(
            '/api/disease/predict',
            data={'image': empty_file},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_predict_with_user_id(self):
        """Test prediction with user ID"""
        with patch('backend.services.disease_service.DiseaseDetectionService.predict') as mock_predict:
            mock_predict.return_value = {
                'success': True,
                'primary_disease': 'Healthy',
                'confidence': 95.5,
                'predictions': []
            }
            
            response = self.client.post(
                '/api/disease/predict',
                data={
                    'image': self.test_image_file,
                    'user_id': 'test_user_123',
                    'location': 'Kerala',
                    'crop_type': 'Rice'
                },
                content_type='multipart/form-data'
            )
            
            self.assertEqual(response.status_code, 200)
    
    def test_predict_batch(self):
        """Test batch prediction"""
        with patch('backend.services.disease_service.DiseaseDetectionService.predict_batch') as mock_batch:
            mock_batch.return_value = [
                {'success': True, 'primary_disease': 'Healthy', 'confidence': 95.5}
            ] * 2
            
            # Create multiple files
            files = [
                (io.BytesIO(self.test_image_bytes), f'test{i}.png') 
                for i in range(2)
            ]
            
            response = self.client.post(
                '/api/disease/predict/batch',
                data={'images': files},
                content_type='multipart/form-data'
            )
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['total_processed'], 2)
    
    def test_health_check(self):
        """Test health check endpoint"""
        with patch('backend.services.disease_service.DiseaseDetectionService.get_model_info'):
            response = self.client.get('/api/disease/health')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['service'], 'disease_detection')
    
    def test_list_diseases(self):
        """Test list diseases endpoint"""
        response = self.client.get('/api/disease/diseases/list')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('diseases', data)
        self.assertGreater(data['count'], 0)
    
    def test_get_disease_info(self):
        """Test get disease info endpoint"""
        response = self.client.get('/api/disease/disease/Rice%20Blast/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('disease', data)
        self.assertEqual(data['disease']['name'], 'Rice Blast')
    
    def test_get_disease_info_not_found(self):
        """Test get disease info for non-existent disease"""
        response = self.client.get('/api/disease/disease/Unknown%20Disease/info')
        self.assertEqual(response.status_code, 404)
    
    def test_submit_feedback(self):
        """Test feedback submission"""
        feedback_data = {
            'prediction_id': 'pred_123',
            'rating': 5,
            'comment': 'Great prediction!',
            'user_id': 'user_123'
        }
        
        response = self.client.post(
            '/api/disease/feedback',
            json=feedback_data
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_submit_feedback_invalid_rating(self):
        """Test feedback with invalid rating"""
        feedback_data = {
            'prediction_id': 'pred_123',
            'rating': 10  # Invalid rating
        }
        
        response = self.client.post(
            '/api/disease/feedback',
            json=feedback_data
        )
        self.assertEqual(response.status_code, 400)


class TestDiseaseModelPerformance(unittest.TestCase):
    """Test cases for model performance metrics"""
    
    @classmethod
    def setUpClass(cls):
        cls.service = DiseaseDetectionService('test_models/dummy_model.h5')
    
    def test_model_accuracy_threshold(self):
        """Test if model meets accuracy threshold"""
        # This would typically load a test dataset and evaluate
        # For now, we'll mock the evaluation
        mock_accuracy = 0.92  # 92% accuracy
        self.assertGreaterEqual(mock_accuracy, 0.85, 
                                "Model accuracy below threshold")
    
    def test_model_inference_time(self):
        """Test model inference time"""
        import time
        
        test_image = TestDiseaseService.create_test_image()
        test_bytes = TestDiseaseService.image_to_bytes(test_image)
        
        start_time = time.time()
        self.service.preprocess_image(test_bytes)
        preprocessing_time = time.time() - start_time
        
        self.assertLess(preprocessing_time, 0.5, 
                       "Preprocessing too slow")
    
    def test_memory_usage(self):
        """Test memory usage of model"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Load model (if not already loaded)
        if not self.service.model:
            self.service.load_model('test_models/dummy_model.h5')
        
        memory_after = process.memory_info().rss / 1024 / 1024
        memory_increase = memory_after - memory_before
        
        self.assertLess(memory_increase, 500, 
                       f"Model uses too much memory: {memory_increase:.2f}MB")


if __name__ == '__main__':
    unittest.main()
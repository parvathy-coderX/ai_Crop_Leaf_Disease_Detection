"""
Unit tests for weather service and risk prediction
"""

import unittest
import sys
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, Mock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.weather_service import WeatherService
from backend.routes.weather_routes import weather_bp
from backend.app import create_app
from backend.config import Config
from backend.utils.risk_calculator import calculate_risk_score

class TestWeatherService(unittest.TestCase):
    """Test cases for WeatherService class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.service = WeatherService()
        cls.test_lat = 10.5276
        cls.test_lon = 76.2144
        cls.test_crop = 'rice'
        
    def setUp(self):
        """Set up before each test"""
        self.service.api_key = 'test_api_key'
    
    def test_init(self):
        """Test service initialization"""
        self.assertIsNotNone(self.service.api_key)
        self.assertIsNotNone(self.service.crop_thresholds)
        self.assertIn('rice', self.service.crop_thresholds)
        self.assertIn('wheat', self.service.crop_thresholds)
    
    def test_crop_thresholds_structure(self):
        """Test crop thresholds structure"""
        rice_thresholds = self.service.crop_thresholds['rice']
        
        required_keys = ['temp_min', 'temp_max', 'temp_optimal', 
                        'humidity_min', 'humidity_max', 'humidity_optimal',
                        'rain_optimal', 'disease_risk_humidity']
        
        for key in required_keys:
            self.assertIn(key, rice_thresholds)
        
        # Check optimal ranges
        self.assertEqual(len(rice_thresholds['temp_optimal']), 2)
        self.assertLess(rice_thresholds['temp_optimal'][0], 
                       rice_thresholds['temp_optimal'][1])
    
    @patch('requests.get')
    def test_get_current_weather_success(self, mock_get):
        """Test successful weather API call"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {
                'temp': 28.5,
                'feels_like': 30.2,
                'temp_min': 26.0,
                'temp_max': 32.0,
                'humidity': 75,
                'pressure': 1012
            },
            'weather': [{
                'main': 'Clouds',
                'description': 'scattered clouds',
                'icon': '03d'
            }],
            'wind': {
                'speed': 3.6,
                'deg': 180
            },
            'clouds': {
                'all': 40
            },
            'visibility': 10000,
            'name': 'Thrissur',
            'sys': {
                'country': 'IN',
                'sunrise': 1706924400,
                'sunset': 1706965200
            },
            'timezone': 19800
        }
        mock_get.return_value = mock_response
        
        weather_data = self.service.get_current_weather(self.test_lat, self.test_lon)
        
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['temperature'], 28.5)
        self.assertEqual(weather_data['humidity'], 75)
        self.assertEqual(weather_data['city_name'], 'Thrissur')
        self.assertEqual(weather_data['country'], 'IN')
    
    @patch('requests.get')
    def test_get_current_weather_fallback(self, mock_get):
        """Test fallback when API fails"""
        mock_get.side_effect = Exception("API Error")
        
        weather_data = self.service.get_current_weather(self.test_lat, self.test_lon)
        
        self.assertIsNotNone(weather_data)
        self.assertTrue(weather_data.get('is_fallback', False))
        self.assertIn('temperature', weather_data)
    
    @patch('requests.get')
    def test_get_forecast_success(self, mock_get):
        """Test successful forecast API call"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'list': [
                {
                    'dt_txt': '2024-01-15 12:00:00',
                    'main': {'temp': 30, 'humidity': 70},
                    'weather': [{'main': 'Clear'}],
                    'wind': {'speed': 3.5}
                } for _ in range(8)  # 8 periods for one day
            ]
        }
        mock_get.return_value = mock_response
        
        forecast = self.service.get_forecast(self.test_lat, self.test_lon, days=1)
        
        self.assertIsNotNone(forecast)
        self.assertEqual(len(forecast), 1)
        self.assertIn('temperature', forecast[0])
        self.assertIn('humidity', forecast[0])
    
    @patch('requests.get')
    def test_predict_disease_risk(self, mock_get):
        """Test disease risk prediction"""
        # Mock weather data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 32, 'humidity': 85},
            'weather': [{'main': 'Clouds'}],
            'wind': {'speed': 3.6},
            'name': 'Test City'
        }
        mock_get.return_value = mock_response
        
        risk_assessment = self.service.predict_disease_risk(
            self.test_lat, self.test_lon, 'rice'
        )
        
        self.assertIsNotNone(risk_assessment)
        self.assertIn('risk_level', risk_assessment)
        self.assertIn('risk_score', risk_assessment)
        self.assertIn('risk_factors', risk_assessment)
        self.assertIn('current_weather', risk_assessment)
        self.assertIn('recommendation', risk_assessment)
    
    def test_risk_score_calculation_high(self):
        """Test high risk score calculation"""
        weather = {
            'temperature': 32,
            'humidity': 85,
            'rainfall': 25
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertEqual(risk['risk_level'], 'HIGH')
        self.assertGreater(risk['risk_score'], 70)
        self.assertGreater(len(risk['risk_factors']), 0)
    
    def test_risk_score_calculation_medium(self):
        """Test medium risk score calculation"""
        weather = {
            'temperature': 28,
            'humidity': 72,
            'rainfall': 15
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertEqual(risk['risk_level'], 'MEDIUM')
        self.assertGreaterEqual(risk['risk_score'], 40)
        self.assertLess(risk['risk_score'], 70)
    
    def test_risk_score_calculation_low(self):
        """Test low risk score calculation"""
        weather = {
            'temperature': 25,
            'humidity': 65,
            'rainfall': 5
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertEqual(risk['risk_level'], 'LOW')
        self.assertLess(risk['risk_score'], 40)
    
    def test_predict_likely_diseases(self):
        """Test disease prediction based on weather"""
        weather = {
            'temperature': 32,
            'humidity': 85,
            'rainfall': 20
        }
        
        diseases = self.service.predict_likely_diseases(
            weather, 'rice', self.service.crop_thresholds['rice']
        )
        
        self.assertIsInstance(diseases, list)
        if diseases:  # May be empty if no conditions met
            self.assertIn('disease', diseases[0])
            self.assertIn('probability', diseases[0])
    
    def test_get_fallback_weather(self):
        """Test fallback weather data generation"""
        fallback = self.service.get_fallback_weather(self.test_lat, self.test_lon)
        
        self.assertIsNotNone(fallback)
        self.assertTrue(fallback.get('is_fallback', False))
        self.assertIn('temperature', fallback)
        self.assertIn('humidity', fallback)
    
    def test_get_fallback_forecast(self):
        """Test fallback forecast generation"""
        forecast = self.service.get_fallback_forecast(days=3)
        
        self.assertEqual(len(forecast), 3)
        for day in forecast:
            self.assertIn('date', day)
            self.assertIn('temperature', day)
            self.assertTrue(day.get('is_fallback', False))
    
    def test_different_crop_thresholds(self):
        """Test thresholds for different crops"""
        crops = ['rice', 'wheat', 'cotton', 'sugarcane', 'banana', 'coconut']
        
        for crop in crops:
            thresholds = self.service.crop_thresholds.get(crop)
            self.assertIsNotNone(thresholds, f"Missing thresholds for {crop}")
            self.assertIn('temp_min', thresholds)
            self.assertIn('temp_max', thresholds)
    
    @patch('requests.get')
    def test_ml_prediction_integration(self, mock_get):
        """Test integration with ML model"""
        # Mock ML model
        mock_model = MagicMock()
        mock_model.predict_proba.return_value = np.array([[0.2, 0.3, 0.5]])
        self.service.model = mock_model
        
        # Mock weather API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 30, 'humidity': 80},
            'weather': [{'main': 'Clouds'}]
        }
        mock_get.return_value = mock_response
        
        risk = self.service.predict_disease_risk(self.test_lat, self.test_lon, 'rice')
        
        self.assertIn('ml_prediction', risk)
        self.assertEqual(len(risk['ml_prediction']), 3)


class TestWeatherRoutes(unittest.TestCase):
    """Test cases for weather API routes"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test app"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        
    def test_get_weather_risk_success(self):
        """Test successful risk assessment"""
        with patch('backend.services.weather_service.WeatherService.predict_disease_risk') as mock_predict:
            mock_predict.return_value = {
                'risk_level': 'MEDIUM',
                'risk_score': 65,
                'risk_factors': ['High humidity'],
                'current_weather': {'temperature': 30, 'humidity': 80},
                'forecast': [],
                'recommendation': 'Monitor crops'
            }
            
            response = self.client.post('/api/weather/risk', json={
                'lat': 10.5276,
                'lon': 76.2144,
                'crop_type': 'rice'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['risk_level'], 'MEDIUM')
    
    def test_get_weather_risk_missing_params(self):
        """Test risk assessment with missing parameters"""
        response = self.client.post('/api/weather/risk', json={
            'lat': 10.5276
            # Missing lon and crop_type
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'MISSING_FIELD')
    
    def test_get_weather_risk_invalid_crop(self):
        """Test risk assessment with invalid crop type"""
        response = self.client.post('/api/weather/risk', json={
            'lat': 10.5276,
            'lon': 76.2144,
            'crop_type': 'invalid_crop'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'INVALID_CROP')
        self.assertIn('suggestions', data)
    
    def test_get_weather_risk_invalid_coords(self):
        """Test risk assessment with invalid coordinates"""
        response = self.client.post('/api/weather/risk', json={
            'lat': 1000,  # Invalid latitude
            'lon': 76.2144,
            'crop_type': 'rice'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], 'INVALID_COORDS')
    
    def test_get_current_weather(self):
        """Test current weather endpoint"""
        with patch('backend.services.weather_service.WeatherService.get_current_weather') as mock_weather:
            mock_weather.return_value = {
                'temperature': 30,
                'humidity': 75,
                'city_name': 'Thrissur'
            }
            
            response = self.client.get('/api/weather/current?lat=10.5276&lon=76.2144')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['data']['temperature'], 30)
    
    def test_get_current_weather_missing_params(self):
        """Test current weather with missing parameters"""
        response = self.client.get('/api/weather/current')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
    
    def test_get_forecast(self):
        """Test forecast endpoint"""
        with patch('backend.services.weather_service.WeatherService.get_forecast') as mock_forecast:
            mock_forecast.return_value = [
                {'date': '2024-01-15', 'temperature': 30, 'humidity': 75}
            ]
            
            response = self.client.get('/api/weather/forecast?lat=10.5276&lon=76.2144&days=3')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertIn('forecast', data['data'])
    
    def test_get_forecast_days_limit(self):
        """Test forecast days limit (max 7)"""
        with patch('backend.services.weather_service.WeatherService.get_forecast') as mock_forecast:
            mock_forecast.return_value = []
            
            response = self.client.get('/api/weather/forecast?lat=10.5276&lon=76.2144&days=10')
            
            # Should limit to 7 days
            mock_forecast.assert_called_with(10.5276, 76.2144, days=7)
    
    def test_get_supported_crops(self):
        """Test supported crops endpoint"""
        response = self.client.get('/api/weather/crops')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)
        self.assertIn('crops', data)
    
    def test_get_weather_alerts(self):
        """Test weather alerts endpoint"""
        with patch('backend.services.weather_service.WeatherService.get_current_weather') as mock_weather, \
             patch('backend.services.weather_service.WeatherService.get_forecast') as mock_forecast:
            
            mock_weather.return_value = {
                'temperature': 42,  # Extreme heat
                'humidity': 80,
                'rainfall': 60
            }
            mock_forecast.return_value = []
            
            response = self.client.post('/api/weather/alerts', json={
                'lat': 10.5276,
                'lon': 76.2144,
                'crop_type': 'rice'
            })
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertGreater(data['alert_count'], 0)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/weather/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['service'], 'weather_service')
        self.assertIn('supported_crops', data)


class TestRiskCalculator(unittest.TestCase):
    """Test cases for risk calculator utility"""
    
    def test_calculate_risk_score_all_factors(self):
        """Test risk score with all factors"""
        weather = {
            'temperature': 38,  # Too high
            'humidity': 90,      # Too high
            'rainfall': 80       # Too high
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertEqual(risk['risk_level'], 'HIGH')
        self.assertGreater(risk['risk_score'], 80)
        self.assertGreater(len(risk['risk_factors']), 2)
    
    def test_calculate_risk_score_edge_cases(self):
        """Test risk score at threshold boundaries"""
        weather = {
            'temperature': 35,  # At max threshold
            'humidity': 80,     # At disease risk threshold
            'rainfall': 20      # Moderate
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertIn(risk['risk_level'], ['MEDIUM', 'HIGH'])
        self.assertIsInstance(risk['risk_score'], float)
    
    def test_calculate_risk_score_different_crops(self):
        """Test risk score for different crops"""
        weather = {
            'temperature': 30,
            'humidity': 75,
            'rainfall': 15
        }
        
        rice_risk = calculate_risk_score(weather, 'rice')
        wheat_risk = calculate_risk_score(weather, 'wheat')
        
        # Different crops should have different risk scores
        self.assertNotEqual(rice_risk['risk_score'], wheat_risk['risk_score'])
    
    def test_risk_factors_generation(self):
        """Test risk factors generation"""
        weather = {
            'temperature': 15,  # Low
            'humidity': 85,     # High
            'rainfall': 60      # High
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertGreater(len(risk['risk_factors']), 0)
        for factor in risk['risk_factors']:
            self.assertIsInstance(factor, str)
            self.assertTrue(len(factor) > 10)
    
    def test_recommendation_generation(self):
        """Test recommendation generation based on risk level"""
        test_cases = [
            ({'temperature': 38, 'humidity': 90, 'rainfall': 80}, 'HIGH', 'immediate'),
            ({'temperature': 30, 'humidity': 75, 'rainfall': 15}, 'MEDIUM', 'monitor'),
            ({'temperature': 25, 'humidity': 60, 'rainfall': 5}, 'LOW', 'continue')
        ]
        
        for weather, expected_level, keyword in test_cases:
            risk = calculate_risk_score(weather, 'rice')
            self.assertEqual(risk['risk_level'], expected_level)
            self.assertIn(keyword, risk['recommendation'].lower())
    
    def test_weather_summary_in_risk(self):
        """Test that weather summary is included in risk assessment"""
        weather = {
            'temperature': 30,
            'humidity': 75,
            'rainfall': 15
        }
        
        risk = calculate_risk_score(weather, 'rice')
        
        self.assertIn('weather_summary', risk)
        self.assertEqual(risk['weather_summary']['temperature'], 30)
        self.assertEqual(risk['weather_summary']['humidity'], 75)
        self.assertEqual(risk['weather_summary']['rainfall'], 15)
    
    def test_risk_score_bounds(self):
        """Test that risk score is bounded between 0 and 100"""
        # Test extreme values
        weather_extreme = {
            'temperature': 50,
            'humidity': 100,
            'rainfall': 200
        }
        risk = calculate_risk_score(weather_extreme, 'rice')
        self.assertLessEqual(risk['risk_score'], 100)
        
        # Test normal values
        weather_normal = {
            'temperature': 25,
            'humidity': 60,
            'rainfall': 5
        }
        risk = calculate_risk_score(weather_normal, 'rice')
        self.assertGreaterEqual(risk['risk_score'], 0)


class TestWeatherModelPerformance(unittest.TestCase):
    """Test cases for weather model performance"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data for performance testing"""
        cls.service = WeatherService()
        cls.test_cases = [
            {'temp': 35, 'humidity': 90, 'rain': 50, 'expected': 'HIGH'},
            {'temp': 30, 'humidity': 80, 'rain': 25, 'expected': 'MEDIUM'},
            {'temp': 25, 'humidity': 65, 'rain': 10, 'expected': 'LOW'},
            {'temp': 15, 'humidity': 95, 'rain': 40, 'expected': 'HIGH'},
            {'temp': 32, 'humidity': 70, 'rain': 5, 'expected': 'MEDIUM'}
        ]
    
    def test_prediction_accuracy(self):
        """Test prediction accuracy against expected values"""
        correct_predictions = 0
        
        for case in self.test_cases:
            weather = {
                'temperature': case['temp'],
                'humidity': case['humidity'],
                'rainfall': case['rain']
            }
            
            risk = calculate_risk_score(weather, 'rice')
            
            if risk['risk_level'] == case['expected']:
                correct_predictions += 1
        
        accuracy = correct_predictions / len(self.test_cases)
        self.assertGreaterEqual(accuracy, 0.8, 
                               f"Accuracy too low: {accuracy:.2%}")
    
    def test_response_time(self):
        """Test API response time"""
        import time
        
        start_time = time.time()
        
        # Simulate multiple predictions
        for _ in range(100):
            weather = {
                'temperature': np.random.uniform(15, 40),
                'humidity': np.random.uniform(40, 100),
                'rainfall': np.random.uniform(0, 100)
            }
            calculate_risk_score(weather, 'rice')
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        
        self.assertLess(avg_time, 0.01, 
                       f"Average response time too high: {avg_time*1000:.2f}ms")
    
    def test_crop_specificity(self):
        """Test that different crops get different risk scores"""
        weather = {
            'temperature': 30,
            'humidity': 80,
            'rainfall': 20
        }
        
        crops = ['rice', 'wheat', 'cotton', 'sugarcane']
        risk_scores = []
        
        for crop in crops:
            risk = calculate_risk_score(weather, crop)
            risk_scores.append(risk['risk_score'])
        
        # Check that not all scores are identical
        self.assertGreater(len(set(risk_scores)), 1)
    
    def test_seasonal_variation(self):
        """Test that risk assessment accounts for seasonal variations"""
        # This test would need season data integration
        # For now, just verify the function exists and returns valid results
        weather = {
            'temperature': 28,
            'humidity': 75,
            'rainfall': 15,
            'season': 'monsoon'
        }
        
        risk = calculate_risk_score(weather, 'rice')
        self.assertIsNotNone(risk['risk_level'])


class TestWeatherAPIEndToEnd(unittest.TestCase):
    """End-to-end tests for weather API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client"""
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_full_workflow(self):
        """Test complete weather risk workflow"""
        # Step 1: Get current weather
        response1 = self.client.get('/api/weather/current?lat=10.5276&lon=76.2144')
        self.assertEqual(response1.status_code, 200)
        
        # Step 2: Get forecast
        response2 = self.client.get('/api/weather/forecast?lat=10.5276&lon=76.2144&days=3')
        self.assertEqual(response2.status_code, 200)
        
        # Step 3: Get risk assessment
        response3 = self.client.post('/api/weather/risk', json={
            'lat': 10.5276,
            'lon': 76.2144,
            'crop_type': 'rice',
            'days_ahead': 3
        })
        self.assertEqual(response3.status_code, 200)
        
        # Step 4: Get weather alerts
        response4 = self.client.post('/api/weather/alerts', json={
            'lat': 10.5276,
            'lon': 76.2144,
            'crop_type': 'rice'
        })
        self.assertEqual(response4.status_code, 200)
    
    def test_error_recovery(self):
        """Test API recovery from errors"""
        # Test with invalid coordinates - should return 400
        response = self.client.post('/api/weather/risk', json={
            'lat': 999,
            'lon': 999,
            'crop_type': 'rice'
        })
        self.assertEqual(response.status_code, 400)
        
        # Test with missing API key - service should use fallback
        with patch.dict('os.environ', {'OPENWEATHER_API_KEY': ''}):
            response = self.client.get('/api/weather/current?lat=10.5276&lon=76.2144')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['data'].get('is_fallback', False))
    
    def test_rate_limiting(self):
        """Test rate limiting (if implemented)"""
        # Make multiple rapid requests
        responses = []
        for _ in range(10):
            response = self.client.get('/api/weather/current?lat=10.5276&lon=76.2144')
            responses.append(response.status_code)
        
        # Should not hit rate limit (or should handle gracefully)
        self.assertTrue(all(code == 200 for code in responses))


def run_weather_tests():
    """Run all weather-related tests"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWeatherService))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWeatherRoutes))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRiskCalculator))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWeatherModelPerformance))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWeatherAPIEndToEnd))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 70)
    print("Running Weather Model Tests")
    print("=" * 70)
    
    result = run_weather_tests()
    
    print("\n" + "=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ All weather tests passed!")
    else:
        print("\n❌ Some tests failed. Check output above.")
"""
Weather data fetching and risk prediction service
Handles API calls to OpenWeatherMap and risk calculations
"""

import requests
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from config import Config
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service class for weather data and risk prediction
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize weather service
        
        Args:
            model_path: Path to trained ML model for risk prediction
        """
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.model = None
        self.model_path = model_path
        
        # Crop-specific risk thresholds
        self.crop_thresholds = {
            'rice': {
                'temp_min': 15,
                'temp_max': 35,
                'temp_optimal': (20, 30),
                'humidity_min': 50,
                'humidity_max': 90,
                'humidity_optimal': (60, 80),
                'rain_optimal': (10, 50),
                'disease_risk_humidity': 80,
                'disease_risk_temp_range': (25, 32)
            },
            'wheat': {
                'temp_min': 10,
                'temp_max': 30,
                'temp_optimal': (15, 25),
                'humidity_min': 40,
                'humidity_max': 70,
                'humidity_optimal': (40, 60),
                'rain_optimal': (5, 30),
                'disease_risk_humidity': 70,
                'disease_risk_temp_range': (20, 28)
            },
            'cotton': {
                'temp_min': 18,
                'temp_max': 38,
                'temp_optimal': (25, 35),
                'humidity_min': 40,
                'humidity_max': 80,
                'humidity_optimal': (50, 70),
                'rain_optimal': (10, 40),
                'disease_risk_humidity': 75,
                'disease_risk_temp_range': (25, 35)
            },
            'sugarcane': {
                'temp_min': 20,
                'temp_max': 40,
                'temp_optimal': (25, 35),
                'humidity_min': 50,
                'humidity_max': 85,
                'humidity_optimal': (60, 80),
                'rain_optimal': (20, 60),
                'disease_risk_humidity': 80,
                'disease_risk_temp_range': (25, 35)
            },
            'banana': {
                'temp_min': 20,
                'temp_max': 35,
                'temp_optimal': (25, 30),
                'humidity_min': 60,
                'humidity_max': 90,
                'humidity_optimal': (70, 85),
                'rain_optimal': (30, 70),
                'disease_risk_humidity': 80,
                'disease_risk_temp_range': (25, 32)
            },
            'coconut': {
                'temp_min': 22,
                'temp_max': 36,
                'temp_optimal': (27, 32),
                'humidity_min': 60,
                'humidity_max': 90,
                'humidity_optimal': (70, 85),
                'rain_optimal': (40, 80),
                'disease_risk_humidity': 85,
                'disease_risk_temp_range': (25, 35)
            }
        }
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path: str) -> None:
        """
        Load trained weather risk prediction model
        
        Args:
            model_path: Path to model file
        """
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            logger.info(f"Weather model loaded from {model_path}")
        except Exception as e:
            logger.error(f"Error loading weather model: {str(e)}")
            logger.info("Continuing without ML model")
    
    def get_current_weather(self, lat: float, lon: float) -> Dict:
        """
        Fetch current weather data from OpenWeatherMap API
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with current weather data
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            logger.info(f"Fetching weather for coordinates: {lat}, {lon}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant weather data
                weather_data = {
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'temp_min': data['main']['temp_min'],
                    'temp_max': data['main']['temp_max'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'sea_level': data['main'].get('sea_level'),
                    'grnd_level': data['main'].get('grnd_level'),
                    'weather_main': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description'],
                    'weather_icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'wind_deg': data['wind']['deg'],
                    'wind_gust': data['wind'].get('gust'),
                    'clouds': data['clouds']['all'],
                    'visibility': data.get('visibility', 0),
                    'timestamp': datetime.now().isoformat(),
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                    'timezone': data['timezone'],
                    'city_name': data['name'],
                    'country': data['sys']['country']
                }
                
                # Add rainfall if available
                if 'rain' in data:
                    weather_data['rain_1h'] = data['rain'].get('1h', 0)
                    weather_data['rain_3h'] = data['rain'].get('3h', 0)
                    weather_data['rainfall'] = data['rain'].get('1h', 0)
                else:
                    weather_data['rainfall'] = 0
                
                # Add snowfall if available
                if 'snow' in data:
                    weather_data['snow_1h'] = data['snow'].get('1h', 0)
                
                logger.info(f"Weather data fetched successfully for {weather_data['city_name']}")
                return weather_data
                
            else:
                error_msg = f"Weather API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                
                # Return fallback data for testing
                return self.get_fallback_weather(lat, lon)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching weather: {str(e)}")
            return self.get_fallback_weather(lat, lon)
        except Exception as e:
            logger.error(f"Unexpected error fetching weather: {str(e)}")
            return self.get_fallback_weather(lat, lon)
    
    def get_forecast(self, lat: float, lon: float, days: int = 5) -> List[Dict]:
        """
        Get weather forecast for next few days
        
        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days for forecast (max 5)
            
        Returns:
            List of forecast data by day
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': min(days * 8, 40)  # API returns 3-hour intervals, 8 per day
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Group by day
                daily_forecast = {}
                
                for item in data['list']:
                    date = item['dt_txt'].split()[0]
                    
                    if date not in daily_forecast:
                        daily_forecast[date] = {
                            'date': date,
                            'temperatures': [],
                            'humidity': [],
                            'weather_conditions': [],
                            'rainfall': 0,
                            'wind_speed': []
                        }
                    
                    daily_forecast[date]['temperatures'].append(item['main']['temp'])
                    daily_forecast[date]['humidity'].append(item['main']['humidity'])
                    daily_forecast[date]['weather_conditions'].append(item['weather'][0]['main'])
                    daily_forecast[date]['wind_speed'].append(item['wind']['speed'])
                    
                    if 'rain' in item and '3h' in item['rain']:
                        daily_forecast[date]['rainfall'] += item['rain']['3h']
                
                # Calculate daily averages
                forecast = []
                for date, day_data in daily_forecast.items():
                    forecast.append({
                        'date': date,
                        'temperature': round(sum(day_data['temperatures']) / len(day_data['temperatures']), 1),
                        'temp_min': min(day_data['temperatures']),
                        'temp_max': max(day_data['temperatures']),
                        'humidity': round(sum(day_data['humidity']) / len(day_data['humidity']), 1),
                        'humidity_min': min(day_data['humidity']),
                        'humidity_max': max(day_data['humidity']),
                        'rainfall': round(day_data['rainfall'], 1),
                        'wind_speed': round(sum(day_data['wind_speed']) / len(day_data['wind_speed']), 1),
                        'dominant_weather': max(set(day_data['weather_conditions']), key=day_data['weather_conditions'].count)
                    })
                
                return forecast[:days]
                
            else:
                logger.error(f"Forecast API error: {response.status_code}")
                return self.get_fallback_forecast(days)
                
        except Exception as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            return self.get_fallback_forecast(days)
    
    def predict_disease_risk(self, lat: float, lon: float, crop_type: str) -> Dict:
        """
        Predict disease risk based on weather conditions
        
        Args:
            lat: Latitude
            lon: Longitude
            crop_type: Type of crop
            
        Returns:
            Risk assessment dictionary
        """
        try:
            # Get current weather
            weather = self.get_current_weather(lat, lon)
            
            # Get crop-specific thresholds
            thresholds = self.crop_thresholds.get(crop_type.lower(), self.crop_thresholds['rice'])
            
            # Calculate risk score
            risk_score = 0
            risk_factors = []
            
            # Temperature risk
            temp = weather['temperature']
            if temp < thresholds['temp_min']:
                risk_score += 30
                risk_factors.append(f"Temperature too low ({temp}°C) - stress risk")
            elif temp > thresholds['temp_max']:
                risk_score += 30
                risk_factors.append(f"Temperature too high ({temp}°C) - heat stress risk")
            elif thresholds['temp_optimal'][0] <= temp <= thresholds['temp_optimal'][1]:
                risk_score -= 10  # Optimal temperature reduces risk
            else:
                risk_score += 15
                risk_factors.append(f"Temperature ({temp}°C) suboptimal for {crop_type}")
            
            # Humidity risk
            humidity = weather['humidity']
            if humidity > thresholds.get('disease_risk_humidity', 80):
                risk_score += 40
                risk_factors.append(f"Very high humidity ({humidity}%) - high disease risk")
            elif humidity > thresholds['humidity_optimal'][1]:
                risk_score += 25
                risk_factors.append(f"High humidity ({humidity}%) - moderate disease risk")
            elif humidity < thresholds['humidity_min']:
                risk_score += 20
                risk_factors.append(f"Low humidity ({humidity}%) - drought stress risk")
            
            # Rainfall risk
            rainfall = weather.get('rainfall', 0)
            if rainfall > thresholds.get('rain_optimal', (10, 50))[1]:
                risk_score += 25
                risk_factors.append(f"Heavy rainfall ({rainfall}mm) - waterlogging risk")
            elif rainfall > 0:
                # Light rain might be beneficial
                risk_score -= 5
            
            # Wind risk
            wind_speed = weather.get('wind_speed', 0)
            if wind_speed > 30:
                risk_score += 20
                risk_factors.append(f"High wind speed ({wind_speed} m/s) - physical damage risk")
            elif wind_speed > 20:
                risk_score += 10
                risk_factors.append(f"Moderate wind speed ({wind_speed} m/s)")
            
            # Get forecast
            forecast = self.get_forecast(lat, lon, days=5)
            
            # Check forecast for risks
            future_risks = []
            for day in forecast[:3]:  # Check next 3 days
                day_risk = 0
                
                if day['temperature'] < thresholds['temp_min'] or day['temperature'] > thresholds['temp_max']:
                    day_risk += 20
                
                if day['humidity'] > thresholds.get('disease_risk_humidity', 80):
                    day_risk += 30
                
                if day.get('rainfall', 0) > thresholds.get('rain_optimal', (10, 50))[1]:
                    day_risk += 25
                
                if day_risk > 50:
                    future_risks.append({
                        'date': day['date'],
                        'risk_level': 'HIGH' if day_risk > 70 else 'MEDIUM',
                        'conditions': day
                    })
            
            # Calculate ML prediction if model is available
            ml_prediction = None
            if self.model:
                try:
                    features = np.array([[
                        temp,
                        humidity,
                        rainfall,
                        wind_speed,
                        weather.get('pressure', 1013)
                    ]])
                    ml_prediction = self.model.predict_proba(features)[0].tolist()
                except Exception as e:
                    logger.error(f"ML prediction error: {str(e)}")
            
            # Determine risk level
            risk_score = max(0, min(100, risk_score))  # Clamp between 0-100
            
            if risk_score >= 70:
                risk_level = "HIGH"
                recommendation = "Take immediate preventive measures. Consider fungicide application and increase field monitoring."
            elif risk_score >= 40:
                risk_level = "MEDIUM"
                recommendation = "Monitor crops closely. Prepare preventive measures and check fields daily."
            else:
                risk_level = "LOW"
                recommendation = "Normal conditions. Continue regular monitoring and good agricultural practices."
            
            # Get likely diseases based on conditions
            likely_diseases = self.predict_likely_diseases(weather, crop_type, thresholds)
            
            return {
                'risk_level': risk_level,
                'risk_score': round(risk_score, 2),
                'risk_factors': risk_factors,
                'current_weather': weather,
                'forecast': forecast,
                'future_risks': future_risks,
                'likely_diseases': likely_diseases,
                'recommendation': recommendation,
                'ml_prediction': ml_prediction,
                'crop_thresholds': thresholds,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in risk prediction: {str(e)}")
            return {
                'risk_level': "UNKNOWN",
                'error': str(e),
                'fallback': True,
                'recommendation': "Unable to calculate risk. Please check manually."
            }
    
    def predict_likely_diseases(self, weather: Dict, crop_type: str, thresholds: Dict) -> List[Dict]:
        """
        Predict likely diseases based on weather conditions
        
        Args:
            weather: Current weather data
            crop_type: Type of crop
            thresholds: Crop-specific thresholds
            
        Returns:
            List of likely diseases with probabilities
        """
        likely_diseases = []
        
        temp = weather['temperature']
        humidity = weather['humidity']
        rainfall = weather.get('rainfall', 0)
        
        # Disease database (simplified)
        disease_db = {
            'rice': {
                'high_humidity': {
                    'name': 'Rice Blast',
                    'condition': humidity > 85,
                    'probability': min(90, humidity)
                },
                'moderate_humidity': {
                    'name': 'Brown Spot',
                    'condition': 70 < humidity <= 85 and temp > 25,
                    'probability': 70
                },
                'wet_conditions': {
                    'name': 'Sheath Blight',
                    'condition': humidity > 80 and rainfall > 20,
                    'probability': 80
                }
            },
            'wheat': {
                'high_humidity': {
                    'name': 'Wheat Rust',
                    'condition': humidity > 75 and 15 < temp < 25,
                    'probability': 85
                },
                'cool_wet': {
                    'name': 'Powdery Mildew',
                    'condition': humidity > 70 and temp < 20,
                    'probability': 75
                }
            }
        }
        
        # Get diseases for crop type
        crop_diseases = disease_db.get(crop_type.lower(), {})
        
        for disease_key, disease_info in crop_diseases.items():
            if disease_info['condition']:
                likely_diseases.append({
                    'disease': disease_info['name'],
                    'probability': disease_info['probability'],
                    'confidence': 'High' if disease_info['probability'] > 80 else 'Medium'
                })
        
        return likely_diseases[:3]  # Return top 3
    
    def get_fallback_weather(self, lat: float, lon: float) -> Dict:
        """
        Get fallback weather data for testing
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Fallback weather data
        """
        return {
            'temperature': 28.5,
            'feels_like': 30.2,
            'temp_min': 26.0,
            'temp_max': 32.0,
            'humidity': 75,
            'pressure': 1012,
            'weather_main': 'Clouds',
            'weather_description': 'scattered clouds',
            'wind_speed': 3.6,
            'clouds': 40,
            'rainfall': 5.2,
            'timestamp': datetime.now().isoformat(),
            'city_name': 'Sample Location',
            'country': 'IN',
            'is_fallback': True
        }
    
    def get_fallback_forecast(self, days: int) -> List[Dict]:
        """
        Get fallback forecast data for testing
        
        Args:
            days: Number of days
            
        Returns:
            Fallback forecast data
        """
        forecast = []
        start_date = datetime.now()
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'temperature': round(28 + (i % 5) - 2, 1),
                'temp_min': round(24 + (i % 3), 1),
                'temp_max': round(32 - (i % 4), 1),
                'humidity': round(70 + (i % 10), 1),
                'rainfall': round(max(0, (i % 15) - 5), 1),
                'wind_speed': round(3 + (i % 4), 1),
                'dominant_weather': 'Clouds' if i % 2 == 0 else 'Clear',
                'is_fallback': True
            })
        
        return forecast
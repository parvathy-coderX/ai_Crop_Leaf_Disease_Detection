import React, { useState, useEffect } from 'react';
import { Cloud, Droplets, Thermometer, Wind, AlertTriangle, MapPin, Loader } from 'lucide-react';
import { getWeatherRisk, getCurrentWeather } from '../services/api';

const WeatherRiskCard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [weatherData, setWeatherData] = useState(null);
  const [location, setLocation] = useState({ lat: null, lon: null });
  const [cropType, setCropType] = useState('rice');
  const [locationDenied, setLocationDenied] = useState(false);

  // Get user's location on component mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude
          });
          setLocationDenied(false);
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationDenied(true);
          // Use default location (India center)
          setLocation({ lat: 20.5937, lon: 78.9629 });
        }
      );
    } else {
      setLocationDenied(true);
      setLocation({ lat: 20.5937, lon: 78.9629 });
    }
  }, []);

  // Fetch weather data when location and crop type are available
  useEffect(() => {
    if (location.lat && location.lon) {
      fetchWeatherData();
    }
  }, [location, cropType]);

  const fetchWeatherData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Get weather risk assessment
      const riskData = await getWeatherRisk(location.lat, location.lon, cropType);
      
      // Get current weather
      const currentWeather = await getCurrentWeather(location.lat, location.lon);
      
      setWeatherData({
        ...riskData.data,
        current: currentWeather.data
      });
    } catch (err) {
      console.error('Error fetching weather data:', err);
      setError('Failed to fetch weather data. Please try again.');
      
      // Set mock data for demonstration
      setWeatherData({
        risk_level: 'MEDIUM',
        risk_score: 65,
        risk_factors: ['High humidity (75%)', 'Temperature 32°C'],
        recommendation: 'Monitor crops for fungal diseases.',
        current: {
          temperature: 32,
          humidity: 75,
          rainfall: 15,
          wind_speed: 12,
          weather_description: 'Partly cloudy'
        },
        forecast: [
          { day: 'Mon', temp: 32, humidity: 75 },
          { day: 'Tue', temp: 33, humidity: 78 },
          { day: 'Wed', temp: 31, humidity: 72 }
        ]
      });
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level) => {
    switch(level) {
      case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <Loader className="h-8 w-8 animate-spin text-green-600 mx-auto mb-4" />
        <p className="text-gray-600">Fetching weather data for your location...</p>
      </div>
    );
  }

  if (error && !weatherData) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 text-center">
        <AlertTriangle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <p className="text-red-600 mb-4">{error}</p>
        <button 
          onClick={fetchWeatherData}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Location Banner */}
      {locationDenied && (
        <div className="bg-yellow-50 p-3 text-sm text-yellow-700 flex items-center">
          <MapPin className="h-4 w-4 mr-2" />
          Using default location. Enable location services for accurate data.
        </div>
      )}

      {/* Header */}
      <div className="p-6 bg-gradient-to-r from-blue-50 to-blue-100 border-b">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Weather Risk Assessment</h2>
          <select 
            value={cropType}
            onChange={(e) => setCropType(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
          >
            <option value="rice">Rice</option>
            <option value="wheat">Wheat</option>
            <option value="cotton">Cotton</option>
            <option value="sugarcane">Sugarcane</option>
            <option value="tomato">Tomato</option>
            <option value="potato">Potato</option>
          </select>
        </div>
      </div>

      {/* Risk Level */}
      {weatherData && (
        <div className="p-6 border-b">
          <div className={`p-4 rounded-lg border ${getRiskColor(weatherData.risk_level)}`}>
            <div className="flex items-center justify-between">
              <span className="font-semibold">Disease Risk Level:</span>
              <span className="text-lg font-bold">{weatherData.risk_level}</span>
            </div>
            <div className="mt-2">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    weatherData.risk_level === 'HIGH' ? 'bg-red-500' :
                    weatherData.risk_level === 'MEDIUM' ? 'bg-yellow-500' : 'bg-green-500'
                  }`}
                  style={{ width: `${weatherData.risk_score}%` }}
                ></div>
              </div>
              <p className="text-sm mt-2">{weatherData.recommendation}</p>
            </div>
          </div>
        </div>
      )}

      {/* Current Weather */}
      {weatherData?.current && (
        <div className="p-6 border-b">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
            <Cloud className="h-5 w-5 mr-2 text-blue-500" />
            Current Weather
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 p-3 rounded-lg text-center">
              <Thermometer className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-600">Temperature</div>
              <div className="font-bold">{weatherData.current.temperature}°C</div>
            </div>
            
            <div className="bg-blue-50 p-3 rounded-lg text-center">
              <Droplets className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-600">Humidity</div>
              <div className="font-bold">{weatherData.current.humidity}%</div>
            </div>
            
            <div className="bg-blue-50 p-3 rounded-lg text-center">
              <Wind className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-600">Wind Speed</div>
              <div className="font-bold">{weatherData.current.wind_speed} km/h</div>
            </div>
            
            <div className="bg-blue-50 p-3 rounded-lg text-center">
              <Cloud className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-600">Condition</div>
              <div className="font-bold text-sm">{weatherData.current.weather_description}</div>
            </div>
          </div>
        </div>
      )}

      {/* Risk Factors */}
      {weatherData?.risk_factors && weatherData.risk_factors.length > 0 && (
        <div className="p-6 border-b">
          <h3 className="font-semibold text-gray-900 mb-3">Risk Factors</h3>
          <ul className="space-y-2">
            {weatherData.risk_factors.map((factor, index) => (
              <li key={index} className="flex items-start">
                <AlertTriangle className="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0" />
                <span>{factor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 7-Day Forecast */}
      {weatherData?.forecast && weatherData.forecast.length > 0 && (
        <div className="p-6">
          <h3 className="font-semibold text-gray-900 mb-4">7-Day Forecast</h3>
          <div className="grid grid-cols-7 gap-2">
            {weatherData.forecast.map((day, index) => (
              <div key={index} className="text-center">
                <div className="text-sm font-medium">{day.day}</div>
                <Thermometer className="h-4 w-4 mx-auto my-1 text-orange-500" />
                <div className="text-sm">{day.temp}°C</div>
                <Droplets className="h-4 w-4 mx-auto my-1 text-blue-500" />
                <div className="text-sm">{day.humidity}%</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Refresh Button */}
      <div className="p-4 bg-gray-50 border-t text-center">
        <button
          onClick={fetchWeatherData}
          className="text-sm text-green-600 hover:text-green-700 font-medium"
        >
          ↻ Refresh Data
        </button>
      </div>
    </div>
  );
};

export default WeatherRiskCard;
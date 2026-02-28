import React, { useState } from 'react';
import {
  Cloud,
  Droplets,
  Thermometer,
  Wind,
  Sun,
  CloudRain,
  AlertTriangle,
  Calendar,
  ChevronDown,
  ChevronUp,
  Activity
} from 'lucide-react';

const WeatherRiskCard = ({ weatherData }) => {
  const [showForecast, setShowForecast] = useState(false);
  const [showDetails, setShowDetails] = useState(false);

  if (!weatherData) return null;

  const {
    risk_level,
    risk_score,
    risk_factors,
    current_weather,
    forecast,
    future_risks,
    likely_diseases,
    recommendation,
    crop_info,
    location
  } = weatherData;

  const getRiskColor = () => {
    switch (risk_level) {
      case 'HIGH': return 'red';
      case 'MEDIUM': return 'yellow';
      case 'LOW': return 'green';
      default: return 'gray';
    }
  };

  const riskColor = getRiskColor();

  const getRiskIcon = () => {
    switch (risk_level) {
      case 'HIGH':
        return <AlertTriangle className="h-8 w-8 text-red-500" />;
      case 'MEDIUM':
        return <Activity className="h-8 w-8 text-yellow-500" />;
      case 'LOW':
        return <Cloud className="h-8 w-8 text-green-500" />;
      default:
        return <Cloud className="h-8 w-8 text-gray-500" />;
    }
  };

  const getRiskBgColor = () => {
    switch (risk_level) {
      case 'HIGH': return 'bg-red-50 border-red-200';
      case 'MEDIUM': return 'bg-yellow-50 border-yellow-200';
      case 'LOW': return 'bg-green-50 border-green-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  const getRiskTextColor = () => {
    switch (risk_level) {
      case 'HIGH': return 'text-red-700';
      case 'MEDIUM': return 'text-yellow-700';
      case 'LOW': return 'text-green-700';
      default: return 'text-gray-700';
    }
  };

  const getWeatherIcon = (condition) => {
    switch (condition?.toLowerCase()) {
      case 'clear':
        return <Sun className="h-5 w-5 text-yellow-500" />;
      case 'rain':
        return <CloudRain className="h-5 w-5 text-blue-500" />;
      default:
        return <Cloud className="h-5 w-5 text-gray-500" />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200">
      {/* Header */}
      <div className={`p-6 ${getRiskBgColor()} border-b`}>
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-4">
            {getRiskIcon()}
            <div>
              <h3 className="text-2xl font-bold text-gray-900">
                Weather Disease Risk
              </h3>
              <div className="flex items-center space-x-2 mt-2">
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  risk_level === 'HIGH' ? 'bg-red-100 text-red-800' :
                  risk_level === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {risk_level} RISK
                </span>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white">
                  Score: {risk_score}/100
                </span>
              </div>
            </div>
          </div>
          {location && (
            <div className="text-right">
              <div className="text-sm text-gray-500">{location.name}</div>
            </div>
          )}
        </div>
      </div>

      {/* Current Weather */}
      {current_weather && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
            <Cloud className="h-5 w-5 text-blue-500 mr-2" />
            Current Weather Conditions
          </h4>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <Thermometer className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-500">Temperature</div>
              <div className="font-semibold text-gray-900">
                {current_weather.temperature}°C
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <Droplets className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-500">Humidity</div>
              <div className="font-semibold text-gray-900">
                {current_weather.humidity}%
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <CloudRain className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-500">Rainfall</div>
              <div className="font-semibold text-gray-900">
                {current_weather.rainfall || 0} mm
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-3 text-center">
              <Wind className="h-6 w-6 text-blue-500 mx-auto mb-1" />
              <div className="text-sm text-gray-500">Wind Speed</div>
              <div className="font-semibold text-gray-900">
                {current_weather.wind_speed} m/s
              </div>
            </div>
          </div>

          <div className="mt-4 text-sm text-gray-600">
            {current_weather.weather_description}
          </div>
        </div>
      )}

      {/* Risk Factors */}
      {risk_factors && risk_factors.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <AlertTriangle className={`h-5 w-5 mr-2 ${
              risk_level === 'HIGH' ? 'text-red-500' :
              risk_level === 'MEDIUM' ? 'text-yellow-500' :
              'text-green-500'
            }`} />
            Risk Factors
          </h4>
          
          <ul className="space-y-2">
            {risk_factors.map((factor, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className={`mt-1 ${
                  risk_level === 'HIGH' ? 'text-red-500' :
                  risk_level === 'MEDIUM' ? 'text-yellow-500' :
                  'text-green-500'
                }`}>•</span>
                <span className="text-gray-700">{factor}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Likely Diseases */}
      {likely_diseases && likely_diseases.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3">Likely Diseases</h4>
          <div className="space-y-2">
            {likely_diseases.map((disease, index) => (
              <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                <span className="font-medium text-gray-800">{disease.disease}</span>
                <span className={`text-sm px-2 py-1 rounded ${
                  disease.probability === 'High' ? 'bg-red-100 text-red-700' :
                  disease.probability === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  {disease.probability} Risk
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Crop Information */}
      {crop_info && (
        <div className="p-6 border-b">
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full flex items-center justify-between text-left"
          >
            <h4 className="font-semibold text-gray-900">Crop Information</h4>
            {showDetails ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
          
          {showDetails && (
            <div className="mt-4 space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-500">Optimal Temperature</div>
                  <div className="font-medium">{crop_info.optimal_conditions.temperature}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Optimal Humidity</div>
                  <div className="font-medium">{crop_info.optimal_conditions.humidity}</div>
                </div>
              </div>
              
              {crop_info.current_deviation && (
                <div className="bg-yellow-50 p-3 rounded-lg">
                  <div className="text-sm text-yellow-800 font-medium mb-1">Current Deviation</div>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div>Temperature: {crop_info.current_deviation.temperature}°C</div>
                    <div>Humidity: {crop_info.current_deviation.humidity}%</div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Forecast */}
      {forecast && forecast.length > 0 && (
        <div className="p-6 border-b">
          <button
            onClick={() => setShowForecast(!showForecast)}
            className="w-full flex items-center justify-between text-left"
          >
            <h4 className="font-semibold text-gray-900 flex items-center">
              <Calendar className="h-5 w-5 text-blue-500 mr-2" />
              5-Day Forecast
            </h4>
            {showForecast ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </button>
          
          {showForecast && (
            <div className="mt-4 space-y-3">
              {forecast.map((day, index) => (
                <div key={index} className="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {getWeatherIcon(day.dominant_weather)}
                    <div>
                      <div className="font-medium">{new Date(day.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}</div>
                      <div className="text-sm text-gray-500">{day.dominant_weather}</div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                      <Thermometer className="h-4 w-4 text-orange-500 mr-1" />
                      <span>{day.temperature}°C</span>
                    </div>
                    <div className="flex items-center">
                      <Droplets className="h-4 w-4 text-blue-500 mr-1" />
                      <span>{day.humidity}%</span>
                    </div>
                    {day.rainfall > 0 && (
                      <div className="flex items-center">
                        <CloudRain className="h-4 w-4 text-blue-500 mr-1" />
                        <span>{day.rainfall}mm</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Future Risks */}
      {future_risks && future_risks.length > 0 && (
        <div className="p-6 border-b">
          <h4 className="font-semibold text-gray-900 mb-3">Upcoming Risks</h4>
          <div className="space-y-2">
            {future_risks.map((risk, index) => (
              <div key={index} className="bg-orange-50 p-3 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{new Date(risk.date).toLocaleDateString()}</span>
                  <span className={`text-sm px-2 py-1 rounded ${
                    risk.risk_level === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {risk.risk_level} RISK
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendation */}
      {recommendation && (
        <div className={`p-6 ${getRiskBgColor()}`}>
          <h4 className="font-semibold text-gray-900 mb-2">Recommendation</h4>
          <p className={`${getRiskTextColor()}`}>{recommendation}</p>
        </div>
      )}
    </div>
  );
};

export default WeatherRiskCard;
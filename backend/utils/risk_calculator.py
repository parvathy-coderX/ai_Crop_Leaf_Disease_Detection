"""
Weather risk calculation utilities
"""

def calculate_risk_score(weather_data, crop_type):
    """
    Calculate disease risk based on weather conditions
    Args:
        weather_data: dict with temp, humidity, rainfall
        crop_type: type of crop
    Returns:
        risk_level and score
    """
    
    risk_score = 0
    risk_factors = []
    
    # Temperature risk
    temp = weather_data.get('temperature', 25)
    if temp > 30:
        risk_score += 30
        risk_factors.append(f"High temperature ({temp}°C) increases disease risk")
    elif temp < 15:
        risk_score += 20
        risk_factors.append(f"Low temperature ({temp}°C) may stress crops")
    
    # Humidity risk
    humidity = weather_data.get('humidity', 60)
    if humidity > 80:
        risk_score += 40
        risk_factors.append(f"Very high humidity ({humidity}%) - fungal disease risk")
    elif humidity > 70:
        risk_score += 25
        risk_factors.append(f"High humidity ({humidity}%) - moderate risk")
    
    # Rainfall risk
    rainfall = weather_data.get('rainfall', 0)
    if rainfall > 50:
        risk_score += 30
        risk_factors.append(f"Heavy rainfall ({rainfall}mm) - waterlogging risk")
    elif rainfall > 20:
        risk_score += 15
        risk_factors.append(f"Moderate rainfall ({rainfall}mm) - monitor crops")
    
    # Crop-specific adjustments
    crop_risk_factors = {
        'rice': {'humidity_weight': 1.2, 'temp_weight': 0.8},
        'wheat': {'humidity_weight': 0.8, 'temp_weight': 1.1},
        'cotton': {'humidity_weight': 1.0, 'temp_weight': 1.2},
        'sugarcane': {'humidity_weight': 1.1, 'temp_weight': 1.0}
    }
    
    if crop_type.lower() in crop_risk_factors:
        factors = crop_risk_factors[crop_type.lower()]
        risk_score = risk_score * factors.get('humidity_weight', 1.0)
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH"
        recommendation = "Take immediate preventive measures. Consider fungicide application."
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        recommendation = "Monitor crops closely. Prepare preventive measures."
    else:
        risk_level = "LOW"
        recommendation = "Normal conditions. Continue regular monitoring."
    
    return {
        'risk_level': risk_level,
        'risk_score': round(risk_score, 2),
        'risk_factors': risk_factors,
        'recommendation': recommendation,
        'weather_summary': {
            'temperature': temp,
            'humidity': humidity,
            'rainfall': rainfall
        }
    }
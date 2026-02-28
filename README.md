**AI-Based Crop Leaf Disease Detection and Weather-Driven Risk Prediction System for Smart Agriculture** 🎯


**Team Name**: Zentrix

**Team Member**s:

Parvathy Santhosh C - MACE

**Hosted Project Link**:
https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection

**Project Description**

This system allows farmers to upload images of crop leaves and automatically detect diseases using AI. It also predicts weather-driven disease risks and provides preventive recommendations to protect crops.

**The Problem Statement**

Farmers often face crop losses due to undiagnosed diseases and unpredictable weather conditions. Early disease detection and weather-based risk prediction are crucial to reduce losses and improve yield.

**The Solution**

We use AI-based image recognition to detect leaf diseases and weather analysis to predict disease risks. The system provides real-time disease information, risk levels, and actionable recommendations to help farmers take timely preventive measures.
**video**
**Technical Details**
**Technologies/Components Used**

Software:

Languages: Python

Frameworks: Flask

Libraries: TensorFlow / PyTorch (for AI model), OpenCV, Pillow, NumPy, Pandas, Requests

Tools: VS Code, Git

Features

Key Features:

Leaf Image Disease Detection: Upload a leaf image to identify the disease using AI.

Weather-Based Disease Risk Prediction: Analyze local weather to estimate disease risk levels.

Preventive Recommendations: Provides actionable guidance based on disease and weather risk.

Weather Forecast Integration: Shows upcoming weather conditions that may impact crop health.

Crop Database: Supports multiple crops with crop-specific optimal conditions and thresholds.

Unique Features Compared to Existing Systems:

Combines AI image-based detection with weather-driven risk prediction.

Provides real-time recommendations for disease prevention.

Forecast analysis for future disease risks.

Supports multiple crops with crop-specific thresholds.

Implementation
Installation

Clone the repository:

git clone [your_repo_link]

Navigate to the project folder:

cd SmartAgriAI

Install required Python libraries:

pip install -r requirements.txt
Run
python app.py

Access API endpoints via http://localhost:5000/

Upload leaf images via /disease/predict endpoint

Project Documentation
**Screenshort*[*
](https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection/blob/2ad3422c189e4f68dea7f8dcc01e5653833d2f7a/Screenshot%202026-02-28%20102320.png)
Diagrams

System Architecture:

Upload leaf image → Preprocessing → AI Model → Disease Prediction → Display results

Weather API → Current weather + Forecast → Risk analysis → Recommendations

Application Workflow:

User uploads leaf image

System predicts disease with confidence

System fetches weather and predicts disease risk

Recommendations displayed based on risk level

API Documentation

Base URL: http://localhost:5000/

Endpoints:

POST /disease/predict

Description: Detect disease from uploaded leaf image

Form-data:

image (file): Leaf image

Response:

{
  "success": true,
  "disease": "Leaf Blight",
  "confidence": 92.5,
  "image_path": "20260228_123456_ab12cd34.jpg"
}

POST /weather/risk

Description: Predict weather-based disease risk

JSON body:

{
  "lat": 12.9716,
  "lon": 77.5946,
  "crop_type": "rice"
}

Response:

{
  "success": true,
  "data": {
    "risk_level": "HIGH",
    "risk_score": 78,
    "risk_factors": ["High humidity", "Heavy rainfall"],
    "recommendation": "Take preventive measures immediately."
  }
}

GET /weather/forecast

Description: Get 5-day weather forecast for a location

Query parameters: lat, lon

Response: Forecast JSON array

Project Demo

Video:
[Add your demo video link here]
Caption: Demonstrates leaf disease detection, weather risk prediction, and recommendations.

AI Tools Used (Optional)

Tool: ChatGPT, GitHub Copilot

Purpose: Boilerplate code, debugging assistance, API integration

Percentage of AI-generated code: ~20%

Human Contributions: AI model design, backend integration, preprocessing, recommendation logic

Team Contributions

Parvathy Santhosh C: Backend development, AI model integration, API implementation, testing, documentation

License

This project is licensed under the MIT License - see the LICENSE file for details.






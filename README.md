

# 🚀 **AI-Based Crop Leaf Disease Detection and Weather-Driven Risk Prediction System for Smart Agriculture**

## 🌟 Overview

An intelligent system that helps farmers **detect crop leaf diseases using AI** and **predict weather-driven risks**, enabling early intervention and better crop management.

---

## 🎯 Key Highlights

* 🌿 AI-powered leaf disease detection
* 🌦️ Weather-based disease risk prediction
* 💡 Preventive recommendations for farmers
* 📊 Multi-crop support with optimized thresholds
* 🔮 Forecast-based future risk analysis

---

## 👩‍💻 Author

**Parvathy Santhosh C**
B.Tech in AI & ML, MACE

---

## 🔗 Project Repository

(https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection)

---
## 🧾 Approach Document

https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection/blob/main/Approach%20Document.pdf

---

## 🎥 Demo Video

Watch here: [https://drive.google.com/file/d/1RoPzNlWmfQWAc3aVT9mTkabX80EtuIOl/view?usp=sharing](https://drive.google.com/file/d/1RoPzNlWmfQWAc3aVT9mTkabX80EtuIOl/view?usp=sharing)

---

## 📌 Project Description

This system allows users to upload images of crop leaves and automatically detect diseases using AI. It also analyzes weather conditions to predict disease risks and provides preventive recommendations to protect crops.

---

## ❗ Problem Statement

Farmers often face significant crop losses due to:

* Late detection of plant diseases
* Unpredictable weather conditions

Early disease identification and weather-based risk prediction are essential to reduce losses and improve agricultural productivity.

---

## 💡 Solution

The system combines:

* **AI-based image recognition** for disease detection
* **Weather data analysis** for risk prediction

It provides:

* Real-time disease detection
* Risk level classification
* Actionable preventive recommendations

---

## ⚙️ Tech Stack

* **Languages:** Python
* **Framework:** Flask
* **Libraries:** TensorFlow / PyTorch, OpenCV, Pillow, NumPy, Pandas, Requests
* **Tools:** VS Code, Git

---

## 🚀 Features

### 🔍 Core Features

* Leaf Disease Detection from uploaded images
* Weather-Based Risk Prediction
* Preventive Recommendations
* 5-Day Weather Forecast Integration

### 🌟 Unique Features

* Combines AI + weather analytics
* Real-time actionable insights
* Multi-crop support with custom thresholds

---

## 🛠️ Installation & Setup

```bash
git clone https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection.git
cd SmartAgriAI
pip install -r requirements.txt
python app.py
```

👉 Access API at: `http://localhost:5000/`

---

## 🔄 Workflow

### System Flow

* Upload leaf image → Preprocessing → AI Model → Disease Prediction
* Weather API → Forecast Data → Risk Analysis → Recommendations

### Application Flow

1. User uploads leaf image
2. System detects disease with confidence score
3. Weather data is fetched
4. Risk level is calculated
5. Recommendations are displayed

---

## 📸 Screenshot

(https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection/blob/main/Screenshot%202026-02-28%20102320.png)

---

## 📡 API Documentation

### 🔹 Base URL

```
http://localhost:5000/
```

---

### 🔹 Disease Detection

**POST /disease/predict**

**Input:**

https://github.com/parvathy-coderX/ai_Crop_Leaf_Disease_Detection/blob/main/septoria-spot-tomato-plant-ea2ab44d-e6f21d609dd04b2f96d96a33e98aab07.jpg

**Response:**

```json
{
  "success": true,
  "disease": "Leaf Blight",
  "confidence": 92.5,
  "image_path": "20260228_123456_ab12cd34.jpg"
}
```

---

### 🔹 Weather Risk Prediction

**POST /weather/risk**

**Input:**

```json
{
  "lat": 12.9716,
  "lon": 77.5946,
  "crop_type": "rice"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "risk_level": "HIGH",
    "risk_score": 78,
    "risk_factors": ["High humidity", "Heavy rainfall"],
    "recommendation": "Take preventive measures immediately."
  }
}
```

---

### 🔹 Weather Forecast

**GET /weather/forecast**

**Params:** `lat`, `lon`

**Response:** Forecast data (JSON)

---

## 🤖 AI Tools Used

* ChatGPT
* GitHub Copilot

**Usage:**

* Boilerplate code
* Debugging assistance
* API integration

**AI Contribution:** ~20%
**Human Contribution:** Model design, backend logic, integration, testing

---

## 🔮 Future Enhancements

* 📱 Mobile app integration
* 🌍 Real-time IoT sensor data
* 📊 Advanced analytics dashboard
* 🌱 More crop datasets

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork and improve the project.

---

## 📄 License

This project is licensed under the MIT License.

---

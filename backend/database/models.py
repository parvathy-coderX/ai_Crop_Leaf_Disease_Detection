"""
Database models for SmartAgriAI
"""

from database.db_config import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User model for farmers"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(200))
    
    # Personal info
    full_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(10))
    
    # Farm details
    farm_size = db.Column(db.Float)  # in acres
    primary_crop = db.Column(db.String(50))
    soil_type = db.Column(db.String(50))
    
    # Location (GPS coordinates)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='farmer', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'full_name': self.full_name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pincode': self.pincode,
            'farm_size': self.farm_size,
            'primary_crop': self.primary_crop,
            'soil_type': self.soil_type,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Prediction(db.Model):
    """Disease prediction model"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Image info
    image_filename = db.Column(db.String(200))
    image_path = db.Column(db.String(500))
    
    # Prediction results
    disease_detected = db.Column(db.String(200))
    confidence = db.Column(db.Float)
    severity = db.Column(db.String(50))
    
    # Crop info
    crop_type = db.Column(db.String(50))
    
    # Location
    location_name = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Weather at time of prediction
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    weather_condition = db.Column(db.String(100))
    weather_risk = db.Column(db.String(50))
    
    # Recommendations
    recommendations = db.Column(db.Text)  # JSON string of recommendations
    
    # Metadata
    processing_time = db.Column(db.Float)  # in seconds
    model_version = db.Column(db.String(20))
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'image_url': f'/static/uploads/{self.image_filename}' if self.image_filename else None,
            'disease': self.disease_detected,
            'confidence': self.confidence,
            'confidence_percentage': f"{self.confidence * 100:.2f}%" if self.confidence else None,
            'severity': self.severity,
            'crop_type': self.crop_type,
            'location': self.location_name,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'rainfall': self.rainfall,
            'weather_risk': self.weather_risk,
            'recommendations': self.recommendations,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Scheme(db.Model):
    """Government schemes model"""
    __tablename__ = 'schemes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Eligibility criteria
    eligibility = db.Column(db.Text)
    eligibility_criteria = db.Column(db.JSON)  # Structured eligibility
    
    # Benefits
    benefits = db.Column(db.Text)
    benefit_amount = db.Column(db.String(100))
    
    # Applicability
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    crop_type = db.Column(db.String(100))
    farmer_type = db.Column(db.String(100))  # Small, marginal, etc.
    
    # Scheme details
    scheme_type = db.Column(db.String(50))  # Central/State
    department = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    website = db.Column(db.String(200))
    
    # Application
    application_process = db.Column(db.Text)
    documents_required = db.Column(db.JSON)
    deadline = db.Column(db.String(100))
    
    # Metadata
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'eligibility': self.eligibility,
            'benefits': self.benefits,
            'benefit_amount': self.benefit_amount,
            'state': self.state,
            'district': self.district,
            'crop_type': self.crop_type,
            'farmer_type': self.farmer_type,
            'scheme_type': self.scheme_type,
            'department': self.department,
            'contact': self.contact,
            'website': self.website,
            'application_process': self.application_process,
            'documents_required': self.documents_required,
            'deadline': self.deadline,
            'active': self.active
        }

class Notification(db.Model):
    """User notifications model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    type = db.Column(db.String(50))  # weather_alert, disease_alert, scheme_update
    
    # Related data
    related_id = db.Column(db.Integer)  # ID of related entity (prediction, scheme, etc.)
    
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class WeatherData(db.Model):
    """Stored weather data"""
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    weather_condition = db.Column(db.String(100))
    
    # Forecast data (JSON)
    forecast = db.Column(db.JSON)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'rainfall': self.rainfall,
            'condition': self.weather_condition,
            'forecast': self.forecast,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
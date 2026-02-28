"""
Database configuration and initialization
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

logger = logging.getLogger(__name__)
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with app"""
    try:
        db.init_app(app)
        migrate.init_app(app, db)
        
        # Create tables
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Seed initial data
            seed_database()
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

def seed_database():
    """Seed database with initial data"""
    from database.models import Scheme, User
    
    # Check if schemes already exist
    if Scheme.query.count() == 0:
        seed_schemes()

def seed_schemes():
    """Seed government schemes"""
    from database.models import Scheme
    
    schemes = [
        {
            'name': 'Pradhan Mantri Fasal Bima Yojana',
            'description': 'Comprehensive crop insurance scheme to protect farmers against crop loss',
            'eligibility': 'All farmers growing notified crops in notified areas',
            'benefits': 'Insurance coverage for crop loss due to natural calamities, pests, and diseases',
            'state': 'All India',
            'crop_type': 'All',
            'scheme_type': 'Central',
            'department': 'Ministry of Agriculture',
            'contact': '1800-180-1551',
            'website': 'https://pmfby.gov.in',
            'application_process': 'Through local bank branches or common service centers',
            'deadline': 'Before sowing season'
        },
        {
            'name': 'Kisan Credit Card Scheme',
            'description': 'Provides farmers with timely access to credit for agricultural needs',
            'eligibility': 'All farmers, sharecroppers, tenant farmers',
            'benefits': 'Access to credit up to ₹3 lakhs at subsidized interest rates',
            'state': 'All India',
            'crop_type': 'All',
            'scheme_type': 'Central',
            'department': 'NABARD',
            'contact': '1800-180-1552',
            'website': 'https://www.nabard.org',
            'application_process': 'Apply at any nationalized bank with land documents',
            'deadline': 'Rolling application'
        },
        {
            'name': 'PM-KISAN Samman Nidhi',
            'description': 'Income support scheme for small and marginal farmers',
            'eligibility': 'Small and marginal farmer families with landholding up to 2 hectares',
            'benefits': '₹6000 per year in three equal installments',
            'state': 'All India',
            'crop_type': 'All',
            'scheme_type': 'Central',
            'department': 'Ministry of Agriculture',
            'contact': '1800-180-1553',
            'website': 'https://pmkisan.gov.in',
            'application_process': 'Apply online through PM-KISAN portal or at local agriculture office',
            'deadline': 'Rolling application'
        },
        {
            'name': 'Soil Health Card Scheme',
            'description': 'Provides soil health cards to farmers with nutrient recommendations',
            'eligibility': 'All farmers',
            'benefits': 'Soil testing and recommendations for optimal fertilizer use',
            'state': 'All India',
            'crop_type': 'All',
            'scheme_type': 'Central',
            'department': 'Department of Agriculture',
            'contact': '1800-180-1554',
            'website': 'https://soilhealth.dac.gov.in',
            'application_process': 'Contact local agriculture office or apply online',
            'deadline': 'Rolling application'
        },
        {
            'name': 'Kerala - Subsidy for Banana Cultivation',
            'description': 'State subsidy for banana farmers in Kerala',
            'eligibility': 'Banana farmers in Kerala with less than 5 acres',
            'benefits': '50% subsidy on tissue culture plants and inputs',
            'state': 'Kerala',
            'crop_type': 'banana',
            'scheme_type': 'State',
            'department': 'Kerala State Horticulture Mission',
            'contact': '0471-230-1122',
            'website': 'https://keralaagriculture.gov.in',
            'application_process': 'Apply through Krishi Bhavan',
            'deadline': 'Before planting season'
        }
    ]
    
    for scheme_data in schemes:
        scheme = Scheme(**scheme_data)
        db.session.add(scheme)
    
    db.session.commit()
    logger.info(f"Seeded {len(schemes)} government schemes")
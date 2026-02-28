"""
Government scheme recommendation service
Handles fetching and filtering government agricultural schemes
"""

import json
import logging
from typing import Dict, List, Optional
from difflib import get_close_matches
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchemeService:
    """
    Service class for government scheme recommendations
    """
    
    def __init__(self, schemes_file: str = 'datasets/scheme_data/government_schemes.json'):
        """
        Initialize scheme service
        
        Args:
            schemes_file: Path to schemes JSON file
        """
        self.schemes_file = schemes_file
        self.schemes = self.load_schemes()
        self.state_mapping = self.create_state_mapping()
        
    def load_schemes(self) -> Dict:
        """
        Load government schemes from JSON file
        
        Returns:
            Dictionary of schemes
        """
        try:
            with open(self.schemes_file, 'r', encoding='utf-8') as f:
                schemes = json.load(f)
                logger.info(f"Loaded {self.count_schemes(schemes)} schemes from {self.schemes_file}")
                return schemes
        except FileNotFoundError:
            logger.warning(f"Schemes file not found at {self.schemes_file}. Using default schemes.")
            return self.get_default_schemes()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing schemes JSON: {str(e)}")
            return self.get_default_schemes()
    
    def create_state_mapping(self) -> Dict:
        """
        Create mapping of state names variations
        
        Returns:
            Dictionary mapping variations to standard state names
        """
        return {
            'kerala': ['kerala', 'keralam', 'kerela'],
            'tamil_nadu': ['tamil nadu', 'tamilnadu', 'tn', 'madras'],
            'karnataka': ['karnataka', 'mysore', 'karnatak'],
            'andhra_pradesh': ['andhra pradesh', 'andhra', 'ap'],
            'telangana': ['telangana', 'tg'],
            'maharashtra': ['maharashtra', 'mumbai'],
            'punjab': ['punjab', 'punjab'],
            'haryana': ['haryana', 'haryanvi'],
            'uttar_pradesh': ['uttar pradesh', 'up', 'uttar pradesh'],
            'west_bengal': ['west bengal', 'bengal', 'paschim banga'],
            'gujarat': ['gujarat', 'gujrat'],
            'rajasthan': ['rajasthan', 'rajasthan'],
            'madhya_pradesh': ['madhya pradesh', 'mp'],
            'bihar': ['bihar', 'bihar'],
            'odisha': ['odisha', 'orissa']
        }
    
    def count_schemes(self, schemes: Dict) -> int:
        """
        Count total number of schemes
        
        Args:
            schemes: Schemes dictionary
            
        Returns:
            Total scheme count
        """
        count = 0
        for key, value in schemes.items():
            if isinstance(value, list):
                count += len(value)
            elif isinstance(value, dict):
                for sub_value in value.values():
                    if isinstance(sub_value, list):
                        count += len(sub_value)
        return count
    
    def get_default_schemes(self) -> Dict:
        """
        Default government schemes data
        
        Returns:
            Dictionary with default schemes
        """
        return {
            "central_schemes": [
                {
                    "id": "pmfby_001",
                    "name": "Pradhan Mantri Fasal Bima Yojana",
                    "short_name": "PMFBY",
                    "type": "insurance",
                    "ministry": "Ministry of Agriculture",
                    "description": "Comprehensive crop insurance scheme to protect farmers against crop loss due to natural calamities, pests, and diseases",
                    "benefits": [
                        "Insurance coverage for all stages of crop cycle",
                        "Very low premium rates (2% for Kharif, 1.5% for Rabi)",
                        "Full claim amount for prevented sowing",
                        "Post-harvest losses covered up to 14 days"
                    ],
                    "eligibility": [
                        "All farmers growing notified crops",
                        "Both loanee and non-loanee farmers",
                        "Sharecroppers and tenant farmers"
                    ],
                    "documents_required": [
                        "Aadhaar card",
                        "Land records/lease agreement",
                        "Bank account details",
                        "Crop details"
                    ],
                    "how_to_apply": "Apply through nearest bank branch, insurance company, or CSC center",
                    "application_deadline": "July 31 for Kharif, December 31 for Rabi",
                    "contact": "Toll-free: 1800-180-1551",
                    "website": "pmfby.gov.in",
                    "coverage": "All India",
                    "beneficiaries": "15+ crore farmers"
                },
                {
                    "id": "pmkisan_001",
                    "name": "PM Kisan Samman Nidhi",
                    "short_name": "PM-KISAN",
                    "type": "income_support",
                    "ministry": "Ministry of Agriculture",
                    "description": "Income support scheme providing financial benefit to small and marginal farmers",
                    "benefits": [
                        "₹6000 per year in three equal installments",
                        "Direct transfer to bank account",
                        "No intermediaries"
                    ],
                    "eligibility": [
                        "Small and marginal farmers with landholding up to 2 hectares",
                        "All farmer families (subject to exclusion criteria)"
                    ],
                    "exclusion_criteria": [
                        "Institutional land holders",
                        "Farmers paying income tax",
                        "Retired pensioners with >₹10,000 pension",
                        "Former and present MPs/MLAs"
                    ],
                    "documents_required": [
                        "Aadhaar card",
                        "Land records",
                        "Bank account with IFSC code"
                    ],
                    "how_to_apply": "Register online at pmkisan.gov.in or through local agriculture office",
                    "installment_schedule": "April-July, August-November, December-March",
                    "contact": "Toll-free: 1800-180-1551",
                    "website": "pmkisan.gov.in"
                },
                {
                    "id": "kcc_001",
                    "name": "Kisan Credit Card",
                    "short_name": "KCC",
                    "type": "credit",
                    "ministry": "Ministry of Finance",
                    "description": "Provides farmers with timely access to credit for agricultural needs",
                    "benefits": [
                        "Short-term loans for cultivation needs",
                        "Flexible withdrawal options",
                        "Personal accident insurance up to ₹50,000",
                        "Life insurance coverage"
                    ],
                    "loan_features": {
                        "interest_rate": "4-7% per annum (with 2% interest subvention)",
                        "maximum_limit": "₹3,00,000 (can be enhanced based on performance)",
                        "repayment_period": "Up to 12 months",
                        "moratorium": "Up to 6 months"
                    },
                    "eligibility": [
                        "All farmers",
                        "Sharecroppers",
                        "Tenant farmers",
                        "Self Help Groups"
                    ],
                    "documents_required": [
                        "Aadhaar card",
                        "Land records",
                        "Passport size photos",
                        "Bank account"
                    ],
                    "how_to_apply": "Visit any nationalized bank with required documents",
                    "contact": "Contact your nearest bank branch"
                },
                {
                    "id": "nmsa_001",
                    "name": "National Mission for Sustainable Agriculture",
                    "short_name": "NMSA",
                    "type": "sustainable_farming",
                    "ministry": "Ministry of Agriculture",
                    "description": "Promotes sustainable agriculture practices and climate-resilient farming",
                    "benefits": [
                        "Subsidy for organic farming",
                        "Support for water conservation",
                        "Soil health management",
                        "Training and capacity building"
                    ],
                    "subsidies": {
                        "organic_farming": "50% subsidy up to ₹50,000/ha",
                        "vermicompost": "50% subsidy up to ₹25,000",
                        "rainwater_harvesting": "50% subsidy up to ₹75,000",
                        "drip_irrigation": "70% subsidy up to ₹45,000"
                    },
                    "eligibility": [
                        "All farmers",
                        "Farmer Producer Organizations",
                        "Self Help Groups",
                        "Cooperatives"
                    ],
                    "how_to_apply": "Apply through District Agriculture Office",
                    "components": [
                        "Rainfed Area Development",
                        "Soil Health Management",
                        "Climate Change Adaptation"
                    ]
                },
                {
                    "id": "smam_001",
                    "name": "Sub-Mission on Agricultural Mechanization",
                    "short_name": "SMAM",
                    "type": "mechanization",
                    "description": "Promotes farm mechanization among small and marginal farmers",
                    "benefits": [
                        "Subsidy on farm equipment",
                        "Custom hiring centers",
                        "Training on equipment use"
                    ],
                    "subsidies": {
                        "tractors": "25% subsidy up to ₹75,000",
                        "harvesters": "40% subsidy up to ₹2,00,000",
                        "power_tillers": "35% subsidy up to ₹50,000",
                        "small_equipment": "50% subsidy up to ₹15,000"
                    },
                    "how_to_apply": "Apply at District Agriculture Office"
                }
            ],
            "state_schemes": {
                "kerala": [
                    {
                        "id": "kl_agri_001",
                        "name": "Kerala Agriculture Subsidy Scheme",
                        "state": "Kerala",
                        "type": "subsidy",
                        "description": "Comprehensive subsidy scheme for farmers in Kerala",
                        "benefits": [
                            "50% subsidy on seeds and planting materials",
                            "40% subsidy on farm equipment",
                            "Free soil testing",
                            "Technical advisory services"
                        ],
                        "specific_subsidies": {
                            "coconut": "₹100 per plant (max 100 plants)",
                            "rubber": "₹50,000 per hectare for replanting",
                            "vegetables": "50% subsidy on seeds",
                            "organic_inputs": "75% subsidy up to ₹10,000"
                        },
                        "eligibility": [
                            "All farmers in Kerala",
                            "Land ownership or lease agreement",
                            "Should not have availed similar subsidy in last 3 years"
                        ],
                        "how_to_apply": "Apply online at agriculture.kerala.gov.in or through Krishi Bhavan",
                        "contact": "Krishi Bhavan, 1800-425-1660",
                        "documents": [
                            "Aadhaar",
                            "Land tax receipt",
                            "Bank passbook"
                        ]
                    },
                    {
                        "id": "kl_irri_001",
                        "name": "Kerala Rice Development Scheme",
                        "state": "Kerala",
                        "type": "crop_specific",
                        "description": "Special scheme for rice farmers in Kerala",
                        "benefits": [
                            "Subsidized rice seeds",
                            "Mechanization support",
                            "Price support for paddy",
                            "Incentive for organic rice farming"
                        ],
                        "incentives": {
                            "paddy_price": "₹28.50 per kg minimum support price",
                            "mechanization": "40% subsidy on harvesters",
                            "organic_rice": "₹5,000 per hectare incentive"
                        },
                        "eligibility": [
                            "Rice farmers in Kerala",
                            "Minimum 0.1 hectare of paddy cultivation"
                        ],
                        "how_to_apply": "Register at nearest Krishi Bhavan"
                    }
                ],
                "tamil_nadu": [
                    {
                        "id": "tn_agri_001",
                        "name": "Tamil Nadu Farmer Subsidy Scheme",
                        "state": "Tamil Nadu",
                        "type": "subsidy",
                        "description": "Direct benefit transfer and subsidy scheme for Tamil Nadu farmers",
                        "benefits": [
                            "₹2,000 per acre per season for input costs",
                            "Free electricity for agriculture pumps",
                            "Subsidized fertilizers and seeds",
                            "Crop loan at 0% interest"
                        ],
                        "financial_benefits": {
                            "input_subsidy": "₹2,000/acre (max 5 acres)",
                            "interest_free_loan": "Up to ₹3,00,000",
                            "equipment_subsidy": "50% up to ₹50,000"
                        },
                        "eligibility": [
                            "Farmers with less than 5 acres",
                            "Should be registered in farmer database"
                        ],
                        "how_to_apply": "Apply at local agriculture office or through Uzhavan app"
                    },
                    {
                        "id": "tn_cane_001",
                        "name": "Tamil Nadu Sugarcane Development Scheme",
                        "state": "Tamil Nadu",
                        "type": "crop_specific",
                        "description": "Special scheme for sugarcane farmers",
                        "benefits": [
                            "High-yielding variety seeds",
                            "Subsidy for micro-irrigation",
                            "Training on modern cultivation",
                            "Fair price guarantee"
                        ],
                        "subsidies": {
                            "drip_irrigation": "75% subsidy up to ₹45,000/hectare",
                            "seeds": "50% subsidy on certified seeds",
                            "organic_farming": "₹10,000 per hectare"
                        },
                        "how_to_apply": "Apply through sugar mills or agriculture department"
                    }
                ],
                "karnataka": [
                    {
                        "id": "ka_agri_001",
                        "name": "Karnataka Raitha Suraksha Scheme",
                        "state": "Karnataka",
                        "type": "comprehensive",
                        "description": "Comprehensive farmer protection scheme",
                        "benefits": [
                            "Crop insurance coverage",
                            "Input subsidy",
                            "Price support",
                            "Pension for elderly farmers"
                        ],
                        "features": {
                            "insurance": "Complete crop coverage",
                            "pension": "₹1,500 per month for senior farmers",
                            "input_subsidy": "Up to ₹10,000 per acre"
                        },
                        "how_to_apply": "Apply through Raitha Samparka Kendras"
                    }
                ],
                "punjab": [
                    {
                        "id": "pb_agri_001",
                        "name": "Punjab Wheat Development Scheme",
                        "state": "Punjab",
                        "type": "crop_specific",
                        "description": "Special scheme for wheat farmers",
                        "benefits": [
                            "High-quality wheat seeds",
                            "Soil testing facilities",
                            "Mechanization support",
                            "Direct procurement"
                        ],
                        "how_to_apply": "Contact Agriculture Department"
                    }
                ]
            },
            "crop_specific": {
                "rice": [
                    {
                        "id": "rice_nfsm_001",
                        "name": "National Food Security Mission - Rice",
                        "type": "production",
                        "description": "Increases rice production through area expansion and productivity enhancement",
                        "benefits": [
                            "Cluster demonstrations",
                            "Seed distribution",
                            "Nutrient management",
                            "Water saving technologies"
                        ],
                        "interventions": [
                            "System of Rice Intensification",
                            "Aerobic rice",
                            "Direct seeded rice"
                        ]
                    },
                    {
                        "id": "rice_br_001",
                        "name": "Rice Development Programme",
                        "description": "Comprehensive support for rice cultivation",
                        "benefits": [
                            "Subsidized high-yielding varieties",
                            "Technical support for disease management",
                            "Mechanization support",
                            "Post-harvest management"
                        ],
                        "schemes": [
                            "Bringing Green Revolution to Eastern India",
                            "National Food Security Mission - Rice",
                            "Rice Fallow Management"
                        ]
                    }
                ],
                "wheat": [
                    {
                        "id": "wheat_nfsm_001",
                        "name": "National Food Security Mission - Wheat",
                        "type": "production",
                        "description": "Enhances wheat production through improved technologies",
                        "benefits": [
                            "Heat tolerant varieties",
                            "Water saving technologies",
                            "Integrated nutrient management"
                        ]
                    }
                ],
                "coconut": [
                    {
                        "id": "coc_cdb_001",
                        "name": "Coconut Development Board Schemes",
                        "type": "plantation",
                        "description": "Various schemes for coconut farmers",
                        "benefits": [
                            "Subsidy for planting materials (₹25-100 per plant)",
                            "Support for processing equipment (50% subsidy)",
                            "Technology demonstration",
                            "Export promotion"
                        ],
                        "schemes": [
                            "Productivity Improvement Programme",
                            "Technology Mission on Coconut",
                            "Coconut Palm Insurance Scheme"
                        ],
                        "how_to_apply": "Apply at Coconut Development Board office or online at cdb.gov.in"
                    }
                ],
                "cotton": [
                    {
                        "id": "cot_tech_001",
                        "name": "Cotton Technical Assistance Programme",
                        "type": "technical",
                        "description": "Support for cotton farmers",
                        "benefits": [
                            "High-quality seeds",
                            "Integrated pest management training",
                            "Soil health management",
                            "Better price realization"
                        ],
                        "features": {
                            "seed_subsidy": "50% on certified seeds",
                            "pest_management": "Free advisory services",
                            "price_support": "MSP guarantee"
                        }
                    }
                ]
            },
            "emergency_schemes": [
                {
                    "id": "cld_emergency_001",
                    "name": "Crop Loss Emergency Assistance",
                    "type": "emergency",
                    "description": "Immediate financial assistance for crop loss due to diseases or natural calamities",
                    "benefits": [
                        "Immediate relief up to ₹10,000",
                        "Input subsidy for next season",
                        "Loan restructuring",
                        "Free seeds for next crop"
                    ],
                    "eligibility": [
                        "Minimum 33% crop loss",
                        "Reported within 72 hours",
                        "Revenue department verification"
                    ],
                    "how_to_apply": "Report to agriculture officer immediately",
                    "documents": [
                        "Crop loss certificate",
                        "Land records",
                        "Photographs of damaged crop"
                    ]
                }
            ],
            "scheme_categories": {
                "insurance": ["PMFBY", "Coconut Palm Insurance"],
                "income_support": ["PM-KISAN"],
                "credit": ["KCC", "Agriculture Infrastructure Fund"],
                "subsidy": ["State subsidies", "Equipment subsidy"],
                "technical": ["Soil Health Card", "Paramparagat Krishi Vikas Yojana"],
                "emergency": ["Crop loss compensation", "Natural calamity relief"]
            }
        }
    
    def normalize_state_name(self, state: str) -> str:
        """
        Normalize state name to standard format
        
        Args:
            state: Input state name
            
        Returns:
            Standardized state name
        """
        state_lower = state.lower().strip()
        
        for standard_state, variations in self.state_mapping.items():
            for variation in variations:
                if variation in state_lower or state_lower in variation:
                    return standard_state
        
        return state_lower.replace(' ', '_')
    
    def get_schemes_by_location(self, state: str) -> List[Dict]:
        """
        Get schemes based on farmer's location
        
        Args:
            state: State name
            
        Returns:
            List of schemes for the location
        """
        recommended = []
        
        # Add central schemes (available everywhere)
        central_schemes = self.schemes.get('central_schemes', [])
        for scheme in central_schemes:
            scheme_copy = scheme.copy()
            scheme_copy['scheme_type'] = 'central'
            scheme_copy['applicability'] = 'All India'
            recommended.append(scheme_copy)
        
        # Add state-specific schemes
        if state:
            normalized_state = self.normalize_state_name(state)
            state_schemes = self.schemes.get('state_schemes', {}).get(normalized_state, [])
            
            for scheme in state_schemes:
                scheme_copy = scheme.copy()
                scheme_copy['scheme_type'] = 'state'
                scheme_copy['applicability'] = state.title()
                recommended.append(scheme_copy)
        
        return recommended
    
    def get_schemes_by_crop(self, crop_type: str) -> List[Dict]:
        """
        Get crop-specific schemes
        
        Args:
            crop_type: Type of crop
            
        Returns:
            List of crop-specific schemes
        """
        crop_lower = crop_type.lower().strip()
        crop_schemes = self.schemes.get('crop_specific', {})
        
        # Direct match
        if crop_lower in crop_schemes:
            schemes = crop_schemes[crop_lower]
            for scheme in schemes:
                scheme['scheme_type'] = 'crop_specific'
                scheme['crop'] = crop_type.title()
            return schemes
        
        # Fuzzy match
        matches = get_close_matches(crop_lower, crop_schemes.keys(), n=1, cutoff=0.6)
        if matches:
            schemes = crop_schemes[matches[0]]
            for scheme in schemes:
                scheme['scheme_type'] = 'crop_specific'
                scheme['crop'] = matches[0].title()
            return schemes
        
        return []
    
    def get_schemes_by_type(self, scheme_type: str) -> List[Dict]:
        """
        Get schemes by type (insurance, subsidy, etc.)
        
        Args:
            scheme_type: Type of scheme
            
        Returns:
            List of schemes of that type
        """
        schemes = []
        scheme_type_lower = scheme_type.lower()
        
        # Search in all scheme categories
        for category in ['central_schemes', 'state_schemes', 'crop_specific', 'emergency_schemes']:
            category_data = self.schemes.get(category, {})
            
            if isinstance(category_data, list):
                for scheme in category_data:
                    if scheme.get('type', '').lower() == scheme_type_lower:
                        schemes.append(scheme)
            elif isinstance(category_data, dict):
                for state_schemes in category_data.values():
                    for scheme in state_schemes:
                        if scheme.get('type', '').lower() == scheme_type_lower:
                            schemes.append(scheme)
        
        return schemes
    
    def recommend_schemes(self, 
                         state: Optional[str] = None, 
                         crop_type: Optional[str] = None, 
                         disease: Optional[str] = None,
                         scheme_type: Optional[str] = None,
                         max_recommendations: int = 10) -> List[Dict]:
        """
        Recommend relevant schemes based on farmer profile
        
        Args:
            state: Farmer's state
            crop_type: Type of crop
            disease: Detected disease (if any)
            scheme_type: Specific scheme type
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of recommended schemes with relevance scores
        """
        all_schemes = []
        seen_ids = set()
        
        # Get location-based schemes
        if state:
            location_schemes = self.get_schemes_by_location(state)
            for scheme in location_schemes:
                if scheme['id'] not in seen_ids:
                    scheme_copy = scheme.copy()
                    scheme_copy['relevance'] = 'High - Based on your location'
                    scheme_copy['relevance_score'] = 90
                    scheme_copy['relevance_reason'] = f"Scheme applicable in {state.title()}"
                    all_schemes.append(scheme_copy)
                    seen_ids.add(scheme['id'])
        
        # Get crop-specific schemes
        if crop_type:
            crop_schemes = self.get_schemes_by_crop(crop_type)
            for scheme in crop_schemes:
                if scheme['id'] not in seen_ids:
                    scheme_copy = scheme.copy()
                    scheme_copy['relevance'] = f'High - For {crop_type.title()} farmers'
                    scheme_copy['relevance_score'] = 85
                    scheme_copy['relevance_reason'] = f"Specifically designed for {crop_type.title()} cultivation"
                    all_schemes.append(scheme_copy)
                    seen_ids.add(scheme['id'])
        
        # Get type-specific schemes
        if scheme_type:
            type_schemes = self.get_schemes_by_type(scheme_type)
            for scheme in type_schemes:
                if scheme['id'] not in seen_ids:
                    scheme_copy = scheme.copy()
                    scheme_copy['relevance'] = f'High - {scheme_type.title()} scheme'
                    scheme_copy['relevance_score'] = 80
                    scheme_copy['relevance_reason'] = f"Scheme type: {scheme_type.title()}"
                    all_schemes.append(scheme_copy)
                    seen_ids.add(scheme['id'])
        
        # Add emergency schemes if disease detected
        if disease and disease.lower() != "healthy":
            emergency_schemes = self.schemes.get('emergency_schemes', [])
            for scheme in emergency_schemes:
                if scheme['id'] not in seen_ids:
                    scheme_copy = scheme.copy()
                    scheme_copy['relevance'] = 'Emergency - Disease detected'
                    scheme_copy['relevance_score'] = 100
                    scheme_copy['relevance_reason'] = f"Immediate assistance for {disease} affected crops"
                    all_schemes.append(scheme_copy)
                    seen_ids.add(scheme['id'])
        
        # Sort by relevance score
        all_schemes.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Add scheme category counts
        for scheme in all_schemes:
            scheme['benefits_count'] = len(scheme.get('benefits', []))
            scheme['is_urgent'] = scheme.get('relevance_score', 0) >= 90
        
        return all_schemes[:max_recommendations]
    
    def search_schemes(self, query: str) -> List[Dict]:
        """
        Search schemes by keyword
        
        Args:
            query: Search query
            
        Returns:
            List of matching schemes
        """
        query_lower = query.lower()
        results = []
        seen_ids = set()
        
        # Collect all schemes
        all_schemes = []
        all_schemes.extend(self.schemes.get('central_schemes', []))
        all_schemes.extend(self.schemes.get('emergency_schemes', []))
        
        for state_schemes in self.schemes.get('state_schemes', {}).values():
            all_schemes.extend(state_schemes)
        
        for crop_schemes in self.schemes.get('crop_specific', {}).values():
            all_schemes.extend(crop_schemes)
        
        # Search in scheme attributes
        for scheme in all_schemes:
            if scheme['id'] in seen_ids:
                continue
                
            searchable_text = ' '.join([
                str(scheme.get('name', '')),
                str(scheme.get('description', '')),
                str(scheme.get('type', '')),
                ' '.join([str(b) for b in scheme.get('benefits', [])])
            ]).lower()
            
            if query_lower in searchable_text:
                scheme_copy = scheme.copy()
                scheme_copy['search_relevance'] = self.calculate_search_relevance(query_lower, scheme)
                results.append(scheme_copy)
                seen_ids.add(scheme['id'])
        
        # Sort by search relevance
        results.sort(key=lambda x: x.get('search_relevance', 0), reverse=True)
        
        return results[:20]  # Return top 20 results
    
    def calculate_search_relevance(self, query: str, scheme: Dict) -> float:
        """
        Calculate relevance score for search results
        
        Args:
            query: Search query
            scheme: Scheme dictionary
            
        Returns:
            Relevance score (0-100)
        """
        score = 0
        
        # Check name match
        if query in scheme.get('name', '').lower():
            score += 50
        
        # Check description match
        if query in scheme.get('description', '').lower():
            score += 30
        
        # Check benefits match
        for benefit in scheme.get('benefits', []):
            if query in benefit.lower():
                score += 10
        
        return min(score, 100)
    
    def get_scheme_by_id(self, scheme_id: str) -> Optional[Dict]:
        """
        Get scheme by ID
        
        Args:
            scheme_id: Scheme identifier
            
        Returns:
            Scheme dictionary or None if not found
        """
        # Search in all scheme collections
        for category in ['central_schemes', 'state_schemes', 'crop_specific', 'emergency_schemes']:
            category_data = self.schemes.get(category, {})
            
            if isinstance(category_data, list):
                for scheme in category_data:
                    if scheme.get('id') == scheme_id:
                        return scheme
            elif isinstance(category_data, dict):
                for state_schemes in category_data.values():
                    for scheme in state_schemes:
                        if scheme.get('id') == scheme_id:
                            return scheme
        
        return None
    
    def get_scheme_categories(self) -> Dict:
        """
        Get scheme categories and counts
        
        Returns:
            Dictionary with category information
        """
        categories = {}
        
        for scheme_type in self.schemes.get('scheme_categories', {}):
            categories[scheme_type] = {
                'name': scheme_type.replace('_', ' ').title(),
                'count': len(self.get_schemes_by_type(scheme_type))
            }
        
        return categories
    
    def get_statistics(self) -> Dict:
        """
        Get scheme statistics
        
        Returns:
            Dictionary with scheme statistics
        """
        return {
            'total_schemes': self.count_schemes(self.schemes),
            'central_schemes': len(self.schemes.get('central_schemes', [])),
            'states_covered': len(self.schemes.get('state_schemes', {})),
            'crop_categories': len(self.schemes.get('crop_specific', {})),
            'emergency_schemes': len(self.schemes.get('emergency_schemes', [])),
            'scheme_categories': self.get_scheme_categories()
        }
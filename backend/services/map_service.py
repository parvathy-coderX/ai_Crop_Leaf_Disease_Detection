"""
Map and location services for SmartAgriAI
Handles geocoding, nearby facilities, and agricultural office locations
"""

import requests
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MapService:
    """
    Service class for map and location services
    """
    
    def __init__(self):
        """Initialize map service with API keys"""
        self.google_maps_key = Config.GOOGLE_MAPS_API_KEY
        self.geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        self.distance_matrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        
        # Agricultural offices database (fallback)
        self.agriculture_offices = self.load_agriculture_offices()
    
    def load_agriculture_offices(self) -> Dict:
        """
        Load agriculture office database
        
        Returns:
            Dictionary of agriculture offices by state
        """
        return {
            "kerala": [
                {
                    "name": "Krishi Bhavan - Thiruvananthapuram",
                    "address": "Vikas Bhavan P.O., Thiruvananthapuram, Kerala 695033",
                    "lat": 8.5241,
                    "lon": 76.9366,
                    "phone": "0471-2304425",
                    "email": "agri.dir@kerala.gov.in",
                    "type": "District Office"
                },
                {
                    "name": "Krishi Bhavan - Kochi",
                    "address": "Ernakulam South, Kochi, Kerala 682016",
                    "lat": 9.9816,
                    "lon": 76.2995,
                    "phone": "0484-2375234",
                    "email": "agrikochi@gmail.com",
                    "type": "Regional Office"
                },
                {
                    "name": "Krishi Bhavan - Thrissur",
                    "address": "Ayyappan Kovil Rd, Thrissur, Kerala 680001",
                    "lat": 10.5276,
                    "lon": 76.2144,
                    "phone": "0487-2320752",
                    "type": "District Office"
                },
                {
                    "name": "Krishi Bhavan - Palakkad",
                    "address": "Civil Station, Palakkad, Kerala 678001",
                    "lat": 10.7867,
                    "lon": 76.6548,
                    "phone": "0491-2505346",
                    "type": "District Office"
                },
                {
                    "name": "Agricultural Technology Management Agency",
                    "address": "Agriculture Department, Thrissur, Kerala",
                    "lat": 10.5255,
                    "lon": 76.2132,
                    "phone": "0487-2333155",
                    "type": "ATMA"
                }
            ],
            "tamil_nadu": [
                {
                    "name": "Department of Agriculture - Chennai",
                    "address": "Ezhilagam, Chepauk, Chennai 600005",
                    "lat": 13.0827,
                    "lon": 80.2707,
                    "phone": "044-28523252",
                    "email": "agri@tn.gov.in",
                    "type": "Head Office"
                },
                {
                    "name": "Agriculture Office - Coimbatore",
                    "address": "TNAU Campus, Coimbatore 641003",
                    "lat": 11.0135,
                    "lon": 76.9337,
                    "phone": "0422-6611300",
                    "type": "Regional Office"
                }
            ],
            "karnataka": [
                {
                    "name": "Department of Agriculture - Bangalore",
                    "address": "Sheshadri Road, Bangalore 560001",
                    "lat": 12.9784,
                    "lon": 77.5902,
                    "phone": "080-22254852",
                    "email": "agri@karnataka.gov.in",
                    "type": "Head Office"
                }
            ],
            "punjab": [
                {
                    "name": "Department of Agriculture - Chandigarh",
                    "address": "Sector 18-C, Chandigarh 160018",
                    "lat": 30.7562,
                    "lon": 76.7872,
                    "phone": "0172-2705156",
                    "type": "Head Office"
                }
            ]
        }
    
    def geocode_address(self, address: str) -> Optional[Dict]:
        """
        Convert address to coordinates
        
        Args:
            address: Address string
            
        Returns:
            Dictionary with location data or None
        """
        try:
            params = {
                'address': address,
                'key': self.google_maps_key
            }
            
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    location = data['results'][0]['geometry']['location']
                    formatted_address = data['results'][0]['formatted_address']
                    
                    return {
                        'latitude': location['lat'],
                        'longitude': location['lng'],
                        'formatted_address': formatted_address,
                        'place_id': data['results'][0]['place_id']
                    }
                else:
                    logger.warning(f"Geocoding failed for address: {address}")
                    return None
            else:
                logger.error(f"Geocoding API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error geocoding address: {str(e)}")
            return None
    
    def reverse_geocode(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Convert coordinates to address
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with address information
        """
        try:
            params = {
                'latlng': f"{lat},{lon}",
                'key': self.google_maps_key
            }
            
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    result = data['results'][0]
                    
                    # Extract address components
                    address_components = {}
                    for component in result.get('address_components', []):
                        for type in component.get('types', []):
                            if type in ['locality', 'administrative_area_level_1', 'country', 'postal_code']:
                                address_components[type] = component.get('long_name')
                    
                    return {
                        'formatted_address': result['formatted_address'],
                        'place_id': result['place_id'],
                        'latitude': lat,
                        'longitude': lon,
                        'city': address_components.get('locality', ''),
                        'state': address_components.get('administrative_area_level_1', ''),
                        'country': address_components.get('country', ''),
                        'postal_code': address_components.get('postal_code', '')
                    }
                else:
                    logger.warning(f"Reverse geocoding failed for coordinates: {lat}, {lon}")
                    return None
            else:
                logger.error(f"Reverse geocoding API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error reverse geocoding: {str(e)}")
            return None
    
    def find_nearby_agriculture_offices(self, 
                                       lat: float, 
                                       lon: float, 
                                       radius: int = 20000) -> List[Dict]:
        """
        Find nearby agriculture offices using Google Places API
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in meters (max 50000)
            
        Returns:
            List of nearby agriculture offices
        """
        try:
            # Try Google Places API first
            params = {
                'location': f"{lat},{lon}",
                'radius': min(radius, 50000),
                'keyword': 'krishi bhavan agriculture office',
                'key': self.google_maps_key
            }
            
            response = requests.get(self.places_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK' and data['results']:
                    offices = []
                    
                    for place in data['results'][:10]:  # Top 10 results
                        place_lat = place['geometry']['location']['lat']
                        place_lon = place['geometry']['location']['lng']
                        
                        # Calculate distance
                        distance = self.calculate_distance(lat, lon, place_lat, place_lon)
                        
                        offices.append({
                            'name': place.get('name', 'Agriculture Office'),
                            'address': place.get('vicinity', ''),
                            'place_id': place.get('place_id', ''),
                            'latitude': place_lat,
                            'longitude': place_lon,
                            'distance': round(distance, 2),
                            'distance_text': self.format_distance(distance),
                            'rating': place.get('rating', None),
                            'user_ratings_total': place.get('user_ratings_total', 0),
                            'types': place.get('types', []),
                            'source': 'google_places'
                        })
                    
                    # Sort by distance
                    offices.sort(key=lambda x: x['distance'])
                    return offices
                else:
                    logger.info("No places found via Google API, using fallback database")
                    return self.find_nearby_offices_fallback(lat, lon, radius)
            else:
                logger.error(f"Places API error: {response.status_code}")
                return self.find_nearby_offices_fallback(lat, lon, radius)
                
        except Exception as e:
            logger.error(f"Error finding nearby offices: {str(e)}")
            return self.find_nearby_offices_fallback(lat, lon, radius)
    
    def find_nearby_offices_fallback(self, lat: float, lon: float, radius: int) -> List[Dict]:
        """
        Fallback method using local database
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in meters
            
        Returns:
            List of nearby offices from database
        """
        try:
            # Get state from coordinates
            location_info = self.reverse_geocode(lat, lon)
            if not location_info:
                return []
            
            state = location_info.get('state', '').lower()
            
            # Find matching state in database
            for state_key, offices in self.agriculture_offices.items():
                if state_key in state or state in state_key:
                    nearby_offices = []
                    
                    for office in offices:
                        # Calculate distance
                        distance = self.calculate_distance(
                            lat, lon, 
                            office['lat'], office['lon']
                        )
                        
                        if distance <= radius / 1000:  # Convert radius to km
                            office_copy = office.copy()
                            office_copy['distance'] = round(distance, 2)
                            office_copy['distance_text'] = self.format_distance(distance)
                            office_copy['source'] = 'database'
                            nearby_offices.append(office_copy)
                    
                    # Sort by distance
                    nearby_offices.sort(key=lambda x: x['distance'])
                    return nearby_offices[:10]
            
            return []
            
        except Exception as e:
            logger.error(f"Error in fallback search: {str(e)}")
            return []
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        
        Args:
            lat1: Latitude of point 1
            lon1: Longitude of point 1
            lat2: Latitude of point 2
            lon2: Longitude of point 2
            
        Returns:
            Distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def format_distance(self, distance_km: float) -> str:
        """
        Format distance for display
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Formatted distance string
        """
        if distance_km < 1:
            return f"{int(distance_km * 1000)} meters"
        elif distance_km < 10:
            return f"{distance_km:.1f} km"
        else:
            return f"{int(distance_km)} km"
    
    def get_distance_matrix(self, 
                          origins: List[Tuple[float, float]], 
                          destinations: List[Tuple[float, float]]) -> Optional[Dict]:
        """
        Get distance and time matrix between points
        
        Args:
            origins: List of (lat, lon) origin coordinates
            destinations: List of (lat, lon) destination coordinates
            
        Returns:
            Distance matrix data
        """
        try:
            origin_str = '|'.join([f"{lat},{lon}" for lat, lon in origins])
            dest_str = '|'.join([f"{lat},{lon}" for lat, lon in destinations])
            
            params = {
                'origins': origin_str,
                'destinations': dest_str,
                'key': self.google_maps_key,
                'units': 'metric'
            }
            
            response = requests.get(self.distance_matrix_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK':
                    return data
                else:
                    logger.error(f"Distance Matrix API error: {data['status']}")
                    return None
            else:
                logger.error(f"Distance Matrix API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting distance matrix: {str(e)}")
            return None
    
    def get_map_static_url(self, 
                          lat: float, 
                          lon: float, 
                          markers: Optional[List[Dict]] = None,
                          zoom: int = 12,
                          width: int = 600,
                          height: int = 400) -> str:
        """
        Generate static map URL
        
        Args:
            lat: Center latitude
            lon: Center longitude
            markers: List of marker locations
            zoom: Zoom level (0-21)
            width: Image width
            height: Image height
            
        Returns:
            Static map URL
        """
        base_url = "https://maps.googleapis.com/maps/api/staticmap"
        
        params = {
            'center': f"{lat},{lon}",
            'zoom': zoom,
            'size': f"{width}x{height}",
            'key': self.google_maps_key
        }
        
        # Add markers
        if markers:
            marker_str = []
            for marker in markers:
                color = marker.get('color', 'red')
                label = marker.get('label', '')
                marker_lat = marker.get('lat', lat)
                marker_lon = marker.get('lon', lon)
                
                if label:
                    marker_str.append(f"color:{color}|label:{label}|{marker_lat},{marker_lon}")
                else:
                    marker_str.append(f"color:{color}|{marker_lat},{marker_lon}")
            
            if marker_str:
                params['markers'] = '|'.join(marker_str)
        
        # Build URL
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def get_location_suggestions(self, query: str) -> List[Dict]:
        """
        Get location autocomplete suggestions
        
        Args:
            query: Partial location query
            
        Returns:
            List of location suggestions
        """
        try:
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                'input': query,
                'types': '(regions)',
                'key': self.google_maps_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK':
                    suggestions = []
                    
                    for prediction in data.get('predictions', [])[:10]:
                        suggestions.append({
                            'description': prediction.get('description', ''),
                            'place_id': prediction.get('place_id', ''),
                            'types': prediction.get('types', [])
                        })
                    
                    return suggestions
                else:
                    logger.error(f"Places API error: {data['status']}")
                    return []
            else:
                logger.error(f"Places API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting suggestions: {str(e)}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information about a place
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Place details
        """
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,geometry,formatted_phone_number,website,opening_hours,rating',
                'key': self.google_maps_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'OK':
                    result = data['result']
                    return {
                        'name': result.get('name', ''),
                        'address': result.get('formatted_address', ''),
                        'phone': result.get('formatted_phone_number', ''),
                        'website': result.get('website', ''),
                        'latitude': result.get('geometry', {}).get('location', {}).get('lat'),
                        'longitude': result.get('geometry', {}).get('location', {}).get('lng'),
                        'rating': result.get('rating'),
                        'opening_hours': result.get('opening_hours', {}).get('weekday_text', [])
                    }
                else:
                    logger.error(f"Place Details API error: {data['status']}")
                    return None
            else:
                logger.error(f"Place Details API error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting place details: {str(e)}")
            return None
    
    def get_farming_regions(self, lat: float, lon: float) -> Dict:
        """
        Get information about farming regions
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Farming region information
        """
        # This is a simplified version. In production, you might want to
        # integrate with soil databases or agricultural zoning maps
        
        # Major agricultural regions in India (simplified)
        regions = {
            'north': {
                'states': ['punjab', 'haryana', 'uttar pradesh'],
                'major_crops': ['wheat', 'rice', 'sugarcane'],
                'soil_type': 'alluvial'
            },
            'south': {
                'states': ['tamil nadu', 'kerala', 'karnataka', 'andhra pradesh'],
                'major_crops': ['rice', 'coconut', 'cotton', 'sugarcane'],
                'soil_type': 'laterite, red'
            },
            'west': {
                'states': ['gujarat', 'maharashtra', 'rajasthan'],
                'major_crops': ['cotton', 'groundnut', 'bajra'],
                'soil_type': 'black, desert'
            },
            'east': {
                'states': ['west bengal', 'odisha', 'bihar', 'assam'],
                'major_crops': ['rice', 'jute', 'tea'],
                'soil_type': 'alluvial, deltaic'
            }
        }
        
        # Get location info
        location = self.reverse_geocode(lat, lon)
        
        if not location:
            return {
                'region': 'Unknown',
                'major_crops': [],
                'soil_type': 'Unknown'
            }
        
        state = location.get('state', '').lower()
        
        # Find region
        for region_name, region_info in regions.items():
            for region_state in region_info['states']:
                if region_state in state:
                    return {
                        'region': region_name.title(),
                        'state': location.get('state'),
                        'major_crops': region_info['major_crops'],
                        'soil_type': region_info['soil_type'],
                        'climate': self.get_climate_zone(lat, lon)
                    }
        
        return {
            'region': 'Other',
            'state': location.get('state'),
            'major_crops': ['rice', 'wheat'],  # Default
            'soil_type': 'varies'
        }
    
    def get_climate_zone(self, lat: float, lon: float) -> str:
        """
        Determine climate zone based on coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Climate zone name
        """
        # Simplified climate zones for India
        if 8.0 <= lat <= 12.0:
            return "Tropical (South)"
        elif 12.0 < lat <= 20.0:
            return "Tropical (Central)"
        elif 20.0 < lat <= 28.0:
            return "Subtropical (North)"
        elif 28.0 < lat <= 35.0:
            return "Temperate (Himalayan)"
        else:
            return "Unknown"
    
    def get_service_status(self) -> Dict:
        """
        Get service status
        
        Returns:
            Service status information
        """
        return {
            'service': 'map_service',
            'google_maps_api': 'configured' if self.google_maps_key != 'your_api_key_here' else 'not_configured',
            'offices_in_database': sum(len(offices) for offices in self.agriculture_offices.values()),
            'states_covered': list(self.agriculture_offices.keys()),
            'timestamp': datetime.now().isoformat()
        }
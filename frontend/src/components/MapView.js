import React, { useState, useEffect, useRef } from 'react';
import { MapPin, Navigation, Phone, Clock, Star, ExternalLink, Loader, Search, X, AlertCircle } from 'lucide-react';

const MapView = () => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [selectedOffice, setSelectedOffice] = useState(null);
  const [userLocation, setUserLocation] = useState(null);
  const [offices, setOffices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [locationLoading, setLocationLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [locationDenied, setLocationDenied] = useState(false);
  const [mapsError, setMapsError] = useState(false);
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const [apiKeyMissing, setApiKeyMissing] = useState(false);

  // Get API key from environment
  const googleMapsApiKey = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;

  // Mock data for agriculture offices (fallback)
  const mockOffices = [
    {
      id: 1,
      name: "Krishi Bhavan - Thrissur",
      address: "Ayyappan Kovil Rd, Thrissur, Kerala 680001",
      latitude: 10.5276,
      longitude: 76.2144,
      phone: "0487-2320752",
      type: "District Office",
      rating: 4.3,
      hours: "Mon-Sat: 9:00 AM - 5:00 PM"
    },
    {
      id: 2,
      name: "Agricultural Technology Management Agency",
      address: "Agriculture Department, Thrissur, Kerala",
      latitude: 10.5255,
      longitude: 76.2132,
      phone: "0487-2333155",
      type: "ATMA",
      rating: 4.1,
      hours: "Mon-Fri: 10:00 AM - 4:00 PM"
    },
    {
      id: 3,
      name: "Krishi Bhavan - Kochi",
      address: "Ernakulam South, Kochi, Kerala 682016",
      latitude: 9.9816,
      longitude: 76.2995,
      phone: "0484-2375234",
      type: "Regional Office",
      rating: 4.5,
      hours: "Mon-Sat: 9:30 AM - 5:30 PM"
    },
    {
      id: 4,
      name: "Krishi Bhavan - Palakkad",
      address: "Civil Station, Palakkad, Kerala 678001",
      latitude: 10.7867,
      longitude: 76.6548,
      phone: "0491-2505346",
      type: "District Office",
      rating: 4.2,
      hours: "Mon-Sat: 9:00 AM - 5:00 PM"
    },
    {
      id: 5,
      name: "Krishi Bhavan - Thiruvananthapuram",
      address: "Vikas Bhavan P.O., Thiruvananthapuram, Kerala 695033",
      latitude: 8.5241,
      longitude: 76.9366,
      phone: "0471-2304425",
      type: "Head Office",
      rating: 4.4,
      hours: "Mon-Fri: 9:00 AM - 6:00 PM"
    }
  ];

  // Check API key on mount
  useEffect(() => {
    if (!googleMapsApiKey || googleMapsApiKey === 'your_api_key_here') {
      console.error('Google Maps API key is missing or invalid');
      setApiKeyMissing(true);
      setMapsError(true);
      setLoading(false);
    }
  }, [googleMapsApiKey]);

  // Load Google Maps script dynamically
  useEffect(() => {
    if (apiKeyMissing || !googleMapsApiKey) return;

    // If already loaded, set loaded state
    if (window.google && window.google.maps) {
      console.log('Google Maps already loaded');
      setMapsLoaded(true);
      setMapsError(false);
      return;
    }

    // Check if script is already being loaded
    const existingScript = document.querySelector('script[src*="maps.googleapis"]');
    if (existingScript) {
      console.log('Google Maps script already loading, waiting...');
      const checkInterval = setInterval(() => {
        if (window.google && window.google.maps) {
          console.log('Google Maps loaded successfully');
          setMapsLoaded(true);
          setMapsError(false);
          clearInterval(checkInterval);
        }
      }, 500);
      
      setTimeout(() => {
        clearInterval(checkInterval);
        if (!window.google || !window.google.maps) {
          console.error('Google Maps load timeout');
          setMapsError(true);
          setLoading(false);
        }
      }, 10000);
      
      return;
    }

    // Load the script
    console.log('Loading Google Maps script with API key...');
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&libraries=places&callback=initMap`;
    script.async = true;
    script.defer = true;

    // Define callback
    window.initMap = function() {
      console.log('Google Maps loaded via callback');
      setMapsLoaded(true);
      setMapsError(false);
    };

    script.addEventListener('load', () => {
      console.log('Google Maps script loaded');
      // If callback hasn't fired yet, check manually
      if (window.google && window.google.maps) {
        setMapsLoaded(true);
        setMapsError(false);
      }
    });

    script.addEventListener('error', (error) => {
      console.error('Failed to load Google Maps script:', error);
      setMapsError(true);
      setLoading(false);
    });

    document.head.appendChild(script);

    // Cleanup
    return () => {
      // Optional: remove script if needed
    };
  }, [googleMapsApiKey, apiKeyMissing]);

  // Get user's location on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          setLocationDenied(false);
          setLocationLoading(false);
          
          // Load nearby offices based on location
          loadNearbyOffices(position.coords.latitude, position.coords.longitude);
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationDenied(true);
          setLocationLoading(false);
          // Use default location (Kerala, India)
          const defaultLat = 10.5276;
          const defaultLng = 76.2144;
          setUserLocation({ lat: defaultLat, lng: defaultLng });
          loadNearbyOffices(defaultLat, defaultLng);
        }
      );
    } else {
      setLocationDenied(true);
      setLocationLoading(false);
      // Use default location
      const defaultLat = 10.5276;
      const defaultLng = 76.2144;
      setUserLocation({ lat: defaultLat, lng: defaultLng });
      loadNearbyOffices(defaultLat, defaultLng);
    }
  }, []);

  // Load nearby offices (simulated API call)
  const loadNearbyOffices = (lat, lng) => {
    setLoading(true);
    setError(null);
    
    // Simulate API delay
    setTimeout(() => {
      try {
        // Sort offices by distance from user
        const officesWithDistance = mockOffices.map(office => ({
          ...office,
          distance: calculateDistance(lat, lng, office.latitude, office.longitude)
        }));
        
        // Sort by distance
        officesWithDistance.sort((a, b) => a.distance - b.distance);
        
        setOffices(officesWithDistance);
        setLoading(false);
      } catch (err) {
        console.error('Error loading offices:', err);
        setError('Failed to load nearby offices');
        setLoading(false);
      }
    }, 1000);
  };

  // Initialize map when user location is available and maps are loaded
  useEffect(() => {
    if (!userLocation || !mapsLoaded || !mapRef.current || mapsError) return;

    try {
      const mapOptions = {
        center: userLocation,
        zoom: 10,
        styles: [
          {
            featureType: 'poi',
            elementType: 'labels',
            stylers: [{ visibility: 'off' }]
          }
        ],
        mapTypeControl: true,
        fullscreenControl: true,
        streetViewControl: false,
        zoomControl: true
      };

      const newMap = new window.google.maps.Map(mapRef.current, mapOptions);
      setMap(newMap);

      // Add user location marker
      addUserLocationMarker(newMap);
    } catch (err) {
      console.error('Error initializing map:', err);
      setMapsError(true);
    }

  }, [userLocation, mapsLoaded, mapsError]);

  // Add markers when map is ready and offices are loaded
  useEffect(() => {
    if (!map || !mapsLoaded || offices.length === 0 || mapsError) return;

    try {
      // Clear existing markers
      markers.forEach(marker => marker.setMap(null));
      
      const newMarkers = offices.map((office, index) => {
        const marker = new window.google.maps.Marker({
          position: { lat: office.latitude, lng: office.longitude },
          map: map,
          title: office.name,
          animation: window.google.maps.Animation.DROP,
          icon: {
            url: index === 0 
              ? 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
              : 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            scaledSize: new window.google.maps.Size(40, 40)
          }
        });

        // Add info window
        const infoWindow = new window.google.maps.InfoWindow({
          content: createInfoWindowContent(office)
        });

        marker.addListener('click', () => {
          infoWindow.open(map, marker);
          setSelectedOffice(office);
        });

        return marker;
      });

      setMarkers(newMarkers);

      // Fit bounds to show all markers
      if (offices.length > 0) {
        const bounds = new window.google.maps.LatLngBounds();
        bounds.extend(userLocation);
        offices.forEach(office => {
          bounds.extend({ lat: office.latitude, lng: office.longitude });
        });
        map.fitBounds(bounds);
      }
    } catch (err) {
      console.error('Error adding markers:', err);
      setMapsError(true);
    }

  }, [map, offices, mapsLoaded, userLocation, mapsError]);

  const addUserLocationMarker = (mapInstance) => {
    if (!userLocation) return;

    new window.google.maps.Marker({
      position: userLocation,
      map: mapInstance,
      title: 'Your Location',
      icon: {
        path: window.google.maps.SymbolPath.CIRCLE,
        scale: 10,
        fillColor: '#4285F4',
        fillOpacity: 1,
        strokeColor: '#FFFFFF',
        strokeWeight: 2,
      },
      zIndex: 999
    });
  };

  const createInfoWindowContent = (office) => {
    return `
      <div style="padding: 12px; max-width: 250px;">
        <h3 style="font-weight: bold; margin-bottom: 8px; color: #333;">${office.name}</h3>
        <p style="color: #666; margin-bottom: 5px; font-size: 13px;">${office.address}</p>
        ${office.phone ? `<p style="color: #666; margin-bottom: 5px; font-size: 13px;">📞 ${office.phone}</p>` : ''}
        ${office.distance ? `<p style="color: #666; margin-bottom: 8px; font-size: 13px;">📍 ${office.distance.toFixed(2)} km away</p>` : ''}
        <a href="https://www.google.com/maps/dir/?api=1&destination=${office.latitude},${office.longitude}" 
           target="_blank" 
           rel="noopener noreferrer"
           style="color: #4CAF50; text-decoration: none; font-size: 13px; display: inline-block; margin-top: 5px;">
          Get Directions →
        </a>
      </div>
    `;
  };

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Earth's radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  };

  const getUserLocation = () => {
    setLocationLoading(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const newLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(newLocation);
          setLocationDenied(false);
          setLocationLoading(false);
          
          // Center map on new location
          if (map) {
            map.setCenter(newLocation);
            map.setZoom(12);
          }
          
          // Reload nearby offices
          loadNearbyOffices(newLocation.lat, newLocation.lng);
        },
        (error) => {
          console.error('Error getting location:', error);
          setLocationDenied(true);
          setLocationLoading(false);
        }
      );
    }
  };

  const getDirections = (office) => {
    if (!userLocation) {
      alert('Please enable location services to get directions');
      return;
    }

    const url = `https://www.google.com/maps/dir/?api=1&origin=${userLocation.lat},${userLocation.lng}&destination=${office.latitude},${office.longitude}`;
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const searchLocation = async () => {
    if (!searchQuery.trim() || !window.google || mapsError) return;

    setLoading(true);
    try {
      const geocoder = new window.google.maps.Geocoder();
      geocoder.geocode({ address: searchQuery }, (results, status) => {
        if (status === 'OK' && results[0]) {
          const location = results[0].geometry.location;
          const newLocation = { lat: location.lat(), lng: location.lng() };
          
          // Update map
          if (map) {
            map.setCenter(newLocation);
            map.setZoom(12);
          }
          
          // Load offices near searched location
          loadNearbyOffices(newLocation.lat, newLocation.lng);
          setSearchQuery('');
        } else {
          alert('Location not found');
        }
        setLoading(false);
      });
    } catch (error) {
      console.error('Error searching location:', error);
      setLoading(false);
    }
  };

  if (locationLoading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-12 text-center">
        <Loader className="h-12 w-12 animate-spin text-green-600 mx-auto mb-4" />
        <p className="text-gray-600">Getting your location...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header - Always visible */}
      <div className="p-6 bg-gradient-to-r from-green-50 to-emerald-50 border-b">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900 flex items-center">
            <MapPin className="h-6 w-6 text-green-600 mr-2" />
            Nearby Agricultural Offices
          </h2>
          
          <button
            onClick={getUserLocation}
            disabled={locationLoading}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {locationLoading ? (
              <Loader className="h-4 w-4 animate-spin mr-2" />
            ) : (
              <Navigation className="h-4 w-4 mr-2" />
            )}
            My Location
          </button>
        </div>

        {/* Location Status */}
        {locationDenied && (
          <div className="mb-4 p-3 bg-yellow-50 rounded-lg flex items-center text-yellow-700">
            <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0" />
            <span className="text-sm">Location access denied. Showing default location.</span>
          </div>
        )}

        {/* Search Bar */}
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search for a location..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && searchLocation()}
              disabled={mapsError}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-100"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2"
              >
                <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
              </button>
            )}
          </div>
          <button
            onClick={searchLocation}
            disabled={loading || mapsError}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            Search
          </button>
        </div>

        {/* API Key Missing Warning - Shows within the header */}
        {apiKeyMissing && (
          <div className="mt-4 p-4 bg-red-50 rounded-lg flex items-start text-red-700">
            <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Google Maps API Key Missing</p>
              <p className="text-sm mt-1">Please add your Google Maps API key to the .env file:</p>
              <div className="bg-white p-2 rounded mt-2 text-sm font-mono">
                REACT_APP_GOOGLE_MAPS_API_KEY=your_api_key_here
              </div>
            </div>
          </div>
        )}

        {/* Maps Error Warning */}
        {mapsError && !apiKeyMissing && (
          <div className="mt-4 p-4 bg-yellow-50 rounded-lg flex items-start text-yellow-700">
            <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium">Google Maps Failed to Load</p>
              <p className="text-sm mt-1">Unable to load Google Maps. Showing list view instead.</p>
            </div>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 bg-red-50 border-b flex items-center text-red-700">
          <AlertCircle className="h-5 w-5 mr-2 flex-shrink-0" />
          <span className="flex-1">{error}</span>
          <button onClick={() => setError(null)} className="text-red-500 hover:text-red-700">
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Map Container - Only show if maps loaded successfully */}
      {!apiKeyMissing && !mapsError && (
        <div 
          ref={mapRef} 
          style={{ height: '400px', width: '100%' }}
          className="relative bg-gray-100"
        >
          {!mapsLoaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
              <div className="text-center">
                <Loader className="h-8 w-8 animate-spin text-green-600 mx-auto mb-2" />
                <p className="text-gray-600">Loading Google Maps...</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Offices List - Always visible */}
      <div className="border-t max-h-96 overflow-y-auto">
        <div className="p-4 bg-gray-50 border-b">
          <h3 className="font-medium text-gray-700">
            {loading ? 'Loading offices...' : `Found ${offices.length} nearby offices`}
          </h3>
        </div>
        
        {loading ? (
          <div className="p-8 text-center">
            <Loader className="h-8 w-8 animate-spin text-green-600 mx-auto mb-2" />
            <p className="text-gray-600">Finding nearby agricultural offices...</p>
          </div>
        ) : offices.length === 0 ? (
          <div className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-600">No agricultural offices found nearby</p>
          </div>
        ) : (
          <div className="divide-y">
            {offices.map((office) => (
              <div
                key={office.id}
                className={`p-4 hover:bg-gray-50 cursor-pointer transition-colors ${
                  selectedOffice?.id === office.id ? 'bg-green-50' : ''
                }`}
                onClick={() => {
                  setSelectedOffice(office);
                  if (map && !mapsError) {
                    map.setCenter({ lat: office.latitude, lng: office.longitude });
                    map.setZoom(15);
                  }
                }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{office.name}</h4>
                    <p className="text-sm text-gray-600 mt-1">{office.address}</p>
                    
                    <div className="flex flex-wrap items-center gap-4 mt-2">
                      {office.distance && (
                        <span className="text-xs text-gray-500 flex items-center">
                          <Navigation className="h-3 w-3 mr-1" />
                          {office.distance.toFixed(2)} km
                        </span>
                      )}
                      {office.phone && (
                        <span className="text-xs text-gray-500 flex items-center">
                          <Phone className="h-3 w-3 mr-1" />
                          {office.phone}
                        </span>
                      )}
                      {office.rating && (
                        <span className="text-xs text-gray-500 flex items-center">
                          <Star className="h-3 w-3 mr-1 text-yellow-400 fill-current" />
                          {office.rating}
                        </span>
                      )}
                      {office.hours && (
                        <span className="text-xs text-gray-500 flex items-center">
                          <Clock className="h-3 w-3 mr-1" />
                          {office.hours}
                        </span>
                      )}
                    </div>
                    
                    <span className="inline-block mt-2 text-xs px-2 py-1 bg-green-100 text-green-800 rounded-full">
                      {office.type}
                    </span>
                  </div>
                  
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      getDirections(office);
                    }}
                    className="ml-4 p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                    title="Get directions"
                  >
                    <ExternalLink className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selected Office Details */}
      {selectedOffice && (
        <div className="p-4 bg-green-50 border-t">
          <div className="flex items-start justify-between mb-3">
            <div>
              <h4 className="font-semibold text-gray-900">{selectedOffice.name}</h4>
              <p className="text-sm text-gray-700 mt-1">{selectedOffice.address}</p>
              
              {selectedOffice.phone && (
                <p className="text-sm text-gray-700 mt-2 flex items-center">
                  <Phone className="h-4 w-4 mr-2" />
                  {selectedOffice.phone}
                </p>
              )}
              
              {selectedOffice.hours && (
                <p className="text-sm text-gray-700 mt-1 flex items-center">
                  <Clock className="h-4 w-4 mr-2" />
                  {selectedOffice.hours}
                </p>
              )}
              
              {selectedOffice.distance && (
                <p className="text-sm text-gray-700 mt-1 flex items-center">
                  <Navigation className="h-4 w-4 mr-2" />
                  {selectedOffice.distance.toFixed(2)} km away
                </p>
              )}
            </div>
            
            <button
              onClick={() => setSelectedOffice(null)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          
          <div className="flex gap-3">
            <a
              href={`https://www.google.com/maps/dir/?api=1&destination=${selectedOffice.latitude},${selectedOffice.longitude}`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 text-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Get Directions
            </a>
            {selectedOffice.phone && (
              <a
                href={`tel:${selectedOffice.phone}`}
                className="flex-1 text-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Call
              </a>
            )}
          </div>
        </div>
      )}

      {/* Map Legend */}
      {!apiKeyMissing && !mapsError && (
        <div className="p-3 bg-gray-50 border-t text-xs text-gray-500 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-blue-500 rounded-full mr-1"></div>
              <span>Your Location</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-1"></div>
              <span>Nearest Office</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-500 rounded-full mr-1"></div>
              <span>Other Offices</span>
            </div>
          </div>
          <span>Powered by Google Maps</span>
        </div>
      )}
    </div>
  );
};

export default MapView;
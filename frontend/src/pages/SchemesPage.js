import React, { useState, useEffect } from 'react';
import { Award, MapPin, Leaf, Search, Loader, AlertCircle } from 'lucide-react';
import { getSchemeRecommendations, searchSchemes } from '../services/api';

const SchemeCard = () => {
  const [loading, setLoading] = useState(false);
  const [schemes, setSchemes] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    state: 'Kerala',
    cropType: '',
    disease: ''
  });

  // Load default schemes on mount
  useEffect(() => {
    fetchSchemes();
  }, []);

  const fetchSchemes = async () => {
    setLoading(true);
    try {
      const response = await getSchemeRecommendations(
        filters.state,
        filters.cropType || undefined,
        filters.disease || undefined
      );
      setSchemes(response.schemes || []);
    } catch (error) {
      console.error('Error fetching schemes:', error);
      // Set mock data for demonstration
      setSchemes([
        {
          id: 1,
          name: 'PM Kisan Samman Nidhi',
          description: 'Income support of ₹6000 per year for farmers',
          eligibility: ['Small and marginal farmers'],
          benefits: ['₹2000 per installment', 'Direct bank transfer'],
          type: 'income_support'
        },
        {
          id: 2,
          name: 'Pradhan Mantri Fasal Bima Yojana',
          description: 'Crop insurance scheme for farmers',
          eligibility: ['All farmers growing notified crops'],
          benefits: ['Insurance coverage', 'Low premium rates'],
          type: 'insurance'
        },
        {
          id: 3,
          name: 'Kisan Credit Card',
          description: 'Affordable credit for farmers',
          eligibility: ['All farmers'],
          benefits: ['Short-term loans', 'Flexible repayment'],
          type: 'credit'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchSchemes();
      return;
    }
    
    setLoading(true);
    try {
      const response = await searchSchemes(searchQuery);
      setSchemes(response.schemes || []);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTypeIcon = (type) => {
    switch(type) {
      case 'insurance': return '🛡️';
      case 'income_support': return '💰';
      case 'credit': return '💳';
      case 'subsidy': return '🏷️';
      default: return '📄';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="p-6 bg-gradient-to-r from-green-50 to-green-100 border-b">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Government Schemes</h2>
        
        {/* Search Bar */}
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search schemes..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Search
          </button>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-3 gap-4 mt-4">
          <select
            value={filters.state}
            onChange={(e) => setFilters({...filters, state: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="Kerala">Kerala</option>
            <option value="Tamil Nadu">Tamil Nadu</option>
            <option value="Karnataka">Karnataka</option>
            <option value="Maharashtra">Maharashtra</option>
            <option value="Punjab">Punjab</option>
          </select>
          
          <select
            value={filters.cropType}
            onChange={(e) => setFilters({...filters, cropType: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg"
          >
            <option value="">All Crops</option>
            <option value="rice">Rice</option>
            <option value="wheat">Wheat</option>
            <option value="cotton">Cotton</option>
            <option value="sugarcane">Sugarcane</option>
          </select>
          
          <button
            onClick={fetchSchemes}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
          >
            Apply Filters
          </button>
        </div>
      </div>

      {/* Schemes List */}
      <div className="p-6 max-h-[600px] overflow-y-auto">
        {loading ? (
          <div className="text-center py-8">
            <Loader className="h-8 w-8 animate-spin text-green-600 mx-auto mb-4" />
            <p className="text-gray-600">Loading schemes...</p>
          </div>
        ) : schemes.length === 0 ? (
          <div className="text-center py-8">
            <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No schemes found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {schemes.map((scheme) => (
              <div key={scheme.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <span className="text-2xl mr-2">{getTypeIcon(scheme.type)}</span>
                      <h3 className="font-semibold text-gray-900">{scheme.name}</h3>
                    </div>
                    <p className="text-gray-600 text-sm mb-3">{scheme.description}</p>
                    
                    {scheme.eligibility && scheme.eligibility.length > 0 && (
                      <div className="mb-2">
                        <span className="text-xs font-semibold text-gray-700">Eligibility:</span>
                        <ul className="text-xs text-gray-600 list-disc list-inside">
                          {scheme.eligibility.slice(0, 2).map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    {scheme.benefits && scheme.benefits.length > 0 && (
                      <div>
                        <span className="text-xs font-semibold text-gray-700">Benefits:</span>
                        <ul className="text-xs text-gray-600 list-disc list-inside">
                          {scheme.benefits.slice(0, 2).map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                  
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                    {scheme.type?.replace('_', ' ')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-4 bg-gray-50 border-t text-center text-sm text-gray-600">
        Showing {schemes.length} schemes • Updated regularly
      </div>
    </div>
  );
};

export default SchemeCard;
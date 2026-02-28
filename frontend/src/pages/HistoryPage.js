import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Calendar,
  Filter,
  Download,
  ChevronLeft,
  ChevronRight,
  Search,
  X,
  Eye,
  Trash2,
  ArrowUpDown,
  Leaf,
  AlertTriangle,
  CheckCircle,
  Clock,
  MapPin,
  Thermometer,
  Droplets
} from 'lucide-react';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedItems, setSelectedItems] = useState([]);
  const [filterOpen, setFilterOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [sortConfig, setSortConfig] = useState({ key: 'date', direction: 'desc' });
  const [filters, setFilters] = useState({
    cropType: 'all',
    diseaseType: 'all',
    dateRange: 'all',
    riskLevel: 'all'
  });

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setHistory(mockHistoryData);
      setFilteredHistory(mockHistoryData);
      setLoading(false);
    }, 1500);
  }, []);

  useEffect(() => {
    // Apply filters and search
    let filtered = [...history];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.crop.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.disease.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.location.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Crop type filter
    if (filters.cropType !== 'all') {
      filtered = filtered.filter(item => item.crop === filters.cropType);
    }

    // Disease type filter
    if (filters.diseaseType !== 'all') {
      filtered = filtered.filter(item => item.disease === filters.diseaseType);
    }

    // Risk level filter
    if (filters.riskLevel !== 'all') {
      filtered = filtered.filter(item => item.weatherRisk === filters.riskLevel);
    }

    // Date range filter
    if (filters.dateRange !== 'all') {
      const now = new Date();
      const daysAgo = {
        '7': 7,
        '30': 30,
        '90': 90
      }[filters.dateRange];

      if (daysAgo) {
        const cutoff = new Date(now.setDate(now.getDate() - daysAgo));
        filtered = filtered.filter(item => new Date(item.date) >= cutoff);
      }
    }

    // Apply sorting
    filtered.sort((a, b) => {
      if (sortConfig.key === 'date') {
        return sortConfig.direction === 'asc'
          ? new Date(a.date) - new Date(b.date)
          : new Date(b.date) - new Date(a.date);
      }
      if (sortConfig.key === 'confidence') {
        return sortConfig.direction === 'asc'
          ? a.confidence - b.confidence
          : b.confidence - a.confidence;
      }
      return 0;
    });

    setFilteredHistory(filtered);
    setCurrentPage(1);
  }, [searchTerm, filters, history, sortConfig]);

  const mockHistoryData = [
    {
      id: 1,
      date: '2024-01-15T10:30:00',
      image: '/images/rice-1.jpg',
      crop: 'Rice',
      disease: 'Rice Blast',
      confidence: 95,
      severity: 'high',
      weatherRisk: 'HIGH',
      location: 'Thrissur, Kerala',
      temperature: 32,
      humidity: 85,
      recommendations: ['Apply Tricyclazole', 'Reduce nitrogen fertilizer']
    },
    {
      id: 2,
      date: '2024-01-14T14:20:00',
      image: '/images/wheat-1.jpg',
      crop: 'Wheat',
      disease: 'Healthy',
      confidence: 98,
      severity: 'healthy',
      weatherRisk: 'LOW',
      location: 'Thrissur, Kerala',
      temperature: 30,
      humidity: 65,
      recommendations: ['Continue regular monitoring']
    },
    {
      id: 3,
      date: '2024-01-13T09:15:00',
      image: '/images/cotton-1.jpg',
      crop: 'Cotton',
      disease: 'Leaf Curl',
      confidence: 87,
      severity: 'medium',
      weatherRisk: 'MEDIUM',
      location: 'Palakkad, Kerala',
      temperature: 34,
      humidity: 72,
      recommendations: ['Apply imidacloprid', 'Remove infected plants']
    },
    {
      id: 4,
      date: '2024-01-12T16:45:00',
      image: '/images/sugarcane-1.jpg',
      crop: 'Sugarcane',
      disease: 'Red Rot',
      confidence: 92,
      severity: 'high',
      weatherRisk: 'HIGH',
      location: 'Kozhikode, Kerala',
      temperature: 31,
      humidity: 88,
      recommendations: ['Use resistant varieties', 'Improve drainage']
    },
    {
      id: 5,
      date: '2024-01-11T11:30:00',
      image: '/images/rice-2.jpg',
      crop: 'Rice',
      disease: 'Brown Spot',
      confidence: 82,
      severity: 'medium',
      weatherRisk: 'MEDIUM',
      location: 'Ernakulam, Kerala',
      temperature: 33,
      humidity: 78,
      recommendations: ['Apply Mancozeb', 'Balance soil nutrients']
    },
    {
      id: 6,
      date: '2024-01-10T13:20:00',
      image: '/images/banana-1.jpg',
      crop: 'Banana',
      disease: 'Panama Wilt',
      confidence: 94,
      severity: 'high',
      weatherRisk: 'HIGH',
      location: 'Thrissur, Kerala',
      temperature: 35,
      humidity: 82,
      recommendations: ['Remove infected plants', 'Soil solarization']
    },
    {
      id: 7,
      date: '2024-01-09T10:00:00',
      image: '/images/coconut-1.jpg',
      crop: 'Coconut',
      disease: 'Healthy',
      confidence: 96,
      severity: 'healthy',
      weatherRisk: 'LOW',
      location: 'Alappuzha, Kerala',
      temperature: 29,
      humidity: 70,
      recommendations: ['Continue maintenance']
    },
    {
      id: 8,
      date: '2024-01-08T15:40:00',
      image: '/images/rice-3.jpg',
      crop: 'Rice',
      disease: 'Sheath Blight',
      confidence: 88,
      severity: 'medium',
      weatherRisk: 'MEDIUM',
      location: 'Thrissur, Kerala',
      temperature: 31,
      humidity: 76,
      recommendations: ['Apply fungicides', 'Improve air circulation']
    }
  ];

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return 'text-red-600 bg-red-100';
      case 'medium': return 'text-orange-600 bg-orange-100';
      case 'healthy': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getRiskColor = (risk) => {
    switch(risk) {
      case 'HIGH': return 'text-red-600 bg-red-100';
      case 'MEDIUM': return 'text-orange-600 bg-orange-100';
      case 'LOW': return 'text-green-600 bg-green-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleSelectAll = () => {
    if (selectedItems.length === currentItems.length) {
      setSelectedItems([]);
    } else {
      setSelectedItems(currentItems.map(item => item.id));
    }
  };

  const handleSelectItem = (id) => {
    if (selectedItems.includes(id)) {
      setSelectedItems(selectedItems.filter(itemId => itemId !== id));
    } else {
      setSelectedItems([...selectedItems, id]);
    }
  };

  const handleDelete = (ids) => {
    if (window.confirm(`Delete ${ids.length} item(s)?`)) {
      setHistory(history.filter(item => !ids.includes(item.id)));
      setSelectedItems([]);
    }
  };

  const handleExport = () => {
    const dataToExport = selectedItems.length > 0
      ? history.filter(item => selectedItems.includes(item.id))
      : filteredHistory;

    const csv = [
      ['Date', 'Crop', 'Disease', 'Confidence', 'Weather Risk', 'Location', 'Temperature', 'Humidity'],
      ...dataToExport.map(item => [
        item.date,
        item.crop,
        item.disease,
        `${item.confidence}%`,
        item.weatherRisk,
        item.location,
        `${item.temperature}°C`,
        `${item.humidity}%`
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartagriai_history_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  // Pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredHistory.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);

  const requestSort = (key) => {
    setSortConfig({
      key,
      direction: sortConfig.key === key && sortConfig.direction === 'asc' ? 'desc' : 'asc'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-green-500 border-t-transparent mb-4"></div>
          <p className="text-gray-600">Loading your history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Detection History</h1>
          <p className="text-gray-600">
            View and manage all your past crop disease detections
          </p>
        </div>

        {/* Filters Bar */}
        <div className="bg-white rounded-xl shadow-sm p-4 mb-6">
          <div className="flex flex-wrap items-center gap-4">
            {/* Search */}
            <div className="flex-1 min-w-[200px]">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by crop, disease, location..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                {searchTerm && (
                  <button
                    onClick={() => setSearchTerm('')}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2"
                  >
                    <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
                  </button>
                )}
              </div>
            </div>

            {/* Filter Button */}
            <button
              onClick={() => setFilterOpen(!filterOpen)}
              className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <Filter className="h-4 w-4 mr-2" />
              Filters
              {(filters.cropType !== 'all' || filters.diseaseType !== 'all' || filters.dateRange !== 'all' || filters.riskLevel !== 'all') && (
                <span className="ml-2 w-2 h-2 bg-green-500 rounded-full"></span>
              )}
            </button>

            {/* Export Button */}
            <button
              onClick={handleExport}
              className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              disabled={filteredHistory.length === 0}
            >
              <Download className="h-4 w-4 mr-2" />
              Export {selectedItems.length > 0 ? 'Selected' : 'All'}
            </button>

            {/* Bulk Delete */}
            {selectedItems.length > 0 && (
              <button
                onClick={() => handleDelete(selectedItems)}
                className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete ({selectedItems.length})
              </button>
            )}
          </div>

          {/* Expanded Filters */}
          {filterOpen && (
            <div className="grid md:grid-cols-4 gap-4 mt-4 pt-4 border-t">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Crop Type
                </label>
                <select
                  value={filters.cropType}
                  onChange={(e) => setFilters({...filters, cropType: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="all">All Crops</option>
                  <option value="Rice">Rice</option>
                  <option value="Wheat">Wheat</option>
                  <option value="Cotton">Cotton</option>
                  <option value="Sugarcane">Sugarcane</option>
                  <option value="Banana">Banana</option>
                  <option value="Coconut">Coconut</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Disease Type
                </label>
                <select
                  value={filters.diseaseType}
                  onChange={(e) => setFilters({...filters, diseaseType: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="all">All Diseases</option>
                  <option value="Rice Blast">Rice Blast</option>
                  <option value="Brown Spot">Brown Spot</option>
                  <option value="Leaf Curl">Leaf Curl</option>
                  <option value="Red Rot">Red Rot</option>
                  <option value="Healthy">Healthy</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Weather Risk
                </label>
                <select
                  value={filters.riskLevel}
                  onChange={(e) => setFilters({...filters, riskLevel: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="all">All Risks</option>
                  <option value="HIGH">High Risk</option>
                  <option value="MEDIUM">Medium Risk</option>
                  <option value="LOW">Low Risk</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date Range
                </label>
                <select
                  value={filters.dateRange}
                  onChange={(e) => setFilters({...filters, dateRange: e.target.value})}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2"
                >
                  <option value="all">All Time</option>
                  <option value="7">Last 7 Days</option>
                  <option value="30">Last 30 Days</option>
                  <option value="90">Last 90 Days</option>
                </select>
              </div>
            </div>
          )}
        </div>

        {/* Results Summary */}
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-gray-600">
            Showing {indexOfFirstItem + 1}-{Math.min(indexOfLastItem, filteredHistory.length)} of {filteredHistory.length} results
          </p>
          <button
            onClick={handleSelectAll}
            className="text-sm text-green-600 hover:text-green-700"
          >
            {selectedItems.length === currentItems.length ? 'Deselect All' : 'Select All'}
          </button>
        </div>

        {/* History Table */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left">
                    <input
                      type="checkbox"
                      checked={selectedItems.length === currentItems.length && currentItems.length > 0}
                      onChange={handleSelectAll}
                      className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                    />
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Image
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => requestSort('date')}
                  >
                    <div className="flex items-center">
                      Date
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Crop
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Disease
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                    onClick={() => requestSort('confidence')}
                  >
                    <div className="flex items-center">
                      Confidence
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Weather Risk
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {currentItems.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <input
                        type="checkbox"
                        checked={selectedItems.includes(item.id)}
                        onChange={() => handleSelectItem(item.id)}
                        className="rounded border-gray-300 text-green-600 focus:ring-green-500"
                      />
                    </td>
                    <td className="px-6 py-4">
                      <div className="w-12 h-12 bg-gray-200 rounded-lg overflow-hidden">
                        {item.image && (
                          <img src={item.image} alt={item.crop} className="w-full h-full object-cover" />
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">{formatDate(item.date)}</div>
                      <div className="text-xs text-gray-500 flex items-center mt-1">
                        <Clock className="h-3 w-3 mr-1" />
                        {new Date(item.date).toLocaleTimeString()}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <Leaf className="h-4 w-4 text-green-600 mr-2" />
                        <span className="text-sm font-medium text-gray-900">{item.crop}</span>
                      </div>
                      <div className="text-xs text-gray-500 flex items-center mt-1">
                        <MapPin className="h-3 w-3 mr-1" />
                        {item.location.split(',')[0]}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{item.disease}</div>
                      <div className="flex items-center mt-1">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getSeverityColor(item.severity)}`}>
                          {item.severity === 'healthy' ? 'Healthy' : `${item.severity.toUpperCase()} Severity`}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className={`h-2 rounded-full ${
                              item.confidence >= 90 ? 'bg-green-500' :
                              item.confidence >= 70 ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                            style={{ width: `${item.confidence}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium">{item.confidence}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="space-y-1">
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getRiskColor(item.weatherRisk)}`}>
                          {item.weatherRisk}
                        </span>
                        <div className="flex items-center text-xs text-gray-500">
                          <Thermometer className="h-3 w-3 mr-1" />
                          {item.temperature}°C
                          <Droplets className="h-3 w-3 ml-2 mr-1" />
                          {item.humidity}%
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        <Link
                          to={`/history/${item.id}`}
                          className="p-1 text-gray-400 hover:text-gray-600"
                          title="View Details"
                        >
                          <Eye className="h-5 w-5" />
                        </Link>
                        <button
                          onClick={() => handleDelete([item.id])}
                          className="p-1 text-gray-400 hover:text-red-600"
                          title="Delete"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Empty State */}
          {filteredHistory.length === 0 && (
            <div className="text-center py-12">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
                <Calendar className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No history found</h3>
              <p className="text-gray-500 mb-6">
                {searchTerm || Object.values(filters).some(v => v !== 'all')
                  ? 'Try adjusting your filters or search terms'
                  : 'Start detecting diseases to build your history'}
              </p>
              <Link
                to="/detect"
                className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
              >
                <Leaf className="h-4 w-4 mr-2" />
                New Detection
              </Link>
            </div>
          )}
        </div>

        {/* Pagination */}
        {filteredHistory.length > 0 && (
          <div className="flex items-center justify-between mt-6">
            <div className="text-sm text-gray-700">
              Page {currentPage} of {totalPages}
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              {[...Array(totalPages)].map((_, i) => (
                <button
                  key={i + 1}
                  onClick={() => setCurrentPage(i + 1)}
                  className={`px-3 py-1 rounded-lg ${
                    currentPage === i + 1
                      ? 'bg-green-600 text-white'
                      : 'border border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  {i + 1}
                </button>
              ))}
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryPage;
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Camera,
  Cloud,
  Leaf,
  MapPin,
  TrendingUp,
  Users,
  Calendar,
  Bell,
  Settings,
  LogOut,
  Activity,
  Award,
  AlertTriangle,
  ChevronRight,
  Download,
  Share2,
  MoreVertical,
  Sun,
  Droplets,
  Thermometer,
  Wind,
  Map
} from 'lucide-react';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = ({ user }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [notifications, setNotifications] = useState([]);
  const [recentPredictions, setRecentPredictions] = useState([]);
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    // Simulate loading data
    setTimeout(() => {
      setRecentPredictions(mockPredictions);
      setWeatherData(mockWeather);
      setNotifications(mockNotifications);
      setLoading(false);
    }, 1500);
  }, []);

  const mockPredictions = [
    {
      id: 1,
      date: '2024-01-15',
      crop: 'Rice',
      disease: 'Rice Blast',
      confidence: 95,
      status: 'high',
      image: '/images/rice-blast.jpg'
    },
    {
      id: 2,
      date: '2024-01-14',
      crop: 'Wheat',
      disease: 'Healthy',
      confidence: 98,
      status: 'healthy',
      image: '/images/wheat-healthy.jpg'
    },
    {
      id: 3,
      date: '2024-01-13',
      crop: 'Cotton',
      disease: 'Leaf Curl',
      confidence: 87,
      status: 'medium',
      image: '/images/cotton-leaf.jpg'
    },
    {
      id: 4,
      date: '2024-01-12',
      crop: 'Sugarcane',
      disease: 'Red Rot',
      confidence: 92,
      status: 'high',
      image: '/images/sugarcane-rot.jpg'
    }
  ];

  const mockWeather = {
    temperature: 32,
    humidity: 75,
    rainfall: 15,
    windSpeed: 12,
    condition: 'Partly Cloudy',
    risk: 'MEDIUM',
    forecast: [
      { day: 'Mon', temp: 32, humidity: 75 },
      { day: 'Tue', temp: 33, humidity: 78 },
      { day: 'Wed', temp: 31, humidity: 72 },
      { day: 'Thu', temp: 30, humidity: 70 },
      { day: 'Fri', temp: 32, humidity: 74 },
      { day: 'Sat', temp: 34, humidity: 76 },
      { day: 'Sun', temp: 33, humidity: 75 }
    ]
  };

  const mockNotifications = [
    {
      id: 1,
      type: 'weather',
      title: 'High Humidity Alert',
      message: 'High humidity (85%) detected in your area. Increased risk of fungal diseases.',
      time: '2 hours ago',
      read: false
    },
    {
      id: 2,
      type: 'scheme',
      title: 'New Scheme Available',
      message: 'PM Kisan Samman Nidhi 12th installment has been released.',
      time: '1 day ago',
      read: false
    },
    {
      id: 3,
      type: 'disease',
      title: 'Disease Alert',
      message: 'Rice Blast reported in neighboring farms. Consider preventive measures.',
      time: '2 days ago',
      read: true
    }
  ];

  const getStatusColor = (status) => {
    switch(status) {
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

  // Chart Data
  const diseaseChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Detections',
        data: [12, 19, 15, 25, 22, 30],
        borderColor: 'rgb(5, 150, 105)',
        backgroundColor: 'rgba(5, 150, 105, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };

  const cropHealthData = {
    labels: ['Healthy', 'Mild', 'Moderate', 'Severe'],
    datasets: [
      {
        data: [45, 25, 20, 10],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(234, 179, 8, 0.8)',
          'rgba(249, 115, 22, 0.8)',
          'rgba(239, 68, 68, 0.8)'
        ],
        borderWidth: 0
      }
    ]
  };

  const weatherChartData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        type: 'line',
        label: 'Temperature (°C)',
        data: [32, 33, 31, 30, 32, 34, 33],
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        yAxisID: 'y',
      },
      {
        type: 'bar',
        label: 'Humidity (%)',
        data: [75, 78, 72, 70, 74, 76, 75],
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        yAxisID: 'y1',
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    }
  };

  const weatherChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      }
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Temperature (°C)'
        }
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        grid: {
          drawOnChartArea: false,
        },
        title: {
          display: true,
          text: 'Humidity (%)'
        }
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <nav className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Leaf className="h-8 w-8 text-green-600 mr-2" />
              <span className="font-bold text-xl text-gray-900">SmartAgriAI</span>
            </div>

            <div className="flex items-center space-x-4">
              {/* Notifications */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="relative p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
                >
                  <Bell className="h-5 w-5" />
                  {notifications.filter(n => !n.read).length > 0 && (
                    <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                  )}
                </button>

                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border z-50">
                    <div className="p-3 border-b">
                      <h3 className="font-semibold">Notifications</h3>
                    </div>
                    <div className="max-h-96 overflow-y-auto">
                      {notifications.map(notif => (
                        <div key={notif.id} className={`p-3 border-b hover:bg-gray-50 ${!notif.read ? 'bg-blue-50' : ''}`}>
                          <div className="flex items-start">
                            <div className={`p-1 rounded-full mr-3 ${
                              notif.type === 'weather' ? 'bg-blue-100' :
                              notif.type === 'scheme' ? 'bg-green-100' : 'bg-orange-100'
                            }`}>
                              {notif.type === 'weather' && <Cloud className="h-4 w-4 text-blue-600" />}
                              {notif.type === 'scheme' && <Award className="h-4 w-4 text-green-600" />}
                              {notif.type === 'disease' && <AlertTriangle className="h-4 w-4 text-orange-600" />}
                            </div>
                            <div className="flex-1">
                              <p className="text-sm font-medium">{notif.title}</p>
                              <p className="text-xs text-gray-500">{notif.message}</p>
                              <p className="text-xs text-gray-400 mt-1">{notif.time}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="p-2 border-t text-center">
                      <button className="text-sm text-green-600 hover:text-green-700">
                        Mark all as read
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* User Menu */}
              <div className="flex items-center space-x-3">
                <div className="text-right hidden sm:block">
                  <div className="text-sm font-medium text-gray-900">
                    {user?.name || 'Rajesh Kumar'}
                  </div>
                  <div className="text-xs text-gray-500">
                    {user?.location || 'Thrissur, Kerala'}
                  </div>
                </div>
                <img
                  src="https://randomuser.me/api/portraits/men/1.jpg"
                  alt="Profile"
                  className="w-8 h-8 rounded-full"
                />
                <button className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg">
                  <LogOut className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Banner */}
        <div className="bg-gradient-to-r from-green-600 to-green-500 rounded-2xl p-6 mb-8 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold mb-2">
                Welcome back, {user?.name || 'Rajesh'}! 👋
              </h1>
              <p className="text-green-100">
                Here's what's happening with your farm today
              </p>
            </div>
            <div className="hidden md:block">
              <Calendar className="h-12 w-12 text-green-200" />
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Camera className="h-6 w-6 text-blue-600" />
              </div>
              <span className="text-2xl font-bold text-gray-900">24</span>
            </div>
            <h3 className="text-gray-600">Total Detections</h3>
            <p className="text-sm text-green-600 mt-2">+12% from last month</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <Activity className="h-6 w-6 text-green-600" />
              </div>
              <span className="text-2xl font-bold text-gray-900">18</span>
            </div>
            <h3 className="text-gray-600">Healthy Crops</h3>
            <p className="text-sm text-green-600 mt-2">75% of total</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-orange-100 rounded-lg">
                <Award className="h-6 w-6 text-orange-600" />
              </div>
              <span className="text-2xl font-bold text-gray-900">6</span>
            </div>
            <h3 className="text-gray-600">Schemes Applied</h3>
            <p className="text-sm text-green-600 mt-2">3 pending approval</p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="p-2 bg-purple-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
              <span className="text-2xl font-bold text-gray-900">₹45k</span>
            </div>
            <h3 className="text-gray-600">Subsidy Received</h3>
            <p className="text-sm text-green-600 mt-2">This year</p>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Disease Trends */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-gray-900">Disease Detection Trends</h3>
              <select className="text-sm border rounded-lg px-2 py-1">
                <option>Last 6 months</option>
                <option>Last year</option>
              </select>
            </div>
            <div className="h-64">
              <Line data={diseaseChartData} options={chartOptions} />
            </div>
          </div>

          {/* Crop Health Distribution */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-gray-900">Crop Health Distribution</h3>
              <select className="text-sm border rounded-lg px-2 py-1">
                <option>All crops</option>
                <option>Rice</option>
                <option>Wheat</option>
              </select>
            </div>
            <div className="h-64 flex items-center justify-center">
              <div className="w-48 h-48">
                <Doughnut data={cropHealthData} options={{ cutout: '60%' }} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2 mt-4">
              {cropHealthData.labels.map((label, i) => (
                <div key={i} className="flex items-center text-sm">
                  <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: cropHealthData.datasets[0].backgroundColor[i] }}></div>
                  <span>{label}: {cropHealthData.datasets[0].data[i]}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Weather & Risk Section */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          {/* Current Weather */}
          <div className="lg:col-span-1 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white">
            <h3 className="font-semibold mb-4 flex items-center">
              <Cloud className="h-5 w-5 mr-2" />
              Current Weather
            </h3>
            
            <div className="text-center mb-6">
              <Sun className="h-16 w-16 mx-auto mb-2 text-yellow-300" />
              <div className="text-4xl font-bold mb-1">{weatherData?.temperature}°C</div>
              <div className="text-blue-100">{weatherData?.condition}</div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="text-center">
                <Droplets className="h-5 w-5 mx-auto mb-1" />
                <div className="text-sm">Humidity</div>
                <div className="font-semibold">{weatherData?.humidity}%</div>
              </div>
              <div className="text-center">
                <Wind className="h-5 w-5 mx-auto mb-1" />
                <div className="text-sm">Wind Speed</div>
                <div className="font-semibold">{weatherData?.windSpeed} km/h</div>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-blue-400">
              <div className="flex items-center justify-between">
                <span>Disease Risk</span>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskColor(weatherData?.risk)}`}>
                  {weatherData?.risk}
                </span>
              </div>
            </div>
          </div>

          {/* Weather Chart */}
          <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-6">7-Day Weather Forecast</h3>
            <div className="h-48">
              <Bar data={weatherChartData} options={weatherChartOptions} />
            </div>
          </div>
        </div>

        {/* Recent Predictions */}
        <div className="bg-white rounded-xl shadow-sm mb-8">
          <div className="p-6 border-b">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Recent Detections</h3>
              <Link to="/history" className="text-sm text-green-600 hover:text-green-700 flex items-center">
                View All
                <ChevronRight className="h-4 w-4 ml-1" />
              </Link>
            </div>
          </div>

          <div className="divide-y">
            {recentPredictions.map(pred => (
              <div key={pred.id} className="p-4 hover:bg-gray-50">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gray-200 rounded-lg mr-4 overflow-hidden">
                    {pred.image && (
                      <img src={pred.image} alt={pred.crop} className="w-full h-full object-cover" />
                    )}
                  </div>
                  
                  <div className="flex-1 grid grid-cols-4 gap-4">
                    <div>
                      <div className="text-sm text-gray-500">Date</div>
                      <div className="font-medium">{new Date(pred.date).toLocaleDateString()}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Crop</div>
                      <div className="font-medium">{pred.crop}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Disease</div>
                      <div className="font-medium">{pred.disease}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Status</div>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(pred.status)}`}>
                        {pred.confidence}% confidence
                      </span>
                    </div>
                  </div>

                  <button className="ml-4 p-2 text-gray-400 hover:text-gray-600">
                    <MoreVertical className="h-5 w-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-3 gap-6">
          <Link
            to="/detect"
            className="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white hover:shadow-lg transition-shadow"
          >
            <Camera className="h-8 w-8 mb-4" />
            <h4 className="font-semibold text-lg mb-1">New Detection</h4>
            <p className="text-sm text-green-100">Upload a crop image for instant analysis</p>
          </Link>

          <Link
            to="/weather"
            className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-6 text-white hover:shadow-lg transition-shadow"
          >
            <Cloud className="h-8 w-8 mb-4" />
            <h4 className="font-semibold text-lg mb-1">Weather Risk</h4>
            <p className="text-sm text-blue-100">Check disease risk based on weather</p>
          </Link>

          <Link
            to="/map"
            className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-6 text-white hover:shadow-lg transition-shadow"
          >
            <Map className="h-8 w-8 mb-4" />
            <h4 className="font-semibold text-lg mb-1">Nearby Services</h4>
            <p className="text-sm text-purple-100">Find Krishi Bhavans near you</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
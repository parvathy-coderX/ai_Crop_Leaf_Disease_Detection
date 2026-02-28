import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Camera,
  Cloud,
  Leaf,
  MapPin,
  ArrowRight,
  TrendingUp,
  Users,
  Award,
  Shield,
  Sun,
  Droplets,
  Thermometer,
  ChevronRight,
  Star,
  Clock,
  CheckCircle
} from 'lucide-react';

const HomePage = () => {
  const [stats, setStats] = useState({
    farmersHelped: 0,
    diseasesDetected: 0,
    accuracy: 0,
    schemesAvailable: 0
  });
  const [animateStats, setAnimateStats] = useState(false);

  useEffect(() => {
    // Animate stats on load
    setAnimateStats(true);
    
    // Simulate counting animation
    const timer = setTimeout(() => {
      setStats({
        farmersHelped: 50000,
        diseasesDetected: 75000,
        accuracy: 95,
        schemesAvailable: 150
      });
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  const features = [
    {
      icon: Camera,
      title: 'AI Disease Detection',
      description: 'Upload photos of your crops and get instant disease identification with treatment recommendations.',
      color: 'green',
      link: '/detect',
      stats: '95% accuracy'
    },
    {
      icon: Cloud,
      title: 'Weather Risk Assessment',
      description: 'Real-time weather monitoring and disease risk prediction based on local conditions.',
      color: 'blue',
      link: '/weather',
      stats: '7-day forecast'
    },
    {
      icon: Leaf,
      title: 'Government Schemes',
      description: 'Find relevant agricultural schemes, subsidies, and financial assistance programs.',
      color: 'orange',
      link: '/schemes',
      stats: '150+ schemes'
    },
    {
      icon: MapPin,
      title: 'Nearby Services',
      description: 'Locate Krishi Bhavans, agricultural offices, and service centers near you.',
      color: 'purple',
      link: '/map',
      stats: 'Real-time location'
    }
  ];

  const testimonials = [
    {
      name: 'Rajesh Kumar',
      location: 'Thrissur, Kerala',
      image: 'https://randomuser.me/api/portraits/men/1.jpg',
      text: 'SmartAgriAI helped me identify a fungal infection in my rice crop within seconds. The treatment recommendations saved my entire harvest!',
      rating: 5
    },
    {
      name: 'Lakshmi Devi',
      location: 'Coimbatore, Tamil Nadu',
      image: 'https://randomuser.me/api/portraits/women/2.jpg',
      text: 'The weather risk prediction warned me about high humidity conditions. I applied preventive measures and avoided a major disease outbreak.',
      rating: 5
    },
    {
      name: 'Suresh Patil',
      location: 'Kolhapur, Maharashtra',
      image: 'https://randomuser.me/api/portraits/men/3.jpg',
      text: 'I discovered government schemes I never knew about through this platform. Applied for subsidy and saved ₹50,000 on equipment!',
      rating: 5
    }
  ];

  const howItWorks = [
    {
      step: 1,
      title: 'Upload Image',
      description: 'Take a photo of your crop and upload it to our platform',
      icon: Camera
    },
    {
      step: 2,
      title: 'AI Analysis',
      description: 'Our AI analyzes the image and detects any diseases',
      icon: TrendingUp
    },
    {
      step: 3,
      title: 'Get Recommendations',
      description: 'Receive treatment plans and preventive measures',
      icon: CheckCircle
    },
    {
      step: 4,
      title: 'Access Benefits',
      description: 'Discover relevant government schemes and nearby services',
      icon: Award
    }
  ];

  const stats_data = [
    { label: 'Farmers Helped', value: stats.farmersHelped, icon: Users, suffix: '+' },
    { label: 'Diseases Detected', value: stats.diseasesDetected, icon: Camera, suffix: '+' },
    { label: 'Accuracy Rate', value: stats.accuracy, icon: Shield, suffix: '%' },
    { label: 'Schemes Available', value: stats.schemesAvailable, icon: Award, suffix: '+' }
  ];

  const StatCounter = ({ value }) => {
    const [count, setCount] = useState(0);

    useEffect(() => {
      if (animateStats) {
        let start = 0;
        const end = value;
        const duration = 2000;
        const increment = end / (duration / 16);
        
        const timer = setInterval(() => {
          start += increment;
          if (start > end) {
            setCount(end);
            clearInterval(timer);
          } else {
            setCount(Math.floor(start));
          }
        }, 16);

        return () => clearInterval(timer);
      }
    }, [value, animateStats]);

    return <span>{count.toLocaleString()}</span>;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-r from-green-700 to-green-600 text-white py-20">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="absolute -right-40 -top-40 w-80 h-80 bg-green-500 rounded-full opacity-20"></div>
        <div className="absolute -left-40 -bottom-40 w-80 h-80 bg-green-400 rounded-full opacity-20"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <h1 className="text-5xl md:text-6xl font-bold leading-tight">
                Smart Agriculture
                <span className="block text-green-200">AI Assistant</span>
              </h1>
              <p className="text-xl text-green-100 max-w-lg">
                Empower your farming with artificial intelligence. Detect diseases early, 
                predict weather risks, and access government benefits - all in one place.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <Link
                  to="/detect"
                  className="inline-flex items-center px-6 py-3 bg-white text-green-700 rounded-lg font-semibold hover:bg-green-50 transition-colors duration-200 shadow-lg"
                >
                  <Camera className="h-5 w-5 mr-2" />
                  Start Detection
                </Link>
                <Link
                  to="/about"
                  className="inline-flex items-center px-6 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-green-700 transition-colors duration-200"
                >
                  Learn More
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Link>
              </div>

              {/* Stats Row */}
              <div className="flex items-center space-x-6 pt-8">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <img
                      key={i}
                      src={`https://randomuser.me/api/portraits/men/${i}.jpg`}
                      alt="User"
                      className="w-8 h-8 rounded-full border-2 border-white"
                    />
                  ))}
                </div>
                <div className="text-sm">
                  <span className="font-bold">50,000+</span> farmers trust us
                </div>
              </div>
            </div>

            {/* Hero Image/Animation */}
            <div className="hidden md:block relative">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-3">
                    <div className="bg-white/20 rounded-lg p-3">
                      <Camera className="h-6 w-6" />
                    </div>
                    <div className="bg-white/20 rounded-lg p-3">
                      <Cloud className="h-6 w-6" />
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="bg-white/20 rounded-lg p-3">
                      <Leaf className="h-6 w-6" />
                    </div>
                    <div className="bg-white/20 rounded-lg p-3">
                      <MapPin className="h-6 w-6" />
                    </div>
                  </div>
                </div>
                <div className="mt-4 text-center">
                  <div className="inline-flex items-center bg-green-500 rounded-full px-4 py-2">
                    <span className="text-sm font-medium">AI-Powered Analysis</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white border-y">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats_data.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="inline-flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mb-4">
                    <Icon className="h-6 w-6 text-green-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900">
                    <StatCounter value={stat.value} />
                    {stat.suffix}
                  </div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need for Smart Farming
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Integrated tools powered by artificial intelligence to help you make better farming decisions
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const colorClasses = {
                green: 'from-green-500 to-green-600 text-white',
                blue: 'from-blue-500 to-blue-600 text-white',
                orange: 'from-orange-500 to-orange-600 text-white',
                purple: 'from-purple-500 to-purple-600 text-white'
              };

              return (
                <Link
                  key={index}
                  to={feature.link}
                  className="group relative bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${colorClasses[feature.color]} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>
                  
                  <div className="p-6">
                    <div className={`inline-flex items-center justify-center w-12 h-12 bg-${feature.color}-100 rounded-lg mb-4 group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className={`h-6 w-6 text-${feature.color}-600`} />
                    </div>
                    
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    
                    <p className="text-gray-600 mb-4">
                      {feature.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-green-600">
                        {feature.stats}
                      </span>
                      <ArrowRight className="h-5 w-5 text-gray-400 group-hover:text-green-600 group-hover:translate-x-1 transition-all duration-300" />
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600">
              Get started in four simple steps
            </p>
          </div>

          <div className="relative">
            {/* Connection Line */}
            <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-green-200 -translate-y-1/2"></div>
            
            <div className="grid md:grid-cols-4 gap-8 relative">
              {howItWorks.map((item) => {
                const Icon = item.icon;
                return (
                  <div key={item.step} className="relative">
                    <div className="bg-white rounded-xl p-6 shadow-lg text-center relative z-10">
                      <div className="inline-flex items-center justify-center w-12 h-12 bg-green-600 rounded-full text-white font-bold text-lg mb-4">
                        {item.step}
                      </div>
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                        <Icon className="h-8 w-8 text-green-600" />
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">
                        {item.title}
                      </h3>
                      <p className="text-gray-600 text-sm">
                        {item.description}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>

      {/* Live Weather Preview */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-blue-600 to-blue-500 rounded-2xl shadow-xl overflow-hidden">
            <div className="grid md:grid-cols-2">
              <div className="p-12 text-white">
                <h3 className="text-3xl font-bold mb-4">
                  Real-Time Weather Intelligence
                </h3>
                <p className="text-blue-100 mb-8">
                  Get hyperlocal weather forecasts and disease risk predictions for your exact location.
                </p>
                
                <div className="space-y-4">
                  <div className="flex items-center">
                    <Thermometer className="h-5 w-5 mr-3" />
                    <span>Temperature tracking with stress alerts</span>
                  </div>
                  <div className="flex items-center">
                    <Droplets className="h-5 w-5 mr-3" />
                    <span>Humidity-based disease risk assessment</span>
                  </div>
                  <div className="flex items-center">
                    <Sun className="h-5 w-5 mr-3" />
                    <span>7-day forecast with actionable insights</span>
                  </div>
                </div>

                <Link
                  to="/weather"
                  className="inline-flex items-center mt-8 px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors duration-200"
                >
                  Check Weather Risk
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Link>
              </div>
              
              <div className="hidden md:block bg-blue-400 p-12">
                <div className="bg-white/10 backdrop-blur rounded-xl p-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-white">32°C</div>
                      <div className="text-sm text-blue-100">Temperature</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-white">75%</div>
                      <div className="text-sm text-blue-100">Humidity</div>
                    </div>
                  </div>
                  <div className="mt-4 text-center text-white">
                    <div className="text-lg font-semibold">Disease Risk: HIGH</div>
                    <div className="text-sm text-blue-100">Fungal infection warning</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Trusted by Farmers Across India
            </h2>
            <p className="text-xl text-gray-600">
              Join thousands of farmers who have transformed their farming with AI
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-lg">
                <div className="flex items-center mb-4">
                  <img
                    src={testimonial.image}
                    alt={testimonial.name}
                    className="w-12 h-12 rounded-full mr-4"
                  />
                  <div>
                    <h4 className="font-semibold text-gray-900">{testimonial.name}</h4>
                    <p className="text-sm text-gray-500">{testimonial.location}</p>
                  </div>
                </div>
                
                <div className="flex mb-3">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <p className="text-gray-700 italic">"{testimonial.text}"</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Farming?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join the AI-powered agricultural revolution today
          </p>
          
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/detect"
              className="inline-flex items-center px-8 py-4 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors duration-200 shadow-lg"
            >
              <Camera className="h-5 w-5 mr-2" />
              Detect Disease Now
            </Link>
            <Link
              to="/register"
              className="inline-flex items-center px-8 py-4 border-2 border-green-600 text-green-600 rounded-lg font-semibold hover:bg-green-50 transition-colors duration-200"
            >
              Create Free Account
              <ArrowRight className="h-5 w-5 ml-2" />
            </Link>
          </div>

          <p className="mt-6 text-sm text-gray-500 flex items-center justify-center">
            <Clock className="h-4 w-4 mr-1" />
            Free for farmers • No credit card required
          </p>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
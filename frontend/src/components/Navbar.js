import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Camera, 
  Cloud, 
  Map, 
  History, 
  Menu, 
  X,
  Leaf,
  LogIn,
  User
} from 'lucide-react';

const Navbar = ({ isLoggedIn, userName }) => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Disease Detection', href: '/detect', icon: Camera },
    { name: 'Weather Risk', href: '/weather', icon: Cloud },
    { name: 'Government Schemes', href: '/schemes', icon: Leaf },
    { name: 'Map', href: '/map', icon: Map },
    { name: 'History', href: '/history', icon: History },
  ];

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-gradient-to-r from-green-700 to-green-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Leaf className="h-8 w-8 text-green-200" />
              <span className="font-bold text-xl hidden sm:block">SmartAgriAI</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isActive(item.href)
                      ? 'bg-green-800 text-white'
                      : 'text-green-100 hover:bg-green-600 hover:text-white'
                  }`}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {item.name}
                </Link>
              );
            })}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isLoggedIn ? (
              <div className="flex items-center space-x-2">
                <div className="flex items-center bg-green-800 px-3 py-1 rounded-full">
                  <User className="h-4 w-4 mr-2" />
                  <span className="text-sm font-medium">{userName || 'Farmer'}</span>
                </div>
              </div>
            ) : (
              <Link
                to="/login"
                className="flex items-center px-4 py-2 rounded-md bg-white text-green-700 hover:bg-green-50 transition-colors duration-200"
              >
                <LogIn className="h-4 w-4 mr-2" />
                Login
              </Link>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-green-100 hover:text-white hover:bg-green-600 focus:outline-none"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center px-3 py-2 rounded-md text-base font-medium ${
                    isActive(item.href)
                      ? 'bg-green-800 text-white'
                      : 'text-green-100 hover:bg-green-600 hover:text-white'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <Icon className="h-5 w-5 mr-3" />
                  {item.name}
                </Link>
              );
            })}
            {!isLoggedIn && (
              <Link
                to="/login"
                className="flex items-center px-3 py-2 rounded-md text-base font-medium bg-white text-green-700"
                onClick={() => setIsOpen(false)}
              >
                <LogIn className="h-5 w-5 mr-3" />
                Login
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
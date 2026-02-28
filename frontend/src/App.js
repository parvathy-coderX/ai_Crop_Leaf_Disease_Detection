import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';

// Pages
import HomePage from './pages/HomePage';
import Dashboard from './pages/Dashboard';
import HistoryPage from './pages/HistoryPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import SchemesPage from './pages/SchemesPage';
import WeatherPage from './pages/WeatherPage';

// Components
import Navbar from './components/Navbar';
import ImageUpload from './components/ImageUpload';
import WeatherRiskCard from './components/WeatherRiskCard';
import SchemeCard from './components/SchemeCard';
import MapView from './components/MapView';
import PrivateRoute from './components/PrivateRoute';

// Styles
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              {/* Public routes - accessible without login */}
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/detect" element={<ImageUpload />} />
              <Route path="/weather" element={<WeatherPage />} /> {/* ✅ Now public */}
              <Route path="/weather-card" element={<WeatherRiskCard />} /> {/* ✅ Now public */}
              <Route path="/schemes" element={<SchemesPage />} /> {/* ✅ Now public */}
              <Route path="/scheme-card" element={<SchemeCard />} /> {/* ✅ Now public */}
              <Route path="/map" element={<MapView />} /> {/* ✅ Now public */}
              
              {/* Protected routes - require login */}
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/history" element={
                <PrivateRoute>
                  <HistoryPage />
                </PrivateRoute>
              } />
              
              {/* Redirect to home if route not found */}
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 4000,
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
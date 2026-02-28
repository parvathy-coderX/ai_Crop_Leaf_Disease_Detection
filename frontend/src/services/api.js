/**
 * API service for SmartAgriAI frontend
 * Handles all backend API calls
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Helper function to handle responses
const handleResponse = async (response) => {
  const data = await response.json();
  
  if (!response.ok) {
    const error = data.error || data.message || 'Something went wrong';
    throw new Error(error);
  }
  
  return data;
};

// ===== DISEASE DETECTION API =====

/**
 * Upload an image for disease prediction
 */
export const uploadImage = async (formData) => {
  try {
    console.log('Uploading to:', `${API_BASE_URL}/disease/predict`);
    
    const response = await fetch(`${API_BASE_URL}/disease/predict`, {
      method: 'POST',
      body: formData,
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

// ===== USER AUTHENTICATION API =====

/**
 * Register a new user
 */
export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

/**
 * Login user
 */
export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    
    const data = await handleResponse(response);
    
    // Store user data in localStorage
    if (data.success) {
      localStorage.setItem('userId', data.user_id);
      localStorage.setItem('userName', data.name);
      localStorage.setItem('userPhone', data.phone);
    }
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

/**
 * Get current user ID from localStorage
 */
export const getCurrentUserId = () => {
  return localStorage.getItem('userId');
};

/**
 * Get current user name from localStorage
 */
export const getCurrentUserName = () => {
  return localStorage.getItem('userName');
};

/**
 * Check if user is logged in
 */
export const isLoggedIn = () => {
  return !!localStorage.getItem('userId');
};

/**
 * Logout user
 */
export const logoutUser = () => {
  localStorage.removeItem('userId');
  localStorage.removeItem('userName');
  localStorage.removeItem('userPhone');
  localStorage.removeItem('authToken');
};

/**
 * Get user profile
 */
export const getUserProfile = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/${userId}/profile`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Profile fetch error:', error);
    throw error;
  }
};

/**
 * Update user profile
 */
export const updateUserProfile = async (userId, updates) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/${userId}/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Profile update error:', error);
    throw error;
  }
};

/**
 * Get user history
 */
export const getUserHistory = async (userId, limit = 20) => {
  try {
    const response = await fetch(`${API_BASE_URL}/user/${userId}/history?limit=${limit}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('History fetch error:', error);
    throw error;
  }
};

// ===== WEATHER API =====

/**
 * Get weather risk assessment
 */
export const getWeatherRisk = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}/weather/risk`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Weather risk error:', error);
    throw error;
  }
};

/**
 * Get current weather
 */
export const getCurrentWeather = async (lat, lon) => {
  try {
    const response = await fetch(`${API_BASE_URL}/weather/current?lat=${lat}&lon=${lon}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Weather fetch error:', error);
    throw error;
  }
};

// ===== SCHEMES API =====

/**
 * Get scheme recommendations
 */
export const getSchemeRecommendations = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}/schemes/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Scheme recommendations error:', error);
    throw error;
  }
};

/**
 * Search schemes
 */
export const searchSchemes = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/schemes/search?q=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Scheme search error:', error);
    throw error;
  }
};

// ===== HEALTH CHECKS =====

/**
 * Check disease service health
 */
export const checkDiseaseHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/disease/health`, {
      method: 'GET',
    });
    
    return await handleResponse(response);
  } catch (error) {
    console.error('Health check error:', error);
    throw error;
  }
};
import React, { createContext, useState, useContext, useEffect } from 'react';
import { loginUser, registerUser, getCurrentUserId, getCurrentUserName, logoutUser } from '../services/api';
import toast from 'react-hot-toast';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const userId = getCurrentUserId();
    const userName = getCurrentUserName();
    
    if (userId) {
      setUser({ id: userId, name: userName });
    }
    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const response = await loginUser(credentials);
      if (response.success) {
        setUser({
          id: response.user_id,
          name: response.name,
          phone: response.phone
        });
        toast.success('Login successful!');
        return true;
      }
    } catch (error) {
      toast.error(error.message || 'Login failed');
      return false;
    }
  };

  const register = async (userData) => {
    try {
      const response = await registerUser(userData);
      if (response.success) {
        toast.success('Registration successful! Please login.');
        return true;
      }
    } catch (error) {
      toast.error(error.message || 'Registration failed');
      return false;
    }
  };

  const logout = () => {
    logoutUser();
    setUser(null);
    toast.success('Logged out successfully');
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
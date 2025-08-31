// src/services/api.js
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Configure axios with JWT
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, {
      username,
      password
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const getRecommendations = async (query, context = {}) => {
  try {
    const userId = localStorage.getItem('userId');
    const response = await axios.post(`${API_URL}/recommendations`, {
      user_id: userId,
      query,
      context
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};


import axios from 'axios';

// Get the current hostname (EC2 public IP or domain)
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'http://3.65.249.159:8001'
  : 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/polybot/login';
    }
    return Promise.reject(error);
  }
);

export const getMarkets = async () => {
  const response = await api.get('/api/markets');
  return response.data;
};

export const getMarketDetails = async (marketId: string) => {
  const response = await api.get(`/api/markets/${marketId}`);
  return response.data;
};

export const getMarketEvents = async (marketId: string) => {
  const response = await api.get(`/api/markets/${marketId}/events`);
  return response.data;
};

export const getStats = async () => {
  const response = await api.get('/api/stats');
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const saveSettings = async (settings: any) => {
  const response = await api.post('/api/settings', settings);
  return response.data;
};

export default api; 
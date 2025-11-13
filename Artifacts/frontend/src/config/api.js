// API configuration - uses VITE_API_BASE_URL from environment variables
// In production, this should be set to: https://cipher-threat-api.onrender.com/api
const envApiUrl = import.meta.env.VITE_API_BASE_URL;
export const API_BASE_URL = envApiUrl 
  ? envApiUrl.replace(/\/+$/, '') 
  : 'http://localhost:8000/api';

// Always log in production to debug
console.log('[API Config] Environment variable VITE_API_BASE_URL:', envApiUrl || '(NOT SET)');
console.log('[API Config] Using API_BASE_URL:', API_BASE_URL);

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  const fullUrl = `${API_BASE_URL}/${normalizedPath}`;
  console.log(`[apiPath] Building URL for "${path}": ${fullUrl}`);
  return fullUrl;
};



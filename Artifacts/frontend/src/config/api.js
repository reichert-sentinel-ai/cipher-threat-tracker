// API configuration - uses VITE_API_BASE_URL from environment variables
// In production, this should be set to: https://cipher-threat-api.onrender.com/api
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') || 'http://localhost:8000/api';

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  const fullUrl = `${API_BASE_URL}/${normalizedPath}`;
  // Debug log to verify API URL is correct (remove in production)
  if (import.meta.env.DEV || import.meta.env.VITE_API_BASE_URL) {
    console.log(`[apiPath] Building URL for "${path}": ${fullUrl}`);
  }
  return fullUrl;
};



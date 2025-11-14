// API configuration - uses VITE_API_BASE_URL from environment variables
// In production, this should be set to: https://cipher-threat-api.onrender.com/api
// Force Vite to replace this at build time by using it directly
const envApiUrl = import.meta.env.VITE_API_BASE_URL;
const defaultUrl = 'http://localhost:8000/api';
export const API_BASE_URL = envApiUrl 
  ? String(envApiUrl).replace(/\/+$/, '') 
  : defaultUrl;

// Always log in production to debug - this will show what's actually in the build
console.log('[API Config] Environment variable VITE_API_BASE_URL:', envApiUrl || '(NOT SET)');
console.log('[API Config] Using API_BASE_URL:', API_BASE_URL);
console.log('[API Config] Build time replacement check:', import.meta.env.VITE_API_BASE_URL);

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  const fullUrl = `${API_BASE_URL}/${normalizedPath}`;
  console.log(`[apiPath] Building URL for "${path}": ${fullUrl}`);
  return fullUrl;
};



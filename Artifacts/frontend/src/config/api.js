// API configuration - uses VITE_API_BASE_URL from environment variables
// In production, this should be set to: https://cipher-threat-api.onrender.com/api
// Vite will replace import.meta.env.VITE_API_BASE_URL at build time
const envApiUrl = import.meta.env.VITE_API_BASE_URL;
const defaultUrl = 'http://localhost:8000/api';

// Use direct string replacement - Vite can statically analyze this
export const API_BASE_URL = envApiUrl 
  ? envApiUrl.replace(/\/+$/, '') 
  : defaultUrl;

// Debug logs - these will show what's actually in the built bundle
console.log('[API Config Debug]');
console.log('  - import.meta.env.VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('  - envApiUrl variable:', envApiUrl);
console.log('  - API_BASE_URL (final):', API_BASE_URL);

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  const fullUrl = `${API_BASE_URL}/${normalizedPath}`;
  console.log(`[apiPath] "${path}" -> ${fullUrl}`);
  return fullUrl;
};



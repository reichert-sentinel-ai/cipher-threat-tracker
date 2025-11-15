// API configuration - uses VITE_API_BASE_URL from environment variables
// In production, this should be set to: https://cipher-threat-api.onrender.com/api
// Vite will replace import.meta.env.VITE_API_BASE_URL at build time
const envApiUrl = import.meta.env.VITE_API_BASE_URL;
const defaultUrl = 'http://localhost:8000/api';

// Use direct string replacement - Vite can statically analyze this
// Remove trailing slashes and ensure clean URL
export const API_BASE_URL = envApiUrl 
  ? String(envApiUrl).trim().replace(/\/+$/, '') 
  : defaultUrl;

// Check if we're in production but using localhost (indicates missing env var)
const isProduction = import.meta.env.PROD;
const isUsingLocalhost = API_BASE_URL.includes('localhost') || API_BASE_URL.includes('127.0.0.1');

if (isProduction && isUsingLocalhost) {
  console.error('[API Config Error] Production build is using localhost!');
  console.error('  - VITE_API_BASE_URL is not set in Vercel environment variables');
  console.error('  - Set VITE_API_BASE_URL=https://cipher-threat-api.onrender.com/api in Vercel');
  console.error('  - Then trigger a new deployment');
}

// Debug logs - these will show what's actually in the built bundle
console.log('[API Config Debug]');
console.log('  - import.meta.env.VITE_API_BASE_URL:', import.meta.env.VITE_API_BASE_URL);
console.log('  - envApiUrl variable:', envApiUrl);
console.log('  - API_BASE_URL (final):', API_BASE_URL);
console.log('  - Production mode:', isProduction);

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  const fullUrl = `${API_BASE_URL}/${normalizedPath}`;
  console.log(`[apiPath] "${path}" -> ${fullUrl}`);
  return fullUrl;
};



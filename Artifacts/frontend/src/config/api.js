// API configuration - uses VITE_API_BASE_URL from environment variables
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') || 'http://localhost:8000/api';

export const apiPath = (path) => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path;
  return `${API_BASE_URL}/${normalizedPath}`;
};



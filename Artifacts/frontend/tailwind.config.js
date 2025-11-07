/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0f0f0f',
          surface: '#1a1a1a',
          card: '#1f1f1f',
          border: '#2a2a2a',
          text: '#e5e5e5',
          'text-muted': '#a0a0a0',
        },
      },
    },
  },
  plugins: [],
}


# Frontend Setup Instructions

## Status

✅ **Backend Server**: Running on `http://localhost:8000`
⚠️ **Frontend**: Requires Node.js/npm to be installed

## Frontend Directory Location

The frontend has been created at: `project/repo-cipher/frontend/`

## Setup Steps

### 1. Install Node.js (if not already installed)

Download and install Node.js from: https://nodejs.org/
- This will also install npm (Node Package Manager)

### 2. Navigate to Frontend Directory

```powershell
cd project/repo-cipher/frontend
```

### 3. Install Dependencies

```powershell
npm install
```

This will install all required packages:
- react
- react-dom
- react-router-dom
- recharts
- lucide-react
- axios
- tailwindcss
- vite

### 4. Start Development Server

```powershell
npm run dev
```

The frontend will start on `http://localhost:5173`

### 5. View Threat Timeline

Open your browser and navigate to:
```
http://localhost:5173/threat-timeline
```

## Expected Output

After running `npm run dev`, you should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## Troubleshooting

### npm not found
- Ensure Node.js is installed: https://nodejs.org/
- Restart your terminal after installing Node.js
- Verify installation: `node --version` and `npm --version`

### Port Already in Use
- If port 5173 is in use, Vite will automatically use the next available port
- Check the terminal output for the actual URL

### Dependencies Installation Issues
- Try clearing npm cache: `npm cache clean --force`
- Delete `node_modules` folder and `package-lock.json` if they exist
- Run `npm install` again

## Backend Status

✅ Backend is running and tested
- Threat Timeline endpoint: `http://localhost:8000/api/threat-timeline/events`
- All endpoints are functional

The frontend is configured to proxy API requests to `http://localhost:8000` automatically.


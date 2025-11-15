# Frontend Setup Instructions

## Status

✅ **Backend Server**: Default local URL `http://localhost:8000`
⚠️ **Frontend**: Requires Node.js/npm to be installed

## Frontend Directory Location

The frontend lives at: `Artifacts/frontend/`

## Setup Steps

### 1. Install Node.js (if not already installed)

Download and install Node.js from: https://nodejs.org/
- This will also install npm (Node Package Manager)

### 2. Navigate to Frontend Directory

```powershell
cd Artifacts/frontend
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

### 4. Configure API endpoint (optional)

Create a `.env` file if you need to point at a remote backend:

```
VITE_API_BASE_URL=https://api.example.com
```

Defaults to `http://localhost:8000/api` when unset.

### 5. Start Development Server

```powershell
npm run dev
```

The frontend will start on `http://localhost:5173`

### 6. View Threat Timeline

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

### Build for Production

```powershell
npm run build
npm run preview # optional – serves the dist folder locally
```

### Deploy to Vercel (Production)

1. Push this repository to GitHub (the project root can stay as-is).
2. In Vercel, click **New Project → Import** and choose `reichert-sentinel-ai/cipher-threat-tracker`.
3. When prompted for the root directory, select `Artifacts/frontend`.
4. Configure the build:
   - **Framework preset:** Vite
   - **Install command:** `npm install`
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
5. Add an environment variable in Vercel project settings:
   - `VITE_API_BASE_URL=https://cipher-threat-api.onrender.com/api`
6. Deploy. Vercel will issue a URL such as `https://cipher-threat-tracker.vercel.app`—share that link with recruiters.
7. (Optional) Create a local `.env.production` mirroring the same `VITE_API_BASE_URL` to test the production build against the hosted API.

### Dependencies Installation Issues
- Try clearing npm cache: `npm cache clean --force`
- Delete `node_modules` folder and `package-lock.json` if they exist
- Run `npm install` again

## Backend Status

✅ Backend is running and tested locally
- Threat Timeline endpoint: `http://localhost:8000/api/threat-timeline/events`
- All endpoints are functional

Set `VITE_API_BASE_URL` if you deploy the FastAPI service; otherwise the app will call the local instance.


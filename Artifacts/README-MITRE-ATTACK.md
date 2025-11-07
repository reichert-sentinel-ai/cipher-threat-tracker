# MITRE ATT&CK Coverage Map - Setup Guide

## ✅ Implementation Complete

The MITRE ATT&CK Coverage Map feature has been successfully implemented with:
- ✅ Backend API endpoints at `/api/mitre/*`
- ✅ Frontend component at `/mitre-attack` route
- ✅ Full integration with existing Cipher platform

## 🚀 Quick Start

### Option 1: Use the Startup Script (Recommended)

```powershell
cd project/repo-cipher
.\start-servers.ps1
```

### Option 2: Manual Start (PowerShell)

**Backend:**
```powershell
cd project/repo-cipher/src/api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (new terminal):**
```powershell
cd project/repo-cipher/frontend
npm run dev
```

## 📍 Access Points

- **Frontend**: http://localhost:5173
- **MITRE ATT&CK Page**: http://localhost:5173/mitre-attack
- **Backend API Docs**: http://localhost:8000/docs
- **MITRE API Endpoint**: http://localhost:8000/api/mitre/coverage-matrix

## 🔍 API Endpoints

All endpoints are prefixed with `/api/mitre`:

- `GET /api/mitre/coverage-matrix` - Get complete coverage matrix
- `GET /api/mitre/gap-analysis` - Get detection gaps and recommendations
- `GET /api/mitre/threat-actor-ttps/{actor_name}` - Get TTPs for threat actor
- `GET /api/mitre/technique-details/{technique_id}` - Get technique details
- `GET /api/mitre/detection-rules/{technique_id}` - Get detection rules
- `GET /api/mitre/tactic-summary/{tactic_name}` - Get tactic summary

## ✨ Features

1. **Coverage Matrix** - View all MITRE ATT&CK techniques with detection coverage
2. **Tactics Analysis** - Tactic-level coverage visualization
3. **Gap Analysis** - Identify critical detection gaps with recommendations
4. **Threat Actor TTPs** - Analyze techniques used by specific threat actors
5. **Overview Dashboard** - Key metrics and coverage distribution

## 🛠️ Troubleshooting

### Backend Not Starting
- Ensure Python dependencies are installed: `pip install fastapi uvicorn numpy pydantic`
- Check if port 8000 is available: `netstat -ano | findstr ":8000"`

### Frontend Not Starting
- Ensure Node.js dependencies are installed: `npm install`
- Check if port 5173 is available: `netstat -ano | findstr ":5173"`

### API Errors
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure API endpoint matches: `http://localhost:8000/api/mitre/*`

## 📝 Implementation Notes

- Follows same patterns as IOC Search implementation
- Uses consistent error handling and loading states
- Fully integrated with existing UI components
- Supports dark mode
- Responsive design for all screen sizes

## 🎯 Next Steps

1. Visit http://localhost:5173/mitre-attack
2. Explore the coverage matrix and tactics
3. Analyze gap recommendations
4. Review threat actor TTPs

# Frontend Troubleshooting Guide

## Issue: Page doesn't load - Console Error

### Step 1: Check Backend Server
Make sure the backend server is running and has the latest code:

```bash
cd project/repo-cipher
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Test Backend API Directly
```bash
curl http://localhost:8000/api/threat-timeline/events?days_back=30
```

If you see `{"detail":"Internal server error: high is out of bounds for int32"}`, the server needs to be restarted to pick up the hash generation fix.

### Step 3: Check Frontend Console
Open browser developer tools (F12) and check:
- Console tab for errors
- Network tab to see if API requests are failing

### Step 4: Common Issues

#### Issue: Backend not running
**Solution**: Start the backend server (see Step 1)

#### Issue: CORS errors
**Solution**: Backend should have CORS enabled. Check `src/api/main.py` has:
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

#### Issue: API endpoint returning 500
**Solution**: 
1. Restart backend server
2. Check backend logs for error details
3. Verify the hash generation fix is in place

#### Issue: UI components not found
**Solution**: UI components should be in `frontend/src/components/ui/`. If missing, they need to be created.

### Step 5: Verify Frontend Setup
```bash
cd project/repo-cipher/frontend
npm install
npm run dev
```

### Step 6: Check Routes
Make sure `App.jsx` has the route:
```jsx
<Route path="/threat-timeline" element={<ThreatTimeline />} />
```

## Fixed Issues

1. ✅ **Hash Generation**: Fixed int32 overflow by generating hex strings instead of large integers
2. ✅ **Error Handling**: Added better error handling in frontend to prevent crashes
3. ✅ **Null Checks**: Added check for null timelineData before rendering

## Next Steps

1. **Restart Backend**: Kill and restart the backend server to ensure it has the latest code
2. **Clear Browser Cache**: Hard refresh (Ctrl+Shift+R) or clear cache
3. **Check Console**: Look for specific error messages in browser console

If the backend test passed but the page still doesn't load, the issue is likely:
- Backend server needs restart
- Frontend can't connect to backend (check CORS/network)
- Missing dependencies in frontend


# IOC Search Route Troubleshooting

## Issue: "No routes matched location '/ioc-search'"

### Root Cause
This error typically occurs when:
1. The dev server hasn't reloaded the route changes
2. Browser cache is serving old JavaScript
3. Component import fails silently

### Solutions

#### Solution 1: Hard Restart Dev Server
```powershell
# Stop the current dev server (Ctrl+C)
# Then restart:
cd project/repo-cipher/frontend
& "C:\Program Files\nodejs\npm.cmd" run dev
```

#### Solution 2: Clear Browser Cache
1. Open browser DevTools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"
4. Or use: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)

#### Solution 3: Verify Component Import
Check browser console for import errors:
- Open DevTools (F12)
- Go to Console tab
- Look for red errors mentioning IOCSearch or import failures

#### Solution 4: Test Route Directly
Try accessing the route after restarting:
- `http://localhost:5173/ioc-search`
- Should load the IOC Search component

### Verification Checklist

✅ **Component File Exists**
```powershell
Test-Path "project/repo-cipher/frontend/src/components/IOCSearch.jsx"
# Should return: True
```

✅ **Component Has Default Export**
```powershell
Get-Content "project/repo-cipher/frontend/src/components/IOCSearch.jsx" | Select-String "export default"
# Should show: export default function IOCSearch()
```

✅ **Route Configured in App.jsx**
```powershell
Get-Content "project/repo-cipher/frontend/src/App.jsx" | Select-String "ioc-search"
# Should show: Route path="/ioc-search" element={<IOCSearch />} />
```

✅ **Import Statement Correct**
```powershell
Get-Content "project/repo-cipher/frontend/src/App.jsx" | Select-String "IOCSearch"
# Should show: import IOCSearch from './components/IOCSearch.jsx';
```

### Quick Fix Script
```powershell
# Stop dev server, clear cache, restart
Write-Host "Stopping dev server..." -ForegroundColor Yellow
# Press Ctrl+C in the dev server terminal first

Write-Host "Clearing Vite cache..." -ForegroundColor Yellow
cd project/repo-cipher/frontend
Remove-Item -Path "node_modules/.vite" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Restarting dev server..." -ForegroundColor Green
& "C:\Program Files\nodejs\npm.cmd" run dev
```

### Expected Behavior
After restart:
1. Navigate to `http://localhost:5173/ioc-search`
2. Should see IOC Search interface with:
   - Search bar
   - Feed status cards
   - Search/Bulk tabs
   - No console errors

### If Still Not Working
1. Check browser console for specific error messages
2. Verify backend is running: `http://localhost:8000/docs`
3. Check network tab for failed API calls
4. Try accessing other routes (e.g., `/threat-timeline`) to confirm routing works


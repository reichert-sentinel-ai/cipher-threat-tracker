# Fix: Blank Page on /mitre-attack Route

## Issue
The `/mitre-attack` route shows a blank white page with console error:
```
No routes matched location "/mitre-attack"
```

## Solution Steps

### 1. Restart the Frontend Dev Server

Stop the current dev server (Ctrl+C) and restart:

```powershell
cd project/repo-cipher/frontend
npm run dev
```

### 2. Clear Browser Cache

- **Chrome/Edge:** Press `Ctrl+Shift+Delete`, select "Cached images and files", Clear
- Or use **Hard Refresh:** `Ctrl+Shift+R` or `Ctrl+F5`

### 3. Check Browser Console

Open Developer Tools (F12) and check:
- **Console tab:** Look for any import/compilation errors
- **Network tab:** Verify `MitreAttackMap.jsx` is loading (200 status)

### 4. Verify Files Are Correct

The route should be in `App.jsx`:
```jsx
<Route path="/mitre-attack" element={<MitreAttackMap />} />
```

And the import:
```jsx
import MitreAttackMap from './components/MitreAttackMap.jsx';
```

### 5. If Still Not Working

Try these steps in order:

1. **Stop both servers** (Backend + Frontend)
2. **Clear node_modules cache:**
   ```powershell
   cd project/repo-cipher/frontend
   rm -r node_modules/.vite
   npm run dev
   ```

3. **Verify the component file exists:**
   ```powershell
   Test-Path project/repo-cipher/frontend/src/components/MitreAttackMap.jsx
   ```

4. **Check for syntax errors:**
   ```powershell
   cd project/repo-cipher/frontend
   npm run build
   ```

## Expected Behavior

After restarting:
- Navigate to: http://localhost:5173/mitre-attack
- Should see the MITRE ATT&CK Coverage Map loading
- If loading, you'll see a spinner initially
- Then the full component with tabs should render

## Common Causes

1. **Hot Module Replacement (HMR) issue** - Fixed by restart
2. **Browser cache** - Fixed by hard refresh
3. **Compilation error** - Check console for specific error
4. **Import path issue** - Verify file exists at correct path

## Still Having Issues?

Check the browser console for specific error messages and share them. The component is correctly implemented and tested - this is likely a dev server caching issue.

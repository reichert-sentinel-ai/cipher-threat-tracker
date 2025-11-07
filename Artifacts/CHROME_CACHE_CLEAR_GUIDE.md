# Chrome Browser Cache Clearing Guide

## Quick Method (Recommended)
**Press `Ctrl+Shift+Delete`**
1. Select "Cached images and files"
2. Time range: "All time"
3. Click "Clear data"

## DevTools Method (Best for Development)
1. Open DevTools (`F12` or `Ctrl+Shift+I`)
2. Go to **Application** tab
3. Click **Storage** in left sidebar
4. Click **Clear site data** button
5. Check all boxes (especially "Cached storage")
6. Click **Clear site data**

## Hard Refresh (Quick Fix)
**Press `Ctrl+Shift+R`** on any page
- Forces reload without cache
- Good for testing after clearing cache

## For IOC Search Route Issue
**Complete Steps:**
1. Open `http://localhost:5174`
2. Press `F12` to open DevTools
3. Go to **Application** tab
4. Click **Clear site data**
5. Navigate to: `http://localhost:5174/ioc-search`
6. If still issues, try `Ctrl+Shift+R` on the page

## Why Clear Cache?
- Removes old JavaScript files
- Forces browser to load fresh code
- Fixes "No routes matched" errors from cached React Router
- Ensures latest component code loads


# API Connection Troubleshooting Guide

**Date**: November 5, 2025  
**Issue**: Connection Refused Error

---

## ⚠️ Error: "Connection Refused" or "ERR_CONNECTION_REFUSED"

This error means the dashboard cannot connect to the API server at the specified URL.

---

## 🔍 Common Causes

1. **API Server Not Running**
   - The FastAPI server hasn't been started
   - The server crashed or stopped

2. **Wrong IP Address or Port**
   - Incorrect IP address (e.g., 71.162.0.66)
   - Wrong port number (default is 8000)

3. **Firewall Blocking Connection**
   - Windows Firewall blocking the connection
   - Network firewall blocking the port

4. **Server Not Accessible**
   - Server is on a different network
   - Server is not configured to accept external connections

---

## ✅ Solutions

### Solution 1: Use Localhost (Recommended for Testing)

If you're testing locally, use the local API server:

1. **Start the API server:**
   ```powershell
   cd C:\Users\reich\Projects\intelligence-security\repos\cipher
   python -m uvicorn src.api.main:app --reload --port 8000
   ```

2. **In the dashboard sidebar, set API URL to:**
   ```
   http://localhost:8000
   ```

3. **Test the connection:**
   - Click "🔍 Test Connection" button in the sidebar
   - Or open: http://localhost:8000/docs in your browser

---

### Solution 2: Connect to Remote API Server

If you need to connect to a remote server (e.g., 71.162.0.66):

1. **Verify the server is running:**
   - Check if the API server is running on that machine
   - Verify the port number (usually 8000)

2. **Check firewall settings:**
   - Ensure port 8000 (or your port) is open
   - Check Windows Firewall rules
   - Check network firewall rules

3. **Test connection manually:**
   ```powershell
   # Test if server is reachable
   curl http://71.162.0.66:8000/docs
   
   # Or use PowerShell
   Invoke-WebRequest -Uri "http://71.162.0.66:8000/docs"
   ```

4. **In the dashboard sidebar, set API URL to:**
   ```
   http://71.162.0.66:8000
   ```
   (Replace 8000 with the correct port if different)

---

### Solution 3: Check API Server Configuration

If the API server is running but not accessible:

1. **Check if server is listening on all interfaces:**
   ```python
   # In src/api/main.py, ensure:
   uvicorn.run(app, host="0.0.0.0", port=8000)  # Not "127.0.0.1"
   ```

2. **Check server logs:**
   - Look for startup messages
   - Check for error messages
   - Verify the port is correct

---

### Solution 4: Use Demo Mode (No API Required)

If you just want to test the dashboard UI without an API:

1. **The dashboard will show API errors, but you can still:**
   - Test navigation between pages
   - Test UI structure
   - Test dark theme
   - Test error handling

2. **This is fine for:**
   - UI testing
   - Dashboard deployment testing
   - Visual verification

---

## 🧪 Testing Steps

### Step 1: Test Local API Server

```powershell
# Start API server
cd C:\Users\reich\Projects\intelligence-security\repos\cipher
python -m uvicorn src.api.main:app --reload --port 8000

# In another terminal, test connection
curl http://localhost:8000/docs
```

### Step 2: Test Remote API Server

```powershell
# Test if server is reachable
Invoke-WebRequest -Uri "http://71.162.0.66:8000/docs"

# Or use curl
curl http://71.162.0.66:8000/docs
```

### Step 3: Test from Dashboard

1. Open dashboard: http://localhost:8501
2. In sidebar, enter API URL: `http://localhost:8000` (or remote URL)
3. Click "🔍 Test Connection" button
4. Check the result

---

## 📋 Quick Checklist

- [ ] API server is running
- [ ] Correct IP address entered
- [ ] Correct port number entered
- [ ] Using `http://` not `https://` for IP addresses
- [ ] Firewall allows connection
- [ ] Server is accessible from your network
- [ ] Test connection button shows success

---

## 💡 Tips

1. **For local testing:** Always use `http://localhost:8000`
2. **For remote servers:** Use `http://IP_ADDRESS:PORT` (e.g., `http://71.162.0.66:8000`)
3. **Check port:** Default is 8000, but may be different
4. **Use Test Connection:** The dashboard has a "Test Connection" button in the sidebar
5. **Check browser console:** F12 → Console tab for detailed errors

---

## 🚀 Next Steps

1. **If localhost works:** Great! Continue testing with local API
2. **If remote server needed:** 
   - Verify server is running
   - Check firewall settings
   - Verify network connectivity
3. **If API not available:** 
   - Test dashboard UI only (errors are expected)
   - Deploy dashboard to Streamlit Cloud
   - Configure API URL in deployment settings

---

**Last Updated**: November 5, 2025


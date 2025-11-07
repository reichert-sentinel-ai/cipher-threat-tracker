# Frontend Testing Guide - repo-cipher

## 🌐 Access the Frontend

**Frontend URL**: http://localhost:5173

## 🚀 Quick Start

### 1. Start the Frontend Server

```powershell
cd project\repo-cipher\frontend
npm run dev
```

The server will start on **http://localhost:5173**

### 2. Start the Backend Server (Required for API calls)

```powershell
cd project\repo-cipher
python run_server.py
```

Or:
```powershell
cd project\repo-cipher\src\api
uvicorn main:app --reload --port 8000
```

The backend will start on **http://localhost:8000**

---

## 🧪 Manual Testing Guide

### Test the Home Page

1. **Open Browser**: Navigate to http://localhost:5173
2. **Verify Page Loads**: You should see the Cipher platform homepage
3. **Check Navigation**: Verify all navigation links work
4. **Test Dark Theme**: Click theme toggle (if available) to switch themes
5. **Test Print**: Press `Ctrl+P` (or `Cmd+P` on Mac) to test print preview

### Test All Pages

Visit these URLs directly:

- **Home**: http://localhost:5173/
- **Threat Timeline**: http://localhost:5173/threat-timeline
- **IOC Search**: http://localhost:5173/ioc-search
- **MITRE ATT&CK**: http://localhost:5173/mitre-attack
- **IR Playbooks**: http://localhost:5173/ir-playbooks

### What to Check on Each Page

1. ✅ Page loads without errors
2. ✅ Content displays correctly
3. ✅ Dark theme toggle works
4. ✅ Navigation links work
5. ✅ Forms/interactions work (if applicable)
6. ✅ Print preview shows dark theme (if dark mode enabled)

---

## 🤖 Automated Testing

### Run Frontend Integration Test

```powershell
cd project\repo-cipher
python test_frontend_integration.py
```

This will:
- Test all 5 main pages
- Verify dark theme print support
- Check CSS loading
- Validate React components

### Run Specific Tests

```powershell
# Test IR Playbook Generator
python test_generate_playbook.py

# Test C4 Checklist
python test_c4_checklist.py

# Test Empty State
python test_c4_empty_state.py

# Test UX
python test_c4_ux.py
```

---

## 🐛 Troubleshooting

### Page Won't Load

1. **Check if frontend server is running**:
   ```powershell
   # Should see output like:
   # VITE v5.x.x  ready in xxx ms
   # ➜  Local:   http://localhost:5173/
   ```

2. **Check if port 5173 is in use**:
   ```powershell
   netstat -ano | findstr :5173
   ```

3. **Restart frontend server**:
   ```powershell
   cd project\repo-cipher\frontend
   npm run dev
   ```

### API Calls Fail

1. **Check if backend is running**:
   - Visit: http://localhost:8000/docs
   - Should see FastAPI documentation

2. **Check browser console** (F12):
   - Look for API errors
   - Check Network tab for failed requests

### Dark Theme Not Working

1. **Check browser console** (F12) for errors
2. **Verify CSS is loaded**: Check Network tab for `index.css`
3. **Try hard refresh**: `Ctrl+Shift+R` (or `Cmd+Shift+R`)

---

## 📋 Testing Checklist

### Home Page (`/`)
- [ ] Page loads successfully
- [ ] Title shows "Cipher - Threat Intelligence Platform"
- [ ] Navigation menu visible
- [ ] All links work
- [ ] Dark theme toggle works

### Threat Timeline (`/threat-timeline`)
- [ ] Page loads successfully
- [ ] Timeline visualization displays
- [ ] Can interact with timeline
- [ ] Data loads from API

### IOC Search (`/ioc-search`)
- [ ] Page loads successfully
- [ ] Search form visible
- [ ] Can enter search terms
- [ ] Results display correctly

### MITRE ATT&CK (`/mitre-attack`)
- [ ] Page loads successfully
- [ ] Coverage map displays
- [ ] Can interact with map
- [ ] Techniques load correctly

### IR Playbooks (`/ir-playbooks`)
- [ ] Page loads successfully
- [ ] Configuration form visible
- [ ] Can generate playbook
- [ ] Playbook displays correctly
- [ ] Export/Copy buttons work

### Dark Theme Print
- [ ] Enable dark theme
- [ ] Open print dialog (Ctrl+P)
- [ ] Preview shows dark background
- [ ] Text is readable (light on dark)
- [ ] Colors are preserved

---

## 🔗 Quick Links

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Test Results**: `project/repo-cipher/FRONTEND_TEST_RESULTS.md`

---

## 📝 Notes

- Frontend runs on **port 5173** (Vite dev server)
- Backend runs on **port 8000** (FastAPI)
- Both servers must be running for full functionality
- Dark theme print styles are automatically applied when dark mode is enabled

---

**Last Updated**: Frontend Integration Test - 100% Pass Rate ✅


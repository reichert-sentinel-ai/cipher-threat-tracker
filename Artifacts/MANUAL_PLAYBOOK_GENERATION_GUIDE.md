# How to Generate an IR Playbook - Manual Guide

## 🎯 Quick Steps

### 1. Open the Page
Navigate to: **http://localhost:5173/ir-playbooks**

### 2. You'll See the Empty State
```
┌─────────────────────────────────────────┐
│  📄 No Playbook Generated               │
│                                         │
│  Configure your incident parameters     │
│  above and click "Generate Playbook"   │
└─────────────────────────────────────────┘
```

### 3. Configuration Form (Above Empty State)
The form has 4 dropdowns:
- **Incident Type** - Click to select (default: Ransomware Attack)
- **Severity** - Click to select (default: High)
- **Scope** - Click to select (default: Single System)
- **Automation** - Click to select (default: Standard)

### 4. Click "Generate Playbook" Button
- Large button below the form
- Should say "Generate Playbook" or have a play icon ▶️

### 5. Wait for Generation
- Button will show loading state
- Playbook appears in 2-5 seconds

### 6. Verify Playbook Generated
You should see:
- ✅ Playbook ID (PB-YYYYMMDDHHMMSS)
- ✅ Playbook Overview Card
- ✅ Performance Metrics
- ✅ Tabs: Response Steps | Stakeholders | Evidence | Compliance

## 🔍 Troubleshooting

### If Generate Button Doesn't Work:

1. **Check Browser Console** (F12 → Console tab)
   - Look for red errors
   - Check if API calls are failing

2. **Check Network Tab** (F12 → Network tab)
   - Click Generate button
   - Look for `/api/ir-playbooks/generate` request
   - Check if it returns 200 (success) or error

3. **Verify Backend is Running**
   ```powershell
   Test-NetConnection -ComputerName localhost -Port 8000
   ```
   Should return: `TcpTestSucceeded : True`

4. **Check API Directly**
   Open in browser: http://localhost:8000/api/ir-playbooks/templates
   Should show JSON with templates

### Common Issues:

**Issue**: Dropdowns don't open
- **Solution**: Click directly on the button part of the dropdown
- **Solution**: Wait a moment for React to render

**Issue**: Generate button does nothing
- **Solution**: Check if backend API is running
- **Solution**: Check browser console for errors
- **Solution**: Verify all dropdowns have values selected

**Issue**: Playbook doesn't appear after clicking
- **Solution**: Wait 5-10 seconds (API call takes time)
- **Solution**: Check browser console for API errors
- **Solution**: Verify backend is running on port 8000

## 🧪 Automated Test

Run the automated test:
```powershell
cd project\repo-cipher
python test_generate_playbook.py
```

Or with visible browser:
```powershell
python test_generate_playbook.py
```

Or headless:
```powershell
python test_generate_playbook.py --headless
```

## ✅ Expected Result

After clicking Generate, you should see:

```
┌─────────────────────────────────────────┐
│  Playbook ID: PB-20241104230000         │
│  Incident Type: Ransomware Attack       │
│  Severity: HIGH                         │
│  Estimated Duration: 24-72 hours        │
└─────────────────────────────────────────┘

[Performance Metrics]
Time to Detect | Time to Respond | Time to Contain | ...

[Tabs]
Response Steps | Stakeholders | Evidence | Compliance
```

## 📝 Manual Checklist

- [ ] Page loads at http://localhost:5173/ir-playbooks
- [ ] Empty state message is visible
- [ ] Configuration form is visible
- [ ] Can see "Generate Playbook" button
- [ ] Click Generate button
- [ ] Button shows loading state
- [ ] Playbook ID appears (PB-XXXXXX)
- [ ] Playbook sections are visible
- [ ] Tabs are clickable
- [ ] Export button works
- [ ] Copy button works


# How to Generate an IR Playbook - Step-by-Step Guide

## Quick Steps

1. **Navigate to**: http://localhost:5173/ir-playbooks

2. **Configure Incident Parameters**:
   - **Incident Type**: Click dropdown and select (e.g., "Ransomware Attack")
   - **Severity**: Click dropdown and select (e.g., "High")
   - **Scope**: Click dropdown and select (e.g., "Single System")
   - **Automation**: Click dropdown and select (e.g., "Standard")

3. **Click "Generate Playbook"** button

4. **Wait for Generation**: The playbook will appear with:
   - Playbook ID (PB-XXXXXX)
   - All NIST phases
   - Steps, Stakeholders, Evidence, Compliance tabs

## Manual Testing Checklist

- [ ] Page loads successfully
- [ ] Configuration form is visible
- [ ] All 4 dropdowns are clickable
- [ ] Can select incident type
- [ ] Can select severity
- [ ] Can select scope
- [ ] Can select automation level
- [ ] Generate button is visible
- [ ] Generate button is clickable
- [ ] Playbook generates after clicking
- [ ] Playbook ID appears
- [ ] All tabs are accessible
- [ ] Export button works
- [ ] Copy button works

## Troubleshooting

**If playbook doesn't generate:**
1. Check browser console for errors (F12)
2. Verify backend is running on port 8000
3. Check network tab for API errors
4. Verify all dropdowns have values selected

**If dropdowns don't open:**
1. Click directly on the dropdown button
2. Wait a moment for React to render
3. Try clicking multiple times
4. Check if templates loaded from API


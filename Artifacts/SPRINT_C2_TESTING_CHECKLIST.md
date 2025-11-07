# Sprint C2: IOC Search Interface - Testing Guide

## ✅ Implementation Complete

### Backend Status
- ✅ Server running on `http://localhost:8000`
- ✅ IOC Search API endpoints working
- ✅ All Pydantic errors fixed
- ✅ API tested successfully

### Frontend Status  
- ✅ Dev server running on `http://localhost:5173` (Status: 200)
- ✅ IOCSearch component created (816 lines)
- ✅ Route configured in App.jsx (`/ioc-search`)
- ✅ Component exports correctly
- ✅ All UI components created

## 🧪 Testing Checklist

Navigate to: **http://localhost:5173/ioc-search**

### Test 1: Search Returns Relevant IOCs
- [ ] Enter an IOC value (e.g., `185.220.101.45`)
- [ ] Click Search button
- [ ] Verify: Results appear with IOC details

### Test 2: IOC Type Auto-Detection
- [ ] Enter IP: `185.220.101.45` → Should detect as "ip"
- [ ] Enter Domain: `malicious-domain.com` → Should detect as "domain"
- [ ] Enter Email: `test@evil.com` → Should detect as "email"
- [ ] Enter Hash: `a1b2c3d4...` → Should detect as "hash"

### Test 3: Enrichment Displays All Data Sections
- [ ] Click on any IOC result
- [ ] Verify Enrichment tab opens
- [ ] Check all sections render:
  - Reputation score
  - Community votes (pie chart)
  - Threat intelligence data
  - Related IOCs
  - Detection rules
  - Recommendations

### Test 4: Geolocation Shows for IP Addresses
- [ ] Search for an IP address
- [ ] Click to enrich
- [ ] Verify: Geolocation section shows country, city, ASN

### Test 5: WHOIS Displays for Domains
- [ ] Search for a domain
- [ ] Click to enrich
- [ ] Verify: WHOIS section shows registrar, creation date

### Test 6: Malware Analysis Shows for Hashes
- [ ] Search for a hash value
- [ ] Click to enrich
- [ ] Verify: Malware analysis section shows behaviors, MITRE techniques

### Test 7: Related IOCs Are Clickable
- [ ] Enrich any IOC
- [ ] Scroll to Related IOCs section
- [ ] Click on a related IOC
- [ ] Verify: It enriches the related IOC

### Test 8: Correlation Analysis Renders Correctly
- [ ] Enrich an IOC
- [ ] Scroll to Correlation Analysis section
- [ ] Verify: Correlation score, related IOCs, timeline display

### Test 9: Bulk Check Processes Multiple IOCs
- [ ] Switch to Bulk Check tab
- [ ] Enter multiple IOCs (one per line)
- [ ] Click "Check All IOCs"
- [ ] Verify: Statistics and detailed results appear

### Test 10: Copy-to-Clipboard Functions Properly
- [ ] Click copy icon on any IOC
- [ ] Paste in a text editor
- [ ] Verify: IOC value copied correctly

### Test 11: Feed Status Displays Accurately
- [ ] Check feed status cards at top of page
- [ ] Verify: All 5 feeds show statistics
- [ ] Verify: Feed reliability badges display

### Test 12: All Filters Update Results Dynamically
- [ ] Use IOC Type filter (select "IP")
- [ ] Use Threat Level filter (select "Critical")
- [ ] Enter search query
- [ ] Verify: Results update based on filters

## 🐛 Troubleshooting

### Route Not Found Error
- **Solution**: Hard refresh browser (`Ctrl+Shift+R`)
- **Check**: Browser console for import errors
- **Verify**: Component file exists at `src/components/IOCSearch.jsx`

### API Calls Failing
- **Verify**: Backend server running on port 8000
- **Check**: Browser console for CORS errors
- **Test**: Visit `http://localhost:8000/docs` to verify API

### Component Not Loading
- **Check**: Browser console for syntax errors
- **Verify**: All imports are correct
- **Restart**: Frontend dev server

## 📊 Expected Results

- ✅ All 5 threat intelligence feeds show status
- ✅ Search returns relevant IOCs with threat levels
- ✅ Type detection works for IP, domain, email, hash, URL
- ✅ Enrichment shows all data sections
- ✅ Geolocation appears for IP addresses
- ✅ WHOIS appears for domains
- ✅ Malware analysis appears for hashes
- ✅ Related IOCs are clickable
- ✅ Correlation analysis displays correctly
- ✅ Bulk check processes multiple IOCs
- ✅ Copy-to-clipboard functions properly
- ✅ Feed status displays accurately
- ✅ Filters update results dynamically

## 🎯 Success Criteria

All 12 checklist items should pass. The IOC Search interface demonstrates:
- Threat intelligence aggregation
- IOC enrichment and correlation
- Multi-source data fusion
- Security recommendations
- Bulk processing capabilities

**Status**: Ready for testing! 🚀


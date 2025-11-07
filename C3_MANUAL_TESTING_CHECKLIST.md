# Sprint C3: MITRE ATT&CK Coverage Map - Manual Testing Checklist

## Pre-Testing Setup

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 5173
- [ ] Both servers accessible (no errors in console)
- [ ] Browser console open (F12) to monitor errors

---

## 1. Route Accessibility & Navigation

### 1.1 Navigation Link
- [ ] Navigate to http://localhost:5173
- [ ] Verify "MITRE ATT&CK" link appears in navigation bar
- [ ] Click "MITRE ATT&CK" link
- [ ] Verify route changes to `/mitre-attack`
- [ ] Verify page loads (not blank white screen)

### 1.2 Direct Route Access
- [ ] Navigate directly to http://localhost:5173/mitre-attack
- [ ] Verify page loads successfully
- [ ] No console errors in browser dev tools

### 1.3 Browser Console Check
- [ ] Open browser console (F12)
- [ ] Check for any JavaScript errors
- [ ] Check for any network errors (404, 500, CORS issues)
- [ ] Verify API calls are being made successfully

---

## 2. Loading States

### 2.1 Initial Load
- [ ] Verify loading spinner appears on initial page load
- [ ] Verify loading spinner disappears after data loads
- [ ] Verify no infinite loading state

### 2.2 Data Loading
- [ ] Verify data appears within 2-3 seconds
- [ ] Check Network tab - verify API calls to `/api/mitre/coverage-matrix` and `/api/mitre/gap-analysis`

---

## 3. Coverage Matrix Tab

### 3.1 Overview Section
- [ ] Verify "Overall Coverage" card displays
- [ ] Verify percentage is shown (e.g., "81.2%")
- [ ] Verify total techniques count displayed
- [ ] Verify covered techniques count displayed
- [ ] Verify gap techniques count displayed

### 3.2 Technique Grid
- [ ] Verify all 14 tactics are displayed
- [ ] Verify techniques are shown under each tactic
- [ ] Verify techniques have correct color coding:
  - [ ] **Red** (none) - No detection coverage
  - [ ] **Orange** (partial) - Partial detection coverage
  - [ ] **Blue** (good) - Good detection coverage
  - [ ] **Green** (excellent) - Excellent detection coverage

### 3.3 Technique Cards
- [ ] Verify each technique shows:
  - [ ] Technique ID (e.g., T1566)
  - [ ] Technique name (e.g., "Phishing")
  - [ ] Coverage badge/indicator
  - [ ] Threat actors using this technique (if any)
  - [ ] Recent detections count

### 3.4 Search Functionality
- [ ] Type in search box (e.g., "Phishing")
- [ ] Verify techniques filter in real-time
- [ ] Verify search works for:
  - [ ] Technique ID (e.g., "T1566")
  - [ ] Technique name (e.g., "Phishing")
  - [ ] Tactic name (e.g., "Initial Access")
- [ ] Clear search - verify all techniques reappear

### 3.5 Interactive Elements
- [ ] Click on a technique card
- [ ] Verify technique details modal/section appears
- [ ] Verify details include:
  - [ ] Full description
  - [ ] Data sources
  - [ ] Platforms affected
  - [ ] Detection rules
- [ ] Close details modal/section

---

## 4. Tactics Tab

### 4.1 Bar Chart
- [ ] Verify bar chart displays for all 14 tactics
- [ ] Verify each bar shows coverage percentage
- [ ] Verify bars are color-coded appropriately
- [ ] Hover over bars - verify tooltip shows details
- [ ] Verify chart is responsive (resize browser window)

### 4.2 Tactic Cards
- [ ] Verify all 14 tactics have individual cards
- [ ] Each card should show:
  - [ ] Tactic name
  - [ ] Coverage percentage
  - [ ] Total techniques count
  - [ ] Covered techniques count
  - [ ] Gap count
  - [ ] Priority gaps list
  - [ ] Progress bar visualization

### 4.3 Tactic Interaction
- [ ] Click on a tactic card
- [ ] Verify techniques for that tactic are filtered/displayed
- [ ] Verify "View All Techniques" or similar action works

---

## 5. Gap Analysis Tab

### 5.1 Critical Gaps Section
- [ ] Verify critical gaps are listed
- [ ] Each gap should show:
  - [ ] Technique ID and name
  - [ ] Risk level (Critical/High/Medium)
  - [ ] Threat actors using this technique
  - [ ] Recent campaigns count
  - [ ] Estimated effort/time to implement

### 5.2 Risk Score
- [ ] Verify overall risk score is displayed
- [ ] Verify score is in range 0-100
- [ ] Verify risk indicator (color coding)

### 5.3 Recommended Detections
- [ ] Verify recommended detections are listed
- [ ] Each recommendation should show:
  - [ ] Technique ID and name
  - [ ] Recommended data source
  - [ ] Detection method
  - [ ] Implementation priority
  - [ ] Expected false positive rate

### 5.4 Priority Order
- [ ] Verify priority order list is displayed
- [ ] Verify items are ordered by priority
- [ ] Verify actionable recommendations are shown

---

## 6. Threat Actors Tab

### 6.1 Threat Actor Selection
- [ ] Verify dropdown/selector for threat actors
- [ ] Default selection: APT28
- [ ] Select different threat actor (e.g., APT29, Lazarus Group)
- [ ] Verify data updates for selected actor

### 6.2 TTPs Display
- [ ] Verify techniques used by threat actor are listed
- [ ] Each technique should show:
  - [ ] Technique ID and name
  - [ ] Tactic
  - [ ] Frequency (common/occasional/rare)
  - [ ] First observed date
  - [ ] Last observed date
  - [ ] Detection coverage indicator

### 6.3 Coverage Summary
- [ ] Verify detection coverage percentage is shown
- [ ] Verify tactics distribution chart displays
- [ ] Verify high-risk techniques section shows techniques without detection

### 6.4 Charts
- [ ] Verify tactics distribution chart renders
- [ ] Verify chart is interactive (hover, tooltips)
- [ ] Verify chart displays correct data for selected actor

---

## 7. Overview Tab

### 7.1 Key Metrics
- [ ] Verify key metrics cards display:
  - [ ] Overall coverage percentage
  - [ ] Total techniques count
  - [ ] Coverage distribution
  - [ ] Gap count

### 7.2 Coverage Distribution Chart
- [ ] Verify pie chart displays coverage distribution
- [ ] Verify chart shows:
  - [ ] Excellent coverage slice
  - [ ] Good coverage slice
  - [ ] Partial coverage slice
  - [ ] No coverage slice
- [ ] Verify legend displays correctly
- [ ] Hover over slices - verify tooltip shows percentages

### 7.3 Common Data Sources
- [ ] Verify common data sources are listed
- [ ] Verify data sources are relevant (e.g., Sysmon, EDR, Network logs)

### 7.4 Recommended Actions
- [ ] Verify recommended action items are listed
- [ ] Verify actions are prioritized
- [ ] Verify actionable recommendations (not just informational)

---

## 8. Visual Design & UI/UX

### 8.1 Dark Mode Support
- [ ] Verify dark mode works (if available)
- [ ] Verify text is readable in dark mode
- [ ] Verify charts are visible in dark mode
- [ ] Verify colors maintain contrast

### 8.2 Responsive Design
- [ ] Resize browser to mobile width (<768px)
- [ ] Verify layout adapts correctly
- [ ] Verify charts are responsive
- [ ] Verify text is readable
- [ ] Verify navigation is accessible

### 8.3 Color Coding Consistency
- [ ] Verify coverage colors are consistent across all tabs
- [ ] Verify risk level colors are consistent
- [ ] Verify badge colors match their meaning

### 8.4 Typography & Spacing
- [ ] Verify text is readable
- [ ] Verify proper spacing between elements
- [ ] Verify headings are properly sized
- [ ] Verify no text overflow

---

## 9. Error Handling

### 9.1 API Errors
- [ ] Stop backend server
- [ ] Reload frontend page
- [ ] Verify error message is displayed (not blank screen)
- [ ] Verify error is user-friendly
- [ ] Restart backend server
- [ ] Verify page recovers and data loads

### 9.2 Network Errors
- [ ] Simulate network failure (disable network in dev tools)
- [ ] Verify graceful error handling
- [ ] Re-enable network
- [ ] Verify retry mechanism works (if implemented)

### 9.3 Invalid Data
- [ ] Navigate to invalid technique ID in URL (if possible)
- [ ] Verify error handling
- [ ] Verify user is redirected or shown error message

---

## 10. Performance

### 10.1 Page Load Time
- [ ] Verify page loads within 3 seconds
- [ ] Check Network tab - verify API calls complete quickly
- [ ] Verify no unnecessary API calls on initial load

### 10.2 Chart Rendering
- [ ] Verify charts render smoothly
- [ ] Verify no lag when hovering over chart elements
- [ ] Verify chart animations are smooth (if any)

### 10.3 Search Performance
- [ ] Type in search box rapidly
- [ ] Verify search filters quickly (no lag)
- [ ] Verify no excessive re-renders

---

## 11. Integration Testing

### 11.1 Cross-Tab Navigation
- [ ] Switch between tabs rapidly
- [ ] Verify data persists correctly
- [ ] Verify no data loss when switching tabs

### 11.2 Data Consistency
- [ ] Verify coverage percentages are consistent across tabs
- [ ] Verify technique counts match across different views
- [ ] Verify gap analysis matches coverage matrix

### 11.3 State Management
- [ ] Select a threat actor
- [ ] Switch tabs
- [ ] Switch back to Threat Actors tab
- [ ] Verify selected threat actor is still selected

---

## 12. Browser Compatibility

### 12.1 Chrome/Edge
- [ ] Test in Chrome
- [ ] Test in Edge
- [ ] Verify all features work

### 12.2 Firefox
- [ ] Test in Firefox
- [ ] Verify all features work
- [ ] Verify no console errors

### 12.3 Safari (if available)
- [ ] Test in Safari
- [ ] Verify all features work

---

## Testing Notes

**Date:** _______________  
**Tester:** _______________  
**Browser:** _______________  
**OS:** _______________

### Issues Found:
1. 
2. 
3. 

### Recommendations:
1. 
2. 
3. 

---

## Sign-Off

- [ ] All critical tests passed
- [ ] No blocking issues found
- [ ] Ready for production: ☐ Yes  ☐ No

**Tester Signature:** _______________  
**Date:** _______________

# Cipher Threat Intelligence Platform - UX Testing Guide

## 🎯 Pages Available for UX Testing

### Base URL: http://localhost:5173

---

## 1. 🆕 **IR Playbooks** (`/ir-playbooks`) - **PRIORITY FOR UX TESTING**

**Status**: ✅ Just completed (Sprint C4)  
**Why UX Testing Needed**: New feature, complex interactions, multiple workflows

### UX Testing Checklist:
- [ ] **Configuration Form Usability**
  - Are the dropdowns (Incident Type, Severity, Scope, Automation) clear and easy to use?
  - Are the labels descriptive?
  - Is the "Generate Playbook" button prominent enough?

- [ ] **Playbook Display & Navigation**
  - Is the phase navigation intuitive?
  - Can users easily understand which phase they're in?
  - Are the phase buttons clickable and responsive?

- [ ] **Tab Navigation**
  - Are the tabs (Steps, Stakeholders, Evidence, Compliance) clearly labeled?
  - Is the active tab obvious?
  - Is tab switching smooth?

- [ ] **Content Readability**
  - Are the playbook steps easy to read?
  - Is the information hierarchy clear?
  - Are success criteria and escalation triggers easy to scan?

- [ ] **Export/Copy Functionality**
  - Are the export and copy buttons easy to find?
  - Is feedback provided when actions complete?
  - Are the buttons appropriately sized?

- [ ] **Responsive Design**
  - Does it work well on mobile/tablet?
  - Are dropdowns usable on touch devices?
  - Does the layout adapt well to smaller screens?

- [ ] **Performance Metrics Display**
  - Are the metrics easy to understand?
  - Is the visual presentation clear?
  - Are colors/sizing appropriate?

- [ ] **Error Handling**
  - What happens if API fails?
  - Are error messages clear and actionable?
  - Is loading state visible?

---

## 2. **Threat Timeline** (`/threat-timeline`)

**Status**: ✅ Implemented (Sprint C1)  
**UX Testing Focus**: Timeline visualization, filtering, interaction

### Key UX Areas:
- Timeline visualization clarity
- Filter functionality
- Event details display
- Search and filtering interactions

---

## 3. **IOC Search** (`/ioc-search`)

**Status**: ✅ Implemented (Sprint C2)  
**UX Testing Focus**: Search interface, results display, IOC enrichment

### Key UX Areas:
- Search input usability
- Results presentation
- IOC detail views
- Correlation visualization

---

## 4. **MITRE ATT&CK Map** (`/mitre-attack`)

**Status**: ✅ Implemented (Sprint C3)  
**UX Testing Focus**: Coverage visualization, gap analysis, threat actor mapping

### Key UX Areas:
- Coverage matrix visualization
- Tab navigation
- Chart readability
- Gap analysis presentation

---

## 5. **Home Page** (`/`)

**Status**: Basic landing page  
**UX Testing Focus**: Navigation, introduction clarity

### Key UX Areas:
- Clear value proposition
- Navigation to features
- Visual hierarchy

---

## 🎨 Overall UX Testing Considerations

### Navigation
- [ ] Is navigation consistent across all pages?
- [ ] Is the current page obvious in the nav?
- [ ] Are breadcrumbs needed?
- [ ] Mobile navigation menu?

### Dark Mode
- [ ] Does dark mode work well on all pages?
- [ ] Are colors readable in dark mode?
- [ ] Are contrast ratios sufficient?

### Loading States
- [ ] Are loading indicators clear?
- [ ] Do users understand what's happening?
- [ ] Are skeleton screens needed?

### Error States
- [ ] Are error messages helpful?
- [ ] Can users recover from errors easily?
- [ ] Is retry functionality available?

### Accessibility
- [ ] Keyboard navigation works?
- [ ] Screen reader compatible?
- [ ] Focus indicators visible?
- [ ] Color contrast adequate?

---

## 📋 Recommended UX Testing Priority

### 🔴 **HIGH PRIORITY** (New Feature)
1. **IR Playbooks** (`/ir-playbooks`) - Sprint C4 - Most critical for UX testing

### 🟡 **MEDIUM PRIORITY** (Existing Features)
2. **Threat Timeline** (`/threat-timeline`)
3. **IOC Search** (`/ioc-search`)
4. **MITRE ATT&CK** (`/mitre-attack`)

### 🟢 **LOW PRIORITY** (Simple Pages)
5. **Home Page** (`/`)

---

## 🚀 Quick UX Testing Checklist for IR Playbooks

**URL**: http://localhost:5173/ir-playbooks

### Critical Path Testing:
1. ✅ Can user select incident type easily?
2. ✅ Can user configure severity/scope/automation?
3. ✅ Does "Generate Playbook" button work?
4. ✅ Can user navigate between phases?
5. ✅ Can user switch between tabs?
6. ✅ Can user export playbook?
7. ✅ Can user copy playbook?
8. ✅ Is information easy to read?
9. ✅ Does it work on mobile?
10. ✅ Are error messages helpful?

---

## 📝 UX Testing Tools Recommended

- **Browser DevTools**: Responsive design testing
- **Accessibility**: Lighthouse, axe DevTools
- **Performance**: Lighthouse Performance audit
- **Usability**: Manual testing with real users
- **Cross-browser**: Chrome, Firefox, Edge, Safari

---

## 🎯 Focus Area: IR Playbooks UX Testing

Since Sprint C4 was just completed, **IR Playbooks** should be the primary focus for UX testing to ensure:
- The complex workflow is intuitive
- Users can generate playbooks easily
- Information is presented clearly
- All interactions feel smooth
- Mobile experience is good


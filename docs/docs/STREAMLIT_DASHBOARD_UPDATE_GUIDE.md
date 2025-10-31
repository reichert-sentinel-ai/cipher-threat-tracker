# 🎨 Streamlit Dashboard Update Guide

**Goal:** Add 12 new pages to existing 10-page dashboard  
**Target:** 22 total pages for complete portfolio presentation  
**Status:** Template created, ready for implementation

---

## 📋 NEW PAGES TO ADD

### Measure Pages (11 pages)

1. **KED** - Kidney Health Evaluation [3x weighted, NEW 2025]
2. **EED** - Eye Exam for Diabetes
3. **PDC-DR** - Medication Adherence (Diabetes)
4. **BPD** - Blood Pressure Control (Diabetes) [NEW 2025]
5. **CBP** - Controlling High Blood Pressure [3x weighted]
6. **SUPD** - Statin Therapy
7. **PDC-RASA** - Medication Adherence (Hypertension)
8. **PDC-STA** - Medication Adherence (Cholesterol)
9. **BCS** - Breast Cancer Screening
10. **COL** - Colorectal Cancer Screening
11. **GSD UPDATE** - Refresh with new template

### HEI Page (1 page)

12. **HEI Dashboard** - Health Equity Index visualization

---

## 🔧 Implementation Steps

### Step 1: Update Navigation (streamlit_app.py)

Add new pages to sidebar selectbox:

```python
page = st.sidebar.selectbox(
    "Select Page",
    [
        "🏠 Executive Summary",
        "⚠️ Problem Statement",
        "📊 Portfolio Overview",
        "💰 Financial Impact",
        "⭐ Star Rating Simulator",
        "🤖 AI/ML Models",
        "🏥 Health Equity Index",  # NEW
        "📈 Visualizations",
        "💻 Technical Architecture",
        "👤 About Me",
        # NEW MEASURE PAGES
        "📊 KED - Kidney Health",
        "📊 EED - Eye Exam",
        "📊 PDC-DR - Diabetes Meds",
        "📊 BPD - BP Control (Diabetes)",
        "📊 CBP - Blood Pressure",
        "📊 SUPD - Statin Therapy",
        "📊 PDC-RASA - HTN Meds",
        "📊 PDC-STA - Cholesterol Meds",
        "📊 BCS - Breast Cancer",
        "📊 COL - Colorectal Cancer",
        "📊 GSD - Glycemic Status"  # Updated
    ]
)
```

### Step 2: Add Page Logic

For each measure, add:

```python
elif page == "📊 KED - Kidney Health":
    from streamlit_pages.measure_page_template import create_measure_page
    create_measure_page(
        measure_code="KED",
        measure_name="Kidney Health Evaluation for Patients with Diabetes",
        tier=1,
        weight=3.0,
        value_estimate="$360K-$615K",
        description="Percentage of members 18-75 with diabetes who received kidney health evaluation (eGFR and urine albumin tests) during the measurement year.",
        target_population="Members 18-75 years with diabetes diagnosis",
        numerator_criteria="Both eGFR and ACR tests completed in measurement year",
        denominator_criteria="Members with diabetes, continuous enrollment, pharmacy benefit",
        exclusions="ESRD, kidney transplant, hospice, SNP enrollment",
        new_measure=True,
        model_auc=0.87
    )
```

### Step 3: Create HEI Dashboard Page

See `HEI_DASHBOARD_DESIGN.md` for complete implementation.

---

## 📊 Complete Page Structure (22 Pages)

### Executive/Overview (4 pages)
1. Executive Summary
2. Problem Statement  
3. Portfolio Overview
4. Financial Impact

### Analysis (3 pages)
5. Star Rating Simulator
6. AI/ML Models
7. **HEI Dashboard** ← NEW

### Technical (2 pages)
8. Visualizations
9. Technical Architecture

### Personal (1 page)
10. About Me

### Tier 1 - Diabetes (5 pages)
11. **GSD** - Glycemic Status [3x]
12. **KED** - Kidney Health [3x, NEW 2025] ← NEW
13. **EED** - Eye Exam ← NEW
14. **PDC-DR** - Medication Adherence ← NEW
15. **BPD** - BP Control [NEW 2025] ← NEW

### Tier 2 - Cardiovascular (4 pages)
16. **CBP** - Blood Pressure [3x] ← NEW
17. **SUPD** - Statin Therapy ← NEW
18. **PDC-RASA** - HTN Meds ← NEW
19. **PDC-STA** - Cholesterol Meds ← NEW

### Tier 3 - Cancer Screening (2 pages)
20. **BCS** - Breast Cancer ← NEW
21. **COL** - Colorectal Cancer ← NEW

### Navigation (1 page)
22. Measure comparison/selector

---

## 🎯 Priority Order

**Phase 1: High-Value Measures** (3x weighted + NEW)
1. KED [3x, NEW 2025]
2. CBP [3x]
3. BPD [NEW 2025]
4. GSD [3x] - update

**Phase 2: HEI Showcase**
5. HEI Dashboard [UNIQUE, 2+ years early]

**Phase 3: Standard Measures**
6. EED, PDC-DR, SUPD, PDC-RASA, PDC-STA, BCS, COL

---

## ⏱️ Time Estimates

- Measure page (using template): 15-20 min each
- HEI dashboard page: 60 min
- Navigation updates: 15 min
- Testing & polish: 30 min

**Total: 4-5 hours**

---

**Status:** Guide complete, ready for implementation  
**Next:** Systematic page creation using template



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*

# 🏥 Criminal Intelligence Database API Documentation: Health Equity Index (HEI) Endpoints

**Version:** 2.0  
**Date:** October 25, 2025  
**New Feature:** HEI (Health Equity Index) - CMS 2027 Mandate (2+ years early)

---

## 🎯 Overview

The Criminal Intelligence Database Star Rating Portfolio Optimizer now includes comprehensive Health Equity Index (HEI) endpoints, implementing CMS's 2027 mandate **2+ years ahead of schedule**.

**Value Proposition:**
- **$10M-$20M downside protection** (100K individual plan)
- **First-mover competitive advantage**
- **Proactive equity management**
- **CMS compliance ready**

---

## 📊 Complete API Endpoint List

### **Total Endpoints: 17**

| Category | Endpoints | Description |
|----------|-----------|-------------|
| **Health Equity Index** | 4 | NEW - Equity analysis & compliance |
| **Predictions** | 3 | Gap predictions (single, batch, portfolio) |
| **Portfolio** | 4 | Portfolio management & optimization |
| **Analytics** | 3 | Star ratings, simulations, ROI |
| **Measures** | 3 | Measure information & performance |

---

## 🆕 HEALTH EQUITY INDEX (HEI) ENDPOINTS

### **Base URL:** `/api/v1/equity`

---

### **1. POST `/equity/analyze`**

**Analyze health equity for a single Criminal Intelligence Database measure**

Performs stratified analysis by demographic group to identify disparities in measure performance.

**Request Body:**
```json
{
  "measure_code": "GSD",
  "measure_results": [
    {
      "member_id": "M001",
      "GSD_in_denominator": 1,
      "GSD_in_numerator": 1,
      "GSD_gap": 0
    }
  ],
  "hei_data": [
    {
      "member_id": "M001",
      "race_ethnicity_std": "WHITE",
      "language_std": "ENGLISH",
      "is_lep": 0,
      "lis": 0,
      "dual_eligible": 0
    }
  ],
  "stratification_var": "race_ethnicity_std",
  "disparity_threshold": 10.0,
  "measurement_year": 2025
}
```

**Response:**
```json
{
  "request_id": "abc123",
  "measure_code": "GSD",
  "stratification_var": "race_ethnicity_std",
  "stratified_performance": [
    {
      "group": "WHITE",
      "denominator": 40,
      "numerator": 32,
      "gaps": 8,
      "compliance_rate": 80.0,
      "gap_rate": 20.0,
      "is_valid_group": true
    },
    {
      "group": "BLACK",
      "denominator": 30,
      "numerator": 18,
      "gaps": 12,
      "compliance_rate": 60.0,
      "gap_rate": 40.0,
      "is_valid_group": true
    }
  ],
  "disparity_info": {
    "has_disparity": true,
    "disparity_magnitude": 20.0,
    "disparity_category": "HIGH",
    "highest_performing_group": "WHITE",
    "lowest_performing_group": "BLACK",
    "highest_compliance_rate": 80.0,
    "lowest_compliance_rate": 60.0,
    "equity_score": 60.0
  },
  "analysis_timestamp": "2025-10-25T12:00:00",
  "measurement_year": 2025
}
```

**Use Case:** Detect if certain demographic groups have lower compliance rates for a specific measure.

---

### **2. POST `/equity/score`**

**Calculate portfolio-level Health Equity Index (HEI) score**

Evaluates equity across all measures and determines CMS penalty tier.

**Penalty Tiers:**
- Score ≥ 70: **No penalty** ✅
- Score 50-69: **-0.25 stars** ($10M penalty)
- Score < 50: **-0.5 stars** ($20M penalty)

**Request Body:**
```json
{
  "measure_results": {
    "GSD": [{"member_id": "M001", "GSD_in_denominator": 1, "GSD_in_numerator": 1, "GSD_gap": 0}],
    "KED": [{"member_id": "M001", "KED_in_denominator": 1, "KED_in_numerator": 1, "KED_gap": 0}]
  },
  "hei_data": [
    {"member_id": "M001", "race_ethnicity_std": "WHITE", "language_std": "ENGLISH"}
  ],
  "measure_weights": {
    "GSD": 3.0,
    "KED": 3.0
  },
  "stratification_vars": ["race_ethnicity_std", "language_std"],
  "measurement_year": 2025
}
```

**Response:**
```json
{
  "request_id": "def456",
  "overall_equity_score": 75.5,
  "penalty_category": "NO_PENALTY",
  "penalty_amount": 0.0,
  "measures_analyzed": 2,
  "measures_with_disparities": 0,
  "stratifications_evaluated": 2,
  "total_comparisons": 4,
  "equity_score_by_measure": {
    "GSD": 80.0,
    "KED": 71.0
  },
  "analysis_timestamp": "2025-10-25T12:05:00",
  "financial_impact": {
    "description": "No penalty - excellent equity performance",
    "estimated_value": 0,
    "penalty_stars": 0.0,
    "basis": "100K member MA plan"
  }
}
```

**Use Case:** Determine if your health plan meets CMS equity requirements and avoid penalties.

---

### **3. POST `/equity/interventions`**

**Get priority intervention recommendations**

Identifies top opportunities to improve equity with actionable recommendations.

**Request Body:** Same as `/equity/score` plus:
```json
{
  "...": "...",
  "top_n": 10
}
```

**Response:**
```json
{
  "request_id": "ghi789",
  "interventions": [
    {
      "priority_rank": 1,
      "measure": "GSD",
      "stratification": "race_ethnicity_std",
      "target_group": "BLACK",
      "current_rate": 60.0,
      "goal_rate": 80.0,
      "gap_to_close": 20.0,
      "disparity_category": "HIGH",
      "measure_weight": 3.0,
      "recommended_actions": [
        "Conduct cultural competency training for BLACK population",
        "Partner with BLACK community organizations",
        "Analyze provider network adequacy for this group",
        "Review barriers to care specific to this group",
        "Target outreach to BLACK members with gaps",
        "Monitor progress monthly for GSD"
      ]
    }
  ],
  "total_interventions": 10,
  "high_priority_count": 3,
  "financial_impact_potential": "$10M-$20M penalty avoidance",
  "analysis_timestamp": "2025-10-25T12:10:00"
}
```

**Use Case:** Create an actionable equity improvement plan to avoid CMS penalties.

---

### **4. POST `/equity/report`**

**Generate comprehensive HEI report**

Creates formatted report (summary or detailed) for executive presentations.

**Request Body:**
```json
{
  "measure_results": {"...": "..."},
  "hei_data": [...],
  "measure_weights": {...},
  "stratification_vars": ["race_ethnicity_std"],
  "report_format": "summary",
  "measurement_year": 2025
}
```

**Report Formats:**
- `"summary"`: 1-2 pages (executive brief)
- `"detailed"`: 5-10 pages (comprehensive analysis)

**Response:**
```json
{
  "request_id": "jkl012",
  "report_format": "summary",
  "report_content": "=== HEALTH EQUITY INDEX (HEI) REPORT ===\n...",
  "overall_equity_score": 75.5,
  "penalty_category": "NO_PENALTY",
  "key_findings": [
    "Excellent equity performance (score: 75.5)",
    "0 measures have significant disparities"
  ],
  "top_priorities": [],
  "analysis_timestamp": "2025-10-25T12:15:00"
}
```

**Use Case:** Executive reporting, board presentations, CMS compliance documentation.

---

## 🔄 Complete Endpoint Reference

### **Predictions** (`/api/v1`)

1. **POST `/predict/{measure_code}`** - Single member prediction
2. **POST `/predict/batch/{measure_code}`** - Batch predictions
3. **POST `/predict/portfolio`** - Portfolio-level predictions

### **Portfolio** (`/api/v1/portfolio`)

4. **GET `/portfolio/summary`** - Portfolio summary
5. **POST `/portfolio/gaps`** - Generate gap lists
6. **GET `/portfolio/priority-list`** - Priority members
7. **POST `/portfolio/optimize`** - Cross-measure optimization

### **Analytics** (`/api/v1/analytics`)

8. **POST `/analytics/star-rating`** - Calculate star rating
9. **POST `/analytics/simulate`** - Star rating scenarios
10. **GET `/analytics/roi`** - ROI calculation

### **Measures** (`/api/v1/measures`)

11. **GET `/measures`** - List all 12 measures
12. **GET `/measures/{measure_code}`** - Measure details
13. **GET `/measures/{measure_code}/performance`** - Current performance

### **Health Equity Index** (`/api/v1/equity`) **← NEW!**

14. **POST `/equity/analyze`** - Single measure equity analysis
15. **POST `/equity/score`** - Portfolio equity score & penalty tier
16. **POST `/equity/interventions`** - Priority recommendations
17. **POST `/equity/report`** - Comprehensive equity report

---

## 🔐 Authentication

**API Key Header:**
```
X-API-Key: your-api-key-here
```

**Rate Limiting:**
- 100 requests/minute per API key
- 1000 requests/hour per API key

---

## 📋 Example Workflows

### **Workflow 1: Complete Equity Assessment**

1. **Analyze each measure:** `POST /equity/analyze` (x12 measures)
2. **Calculate portfolio score:** `POST /equity/score`
3. **Get interventions:** `POST /equity/interventions`
4. **Generate report:** `POST /equity/report`

**Result:** Complete equity assessment with actionable recommendations.

---

### **Workflow 2: Proactive Equity Monitoring**

**Monthly:**
1. Calculate portfolio equity score
2. Monitor penalty category
3. Track equity score trends

**Quarterly:**
1. Full equity analysis
2. Update intervention plans
3. Report to board/CMS

**Annually:**
1. Comprehensive equity report
2. Strategic equity planning
3. CMS compliance submission

---

## 💰 Financial Impact Examples

### **Scenario 1: Avoid HIGH Penalty**
- Current equity score: 45
- Risk: -0.5 stars = **$20M penalty**
- Action: Implement top 10 interventions
- Target: Score ≥ 70
- **Savings: $20M**

### **Scenario 2: Avoid MODERATE Penalty**
- Current equity score: 65
- Risk: -0.25 stars = **$10M penalty**
- Action: Focus on 3 high-priority measures
- Target: Score ≥ 70
- **Savings: $10M**

### **Scenario 3: Maintain Excellence**
- Current equity score: 75
- Risk: None
- Action: Proactive monitoring
- Target: Maintain ≥ 70
- **Protection: Competitive advantage**

---

## 🎯 HEI Implementation Advantages

### **First-Mover Benefits:**
1. ✅ **2+ years ahead** of CMS 2027 mandate
2. ✅ **Proactive equity management** vs reactive compliance
3. ✅ **Competitive differentiation** in market
4. ✅ **Risk mitigation** before penalties start
5. ✅ **Industry leadership** position

### **Technical Benefits:**
1. ✅ **Complete API** for equity analysis
2. ✅ **Automated monitoring** capabilities
3. ✅ **Actionable insights** with recommendations
4. ✅ **Executive reporting** ready
5. ✅ **Integration-ready** for EHR/claims systems

---

## 📞 Support & Documentation

**API Documentation:** `/docs` (Swagger UI)  
**Interactive API:** `/redoc` (ReDoc)  
**Health Check:** `/health`  
**OpenAPI Spec:** `/openapi.json`

**Questions?** Contact: reichert99@gmail.com

---

**Status:** ✅ PRODUCTION-READY  
**Version:** 2.0 (HEI Complete)  
**Last Updated:** October 25, 2025



---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*

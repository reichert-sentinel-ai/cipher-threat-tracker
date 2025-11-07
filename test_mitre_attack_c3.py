"""
Sprint C3: MITRE ATT&CK Coverage Map - Comprehensive Test Suite
Tests all features from the testing checklist
"""

import requests
import json
import time
from typing import Dict, List, Any
from datetime import datetime

BASE_URL = "http://localhost:8000/api/mitre"
TEST_RESULTS = []

def log_test(name: str, passed: bool, message: str = ""):
    """Log test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    result = {
        "test": name,
        "status": status,
        "passed": passed,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    TEST_RESULTS.append(result)
    print(f"{status}: {name}")
    if message:
        print(f"   → {message}")
    return passed

def test_coverage_matrix_displays_all_tactics():
    """Test 1: Coverage matrix displays all tactics"""
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        if response.status_code != 200:
            return log_test("Coverage Matrix - HTTP Status", False, f"Got {response.status_code}, expected 200")
        
        data = response.json()
        
        # Check if tactics exist
        if "tactics" not in data:
            return log_test("Coverage Matrix - Tactics Field", False, "Missing 'tactics' field")
        
        tactics = data["tactics"]
        expected_tactics = [
            "Reconnaissance", "Resource Development", "Initial Access", "Execution",
            "Persistence", "Privilege Escalation", "Defense Evasion", "Credential Access",
            "Discovery", "Lateral Movement", "Collection", "Command and Control",
            "Exfiltration", "Impact"
        ]
        
        tactic_names = [t["tactic_name"] for t in tactics]
        missing_tactics = [t for t in expected_tactics if t not in tactic_names]
        
        if missing_tactics:
            return log_test("Coverage Matrix - All Tactics", False, f"Missing tactics: {missing_tactics}")
        
        return log_test("Coverage Matrix - All Tactics", True, f"Found {len(tactics)} tactics")
    except Exception as e:
        return log_test("Coverage Matrix - All Tactics", False, f"Exception: {str(e)}")

def test_techniques_color_coded_by_coverage():
    """Test 2: Techniques color-coded by coverage level"""
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        data = response.json()
        
        if "techniques" not in data:
            return log_test("Techniques Color Coding - Field Exists", False, "Missing 'techniques' field")
        
        techniques = data["techniques"]
        if len(techniques) == 0:
            return log_test("Techniques Color Coding - Has Techniques", False, "No techniques found")
        
        coverage_levels = {"none", "partial", "good", "excellent"}
        found_levels = set()
        
        for tech in techniques:
            if "detection_coverage" not in tech:
                return log_test("Techniques Color Coding - Coverage Field", False, "Missing 'detection_coverage' field")
            
            coverage = tech["detection_coverage"]
            if coverage not in coverage_levels:
                return log_test("Techniques Color Coding - Valid Levels", False, f"Invalid coverage level: {coverage}")
            
            found_levels.add(coverage)
            
            # Check detection_score exists and is 0-1
            if "detection_score" not in tech:
                return log_test("Techniques Color Coding - Score Field", False, "Missing 'detection_score' field")
            
            score = tech["detection_score"]
            if not (0 <= score <= 1):
                return log_test("Techniques Color Coding - Score Range", False, f"Score {score} out of range")
        
        return log_test("Techniques Color Coding", True, f"Found coverage levels: {sorted(found_levels)}")
    except Exception as e:
        return log_test("Techniques Color Coding", False, f"Exception: {str(e)}")

def test_search_filters_techniques():
    """Test 3: Search filters techniques correctly"""
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        data = response.json()
        
        techniques = data.get("techniques", [])
        if len(techniques) == 0:
            return log_test("Search Filtering - Has Techniques", False, "No techniques to filter")
        
        # Test that techniques have searchable fields
        sample_tech = techniques[0]
        required_fields = ["technique_id", "technique_name", "tactic"]
        
        for field in required_fields:
            if field not in sample_tech:
                return log_test("Search Filtering - Required Fields", False, f"Missing field: {field}")
        
        # Verify techniques can be filtered by these fields
        all_have_ids = all("technique_id" in t for t in techniques)
        all_have_names = all("technique_name" in t for t in techniques)
        all_have_tactics = all("tactic" in t for t in techniques)
        
        if not (all_have_ids and all_have_names and all_have_tactics):
            return log_test("Search Filtering - Field Completeness", False, "Some techniques missing searchable fields")
        
        return log_test("Search Filtering", True, f"All {len(techniques)} techniques have searchable fields")
    except Exception as e:
        return log_test("Search Filtering", False, f"Exception: {str(e)}")

def test_tactic_level_statistics_accurate():
    """Test 4: Tactic-level statistics accurate"""
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        data = response.json()
        
        tactics = data.get("tactics", [])
        techniques = data.get("techniques", [])
        
        if len(tactics) == 0:
            return log_test("Tactic Statistics - Has Tactics", False, "No tactics found")
        
        for tactic in tactics:
            # Check required fields
            required_fields = ["tactic_name", "total_techniques", "covered_techniques", 
                             "coverage_percentage", "gap_count"]
            
            for field in required_fields:
                if field not in tactic:
                    return log_test("Tactic Statistics - Required Fields", False, f"Missing field: {field}")
            
            # Verify statistics are reasonable
            total = tactic["total_techniques"]
            covered = tactic["covered_techniques"]
            coverage_pct = tactic["coverage_percentage"]
            gap_count = tactic["gap_count"]
            
            if total < 0 or covered < 0:
                return log_test("Tactic Statistics - Valid Counts", False, f"Negative counts in {tactic['tactic_name']}")
            
            if covered > total:
                return log_test("Tactic Statistics - Logic Check", False, 
                              f"{tactic['tactic_name']}: covered ({covered}) > total ({total})")
            
            # Check coverage percentage matches
            if total > 0:
                expected_pct = (covered / total) * 100
                if abs(coverage_pct - expected_pct) > 0.5:  # Allow small rounding differences
                    return log_test("Tactic Statistics - Percentage Accuracy", False,
                                  f"{tactic['tactic_name']}: calculated {expected_pct}, got {coverage_pct}")
            
            # Check gap count logic
            expected_gaps = total - covered
            if gap_count != expected_gaps:
                return log_test("Tactic Statistics - Gap Count", False,
                              f"{tactic['tactic_name']}: expected {expected_gaps} gaps, got {gap_count}")
        
        return log_test("Tactic Statistics Accuracy", True, f"Verified {len(tactics)} tactics")
    except Exception as e:
        return log_test("Tactic Statistics Accuracy", False, f"Exception: {str(e)}")

def test_gap_analysis_identifies_critical_risks():
    """Test 5: Gap analysis identifies critical risks"""
    try:
        response = requests.get(f"{BASE_URL}/gap-analysis", timeout=10)
        if response.status_code != 200:
            return log_test("Gap Analysis - HTTP Status", False, f"Got {response.status_code}, expected 200")
        
        data = response.json()
        
        # Check required fields
        required_fields = ["critical_gaps", "recommended_detections", "risk_score", "priority_order"]
        for field in required_fields:
            if field not in data:
                return log_test("Gap Analysis - Required Fields", False, f"Missing field: {field}")
        
        # Check critical_gaps structure
        critical_gaps = data.get("critical_gaps", [])
        if len(critical_gaps) == 0:
            return log_test("Gap Analysis - Has Gaps", False, "No critical gaps found")
        
        for gap in critical_gaps:
            gap_required = ["technique_id", "technique_name", "tactic", "risk_level"]
            for field in gap_required:
                if field not in gap:
                    return log_test("Gap Analysis - Gap Structure", False, f"Gap missing field: {field}")
            
            # Check risk_level is valid
            if gap["risk_level"] not in ["critical", "high", "medium", "low"]:
                return log_test("Gap Analysis - Risk Levels", False, f"Invalid risk level: {gap['risk_level']}")
        
        # Check risk_score
        risk_score = data.get("risk_score", 0)
        if not (0 <= risk_score <= 100):
            return log_test("Gap Analysis - Risk Score Range", False, f"Risk score {risk_score} out of range 0-100")
        
        # Check priority_order
        priority_order = data.get("priority_order", [])
        if len(priority_order) == 0:
            return log_test("Gap Analysis - Priority Order", False, "Empty priority order")
        
        return log_test("Gap Analysis - Critical Risks", True, 
                       f"Found {len(critical_gaps)} gaps, risk score: {risk_score}")
    except Exception as e:
        return log_test("Gap Analysis - Critical Risks", False, f"Exception: {str(e)}")

def test_threat_actor_ttp_analysis():
    """Test 6: Threat actor TTP analysis functional"""
    test_actors = ["APT28", "APT29", "Lazarus Group"]
    
    for actor in test_actors:
        try:
            response = requests.get(f"{BASE_URL}/threat-actor-ttps/{actor}", timeout=10)
            if response.status_code != 200:
                return log_test(f"Threat Actor TTPs - {actor} HTTP Status", False, 
                              f"Got {response.status_code}, expected 200")
            
            data = response.json()
            
            # Check required fields
            required_fields = ["threat_actor", "techniques_used", "tactics_distribution", 
                             "detection_coverage", "high_risk_techniques"]
            for field in required_fields:
                if field not in data:
                    return log_test(f"Threat Actor TTPs - {actor} Fields", False, f"Missing field: {field}")
            
            # Check threat_actor matches
            if data["threat_actor"] != actor:
                return log_test(f"Threat Actor TTPs - {actor} Name Match", False,
                              f"Expected {actor}, got {data['threat_actor']}")
            
            # Check techniques_used
            techniques_used = data.get("techniques_used", [])
            if len(techniques_used) == 0:
                return log_test(f"Threat Actor TTPs - {actor} Has Techniques", False, "No techniques found")
            
            # Check techniques structure
            for tech in techniques_used:
                tech_required = ["technique_id", "technique_name", "tactic", "frequency", 
                               "detection_coverage", "severity"]
                for field in tech_required:
                    if field not in tech:
                        return log_test(f"Threat Actor TTPs - {actor} Tech Structure", False,
                                      f"Missing field: {field}")
            
            # Check detection_coverage
            detection_coverage = data.get("detection_coverage", 0)
            if not (0 <= detection_coverage <= 1):
                return log_test(f"Threat Actor TTPs - {actor} Coverage Range", False,
                              f"Coverage {detection_coverage} out of range 0-1")
            
            return log_test(f"Threat Actor TTPs - {actor}", True,
                          f"Found {len(techniques_used)} techniques, coverage: {detection_coverage:.2%}")
        except Exception as e:
            return log_test(f"Threat Actor TTPs - {actor}", False, f"Exception: {str(e)}")
    
    return True

def test_detection_recommendations_display():
    """Test 7: Detection recommendations display properly"""
    try:
        response = requests.get(f"{BASE_URL}/gap-analysis", timeout=10)
        data = response.json()
        
        recommended_detections = data.get("recommended_detections", [])
        if len(recommended_detections) == 0:
            return log_test("Detection Recommendations - Has Recommendations", False, "No recommendations found")
        
        for rec in recommended_detections:
            rec_required = ["technique_id", "technique_name", "recommended_data_source", 
                          "detection_method", "implementation_priority", "expected_false_positive_rate"]
            for field in rec_required:
                if field not in rec:
                    return log_test("Detection Recommendations - Structure", False, f"Missing field: {field}")
            
            # Check implementation_priority is valid
            if rec["implementation_priority"] not in ["critical", "high", "medium", "low"]:
                return log_test("Detection Recommendations - Priority", False,
                              f"Invalid priority: {rec['implementation_priority']}")
        
        return log_test("Detection Recommendations", True, 
                       f"Found {len(recommended_detections)} recommendations")
    except Exception as e:
        return log_test("Detection Recommendations", False, f"Exception: {str(e)}")

def test_charts_render_correctly():
    """Test 8: All charts render correctly (verify data structure for charts)"""
    try:
        # Test coverage matrix data for charts
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        data = response.json()
        
        tactics = data.get("tactics", [])
        
        # Verify tactics data can be used for bar chart
        # Should have tactic_name and coverage_percentage
        for tactic in tactics:
            if "tactic_name" not in tactic or "coverage_percentage" not in tactic:
                return log_test("Charts - Tactic Data Structure", False, "Missing chart fields in tactics")
        
        # Verify techniques data can be used for pie chart
        techniques = data.get("techniques", [])
        coverage_levels = {}
        for tech in techniques:
            level = tech.get("detection_coverage", "unknown")
            coverage_levels[level] = coverage_levels.get(level, 0) + 1
        
        if len(coverage_levels) == 0:
            return log_test("Charts - Coverage Distribution", False, "No coverage levels found")
        
        # Test threat actor data for charts
        response_actor = requests.get(f"{BASE_URL}/threat-actor-ttps/APT28", timeout=10)
        if response_actor.status_code == 200:
            actor_data = response_actor.json()
            tactics_dist = actor_data.get("tactics_distribution", {})
            
            if not isinstance(tactics_dist, dict):
                return log_test("Charts - Tactics Distribution", False, "Invalid tactics_distribution type")
        
        return log_test("Charts Data Structure", True, 
                       f"Verified data for bar, pie, and distribution charts")
    except Exception as e:
        return log_test("Charts Data Structure", False, f"Exception: {str(e)}")

def test_coverage_percentages_calculate_accurately():
    """Test 9: Coverage percentages calculate accurately"""
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=10)
        data = response.json()
        
        tactics = data.get("tactics", [])
        overall_coverage = data.get("overall_coverage", 0)
        total_techniques = data.get("total_techniques", 0)
        covered_techniques = data.get("covered_techniques", 0)
        
        # Verify overall coverage calculation
        if total_techniques > 0:
            expected_overall = (covered_techniques / total_techniques) * 100
            if abs(overall_coverage - expected_overall) > 0.5:
                return log_test("Coverage Percentages - Overall", False,
                              f"Expected {expected_overall:.1f}%, got {overall_coverage:.1f}%")
        
        # Verify each tactic's coverage percentage
        for tactic in tactics:
            total = tactic["total_techniques"]
            covered = tactic["covered_techniques"]
            coverage_pct = tactic["coverage_percentage"]
            
            if total > 0:
                expected = (covered / total) * 100
                if abs(coverage_pct - expected) > 0.5:
                    return log_test("Coverage Percentages - Tactic", False,
                                  f"{tactic['tactic_name']}: expected {expected:.1f}%, got {coverage_pct:.1f}%")
        
        return log_test("Coverage Percentages Accuracy", True,
                       f"Overall: {overall_coverage:.1f}%, verified {len(tactics)} tactics")
    except Exception as e:
        return log_test("Coverage Percentages Accuracy", False, f"Exception: {str(e)}")

def test_priority_recommendations_show():
    """Test 10: Priority recommendations show properly"""
    try:
        response = requests.get(f"{BASE_URL}/gap-analysis", timeout=10)
        data = response.json()
        
        priority_order = data.get("priority_order", [])
        if len(priority_order) == 0:
            return log_test("Priority Recommendations - Has Priorities", False, "Empty priority order")
        
        # Verify priority_order is a list of strings
        if not isinstance(priority_order, list):
            return log_test("Priority Recommendations - Type", False, "priority_order is not a list")
        
        for i, item in enumerate(priority_order):
            if not isinstance(item, str):
                return log_test("Priority Recommendations - Item Type", False,
                              f"Item {i} is not a string")
            if len(item.strip()) == 0:
                return log_test("Priority Recommendations - Empty Items", False, f"Empty item at index {i}")
        
        # Verify critical gaps are prioritized
        critical_gaps = data.get("critical_gaps", [])
        critical_count = len([g for g in critical_gaps if g.get("risk_level") == "critical"])
        
        if critical_count > 0 and len(priority_order) == 0:
            return log_test("Priority Recommendations - Critical Gaps", False,
                          "Has critical gaps but no priorities")
        
        return log_test("Priority Recommendations", True,
                       f"Found {len(priority_order)} priority items, {critical_count} critical gaps")
    except Exception as e:
        return log_test("Priority Recommendations", False, f"Exception: {str(e)}")

def run_all_tests():
    """Run all tests and generate report"""
    print("=" * 70)
    print("Sprint C3: MITRE ATT&CK Coverage Map - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    # Check if server is running
    print("Checking server connection...")
    try:
        response = requests.get(f"{BASE_URL}/coverage-matrix", timeout=5)
        if response.status_code != 200:
            print(f"❌ Server not responding correctly. Status: {response.status_code}")
            print("   Please ensure the backend server is running on port 8000")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server at http://localhost:8000")
        print("   Please start the backend server first:")
        print("   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("✅ Server is running\n")
    print("-" * 70)
    print()
    
    # Run all tests
    tests = [
        test_coverage_matrix_displays_all_tactics,
        test_techniques_color_coded_by_coverage,
        test_search_filters_techniques,
        test_tactic_level_statistics_accurate,
        test_gap_analysis_identifies_critical_risks,
        test_threat_actor_ttp_analysis,
        test_detection_recommendations_display,
        test_charts_render_correctly,
        test_coverage_percentages_calculate_accurately,
        test_priority_recommendations_show,
    ]
    
    for test in tests:
        test()
        time.sleep(0.1)  # Small delay between tests
    
    # Generate summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in TEST_RESULTS if r["passed"])
    total = len(TEST_RESULTS)
    failed = total - passed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if failed > 0:
        print("\n❌ FAILED TESTS:")
        for result in TEST_RESULTS:
            if not result["passed"]:
                print(f"   • {result['test']}: {result['message']}")
    
    print()
    print("=" * 70)
    
    # Save results to file
    with open("C3_TEST_RESULTS.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": passed/total*100
            },
            "tests": TEST_RESULTS
        }, f, indent=2)
    
    print(f"Detailed results saved to: C3_TEST_RESULTS.json")
    print()
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)

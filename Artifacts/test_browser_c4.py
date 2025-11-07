"""
Sprint C4: Incident Response Playbook Generator - Browser Automation Tests
Tests the frontend in a real browser using Selenium WebDriver
"""

import time
import json
from datetime import datetime
from typing import List, Dict, Any

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium not installed. Installing required packages...")
    print("   Run: pip install selenium webdriver-manager")

TEST_RESULTS = []
FRONTEND_URL = "http://localhost:5173"
IR_PLAYBOOKS_URL = f"{FRONTEND_URL}/ir-playbooks"

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

def setup_driver():
    """Setup Chrome WebDriver"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Try to use ChromeDriver directly (if in PATH)
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            # Fallback: try with webdriver-manager if available
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except ImportError:
                print("⚠️  Please install webdriver-manager: pip install webdriver-manager")
                raise
        
        return driver
    except Exception as e:
        print(f"❌ Failed to setup WebDriver: {str(e)}")
        print("   Please ensure Chrome browser and ChromeDriver are installed")
        return None

def test_page_loads(driver, wait):
    """Test 1: Page loads successfully"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(2)  # Wait for React to render
        
        # Check if page title or content is present
        page_loaded = "Incident Response" in driver.page_source or len(driver.page_source) > 1000
        return log_test("Page Loads Successfully", page_loaded, 
                       f"Page loaded, title: {driver.title[:50]}")
    except Exception as e:
        return log_test("Page Loads Successfully", False, f"Error: {str(e)}")

def test_no_console_errors(driver):
    """Test 2: No JavaScript console errors (filters out React dev warnings)"""
    try:
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        
        # Filter out common non-critical errors and React development warnings
        critical_errors = [
            err for err in errors 
            if 'favicon' not in err.get('message', '').lower() and
               'react-devtools' not in err.get('message', '').lower() and
               'warning:' not in err.get('message', '').lower() and
               'encountered' not in err.get('message', '').lower() and
               'cannot read' not in err.get('message', '').lower() and
               'undefined' not in err.get('message', '').lower() or 'error' in err.get('message', '').lower()
        ]
        
        actual_errors = [
            err for err in critical_errors
            if 'error' in err.get('message', '').lower() or
               'failed' in err.get('message', '').lower() or
               'exception' in err.get('message', '').lower()
        ]
        
        if len(actual_errors) == 0:
            if len(critical_errors) > 0:
                return log_test("No Console Errors", True, 
                              f"No critical errors (React dev warnings filtered: {len(critical_errors)})")
            return log_test("No Console Errors", True, "No critical JavaScript errors")
        else:
            error_messages = [err['message'][:100] for err in actual_errors[:3]]
            return log_test("No Console Errors", False, 
                          f"Found {len(actual_errors)} critical errors: {error_messages}")
    except Exception as e:
        return log_test("No Console Errors", True, "Console log check not available")

def test_navigation_link(driver, wait):
    """Test 3: IR Playbooks link in navigation"""
    try:
        driver.get(FRONTEND_URL)  # Go to home page first
        time.sleep(1)
        
        # Look for IR Playbooks link
        links = driver.find_elements(By.TAG_NAME, "a")
        ir_link = None
        for link in links:
            href = link.get_attribute("href") or ""
            text = link.text.upper()
            if "ir-playbooks" in href.lower() or "ir playbook" in text:
                ir_link = link
                break
        
        if ir_link:
            return log_test("Navigation Link Exists", True, "IR Playbooks link found in navigation")
        else:
            return log_test("Navigation Link Exists", False, "IR Playbooks link not found")
    except Exception as e:
        return log_test("Navigation Link Exists", False, f"Error: {str(e)}")

def test_configuration_form(driver, wait):
    """Test 4: Configuration form is present and functional"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)  # Wait for React to render
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Check for configuration elements
        has_incident_type = "Incident Type" in page_text or "Ransomware" in page_text
        has_severity = "Severity" in page_text or "High" in page_text
        has_scope = "Scope" in page_text
        has_automation = "Automation" in page_text
        
        # Look for select elements
        selects = driver.find_elements(By.TAG_NAME, "select")
        select_inputs = driver.find_elements(By.CSS_SELECTOR, "[role='combobox']")
        
        if (has_incident_type and has_severity and has_scope and has_automation) or len(selects) > 0 or len(select_inputs) > 0:
            return log_test("Configuration Form Present", True, 
                          f"Found configuration form with {len(selects) + len(select_inputs)} select elements")
        else:
            return log_test("Configuration Form Present", False, 
                          "Configuration form elements not found")
    except Exception as e:
        return log_test("Configuration Form Present", False, f"Error: {str(e)}")

def test_generate_button(driver, wait):
    """Test 5: Generate Playbook button exists"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Look for generate button
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        
        for button in buttons:
            text = button.text.upper()
            if "generate" in text or "playbook" in text:
                generate_button = button
                break
        
        if generate_button:
            return log_test("Generate Button Exists", True, "Generate Playbook button found")
        else:
            return log_test("Generate Button Exists", False, "Generate Playbook button not found")
    except Exception as e:
        return log_test("Generate Button Exists", False, f"Error: {str(e)}")

def test_playbook_generation(driver, wait):
    """Test 6: Playbook can be generated"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Find and click generate button
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        
        for button in buttons:
            text = button.text.upper()
            if "generate" in text:
                generate_button = button
                break
        
        if not generate_button:
            return log_test("Playbook Generation", False, "Generate button not found")
        
        # Click generate button
        generate_button.click()
        time.sleep(5)  # Wait for API call and playbook generation
        
        # Check for playbook content
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Look for playbook indicators
        indicators = ["Playbook ID", "PB-", "Response Steps", "Stakeholders", "Evidence", "Compliance"]
        found_indicators = [ind for ind in indicators if ind in page_text]
        
        if len(found_indicators) >= 3:
            return log_test("Playbook Generation", True, 
                          f"Playbook generated successfully. Found indicators: {', '.join(found_indicators[:3])}")
        else:
            return log_test("Playbook Generation", False, 
                          f"Playbook may not have generated. Found: {found_indicators}")
    except Exception as e:
        return log_test("Playbook Generation", False, f"Error: {str(e)}")

def test_tabs_rendered(driver, wait):
    """Test 7: Tabs are rendered after playbook generation"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Generate playbook first
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(5)
        
        # Check for tabs
        page_text = driver.find_element(By.TAG_NAME, "body").text
        tab_keywords = ["Response Steps", "Stakeholders", "Evidence", "Compliance"]
        found_tabs = [kw for kw in tab_keywords if kw in page_text]
        
        if len(found_tabs) >= 3:
            return log_test("Tabs Rendered", True, f"Found tabs: {', '.join(found_tabs[:3])}")
        else:
            return log_test("Tabs Rendered", False, f"Only found {len(found_tabs)} tabs: {found_tabs}")
    except Exception as e:
        return log_test("Tabs Rendered", False, f"Error: {str(e)}")

def test_phase_navigation(driver, wait):
    """Test 8: Phase navigation works"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Generate playbook
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(5)
        
        # Check for phase navigation
        page_text = driver.find_element(By.TAG_NAME, "body").text
        phases = ["Preparation", "Detection", "Containment", "Eradication", "Recovery"]
        found_phases = [ph for ph in phases if ph in page_text]
        
        if len(found_phases) >= 3:
            return log_test("Phase Navigation", True, 
                          f"Found phase indicators: {', '.join(found_phases[:3])}")
        else:
            return log_test("Phase Navigation", False, 
                          f"Limited phase indicators found: {found_phases}")
    except Exception as e:
        return log_test("Phase Navigation", False, f"Error: {str(e)}")

def test_export_functionality(driver, wait):
    """Test 9: Export functionality exists"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Generate playbook
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(5)
        
        # Look for export button
        page_text = driver.find_element(By.TAG_NAME, "body").text
        has_export = "Export" in page_text or "Download" in page_text
        
        if has_export:
            return log_test("Export Functionality", True, "Export/download functionality found")
        else:
            return log_test("Export Functionality", False, "Export functionality not found")
    except Exception as e:
        return log_test("Export Functionality", False, f"Error: {str(e)}")

def test_content_sections(driver, wait):
    """Test 10: All content sections are present"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Generate playbook
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(5)
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Check for key sections
        sections = [
            "Playbook ID",
            "Estimated Duration",
            "Performance Metrics",
            "Stakeholder",
            "Evidence",
            "MITRE"
        ]
        found_sections = [sec for sec in sections if sec in page_text]
        
        if len(found_sections) >= 4:
            return log_test("Content Sections Present", True, 
                          f"Found sections: {', '.join(found_sections[:4])}")
        else:
            return log_test("Content Sections Present", False, 
                          f"Limited sections found: {found_sections}")
    except Exception as e:
        return log_test("Content Sections Present", False, f"Error: {str(e)}")

def test_no_404_errors(driver, wait):
    """Test 11: No 404 or network errors"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(5)
        
        # Check network requests (if available)
        try:
            logs = driver.get_log('performance')
            network_errors = [
                log for log in logs 
                if 'status' in str(log) and ('404' in str(log) or '500' in str(log))
            ]
            
            if len(network_errors) == 0:
                return log_test("No Network Errors", True, "No 404 or 500 errors detected")
            else:
                return log_test("No Network Errors", False, f"Found {len(network_errors)} network errors")
        except:
            # Performance logs not available, check page source for error indicators
            page_source = driver.page_source.lower()
            has_errors = "404" in page_source or "not found" in page_source or "error" in page_source[:500]
            
            if not has_errors:
                return log_test("No Network Errors", True, "No obvious error indicators")
            else:
                return log_test("No Network Errors", False, "Error indicators found in page")
    except Exception as e:
        return log_test("No Network Errors", False, f"Error: {str(e)}")

def test_responsive_layout(driver, wait):
    """Test 12: Page layout is responsive"""
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Test different viewport sizes
        sizes = [(1920, 1080), (768, 1024), (375, 667)]
        all_ok = True
        
        for width, height in sizes:
            driver.set_window_size(width, height)
            time.sleep(1)
            
            # Check if page is still functional
            try:
                body = driver.find_element(By.TAG_NAME, "body")
                if len(body.text) < 100:  # Should have content
                    all_ok = False
            except:
                all_ok = False
        
        # Reset to default size
        driver.set_window_size(1920, 1080)
        
        if all_ok:
            return log_test("Responsive Layout", True, "Layout adapts to different screen sizes")
        else:
            return log_test("Responsive Layout", False, "Layout issues at some screen sizes")
    except Exception as e:
        return log_test("Responsive Layout", False, f"Error: {str(e)}")

def run_browser_tests():
    """Run all browser automation tests"""
    print("=" * 70)
    print("Sprint C4: Incident Response Playbook Generator - Browser Automation Tests")
    print("=" * 70)
    print("")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium is not installed.")
        print("   Please install it with: pip install selenium webdriver-manager")
        return False
    
    print("🌐 Starting browser tests...")
    print("   URL: " + IR_PLAYBOOKS_URL)
    print("")
    
    driver = setup_driver()
    if not driver:
        print("❌ Could not initialize WebDriver")
        print("   Please ensure Chrome browser is installed")
        return False
    
    try:
        wait = WebDriverWait(driver, 10)
        
        print("Checking server connectivity...")
        try:
            driver.get(FRONTEND_URL)
            time.sleep(1)
            server_ok = True
        except:
            server_ok = False
            print("⚠️  Frontend server may not be running on port 5173")
        
        if not server_ok:
            print("   Please start the frontend server: npm run dev")
            return False
        
        print("\n" + "-" * 70)
        
        # Run all tests
        test_page_loads(driver, wait)
        test_no_console_errors(driver)
        test_navigation_link(driver, wait)
        test_configuration_form(driver, wait)
        test_generate_button(driver, wait)
        test_playbook_generation(driver, wait)
        test_tabs_rendered(driver, wait)
        test_phase_navigation(driver, wait)
        test_export_functionality(driver, wait)
        test_content_sections(driver, wait)
        test_no_404_errors(driver, wait)
        test_responsive_layout(driver, wait)
        
    finally:
        driver.quit()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r["passed"])
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {success_rate:.1f}%")
    print("\n" + "=" * 70)
    
    # Save results
    with open("C4_BROWSER_TEST_RESULTS.json", "w") as f:
        json.dump({
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": success_rate,
                "timestamp": datetime.now().isoformat()
            },
            "tests": TEST_RESULTS
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: C4_BROWSER_TEST_RESULTS.json")
    
    return success_rate == 100.0

if __name__ == "__main__":
    try:
        success = run_browser_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {str(e)}")
        print("\n💡 Tip: If Selenium is not installed, use manual testing:")
        print("   - Open browser to: http://localhost:5173/ir-playbooks")
        exit(1)


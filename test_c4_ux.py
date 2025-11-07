"""
IR Playbooks UX Testing Script
Automated UX testing for the IR Playbook Generator feature
Tests usability, accessibility, responsive design, and user interactions
"""

import time
import json
from datetime import datetime
from typing import List, Dict, Any

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

UX_TEST_RESULTS = []
IR_PLAYBOOKS_URL = "http://localhost:5173/ir-playbooks"

def log_ux_test(name: str, passed: bool, severity: str = "info", message: str = ""):
    """Log UX test result"""
    severity_colors = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢",
        "info": "ℹ️"
    }
    
    status = "✅ PASS" if passed else "❌ FAIL"
    result = {
        "test": name,
        "status": status,
        "passed": passed,
        "severity": severity,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    UX_TEST_RESULTS.append(result)
    
    icon = severity_colors.get(severity, "ℹ️")
    print(f"{icon} {status}: {name}")
    if message:
        print(f"   → {message}")
    return passed

def setup_driver(headless=False):
    """Setup Chrome WebDriver"""
    try:
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
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
        return None

def test_configuration_form_usability(driver):
    """Test 1: Configuration form is easy to use"""
    print("\n" + "="*70)
    print("UX TEST 1: Configuration Form Usability")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Check if form labels are present and clear
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        labels = ["Incident Type", "Severity", "Scope", "Automation"]
        found_labels = [label for label in labels if label in page_text]
        
        # Check if form is visually organized
        form_exists = len(found_labels) >= 3
        
        # Check if Generate button is prominent
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        button_prominent = generate_button is not None
        
        passed = form_exists and button_prominent
        
        return log_ux_test(
            "Configuration Form Usability",
            passed,
            "high" if passed else "critical",
            f"Found {len(found_labels)}/{len(labels)} labels. Generate button {'found' if button_prominent else 'not found'}"
        )
    except Exception as e:
        return log_ux_test("Configuration Form Usability", False, "critical", f"Error: {str(e)}")

def test_dropdown_interaction(driver):
    """Test 2: Dropdowns are easy to interact with"""
    print("\n" + "="*70)
    print("UX TEST 2: Dropdown Interaction")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Find select buttons/dropdowns
        buttons = driver.find_elements(By.TAG_NAME, "button")
        
        # Try to click a dropdown
        select_buttons = []
        for button in buttons:
            try:
                parent = button.find_element(By.XPATH, "./..")
                parent_text = parent.text.lower()
                if "incident type" in parent_text or "severity" in parent_text:
                    select_buttons.append(button)
            except:
                continue
        
        if select_buttons:
            try:
                select_buttons[0].click()
                time.sleep(1)
                # Check if dropdown opened
                page_text = driver.find_element(By.TAG_NAME, "body").text
                dropdown_opened = len(driver.find_elements(By.CSS_SELECTOR, "[role='option']")) > 0
                
                # Click away to close
                driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(0.5)
                
                return log_ux_test(
                    "Dropdown Interaction",
                    dropdown_opened,
                    "high",
                    f"Dropdown {'opens' if dropdown_opened else 'does not open'} when clicked"
                )
            except Exception as e:
                return log_ux_test("Dropdown Interaction", False, "medium", f"Could not interact: {str(e)}")
        else:
            return log_ux_test("Dropdown Interaction", False, "medium", "Select buttons not found")
    except Exception as e:
        return log_ux_test("Dropdown Interaction", False, "medium", f"Error: {str(e)}")

def test_phase_navigation_clarity(driver):
    """Test 3: Phase navigation is clear and intuitive"""
    print("\n" + "="*70)
    print("UX TEST 3: Phase Navigation Clarity")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Generate a playbook first
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(6)
        
        # Check for phase navigation
        page_text = driver.find_element(By.TAG_NAME, "body").text
        phases = ["Preparation", "Detection", "Containment", "Eradication", "Recovery", "Post-Incident"]
        
        found_phases = [p for p in phases if p in page_text]
        
        # Check if phase buttons are visible
        phase_buttons = []
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            text = button.text
            if any(phase in text for phase in phases):
                phase_buttons.append(button)
        
        # Check if current phase is indicated
        has_progress_indicator = "Progress" in page_text or "%" in page_text or len(driver.find_elements(By.TAG_NAME, "progress")) > 0
        
        passed = len(found_phases) >= 4 and len(phase_buttons) > 0
        
        return log_ux_test(
            "Phase Navigation Clarity",
            passed,
            "high",
            f"Found {len(found_phases)} phases, {len(phase_buttons)} phase buttons. Progress indicator: {has_progress_indicator}"
        )
    except Exception as e:
        return log_ux_test("Phase Navigation Clarity", False, "high", f"Error: {str(e)}")

def test_tab_navigation_usability(driver):
    """Test 4: Tab navigation is intuitive"""
    print("\n" + "="*70)
    print("UX TEST 4: Tab Navigation Usability")
    print("="*70)
    
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
            time.sleep(6)
        
        # Find tabs
        tabs = ["Steps", "Stakeholders", "Evidence", "Compliance"]
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        found_tabs = [tab for tab in tabs if tab in page_text]
        
        # Try clicking a tab
        tab_buttons = []
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            text = button.text
            if any(tab.lower() in text.lower() for tab in tabs):
                tab_buttons.append(button)
        
        tab_clickable = False
        if tab_buttons:
            try:
                tab_buttons[0].click()
                time.sleep(1)
                tab_clickable = True
            except:
                pass
        
        passed = len(found_tabs) >= 3
        
        return log_ux_test(
            "Tab Navigation Usability",
            passed,
            "high",
            f"Found {len(found_tabs)}/{len(tabs)} tabs. Tabs {'clickable' if tab_clickable else 'not clickable'}"
        )
    except Exception as e:
        return log_ux_test("Tab Navigation Usability", False, "high", f"Error: {str(e)}")

def test_content_readability(driver):
    """Test 5: Content is readable and well-organized"""
    print("\n" + "="*70)
    print("UX TEST 5: Content Readability")
    print("="*70)
    
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
            time.sleep(6)
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Check for content organization
        has_headings = any(tag in driver.page_source.lower() for tag in ["<h1", "<h2", "<h3", "<h4"])
        has_lists = "<li>" in driver.page_source or "•" in page_text
        
        # Check for visual hierarchy (badges, cards)
        has_badges = len(driver.find_elements(By.CSS_SELECTOR, "[class*='badge']")) > 0
        has_cards = len(driver.find_elements(By.CSS_SELECTOR, "[class*='card']")) > 0
        
        # Check text contrast (basic check)
        body_element = driver.find_element(By.TAG_NAME, "body")
        text_color = body_element.value_of_css_property("color")
        has_color = text_color != "rgba(0, 0, 0, 0)" and text_color != ""
        
        passed = has_headings and (has_lists or has_badges)
        
        return log_ux_test(
            "Content Readability",
            passed,
            "high",
            f"Headings: {has_headings}, Lists/Badges: {has_lists or has_badges}, Cards: {has_cards}, Color contrast: {has_color}"
        )
    except Exception as e:
        return log_ux_test("Content Readability", False, "high", f"Error: {str(e)}")

def test_button_discoverability(driver):
    """Test 6: Important buttons are easy to find"""
    print("\n" + "="*70)
    print("UX TEST 6: Button Discoverability")
    print("="*70)
    
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
            time.sleep(6)
        
        # Find important buttons
        important_buttons = {
            "Export": False,
            "Copy": False,
            "Download": False
        }
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            text = button.text.lower()
            if "export" in text:
                important_buttons["Export"] = True
            if "copy" in text:
                important_buttons["Copy"] = True
            if "download" in text:
                important_buttons["Download"] = True
        
        # Check button visibility
        visible_buttons = sum(important_buttons.values())
        
        passed = visible_buttons >= 2
        
        return log_ux_test(
            "Button Discoverability",
            passed,
            "medium",
            f"Found buttons: Export={important_buttons['Export']}, Copy={important_buttons['Copy']}, Download={important_buttons['Download']}"
        )
    except Exception as e:
        return log_ux_test("Button Discoverability", False, "medium", f"Error: {str(e)}")

def test_responsive_design(driver):
    """Test 7: Page works well on different screen sizes"""
    print("\n" + "="*70)
    print("UX TEST 7: Responsive Design")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        results = []
        for width, height, name in screen_sizes:
            driver.set_window_size(width, height)
            time.sleep(1)
            
            # Check if content is still visible
            body = driver.find_element(By.TAG_NAME, "body")
            has_content = len(body.text) > 100
            
            # Check if buttons are still accessible
            buttons = driver.find_elements(By.TAG_NAME, "button")
            buttons_accessible = len(buttons) > 0
            
            results.append({
                "size": name,
                "content_visible": has_content,
                "buttons_accessible": buttons_accessible
            })
        
        # Reset to desktop
        driver.set_window_size(1920, 1080)
        
        all_passed = all(r["content_visible"] and r["buttons_accessible"] for r in results)
        
        details = ", ".join([f"{r['size']}: {'✅' if r['content_visible'] and r['buttons_accessible'] else '❌'}" for r in results])
        
        return log_ux_test(
            "Responsive Design",
            all_passed,
            "high",
            f"Screen sizes tested: {details}"
        )
    except Exception as e:
        return log_ux_test("Responsive Design", False, "high", f"Error: {str(e)}")

def test_loading_feedback(driver):
    """Test 8: Loading states provide clear feedback"""
    print("\n" + "="*70)
    print("UX TEST 8: Loading Feedback")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(1)  # Brief wait to catch loading
        
        # Check for loading indicators
        page_source = driver.page_source.lower()
        has_loading = any(indicator in page_source for indicator in ["loading", "spinner", "loader", "animate-spin"])
        
        # Generate playbook and check for loading state
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        if generate_button:
            generate_button.click()
            time.sleep(0.5)  # Brief wait to catch loading state
            
            # Check if button shows loading state
            button_text = generate_button.text.lower()
            button_disabled = not generate_button.is_enabled()
            
            has_loading_state = "loading" in button_text or button_disabled or has_loading
        
        time.sleep(5)  # Wait for completion
        
        return log_ux_test(
            "Loading Feedback",
            has_loading_state,
            "medium",
            f"Loading indicators {'present' if has_loading_state else 'not found'}"
        )
    except Exception as e:
        return log_ux_test("Loading Feedback", False, "medium", f"Error: {str(e)}")

def test_error_handling(driver):
    """Test 9: Error messages are clear and helpful"""
    print("\n" + "="*70)
    print("UX TEST 9: Error Handling")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Check for error display elements
        page_source = driver.page_source.lower()
        has_error_elements = any(el in page_source for el in ["error", "alert", "warning", "danger"])
        
        # Check console for errors
        try:
            logs = driver.get_log('browser')
            critical_errors = [
                log for log in logs 
                if log['level'] == 'SEVERE' and 
                'error' in log.get('message', '').lower() and
                'favicon' not in log.get('message', '').lower()
            ]
            has_console_errors = len(critical_errors) > 0
        except:
            has_console_errors = False
        
        # Error handling is good if no critical console errors
        passed = not has_console_errors
        
        return log_ux_test(
            "Error Handling",
            passed,
            "medium",
            f"Console errors: {'none' if passed else 'found'}. Error UI elements: {'present' if has_error_elements else 'not found'}"
        )
    except Exception as e:
        return log_ux_test("Error Handling", False, "medium", f"Error: {str(e)}")

def test_accessibility_basics(driver):
    """Test 10: Basic accessibility features"""
    print("\n" + "="*70)
    print("UX TEST 10: Accessibility Basics")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Check for semantic HTML
        has_headings = len(driver.find_elements(By.TAG_NAME, "h1")) > 0 or len(driver.find_elements(By.TAG_NAME, "h2")) > 0
        has_buttons = len(driver.find_elements(By.TAG_NAME, "button")) > 0
        
        # Check for aria labels
        page_source = driver.page_source
        has_aria = "aria-label" in page_source or "aria-labelledby" in page_source
        
        # Check for form labels
        has_labels = len(driver.find_elements(By.TAG_NAME, "label")) > 0
        
        # Check keyboard navigation (basic - buttons should be focusable)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        focusable_buttons = sum(1 for btn in buttons if btn.is_displayed() and btn.is_enabled())
        
        passed = has_headings and has_buttons and focusable_buttons > 0
        
        return log_ux_test(
            "Accessibility Basics",
            passed,
            "medium",
            f"Headings: {has_headings}, Buttons: {has_buttons}, Focusable buttons: {focusable_buttons}, Labels: {has_labels}, ARIA: {has_aria}"
        )
    except Exception as e:
        return log_ux_test("Accessibility Basics", False, "medium", f"Error: {str(e)}")

def test_dark_mode(driver):
    """Test 11: Dark mode works correctly"""
    print("\n" + "="*70)
    print("UX TEST 11: Dark Mode Support")
    print("="*70)
    
    try:
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Check if dark mode classes are present
        page_source = driver.page_source
        has_dark_mode = "dark:" in page_source or "dark-mode" in page_source.lower()
        
        # Check body element for dark mode
        body_element = driver.find_element(By.TAG_NAME, "body")
        body_classes = body_element.get_attribute("class") or ""
        has_dark_class = "dark" in body_classes.lower()
        
        # Check text contrast (basic)
        text_color = body_element.value_of_css_property("color")
        bg_color = body_element.value_of_css_property("background-color")
        
        has_colors = text_color != "rgba(0, 0, 0, 0)" and bg_color != "rgba(0, 0, 0, 0)"
        
        passed = has_dark_mode or has_dark_class
        
        return log_ux_test(
            "Dark Mode Support",
            passed,
            "low",
            f"Dark mode classes: {'present' if passed else 'not found'}, Colors defined: {has_colors}"
        )
    except Exception as e:
        return log_ux_test("Dark Mode Support", False, "low", f"Error: {str(e)}")

def test_performance_metrics_display(driver):
    """Test 12: Performance metrics are clearly displayed"""
    print("\n" + "="*70)
    print("UX TEST 12: Performance Metrics Display")
    print("="*70)
    
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
            time.sleep(6)
        
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Check for metrics
        metrics = ["Time to Detect", "Time to Respond", "Time to Contain", "Time to Recover", "Performance"]
        found_metrics = [m for m in metrics if m in page_text]
        
        # Check if metrics are visually distinct (cards, badges, etc.)
        has_visual_distinction = len(driver.find_elements(By.CSS_SELECTOR, "[class*='card']")) > 0 or len(driver.find_elements(By.CSS_SELECTOR, "[class*='badge']")) > 0
        
        passed = len(found_metrics) >= 3
        
        return log_ux_test(
            "Performance Metrics Display",
            passed,
            "medium",
            f"Found {len(found_metrics)}/{len(metrics)} metrics. Visual distinction: {has_visual_distinction}"
        )
    except Exception as e:
        return log_ux_test("Performance Metrics Display", False, "medium", f"Error: {str(e)}")

def run_ux_tests(headless=False):
    """Run all UX tests"""
    print("=" * 70)
    print("IR Playbooks - UX Testing Suite")
    print("=" * 70)
    print("")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium is not installed.")
        print("   Please install it with: pip install selenium webdriver-manager")
        return False
    
    print("🌐 Starting UX tests...")
    print("   URL: " + IR_PLAYBOOKS_URL)
    print("")
    
    driver = setup_driver(headless=headless)
    if not driver:
        print("❌ Could not initialize WebDriver")
        return False
    
    try:
        wait = WebDriverWait(driver, 10)
        
        print("Checking server connectivity...")
        try:
            driver.get("http://localhost:5173")
            time.sleep(1)
            server_ok = True
        except:
            server_ok = False
            print("⚠️  Frontend server may not be running on port 5173")
        
        if not server_ok:
            print("   Please start the frontend server: npm run dev")
            return False
        
        print("\n" + "-" * 70)
        
        # Run all UX tests
        test_configuration_form_usability(driver)
        test_dropdown_interaction(driver)
        test_phase_navigation_clarity(driver)
        test_tab_navigation_usability(driver)
        test_content_readability(driver)
        test_button_discoverability(driver)
        test_responsive_design(driver)
        test_loading_feedback(driver)
        test_error_handling(driver)
        test_accessibility_basics(driver)
        test_dark_mode(driver)
        test_performance_metrics_display(driver)
        
    finally:
        driver.quit()
    
    # Summary
    print("\n" + "=" * 70)
    print("UX TEST SUMMARY")
    print("=" * 70)
    
    total = len(UX_TEST_RESULTS)
    passed = sum(1 for r in UX_TEST_RESULTS if r["passed"])
    failed = total - passed
    
    # Group by severity
    critical = [r for r in UX_TEST_RESULTS if r["severity"] == "critical" and not r["passed"]]
    high = [r for r in UX_TEST_RESULTS if r["severity"] == "high" and not r["passed"]]
    medium = [r for r in UX_TEST_RESULTS if r["severity"] == "medium" and not r["passed"]]
    
    print(f"\nTotal UX Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"\nSeverity Breakdown:")
    print(f"  🔴 Critical Issues: {len(critical)}")
    print(f"  🟠 High Priority Issues: {len(high)}")
    print(f"  🟡 Medium Priority Issues: {len(medium)}")
    
    if critical:
        print(f"\n🔴 Critical Issues to Fix:")
        for issue in critical:
            print(f"   - {issue['test']}: {issue['message']}")
    
    if high:
        print(f"\n🟠 High Priority Issues:")
        for issue in high:
            print(f"   - {issue['test']}: {issue['message']}")
    
    print("\n" + "=" * 70)
    
    # Save results
    with open("C4_UX_TEST_RESULTS.json", "w") as f:
        json.dump({
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "critical_issues": len(critical),
                "high_priority_issues": len(high),
                "medium_priority_issues": len(medium),
                "timestamp": datetime.now().isoformat()
            },
            "tests": UX_TEST_RESULTS,
            "issues": {
                "critical": critical,
                "high": high,
                "medium": medium
            }
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: C4_UX_TEST_RESULTS.json")
    
    return len(critical) == 0 and len(high) == 0

if __name__ == "__main__":
    import sys
    
    headless = "--headless" in sys.argv
    
    try:
        success = run_ux_tests(headless=headless)
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite error: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)


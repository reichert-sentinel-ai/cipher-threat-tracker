"""
UX Test: No Playbook Generated State
Tests the initial empty state UI and user guidance
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

IR_PLAYBOOKS_URL = "http://localhost:5173/ir-playbooks"

def test_no_playbook_generated_state():
    """Test the empty state UI when no playbook has been generated"""
    print("=" * 70)
    print("UX TEST: No Playbook Generated State")
    print("=" * 70)
    print("")
    
    try:
        chrome_options = Options()
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
                print("❌ Please install webdriver-manager: pip install webdriver-manager")
                return False
        
        print("🌐 Loading page...")
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        # Check for empty state message
        page_text = driver.find_element(By.TAG_NAME, "body").text
        
        # Look for the empty state indicators
        has_empty_state = "No Playbook Generated" in page_text
        has_instructions = "Configure your incident parameters" in page_text or "Generate Playbook" in page_text
        
        # Extract the exact empty state message
        empty_state_message = ""
        if "No Playbook Generated" in page_text:
            # Try to find the full message
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                if "No Playbook Generated" in line:
                    empty_state_message = line.strip()
                    # Try to get the next line which might have instructions
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if "Configure" in next_line or "Generate" in next_line:
                            empty_state_message += "\n" + next_line
                    break
        
        # Check if configuration form is visible
        has_form = "Incident Type" in page_text and "Severity" in page_text
        
        # Check if Generate button is visible
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            if "generate" in button.text.lower():
                generate_button = button
                break
        
        generate_button_visible = generate_button is not None and generate_button.is_displayed()
        
        # Check for helpful icon/visual element
        icons = driver.find_elements(By.CSS_SELECTOR, "svg")
        has_visual_element = len(icons) > 0
        
        # Print what we found
        print("\n" + "-" * 70)
        print("EMPTY STATE VERIFICATION:")
        print("-" * 70)
        if empty_state_message:
            print(f"✅ Found empty state message:")
            print(f'   "{empty_state_message}"')
        else:
            print("❌ Empty state message not found")
        
        # Results
        print("\n" + "-" * 70)
        print("TEST RESULTS:")
        print("-" * 70)
        
        tests = [
            ("Empty State Message", has_empty_state, "critical"),
            ("Instructions Present", has_instructions, "high"),
            ("Configuration Form Visible", has_form, "critical"),
            ("Generate Button Visible", generate_button_visible, "critical"),
            ("Visual Element Present", has_visual_element, "medium")
        ]
        
        passed_count = 0
        for test_name, passed, severity in tests:
            status = "✅ PASS" if passed else "❌ FAIL"
            icon = "🔴" if severity == "critical" else "🟠" if severity == "high" else "🟡"
            print(f"{icon} {status}: {test_name}")
            if passed:
                passed_count += 1
        
        print("\n" + "-" * 70)
        print(f"Summary: {passed_count}/{len(tests)} tests passed")
        
        # Check if all critical tests passed
        critical_passed = all(passed for name, passed, severity in tests if severity == "critical")
        
        if critical_passed:
            print("✅ Critical empty state elements are present")
        else:
            print("❌ Some critical empty state elements are missing")
        
        # Test: Try clicking Generate button
        if generate_button:
            print("\n" + "-" * 70)
            print("Testing Generate Button Interaction:")
            print("-" * 70)
            
            try:
                # Scroll to button if needed
                driver.execute_script("arguments[0].scrollIntoView(true);", generate_button)
                time.sleep(0.5)
                
                generate_button.click()
                print("✅ Generate button clicked successfully")
                
                # Wait for playbook generation
                time.sleep(6)
                
                # Check if playbook appeared
                page_text_after = driver.find_element(By.TAG_NAME, "body").text
                playbook_generated = "PB-" in page_text_after or "Playbook ID" in page_text_after
                
                if playbook_generated:
                    print("✅ Playbook generated successfully after button click")
                    print("✅ Empty state transitions correctly to playbook view")
                else:
                    print("⚠️  Playbook may not have generated (check API)")
                
            except Exception as e:
                print(f"❌ Error clicking Generate button: {str(e)}")
        
        driver.quit()
        
        print("\n" + "=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)
        
        return critical_passed
        
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_no_playbook_generated_state()
    exit(0 if success else 1)


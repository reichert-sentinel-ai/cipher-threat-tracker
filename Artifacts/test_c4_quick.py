"""
Quick verification script for Sprint C4 - Runs faster tests
"""

import time
import json
from datetime import datetime

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

IR_PLAYBOOKS_URL = "http://localhost:5173/ir-playbooks"

def quick_check():
    """Quick check of key functionality"""
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed")
        return False
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except WebDriverException:
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            print("❌ ChromeDriver not available")
            return False
    
    results = {}
    
    try:
        # Test 1: Page loads
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        results['page_loads'] = "Incident Response" in driver.page_source
        
        # Test 2: Generate button exists
        buttons = driver.find_elements(By.TAG_NAME, "button")
        has_generate = any("generate" in b.text.lower() for b in buttons)
        results['generate_button'] = has_generate
        
        # Test 3: Generate playbook
        if has_generate:
            generate_btn = [b for b in buttons if "generate" in b.text.lower()][0]
            generate_btn.click()
            time.sleep(6)
            page_text = driver.find_element(By.TAG_NAME, "body").text
            results['playbook_generated'] = "PB-" in page_text or "Playbook ID" in page_text
            
            if results['playbook_generated']:
                # Quick checks
                results['has_nist_phases'] = any(phase in page_text for phase in ["Preparation", "Containment", "Recovery"])
                results['has_steps'] = "Responsible" in page_text and "Estimated Time" in page_text
                results['has_tabs'] = all(tab in page_text for tab in ["Stakeholders", "Evidence", "Compliance"])
                results['has_metrics'] = "Time to Detect" in page_text or "Performance Metrics" in page_text
                results['has_export'] = "Export" in page_text or "Download" in page_text
        
        driver.quit()
        
        # Print results
        print("\n" + "="*60)
        print("QUICK VERIFICATION RESULTS")
        print("="*60)
        for test, passed in results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {test.replace('_', ' ').title()}: {passed}")
        
        all_passed = all(results.values())
        print("\n" + "="*60)
        print(f"Overall: {'✅ ALL CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'}")
        print("="*60)
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        driver.quit()
        return False

if __name__ == "__main__":
    quick_check()


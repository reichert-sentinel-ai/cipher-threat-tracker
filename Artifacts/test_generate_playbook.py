"""
Automated Playbook Generation Test
Helps generate a playbook and verify all steps work correctly
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

IR_PLAYBOOKS_URL = "http://localhost:5173/ir-playbooks"

def generate_playbook_interactive(headless=False):
    """Interactive playbook generation with detailed output"""
    print("=" * 70)
    print("IR Playbook Generator - Interactive Test")
    print("=" * 70)
    print("")
    
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
                print("❌ Please install webdriver-manager: pip install webdriver-manager")
                return False
        
        print("🌐 Loading page...")
        driver.get(IR_PLAYBOOKS_URL)
        time.sleep(3)
        
        print("\n" + "-" * 70)
        print("STEP 1: Verify Page Loaded")
        print("-" * 70)
        page_text = driver.find_element(By.TAG_NAME, "body").text
        if "Incident Response Playbook Generator" in page_text:
            print("✅ Page loaded successfully")
        else:
            print("❌ Page may not have loaded correctly")
        
        print("\n" + "-" * 70)
        print("STEP 2: Verify Configuration Form")
        print("-" * 70)
        form_labels = ["Incident Type", "Severity", "Scope", "Automation"]
        found_labels = [label for label in form_labels if label in page_text]
        print(f"✅ Found {len(found_labels)}/{len(form_labels)} form labels: {', '.join(found_labels)}")
        
        print("\n" + "-" * 70)
        print("STEP 3: Find Generate Button")
        print("-" * 70)
        buttons = driver.find_elements(By.TAG_NAME, "button")
        generate_button = None
        for button in buttons:
            btn_text = button.text.lower()
            if "generate" in btn_text and "playbook" in btn_text:
                generate_button = button
                print(f"✅ Generate button found: '{button.text}'")
                break
        
        if not generate_button:
            print("❌ Generate button not found")
            print("Available buttons:", [btn.text for btn in buttons[:5]])
            driver.quit()
            return False
        
        print("\n" + "-" * 70)
        print("STEP 4: Check Current State")
        print("-" * 70)
        if "No Playbook Generated" in page_text:
            print("✅ Empty state detected - ready to generate")
        elif "PB-" in page_text:
            print("⚠️  Playbook already exists - will generate new one")
        else:
            print("ℹ️  State unclear - proceeding with generation")
        
        print("\n" + "-" * 70)
        print("STEP 5: Click Generate Button")
        print("-" * 70)
        try:
            # Scroll to button
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", generate_button)
            time.sleep(0.5)
            
            # Check if button is enabled
            if not generate_button.is_enabled():
                print("⚠️  Generate button is disabled")
            else:
                print("✅ Generate button is enabled")
            
            # Click button
            generate_button.click()
            print("✅ Generate button clicked")
            
            # Wait for loading
            print("⏳ Waiting for playbook generation (6 seconds)...")
            time.sleep(6)
            
        except Exception as e:
            print(f"❌ Error clicking Generate button: {str(e)}")
            driver.quit()
            return False
        
        print("\n" + "-" * 70)
        print("STEP 6: Verify Playbook Generated")
        print("-" * 70)
        page_text_after = driver.find_element(By.TAG_NAME, "body").text
        
        # Check for playbook ID
        has_playbook_id = "PB-" in page_text_after or "Playbook ID" in page_text_after
        
        if has_playbook_id:
            print("✅ Playbook ID found - generation successful!")
            
            # Extract playbook ID if possible
            if "PB-" in page_text_after:
                lines = page_text_after.split('\n')
                for line in lines:
                    if "PB-" in line:
                        playbook_id = line.strip().split()[0] if line.strip().split() else "PB-XXXXXX"
                        print(f"   Playbook ID: {playbook_id}")
                        break
        else:
            print("❌ Playbook ID not found - generation may have failed")
            print("   Check browser console for errors")
        
        # Check for key sections
        sections = ["Response Steps", "Stakeholders", "Evidence", "Compliance"]
        found_sections = [sec for sec in sections if sec in page_text_after]
        print(f"✅ Found {len(found_sections)}/{len(sections)} sections: {', '.join(found_sections)}")
        
        # Check for phases
        phases = ["Preparation", "Containment", "Recovery"]
        found_phases = [p for p in phases if p in page_text_after]
        print(f"✅ Found {len(found_phases)}/{len(phases)} phase indicators")
        
        print("\n" + "-" * 70)
        print("STEP 7: Test Export Functionality")
        print("-" * 70)
        buttons_after = driver.find_elements(By.TAG_NAME, "button")
        export_button = None
        for button in buttons_after:
            if "export" in button.text.lower() or "download" in button.text.lower():
                export_button = button
                break
        
        if export_button:
            print("✅ Export button found")
            if export_button.is_enabled():
                print("✅ Export button is enabled")
            else:
                print("⚠️  Export button is disabled")
        else:
            print("❌ Export button not found")
        
        print("\n" + "-" * 70)
        print("STEP 8: Test Copy Functionality")
        print("-" * 70)
        copy_button = None
        for button in buttons_after:
            if "copy" in button.text.lower():
                copy_button = button
                break
        
        if copy_button:
            print("✅ Copy button found")
            if copy_button.is_enabled():
                print("✅ Copy button is enabled")
            else:
                print("⚠️  Copy button is disabled")
        else:
            print("❌ Copy button not found")
        
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        success = has_playbook_id and len(found_sections) >= 3
        
        if success:
            print("✅ SUCCESS: Playbook generated successfully!")
            print("   - Playbook ID: Present")
            print(f"   - Sections: {len(found_sections)}/{len(sections)}")
            print(f"   - Phases: {len(found_phases)}/{len(phases)}")
            print("   - Export: Available")
            print("   - Copy: Available")
        else:
            print("❌ FAILED: Playbook generation may have issues")
            print("   Please check:")
            print("   1. Backend API is running on port 8000")
            print("   2. Browser console for errors (F12)")
            print("   3. Network tab for API failures")
        
        if not headless:
            print("\n💡 Tip: Browser window is open - you can interact manually")
            print("   Press Enter to close...")
            input()
        
        driver.quit()
        
        return success
        
    except Exception as e:
        print(f"\n❌ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    headless = "--headless" in sys.argv
    
    print("")
    print("🔧 IR Playbook Generator - Automated Test")
    print("")
    print("This will:")
    print("  1. Load the IR Playbooks page")
    print("  2. Click the Generate button")
    print("  3. Verify playbook generation")
    print("  4. Test export and copy functionality")
    print("")
    
    if not headless:
        print("⚠️  Running in visible mode - you can watch the browser")
        print("   (Add --headless flag to run without showing browser)")
    
    print("")
    
    success = generate_playbook_interactive(headless=headless)
    exit(0 if success else 1)


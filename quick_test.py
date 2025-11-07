"""Quick test script for threat timeline endpoint"""

import requests
import json

BASE_URL = "http://localhost:8000/api/threat-timeline"

print("=" * 60)
print("THREAT TIMELINE API TEST")
print("=" * 60)

# Test 1: Basic endpoint
print("\n1. Testing basic endpoint...")
try:
    response = requests.get(f"{BASE_URL}/events?days_back=30", timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"   ✅ SUCCESS")
    print(f"   Total Events: {data.get('total_events', 0)}")
    print(f"   Campaigns: {len(data.get('campaigns', []))}")
    print(f"   Date Range: {data.get('date_range', {}).get('start')} to {data.get('date_range', {}).get('end')}")
    if data.get('events'):
        print(f"   First Event: {data['events'][0].get('title', 'N/A')}")
except requests.exceptions.Timeout:
    print(f"   ❌ FAILED: Request timed out - server may not be running or is hanging")
except requests.exceptions.ConnectionError:
    print(f"   ❌ FAILED: Could not connect to server - is it running on port 8000?")
except Exception as e:
    print(f"   ❌ FAILED: {type(e).__name__}: {e}")

# Test 2: Severity filter
print("\n2. Testing severity filter...")
try:
    response = requests.get(f"{BASE_URL}/events?severity=critical", timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"   ✅ SUCCESS")
    print(f"   Critical Events: {data.get('total_events', 0)}")
except Exception as e:
    print(f"   ❌ FAILED: {type(e).__name__}: {e}")

# Test 3: Attack chain
print("\n3. Testing attack chain...")
try:
    response = requests.get(f"{BASE_URL}/attack-chain/camp_001", timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"   ✅ SUCCESS")
    print(f"   Campaign: {data.get('campaign_name', 'N/A')}")
    print(f"   Stages: {len(data.get('stages', []))}")
    print(f"   Duration: {data.get('total_duration', 'N/A')}")
except Exception as e:
    print(f"   ❌ FAILED: {type(e).__name__}: {e}")

# Test 4: Event details
print("\n4. Testing event details...")
try:
    response = requests.get(f"{BASE_URL}/event-details/evt_0001", timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"   ✅ SUCCESS")
    print(f"   Event ID: {data.get('event_id', 'N/A')}")
    print(f"   Response Actions: {len(data.get('response_actions', []))}")
except Exception as e:
    print(f"   ❌ FAILED: {type(e).__name__}: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\n⚠️  NOTE: If tests are timing out, restart the backend server:")
print("   cd project/repo-cipher")
print("   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000")

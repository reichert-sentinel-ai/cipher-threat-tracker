"""Test script for Threat Timeline C1 endpoints"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/threat-timeline"

def test_endpoint(name, url, params=None):
    """Test an endpoint and display results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    if params:
        print(f"Params: {params}")
    print('='*60)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Status: {response.status_code}")
        
        if name == "Timeline Events":
            print(f"   Total Events: {data.get('total_events', 0)}")
            print(f"   Campaigns: {len(data.get('campaigns', []))}")
            print(f"   Date Range: {data.get('date_range', {}).get('start')} to {data.get('date_range', {}).get('end')}")
            if data.get('events'):
                print(f"   First Event Severity: {data['events'][0].get('severity')}")
                print(f"   First Event Type: {data['events'][0].get('event_type')}")
                print(f"   First Event Title: {data['events'][0].get('title')[:50]}...")
            print(f"   Insights: {len(data.get('attack_pattern_insights', []))} insights")
            print(f"   Trending Threats: {len(data.get('trending_threats', []))}")
            
        elif name == "Severity Filter":
            print(f"   Filtered Events: {data.get('total_events', 0)}")
            severities = [e.get('severity') for e in data.get('events', [])]
            print(f"   All Severities: {set(severities)}")
            if all(s == 'critical' for s in severities):
                print("   ✅ All events are critical (filter working)")
            else:
                print("   ⚠️  Filter may not be working correctly")
                
        elif name == "Attack Chain":
            print(f"   Campaign: {data.get('campaign_name')}")
            print(f"   Stages: {len(data.get('stages', []))}")
            print(f"   Kill Chain Phase: {data.get('kill_chain_phase')}")
            print(f"   Duration: {data.get('total_duration')}")
            stages = data.get('stages', [])
            if stages:
                print(f"   First Stage: {stages[0].get('stage')}")
                print(f"   Last Stage: {stages[-1].get('stage')}")
                
        elif name == "Event Details":
            print(f"   Event ID: {data.get('event_id')}")
            print(f"   Response Actions: {len(data.get('response_actions', []))}")
            print(f"   Affected Assets: {len(data.get('affected_assets', []))}")
            print(f"   Attribution Confidence: {data.get('attribution_confidence')}")
            print(f"   Related Campaigns: {len(data.get('related_campaigns', []))}")
            
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("THREAT TIMELINE C1 TEST SUITE")
    print("="*60)
    
    tests = [
        ("Timeline Events", f"{BASE_URL}/events", {"days_back": 7}),
        ("Timeline Events (30 days)", f"{BASE_URL}/events", {"days_back": 30}),
        ("Severity Filter", f"{BASE_URL}/events", {"severity": "critical"}),
        ("Event Type Filter", f"{BASE_URL}/events", {"event_type": "attack"}),
        ("Threat Actor Filter", f"{BASE_URL}/events", {"threat_actor": "APT28 (Fancy Bear)"}),
        ("Attack Chain", f"{BASE_URL}/attack-chain/camp_001", None),
        ("Event Details", f"{BASE_URL}/event-details/evt_0001", None),
    ]
    
    results = []
    for name, url, params in tests:
        success = test_endpoint(name, url, params)
        results.append((name, success))
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")


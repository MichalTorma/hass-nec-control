#!/usr/bin/env python3
"""
Test script for NEC TV Control API
"""

import requests
import json
import sys

def test_api():
    """Test the NEC TV Control API"""
    base_url = "http://localhost:8124"
    
    print("Testing NEC TV Control API...")
    print("=" * 40)
    
    # Test 1: Get service info
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Service Info: {data}")
        else:
            print(f"❌ Service Info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Service Info error: {e}")
    
    # Test 2: Get health status
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")
    
    # Test 3: Turn TV on
    try:
        response = requests.post(
            f"{base_url}/power",
            headers={"Content-Type": "application/json"},
            json={"action": "on"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Turn TV On: {data}")
        else:
            print(f"❌ Turn TV On failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Turn TV On error: {e}")
    
    # Test 4: Turn TV off
    try:
        response = requests.post(
            f"{base_url}/power",
            headers={"Content-Type": "application/json"},
            json={"action": "off"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Turn TV Off: {data}")
        else:
            print(f"❌ Turn TV Off failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Turn TV Off error: {e}")

if __name__ == "__main__":
    test_api() 
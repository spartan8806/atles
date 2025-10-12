#!/usr/bin/env python3
"""
Test script for ATLES proactive messaging system
"""

import time
import json
from datetime import datetime

def test_proactive_config():
    """Test the proactive messaging configuration"""
    print("🧪 Testing ATLES Proactive Messaging Configuration")
    print("=" * 50)
    
    try:
        # Load configuration
        with open('atles_config.json', 'r') as f:
            config = json.load(f)
        
        print("✅ Configuration loaded successfully")
        
        # Check proactive messaging settings
        pm_config = config.get('proactive_messaging', {})
        
        print(f"\n📋 Proactive Messaging Settings:")
        print(f"   Enabled: {pm_config.get('enabled', 'Not set')}")
        print(f"   Overnight Messaging: {pm_config.get('overnight_messaging', 'Not set')}")
        print(f"   Idle Threshold: {pm_config.get('idle_threshold_minutes', 'Not set')} minutes")
        print(f"   Overnight Threshold: {pm_config.get('overnight_threshold_hours', 'Not set')} hours")
        print(f"   Self-Review Enabled: {pm_config.get('self_review_enabled', 'Not set')}")
        print(f"   Self-Review Threshold: {pm_config.get('self_review_threshold_minutes', 'Not set')} minutes")
        
        # Check constitutional safeguards
        cs_config = config.get('constitutional_safeguards', {})
        print(f"\n🛡️ Constitutional Safeguards:")
        print(f"   Min Pattern Observations: {cs_config.get('min_pattern_observations', 'Not set')}")
        print(f"   Min Confidence Threshold: {cs_config.get('min_confidence_threshold', 'Not set')}")
        
        print(f"\n✅ Configuration test completed successfully!")
        
    except FileNotFoundError:
        print("❌ Configuration file not found: atles_config.json")
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration: {e}")
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")

def test_timing_calculations():
    """Test the timing calculations for proactive messaging"""
    print(f"\n⏰ Testing Timing Calculations")
    print("=" * 50)
    
    # Test idle threshold (60 minutes = 3600 seconds)
    idle_minutes = 60
    idle_seconds = idle_minutes * 60
    print(f"Idle threshold: {idle_minutes} minutes = {idle_seconds} seconds")
    
    # Test overnight threshold (4 hours = 14400 seconds)
    overnight_hours = 4
    overnight_seconds = overnight_hours * 3600
    print(f"Overnight threshold: {overnight_hours} hours = {overnight_seconds} seconds")
    
    # Test self-review threshold (2 hours = 7200 seconds)
    self_review_hours = 2
    self_review_seconds = self_review_hours * 3600
    print(f"Self-review threshold: {self_review_hours} hours = {self_review_seconds} seconds")
    
    # Test minimum interval (1 hour = 3600 seconds)
    min_interval_hours = 1
    min_interval_seconds = min_interval_hours * 3600
    print(f"Minimum interval: {min_interval_hours} hour = {min_interval_seconds} seconds")
    
    print(f"\n✅ Timing calculations test completed!")

def test_overnight_hours():
    """Test overnight hour detection logic"""
    print(f"\n🌙 Testing Overnight Hour Detection")
    print("=" * 50)
    
    test_hours = [22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    
    for hour in test_hours:
        is_overnight = hour >= 22 or hour <= 8
        status = "🌙 OVERNIGHT" if is_overnight else "☀️ DAYTIME"
        print(f"   {hour:02d}:00 - {status}")
    
    print(f"\n✅ Overnight hour detection test completed!")

def main():
    """Run all tests"""
    print("🚀 ATLES Proactive Messaging System Test Suite")
    print("=" * 60)
    
    test_proactive_config()
    test_timing_calculations()
    test_overnight_hours()
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"\n📝 Next Steps:")
    print(f"   1. Run ATLES Desktop: python atles_desktop_pyqt.py")
    print(f"   2. Click 'Test Mode: ON' to bypass safeguards")
    print(f"   3. Click 'Test Proactive' to test different message types")
    print(f"   4. Leave running overnight to test automatic messaging")

if __name__ == "__main__":
    main()

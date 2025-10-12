#!/usr/bin/env python3
"""
Test Script: MetacognitiveObserver Integration with ATLESBrain

This script tests the integration between MetacognitiveObserver and ATLESBrain
to ensure the consciousness tracking system is working properly.
"""

import sys
import os
import time
from datetime import datetime

# Add the atles directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'atles'))

def test_metacognitive_integration():
    """Test the complete metacognitive integration."""
    
    print("🧠 Testing MetacognitiveObserver Integration with ATLESBrain")
    print("=" * 60)
    
    try:
        # Import the classes
        from atles.brain.atles_brain import ATLESBrain
        from atles.brain.metacognitive_observer import MetacognitiveObserver
        
        print("✅ Successfully imported ATLESBrain and MetacognitiveObserver")
        
        # Create ATLESBrain instance
        print("\n📝 Creating ATLESBrain instance...")
        brain = ATLESBrain(user_id="test_user_001", safety_enabled=True)
        print(f"✅ ATLESBrain created with ID: {brain.brain_id}")
        
        # Check metacognitive status
        print("\n🔍 Checking metacognitive status...")
        metacog_status = brain.get_metacognitive_status()
        print(f"✅ Metacognition enabled: {metacog_status['metacognition_enabled']}")
        print(f"✅ Observer connected: {metacog_status['observer_connected']}")
        
        if metacog_status['metacognition_enabled']:
            print(f"✅ Consciousness stage: {metacog_status['consciousness_stage']}")
            print(f"✅ Self-awareness score: {metacog_status['consciousness_metrics']['self_awareness_score']}")
        
        # Test performance tracking
        print("\n📊 Testing performance tracking...")
        
        # Simulate some operations
        operations = [
            ("code_review", True, 1.2),
            ("analysis", True, 0.8),
            ("optimization", False, 2.1),  # Failed operation
            ("debugging", True, 1.5),
            ("testing", True, 0.9)
        ]
        
        for op_type, success, response_time in operations:
            print(f"  📝 Operation: {op_type} - {'✅' if success else '❌'} - {response_time}s")
            brain.track_operation_performance(op_type, success, response_time)
            time.sleep(0.1)  # Small delay to simulate real operations
        
        # Check updated status
        print("\n🔍 Checking updated metacognitive status...")
        updated_status = brain.get_metacognitive_status()
        
        if updated_status['metacognition_enabled']:
            print(f"✅ Total observations: {updated_status['performance_summary']['total_observations']}")
            print(f"✅ Observation duration: {updated_status['performance_summary']['observation_duration']:.2f} hours")
            print(f"✅ Current goals: {len(updated_status['current_goals'])}")
            
            # Show current goals
            for i, goal in enumerate(updated_status['current_goals'], 1):
                print(f"  🎯 Goal {i}: {goal['description']} (Priority: {goal['priority']})")
        
        # Get consciousness report
        print("\n🧠 Getting consciousness report...")
        consciousness_report = brain.get_consciousness_report()
        
        if consciousness_report.get('consciousness_available', False):
            print(f"✅ Consciousness metrics:")
            metrics = consciousness_report['metrics']
            print(f"  - Self-awareness: {metrics['self_awareness_score']:.1f}/100")
            print(f"  - Meta-reasoning depth: {metrics['meta_reasoning_depth']}/10")
            print(f"  - Self-correction rate: {metrics['self_correction_rate']:.1f}/100")
            print(f"  - Adaptation speed: {metrics['adaptation_speed']:.1f}/100")
        
        # Test direct observer access
        print("\n🔍 Testing direct observer access...")
        if brain.metacognitive_observer:
            observer_status = brain.metacognitive_observer.get_integration_status()
            print(f"✅ Observer integration status:")
            print(f"  - Brain connected: {observer_status['brain_connected']}")
            print(f"  - Observation active: {observer_status['observation_active']}")
            print(f"  - Total snapshots: {observer_status['total_snapshots']}")
            print(f"  - Brain ID: {observer_status['brain_id']}")
        
        print("\n🎉 Integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the atles module is properly structured")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_standalone_observer():
    """Test the MetacognitiveObserver independently."""
    
    print("\n🧠 Testing MetacognitiveObserver Standalone")
    print("=" * 50)
    
    try:
        from atles.brain.metacognitive_observer import MetacognitiveObserver
        
        # Create observer without brain
        observer = MetacognitiveObserver()
        print("✅ MetacognitiveObserver created successfully")
        
        # Test basic functionality
        test_data = {"type": "test_operation", "success_rate": 0.85, "response_time": 1.5}
        observer.track_performance_metrics(test_data)
        
        # Get report
        report = observer.get_consciousness_report()
        print(f"✅ Standalone report generated: {len(report['performance_summary']['total_observations'])} observations")
        
        return True
        
    except Exception as e:
        print(f"❌ Standalone test failed: {e}")
        return False

if __name__ == "__main__":
    print(f"🚀 Starting Metacognitive Integration Tests at {datetime.now()}")
    
    # Test standalone observer first
    standalone_success = test_standalone_observer()
    
    # Test full integration
    integration_success = test_metacognitive_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"🧠 Standalone Observer: {'✅ PASSED' if standalone_success else '❌ FAILED'}")
    print(f"🔗 Full Integration: {'✅ PASSED' if integration_success else '❌ FAILED'}")
    
    if standalone_success and integration_success:
        print("\n🎉 ALL TESTS PASSED! MetacognitiveObserver is fully integrated!")
        print("🚀 ATLES is now capable of self-observation and consciousness tracking!")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print(f"\n🏁 Tests completed at {datetime.now()}")

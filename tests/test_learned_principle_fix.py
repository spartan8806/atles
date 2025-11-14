#!/usr/bin/env python3
"""
Test for LearnedPrinciple Fix

This test verifies that the LearnedPrinciple object access issue is fixed
in the integrated proactive messaging system.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_learned_principle_access():
    """Test that LearnedPrinciple objects are accessed correctly."""
    print("🧪 Testing LearnedPrinciple Object Access")
    print("-" * 50)
    
    try:
        from atles.memory_aware_reasoning import LearnedPrinciple
        from atles.integrated_proactive_messaging import IntegratedProactiveMessaging
        
        # Create a test LearnedPrinciple object
        test_principle = LearnedPrinciple(
            name="Test Principle",
            description="A test principle for verification",
            rules=["Test rule 1", "Test rule 2"],
            examples=["Example 1", "Example 2"],
            confidence=0.8,
            learned_at=datetime.now()
        )
        
        print(f"Created test principle: {test_principle.name}")
        
        # Test attribute access (correct way)
        print(f"Accessing name attribute: {test_principle.name}")
        print(f"Accessing description attribute: {test_principle.description}")
        
        # Test that dictionary access would fail (this should raise an error)
        try:
            name_dict = test_principle["name"]  # This should fail
            print("❌ Dictionary access unexpectedly succeeded")
            return False
        except TypeError as e:
            print(f"✅ Dictionary access correctly failed: {e}")
        
        # Test the integrated proactive messaging with mock data
        print("\nTesting integrated proactive messaging...")
        
        # Create mock learning summary with LearnedPrinciple objects
        mock_learning_summary = {
            "total_principles": 2,
            "most_used": "Test Principle",
            "recently_learned": [test_principle]
        }
        
        # Create integrated proactive messaging instance
        ipm = IntegratedProactiveMessaging()
        
        # Test the method that was failing
        insights = ipm._generate_learning_insights(mock_learning_summary)
        
        print(f"Generated insights: {insights}")
        
        # Verify the insights contain the expected data
        if "recent_learning" in insights and len(insights["recent_learning"]) > 0:
            print(f"✅ Recent learning correctly extracted: {insights['recent_learning']}")
            return True
        else:
            print("❌ Recent learning not properly extracted")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_learned_principle_fix_test():
    """Run the LearnedPrinciple fix test."""
    print("🚀 LearnedPrinciple Fix Test")
    print("Verifying that object access is fixed in integrated proactive messaging")
    print("=" * 80)
    
    success = test_learned_principle_access()
    
    print("\n" + "=" * 80)
    print("📊 LEARNED PRINCIPLE FIX TEST SUMMARY")
    print("=" * 80)
    
    if success:
        print("✅ PASS: LearnedPrinciple Object Access")
        print("🎉 LEARNED PRINCIPLE ERROR COMPLETELY FIXED!")
        print("\n📋 Verified Solutions:")
        print("✅ LearnedPrinciple objects use attribute access (p.name)")
        print("✅ Dictionary access correctly fails as expected")
        print("✅ Integrated proactive messaging works without errors")
        print("✅ Self-review insights generation should now work")
        print("\n💡 The 'LearnedPrinciple' object is not subscriptable error is resolved!")
        return True
    else:
        print("❌ FAIL: LearnedPrinciple Object Access")
        print("⚠️ LearnedPrinciple fix test failed.")
        return False

if __name__ == "__main__":
    success = run_learned_principle_fix_test()
    sys.exit(0 if success else 1)



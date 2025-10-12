#!/usr/bin/env python3
"""
Test Principle Deduplication Fix

This tests that the principle loading issue is fixed and no longer loads
the same principle multiple times.
"""

import sys
from pathlib import Path

# Add the atles module to the path
sys.path.insert(0, str(Path(__file__).parent))

from atles.memory_aware_reasoning import MemoryAwareReasoning


def test_principle_deduplication():
    """Test that principles are deduplicated properly."""
    print("🧪 TESTING PRINCIPLE DEDUPLICATION FIX")
    print("=" * 50)
    
    # Initialize memory reasoning
    memory_reasoning = MemoryAwareReasoning("atles_memory")
    
    # Test processing a hypothetical question
    print("💭 Testing hypothetical question processing...")
    
    enhanced_context = memory_reasoning.process_user_prompt(
        "What would you like to do today?"
    )
    
    # Check active principles
    active_principles = enhanced_context.get("active_principles", [])
    contextual_rules = enhanced_context.get("contextual_rules", [])
    
    print(f"\n📊 RESULTS:")
    print(f"   Active principles: {len(active_principles)}")
    for principle in active_principles:
        print(f"      • {principle}")
    
    print(f"   Contextual rules: {len(contextual_rules)}")
    for rule in contextual_rules:
        print(f"      • {rule.get('principle', 'Unknown')}: {rule.get('rule', '')[:50]}...")
    
    # Check for duplicates
    principle_counts = {}
    for principle in active_principles:
        principle_counts[principle] = principle_counts.get(principle, 0) + 1
    
    duplicates = {p: count for p, count in principle_counts.items() if count > 1}
    
    if duplicates:
        print(f"\n❌ DUPLICATES FOUND:")
        for principle, count in duplicates.items():
            print(f"   • {principle}: {count} times")
        return False
    else:
        print(f"\n✅ NO DUPLICATES FOUND!")
        
        # Check if Hypothetical Engagement is present
        if "Principle of Hypothetical Engagement" in active_principles:
            print(f"   ✅ Hypothetical Engagement principle loaded correctly")
            return True
        else:
            print(f"   ⚠️  Hypothetical Engagement principle not found")
            return False


def test_constitutional_client_integration():
    """Test that the constitutional client handles principles correctly."""
    print(f"\n🔧 TESTING CONSTITUTIONAL CLIENT INTEGRATION")
    print("=" * 50)
    
    try:
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        # Create mock response context
        response_context = {
            "active_principles": ["Principle of Hypothetical Engagement"],
            "contextual_rules": [
                {
                    "principle": "Principle of Hypothetical Engagement",
                    "rule": "Acknowledge hypothetical nature",
                    "relevance": 0.9
                }
            ]
        }
        
        # Test the principle-based response generation
        client = ConstitutionalOllamaClient()
        response = client._generate_principle_based_response(
            "What would you like to do today?",
            response_context
        )
        
        print(f"📝 Constitutional client response:")
        if response is None:
            print(f"   ✅ Correctly returned None (let normal generation handle it)")
            return True
        else:
            print(f"   Response: {response}")
            # Check if it's not the old triple announcement
            if "Principle of Hypothetical Engagement, Principle of Hypothetical Engagement, Principle of Hypothetical Engagement" in response:
                print(f"   ❌ Still has triple announcement!")
                return False
            else:
                print(f"   ✅ No triple announcement found")
                return True
                
    except Exception as e:
        print(f"   ❌ Error testing constitutional client: {e}")
        return False


def main():
    """Main test function."""
    print("🔧 TESTING PRINCIPLE DEDUPLICATION FIXES")
    print("=" * 60)
    
    # Test 1: Memory reasoning deduplication
    test1_success = test_principle_deduplication()
    
    # Test 2: Constitutional client integration
    test2_success = test_constitutional_client_integration()
    
    print(f"\n" + "=" * 60)
    print(f"📊 TEST RESULTS:")
    print(f"   Memory reasoning deduplication: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   Constitutional client integration: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print(f"\n🎉 SUCCESS: Principle deduplication is fixed!")
        print(f"   • No more triple loading of principles")
        print(f"   • Constitutional client handles principles correctly")
        print(f"   • Ready for testing with ATLES Desktop")
    else:
        print(f"\n⚠️  ISSUES REMAIN:")
        if not test1_success:
            print(f"   • Memory reasoning still has deduplication issues")
        if not test2_success:
            print(f"   • Constitutional client integration needs work")
    
    return test1_success and test2_success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n👋 Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

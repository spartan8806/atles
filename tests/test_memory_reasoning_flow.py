#!/usr/bin/env python3
"""
Test the complete memory-aware reasoning flow step by step.
"""

import sys
import os

# Add the atles directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'atles'))

def test_complete_flow():
    """Test the complete memory-aware reasoning flow."""
    
    print("🔄 Testing Complete Memory-Aware Reasoning Flow")
    print("=" * 60)
    
    try:
        from atles.memory_aware_reasoning import MemoryAwareReasoning
        from atles.learning_response_generator import LearningResponseGenerator
        
        # Test the critical prompt
        test_prompt = "What would you like to do today?"
        
        print(f"🎯 Testing prompt: '{test_prompt}'")
        print()
        
        # Step 1: Test MemoryAwareReasoning directly
        print("📋 Step 1: Testing MemoryAwareReasoning.process_user_prompt()")
        print("-" * 50)
        
        memory_reasoning = MemoryAwareReasoning()
        enhanced_context = memory_reasoning.process_user_prompt(test_prompt)
        
        print(f"✅ Enhanced context generated")
        print(f"   Keys: {list(enhanced_context.keys())}")
        print(f"   Memory informed: {enhanced_context.get('memory_informed', False)}")
        print(f"   Active principles: {enhanced_context.get('active_principles', [])}")
        print(f"   Contextual rules count: {len(enhanced_context.get('contextual_rules', []))}")
        
        if enhanced_context.get('contextual_rules'):
            print("   Contextual rules:")
            for rule in enhanced_context.get('contextual_rules', []):
                print(f"     - {rule['principle']}: {rule['rule'][:100]}...")
        
        # Step 2: Test LearningResponseGenerator
        print(f"\n📋 Step 2: Testing LearningResponseGenerator.generate_memory_informed_response()")
        print("-" * 50)
        
        generator = LearningResponseGenerator()
        response_context = generator.generate_memory_informed_response(test_prompt)
        
        print(f"✅ Response context generated")
        print(f"   Keys: {list(response_context.keys())}")
        print(f"   Memory informed: {response_context.get('memory_informed', False)}")
        print(f"   Active principles: {response_context.get('active_principles', [])}")
        
        # Step 3: Test Constitutional Client integration
        print(f"\n📋 Step 3: Testing ConstitutionalOllamaClient integration")
        print("-" * 50)
        
        from atles.constitutional_client import ConstitutionalOllamaClient
        
        class MockBaseClient:
            def generate(self, model, prompt, **kwargs):
                return "Mock response from base client"
        
        mock_base = MockBaseClient()
        client = ConstitutionalOllamaClient(mock_base)
        
        print(f"✅ Constitutional client initialized")
        print(f"   Memory-aware reasoning available: {client.memory_aware_reasoning is not None}")
        
        # Test the memory-aware reasoning application
        memory_response = client._apply_memory_aware_reasoning(test_prompt)
        
        print(f"✅ Memory-aware reasoning applied")
        print(f"   Response generated: {memory_response is not None}")
        
        if memory_response:
            print(f"   Response length: {len(memory_response)} characters")
            print(f"   Response preview: {memory_response[:200]}...")
            
            # Check if it matches expected patterns
            if "interesting question" in memory_response.lower():
                print("   ✅ Contains 'interesting question' pattern")
            if "ai perspective" in memory_response.lower():
                print("   ✅ Contains 'AI perspective' pattern")
            if "intellectual" in memory_response.lower():
                print("   ✅ Contains 'intellectual' pattern")
                
            return True
        else:
            print("   ❌ No response generated")
            
            # Debug why no response was generated
            print(f"\n🔍 Debugging why no response was generated:")
            
            if not client.memory_aware_reasoning:
                print("   ❌ Memory-aware reasoning not initialized")
            else:
                print("   ✅ Memory-aware reasoning initialized")
                
                # Test the response context again
                test_context = client.memory_aware_reasoning.generate_memory_informed_response(test_prompt)
                print(f"   Memory informed: {test_context.get('memory_informed', False)}")
                print(f"   Active principles: {test_context.get('active_principles', [])}")
                
                if not test_context.get('memory_informed'):
                    print("   ❌ Response context not memory informed")
                elif not test_context.get('active_principles'):
                    print("   ❌ No active principles found")
                else:
                    print("   ✅ Context looks good, issue may be in pattern matching")
                    
                    # Check if "Hypothetical Engagement" is in active principles
                    active_principles = test_context.get('active_principles', [])
                    if "Hypothetical Engagement" in active_principles:
                        print("   ✅ 'Hypothetical Engagement' found in active principles")
                    else:
                        print("   ❌ 'Hypothetical Engagement' NOT found in active principles")
                        print(f"   Available principles: {active_principles}")
            
            return False
            
    except Exception as e:
        print(f"❌ Error in flow test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete flow test."""
    
    print("🚀 ATLES Memory-Aware Reasoning Flow Test")
    print("Testing the complete pipeline from memory to response")
    print("=" * 70)
    
    success = test_complete_flow()
    
    print("\n" + "=" * 70)
    print("📊 FLOW TEST RESULTS")
    print("-" * 25)
    
    if success:
        print("✅ COMPLETE FLOW WORKING!")
        print("The memory-aware reasoning system is generating responses correctly.")
        print("The architectural fix should be functional.")
    else:
        print("❌ FLOW ISSUES DETECTED")
        print("The memory-aware reasoning system has integration problems.")
        print("Further debugging needed.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

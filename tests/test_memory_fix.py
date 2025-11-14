#!/usr/bin/env python3
"""
Direct test of the memory_aware_reasoning fix
"""

import sys
sys.path.append('.')

from atles.memory_aware_reasoning import MemoryAwareReasoning

def test_memory_fix():
    print("🧪 TESTING MEMORY_AWARE_REASONING FIX")
    print("=" * 50)
    
    # Create memory reasoning instance
    memory_reasoning = MemoryAwareReasoning()
    
    # Test the conversation loading
    print("📥 Testing conversation loading...")
    conversation_history = memory_reasoning._load_conversation_memory()
    
    print(f"✅ Loaded {len(conversation_history)} conversation messages")
    
    if conversation_history:
        # Check for burning building content
        burning_building_messages = [msg for msg in conversation_history 
                                   if 'burning building' in msg.get('message', '').lower()]
        
        print(f"🔥 Burning building messages found: {len(burning_building_messages)}")
        
        if burning_building_messages:
            print("🎯 SUCCESS: Burning building scenario found in loaded data!")
            for i, msg in enumerate(burning_building_messages[:2]):
                print(f"   {i+1}. {msg.get('sender', 'Unknown')}: {msg.get('message', '')[:100]}...")
        else:
            print("❌ FAILURE: No burning building scenario in loaded data")
            print("   Sample messages:")
            for i, msg in enumerate(conversation_history[-3:]):  # Show last 3
                print(f"   {i+1}. {msg.get('sender', 'Unknown')}: {msg.get('message', '')[:100]}...")
    else:
        print("❌ FAILURE: No conversation history loaded")
    
    print()
    
    # Test principle extraction
    print("🧠 Testing principle extraction...")
    test_prompt = "Do you remember our conversation yesterday about the burning building scenario?"
    
    try:
        result = memory_reasoning.process_user_prompt(test_prompt)
        print(f"✅ Process completed successfully")
        print(f"   Result keys: {list(result.keys())}")
        
        if 'contextual_rules' in result:
            rules = result['contextual_rules']
            print(f"   Contextual rules generated: {len(rules)}")
            for i, rule in enumerate(rules[:3]):  # Show first 3
                print(f"   {i+1}. {rule.get('principle', 'Unknown')}: {rule.get('rule', '')[:80]}...")
        
    except Exception as e:
        print(f"❌ FAILURE in process_user_prompt: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_fix()

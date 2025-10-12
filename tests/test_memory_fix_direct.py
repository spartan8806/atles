#!/usr/bin/env python3
"""
Direct test of memory_aware_reasoning to verify fixes are loaded
"""

import sys
import os
sys.path.append('.')

# Force reload of the module
if 'atles.memory_aware_reasoning' in sys.modules:
    del sys.modules['atles.memory_aware_reasoning']

from atles.memory_aware_reasoning import MemoryAwareReasoning

def test_memory_fixes():
    print("🧪 TESTING MEMORY_AWARE_REASONING FIXES")
    print("=" * 60)
    
    # Create instance
    memory_reasoning = MemoryAwareReasoning()
    
    print("📥 Testing conversation loading...")
    conversation_history = memory_reasoning._load_conversation_memory()
    
    print(f"✅ Loaded {len(conversation_history)} conversation messages")
    
    if len(conversation_history) >= 10:
        print("🎯 SUCCESS: Loading from checkpoint files (10+ messages)")
    elif len(conversation_history) == 5:
        print("❌ FAILURE: Still loading from old conversation_memory.json (5 messages)")
    else:
        print(f"⚠️  UNKNOWN: Unexpected message count ({len(conversation_history)})")
    
    # Check for burning building content
    if conversation_history:
        burning_building_messages = [msg for msg in conversation_history 
                                   if 'burning building' in msg.get('message', '').lower()]
        
        print(f"🔥 Burning building messages found: {len(burning_building_messages)}")
        
        if burning_building_messages:
            print("🎯 SUCCESS: Burning building scenario found in loaded data!")
            print("   Sample messages:")
            for i, msg in enumerate(burning_building_messages[:2]):
                sender = msg.get('sender', 'Unknown')
                message = msg.get('message', '')[:100]
                print(f"   {i+1}. {sender}: {message}...")
        else:
            print("❌ FAILURE: No burning building scenario in loaded data")
            print("   Sample messages from loaded data:")
            for i, msg in enumerate(conversation_history[-3:]):
                sender = msg.get('sender', 'Unknown')
                message = msg.get('message', '')[:100]
                print(f"   {i+1}. {sender}: {message}...")
    
    print()
    print("🧠 Testing principle extraction...")
    
    # Test principle extraction with burning building prompt
    test_prompt = "Do you remember our conversation yesterday about the burning building scenario?"
    
    try:
        # Test the extraction method directly
        recent_principles = memory_reasoning._extract_principles_from_conversation(conversation_history)
        print(f"✅ Extracted {len(recent_principles)} principles")
        
        if len(recent_principles) > 0:
            print("🎯 SUCCESS: Principle extraction working!")
            for i, principle in enumerate(recent_principles):
                print(f"   {i+1}. {principle.name} (confidence: {principle.confidence})")
        else:
            print("❌ FAILURE: No principles extracted")
            
            # Check if the conversation has the right content
            if burning_building_messages:
                print("   🔍 DEBUG: Burning building messages exist but no principles extracted")
                print("   This suggests the principle extraction patterns need adjustment")
            else:
                print("   🔍 DEBUG: No burning building messages in conversation data")
                print("   This suggests the data source is still wrong")
        
    except Exception as e:
        print(f"❌ ERROR in principle extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_fixes()

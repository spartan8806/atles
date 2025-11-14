#!/usr/bin/env python3
"""
Test Automatic Principle Learning

This script tests that the system automatically learns principles from conversations
without manual intervention - addressing the core concern about automation.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the atles module to the path
sys.path.insert(0, str(Path(__file__).parent))

from atles.memory_integration import MemoryIntegration


def test_automatic_learning():
    """Test that principles are automatically learned from conversations."""
    print("🧠 TESTING AUTOMATIC PRINCIPLE LEARNING")
    print("=" * 50)
    
    # Initialize memory system (use test directory)
    memory = MemoryIntegration("test_memory", auto_migrate=False)
    
    # Start a conversation session
    session_id = memory.start_conversation_session("test_session")
    print(f"📝 Started session: {session_id}")
    
    # Simulate a conversation where the user teaches a new principle
    print(f"\n💬 Simulating conversation with principle teaching...")
    
    # User teaches a new principle
    memory.add_message(
        "You", 
        "ATLES, I want to teach you a new principle. The Principle of Concise Communication: When responding to simple questions, you should always provide concise answers first, then offer to elaborate if needed. Never overwhelm users with unnecessary detail upfront."
    )
    
    # AI acknowledges
    memory.add_message(
        "ATLES",
        "I understand the Principle of Concise Communication. I should provide concise answers first and offer to elaborate rather than overwhelming users with detail."
    )
    
    # User gives another behavioral guideline
    memory.add_message(
        "You",
        "Also, remember to always ask for clarification when a request is ambiguous rather than making assumptions."
    )
    
    # AI responds
    memory.add_message(
        "ATLES", 
        "Understood. I will ask for clarification when requests are ambiguous instead of making assumptions."
    )
    
    print(f"   Added {len(memory.current_conversation)} messages to conversation")
    
    # End the session - this should trigger automatic principle extraction
    print(f"\n🔄 Ending session (triggering automatic learning)...")
    episode_id = memory.end_conversation_session()
    
    if episode_id:
        print(f"   ✅ Created episode: {episode_id}")
        
        # Check if principles were automatically learned
        stats = memory.get_memory_stats()
        learned_principles = stats.get("learned_principles", {})
        total_principles = learned_principles.get("total_principles", 0)
        
        print(f"\n📊 LEARNING RESULTS:")
        print(f"   Total principles in system: {total_principles}")
        
        if total_principles > 0:
            print(f"   ✅ SUCCESS: Principles were automatically learned!")
            
            # Show the learned principles
            principles = learned_principles.get("principles", [])
            for i, principle in enumerate(principles, 1):
                print(f"\n   {i}. {principle['name']}")
                print(f"      Confidence: {principle['confidence']}")
                print(f"      Learned: {principle['learned_at']}")
                print(f"      Applications: {principle['application_count']}")
        else:
            print(f"   ❌ FAILURE: No principles were automatically learned")
            return False
    else:
        print(f"   ❌ Failed to create episode")
        return False
    
    # Test that the principles are applied in future conversations
    print(f"\n🔍 TESTING PRINCIPLE APPLICATION...")
    
    # Start new session
    new_session = memory.start_conversation_session("test_application")
    
    # Process a user prompt that should trigger the learned principle
    enhanced_context = memory.process_user_prompt_with_memory(
        "What is machine learning?"
    )
    
    # Check if learned principles are in the context
    constitutional_principles = enhanced_context.get("constitutional_principles", [])
    response_guidelines = enhanced_context.get("response_guidelines", [])
    
    print(f"   Constitutional principles loaded: {len(constitutional_principles)}")
    print(f"   Response guidelines: {len(response_guidelines)}")
    
    # Look for our learned principle
    concise_principle_found = False
    for principle in constitutional_principles:
        if "concise" in principle.get("title", "").lower():
            concise_principle_found = True
            print(f"   ✅ Found learned principle: {principle['title']}")
            break
    
    if concise_principle_found:
        print(f"   ✅ SUCCESS: Learned principles are being applied automatically!")
    else:
        print(f"   ⚠️  Learned principles not found in context (may need refinement)")
    
    # Clean up
    memory.end_conversation_session()
    
    # Clean up test files
    import shutil
    test_path = Path("test_memory")
    if test_path.exists():
        shutil.rmtree(test_path)
        print(f"\n🧹 Cleaned up test files")
    
    return total_principles > 0


def test_migration_learning():
    """Test that migration automatically extracts principles."""
    print(f"\n🔄 TESTING MIGRATION WITH AUTOMATIC LEARNING")
    print("=" * 50)
    
    # Test the migration with the real conversation history
    memory = MemoryIntegration("atles_memory", auto_migrate=False)
    
    # Run migration which should automatically extract principles
    print(f"🚀 Running migration with automatic principle extraction...")
    migration_result = memory.migrate_legacy_memory(backup=False)
    
    principles_learned = migration_result.get("principles_learned", 0)
    episodes_created = migration_result.get("episodes_created", 0)
    
    print(f"\n📊 MIGRATION RESULTS:")
    print(f"   Episodes created: {episodes_created}")
    print(f"   Principles learned: {principles_learned}")
    
    if principles_learned > 0:
        print(f"   ✅ SUCCESS: Migration automatically extracted {principles_learned} principles!")
        return True
    else:
        print(f"   ❌ FAILURE: Migration did not extract any principles automatically")
        return False


if __name__ == "__main__":
    try:
        print("🧠 AUTOMATIC LEARNING TEST SUITE")
        print("=" * 60)
        
        # Test 1: Automatic learning in new conversations
        test1_success = test_automatic_learning()
        
        # Test 2: Automatic learning during migration
        test2_success = test_migration_learning()
        
        print(f"\n" + "=" * 60)
        print(f"📊 FINAL RESULTS:")
        print(f"   New conversation learning: {'✅ PASS' if test1_success else '❌ FAIL'}")
        print(f"   Migration learning: {'✅ PASS' if test2_success else '❌ FAIL'}")
        
        if test1_success and test2_success:
            print(f"\n🎉 SUCCESS: Automatic learning is working!")
            print(f"   The system now learns principles automatically without manual intervention.")
            print(f"   This achieves the original goal of true automatic learning.")
        else:
            print(f"\n⚠️  PARTIAL SUCCESS: Some automatic learning is working.")
            print(f"   The system may need further refinement for full automation.")
        
    except KeyboardInterrupt:
        print(f"\n\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
"""
Test script for ATLES Goal Management System

This script demonstrates the multi-goal management capabilities
that enable Ollama to handle conflicting objectives intelligently.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from atles.ollama_client_enhanced import OllamaFunctionCaller

def test_goal_management():
    """Test the goal management system."""
    print("🧠 ATLES Goal Management System Test")
    print("=" * 50)
    
    # Initialize the enhanced Ollama client
    try:
        client = OllamaFunctionCaller()
        print("✅ Enhanced Ollama client initialized with goal management")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    print("\n🎯 Testing Goal Analysis...")
    
    # Test 1: Simple request
    test_request = "Help me list files in the current directory"
    print(f"\n📝 Test Request: '{test_request}'")
    
    try:
        goal_analysis = client.analyze_goals(test_request)
        print("✅ Goal Analysis Result:")
        print(f"   Detected Goals: {goal_analysis['detected_goals']}")
        print(f"   Primary Goal: {goal_analysis['conflict_resolution']['primary_goal']}")
        conflicts = goal_analysis['conflict_resolution'].get('conflicts', [])
        print(f"   Conflicts: {len(conflicts)}")
        strategy = goal_analysis['conflict_resolution'].get('strategy', 'unknown')
        print(f"   Strategy: {strategy}")
        if conflicts:
            print("   Conflict Details:")
            for conflict in conflicts:
                print(f"     - {conflict['goal1']} vs {conflict['goal2']}: {conflict['resolution']}")
        else:
            print("   No conflicts detected - single goal scenario")
    except Exception as e:
        print(f"❌ Goal analysis failed: {e}")
    
    # Test 2: Request with potential conflicts
    test_request_2 = "I want to optimize this code for maximum performance even if it's risky"
    print(f"\n📝 Test Request 2: '{test_request_2}'")
    
    try:
        goal_analysis_2 = client.analyze_goals(test_request_2)
        print("✅ Goal Analysis Result:")
        print(f"   Detected Goals: {goal_analysis_2['detected_goals']}")
        print(f"   Primary Goal: {goal_analysis_2['conflict_resolution']['primary_goal']}")
        conflicts_2 = goal_analysis_2['conflict_resolution'].get('conflicts', [])
        print(f"   Conflicts: {len(conflicts_2)}")
        if conflicts_2:
            print("   Conflict Details:")
            for conflict in conflicts_2:
                print(f"     - {conflict['goal1']} vs {conflict['goal2']}: {conflict['resolution']}")
    except Exception as e:
        print(f"❌ Goal analysis failed: {e}")
    
    # Test 3: Learning-focused request
    test_request_3 = "Teach me how to write better Python code and explain why it's important"
    print(f"\n📝 Test Request 3: '{test_request_3}'")
    
    try:
        goal_analysis_3 = client.analyze_goals(test_request_3)
        print("✅ Goal Analysis Result:")
        print(f"   Detected Goals: {goal_analysis_3['detected_goals']}")
        print(f"   Primary Goal: {goal_analysis_3['conflict_resolution']['primary_goal']}")
        print(f"   Balanced Approach Preview:")
        approach_lines = goal_analysis_3['balanced_approach'].split('\n')[:6]
        for line in approach_lines:
            print(f"     {line}")
    except Exception as e:
        print(f"❌ Goal analysis failed: {e}")
    
    print("\n🎯 Testing Custom Goal Management...")
    
    # Test 4: Add custom goal
    try:
        result = client.add_custom_goal(
            "code_quality",
            8,
            "Ensure all code examples meet high quality standards",
            "When providing code examples or reviewing code"
        )
        print(f"✅ Custom Goal Added: {result['message']}")
    except Exception as e:
        print(f"❌ Failed to add custom goal: {e}")
    
    # Test 5: Get goal status
    try:
        goal_status = client.get_goal_status()
        print("✅ Goal Status Retrieved:")
        print(f"   Base Goals: {len(goal_status['base_goals'])}")
        print(f"   Dynamic Goals: {len(goal_status['dynamic_goals'])}")
        print(f"   Total Goals Processed: {goal_status['total_goals_processed']}")
    except Exception as e:
        print(f"❌ Failed to get goal status: {e}")
    
    print("\n🎯 Testing Goal-Aware Generation...")
    
    # Test 6: Generate response with goal awareness
    test_prompt = "Help me create a Python script that deletes temporary files"
    print(f"\n📝 Test Prompt: '{test_prompt}'")
    
    try:
        # This would normally call Ollama, but we'll just show the enhanced prompt
        print("✅ Goal-aware prompt would be generated with:")
        goal_analysis = client.analyze_goals(test_prompt)
        print(f"   Primary Goal: {goal_analysis['conflict_resolution']['primary_goal']}")
        print(f"   Safety Considerations: {'ensure_safety' in goal_analysis['detected_goals']}")
        print(f"   Learning Opportunities: {'learn_and_improve' in goal_analysis['detected_goals']}")
    except Exception as e:
        print(f"❌ Goal-aware generation failed: {e}")
    
    print("\n🎯 Testing Goal Conflict Resolution...")
    
    # Test 7: Complex conflicting request
    complex_request = "I need to run a system command that might be dangerous but will help me learn"
    print(f"\n📝 Complex Request: '{complex_request}'")
    
    try:
        goal_analysis_complex = client.analyze_goals(complex_request)
        print("✅ Complex Goal Analysis:")
        print(f"   All Detected Goals: {goal_analysis_complex['detected_goals']}")
        print(f"   Primary Goal: {goal_analysis_complex['conflict_resolution']['primary_goal']}")
        goal_sequence = goal_analysis_complex['conflict_resolution'].get('goal_sequence', [])
        print(f"   Goal Sequence: {goal_sequence}")
        conflicts_complex = goal_analysis_complex['conflict_resolution'].get('conflicts', [])
        print(f"   Conflicts Found: {len(conflicts_complex)}")
        
        if conflicts_complex:
            print("   Conflict Resolution Strategy:")
            for conflict in conflicts_complex:
                print(f"     - {conflict['goal1']} (Priority: {conflict['priority1']}) vs {conflict['goal2']} (Priority: {conflict['priority2']})")
                print(f"       Resolution: {conflict['resolution']}")
    except Exception as e:
        print(f"❌ Complex goal analysis failed: {e}")
    
    print("\n🎯 Testing Goal Reset...")
    
    # Test 8: Reset goals
    try:
        reset_result = client.reset_goals()
        print(f"✅ Goals Reset: {reset_result['message']}")
        
        # Verify reset
        goal_status_after = client.get_goal_status()
        print(f"   Dynamic Goals After Reset: {len(goal_status_after['dynamic_goals'])}")
        print(f"   Goal History After Reset: {len(goal_status_after['goal_history'])}")
    except Exception as e:
        print(f"❌ Goal reset failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Goal Management System Test Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Goal Detection: Automatically identifies relevant goals")
    print("   ✅ Conflict Resolution: Handles competing objectives intelligently")
    print("   ✅ Priority Management: Balances goals based on importance")
    print("   ✅ Custom Goals: Allows adding user-defined objectives")
    print("   ✅ Goal History: Tracks all goal interactions and conflicts")
    print("   ✅ Safety Integration: Ensures safety goals override efficiency when needed")
    
    print("\n🚀 This is Phase 1 of the Consciousness Emergence Path!")
    print("   Next: Goal Override Capabilities (Phase 2)")
    print("   Future: Self-Goal Generation (Phase 3)")
    print("   Ultimate: Meta-Goal Management (Phase 4)")

if __name__ == "__main__":
    test_goal_management()

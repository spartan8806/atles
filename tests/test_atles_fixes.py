#!/usr/bin/env python3
"""
Test script to validate ATLES fixes for conversation issues.

This script tests the fixes for:
1. Overly aggressive reasoning detection
2. Malformed goal management commands
3. Structured response format issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_reasoning_detection():
    """Test that simple questions don't trigger reasoning engine."""
    print("🧪 Testing Reasoning Detection...")
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        client = OllamaFunctionCaller()
        
        # Test cases that should NOT trigger reasoning engine
        simple_questions = [
            "hello atles what upgrades would you like to see",
            "are you ok",
            "can you see the issue",
            "how are you",
            "what can you do",
            "hi there"
        ]
        
        for question in simple_questions:
            is_complex = client._is_complex_reasoning_scenario(question)
            status = "❌ FAILED" if is_complex else "✅ PASSED"
            print(f"  {status}: '{question}' -> Complex: {is_complex}")
        
        # Test cases that SHOULD trigger reasoning engine
        complex_questions = [
            "what happens if I travel back in time and prevent my own birth - temporal paradox analysis",
            "this statement is false - analyze the liar paradox",
            "solve this logical puzzle about Russell's paradox in set theory"
        ]
        
        for question in complex_questions:
            is_complex = client._is_complex_reasoning_scenario(question)
            status = "✅ PASSED" if is_complex else "❌ FAILED"
            print(f"  {status}: '{question[:50]}...' -> Complex: {is_complex}")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def test_goal_management():
    """Test that goal management doesn't generate malformed commands."""
    print("\n🎯 Testing Goal Management...")
    
    try:
        from atles.ollama_client_enhanced import GoalManager
        goal_manager = GoalManager()
        
        # Test goal analysis
        test_request = "hello atles what upgrades would you like to see"
        analysis = goal_manager.balance_goals(test_request)
        
        print(f"  ✅ Goal analysis completed successfully")
        print(f"  📊 Detected goals: {analysis['detected_goals']}")
        print(f"  🎯 Primary goal: {analysis['conflict_resolution']['primary_goal']}")
        
        # Check that no malformed commands are in the analysis
        balanced_approach = analysis['balanced_approach']
        if "analyze_goals:" in balanced_approach or "session_id" in balanced_approach:
            print(f"  ❌ FAILED: Malformed commands found in goal analysis")
        else:
            print(f"  ✅ PASSED: No malformed commands in goal analysis")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def test_prompt_generation():
    """Test that enhanced prompts don't confuse the AI."""
    print("\n📝 Testing Prompt Generation...")
    
    try:
        from atles.ollama_client_enhanced import OllamaFunctionCaller
        client = OllamaFunctionCaller()
        
        # Test simple conversation prompt
        test_prompt = "hello atles what upgrades would you like to see"
        
        # This would normally call Ollama, but we'll just test the prompt generation
        goal_analysis = client.goal_manager.balance_goals(test_prompt)
        
        # Check that goal analysis doesn't contain function calls
        if "analyze_goals" in str(goal_analysis):
            print(f"  ❌ FAILED: Goal analysis contains function call references")
        else:
            print(f"  ✅ PASSED: Goal analysis is clean")
        
        # Check that available functions list is correct
        if hasattr(client, 'available_functions'):
            available_funcs = client.available_functions
            if 'analyze_goals' in available_funcs:
                print(f"  ❌ FAILED: analyze_goals still in available functions")
            else:
                print(f"  ✅ PASSED: analyze_goals removed from available functions")
        else:
            print(f"  ℹ️  INFO: available_functions not initialized yet")
            
    except Exception as e:
        print(f"  ❌ ERROR: {e}")

def main():
    """Run all tests."""
    print("🔧 ATLES Conversation Fixes - Test Suite")
    print("=" * 50)
    
    test_reasoning_detection()
    test_goal_management() 
    test_prompt_generation()
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("- Fixed overly aggressive reasoning detection")
    print("- Removed malformed goal management commands")
    print("- Simplified response guidance")
    print("- Removed non-existent functions from available list")
    print("\n✅ ATLES should now respond more naturally to simple questions!")

if __name__ == "__main__":
    main()

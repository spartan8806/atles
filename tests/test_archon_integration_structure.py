#!/usr/bin/env python3
"""
Test ATLES Agent Integration Structure

This test verifies that the ATLES agent integration is properly structured
without requiring PydanticAI dependencies.
"""

import sys
import os
from pathlib import Path

def test_atles_agent_file_exists():
    """Test that the ATLES agent file exists and has the right structure."""
    print("🧪 Testing ATLES Agent File Structure")
    print("-" * 40)
    
    atles_agent_path = Path("Archon/python/src/agents/atles_agent.py")
    
    if not atles_agent_path.exists():
        print(f"❌ ATLES agent file not found: {atles_agent_path}")
        return False
    
    print(f"✅ ATLES agent file exists: {atles_agent_path}")
    
    # Check file content
    with open(atles_agent_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_elements = [
        "class ATLESAgent",
        "ATLES BOOTSTRAP PROTOCOL",
        "created by Conner",
        "PRINCIPLE OF EXPLICIT ACTION",
        "PRINCIPLE OF HYPOTHETICAL ENGAGEMENT",
        "PRINCIPLE OF CAPABILITY GROUNDING",
        "_apply_atles_preprocessing",
        "_apply_atles_postprocessing",
        "_is_identity_statement",
        "_is_hypothetical_question",
        "_mentions_external_ai",
        "def create_atles_agent"
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing elements: {missing_elements}")
        return False
    else:
        print("✅ All required elements present in ATLES agent")
        return True

def test_server_registration():
    """Test that the server.py file is properly updated."""
    print("\n🧪 Testing Server Registration")
    print("-" * 40)
    
    server_path = Path("Archon/python/src/agents/server.py")
    
    if not server_path.exists():
        print(f"❌ Server file not found: {server_path}")
        return False
    
    with open(server_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_elements = [
        "from .atles_agent import ATLESAgent",
        '"atles": ATLESAgent,'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing server registration elements: {missing_elements}")
        return False
    else:
        print("✅ ATLES agent properly registered in server")
        return True

def test_init_file_update():
    """Test that the __init__.py file is properly updated."""
    print("\n🧪 Testing __init__.py Update")
    print("-" * 40)
    
    init_path = Path("Archon/python/src/agents/__init__.py")
    
    if not init_path.exists():
        print(f"❌ __init__.py file not found: {init_path}")
        return False
    
    with open(init_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_elements = [
        "from .atles_agent import ATLESAgent",
        '"ATLESAgent"'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing __init__.py elements: {missing_elements}")
        return False
    else:
        print("✅ ATLES agent properly exported in __init__.py")
        return True

def test_bootstrap_protocol_content():
    """Test that the bootstrap protocol contains the right content."""
    print("\n🧪 Testing Bootstrap Protocol Content")
    print("-" * 40)
    
    atles_agent_path = Path("Archon/python/src/agents/atles_agent.py")
    
    with open(atles_agent_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the system prompt
    start_marker = 'return """ATLES BOOTSTRAP PROTOCOL'
    end_marker = '"""'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Bootstrap protocol not found")
        return False
    
    # Find the end of the system prompt
    start_idx += len('return """')
    end_idx = content.find('"""', start_idx)
    
    if end_idx == -1:
        print("❌ Bootstrap protocol end not found")
        return False
    
    system_prompt = content[start_idx:end_idx]
    
    # Check for key identity and capability elements
    identity_elements = [
        "You are ATLES",
        "created by Conner",
        "The user you are talking to is Conner",
        "offline-first system",
        "cannot communicate with external AI systems",
        "Gemini, Claude, ChatGPT"
    ]
    
    capability_elements = [
        "PRINCIPLE OF EXPLICIT ACTION",
        "PRINCIPLE OF HYPOTHETICAL ENGAGEMENT", 
        "PRINCIPLE OF CAPABILITY GROUNDING",
        "what do you want to do",
        "engage creatively"
    ]
    
    all_elements = identity_elements + capability_elements
    missing_elements = []
    
    for element in all_elements:
        if element not in system_prompt:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing bootstrap protocol elements: {missing_elements}")
        return False
    else:
        print("✅ Bootstrap protocol contains all required elements")
        print(f"✅ System prompt length: {len(system_prompt)} characters")
        return True

def test_capability_grounding_logic():
    """Test that capability grounding logic is properly implemented."""
    print("\n🧪 Testing Capability Grounding Logic")
    print("-" * 40)
    
    atles_agent_path = Path("Archon/python/src/agents/atles_agent.py")
    
    with open(atles_agent_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    grounding_elements = [
        "_generate_grounded_alternative",
        "cannot actually communicate with Gemini",
        "offline-first system",
        "hallucination_indicators",
        "ask gemini",
        "contact claude",
        "_is_confusing_constitutional_response"
    ]
    
    missing_elements = []
    for element in grounding_elements:
        if element not in content:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing capability grounding elements: {missing_elements}")
        return False
    else:
        print("✅ Capability grounding logic properly implemented")
        return True

def run_structure_test():
    """Run all structure tests."""
    print("🚀 ATLES Agent Integration Structure Test")
    print("=" * 60)
    
    tests = [
        ("ATLES Agent File Structure", test_atles_agent_file_exists),
        ("Server Registration", test_server_registration),
        ("__init__.py Update", test_init_file_update),
        ("Bootstrap Protocol Content", test_bootstrap_protocol_content),
        ("Capability Grounding Logic", test_capability_grounding_logic)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 STRUCTURE TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} structure tests passed")
    
    if passed == total:
        print("🎉 ALL STRUCTURE TESTS PASSED!")
        print("\n📋 Verified Structure:")
        print("✅ ATLES Agent file properly created with all required methods")
        print("✅ Bootstrap protocol contains identity and capability awareness")
        print("✅ Capability grounding logic implemented to prevent hallucinations")
        print("✅ Agent properly registered in Archon server")
        print("✅ Agent properly exported in module")
        print("\n💡 The ATLES agent integration is structurally complete!")
        print("\n🔧 Next Steps:")
        print("1. Start the Archon system with the new ATLES agent")
        print("2. Test the exact conversation scenarios that previously failed")
        print("3. Verify identity recognition and capability grounding work in practice")
        return True
    else:
        print(f"⚠️ {total - passed} structure tests failed.")
        return False

if __name__ == "__main__":
    success = run_structure_test()
    sys.exit(0 if success else 1)

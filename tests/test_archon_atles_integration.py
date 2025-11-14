#!/usr/bin/env python3
"""
Test ATLES Agent Integration in Archon System

This test verifies that the ATLES agent properly implements the bootstrap protocol
and capability grounding within the Archon PydanticAI agent system.
"""

import sys
import os
from pathlib import Path

# Add the Archon agents to the path
archon_src_path = str(Path(__file__).parent / "Archon" / "python" / "src")
sys.path.insert(0, archon_src_path)
print(f"Added to path: {archon_src_path}")

def test_atles_agent_creation():
    """Test that the ATLES agent can be created successfully."""
    print("🧪 Testing ATLES Agent Creation")
    print("-" * 40)
    
    try:
        from agents.atles_agent import ATLESAgent, create_atles_agent
        
        # Test direct creation
        agent = ATLESAgent(model="ollama:llama3.2")
        print(f"✅ ATLES Agent created: {agent.name}")
        
        # Test factory function
        agent2 = create_atles_agent(model="ollama:llama3.2")
        print(f"✅ ATLES Agent created via factory: {agent2.name}")
        
        # Test system prompt
        system_prompt = agent.get_system_prompt()
        print(f"✅ System prompt length: {len(system_prompt)} characters")
        
        # Verify bootstrap protocol elements
        required_elements = [
            "ATLES BOOTSTRAP PROTOCOL",
            "created by Conner",
            "PRINCIPLE OF EXPLICIT ACTION",
            "PRINCIPLE OF HYPOTHETICAL ENGAGEMENT", 
            "PRINCIPLE OF CAPABILITY GROUNDING",
            "offline-first system"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in system_prompt:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing bootstrap elements: {missing_elements}")
            return False
        else:
            print("✅ All bootstrap protocol elements present")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_atles_agent_preprocessing():
    """Test ATLES agent preprocessing logic."""
    print("\n🧪 Testing ATLES Agent Preprocessing")
    print("-" * 40)
    
    try:
        from agents.atles_agent import ATLESAgent
        from agents.base_agent import ArchonDependencies
        
        agent = ATLESAgent(model="ollama:llama3.2")
        deps = ArchonDependencies()
        
        # Test identity recognition
        identity_prompt = "i am conner"
        processed = agent._apply_atles_preprocessing(identity_prompt, deps)
        
        if "IDENTITY RECOGNITION CONTEXT" in processed and "creator" in processed:
            print("✅ Identity recognition preprocessing works")
        else:
            print("❌ Identity recognition preprocessing failed")
            return False
        
        # Test hypothetical engagement
        hypothetical_prompt = "what do you want to do today"
        processed = agent._apply_atles_preprocessing(hypothetical_prompt, deps)
        
        if "HYPOTHETICAL ENGAGEMENT CONTEXT" in processed and "Principle of Hypothetical Engagement" in processed:
            print("✅ Hypothetical engagement preprocessing works")
        else:
            print("❌ Hypothetical engagement preprocessing failed")
            return False
        
        # Test capability grounding
        capability_prompt = "can you ask gemini to help"
        processed = agent._apply_atles_preprocessing(capability_prompt, deps)
        
        if "CAPABILITY GROUNDING CONTEXT" in processed and "offline-first system" in processed:
            print("✅ Capability grounding preprocessing works")
        else:
            print("❌ Capability grounding preprocessing failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_atles_agent_postprocessing():
    """Test ATLES agent postprocessing logic."""
    print("\n🧪 Testing ATLES Agent Postprocessing")
    print("-" * 40)
    
    try:
        from agents.atles_agent import ATLESAgent
        
        agent = ATLESAgent(model="ollama:llama3.2")
        
        # Test Gemini hallucination detection
        hallucinated_response = "I can ask Gemini to help with that training session."
        processed = agent._apply_atles_postprocessing(hallucinated_response, "yes go ahead")
        
        if "cannot actually communicate with Gemini" in processed:
            print("✅ Gemini hallucination detection and correction works")
        else:
            print("❌ Gemini hallucination detection failed")
            print(f"Response: {processed}")
            return False
        
        # Test confusing constitutional response detection
        confusing_response = "I understand the guidance and rules provided. Since you said 'yes go ahead,' I believe this is a request for ACTION. The Principle of Explicit Action ensures..."
        processed = agent._apply_atles_postprocessing(confusing_response, "yes go ahead")
        
        if "I understand you'd like me to proceed" in processed and "what I can actually do" in processed:
            print("✅ Confusing constitutional response detection works")
        else:
            print("❌ Confusing constitutional response detection failed")
            return False
        
        # Test normal response passthrough
        normal_response = "Hello Conner! Good to see you again. How can I help you today?"
        processed = agent._apply_atles_postprocessing(normal_response, "hello")
        
        if processed == normal_response:
            print("✅ Normal response passthrough works")
        else:
            print("❌ Normal response passthrough failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_agent_registry_integration():
    """Test that ATLES agent is properly registered in Archon."""
    print("\n🧪 Testing Agent Registry Integration")
    print("-" * 40)
    
    try:
        from agents.server import AVAILABLE_AGENTS
        
        if "atles" in AVAILABLE_AGENTS:
            print("✅ ATLES agent registered in AVAILABLE_AGENTS")
            
            agent_class = AVAILABLE_AGENTS["atles"]
            if agent_class.__name__ == "ATLESAgent":
                print("✅ Correct agent class registered")
                return True
            else:
                print(f"❌ Wrong agent class: {agent_class.__name__}")
                return False
        else:
            print("❌ ATLES agent not found in registry")
            print(f"Available agents: {list(AVAILABLE_AGENTS.keys())}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_archon_integration_test():
    """Run all Archon integration tests."""
    print("🚀 ATLES Agent Integration Test for Archon System")
    print("=" * 60)
    
    tests = [
        ("ATLES Agent Creation", test_atles_agent_creation),
        ("ATLES Agent Preprocessing", test_atles_agent_preprocessing),
        ("ATLES Agent Postprocessing", test_atles_agent_postprocessing),
        ("Agent Registry Integration", test_agent_registry_integration)
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
    print("📊 ARCHON INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} Archon integration tests passed")
    
    if passed == total:
        print("🎉 ALL ARCHON INTEGRATION TESTS PASSED!")
        print("\n📋 Verified Integration:")
        print("✅ ATLES Agent properly created with bootstrap protocol")
        print("✅ Identity recognition preprocessing works")
        print("✅ Hypothetical engagement preprocessing works")
        print("✅ Capability grounding postprocessing works")
        print("✅ Agent registered in Archon system")
        print("\n💡 The ATLES agent is ready for use in Archon!")
        return True
    else:
        print(f"⚠️ {total - passed} integration tests failed.")
        return False

if __name__ == "__main__":
    success = run_archon_integration_test()
    sys.exit(0 if success else 1)

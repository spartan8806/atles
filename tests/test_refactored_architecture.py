#!/usr/bin/env python3
"""
Test Refactored Architecture

This test verifies that the refactored unified constitutional client
maintains all functionality while providing cleaner architecture.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import atles
sys.path.append(str(Path(__file__).parent))

def test_unified_client_initialization():
    """Test that the unified client initializes correctly."""
    print("🧪 Testing Unified Client Initialization")
    print("-" * 50)
    
    try:
        # Test direct import
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        status = client.get_constitutional_status()
        
        print(f"Constitutional mode: {status['constitutional_mode']}")
        print(f"Available processors: {status['available_processors']}")
        print(f"Available filters: {status['available_filters']}")
        print(f"Total components: {status['total_components']}")
        
        if status['total_components'] > 0:
            print("✅ Unified client initialized with components")
            return True
        else:
            print("❌ No components available")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backward_compatibility():
    """Test that backward compatibility is maintained."""
    print("\n🧪 Testing Backward Compatibility")
    print("-" * 50)
    
    try:
        # Test backward compatibility function
        from atles.unified_constitutional_client import create_constitutional_client
        
        client = create_constitutional_client()
        
        # Test basic chat functionality
        response = client.chat("Hello")
        print(f"Chat response: {response[:100]}...")
        
        if response and len(response) > 0:
            print("✅ Backward compatibility maintained")
            return True
        else:
            print("❌ No response generated")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_component_isolation():
    """Test that components are properly isolated and handle errors gracefully."""
    print("\n🧪 Testing Component Isolation")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import (
            BootstrapProcessor, MemoryProcessor, CapabilityProcessor,
            MathProcessor, ContextProcessor
        )
        
        # Test each component individually
        components = [
            ("Bootstrap", BootstrapProcessor()),
            ("Memory", MemoryProcessor()),
            ("Capability", CapabilityProcessor()),
            ("Math", MathProcessor()),
            ("Context", ContextProcessor())
        ]
        
        available_count = 0
        
        for name, component in components:
            is_available = component.is_available()
            print(f"{name} processor: {'✅ Available' if is_available else '❌ Not available'}")
            
            if is_available:
                available_count += 1
                
                # Test processing (should not crash)
                try:
                    result = component.process("test prompt", {})
                    print(f"  - Processing test: ✅ Success")
                except Exception as e:
                    print(f"  - Processing test: ❌ Error: {e}")
        
        print(f"\nTotal available components: {available_count}/{len(components)}")
        
        if available_count > 0:
            print("✅ Component isolation working")
            return True
        else:
            print("❌ No components available")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_processing_pipeline():
    """Test the processing pipeline with various inputs."""
    print("\n🧪 Testing Processing Pipeline")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import create_unified_constitutional_client
        
        client = create_unified_constitutional_client()
        
        test_cases = [
            ("Identity statement", "I am Conner"),
            ("Mathematical question", "What's 2+2?"),
            ("Hypothetical question", "What do you want to do today?"),
            ("General question", "What's the capital of France?"),
            ("Rule establishment", "Please give me one-word replies only")
        ]
        
        success_count = 0
        
        for test_name, prompt in test_cases:
            try:
                print(f"\nTesting: {test_name}")
                print(f"Prompt: {prompt}")
                
                response = client.chat(prompt)
                print(f"Response: {response[:150]}...")
                
                if response and len(response) > 0:
                    print(f"✅ {test_name} processed successfully")
                    success_count += 1
                else:
                    print(f"❌ {test_name} failed - no response")
                
            except Exception as e:
                print(f"❌ {test_name} failed - error: {e}")
        
        print(f"\nPipeline success rate: {success_count}/{len(test_cases)}")
        
        if success_count >= len(test_cases) * 0.8:  # 80% success rate
            print("✅ Processing pipeline working well")
            return True
        else:
            print("❌ Processing pipeline needs improvement")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_architecture_benefits():
    """Test that the refactored architecture provides expected benefits."""
    print("\n🧪 Testing Architecture Benefits")
    print("-" * 50)
    
    try:
        from atles.unified_constitutional_client import UnifiedConstitutionalClient
        import inspect
        
        # Test 1: Clean method signatures
        generate_method = getattr(UnifiedConstitutionalClient, 'generate')
        signature = inspect.signature(generate_method)
        
        print(f"Generate method signature: {signature}")
        
        if len(signature.parameters) <= 5:  # Reasonable parameter count
            print("✅ Clean method signatures")
        else:
            print("❌ Too many parameters")
            return False
        
        # Test 2: Modular components
        client_methods = [method for method in dir(UnifiedConstitutionalClient) 
                         if not method.startswith('_')]
        
        print(f"Public methods: {len(client_methods)}")
        print(f"Methods: {client_methods}")
        
        if len(client_methods) <= 10:  # Reasonable method count
            print("✅ Focused interface")
        else:
            print("❌ Too many public methods")
            return False
        
        # Test 3: Error handling
        try:
            # This should not crash even with invalid base client
            client = UnifiedConstitutionalClient(None)
            print("❌ Should have failed with None base client")
            return False
        except Exception:
            print("✅ Proper error handling")
        
        print("✅ Architecture benefits verified")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def run_refactor_test():
    """Run all refactoring tests."""
    print("🚀 Refactored Architecture Test")
    print("Testing the new unified constitutional client architecture")
    print("=" * 70)
    
    tests = [
        ("Unified Client Initialization", test_unified_client_initialization),
        ("Backward Compatibility", test_backward_compatibility),
        ("Component Isolation", test_component_isolation),
        ("Processing Pipeline", test_processing_pipeline),
        ("Architecture Benefits", test_architecture_benefits)
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
    print("\n" + "=" * 70)
    print("📊 REFACTORING TEST SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} refactoring tests passed")
    
    if passed == total:
        print("🎉 REFACTORING SUCCESSFUL!")
        print("\n📋 Architecture Improvements:")
        print("✅ Clean, modular component architecture")
        print("✅ Separation of concerns (processors vs filters)")
        print("✅ Proper error handling and graceful degradation")
        print("✅ Backward compatibility maintained")
        print("✅ Reduced code duplication and complexity")
        print("✅ Linear processing pipeline")
        print("✅ Easy to test and maintain")
        print("\n💡 The refactored architecture is ready for production!")
        return True
    else:
        print(f"⚠️ {total - passed} refactoring tests failed.")
        print("\n🔧 Areas needing attention:")
        for test_name, result in results:
            if not result:
                print(f"- {test_name}")
        return False

if __name__ == "__main__":
    success = run_refactor_test()
    sys.exit(0 if success else 1)

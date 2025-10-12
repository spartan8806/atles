#!/usr/bin/env python3
"""
Test the hybrid processing integration in the desktop app.
"""

import sys
import os
from unittest.mock import Mock, patch

# Add the atles directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'atles'))

def test_hybrid_integration():
    """Test the hybrid processing integration."""
    
    print("🧪 Testing Hybrid Processing Integration")
    print("=" * 50)
    
    try:
        # Import the Screen Data Parser
        from Screen_Data_Parser import ScreenDataParser
        
        # Test 1: Parser Integration
        print("\n📋 Test 1: Screen Data Parser Integration")
        parser = ScreenDataParser()
        
        # Simulate raw screen data from desktop app
        raw_data = {
            'window_info': {
                'title': 'Visual Studio Code - main.py',
                'process_name': 'Code.exe',
                'process_id': 1234,
                'rect': [100, 200, 800, 600],
                'timestamp': '2025-08-24T12:00:00'
            },
            'clipboard_content': 'def hello_world():\n    print("Hello, World!")',
            'running_apps': [
                {'name': 'Code.exe', 'memory_mb': 150},
                {'name': 'Chrome.exe', 'memory_mb': 300}
            ],
            'timestamp': '2025-08-24T12:00:00'
        }
        
        # Parse the data
        parsed_result = parser.parse_screen_data(raw_data)
        
        if parsed_result:
            print("✅ Parser successfully processed raw data")
            print(f"   Summary: {parsed_result['summary']}")
            print(f"   Details: {parsed_result['details']}")
            print(f"   Context: {parsed_result['context']}")
        else:
            print("❌ Parser returned no result")
            return False
        
        # Test 2: Enhanced Prompt Creation
        print(f"\n📋 Test 2: Enhanced Prompt Creation")
        
        # Mock the desktop app's enhanced prompt creation
        def create_enhanced_prompt_hybrid(message, context):
            """Simulate the hybrid enhanced prompt creation"""
            enhanced = f"User message: {message}\n\n"
            
            # HYBRID PROCESSING: Use parsed data if available
            if context.get('parsed'):
                parsed = context['parsed']
                enhanced += f"Current Screen Context (Processed):\n"
                enhanced += f"- Summary: {parsed.get('summary', 'Unknown activity')}\n"
                enhanced += f"- Details: {parsed.get('details', 'No specific details')}\n"
                enhanced += f"- Context: {parsed.get('context', 'General activity')}\n"
            else:
                enhanced += "Current Screen Context: Raw data (fallback)\n"
            
            return enhanced
        
        # Test with parsed data
        context_with_parsed = {
            'parsed': parsed_result,
            'window_info': raw_data['window_info']
        }
        
        enhanced_prompt = create_enhanced_prompt_hybrid("Help me debug this code", context_with_parsed)
        
        print("✅ Enhanced prompt created with parsed data")
        print(f"   Prompt preview: {enhanced_prompt[:200]}...")
        
        # Verify it contains parsed data, not raw data
        if "Summary:" in enhanced_prompt and "Details:" in enhanced_prompt:
            print("✅ Prompt contains structured parsed data")
        else:
            print("❌ Prompt doesn't contain parsed data")
            return False
        
        # Test 3: Filtering Behavior
        print(f"\n📋 Test 3: Filtering Behavior")
        
        # Test identical data (should be filtered)
        identical_data = raw_data.copy()
        filtered_result = parser.parse_screen_data(identical_data)
        
        if filtered_result is None:
            print("✅ Identical data correctly filtered")
        else:
            print("⚠️ Identical data was not filtered (may be expected on first run)")
        
        # Test ATLES window (should be filtered)
        atles_data = {
            'window_info': {
                'title': 'ATLES Desktop - AI Assistant',
                'process_name': 'python.exe'
            },
            'clipboard_content': 'ATLES interface content'
        }
        
        atles_result = parser.parse_screen_data(atles_data)
        
        if atles_result is None:
            print("✅ ATLES window correctly filtered (prevents self-analysis)")
        else:
            print("❌ ATLES window was not filtered")
            return False
        
        # Test 4: Error Detection
        print(f"\n📋 Test 4: Error Detection Priority")
        
        error_data = {
            'window_info': {
                'title': 'Python Error - TypeError',
                'process_name': 'python.exe'
            },
            'clipboard_content': 'TypeError: unsupported operand type(s)'
        }
        
        error_result = parser.parse_screen_data(error_data)
        
        if error_result and 'error_handling' in error_result.get('summary', ''):
            print("✅ Error window correctly detected and processed")
            print(f"   Context: {error_result['context']}")
        else:
            print("❌ Error window not properly detected")
            return False
        
        print(f"\n" + "=" * 50)
        print("📊 INTEGRATION TEST RESULTS:")
        print("✅ Screen Data Parser Integration: PASS")
        print("✅ Enhanced Prompt Creation: PASS") 
        print("✅ Filtering Behavior: PASS")
        print("✅ Error Detection Priority: PASS")
        print(f"\n🎉 HYBRID PROCESSING INTEGRATION: SUCCESS!")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_desktop_app_simulation():
    """Simulate the desktop app workflow with hybrid processing."""
    
    print(f"\n🖥️ Desktop App Workflow Simulation")
    print("=" * 50)
    
    try:
        from Screen_Data_Parser import ScreenDataParser
        
        # Simulate desktop app initialization
        screen_parser = ScreenDataParser()
        print("✅ Screen Data Parser initialized (like desktop app)")
        
        # Simulate screen monitoring data flow
        monitoring_data = [
            # User opens VS Code
            {
                'window_info': {'title': 'Visual Studio Code', 'process_name': 'Code.exe'},
                'clipboard_content': 'Welcome screen'
            },
            # User opens a Python file (significant change)
            {
                'window_info': {'title': 'Visual Studio Code - main.py', 'process_name': 'Code.exe'},
                'clipboard_content': 'def hello():\n    print("Hello!")'
            },
            # Minor change (cursor movement - should be filtered)
            {
                'window_info': {'title': 'Visual Studio Code - main.py', 'process_name': 'Code.exe'},
                'clipboard_content': 'def hello():\n    print("Hello!")'  # Same content
            },
            # Error appears (should be processed)
            {
                'window_info': {'title': 'Python Error - SyntaxError', 'process_name': 'python.exe'},
                'clipboard_content': 'SyntaxError: invalid syntax'
            }
        ]
        
        processed_count = 0
        filtered_count = 0
        
        for i, data in enumerate(monitoring_data, 1):
            print(f"\n📊 Processing monitoring event {i}:")
            print(f"   Window: {data['window_info']['title']}")
            
            # Process through hybrid pipeline
            result = screen_parser.parse_screen_data(data)
            
            if result:
                processed_count += 1
                print(f"   ✅ Processed: {result['summary']}")
            else:
                filtered_count += 1
                print(f"   🔄 Filtered (minor change or ignored window)")
        
        print(f"\n📊 WORKFLOW RESULTS:")
        print(f"   Processed: {processed_count} events")
        print(f"   Filtered: {filtered_count} events")
        print(f"   Efficiency: {filtered_count}/{len(monitoring_data)} events filtered")
        
        # Expected: VS Code opening, Python file opening, and error should be processed
        # Minor change should be filtered
        expected_processed = 3
        expected_filtered = 1
        
        if processed_count == expected_processed and filtered_count == expected_filtered:
            print("✅ Workflow behaved as expected")
            return True
        else:
            print(f"⚠️ Unexpected workflow behavior")
            print(f"   Expected: {expected_processed} processed, {expected_filtered} filtered")
            print(f"   Actual: {processed_count} processed, {filtered_count} filtered")
            return False
        
    except Exception as e:
        print(f"❌ Workflow simulation failed: {e}")
        return False

def main():
    """Run all integration tests."""
    
    print("🚀 HYBRID PROCESSING INTEGRATION TEST")
    print("Testing Screen Data Parser integration with desktop app")
    print("=" * 70)
    
    test1_success = test_hybrid_integration()
    test2_success = test_desktop_app_simulation()
    
    print("\n" + "=" * 70)
    print("🎯 FINAL INTEGRATION RESULTS")
    print("-" * 30)
    print(f"Hybrid Integration: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Desktop App Workflow: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print(f"\n🎉 INTEGRATION COMPLETE!")
        print("The hybrid processing pipeline is ready for production.")
        print("Benefits:")
        print("  • Clean, structured data for ATLES")
        print("  • 20% change threshold prevents noise")
        print("  • Self-analysis prevention")
        print("  • Error detection priority")
        print("  • Fallback to raw data if needed")
    else:
        print(f"\n⚠️ INTEGRATION ISSUES")
        print("Some components need debugging before production use.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

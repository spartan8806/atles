#!/usr/bin/env python3
"""
Test Screen Data Parser with persistent instance (realistic usage).
"""

from Screen_Data_Parser import ScreenDataParser

def test_with_persistence():
    """Test with a single parser instance (realistic scenario)."""
    print("🧪 Screen Data Parser - Persistence Test")
    print("=" * 50)
    
    # Create ONE parser instance (like in real usage)
    parser = ScreenDataParser()
    
    # Test 1: First content
    print("\n📝 Test 1: User opens VS Code")
    data1 = {
        'window_info': {
            'title': 'Visual Studio Code',
            'process_name': 'Code.exe'
        },
        'visible_content': 'Welcome to VS Code',
        'ui_elements': [{'name': 'New File'}]
    }
    
    result1 = parser.parse_screen_data(data1)
    print(f"Result: {'✅ Processed' if result1 else '❌ Not processed'}")
    if result1:
        print(f"   {result1['summary']}")
    
    # Test 2: Identical content (should be filtered)
    print("\n🔄 Test 2: Identical content (cursor blink)")
    data2 = data1.copy()  # Exact same data
    
    result2 = parser.parse_screen_data(data2)
    print(f"Result: {'⚠️ Processed (bad)' if result2 else '✅ Correctly filtered'}")
    
    # Test 3: Minor change (should be filtered)
    print("\n🔄 Test 3: Very minor change")
    data3 = {
        'window_info': {
            'title': 'Visual Studio Code',  # Same
            'process_name': 'Code.exe'
        },
        'visible_content': 'Welcome to VS Code ',  # Added one space
        'ui_elements': [{'name': 'New File'}]
    }
    
    result3 = parser.parse_screen_data(data3)
    print(f"Result: {'⚠️ Processed (bad)' if result3 else '✅ Correctly filtered'}")
    
    # Test 4: Significant change (should be processed)
    print("\n📄 Test 4: Significant change (new file opened)")
    data4 = {
        'window_info': {
            'title': 'Visual Studio Code - main.py',  # Different title
            'process_name': 'Code.exe'
        },
        'visible_content': 'def hello_world():\n    print("Hello!")',  # Different content
        'ui_elements': [{'name': 'Run'}, {'name': 'Debug'}]  # Different UI
    }
    
    result4 = parser.parse_screen_data(data4)
    print(f"Result: {'✅ Processed' if result4 else '❌ Not processed (bad)'}")
    if result4:
        print(f"   {result4['summary']}")
    
    # Test 5: Error window (should always be processed)
    print("\n🚨 Test 5: Error appears")
    data5 = {
        'window_info': {
            'title': 'Python Error - TypeError',
            'process_name': 'python.exe'
        },
        'visible_content': 'TypeError: unsupported operand',
        'ui_elements': [{'name': 'OK'}]
    }
    
    result5 = parser.parse_screen_data(data5)
    print(f"Result: {'✅ Processed' if result5 else '❌ Not processed (bad)'}")
    if result5:
        print(f"   {result5['summary']}")
        print(f"   Context: {result5['context']}")
    
    print("\n" + "=" * 50)
    print("📊 FINAL TEST RESULTS:")
    print(f"✅ Initial processing: {'PASS' if result1 else 'FAIL'}")
    print(f"✅ Identical filtering: {'PASS' if not result2 else 'FAIL'}")
    print(f"✅ Minor change filtering: {'PASS' if not result3 else 'FAIL'}")
    print(f"✅ Significant change processing: {'PASS' if result4 else 'FAIL'}")
    print(f"✅ Error detection: {'PASS' if result5 else 'FAIL'}")
    
    # Overall assessment
    all_pass = result1 and not result2 and not result3 and result4 and result5
    print(f"\n🎯 OVERALL: {'✅ ALL TESTS PASS' if all_pass else '⚠️ SOME ISSUES REMAIN'}")
    
    return all_pass

if __name__ == "__main__":
    test_with_persistence()

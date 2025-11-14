#!/usr/bin/env python3
"""
Realistic test of Screen Data Parser with sequential data.
"""

from Screen_Data_Parser import ScreenDataParser

def test_realistic_scenario():
    """Test with realistic sequential screen data."""
    print("🧪 Realistic Screen Data Parser Test")
    print("=" * 50)
    
    parser = ScreenDataParser()
    
    # Scenario 1: User opens VS Code
    print("\n📝 Scenario 1: User opens VS Code")
    data1 = {
        'window_info': {
            'title': 'Visual Studio Code',
            'process_name': 'Code.exe'
        },
        'visible_content': 'Welcome to VS Code',
        'ui_elements': [{'name': 'New File'}, {'name': 'Open Folder'}]
    }
    
    result1 = parser.parse_screen_data(data1)
    if result1:
        print(f"✅ Processed: {result1['summary']}")
    else:
        print("❌ Not processed")
    
    # Scenario 2: Minor change (cursor blink) - should be filtered
    print("\n🔄 Scenario 2: Minor change (cursor blink)")
    data2 = {
        'window_info': {
            'title': 'Visual Studio Code',  # Same window
            'process_name': 'Code.exe'
        },
        'visible_content': 'Welcome to VS Code',  # Same content
        'ui_elements': [{'name': 'New File'}, {'name': 'Open Folder'}]  # Same UI
    }
    
    result2 = parser.parse_screen_data(data2)
    if result2:
        print(f"⚠️ Processed (should be filtered): {result2['summary']}")
    else:
        print("✅ Correctly filtered minor change")
    
    # Scenario 3: Significant change (user opens file)
    print("\n📄 Scenario 3: User opens a Python file")
    data3 = {
        'window_info': {
            'title': 'Visual Studio Code - main.py',
            'process_name': 'Code.exe'
        },
        'visible_content': 'def hello_world():\n    print("Hello, World!")',
        'ui_elements': [{'name': 'Run'}, {'name': 'Debug'}, {'name': 'Terminal'}]
    }
    
    result3 = parser.parse_screen_data(data3)
    if result3:
        print(f"✅ Processed: {result3['summary']}")
        print(f"   Details: {result3['details']}")
    else:
        print("❌ Not processed (should be processed)")
    
    # Scenario 4: ATLES window - should be ignored
    print("\n🚫 Scenario 4: ATLES window appears")
    data4 = {
        'window_info': {
            'title': 'ATLES Desktop - AI Assistant',
            'process_name': 'python.exe'
        },
        'visible_content': 'ATLES chat interface'
    }
    
    result4 = parser.parse_screen_data(data4)
    if result4:
        print(f"❌ Processed ATLES window (should be ignored): {result4['summary']}")
    else:
        print("✅ Correctly ignored ATLES window")
    
    # Scenario 5: Error window - should be processed with high priority
    print("\n🚨 Scenario 5: Error window appears")
    data5 = {
        'window_info': {
            'title': 'Python Error - Traceback',
            'process_name': 'python.exe'
        },
        'visible_content': 'TypeError: unsupported operand type(s)',
        'ui_elements': [{'name': 'OK'}, {'name': 'Details'}]
    }
    
    result5 = parser.parse_screen_data(data5)
    if result5:
        print(f"✅ Processed error: {result5['summary']}")
        print(f"   Context: {result5['context']}")
    else:
        print("❌ Error not processed")
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"✅ VS Code opening: {'Processed' if result1 else 'Not processed'}")
    print(f"✅ Minor change filtering: {'Working' if not result2 else 'Not working'}")
    print(f"✅ Significant change: {'Processed' if result3 else 'Not processed'}")
    print(f"✅ ATLES filtering: {'Working' if not result4 else 'Not working'}")
    print(f"✅ Error detection: {'Processed' if result5 else 'Not processed'}")

if __name__ == "__main__":
    test_realistic_scenario()

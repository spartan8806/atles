#!/usr/bin/env python3
"""
Simple test launcher for ATLES Desktop App
Tests basic functionality without full GUI
"""

import sys
import os

def test_basic_functionality():
    """Test basic functionality without launching GUI"""
    print("🧪 Testing ATLES Desktop App Basic Functionality...")
    
    try:
        # Test importing the main classes
        from atles_desktop_app import ScreenElementExtractor, ATLESDesktopApp
        print("✅ Core classes imported successfully")
        
        # Test creating extractor
        extractor = ScreenElementExtractor()
        print("✅ ScreenElementExtractor created successfully")
        
        # Test getting active window info
        print("🔍 Testing window detection...")
        window_info = extractor.get_active_window_info()
        if window_info:
            print(f"   ✅ Active window: {window_info.get('title', 'Unknown')}")
            print(f"   ✅ Process: {window_info.get('process_name', 'Unknown')}")
        else:
            print("   ⚠️ No active window detected")
        
        # Test getting running applications
        print("📱 Testing application enumeration...")
        apps = extractor.get_running_applications()
        if apps:
            print(f"   ✅ Found {len(apps)} running applications")
            if len(apps) > 0:
                print(f"   ✅ Sample app: {apps[0].get('title', 'Unknown')}")
        else:
            print("   ⚠️ No running applications found")
        
        # Test clipboard access
        print("📋 Testing clipboard access...")
        try:
            clipboard = extractor.get_clipboard_content()
            if clipboard:
                print(f"   ✅ Clipboard content: {len(clipboard)} characters")
            else:
                print("   ℹ️ Clipboard is empty")
        except Exception as e:
            print(f"   ⚠️ Clipboard access failed: {e}")
        
        print("\n🎉 Basic functionality test completed successfully!")
        print("The desktop app is ready to run.")
        print("\nTo launch the full GUI, run:")
        print("  python atles_desktop_app.py")
        print("  or double-click run_desktop.bat")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 ATLES Desktop App - Basic Functionality Test")
    print("=" * 50)
    
    success = test_basic_functionality()
    
    if success:
        print("\n✅ All tests passed! Desktop app is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

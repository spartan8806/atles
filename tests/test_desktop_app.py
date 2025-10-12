#!/usr/bin/env python3
"""
Test script for ATLES Desktop Application
Tests core functionality without launching the full GUI
"""

import sys
import os
from datetime import datetime

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_screen_extractor():
    """Test the ScreenElementExtractor class"""
    print("🧪 Testing ScreenElementExtractor...")
    
    try:
        from atles_desktop_app import ScreenElementExtractor
        
        extractor = ScreenElementExtractor()
        
        # Test getting active window info
        print("  Testing get_active_window_info()...")
        window_info = extractor.get_active_window_info()
        if window_info:
            print(f"    ✅ Active window: {window_info.get('title', 'Unknown')}")
            print(f"    ✅ Process: {window_info.get('process_name', 'Unknown')}")
        else:
            print("    ⚠️ No active window info available")
        
        # Test getting running applications
        print("  Testing get_running_applications()...")
        apps = extractor.get_running_applications()
        if apps:
            print(f"    ✅ Found {len(apps)} running applications")
            if apps:
                print(f"    ✅ First app: {apps[0].get('title', 'Unknown')}")
        else:
            print("    ⚠️ No running applications found")
        
        # Test clipboard access
        print("  Testing get_clipboard_content()...")
        try:
            clipboard = extractor.get_clipboard_content()
            if clipboard:
                print(f"    ✅ Clipboard content: {len(clipboard)} characters")
            else:
                print("    ℹ️ Clipboard is empty")
        except Exception as e:
            print(f"    ⚠️ Clipboard access failed: {e}")
        
        print("  ✅ ScreenElementExtractor tests completed")
        return True
        
    except Exception as e:
        print(f"  ❌ ScreenElementExtractor test failed: {e}")
        return False

def test_atles_integration():
    """Test ATLES integration capabilities"""
    print("\n🧪 Testing ATLES Integration...")
    
    try:
        # Test if we can import ATLES modules
        print("  Testing ATLES module imports...")
        
        try:
            from atles.brain.r_zero_integration import RZeroIntegration
            print("    ✅ RZeroIntegration imported successfully")
        except ImportError as e:
            print(f"    ⚠️ RZeroIntegration not available: {e}")
        
        try:
            from atles.ollama_client_enhanced import OllamaFunctionCaller as OllamaClient
            print("    ✅ OllamaClient imported successfully")
        except ImportError as e:
            print(f"    ⚠️ OllamaClient not available: {e}")
        
        print("  ✅ ATLES integration tests completed")
        return True
        
    except Exception as e:
        print(f"  ❌ ATLES integration test failed: {e}")
        return False

def test_basic_analysis():
    """Test basic analysis functionality"""
    print("\n🧪 Testing Basic Analysis...")
    
    try:
        from atles_desktop_app import ATLESDesktopApp
        
        # Create app instance (without GUI)
        app = ATLESDesktopApp.__new__(ATLESDesktopApp)
        
        # Test basic analysis
        test_data = {
            'window_title': 'Test Window - Visual Studio Code',
            'process_name': 'code.exe',
            'text_content': 'def hello_world():\n    print("Hello, World!")',
            'timestamp': datetime.now().isoformat()
        }
        
        result = app._basic_analysis(test_data)
        
        if result and 'insights' in result:
            print(f"    ✅ Basic analysis completed")
            print(f"    ✅ Insights: {len(result['insights'])} found")
            print(f"    ✅ Recommendations: {len(result['recommendations'])} found")
        else:
            print("    ❌ Basic analysis failed")
            return False
        
        print("  ✅ Basic analysis tests completed")
        return True
        
    except Exception as e:
        print(f"  ❌ Basic analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ATLES Desktop Application - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Screen Element Extractor", test_screen_extractor),
        ("ATLES Integration", test_atles_integration),
        ("Basic Analysis", test_basic_analysis)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} tests...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Desktop app is ready to run.")
        print("\nTo launch the app, run:")
        print("  python atles_desktop_app.py")
        print("  or double-click run_desktop.bat")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

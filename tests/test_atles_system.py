#!/usr/bin/env python3
"""
ATLES System Test Script
Quick test to verify all components are working after the move.
"""

import os
import sys
import json
from pathlib import Path

def test_file_paths():
    """Test that all critical files exist"""
    print("🔍 Testing ATLES System Files...")
    print("=" * 50)
    
    critical_files = [
        "atles_desktop_pyqt.py",
        "atles_autonomous_v6_ui_evolution.py", 
        "atles_code_studio.py",
        "atles_config.json",
        "atles_settings.json",
        "start_atles_silent.vbs",
        "start_atles_server_auto.bat",
        "run_desktop_pyqt.bat"
    ]
    
    all_good = True
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_good = False
    
    return all_good

def test_configuration():
    """Test configuration files"""
    print("\n🔧 Testing Configuration...")
    print("=" * 50)
    
    # Test atles_config.json
    try:
        with open("atles_config.json", 'r') as f:
            config = json.load(f)
        print("✅ atles_config.json - Valid JSON")
    except Exception as e:
        print(f"❌ atles_config.json - Error: {e}")
        return False
    
    # Test atles_settings.json  
    try:
        with open("atles_settings.json", 'r') as f:
            settings = json.load(f)
        print("✅ atles_settings.json - Valid JSON")
    except Exception as e:
        print(f"❌ atles_settings.json - Error: {e}")
        return False
    
    return True

def test_python_imports():
    """Test critical Python imports"""
    print("\n🐍 Testing Python Imports...")
    print("=" * 50)
    
    imports_to_test = [
        ("PyQt6", "PyQt6.QtWidgets"),
        ("psutil", "psutil"),
        ("PIL", "PIL.Image"),
        ("win32gui", "win32gui"),
        ("requests", "requests")
    ]
    
    all_good = True
    for name, import_path in imports_to_test:
        try:
            __import__(import_path)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_good = False
    
    return all_good

def test_atles_modules():
    """Test ATLES core modules"""
    print("\n🧠 Testing ATLES Modules...")
    print("=" * 50)
    
    atles_modules = [
        "atles.ollama_client_enhanced",
        "atles.constitutional_client", 
        "atles.intelligent_model_router",
        "atles.episodic_semantic_memory"
    ]
    
    all_good = True
    for module in atles_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - Error: {e}")
            all_good = False
    
    return all_good

def test_vbs_file():
    """Test VBScript file content"""
    print("\n📜 Testing VBScript File...")
    print("=" * 50)
    
    try:
        with open("start_atles_silent.vbs", 'r') as f:
            content = f.read()
        
        if "D:\\portfolio\\atles" in content:
            print("✅ VBScript has correct path")
            return True
        else:
            print("❌ VBScript has incorrect path")
            print(f"Content: {content}")
            return False
    except Exception as e:
        print(f"❌ Error reading VBScript: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 ATLES System Test - Post Move Verification")
    print("=" * 60)
    
    tests = [
        ("File Paths", test_file_paths),
        ("Configuration", test_configuration), 
        ("Python Imports", test_python_imports),
        ("ATLES Modules", test_atles_modules),
        ("VBScript File", test_vbs_file)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - Exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ATLES system is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

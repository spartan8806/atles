#!/usr/bin/env python3
"""
Test Proactive Analysis System

This script launches the ATLES Desktop app with the proactive self-analysis system
enabled. It will:
1. Start the ATLES Desktop PyQt app
2. Monitor for 35+ minutes of inactivity
3. Trigger self-analysis
4. Log all analysis activities to the terminal

Usage:
    python test_proactive_analysis.py
"""

import os
import sys
import time
from datetime import datetime

def print_banner():
    """Print test banner"""
    print("\n" + "="*60)
    print("🧠 ATLES PROACTIVE SELF-ANALYSIS TEST")
    print("="*60)
    print("📝 This test will:")
    print("  • Launch the ATLES Desktop PyQt app")
    print("  • Monitor for 35+ minutes of inactivity")
    print("  • Trigger self-analysis when idle")
    print("  • Display detailed debug output")
    print("\n⏱️  The system should analyze conversations after about 35 minutes")
    print("   of inactivity. You can leave it running overnight to collect")
    print("   multiple analysis sessions.")
    print("\n⚠️  Press Ctrl+C in this terminal to exit")
    print("="*60 + "\n")

def main():
    """Main test function"""
    print_banner()
    
    print(f"🕒 Test started at: {datetime.now().isoformat()}")
    print("🚀 Launching ATLES Desktop PyQt...")
    
    # Launch the desktop app (don't capture output to allow it to print directly)
    try:
        # Use the current Python interpreter to run the desktop app
        from subprocess import Popen
        process = Popen([sys.executable, "atles_desktop_pyqt.py"])
        
        print("✅ ATLES Desktop PyQt launched")
        print("\n📊 ANALYSIS LOG:")
        print("-"*60)
        
        # Keep the script running to maintain terminal output
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n❌ Test interrupted by user")
            process.terminate()
            print("🛑 ATLES Desktop PyQt terminated")
    
    except Exception as e:
        print(f"❌ Error launching ATLES Desktop PyQt: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

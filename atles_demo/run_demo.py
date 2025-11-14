#!/usr/bin/env python3
"""
ATLES Demo Runner
================
Proper Python script to run the ATLES demo from within the ATLES system.
"""

import sys
import os
from pathlib import Path

# Add the ATLES root directory to Python path
atles_root = Path(__file__).parent.parent
sys.path.insert(0, str(atles_root))

def main():
    """Run the ATLES demo server"""
    print("🧠 Starting ATLES Demo Server")
    print("=" * 40)
    
    try:
        # Import the demo server
        from atles_demo.atles_demo_server import app
        
        print("✅ Demo server imported successfully")
        print("🌐 Starting Flask server...")
        print("📱 Demo will be available at: http://localhost:5000")
        print("🔑 Demo codes: DEMO001, DEMO002, DEMO003")
        print("⏹️  Press Ctrl+C to stop")
        print()
        
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            use_reloader=False
        )
        
    except ImportError as e:
        print(f"❌ Error importing demo server: {e}")
        print("💡 Make sure you're running from the ATLES directory")
        return 1
    except Exception as e:
        print(f"❌ Error starting demo server: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

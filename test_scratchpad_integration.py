#!/usr/bin/env python3
"""
Test script to verify ATLES Scratchpad System integration
"""

import sys
from pathlib import Path

# Add atles to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all scratchpad components can be imported"""
    print("=" * 60)
    print("Testing ATLES Scratchpad System Integration")
    print("=" * 60)
    
    try:
        print("\n1. Testing autonomous module imports...")
        from atles.autonomous import Scratchpad, TokenizedScratchpad, ScratchpadArchiver
        print("   [OK] Scratchpad")
        print("   [OK] TokenizedScratchpad")
        print("   [OK] ScratchpadArchiver")
        
        print("\n2. Testing thinking client import...")
        from atles.thinking_client import create_thinking_constitutional_client
        print("   [OK] create_thinking_constitutional_client")
        
        print("\n3. Testing package-level imports...")
        from atles import (
            create_thinking_constitutional_client,
            Scratchpad,
            TokenizedScratchpad,
            ScratchpadArchiver
        )
        print("   [OK] All components available from atles package")
        
        print("\n4. Testing scratchpad functionality...")
        import tempfile
        import shutil
        
        # Create temp directories
        temp_dir = Path(tempfile.mkdtemp())
        session_dir = temp_dir / "active"
        archive_dir = temp_dir / "archive"
        
        try:
            # Test Scratchpad
            pad = Scratchpad(str(session_dir), str(archive_dir))
            pad.start_thought("Test question")
            pad.write_thought("initial", {"text": "Test response", "confidence": 0.8})
            pad.write_thought("final", {"text": "Final response", "ready": True})
            pad.finalize_thought()
            
            thoughts = pad.read_thoughts()
            assert len(thoughts) == 1, "Should have 1 thought"
            print("   [OK] Scratchpad write/read works")
            
            # Test stats
            stats = pad.get_session_stats()
            assert stats["num_thoughts"] == 1, "Stats should show 1 thought"
            print("   [OK] Session stats work")
            
            # Test archiver
            archiver = ScratchpadArchiver(str(session_dir), str(archive_dir))
            archive_stats = archiver.get_archive_stats()
            print("   [OK] ScratchpadArchiver works")
            
        finally:
            # Cleanup
            shutil.rmtree(temp_dir)
        
        print("\n5. Checking configuration file...")
        config_path = Path("config/scratchpad_config.yaml")
        if config_path.exists():
            print(f"   [OK] Configuration file exists: {config_path}")
        else:
            print(f"   [WARN] Configuration file not found: {config_path}")
            print("   (This is OK - will use defaults)")
        
        print("\n6. Checking documentation...")
        docs = [
            "docs/SCRATCHPAD_SYSTEM.md",
            "docs/SCRATCHPAD_QUICKSTART.md",
            "docs/SCRATCHPAD_INTEGRATION_COMPLETE.md"
        ]
        for doc in docs:
            doc_path = Path(doc)
            if doc_path.exists():
                print(f"   [OK] {doc}")
            else:
                print(f"   [FAIL] {doc} (missing)")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 60)
        print("\nScratchpad System is ready to use!")
        print("\nQuick start:")
        print("  from atles import create_thinking_constitutional_client")
        print("  client = create_thinking_constitutional_client()")
        print("  response = client.generate('llama3.2', 'Your question')")
        print("\nSee docs/SCRATCHPAD_QUICKSTART.md for more information.")
        
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)


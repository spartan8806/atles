#!/usr/bin/env python3
"""
ATLES Startup Script with Background Learning Daemon

This script:
1. Starts the learning daemon in the background
2. Launches the ATLES chat interface
3. Monitors the chat session
4. When chat closes, triggers memory processing and model fine-tuning
5. Creates detailed logs of all learning activities
"""

import os
import sys
import time
import json
import signal
import atexit
import logging
from pathlib import Path
from datetime import datetime

# Add atles to path
sys.path.insert(0, str(Path(__file__).parent))

from atles.autonomous_learning_daemon import (
    start_daemon, 
    stop_daemon, 
    mark_session_complete,
    get_daemon
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Track current session
current_session = {
    "session_id": None,
    "start_time": None,
    "messages": []
}


def cleanup_on_exit():
    """Cleanup when script exits"""
    logger.info("🧹 Cleanup on exit...")
    
    # If there's an active session, mark it complete
    if current_session["session_id"]:
        logger.info(f"Marking session {current_session['session_id']} as complete")
        mark_session_complete(current_session["session_id"], current_session)
    
    # Keep daemon running (it stays in background)
    logger.info("✅ Cleanup complete (daemon remains running)")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Shutting down ATLES...")
    cleanup_on_exit()
    sys.exit(0)


def start_session():
    """Start a new chat session"""
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    current_session["session_id"] = session_id
    current_session["start_time"] = datetime.now().isoformat()
    current_session["messages"] = []
    
    logger.info(f"📝 Started new session: {session_id}")
    return session_id


def log_message(role: str, content: str):
    """Log a message to current session"""
    if current_session["session_id"]:
        current_session["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })


def print_banner():
    """Print startup banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     🧠 ATLES - Advanced AI with Continuous Learning      ║
║                                                           ║
║     ✨ Background Learning Daemon: ACTIVE                ║
║     🔄 Auto Memory Processing: ENABLED                   ║
║     📈 Model Fine-Tuning: ENABLED                        ║
║     📝 Detailed Logging: ENABLED                         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_daemon_status():
    """Print current daemon status"""
    daemon = get_daemon()
    status = daemon.get_status()
    
    print("\n" + "="*60)
    print("📊 Learning Daemon Status")
    print("="*60)
    print(f"   🕐 Uptime: {status['uptime_hours']:.2f} hours")
    print(f"   ✅ Sessions processed: {status['stats']['sessions_processed']}")
    print(f"   💬 Total messages: {status['stats']['total_messages']}")
    print(f"   🧠 Memory items: {status['stats']['total_memory_items']}")
    print(f"   🎓 Model fine-tunes: {status['stats']['total_fine_tunes']}")
    print(f"   📋 Queue: {status['sessions_in_queue']} sessions")
    print("="*60 + "\n")


def main():
    """Main execution"""
    # Register cleanup and signal handlers
    atexit.register(cleanup_on_exit)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_banner()
    
    # Step 1: Start learning daemon
    logger.info("🚀 Starting Learning Daemon...")
    daemon = start_daemon()
    time.sleep(1)  # Give daemon time to initialize
    logger.info("✅ Learning Daemon started successfully")
    
    # Step 2: Show daemon status
    print_daemon_status()
    
    # Step 3: Start chat session
    session_id = start_session()
    
    # Step 4: Launch chat interface
    print("🎯 Launching ATLES Chat Interface...")
    print("   Options:")
    print("   1. Streamlit Chat (Full UI)")
    print("   2. Simple Console Chat")
    print("   3. Just keep daemon running")
    print()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "1":
        # Launch Streamlit
        logger.info("Launching Streamlit chat...")
        import subprocess
        
        try:
            # Run streamlit and wait for it to close
            subprocess.run(["streamlit", "run", "streamlit_chat.py"])
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logger.error(f"Error launching Streamlit: {e}")
    
    elif choice == "2":
        # Simple console chat
        logger.info("Starting console chat...")
        print("\n" + "="*60)
        print("💬 ATLES Console Chat")
        print("="*60)
        print("Type your messages below (type 'exit' to quit)\n")
        
        try:
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nATLES: Goodbye! Processing this session for learning...\n")
                    break
                
                if not user_input:
                    continue
                
                # Log user message
                log_message("user", user_input)
                
                # Simple echo response (replace with actual ATLES call)
                response = f"I heard: {user_input}"
                log_message("assistant", response)
                
                print(f"ATLES: {response}\n")
                
        except KeyboardInterrupt:
            print("\n")
    
    elif choice == "3":
        # Just run daemon
        logger.info("Running daemon only...")
        print("\n📊 Daemon is running in background")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                time.sleep(60)
                print_daemon_status()
        except KeyboardInterrupt:
            pass
    
    else:
        print("Invalid choice")
        return
    
    # Step 5: Session complete - cleanup will trigger processing
    logger.info("Chat session ended")
    logger.info(f"Session had {len(current_session['messages'])} messages")
    
    # Show final status
    time.sleep(2)  # Give daemon time to process
    print("\n")
    print_daemon_status()
    
    print("✨ Session processing initiated!")
    print("📝 Check logs: atles_memory/learning_daemon/logs/")
    print("🚀 Daemon continues running for next session")
    print()


if __name__ == "__main__":
    main()


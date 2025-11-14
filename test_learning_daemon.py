#!/usr/bin/env python3
"""
Test script for ATLES Autonomous Learning Daemon

This script demonstrates the complete learning pipeline:
1. Start daemon
2. Simulate chat sessions
3. Process sessions
4. View learning results
"""

import time
import json
from pathlib import Path
from datetime import datetime

from atles.autonomous_learning_daemon import (
    start_daemon,
    stop_daemon,
    get_daemon,
    mark_session_complete
)
from atles.daemon_integration import SessionTracker


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def simulate_chat_session(session_num: int, message_count: int = 6):
    """Simulate a chat session"""
    print(f"📝 Simulating chat session {session_num}...")
    
    tracker = SessionTracker(auto_start_daemon=False)
    session_id = tracker.start_session(f"test_session_{session_num:03d}")
    
    # Simulate conversation
    conversations = [
        ("What is Python?", "Python is a high-level programming language known for its simplicity..."),
        ("Show me an example", "Here's a simple example: print('Hello, World!')"),
        ("How do I create a function?", "To create a function in Python, use the 'def' keyword..."),
        ("What about classes?", "Classes in Python are defined using the 'class' keyword..."),
        ("Can you explain decorators?", "Decorators are a way to modify function behavior..."),
        ("What's the difference between list and tuple?", "Lists are mutable while tuples are immutable..."),
    ]
    
    for i, (question, answer) in enumerate(conversations[:message_count]):
        print(f"   User: {question[:50]}...")
        tracker.log_message("user", question)
        
        print(f"   ATLES: {answer[:50]}...")
        tracker.log_message("assistant", answer)
        
        if i < message_count - 1:
            time.sleep(0.5)  # Simulate typing delay
    
    # Add metadata
    tracker.set_metadata("platform", "test_script")
    tracker.set_metadata("quality_rating", 5)
    
    print(f"✅ Session {session_id} complete ({tracker.get_message_count()} messages)\n")
    
    # End session (triggers learning)
    tracker.end_session()
    
    return session_id


def wait_for_processing(max_wait: int = 30):
    """Wait for daemon to process sessions"""
    print("⏳ Waiting for daemon to process sessions...")
    
    start_time = time.time()
    daemon = get_daemon()
    
    while time.time() - start_time < max_wait:
        status = daemon.get_status()
        queue_size = status['sessions_in_queue']
        
        if queue_size == 0:
            print("✅ All sessions processed!\n")
            return True
        
        print(f"   Queue: {queue_size} sessions remaining...")
        time.sleep(2)
    
    print("⚠️  Timeout waiting for processing\n")
    return False


def show_daemon_status():
    """Show current daemon status"""
    daemon = get_daemon()
    status = daemon.get_status()
    
    print("📊 Daemon Status:")
    print(f"   Running: {'✅ Yes' if status['is_running'] else '❌ No'}")
    print(f"   Uptime: {status['uptime_hours']:.2f} hours")
    print(f"   Queue: {status['sessions_in_queue']} sessions")
    print()
    
    stats = status['stats']
    print("📈 Learning Statistics:")
    print(f"   Sessions Processed: {stats['sessions_processed']}")
    print(f"   Total Messages: {stats['total_messages']}")
    print(f"   Memory Items: {stats['total_memory_items']}")
    print(f"   Fine-Tunes: {stats['total_fine_tunes']}")
    print()


def show_session_logs():
    """Show recent session logs"""
    logs_dir = Path("atles_memory/learning_daemon/logs")
    
    if not logs_dir.exists():
        print("⚠️  No logs directory found\n")
        return
    
    # Find session logs
    session_logs = sorted(logs_dir.glob("session_log_*.json"))
    
    if not session_logs:
        print("⚠️  No session logs found\n")
        return
    
    print(f"📝 Recent Session Logs ({len(session_logs)} total):\n")
    
    # Show last 3 logs
    for log_file in session_logs[-3:]:
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
            
            print(f"   Session: {log_data['session_id']}")
            print(f"   Messages: {log_data['messages_count']}")
            print(f"   Memory Items: {log_data['memory_items_created']}")
            print(f"   Fine-Tuned: {'✅ Yes' if log_data['fine_tune_applied'] else '❌ No'}")
            
            if log_data['fine_tune_loss']:
                print(f"   Loss: {log_data['fine_tune_loss']:.3f}")
            
            if log_data['improvements']:
                print(f"   Improvements:")
                for improvement in log_data['improvements'][:3]:
                    print(f"      • {improvement}")
            
            print()
            
        except Exception as e:
            print(f"   ⚠️  Error reading {log_file.name}: {e}\n")


def show_master_log():
    """Show master log summary"""
    master_log = Path("atles_memory/learning_daemon/logs/master_log.jsonl")
    
    if not master_log.exists():
        print("⚠️  No master log found\n")
        return
    
    sessions = []
    with open(master_log, 'r') as f:
        for line in f:
            try:
                sessions.append(json.loads(line))
            except:
                pass
    
    if not sessions:
        print("⚠️  No sessions in master log\n")
        return
    
    print("📊 Master Log Summary:\n")
    print(f"   Total Sessions: {len(sessions)}")
    
    total_messages = sum(s.get('messages_count', 0) for s in sessions)
    print(f"   Total Messages: {total_messages}")
    
    avg_messages = total_messages / len(sessions) if sessions else 0
    print(f"   Avg Messages/Session: {avg_messages:.1f}")
    
    fine_tuned = sum(1 for s in sessions if s.get('fine_tune_applied', False))
    print(f"   Fine-Tuned Sessions: {fine_tuned}")
    
    if fine_tuned > 0:
        fine_tune_rate = (fine_tuned / len(sessions)) * 100
        print(f"   Fine-Tune Rate: {fine_tune_rate:.1f}%")
    
    total_memory = sum(s.get('memory_items_created', 0) for s in sessions)
    print(f"   Total Memory Items: {total_memory}")
    
    print()


def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("  🧪 ATLES Learning Daemon - Test Suite")
    print("="*60)
    print("\nThis test will:")
    print("  1. Start the learning daemon")
    print("  2. Simulate 3 chat sessions")
    print("  3. Process sessions automatically")
    print("  4. Show learning results")
    print()
    
    input("Press Enter to start...")
    
    # Step 1: Start daemon
    print_header("Step 1: Starting Learning Daemon")
    daemon = start_daemon()
    time.sleep(2)
    show_daemon_status()
    
    # Step 2: Simulate sessions
    print_header("Step 2: Simulating Chat Sessions")
    
    session_ids = []
    for i in range(1, 4):
        session_id = simulate_chat_session(i, message_count=6)
        session_ids.append(session_id)
        time.sleep(1)
    
    print(f"✅ Created {len(session_ids)} test sessions\n")
    
    # Step 3: Wait for processing
    print_header("Step 3: Processing Sessions")
    wait_for_processing(max_wait=30)
    
    # Give extra time for file writing
    time.sleep(2)
    
    # Step 4: Show results
    print_header("Step 4: Learning Results")
    
    # Show daemon status
    show_daemon_status()
    
    # Show session logs
    show_session_logs()
    
    # Show master log
    show_master_log()
    
    # Final summary
    print_header("✅ Test Complete!")
    
    print("Check these locations for detailed logs:")
    print(f"  • Daemon log: atles_memory/learning_daemon/daemon.log")
    print(f"  • Session logs: atles_memory/learning_daemon/logs/")
    print(f"  • Statistics: atles_memory/learning_daemon/logs/daemon_stats.json")
    print()
    
    # Ask to stop daemon
    choice = input("Stop daemon? (y/N): ").strip().lower()
    if choice == 'y':
        print("\n🛑 Stopping daemon...")
        stop_daemon()
        print("✅ Daemon stopped\n")
    else:
        print("\n📍 Daemon continues running in background")
        print("   Stop it with: python -c \"from atles.autonomous_learning_daemon import stop_daemon; stop_daemon()\"")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        print("🛑 Stopping daemon...")
        stop_daemon()
        print("✅ Cleanup complete\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("🛑 Stopping daemon...")
        stop_daemon()
        print("✅ Cleanup complete\n")
        raise


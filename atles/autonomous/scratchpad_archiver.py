"""
ATLES Scratchpad Archiver
Daily archival and key thought extraction for analysis and debugging
(Note: Unlike ATLAS, ATLES uses external models so no training data preparation)
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScratchpadArchiver:
    """
    Archives scratchpad sessions daily and extracts key thoughts
    for analysis, debugging, and future improvements
    """
    
    def __init__(self, 
                 session_dir: str = "scratchpad/active",
                 archive_dir: str = "scratchpad/archive",
                 keep_days: int = 30):
        """
        Initialize archiver
        
        Args:
            session_dir: Directory with active sessions
            archive_dir: Directory for archived sessions
            keep_days: How many days of archives to keep
        """
        self.session_dir = Path(session_dir)
        self.archive_dir = Path(archive_dir)
        self.keep_days = keep_days
        
        # Create directories
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def archive_daily(self, date: str = None) -> Dict:
        """
        Archive all sessions from yesterday (or specified date)
        
        Args:
            date: Date to archive (YYYY-MM-DD), defaults to yesterday
        
        Returns:
            Dictionary with archive statistics
        """
        if date is None:
            # Default to yesterday
            yesterday = datetime.now() - timedelta(days=1)
            date = yesterday.strftime("%Y-%m-%d")
        
        logger.info(f"Starting daily archive for {date}")
        
        # Create date directory
        date_dir = self.archive_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Find all session files from that date
        sessions_archived = 0
        total_thoughts = 0
        key_thoughts_found = 0
        
        if self.session_dir.exists():
            for session_file in self.session_dir.glob("session_*.jsonl"):
                # Check if file is from the target date
                file_date = self._get_file_date(session_file)
                if file_date == date:
                    # Move to archive
                    dest = date_dir / session_file.name
                    shutil.move(str(session_file), str(dest))
                    
                    # Count thoughts
                    thoughts = self._read_session(dest)
                    total_thoughts += len(thoughts)
                    key_thoughts_found += sum(1 for t in thoughts if t.get("is_key_thought", False))
                    
                    sessions_archived += 1
        
        # Extract key thoughts for analysis
        key_thoughts = self.extract_key_thoughts(date_dir)
        
        # Save key thoughts
        if key_thoughts:
            key_file = date_dir / "key_thoughts.jsonl"
            with open(key_file, 'w', encoding='utf-8') as f:
                for thought in key_thoughts:
                    f.write(json.dumps(thought) + '\n')
            
            # Also create a human-readable summary
            self._create_summary(date_dir, key_thoughts)
        
        stats = {
            "date": date,
            "sessions_archived": sessions_archived,
            "total_thoughts": total_thoughts,
            "key_thoughts": len(key_thoughts),
            "archive_dir": str(date_dir)
        }
        
        logger.info(f"Archive complete: {stats}")
        
        # Cleanup old archives
        self._cleanup_old_archives()
        
        return stats
    
    def extract_key_thoughts(self, date_dir: Path) -> List[Dict]:
        """
        Extract key thoughts from all sessions in a date directory
        
        Args:
            date_dir: Directory containing session files
        
        Returns:
            List of key thoughts with metadata
        """
        key_thoughts = []
        
        for session_file in date_dir.glob("session_*.jsonl"):
            thoughts = self._read_session(session_file)
            
            for thought in thoughts:
                if thought.get("is_key_thought", False):
                    # Extract relevant information
                    key_thought = {
                        "timestamp": thought["timestamp"],
                        "user_input": thought["user_input"],
                        "reason": thought.get("key_reason", "unknown"),
                        "stages": thought["thought_stages"],
                        "metadata": thought["metadata"],
                        "source_session": session_file.name
                    }
                    
                    # Analyze thought type
                    key_thought["type"] = self._classify_key_thought(key_thought)
                    
                    key_thoughts.append(key_thought)
        
        logger.info(f"Extracted {len(key_thoughts)} key thoughts from {date_dir.name}")
        
        return key_thoughts
    
    def _classify_key_thought(self, thought: Dict) -> str:
        """
        Classify the type of key thought
        
        Args:
            thought: Key thought dictionary
        
        Returns:
            Classification string
        """
        reason = thought.get("reason", "unknown")
        
        # Map reasons to types
        type_mapping = {
            "user_correction": "correction",
            "self_catch": "self_improvement",
            "novel_solution": "innovation",
            "error_recovery": "resilience",
            "unexpected_success": "discovery"
        }
        
        return type_mapping.get(reason, "general")
    
    def _create_summary(self, date_dir: Path, key_thoughts: List[Dict]):
        """
        Create a human-readable summary of key thoughts
        
        Args:
            date_dir: Directory to save summary
            key_thoughts: List of key thoughts
        """
        summary_file = date_dir / "summary.txt"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"ATLES Scratchpad Summary - {date_dir.name}\n")
            f.write("=" * 60 + "\n\n")
            
            # Group by type
            by_type = {}
            for thought in key_thoughts:
                t = thought.get("type", "general")
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(thought)
            
            f.write(f"Total Key Thoughts: {len(key_thoughts)}\n\n")
            
            for thought_type, thoughts in sorted(by_type.items()):
                f.write(f"\n{thought_type.upper()} ({len(thoughts)} thoughts)\n")
                f.write("-" * 60 + "\n")
                
                for i, thought in enumerate(thoughts[:10], 1):  # Limit to top 10
                    f.write(f"\n{i}. {thought['user_input'][:80]}...\n")
                    f.write(f"   Reason: {thought.get('reason', 'unknown')}\n")
                    f.write(f"   Time: {thought.get('timestamp', 'N/A')}\n")
                
                if len(thoughts) > 10:
                    f.write(f"\n   ... and {len(thoughts) - 10} more\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("This data can be used for:\n")
            f.write("- Understanding ATLES's thinking patterns\n")
            f.write("- Debugging response generation issues\n")
            f.write("- Identifying areas for system improvements\n")
            f.write("- Analyzing user interaction patterns\n")
        
        logger.info(f"Created summary: {summary_file}")
    
    def _read_session(self, session_file: Path) -> List[Dict]:
        """Read all thoughts from a session file"""
        thoughts = []
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        thoughts.append(json.loads(line))
        return thoughts
    
    def _get_file_date(self, session_file: Path) -> str:
        """Extract date from session filename"""
        # Format: session_YYYYMMDD_HHMMSS.jsonl
        name = session_file.stem  # Remove .jsonl
        parts = name.split('_')
        if len(parts) >= 2:
            date_str = parts[1]  # YYYYMMDD
            if len(date_str) == 8:
                return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return ""
    
    def _cleanup_old_archives(self):
        """Remove archives older than keep_days"""
        cutoff_date = datetime.now() - timedelta(days=self.keep_days)
        
        for date_dir in self.archive_dir.iterdir():
            if date_dir.is_dir() and date_dir.name != "":
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                    if dir_date < cutoff_date:
                        shutil.rmtree(date_dir)
                        logger.info(f"Removed old archive: {date_dir.name}")
                except ValueError:
                    # Not a date directory, skip
                    pass
    
    def get_archive_stats(self) -> Dict:
        """
        Get statistics about all archives
        
        Returns:
            Dictionary with archive statistics
        """
        total_dates = 0
        total_sessions = 0
        total_key_thoughts = 0
        
        for date_dir in self.archive_dir.iterdir():
            if date_dir.is_dir():
                total_dates += 1
                
                # Count sessions
                sessions = list(date_dir.glob("session_*.jsonl"))
                total_sessions += len(sessions)
                
                # Count key thoughts
                key_file = date_dir / "key_thoughts.jsonl"
                if key_file.exists():
                    key_thoughts = self._read_session(key_file)
                    total_key_thoughts += len(key_thoughts)
        
        return {
            "total_dates": total_dates,
            "total_sessions": total_sessions,
            "total_key_thoughts": total_key_thoughts,
            "keep_days": self.keep_days
        }


if __name__ == "__main__":
    # Test archiver
    archiver = ScratchpadArchiver()
    stats = archiver.get_archive_stats()
    print(f"Archive stats: {stats}")


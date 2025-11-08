"""
ATLES Scratchpad System
Internal thinking workspace for multi-stage response generation
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scratchpad:
    """
    Internal scratchpad for ATLES to think before responding.
    Stores thoughts in AI-optimized structured format (JSON with token IDs).
    User never sees this - it's purely internal to the AI.
    """
    
    def __init__(self, session_dir: str = "scratchpad/active", archive_dir: str = "scratchpad/archive"):
        """
        Initialize scratchpad system
        
        Args:
            session_dir: Directory for active session thoughts
            archive_dir: Directory for archived thoughts
        """
        self.session_dir = Path(session_dir)
        self.archive_dir = Path(archive_dir)
        
        # Create directories
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize session file
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.session_dir / f"session_{self.session_id}.jsonl"
        
        # Current thought being built
        self.current_thought: Optional[Dict] = None
        
        logger.info(f"Scratchpad initialized: {self.session_file}")
    
    def start_thought(self, user_input: str) -> None:
        """
        Start a new thought process for a user input
        
        Args:
            user_input: The user's question/prompt
        """
        self.current_thought = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "thought_stages": {},
            "is_key_thought": False,
            "metadata": {
                "start_time": datetime.now().timestamp()
            }
        }
        logger.debug(f"Started new thought for input: {user_input[:50]}...")
    
    def write_thought(self, stage: str, data: Dict) -> None:
        """
        Write a thought stage to the scratchpad
        
        Args:
            stage: Stage name (initial, critique, revision, final)
            data: Structured data for this stage (tokens, text, issues, etc.)
        """
        if self.current_thought is None:
            logger.warning("No active thought - call start_thought() first")
            return
        
        self.current_thought["thought_stages"][stage] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        logger.debug(f"Wrote thought stage: {stage}")
    
    def mark_key_thought(self, reason: str) -> None:
        """
        Mark current thought as "key" for Sleep Cycle learning
        
        Args:
            reason: Why this is a key thought (user_correction, self_catch, novel_solution)
        """
        if self.current_thought is not None:
            self.current_thought["is_key_thought"] = True
            self.current_thought["key_reason"] = reason
            logger.info(f"Marked as key thought: {reason}")
    
    def finalize_thought(self) -> None:
        """
        Finalize current thought and write to session file
        """
        if self.current_thought is None:
            return
        
        # Add final metadata
        end_time = datetime.now().timestamp()
        start_time = self.current_thought["metadata"]["start_time"]
        self.current_thought["metadata"]["response_time"] = end_time - start_time
        self.current_thought["metadata"]["num_stages"] = len(self.current_thought["thought_stages"])
        
        # Write to session file (JSONL format - one JSON per line)
        with open(self.session_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(self.current_thought) + '\n')
        
        logger.debug(f"Finalized thought ({self.current_thought['metadata']['response_time']:.2f}s)")
        
        # Clear current thought
        self.current_thought = None
    
    def read_thoughts(self) -> List[Dict]:
        """
        Read all thoughts from current session
        
        Returns:
            List of thought dictionaries
        """
        if not self.session_file.exists():
            return []
        
        thoughts = []
        with open(self.session_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    thoughts.append(json.loads(line))
        
        return thoughts
    
    def get_key_thoughts(self) -> List[Dict]:
        """
        Extract only the key thoughts from current session
        
        Returns:
            List of key thought dictionaries
        """
        all_thoughts = self.read_thoughts()
        return [t for t in all_thoughts if t.get("is_key_thought", False)]
    
    def archive_session(self, date: Optional[str] = None) -> Path:
        """
        Move current session to archive
        
        Args:
            date: Date string (YYYY-MM-DD), defaults to today
        
        Returns:
            Path to archived session file
        """
        if not self.session_file.exists():
            logger.warning("No session file to archive")
            return None
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Create date directory
        date_dir = self.archive_dir / date
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Move session file
        archived_path = date_dir / self.session_file.name
        self.session_file.rename(archived_path)
        
        logger.info(f"Archived session to: {archived_path}")
        
        return archived_path
    
    def get_session_stats(self) -> Dict:
        """
        Get statistics about current session
        
        Returns:
            Dictionary with stats (num_thoughts, key_thoughts, avg_response_time, etc.)
        """
        thoughts = self.read_thoughts()
        
        if not thoughts:
            return {
                "num_thoughts": 0,
                "key_thoughts": 0,
                "avg_response_time": 0,
                "total_stages": 0
            }
        
        key_thoughts = [t for t in thoughts if t.get("is_key_thought", False)]
        response_times = [t["metadata"]["response_time"] for t in thoughts]
        total_stages = sum(t["metadata"]["num_stages"] for t in thoughts)
        
        return {
            "num_thoughts": len(thoughts),
            "key_thoughts": len(key_thoughts),
            "avg_response_time": sum(response_times) / len(response_times),
            "total_stages": total_stages,
            "avg_stages_per_thought": total_stages / len(thoughts)
        }


class TokenizedScratchpad(Scratchpad):
    """
    Extended scratchpad that stores token IDs alongside text
    More efficient for AI processing
    """
    
    def __init__(self, session_dir: str = "scratchpad/active", 
                 archive_dir: str = "scratchpad/archive",
                 tokenizer=None):
        """
        Initialize tokenized scratchpad
        
        Args:
            session_dir: Directory for active sessions
            archive_dir: Directory for archives
            tokenizer: Tokenizer instance for encoding text to tokens
        """
        super().__init__(session_dir, archive_dir)
        self.tokenizer = tokenizer
    
    def write_thought(self, stage: str, data: Dict) -> None:
        """
        Write thought with automatic tokenization
        
        Args:
            stage: Stage name
            data: Must include 'text' field for tokenization
        """
        # If tokenizer available and text provided, add token IDs
        if self.tokenizer and 'text' in data:
            encoded = self.tokenizer.encode(data['text'])
            data['tokens'] = encoded.ids
            data['token_count'] = len(encoded.ids)
        
        super().write_thought(stage, data)


def test_scratchpad():
    """Test scratchpad functionality"""
    import tempfile
    import shutil
    
    # Create temp directories
    temp_dir = Path(tempfile.mkdtemp())
    session_dir = temp_dir / "active"
    archive_dir = temp_dir / "archive"
    
    try:
        # Initialize scratchpad
        pad = Scratchpad(str(session_dir), str(archive_dir))
        
        # Simulate a thought process
        pad.start_thought("Explain how ATLES works")
        
        pad.write_thought("initial", {
            "text": "ATLES is a comprehensive AI system.",
            "confidence": 0.7
        })
        
        pad.write_thought("critique", {
            "text": "Too vague, needs more detail",
            "issues": ["lacks detail", "no examples"]
        })
        
        pad.write_thought("revision", {
            "text": "ATLES is an advanced AI system with constitutional principles...",
            "improvements": ["added detail", "explained architecture"]
        })
        
        pad.write_thought("final", {
            "text": "ATLES is an advanced AI system...",
            "ready": True
        })
        
        pad.mark_key_thought("self_improvement")
        pad.finalize_thought()
        
        # Read back
        thoughts = pad.read_thoughts()
        print(f"✓ Recorded {len(thoughts)} thoughts")
        
        key = pad.get_key_thoughts()
        print(f"✓ Found {len(key)} key thoughts")
        
        stats = pad.get_session_stats()
        print(f"✓ Stats: {stats}")
        
        # Archive
        archived = pad.archive_session()
        print(f"✓ Archived to: {archived}")
        
        print("\n✓ Scratchpad test passed!")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_scratchpad()


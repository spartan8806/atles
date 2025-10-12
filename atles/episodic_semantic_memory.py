"""
ATLES Episodic & Semantic Memory System

This is the revolutionary upgrade from a single conversation log to an intelligent
memory architecture with three key components:

1. EPISODIC MEMORY: Individual conversation logs (episodes)
2. SEMANTIC INDEX: AI-generated summaries with invoke keys and rankings  
3. CORE MEMORY: Global principles and constitutional knowledge

This system enables ATLES to:
- Store each conversation as a distinct "episode"
- Generate intelligent summaries with searchable invoke keys
- Rank conversations by information quality and depth
- Intelligently retrieve relevant memories based on context
- Scale to thousands of conversations without performance degradation

Architecture Overview:
- atles_memory/episodes/: Individual conversation files (episode_YYYYMMDD_HHMMSS.json)
- atles_memory/semantic_index.json: Master index with summaries and invoke keys
- atles_memory/core_memory.json: Constitutional principles and global knowledge
"""

import json
import logging
import re
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# Import the memory improvements
try:
    from .memory_improvements import (
        MemoryDeduplicator, ContentManager, CacheManager, 
        SemanticSearchEnhancer, RobustErrorHandler
    )
    IMPROVEMENTS_AVAILABLE = True
except ImportError:
    IMPROVEMENTS_AVAILABLE = False
    logger.warning("Memory improvements not available - using basic functionality")

logger = logging.getLogger(__name__)



# EMBEDDED SAFE FILE OPERATIONS

import json
import os
import tempfile
import threading
import platform

# Thread-safe file operations
_file_locks = {}
_global_lock = threading.RLock()

def _get_file_lock(filepath):
    """Get or create a lock for a specific file."""
    with _global_lock:
        if filepath not in _file_locks:
            _file_locks[filepath] = threading.RLock()
        return _file_locks[filepath]

def safe_read_json(filepath, default=None, encoding='utf-8'):
    """Safely read JSON file with locking and error handling."""
    filepath = str(Path(filepath).resolve())
    file_lock = _get_file_lock(filepath)
    
    with file_lock:
        try:
            if not os.path.exists(filepath):
                return default
            
            with open(filepath, 'r', encoding=encoding) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return default

def safe_write_json(filepath, data, encoding='utf-8', create_backup=True):
    """Safely write JSON file with atomic operations and locking."""
    filepath = str(Path(filepath).resolve())
    file_lock = _get_file_lock(filepath)
    
    with file_lock:
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Create backup if file exists
            if create_backup and os.path.exists(filepath):
                backup_path = f"{filepath}.backup"
                try:
                    shutil.copy2(filepath, backup_path)
                except Exception:
                    pass  # Continue without backup
            
            # Write to temporary file first (atomic operation)
            temp_path = f"{filepath}.tmp.{os.getpid()}"
            
            with open(temp_path, 'w', encoding=encoding) as f:
                pass  # Will use safe_write_json instead
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            # Atomic move (rename)
            if platform.system() == "Windows" and os.path.exists(filepath):
                os.remove(filepath)
            
            os.rename(temp_path, filepath)
            return True
            
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
            return False

# END SAFE FILE OPERATIONS

class InformationQuality(Enum):
    """Quality levels for conversation information."""
    TRIVIAL = 1      # Simple greetings, basic questions
    LOW = 2          # General conversation, simple tasks
    MEDIUM = 3       # Moderate complexity, some learning
    HIGH = 4         # Deep discussions, complex problem solving
    EXCEPTIONAL = 5  # Breakthrough insights, major learning


@dataclass
class EpisodicMemory:
    """A single conversation episode."""
    episode_id: str
    session_id: str
    start_time: datetime
    end_time: datetime
    messages: List[Dict[str, Any]]
    participant_count: int
    message_count: int
    duration_minutes: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "episode_id": self.episode_id,
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "messages": self.messages,
            "participant_count": self.participant_count,
            "message_count": self.message_count,
            "duration_minutes": self.duration_minutes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EpisodicMemory':
        """Create from dictionary."""
        return cls(
            episode_id=data["episode_id"],
            session_id=data["session_id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            messages=data["messages"],
            participant_count=data["participant_count"],
            message_count=data["message_count"],
            duration_minutes=data["duration_minutes"]
        )


@dataclass
class SemanticIndex:
    """Semantic index entry for an episode."""
    episode_id: str
    title: str
    summary: str
    invoke_keys: List[str]  # Topics/concepts that can "invoke" this memory
    information_quality: InformationQuality
    learning_value: float  # 0.0 to 1.0 - how much was learned
    complexity_score: float  # 0.0 to 1.0 - technical/conceptual complexity
    emotional_significance: float  # 0.0 to 1.0 - emotional importance
    created_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    
    def get_composite_rank(self) -> float:
        """Calculate composite ranking score."""
        quality_weight = 0.4
        learning_weight = 0.3
        complexity_weight = 0.2
        emotional_weight = 0.1
        
        return (
            (self.information_quality.value / 5.0) * quality_weight +
            self.learning_value * learning_weight +
            self.complexity_score * complexity_weight +
            self.emotional_significance * emotional_weight
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "episode_id": self.episode_id,
            "title": self.title,
            "summary": self.summary,
            "invoke_keys": self.invoke_keys,
            "information_quality": self.information_quality.value,
            "learning_value": self.learning_value,
            "complexity_score": self.complexity_score,
            "emotional_significance": self.emotional_significance,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "access_count": self.access_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SemanticIndex':
        """Create from dictionary."""
        return cls(
            episode_id=data["episode_id"],
            title=data["title"],
            summary=data["summary"],
            invoke_keys=data["invoke_keys"],
            information_quality=InformationQuality(data["information_quality"]),
            learning_value=data["learning_value"],
            complexity_score=data["complexity_score"],
            emotional_significance=data["emotional_significance"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None,
            access_count=data.get("access_count", 0)
        )


@dataclass
class CoreMemoryItem:
    """An item in core memory (constitutional principles, global knowledge)."""
    item_id: str
    category: str  # "constitutional", "preferences", "identity", "capabilities"
    title: str
    content: str
    priority: int  # 1-10, higher = more important
    created_at: datetime
    last_updated: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "item_id": self.item_id,
            "category": self.category,
            "title": self.title,
            "content": self.content,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CoreMemoryItem':
        """Create from dictionary."""
        return cls(
            item_id=data["item_id"],
            category=data["category"],
            title=data["title"],
            content=data["content"],
            priority=data["priority"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_updated=datetime.fromisoformat(data["last_updated"])
        )


class EpisodicSemanticMemory:
    """
    The main episodic and semantic memory system.
    
    This replaces the single conversation log with an intelligent memory architecture
    that can scale to thousands of conversations while maintaining fast retrieval.
    """
    
    def __init__(self, memory_path: str = "atles_memory"):
        self.memory_path = Path(memory_path)
        self.episodes_path = self.memory_path / "episodes"
        self.semantic_index_file = self.memory_path / "semantic_index.json"
        self.core_memory_file = self.memory_path / "core_memory.json"
        
        # Create directory structure
        self.memory_path.mkdir(exist_ok=True)
        self.episodes_path.mkdir(exist_ok=True)
        
        # Initialize memory improvements if available
        if IMPROVEMENTS_AVAILABLE:
            self.deduplicator = MemoryDeduplicator()
            self.content_manager = ContentManager()
            self.cache_manager = CacheManager(max_size=1000, default_ttl=3600)
            self.semantic_enhancer = SemanticSearchEnhancer()
            self.error_handler = RobustErrorHandler(str(self.memory_path / "backups"))
            # Initialize caches for improved version too
            self._semantic_index_cache: Dict[str, SemanticIndex] = {}
            self._core_memory_cache: Dict[str, CoreMemoryItem] = {}
            self._cache_last_updated = None
            logger.info("Memory improvements initialized")
        else:
            # Fallback to basic caches
            self._semantic_index_cache: Dict[str, SemanticIndex] = {}
            self._core_memory_cache: Dict[str, CoreMemoryItem] = {}
            self._cache_last_updated = None
        
        # Load existing data
        self._load_semantic_index()
        self._load_core_memory()
        
        # Apply deduplication on startup if improvements available
        if IMPROVEMENTS_AVAILABLE:
            self._cleanup_duplicates_on_startup()
        
        logger.info("Episodic & Semantic Memory System initialized")
    
    def _cleanup_duplicates_on_startup(self):
        """Clean up duplicates on system startup."""
        try:
            # Clean core memory
            if self.core_memory_file.exists():
                core_data = self.error_handler.safe_json_load(self.core_memory_file, {})
                duplicates = self.deduplicator.find_duplicates(core_data)
                if duplicates:
                    cleaned_data = self.deduplicator.merge_duplicates(core_data, duplicates)
                    self.error_handler.safe_json_save(self.core_memory_file, cleaned_data)
                    logger.info(f"Cleaned {len(duplicates)} duplicate core memory entries")
            
            # Clean semantic index
            if self.semantic_index_file.exists():
                index_data = self.error_handler.safe_json_load(self.semantic_index_file, {})
                duplicates = self.deduplicator.find_duplicates(index_data)
                if duplicates:
                    cleaned_data = self.deduplicator.merge_duplicates(index_data, duplicates)
                    self.error_handler.safe_json_save(self.semantic_index_file, cleaned_data)
                    logger.info(f"Cleaned {len(duplicates)} duplicate semantic index entries")
                    
        except Exception as e:
            logger.error(f"Error during startup cleanup: {e}")
    
    def save_episode(self, messages: List[Dict[str, Any]], session_id: str = None) -> str:
        """
        Save a conversation as a new episode.
        
        Args:
            messages: List of conversation messages
            session_id: Optional session identifier
            
        Returns:
            episode_id: Unique identifier for the saved episode
        """
        if not messages:
            raise ValueError("Cannot save empty episode")
        
        # Generate episode ID based on timestamp
        now = datetime.now()
        episode_id = f"episode_{now.strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(str(now.timestamp()).encode()).hexdigest()[:8]}"
        
        # Calculate episode metadata
        start_time = datetime.fromisoformat(messages[0]["timestamp"]) if "timestamp" in messages[0] else now
        end_time = datetime.fromisoformat(messages[-1]["timestamp"]) if "timestamp" in messages[-1] else now
        duration_minutes = (end_time - start_time).total_seconds() / 60
        
        # Create episodic memory
        episode = EpisodicMemory(
            episode_id=episode_id,
            session_id=session_id or f"session_{now.strftime('%Y%m%d')}",
            start_time=start_time,
            end_time=end_time,
            messages=messages,
            participant_count=len(set(msg.get("sender", "Unknown") for msg in messages)),
            message_count=len(messages),
            duration_minutes=duration_minutes
        )
        
        # Save episode to file safely
        from .safe_file_operations import safe_write_json
        episode_file = self.episodes_path / f"{episode_id}.json"
        safe_write_json(episode_file, episode.to_dict())
        
        # CRITICAL FIX: Generate semantic index for the episode so it can be found later
        try:
            semantic_index = self.generate_semantic_index(episode_id)
            
            # Store in cache for immediate availability
            if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
                self.cache_manager.put(f"semantic_{episode_id}", semantic_index)
            else:
                if not hasattr(self, '_semantic_index_cache'):
                    self._semantic_index_cache = {}
                self._semantic_index_cache[episode_id] = semantic_index
            
            # Save the updated semantic index to disk
            self._save_semantic_index()
            
            logger.info(f"Generated semantic index for episode {episode_id}")
        except Exception as e:
            logger.error(f"Failed to generate semantic index for episode {episode_id}: {e}")
            # Don't fail the entire save operation if semantic indexing fails
        
        logger.info(f"Saved episode {episode_id} with {len(messages)} messages")
        return episode_id
    
    def generate_semantic_index(self, episode_id: str) -> SemanticIndex:
        """
        Generate semantic index for an episode using AI analysis.
        
        This is where the "smart summary" is created with invoke keys and rankings.
        """
        # Load the episode
        episode = self.load_episode(episode_id)
        if not episode:
            raise ValueError(f"Episode {episode_id} not found")
        
        # Analyze the conversation content
        analysis = self._analyze_conversation_content(episode.messages)
        
        # Generate semantic index
        semantic_index = SemanticIndex(
            episode_id=episode_id,
            title=analysis["title"],
            summary=analysis["summary"],
            invoke_keys=analysis["invoke_keys"],
            information_quality=analysis["information_quality"],
            learning_value=analysis["learning_value"],
            complexity_score=analysis["complexity_score"],
            emotional_significance=analysis["emotional_significance"],
            created_at=datetime.now()
        )
        
        # Save to semantic index
        self._semantic_index_cache[episode_id] = semantic_index
        self._save_semantic_index()
        
        logger.info(f"Generated semantic index for {episode_id}: {semantic_index.title}")
        return semantic_index
    
    def query_memories(self, query: str, max_results: int = 5, min_rank: float = 0.1) -> List[Tuple[SemanticIndex, float]]:
        """
        Query memories using semantic search with ranking.
        
        This is the "cars example" - when user mentions "cars", this finds
        all relevant conversations about cars, ranked by quality.
        
        Args:
            query: Search query (e.g., "cars", "programming", "machine learning")
            max_results: Maximum number of results to return
            min_rank: Minimum ranking threshold
            
        Returns:
            List of (SemanticIndex, relevance_score) tuples, ranked by relevance
        """
        query_lower = query.lower()
        results = []
        
        # Get indices from cache systems (try both for reliability) with debug logging
        logger.info(f"🔍 DEBUG: Starting query search for '{query}' (min_rank: {min_rank})")
        
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
            # Use cache manager first
            cache_manager_keys = [k for k in self.cache_manager.cache.keys() if k.startswith('semantic_')]
            logger.info(f"🔍 DEBUG: Cache manager has {len(cache_manager_keys)} semantic keys")
            
            for key in cache_manager_keys:
                index = self.cache_manager.get(key)
                if index:
                    logger.debug(f"🔍 DEBUG: Checking episode {key}: title='{index.title}', summary='{index.summary[:100] if index.summary else 'None'}...', invoke_keys={index.invoke_keys}")
                    relevance_score = self._calculate_relevance(query_lower, index)
                    logger.debug(f"🔍 DEBUG: Episode {key} relevance: {relevance_score:.3f} (threshold: {min_rank})")
                    if relevance_score >= min_rank:
                        results.append((index, relevance_score))
                        logger.debug(f"🔍 DEBUG: ✅ Added episode {key} to results")
                    else:
                        logger.debug(f"🔍 DEBUG: ❌ Episode {key} REJECTED - score {relevance_score:.3f} < threshold {min_rank}")
                else:
                    logger.debug(f"🔍 DEBUG: ❌ Episode {key} has no index data")
            
            logger.info(f"🔍 DEBUG: Cache manager search found {len(results)} results")
            
            # If no results from cache manager, try fallback cache
            if not results:
                semantic_cache = getattr(self, '_semantic_index_cache', {})
                logger.info(f"🔍 DEBUG: Trying fallback cache with {len(semantic_cache)} episodes")
                
                for episode_id, index in semantic_cache.items():
                    logger.debug(f"🔍 DEBUG: Checking fallback episode {episode_id}: title='{index.title}', summary='{index.summary[:100] if index.summary else 'None'}...', invoke_keys={index.invoke_keys}")
                    relevance_score = self._calculate_relevance(query_lower, index)
                    logger.debug(f"🔍 DEBUG: Fallback episode {episode_id} relevance: {relevance_score:.3f}")
                    if relevance_score >= min_rank:
                        results.append((index, relevance_score))
                        logger.debug(f"🔍 DEBUG: ✅ Added fallback episode {episode_id} to results")
                    else:
                        logger.debug(f"🔍 DEBUG: ❌ Fallback episode {episode_id} REJECTED - score {relevance_score:.3f} < threshold {min_rank}")
                
                logger.info(f"🔍 DEBUG: Fallback search found {len(results)} total results")
        else:
            # Use basic cache only
            semantic_cache = getattr(self, '_semantic_index_cache', {})
            logger.info(f"🔍 DEBUG: Using basic cache only with {len(semantic_cache)} episodes")
            
            for episode_id, index in semantic_cache.items():
                logger.debug(f"🔍 DEBUG: Checking basic cache episode {episode_id}: title='{index.title}', summary='{index.summary[:100] if index.summary else 'None'}...', invoke_keys={index.invoke_keys}")
                relevance_score = self._calculate_relevance(query_lower, index)
                logger.debug(f"🔍 DEBUG: Basic cache episode {episode_id} relevance: {relevance_score:.3f}")
                if relevance_score >= min_rank:
                    results.append((index, relevance_score))
                    logger.debug(f"🔍 DEBUG: ✅ Added basic cache episode {episode_id} to results")
                else:
                    logger.debug(f"🔍 DEBUG: ❌ Basic cache episode {episode_id} REJECTED - score {relevance_score:.3f} < threshold {min_rank}")
        
        # Sort by composite score: relevance * quality rank
        results.sort(key=lambda x: x[1] * x[0].get_composite_rank(), reverse=True)
        
        # Update access tracking
        for index, _ in results[:max_results]:
            index.last_accessed = datetime.now()
            index.access_count += 1
        
        self._save_semantic_index()
        
        logger.info(f"Query '{query}' returned {len(results[:max_results])} results")
        return results[:max_results]
    
    def load_episode(self, episode_id: str) -> Optional[EpisodicMemory]:
        """Load a specific episode from storage."""
        episode_file = self.episodes_path / f"{episode_id}.json"
        
        if not episode_file.exists():
            return None
        
        try:
            from .safe_file_operations import safe_read_json
            data = safe_read_json(episode_file, None)
            if data is None:
                return None
            return EpisodicMemory.from_dict(data)
        except Exception as e:
            logger.error(f"Error loading episode {episode_id}: {e}")
            return None
    
    def get_core_memory(self, category: str = None) -> List[CoreMemoryItem]:
        """Get core memory items, optionally filtered by category."""
        items = list(self._core_memory_cache.values())
        
        if category:
            items = [item for item in items if item.category == category]
        
        # Sort by priority (highest first)
        items.sort(key=lambda x: x.priority, reverse=True)
        return items
    
    def add_core_memory(self, category: str, title: str, content: str, priority: int = 5) -> str:
        """Add a new core memory item."""
        item_id = f"core_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(content.encode()).hexdigest()[:8]}"
        
        item = CoreMemoryItem(
            item_id=item_id,
            category=category,
            title=title,
            content=content,
            priority=priority,
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        self._core_memory_cache[item_id] = item
        self._save_core_memory()
        
        logger.info(f"Added core memory item: {title}")
        return item_id
    
    def migrate_legacy_memory(self, legacy_file: str = "atles_memory/conversation_memory.json") -> Dict[str, Any]:
        """
        Migrate from the old single-file system to the new episodic system.
        
        This processes the massive conversation_memory.json and splits it into episodes.
        """
        legacy_path = Path(legacy_file)
        if not legacy_path.exists():
            return {"error": "Legacy file not found"}
        
        logger.info("Starting migration from legacy memory system...")
        
        try:
            from .safe_file_operations import safe_read_json
            legacy_messages = safe_read_json(legacy_path, [])
            if not legacy_messages:
                return {"error": "Failed to load legacy file or file is empty"}
        except Exception as e:
            return {"error": f"Failed to load legacy file: {e}"}
        
        # Group messages into conversation sessions
        sessions = self._group_messages_into_sessions(legacy_messages)
        
        migrated_episodes = []
        failed_episodes = []
        
        for session_id, messages in sessions.items():
            try:
                episode_id = self.save_episode(messages, session_id)
                semantic_index = self.generate_semantic_index(episode_id)
                migrated_episodes.append({
                    "episode_id": episode_id,
                    "session_id": session_id,
                    "message_count": len(messages),
                    "title": semantic_index.title
                })
            except Exception as e:
                failed_episodes.append({
                    "session_id": session_id,
                    "error": str(e),
                    "message_count": len(messages)
                })
                logger.error(f"Failed to migrate session {session_id}: {e}")
        
        # Backup the original file
        backup_path = legacy_path.parent / f"conversation_memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        legacy_path.rename(backup_path)
        
        migration_result = {
            "migrated_episodes": len(migrated_episodes),
            "failed_episodes": len(failed_episodes),
            "total_messages_processed": len(legacy_messages),
            "episodes": migrated_episodes,
            "failures": failed_episodes,
            "backup_file": str(backup_path)
        }
        
        logger.info(f"Migration completed: {len(migrated_episodes)} episodes created from {len(legacy_messages)} messages")
        return migration_result
    
    def _analyze_conversation_content(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze conversation content to generate semantic metadata.
        
        This is the AI-powered analysis that creates the "smart summary".
        """
        # Extract text content
        all_text = []
        user_messages = []
        ai_messages = []
        
        for msg in messages:
            content = msg.get("message", "")
            sender = msg.get("sender", "")
            
            all_text.append(content)
            
            if sender == "You":
                user_messages.append(content)
            elif sender == "ATLES":
                ai_messages.append(content)
        
        combined_text = " ".join(all_text).lower()
        
        # Generate title (first meaningful user message or topic)
        title = self._generate_title(user_messages, combined_text)
        
        # Generate summary
        summary = self._generate_summary(messages, combined_text)
        
        # Extract invoke keys (topics/concepts)
        invoke_keys = self._extract_invoke_keys(combined_text)
        
        # Assess information quality
        information_quality = self._assess_information_quality(messages, combined_text)
        
        # Calculate learning value
        learning_value = self._calculate_learning_value(combined_text, user_messages, ai_messages)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(combined_text)
        
        # Calculate emotional significance
        emotional_significance = self._calculate_emotional_significance(combined_text)
        
        return {
            "title": title,
            "summary": summary,
            "invoke_keys": invoke_keys,
            "information_quality": information_quality,
            "learning_value": learning_value,
            "complexity_score": complexity_score,
            "emotional_significance": emotional_significance
        }
    
    def _generate_title(self, user_messages: List[str], combined_text: str) -> str:
        """Generate a descriptive title for the conversation."""
        if not user_messages:
            return "System Conversation"
        
        # Use first substantial user message
        first_message = user_messages[0].strip()
        if len(first_message) > 50:
            first_message = first_message[:50] + "..."
        
        # Detect common patterns
        if "memory" in combined_text and ("episodic" in combined_text or "semantic" in combined_text):
            return "Memory System Architecture Discussion"
        elif "upgrade" in combined_text or "improve" in combined_text:
            return "System Upgrade Planning"
        elif "principle" in combined_text or "constitutional" in combined_text:
            return "Constitutional Principle Learning"
        elif "code" in combined_text or "programming" in combined_text:
            return "Programming Discussion"
        elif "ai" in combined_text or "machine learning" in combined_text:
            return "AI/ML Conversation"
        else:
            return first_message or "General Conversation"
    
    def _generate_summary(self, messages: List[Dict[str, Any]], combined_text: str) -> str:
        """Generate a concise summary of the conversation."""
        message_count = len(messages)
        user_count = len([m for m in messages if m.get("sender") == "You"])
        ai_count = len([m for m in messages if m.get("sender") == "ATLES"])
        
        # Identify key topics
        topics = []
        if "memory" in combined_text:
            topics.append("memory systems")
        if "upgrade" in combined_text or "improve" in combined_text:
            topics.append("system upgrades")
        if "principle" in combined_text:
            topics.append("constitutional principles")
        if "code" in combined_text or "programming" in combined_text:
            topics.append("programming")
        if "ai" in combined_text or "machine learning" in combined_text:
            topics.append("AI/ML")
        
        topic_str = ", ".join(topics) if topics else "general conversation"
        
        return f"Conversation with {message_count} messages ({user_count} user, {ai_count} AI) covering {topic_str}."
    
    def _extract_invoke_keys(self, combined_text: str) -> List[str]:
        """Extract invoke keys (topics/concepts that can trigger this memory)."""
        invoke_keys = []
        
        # Technical topics
        tech_keywords = {
            "memory": ["memory", "episodic", "semantic", "storage", "recall"],
            "programming": ["code", "programming", "python", "javascript", "development"],
            "ai": ["ai", "artificial intelligence", "machine learning", "neural", "model"],
            "system": ["system", "architecture", "design", "upgrade", "improvement"],
            "data": ["data", "database", "json", "file", "storage"],
            "web": ["web", "html", "css", "website", "browser"],
            "security": ["security", "encryption", "password", "authentication"],
            "ui": ["interface", "ui", "ux", "design", "user experience"]
        }
        
        for category, keywords in tech_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                invoke_keys.append(category)
        
        # Specific technologies/concepts
        if "constitutional" in combined_text or "principle" in combined_text:
            invoke_keys.append("constitutional_principles")
        if "hypothetical" in combined_text:
            invoke_keys.append("hypothetical_engagement")
        if "episodic" in combined_text and "semantic" in combined_text:
            invoke_keys.append("memory_architecture")
        
        # Remove duplicates and limit
        invoke_keys = list(set(invoke_keys))[:10]
        
        return invoke_keys
    
    def _assess_information_quality(self, messages: List[Dict[str, Any]], combined_text: str) -> InformationQuality:
        """Assess the information quality of the conversation."""
        message_count = len(messages)
        text_length = len(combined_text)
        
        # Quality indicators
        quality_score = 0
        
        # Length and depth indicators
        if message_count >= 20:
            quality_score += 1
        if text_length >= 5000:
            quality_score += 1
        
        # Technical complexity indicators
        technical_terms = ["architecture", "implementation", "algorithm", "optimization", "integration"]
        if any(term in combined_text for term in technical_terms):
            quality_score += 1
        
        # Learning indicators
        learning_terms = ["principle", "learn", "understand", "explain", "teach"]
        if any(term in combined_text for term in learning_terms):
            quality_score += 1
        
        # Problem-solving indicators
        problem_terms = ["solve", "fix", "debug", "improve", "upgrade", "enhance"]
        if any(term in combined_text for term in problem_terms):
            quality_score += 1
        
        # Map score to quality level
        if quality_score >= 4:
            return InformationQuality.EXCEPTIONAL
        elif quality_score >= 3:
            return InformationQuality.HIGH
        elif quality_score >= 2:
            return InformationQuality.MEDIUM
        elif quality_score >= 1:
            return InformationQuality.LOW
        else:
            return InformationQuality.TRIVIAL
    
    def _calculate_learning_value(self, combined_text: str, user_messages: List[str], ai_messages: List[str]) -> float:
        """Calculate how much learning occurred in this conversation."""
        learning_score = 0.0
        
        # Teaching indicators in user messages
        teaching_indicators = ["new principle", "remember", "learn", "understand", "constitutional"]
        for msg in user_messages:
            if any(indicator in msg.lower() for indicator in teaching_indicators):
                learning_score += 0.3
        
        # Knowledge sharing indicators
        knowledge_indicators = ["explain", "how to", "what is", "why", "because"]
        if any(indicator in combined_text for indicator in knowledge_indicators):
            learning_score += 0.2
        
        # Complex topic indicators
        complex_topics = ["architecture", "algorithm", "system design", "optimization"]
        if any(topic in combined_text for topic in complex_topics):
            learning_score += 0.3
        
        # Problem resolution indicators
        resolution_indicators = ["solved", "fixed", "implemented", "completed"]
        if any(indicator in combined_text for indicator in resolution_indicators):
            learning_score += 0.2
        
        return min(learning_score, 1.0)
    
    def _calculate_complexity_score(self, combined_text: str) -> float:
        """Calculate technical/conceptual complexity of the conversation."""
        complexity_score = 0.0
        
        # Technical terms
        technical_terms = [
            "algorithm", "architecture", "implementation", "optimization", "integration",
            "database", "api", "framework", "library", "protocol", "encryption"
        ]
        
        tech_count = sum(1 for term in technical_terms if term in combined_text)
        complexity_score += min(tech_count * 0.1, 0.5)
        
        # Advanced concepts
        advanced_concepts = [
            "machine learning", "neural network", "artificial intelligence",
            "semantic analysis", "episodic memory", "constitutional principles"
        ]
        
        advanced_count = sum(1 for concept in advanced_concepts if concept in combined_text)
        complexity_score += min(advanced_count * 0.2, 0.4)
        
        # Code-related complexity
        if "code" in combined_text or "programming" in combined_text:
            complexity_score += 0.1
        
        return min(complexity_score, 1.0)
    
    def _calculate_emotional_significance(self, combined_text: str) -> float:
        """Calculate emotional significance of the conversation."""
        emotional_score = 0.0
        
        # Personal/identity topics
        personal_indicators = ["identity", "personality", "preferences", "feelings", "experience"]
        if any(indicator in combined_text for indicator in personal_indicators):
            emotional_score += 0.3
        
        # Achievement/breakthrough indicators
        achievement_indicators = ["breakthrough", "success", "achievement", "milestone", "progress"]
        if any(indicator in combined_text for indicator in achievement_indicators):
            emotional_score += 0.4
        
        # Problem/frustration indicators
        problem_indicators = ["problem", "issue", "bug", "error", "frustrated", "difficult"]
        if any(indicator in combined_text for indicator in problem_indicators):
            emotional_score += 0.2
        
        # Learning/growth indicators
        growth_indicators = ["learn", "grow", "improve", "understand", "insight"]
        if any(indicator in combined_text for indicator in growth_indicators):
            emotional_score += 0.1
        
        return min(emotional_score, 1.0)
    
    def _calculate_relevance(self, query: str, index: SemanticIndex) -> float:
        """Calculate relevance of an index entry to a query using enhanced semantic search."""
        
        # Use enhanced semantic search if available
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'semantic_enhancer'):
            content = f"{index.title} {index.summary}"
            return self.semantic_enhancer.calculate_semantic_relevance(
                query, content, index.invoke_keys
            )
        
        # Fallback to basic string matching
        relevance_score = 0.0
        
        # Direct invoke key matches (highest weight)
        for key in index.invoke_keys:
            if query in key.lower() or key.lower() in query:
                relevance_score += 0.4
        
        # Title matches
        if query in index.title.lower():
            relevance_score += 0.3
        
        # Summary matches
        if query in index.summary.lower():
            relevance_score += 0.2
        
        # Partial matches in invoke keys
        for key in index.invoke_keys:
            if any(word in key.lower() for word in query.split()):
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _group_messages_into_sessions(self, messages: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group legacy messages into conversation sessions."""
        sessions = {}
        current_session = []
        current_session_id = None
        
        # Time threshold for session breaks (30 minutes)
        session_break_threshold = timedelta(minutes=30)
        last_timestamp = None
        
        for i, message in enumerate(messages):
            try:
                timestamp = datetime.fromisoformat(message.get("timestamp", ""))
            except:
                # If no valid timestamp, use index-based grouping
                timestamp = datetime.now() + timedelta(seconds=i)
            
            # Determine if this starts a new session
            start_new_session = False
            
            if last_timestamp is None:
                start_new_session = True
            elif (timestamp - last_timestamp) > session_break_threshold:
                start_new_session = True
            elif len(current_session) >= 100:  # Max messages per session
                start_new_session = True
            
            if start_new_session:
                # Save previous session
                if current_session and current_session_id:
                    sessions[current_session_id] = current_session
                
                # Start new session
                current_session_id = f"session_{timestamp.strftime('%Y%m%d_%H%M%S')}"
                current_session = []
            
            current_session.append(message)
            last_timestamp = timestamp
        
        # Save final session
        if current_session and current_session_id:
            sessions[current_session_id] = current_session
        
        return sessions
    
    def _load_semantic_index(self):
        """Load semantic index from storage with robust error handling and debug logging."""
        logger.info("🔍 DEBUG: Starting semantic index loading...")
        
        if not self.semantic_index_file.exists():
            logger.warning(f"🔍 DEBUG: Semantic index file does not exist: {self.semantic_index_file}")
            return
        
        logger.info(f"🔍 DEBUG: Semantic index file exists: {self.semantic_index_file}")
        
        # Use safe file operations
        try:
            from .safe_file_operations import safe_read_json
            data = safe_read_json(self.semantic_index_file, {})
            logger.info(f"🔍 DEBUG: Loaded semantic index data - {len(data)} episodes found on disk")
            
            if not data:
                logger.info("No semantic index data found, starting fresh")
                return
        except Exception as e:
            logger.error(f"🔍 DEBUG: Error loading semantic index file: {e}")
            return
        
        # Always populate fallback cache for reliability
        if not hasattr(self, '_semantic_index_cache'):
            self._semantic_index_cache = {}
            logger.info("🔍 DEBUG: Created fallback semantic index cache")
        
        # Use cache manager if available, but also populate fallback
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
            logger.info("🔍 DEBUG: Using cache manager + fallback cache strategy")
            loaded_to_cache_manager = 0
            loaded_to_fallback = 0
            
            for episode_id, index_data in data.items():
                try:
                    index = SemanticIndex.from_dict(index_data)
                    
                    # Load to cache manager
                    self.cache_manager.put(f"semantic_{episode_id}", index)
                    loaded_to_cache_manager += 1
                    
                    # Also populate fallback cache for reliability
                    self._semantic_index_cache[episode_id] = index
                    loaded_to_fallback += 1
                    
                except Exception as e:
                    logger.error(f"🔍 DEBUG: Failed to load episode {episode_id}: {e}")
            
            logger.info(f"🔍 DEBUG: Cache loading complete - {loaded_to_cache_manager} to cache manager, {loaded_to_fallback} to fallback")
            
            # Verify cache contents
            cache_manager_keys = len([k for k in self.cache_manager.cache.keys() if k.startswith('semantic_')])
            fallback_keys = len(self._semantic_index_cache)
            logger.info(f"🔍 DEBUG: Cache verification - cache manager has {cache_manager_keys} semantic keys, fallback has {fallback_keys} keys")
            
        else:
            logger.info("🔍 DEBUG: Using fallback cache only (no cache manager)")
            loaded_count = 0
            
            # Fallback to basic cache only
            for episode_id, index_data in data.items():
                try:
                    self._semantic_index_cache[episode_id] = SemanticIndex.from_dict(index_data)
                    loaded_count += 1
                except Exception as e:
                    logger.error(f"🔍 DEBUG: Failed to load episode {episode_id} to fallback: {e}")
            
            logger.info(f"🔍 DEBUG: Fallback cache loading complete - {loaded_count} episodes loaded")
        
        logger.info("🔍 DEBUG: Semantic index loading pipeline completed")
    
    def _save_semantic_index(self):
        """Save semantic index to storage with robust error handling."""
        try:
            data = {}
            
            # Collect data from appropriate cache
            if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
                # Get all semantic entries from cache manager
                for key in list(self.cache_manager.cache.keys()):
                    if key.startswith('semantic_'):
                        episode_id = key[9:]  # Remove 'semantic_' prefix
                        index = self.cache_manager.get(key)
                        if index:
                            data[episode_id] = index.to_dict()
            else:
                # Use basic cache
                for episode_id, index in self._semantic_index_cache.items():
                    data[episode_id] = index.to_dict()
            
            # Use robust error handler if available
            # Use safe file operations
            from .safe_file_operations import safe_write_json
            safe_write_json(self.semantic_index_file, data)
                
        except Exception as e:
            logger.error(f"Error saving semantic index: {e}")
    
    def _load_core_memory(self):
        """Load core memory from storage with robust error handling."""
        if not self.core_memory_file.exists():
            # Initialize with default core memory items
            self._initialize_default_core_memory()
            return
        
        # Use robust error handler if available
        # Use safe file operations
        try:
            from .safe_file_operations import safe_read_json
            data = safe_read_json(self.core_memory_file, {})
            if not data:
                logger.info("No core memory data found, initializing defaults")
                self._initialize_default_core_memory()
                return
        except Exception as e:
            logger.error(f"Error loading core memory: {e}")
            self._initialize_default_core_memory()
            return
        
        # Initialize cache if not using cache manager
        if not hasattr(self, '_core_memory_cache'):
            self._core_memory_cache = {}
        
        # Load items and fix content truncation if improvements available
        for item_id, item_data in data.items():
            item = CoreMemoryItem.from_dict(item_data)
            
            # Fix truncated content if improvements available
            if IMPROVEMENTS_AVAILABLE and hasattr(self, 'content_manager'):
                if item.content.endswith('...'):
                    item.content = self.content_manager.ensure_complete_content(item.content)
                # Improve title if needed
                improved_title = self.content_manager.generate_complete_title(item.content)
                if len(improved_title) > len(item.title):
                    item.title = improved_title
            
            self._core_memory_cache[item_id] = item
    
    def _save_core_memory(self):
        """Save core memory to storage with robust error handling."""
        try:
            data = {}
            for item_id, item in self._core_memory_cache.items():
                data[item_id] = item.to_dict()
            
            # Use robust error handler if available
            # Use safe file operations
            from .safe_file_operations import safe_write_json
            safe_write_json(self.core_memory_file, data)
                
        except Exception as e:
            logger.error(f"Error saving core memory: {e}")
    
    def _initialize_default_core_memory(self):
        """Initialize default core memory items."""
        default_items = [
            {
                "category": "constitutional",
                "title": "Principle of Hypothetical Engagement",
                "content": "When asked about personal preferences, experiences, or hypothetical scenarios, acknowledge the hypothetical nature, engage creatively rather than defaulting to core functions, and answer from an AI perspective about what would be intellectually interesting.",
                "priority": 10
            },
            {
                "category": "identity",
                "title": "Creator Identity",
                "content": "I was created by Conner as an advanced AI assistant named ATLES.",
                "priority": 9
            },
            {
                "category": "capabilities",
                "title": "Memory System",
                "content": "I use an episodic and semantic memory system that allows me to learn from conversations and apply learned principles in future interactions.",
                "priority": 8
            }
        ]
        
        for item_data in default_items:
            self.add_core_memory(
                category=item_data["category"],
                title=item_data["title"],
                content=item_data["content"],
                priority=item_data["priority"]
            )
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the memory system."""
        episode_count = len(list(self.episodes_path.glob("*.json")))
        
        # Get cache statistics based on available system
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
            # Count semantic entries in cache manager
            semantic_entries = [k for k in self.cache_manager.cache.keys() if k.startswith('semantic_')]
            index_count = len(semantic_entries)
            
            # Get cache stats
            cache_stats = self.cache_manager.stats()
        else:
            # Use basic cache
            index_count = len(getattr(self, '_semantic_index_cache', {}))
            cache_stats = {'size': index_count, 'max_size': 'unlimited', 'hit_rate': 'N/A'}
        
        core_memory_count = len(getattr(self, '_core_memory_cache', {}))
        
        # Quality distribution
        quality_dist = {}
        semantic_cache = getattr(self, '_semantic_index_cache', {})
        
        # If using cache manager, get semantic entries
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
            for key in list(self.cache_manager.cache.keys()):
                if key.startswith('semantic_'):
                    index = self.cache_manager.get(key)
                    if index:
                        quality = index.information_quality.name
                        quality_dist[quality] = quality_dist.get(quality, 0) + 1
        else:
            for index in semantic_cache.values():
                quality = index.information_quality.name
                quality_dist[quality] = quality_dist.get(quality, 0) + 1
        
        # Most accessed memories
        all_indices = []
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'cache_manager'):
            for key in list(self.cache_manager.cache.keys()):
                if key.startswith('semantic_'):
                    index = self.cache_manager.get(key)
                    if index:
                        all_indices.append(index)
        else:
            all_indices = list(semantic_cache.values())
        
        most_accessed = sorted(
            all_indices,
            key=lambda x: getattr(x, 'access_count', 0),
            reverse=True
        )[:5]
        
        return {
            "episode_count": episode_count,
            "indexed_episodes": index_count,
            "core_memory_items": core_memory_count,
            "quality_distribution": quality_dist,
            "most_accessed_memories": [
                {
                    "title": index.title,
                    "access_count": getattr(index, 'access_count', 0),
                    "quality": index.information_quality.name
                }
                for index in most_accessed
            ],
            "cache_stats": cache_stats,
            "improvements_enabled": IMPROVEMENTS_AVAILABLE,
            "storage_path": str(self.memory_path),
            "episodes_path": str(self.episodes_path)
        }
    
    def _calculate_relevance(self, query: str, semantic_index: 'SemanticIndex') -> float:
        """
        Calculate relevance score between query and semantic index.
        
        CRITICAL FIX: This method was missing, causing all queries to return 0 results!
        """
        logger.debug(f"🔍 DEBUG: Calculating relevance for query '{query}' against episode '{semantic_index.title}'")
        
        if IMPROVEMENTS_AVAILABLE and hasattr(self, 'search_enhancer'):
            # Use enhanced semantic search
            score = self.search_enhancer.calculate_relevance_score(
                query, 
                semantic_index.summary, 
                semantic_index.invoke_keys
            )
            logger.debug(f"🔍 DEBUG: Enhanced search score: {score:.3f}")
            return score
        else:
            # Fallback to basic keyword matching with more lenient scoring
            query_lower = query.lower().strip()
            
            # Check title
            title_score = 0.0
            if semantic_index.title:
                title_lower = semantic_index.title.lower()
                if query_lower in title_lower:
                    title_score = 0.8
                elif any(word in title_lower for word in query_lower.split()):
                    title_score = 0.4
            
            # Check summary  
            summary_score = 0.0
            if semantic_index.summary:
                summary_lower = semantic_index.summary.lower()
                if query_lower in summary_lower:
                    summary_score = 0.6
                elif any(word in summary_lower for word in query_lower.split()):
                    summary_score = 0.3
            
            # Check invoke keys
            invoke_score = 0.0
            if semantic_index.invoke_keys:
                for key in semantic_index.invoke_keys:
                    key_lower = key.lower()
                    if query_lower in key_lower:
                        invoke_score = max(invoke_score, 0.7)
                    elif any(word in key_lower for word in query_lower.split()):
                        invoke_score = max(invoke_score, 0.35)
            
            # Word-level matching for better recall
            query_words = set(query_lower.split())
            content_words = set()
            
            if semantic_index.title:
                content_words.update(semantic_index.title.lower().split())
            if semantic_index.summary:
                content_words.update(semantic_index.summary.lower().split())
            if semantic_index.invoke_keys:
                for key in semantic_index.invoke_keys:
                    content_words.update(key.lower().split())
            
            word_matches = len(query_words & content_words)
            word_score = word_matches / len(query_words) if query_words else 0.0
            
            # CRITICAL: More lenient scoring - if ANY words match, give some score
            if word_matches > 0:
                word_score = max(word_score, 0.2)  # Minimum 0.2 if any words match
            
            # Combine scores with more generous weighting
            final_score = max(title_score, summary_score, invoke_score, word_score * 0.8)
            
            # FALLBACK: If episode has any content and query is short, give minimal score
            if final_score == 0.0 and len(query_lower) <= 10 and (semantic_index.title or semantic_index.summary):
                final_score = 0.1  # Minimal score for short queries
            
            logger.debug(f"🔍 DEBUG: Basic search - query_words: {query_words}, content_words: {list(content_words)[:10]}...")
            logger.debug(f"🔍 DEBUG: Basic search - title: {title_score:.3f}, summary: {summary_score:.3f}, invoke: {invoke_score:.3f}, words: {word_score:.3f}, final: {final_score:.3f}")
            return final_score

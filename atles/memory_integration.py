"""
ATLES Memory Integration Layer

This module integrates the new Episodic & Semantic Memory System with the existing
ATLES architecture. It provides:

1. Backward compatibility with existing memory interfaces
2. Automatic migration from legacy memory format
3. Enhanced memory-aware response generation
4. Seamless integration with conversation flow manager

Key Integration Points:
- Replaces single conversation log with episodic system
- Enhances memory-aware reasoning with semantic search
- Provides migration utilities for existing data
- Maintains API compatibility for existing code
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

from .episodic_semantic_memory import (
    EpisodicSemanticMemory, 
    SemanticIndex, 
    CoreMemoryItem,
    InformationQuality
)
import importlib
import sys
# Force reload of memory_aware_reasoning module to pick up changes
if 'atles.memory_aware_reasoning' in sys.modules:
    importlib.reload(sys.modules['atles.memory_aware_reasoning'])
from .memory_aware_reasoning import MemoryAwareReasoning, LearnedPrinciple

logger = logging.getLogger(__name__)


class MemoryIntegration:
    """
    Integration layer that bridges the new episodic/semantic memory system
    with existing ATLES components.
    
    This class ensures smooth transition from the old memory system while
    providing enhanced capabilities for memory-aware AI responses.
    """
    
    def __init__(self, memory_path: str = "atles_memory", auto_migrate: bool = True):
        self.memory_path = Path(memory_path)
        
        # Initialize the new memory systems
        self.episodic_memory = EpisodicSemanticMemory(memory_path)
        self.memory_reasoning = MemoryAwareReasoning(memory_path, episodic_memory=self.episodic_memory)
        
        # Track current conversation for real-time saving
        self.current_conversation: List[Dict[str, Any]] = []
        self.current_session_id: Optional[str] = None
        self.conversation_start_time: Optional[datetime] = None
        
        # Migration flag
        self._migration_completed = False
        
        # Auto-migrate if requested and needed
        if auto_migrate:
            self._check_and_migrate()
        
        logger.info("Memory Integration Layer initialized")
    
    def start_conversation_session(self, session_id: str = None) -> str:
        """
        Start a new conversation session.
        
        This replaces the old single-log approach with session-based episodic memory.
        """
        # Save any existing conversation first
        if self.current_conversation:
            self.end_conversation_session()
        
        # Start new session
        self.current_session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_conversation = []
        self.conversation_start_time = datetime.now()
        
        logger.info(f"Started conversation session: {self.current_session_id}")
        return self.current_session_id
    
    def add_message(self, sender: str, message: str, context: Dict[str, Any] = None) -> None:
        """
        Add a message to the current conversation.
        
        This maintains compatibility with existing code while building episodic memory.
        """
        if not self.current_session_id:
            self.start_conversation_session()
        
        message_entry = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "message": message,
            "context": context or {}
        }
        
        self.current_conversation.append(message_entry)
        
        print(f"🚨🚨🚨 ATLES DEBUG ADD_MESSAGE: Now have {len(self.current_conversation)} messages")
        logger.info(f"🚨🚨🚨 ATLES DEBUG ADD_MESSAGE: Now have {len(self.current_conversation)} messages")
        
        # Auto-save every 10 messages to prevent data loss
        if len(self.current_conversation) % 10 == 0:
            print(f"🚨🚨🚨 ATLES DEBUG CHECKPOINT: {len(self.current_conversation)} messages!")
            logger.info(f"🚨🚨🚨 ATLES DEBUG CHECKPOINT: {len(self.current_conversation)} messages!")
            self._auto_save_checkpoint()
        
        # Auto-create episode every 25 messages to ensure memories are searchable
        if len(self.current_conversation) % 25 == 0:
            print(f"🚨🚨🚨 ATLES DEBUG AUTO-EPISODE: {len(self.current_conversation)} messages!")
            logger.info(f"🚨🚨🚨 ATLES DEBUG AUTO-EPISODE: {len(self.current_conversation)} messages!")
            logger.info(f"🔄 Auto-creating episode after {len(self.current_conversation)} messages")
            episode_id = self.end_conversation_session()
            if episode_id:
                print(f"🚨🚨🚨 ATLES DEBUG EPISODE SUCCESS: {episode_id}")
                logger.info(f"🚨🚨🚨 ATLES DEBUG EPISODE SUCCESS: {episode_id}")
                logger.info(f"✅ Auto-created episode: {episode_id}")
                # Start a new conversation session
                self.start_conversation_session()
            else:
                print(f"🚨🚨🚨 ATLES DEBUG EPISODE FAILED!")
                logger.info(f"🚨🚨🚨 ATLES DEBUG EPISODE FAILED!")
    
    def end_conversation_session(self) -> Optional[str]:
        """
        End the current conversation session and save as an episode.
        
        This triggers the semantic indexing process.
        """
        if not self.current_conversation:
            return None
        
        try:
            # Save as episode
            episode_id = self.episodic_memory.save_episode(
                messages=self.current_conversation,
                session_id=self.current_session_id
            )
            
            # Generate semantic index
            semantic_index = self.episodic_memory.generate_semantic_index(episode_id)
            
            # Extract and learn any new principles
            self._extract_and_learn_principles(self.current_conversation)
            
            # Clear current conversation
            conversation_count = len(self.current_conversation)
            self.current_conversation = []
            self.current_session_id = None
            self.conversation_start_time = None
            
            logger.info(f"Ended conversation session: {episode_id} ({conversation_count} messages)")
            logger.info(f"Generated semantic index: {semantic_index.title}")
            
            return episode_id
            
        except Exception as e:
            logger.error(f"Error ending conversation session: {e}")
            return None
    
    def process_user_prompt_with_memory(self, user_prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a user prompt with full memory awareness.
        
        This is the main entry point that combines:
        1. Semantic memory retrieval (episodic system)
        2. Constitutional principle application (memory reasoning)
        3. Enhanced context generation
        """
        print("🚨🚨🚨 ATLES DEBUG MEMORY_INTEGRATION LOADED! 🚨🚨🚨")
        logger.info("🚨🚨🚨 ATLES DEBUG MEMORY_INTEGRATION LOADED! 🚨🚨🚨")
        # Step 1: Query relevant memories using semantic search
        relevant_memories = self.query_relevant_memories(user_prompt)
        
        # Step 2: Get constitutional principles and core memory
        core_memory = self.episodic_memory.get_core_memory()
        constitutional_principles = [item for item in core_memory if item.category == "constitutional"]
        
        # Step 3: Use memory-aware reasoning for principle application
        print("🚨🚨🚨 ATLES DEBUG CALLING MEMORY_REASONING! 🚨🚨🚨")
        logger.info("🚨🚨🚨 ATLES DEBUG CALLING MEMORY_REASONING! 🚨🚨🚨")
        reasoning_context = self.memory_reasoning.process_user_prompt(user_prompt, context)
        print(f"🚨🚨🚨 ATLES DEBUG REASONING KEYS: {list(reasoning_context.keys()) if reasoning_context else 'None'}")
        logger.info(f"🚨🚨🚨 ATLES DEBUG REASONING KEYS: {list(reasoning_context.keys()) if reasoning_context else 'None'}")
        
        # Step 4: Combine all memory sources into enhanced context
        enhanced_context = self._create_enhanced_context(
            user_prompt=user_prompt,
            relevant_memories=relevant_memories,
            constitutional_principles=constitutional_principles,
            reasoning_context=reasoning_context,
            core_memory=core_memory
        )
        
        # Step 5: Add message to current conversation
        self.add_message("You", user_prompt, context)
        
        return enhanced_context
    
    def query_relevant_memories(self, query: str, max_results: int = 3) -> List[Tuple[SemanticIndex, float]]:
        """
        Query for relevant memories using the semantic index.
        
        This implements the "cars example" - when user mentions cars,
        find all relevant conversations about cars, ranked by quality.
        """
        return self.episodic_memory.query_memories(query, max_results)
    
    def add_ai_response(self, response: str, context: Dict[str, Any] = None) -> None:
        """
        Add an AI response to the current conversation.
        
        This maintains the conversation flow for episodic memory creation.
        """
        self.add_message("ATLES", response, context)
    
    def learn_new_principle(self, principle_name: str, description: str, rules: List[str], 
                          examples: List[str] = None, priority: int = 5) -> bool:
        """
        Learn a new constitutional principle.
        
        This adds to both the memory reasoning system and core memory.
        """
        try:
            # Add to memory reasoning system
            principle = LearnedPrinciple(
                name=principle_name,
                description=description,
                rules=rules,
                examples=examples or [],
                confidence=0.9,
                learned_at=datetime.now()
            )
            
            reasoning_success = self.memory_reasoning.learn_new_principle(principle)
            
            # Add to core memory
            core_memory_id = self.episodic_memory.add_core_memory(
                category="constitutional",
                title=principle_name,
                content=f"{description}\n\nRules:\n" + "\n".join(f"- {rule}" for rule in rules),
                priority=priority
            )
            
            logger.info(f"Learned new principle: {principle_name}")
            return reasoning_success and bool(core_memory_id)
            
        except Exception as e:
            logger.error(f"Error learning new principle: {e}")
            return False
    
    def get_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent conversation history across all episodes.
        
        This provides backward compatibility with existing code that expects
        a simple conversation history list.
        """
        # Get recent episodes
        recent_episodes = []
        episode_files = sorted(self.episodic_memory.episodes_path.glob("*.json"), 
                             key=lambda x: x.stat().st_mtime, reverse=True)
        
        messages = []
        for episode_file in episode_files[:10]:  # Last 10 episodes
            try:
                episode = self.episodic_memory.load_episode(episode_file.stem)
                if episode:
                    messages.extend(episode.messages)
                    if len(messages) >= limit:
                        break
            except Exception as e:
                logger.error(f"Error loading episode {episode_file}: {e}")
        
        # Add current conversation
        messages.extend(self.current_conversation)
        
        # Return most recent messages
        return messages[-limit:] if len(messages) > limit else messages
    
    def search_memories(self, search_term: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search across all memories for specific terms.
        
        This provides a unified search interface across episodic memory.
        """
        # Semantic search
        semantic_results = self.episodic_memory.query_memories(search_term, max_results)
        
        search_results = []
        for semantic_index, relevance_score in semantic_results:
            # Load the full episode for detailed results
            episode = self.episodic_memory.load_episode(semantic_index.episode_id)
            if episode:
                # Find matching messages within the episode
                matching_messages = []
                for msg in episode.messages:
                    if search_term.lower() in msg.get("message", "").lower():
                        matching_messages.append(msg)
                
                search_results.append({
                    "episode_id": semantic_index.episode_id,
                    "title": semantic_index.title,
                    "summary": semantic_index.summary,
                    "relevance_score": relevance_score,
                    "quality": semantic_index.information_quality.name,
                    "matching_messages": matching_messages[:3],  # Top 3 matches per episode
                    "total_matches": len(matching_messages)
                })
        
        return search_results
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory system statistics."""
        episodic_stats = self.episodic_memory.get_system_stats()
        reasoning_stats = self.memory_reasoning.get_learning_summary()
        
        return {
            "episodic_memory": episodic_stats,
            "learned_principles": reasoning_stats,
            "current_session": {
                "session_id": self.current_session_id,
                "message_count": len(self.current_conversation),
                "duration_minutes": (datetime.now() - self.conversation_start_time).total_seconds() / 60 
                                  if self.conversation_start_time else 0
            },
            "migration_completed": self._migration_completed
        }
    
    def migrate_legacy_memory(self, backup: bool = True) -> Dict[str, Any]:
        """
        Migrate from the legacy single-file memory system.
        
        This is the main migration function that transforms the old system
        into the new episodic/semantic architecture.
        """
        logger.info("Starting legacy memory migration...")
        
        # Check for legacy files
        legacy_conversation_file = self.memory_path / "conversation_memory.json"
        legacy_principles_file = self.memory_path / "learned_principles.json"
        
        migration_results = {
            "conversations_migrated": False,
            "principles_migrated": False,
            "episodes_created": 0,
            "principles_learned": 0,
            "errors": []
        }
        
        # Migrate conversations
        if legacy_conversation_file.exists():
            try:
                # First, extract principles from the entire conversation history
                logger.info("🧠 Extracting learned principles from conversation history...")
                with open(legacy_conversation_file, 'r', encoding='utf-8') as f:
                    all_messages = json.load(f)
                
                # Extract principles from the full conversation history
                extracted_principles = self._enhanced_principle_extraction(all_messages)
                principles_learned = 0
                
                for principle in extracted_principles:
                    try:
                        success = self.memory_reasoning.learn_new_principle(principle)
                        if success:
                            self.episodic_memory.add_core_memory(
                                category="constitutional",
                                title=principle.name,
                                content=principle.description,
                                priority=9  # High priority for migrated principles
                            )
                            principles_learned += 1
                            logger.info(f"🧠 Migrated principle: {principle.name}")
                    except Exception as e:
                        logger.error(f"Failed to migrate principle {principle.name}: {e}")
                
                migration_results["principles_learned"] = principles_learned
                logger.info(f"✅ Extracted {principles_learned} principles from conversation history")
                
                # Now migrate the conversations to episodes
                conversation_result = self.episodic_memory.migrate_legacy_memory(str(legacy_conversation_file))
                migration_results["conversations_migrated"] = True
                migration_results["episodes_created"] = conversation_result.get("migrated_episodes", 0)
                migration_results["conversation_details"] = conversation_result
                
            except Exception as e:
                error_msg = f"Failed to migrate conversations: {e}"
                migration_results["errors"].append(error_msg)
                logger.error(error_msg)
        
        # Migrate learned principles
        if legacy_principles_file.exists():
            try:
                with open(legacy_principles_file, 'r', encoding='utf-8') as f:
                    legacy_principles = json.load(f)
                
                principles_migrated = 0
                for principle_name, principle_data in legacy_principles.items():
                    try:
                        success = self.learn_new_principle(
                            principle_name=principle_data.get("name", principle_name),
                            description=principle_data.get("description", ""),
                            rules=principle_data.get("rules", []),
                            examples=principle_data.get("examples", []),
                            priority=8  # High priority for migrated principles
                        )
                        if success:
                            principles_migrated += 1
                    except Exception as e:
                        migration_results["errors"].append(f"Failed to migrate principle {principle_name}: {e}")
                
                migration_results["principles_migrated"] = True
                migration_results["principles_learned"] = principles_migrated
                
                # Backup and remove legacy file
                if backup:
                    backup_path = legacy_principles_file.parent / f"learned_principles_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    legacy_principles_file.rename(backup_path)
                
            except Exception as e:
                error_msg = f"Failed to migrate principles: {e}"
                migration_results["errors"].append(error_msg)
                logger.error(error_msg)
        
        self._migration_completed = True
        
        logger.info(f"Migration completed: {migration_results['episodes_created']} episodes, {migration_results['principles_learned']} principles")
        return migration_results
    
    def _create_enhanced_context(self, user_prompt: str, relevant_memories: List[Tuple[SemanticIndex, float]],
                               constitutional_principles: List[CoreMemoryItem], reasoning_context: Dict[str, Any],
                               core_memory: List[CoreMemoryItem]) -> Dict[str, Any]:
        """Create enhanced context combining all memory sources."""
        
        logger.info(f"🔍 DEBUG: Creating enhanced context with {len(relevant_memories)} memories, {len(constitutional_principles)} principles")
        logger.info(f"🔍 DEBUG: Reasoning context keys: {list(reasoning_context.keys())}")
        
        enhanced_context = {
            "original_prompt": user_prompt,
            "timestamp": datetime.now().isoformat(),
            "memory_enhanced": True,
            
            # Episodic memory context
            "relevant_episodes": [
                {
                    "episode_id": index.episode_id,
                    "title": index.title,
                    "summary": index.summary,
                    "relevance_score": relevance,
                    "quality": index.information_quality.name,
                    "invoke_keys": index.invoke_keys
                }
                for index, relevance in relevant_memories
            ],
            
            # Constitutional principles
            "constitutional_principles": [
                {
                    "title": principle.title,
                    "content": principle.content,
                    "priority": principle.priority
                }
                for principle in constitutional_principles
            ],
            
            # Memory reasoning context
            "reasoning_context": reasoning_context,
            
            # Contextual rules from memory reasoning
            "contextual_rules": reasoning_context.get("contextual_rules", []),
            
            # Core memory items
            "core_memory": {
                "identity": [item.content for item in core_memory if item.category == "identity"],
                "capabilities": [item.content for item in core_memory if item.category == "capabilities"],
                "preferences": [item.content for item in core_memory if item.category == "preferences"]
            },
            
            # Memory-informed response guidelines
            "response_guidelines": self._generate_memory_informed_guidelines(
                user_prompt, relevant_memories, constitutional_principles, reasoning_context
            )
        }
        
        return enhanced_context
    
    def _generate_memory_informed_guidelines(self, user_prompt: str, relevant_memories: List[Tuple[SemanticIndex, float]],
                                           constitutional_principles: List[CoreMemoryItem], 
                                           reasoning_context: Dict[str, Any]) -> List[str]:
        """Generate specific response guidelines based on memory context."""
        guidelines = []
        
        # Guidelines from relevant episodes
        if relevant_memories:
            guidelines.append("Consider the context from previous relevant conversations")
            high_quality_memories = [mem for mem, score in relevant_memories 
                                   if mem.information_quality.value >= 4]
            if high_quality_memories:
                guidelines.append("Draw insights from high-quality previous discussions on this topic")
        
        # Guidelines from constitutional principles
        for principle in constitutional_principles:
            if principle.priority >= 8:  # High priority principles
                guidelines.append(f"Apply constitutional principle: {principle.title}")
        
        # Guidelines from reasoning context
        if reasoning_context.get("response_guidelines"):
            guidelines.extend(reasoning_context["response_guidelines"])
        
        # Memory-specific guidelines
        guidelines.extend([
            "Use learned knowledge from previous conversations",
            "Maintain consistency with established principles and preferences",
            "Reference relevant past discussions when appropriate"
        ])
        
        return guidelines
    
    def _extract_and_learn_principles(self, conversation: List[Dict[str, Any]]) -> None:
        """Extract and learn new principles from the conversation automatically."""
        try:
            # Enhanced automatic principle extraction
            extracted_principles = self._enhanced_principle_extraction(conversation)
            
            for principle in extracted_principles:
                # Save to memory reasoning system
                success = self.memory_reasoning.learn_new_principle(principle)
                
                if success:
                    # Add to core memory as well
                    self.episodic_memory.add_core_memory(
                        category="constitutional",
                        title=principle.name,
                        content=principle.description,
                        priority=8  # High priority for automatically learned principles
                    )
                    
                    logger.info(f"🧠 Automatically learned principle: {principle.name}")
                
        except Exception as e:
            logger.error(f"Error extracting principles: {e}")
    
    def _enhanced_principle_extraction(self, conversation: List[Dict[str, Any]]) -> List:
        """
        Enhanced automatic principle extraction that catches learning patterns.
        
        This is the core of automatic learning - it should detect when the user
        is teaching new principles without requiring manual intervention.
        """
        from .memory_aware_reasoning import LearnedPrinciple
        from datetime import datetime
        import re
        
        extracted_principles = []
        
        # Enhanced principle indicators - more comprehensive patterns
        principle_indicators = [
            # Explicit teaching
            "new principle", "constitutional principle", "new rule", "principle of",
            "training session", "fix a flaw", "correct this", "adding a new",
            "core principle", "new constitutional", "understand this new",
            
            # Behavioral corrections
            "you should", "always", "never", "remember to", "from now on", 
            "going forward", "new guideline", "important rule",
            
            # Learning contexts
            "when asked about", "if someone asks", "in the future",
            "learn this", "understand that", "apply this principle",
            
            # Correction patterns
            "you failed", "incorrect", "wrong approach", "better way",
            "instead of", "rather than", "don't do", "avoid doing"
        ]
        
        for i, message in enumerate(conversation):
            if message.get('sender') == 'You':  # User messages
                message_text = message.get('message', '')
                message_lower = message_text.lower()
                
                # Check for principle teaching patterns
                if any(indicator in message_lower for indicator in principle_indicators):
                    principle = self._parse_principle_from_message(message, conversation[i:i+3])
                    if principle:
                        extracted_principles.append(principle)
        
        return extracted_principles
    
    def _parse_principle_from_message(self, message: Dict, context_messages: List[Dict]) -> Optional:
        """Parse a principle from a message with enhanced pattern recognition."""
        from .memory_aware_reasoning import LearnedPrinciple
        from datetime import datetime
        import re
        
        try:
            message_text = message.get('message', '')
            
            # Extract principle name with better patterns
            principle_name = "Learned Principle"
            
            # Look for explicit principle names
            name_patterns = [
                r"principle of ([^.!?\n]+)",
                r"new principle[:\s]*([^.!?\n]+)",
                r"constitutional principle[:\s]*([^.!?\n]+)",
                r"the ([^.!?\n]*principle[^.!?\n]*)",
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, message_text, re.IGNORECASE)
                if match:
                    principle_name = match.group(1).strip().title()
                    break
            
            # Special cases for known principles
            if "hypothetical engagement" in message_text.lower():
                principle_name = "Principle of Hypothetical Engagement"
            elif "explicit action" in message_text.lower():
                principle_name = "Principle of Explicit Action"
            
            # Extract rules and guidelines
            rules = []
            
            # Look for behavioral rules
            rule_patterns = [
                r"when ([^,]+), ([^.!?\n]+)",
                r"you should ([^.!?\n]+)",
                r"always ([^.!?\n]+)",
                r"never ([^.!?\n]+)",
                r"remember to ([^.!?\n]+)",
                r"i will:\s*([^.!?\n]+)",
            ]
            
            for pattern in rule_patterns:
                matches = re.findall(pattern, message_text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        rule = f"When {match[0]}, {match[1]}"
                    else:
                        rule = match.strip()
                    
                    if len(rule) > 10:  # Only meaningful rules
                        rules.append(rule)
            
            # Extract examples
            examples = []
            if "for example" in message_text.lower():
                example_match = re.search(r"for example[,:]?\s*([^.!?]+)", message_text, re.IGNORECASE)
                if example_match:
                    examples.append(example_match.group(1).strip())
            
            # Only create principle if we have meaningful content
            if (rules or 
                len(message_text) > 50 and any(word in message_text.lower() 
                for word in ["principle", "rule", "should", "always", "never", "when"])):
                
                return LearnedPrinciple(
                    name=principle_name,
                    description=message_text[:300] + "..." if len(message_text) > 300 else message_text,
                    rules=rules if rules else [message_text[:100] + "..."],
                    examples=examples,
                    confidence=0.8,  # Good confidence for automatic extraction
                    learned_at=datetime.now()
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing principle: {e}")
            return None
    
    def _auto_save_checkpoint(self) -> None:
        """Auto-save conversation checkpoint to prevent data loss."""
        if not self.current_conversation:
            return
        
        try:
            checkpoint_file = self.memory_path / f"checkpoint_{self.current_session_id}.json"
            checkpoint_data = {
                "session_id": self.current_session_id,
                "messages": self.current_conversation,
                "checkpoint_time": datetime.now().isoformat()
            }
            
            with open(checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving checkpoint: {e}")
    
    def _check_and_migrate(self) -> None:
        """Check if migration is needed and perform it."""
        legacy_file = self.memory_path / "conversation_memory.json"
        
        # Check if we have legacy data but no episodes
        has_legacy_data = legacy_file.exists() and legacy_file.stat().st_size > 100
        has_episodes = len(list(self.episodic_memory.episodes_path.glob("*.json"))) > 0
        
        if has_legacy_data and not has_episodes:
            logger.info("Legacy memory detected, starting automatic migration...")
            migration_result = self.migrate_legacy_memory()
            
            if migration_result["conversations_migrated"]:
                logger.info(f"Successfully migrated {migration_result['episodes_created']} episodes")
            else:
                logger.warning("Migration completed but no conversations were migrated")
    
    def cleanup_checkpoints(self) -> None:
        """Clean up old checkpoint files."""
        try:
            checkpoint_files = list(self.memory_path.glob("checkpoint_*.json"))
            cutoff_time = datetime.now() - timedelta(hours=24)  # Keep checkpoints for 24 hours
            
            for checkpoint_file in checkpoint_files:
                if datetime.fromtimestamp(checkpoint_file.stat().st_mtime) < cutoff_time:
                    checkpoint_file.unlink()
                    
        except Exception as e:
            logger.error(f"Error cleaning up checkpoints: {e}")


# Convenience function for easy integration
def create_memory_integration(memory_path: str = "atles_memory", auto_migrate: bool = True) -> MemoryIntegration:
    """
    Create and initialize the memory integration system.
    
    This is the main entry point for integrating the new memory system
    with existing ATLES components.
    """
    return MemoryIntegration(memory_path, auto_migrate)

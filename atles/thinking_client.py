#!/usr/bin/env python3
"""
Thinking Constitutional Client for ATLES

This wraps the lightweight constitutional client and adds internal "scratchpad thinking"
where ATLES can:
1. Draft an initial response
2. Critique it internally
3. Revise if needed
4. Only THEN send the final response to the user

The user never sees the internal thinking - they only get the polished final response.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .autonomous.scratchpad import Scratchpad
from .autonomous.scratchpad_archiver import ScratchpadArchiver
from .lightweight_constitutional_client import LightweightConstitutionalClient

logger = logging.getLogger(__name__)


class ThinkingConstitutionalClient(LightweightConstitutionalClient):
    """
    Enhanced constitutional client that thinks before responding.
    
    Adds an internal thinking stage:
    - Draft → Critique → Revise (if needed) → Send
    
    User only sees the final polished response.
    """
    
    def __init__(self, base_client, scratchpad: Optional[Scratchpad] = None, config: Optional[Dict] = None):
        """
        Initialize thinking client.
        
        Args:
            base_client: Base Ollama client
            scratchpad: Optional scratchpad instance (created if not provided)
            config: Optional configuration dict
        """
        super().__init__(base_client)
        
        # Load configuration
        self.config = config or self._load_config()
        self.thinking_enabled = self.config.get("scratchpad", {}).get("enabled", True)
        self.thinking_config = self.config.get("scratchpad", {}).get("thinking", {})
        
        # Initialize scratchpad if thinking is enabled
        if self.thinking_enabled:
            if scratchpad is None:
                storage_config = self.config.get("scratchpad", {}).get("storage", {})
                active_dir = storage_config.get("active_dir", "atles_memory/scratchpad/active")
                archive_dir = storage_config.get("archive_dir", "atles_memory/scratchpad/archive")
                self.scratchpad = Scratchpad(active_dir, archive_dir)
            else:
                self.scratchpad = scratchpad
            
            logger.info("✅ Scratchpad thinking enabled")
        else:
            self.scratchpad = None
            logger.info("ℹ️ Scratchpad thinking disabled")
    
    def _load_config(self) -> Dict:
        """Load scratchpad configuration from file."""
        config_path = Path("config/scratchpad_config.yaml")
        
        if not config_path.exists():
            logger.warning(f"Config not found at {config_path}, using defaults")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """
        Generate response with internal thinking.
        
        Flow:
        1. If scratchpad disabled or simple request → use parent's generate
        2. Start internal thought process
        3. Generate initial response (draft)
        4. Self-critique the draft
        5. Revise if needed
        6. Finalize and return ONLY the final response
        
        User never sees steps 2-5, only the final polished response.
        """
        # Skip thinking for simple requests or if disabled
        if not self.thinking_enabled or not self.scratchpad:
            return super().generate(model, prompt, **kwargs)
        
        # Check if this is a simple request that doesn't need thinking
        mode = self.config.get("scratchpad", {}).get("mode", "every_response")
        if mode == "complex_only" and self._is_simple_request(prompt):
            return super().generate(model, prompt, **kwargs)
        
        # Start internal thinking process
        self.scratchpad.start_thought(prompt)
        
        try:
            # Stage 1: Generate initial draft
            logger.debug("🤔 Thinking stage 1: Initial draft...")
            initial_response = super().generate(model, prompt, **kwargs)
            
            self.scratchpad.write_thought("initial", {
                "text": initial_response,
                "model": model,
                "confidence": self._estimate_confidence(initial_response)
            })
            
            # Stage 2: Self-critique (if enabled)
            if self.thinking_config.get("critique_enabled", True):
                logger.debug("🔍 Thinking stage 2: Self-critique...")
                critique_result = self._self_critique(initial_response, prompt, model)
                
                self.scratchpad.write_thought("critique", {
                    "text": critique_result["critique"],
                    "needs_revision": critique_result["needs_revision"],
                    "issues": critique_result.get("issues", [])
                })
                
                # Stage 3: Revision (if needed)
                if critique_result["needs_revision"]:
                    max_revisions = self.thinking_config.get("max_revisions", 2)
                    revision_count = 0
                    final_response = initial_response
                    
                    while revision_count < max_revisions and critique_result["needs_revision"]:
                        logger.debug(f"✏️ Thinking stage 3: Revision {revision_count + 1}...")
                        
                        # Generate revision
                        revision_prompt = self._create_revision_prompt(prompt, final_response, critique_result["critique"])
                        final_response = super().generate(model, revision_prompt, **kwargs)
                        
                        self.scratchpad.write_thought(f"revision_{revision_count + 1}", {
                            "text": final_response,
                            "improvements": critique_result.get("issues", [])
                        })
                        
                        # Re-critique to see if we need another revision
                        critique_result = self._self_critique(final_response, prompt, model)
                        revision_count += 1
                    
                    # Mark as key thought if multiple revisions were needed
                    if revision_count >= 2:
                        self.scratchpad.mark_key_thought("multiple_revisions")
                else:
                    final_response = initial_response
            else:
                final_response = initial_response
            
            # Stage 4: Final check (if enabled)
            if self.thinking_config.get("self_check_enabled", True):
                logger.debug("✅ Thinking stage 4: Final check...")
                final_response = self._final_check(final_response, prompt)
            
            # Record final thought
            self.scratchpad.write_thought("final", {
                "text": final_response,
                "ready": True
            })
            
            # Finalize and save to scratchpad
            self.scratchpad.finalize_thought()
            
            logger.debug("💭 Internal thinking complete, sending final response")
            return final_response
            
        except Exception as e:
            logger.error(f"Error during thinking process: {e}")
            # If thinking fails, fall back to simple generation
            if self.scratchpad.current_thought:
                self.scratchpad.finalize_thought()
            return super().generate(model, prompt, **kwargs)
    
    def _is_simple_request(self, prompt: str) -> bool:
        """Check if this is a simple request that doesn't need deep thinking."""
        simple_patterns = [
            "hi", "hello", "hey", "thanks", "thank you", "ok", "okay",
            "yes", "no", "bye", "goodbye"
        ]
        prompt_lower = prompt.lower().strip()
        
        # Very short prompts are usually simple
        if len(prompt_lower) < 20:
            for pattern in simple_patterns:
                if prompt_lower == pattern or prompt_lower.startswith(pattern + " "):
                    return True
        
        return False
    
    def _estimate_confidence(self, response: str) -> float:
        """
        Estimate confidence in a response.
        
        Simple heuristic based on:
        - Length (very short or very long might indicate uncertainty)
        - Hedging words ("maybe", "perhaps", "I think")
        - Completeness
        """
        if not response:
            return 0.0
        
        confidence = 1.0
        response_lower = response.lower()
        
        # Reduce confidence for hedging
        hedging_words = ["maybe", "perhaps", "possibly", "might", "could be", "not sure", "i think"]
        hedge_count = sum(1 for word in hedging_words if word in response_lower)
        confidence -= hedge_count * 0.1
        
        # Reduce confidence for very short responses (might be incomplete)
        if len(response) < 50:
            confidence -= 0.2
        
        # Reduce confidence for disclaimers
        if "i don't have access" in response_lower or "i cannot" in response_lower:
            confidence -= 0.15
        
        return max(0.0, min(1.0, confidence))
    
    def _self_critique(self, response: str, original_prompt: str, model: str) -> Dict:
        """
        Have ATLES critique its own response.
        
        Args:
            response: The draft response to critique
            original_prompt: The original user prompt
            model: The model being used
        
        Returns:
            Dict with critique, needs_revision flag, and issues list
        """
        # Create a meta-prompt for self-critique
        critique_prompt = f"""Review this response critically:

User asked: {original_prompt}

My draft response: {response}

Analyze this response for:
1. Accuracy - Is it correct?
2. Completeness - Does it fully answer the question?
3. Clarity - Is it easy to understand?
4. Conciseness - Is it too verbose or too brief?

Respond in this format:
NEEDS_REVISION: yes/no
ISSUES: [list any problems found]
CRITIQUE: [brief explanation]"""
        
        try:
            # Generate critique (using parent's generate to avoid recursion)
            critique_response = super().generate(model, critique_prompt, stream=False)
            
            # Parse the critique
            needs_revision = "NEEDS_REVISION: yes" in critique_response.lower()
            
            # Extract issues
            issues = []
            if "ISSUES:" in critique_response:
                issues_section = critique_response.split("ISSUES:")[1].split("CRITIQUE:")[0]
                issues = [issue.strip() for issue in issues_section.strip().split("\n") if issue.strip()]
            
            return {
                "critique": critique_response,
                "needs_revision": needs_revision,
                "issues": issues
            }
            
        except Exception as e:
            logger.error(f"Self-critique failed: {e}")
            # If critique fails, assume no revision needed
            return {
                "critique": "Critique unavailable",
                "needs_revision": False,
                "issues": []
            }
    
    def _create_revision_prompt(self, original_prompt: str, draft_response: str, critique: str) -> str:
        """Create a prompt for revising the response based on critique."""
        return f"""The user asked: {original_prompt}

I drafted this response: {draft_response}

But after reviewing it, I found these issues:
{critique}

Please provide an improved response that addresses these issues."""
    
    def _final_check(self, response: str, original_prompt: str) -> str:
        """
        Final check before sending response.
        
        Ensures:
        - Response is relevant to the prompt
        - No placeholder text left
        - Reasonable length
        """
        # Remove any thinking artifacts that might have leaked through
        response = response.replace("NEEDS_REVISION:", "").replace("CRITIQUE:", "")
        response = response.replace("ISSUES:", "").strip()
        
        # Ensure minimum quality
        if len(response) < 10:
            logger.warning("Response too short, might be incomplete")
        
        return response
    
    def mark_user_correction(self, reason: str = "user_correction"):
        """
        Mark the last thought as a key thought due to user correction.
        
        Call this when the user corrects ATLES's response.
        """
        if self.scratchpad and self.scratchpad.current_thought:
            self.scratchpad.mark_key_thought(reason)
            logger.info(f"Marked as key thought: {reason}")
    
    def get_thinking_stats(self) -> Dict:
        """Get statistics about the thinking process."""
        if not self.scratchpad:
            return {"enabled": False}
        
        stats = self.scratchpad.get_session_stats()
        stats["enabled"] = True
        stats["config"] = self.thinking_config
        
        return stats


def create_thinking_constitutional_client(user_id: str = "thinking_user") -> ThinkingConstitutionalClient:
    """
    Factory function to create a thinking constitutional client.
    
    This wraps the lightweight constitutional client with scratchpad thinking.
    """
    try:
        # Import and create base client
        from .ollama_client_enhanced import OllamaFunctionCaller
        base_client = OllamaFunctionCaller()
        
        # Wrap with thinking capability
        thinking_client = ThinkingConstitutionalClient(base_client)
        
        logger.info("✅ Thinking constitutional client created successfully")
        return thinking_client
        
    except Exception as e:
        logger.error(f"Failed to create thinking constitutional client: {e}")
        raise


if __name__ == "__main__":
    # Test the thinking client
    print("🧠 Testing Thinking Constitutional Client")
    print("=" * 60)
    
    try:
        client = create_thinking_constitutional_client()
        
        # Test with a question that might need revision
        test_prompt = "What is the capital of France?"
        
        print(f"\n📝 User: {test_prompt}")
        print("🤔 ATLES is thinking internally...")
        print("   (Draft → Critique → Revise if needed → Finalize)")
        print()
        
        response = client.generate("llama3.2", test_prompt)
        
        print(f"💬 ATLES: {response}")
        print()
        
        # Show thinking stats
        stats = client.get_thinking_stats()
        print(f"📊 Thinking Stats: {stats}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


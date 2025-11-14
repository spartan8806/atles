"""
ATLES Ollama Client - Synchronous Version

Synchronous client to communicate with Ollama models.
This version should work better with Streamlit.
"""

import requests
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClientSync:
    """Synchronous client for communicating with Ollama models."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        
        # CRITICAL FIX: Session isolation to prevent context mixing
        self.conversation_id = None
        self.message_count = 0

    def close(self):
        """Close the HTTP session."""
        if self.session:
            self.session.close()
    
    def start_conversation(self, conversation_id: str = None):
        """
        Start a new conversation session to isolate context.
        This helps prevent context bleeding between different conversations.
        """
        import uuid
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.message_count = 0
        logger.info(f"Started new conversation session: {self.conversation_id}")
        return self.conversation_id
    
    def end_conversation(self):
        """End the current conversation session."""
        if self.conversation_id:
            logger.info(f"Ended conversation session: {self.conversation_id} ({self.message_count} messages)")
        self.conversation_id = None
        self.message_count = 0

    def list_models(self) -> list:
        """List available Ollama models."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
            else:
                logger.error(f"Failed to list models: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def generate(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using an Ollama model."""
        try:
            # CRITICAL FIX: Add context reset and cache busting to prevent context bleeding
            import random
            import time
            
            # Track message count for session isolation
            self.message_count += 1
            
            # Prepare the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                # Cache-busting parameters to force fresh response
                "options": {
                    "seed": random.randint(1, 1000000),  # Randomize seed for unique responses
                    "num_ctx": 4096,  # Explicit context window size
                    "temperature": 0.7 + random.uniform(-0.05, 0.05),  # Slight temperature variation
                }
            }
            
            # Add conversation tracking metadata if available
            if self.conversation_id:
                # Note: Ollama doesn't natively support conversation_id, but we log it
                logger.debug(f"Message {self.message_count} in conversation {self.conversation_id}")

            # Add any additional parameters (user params override defaults)
            if kwargs:
                if "options" in kwargs:
                    payload["options"].update(kwargs["options"])
                    kwargs.pop("options")
                payload.update(kwargs)

            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # CRITICAL FIX: Validate response relevance to detect context bleeding
                if not self._is_response_relevant(prompt, response_text):
                    logger.warning(f"⚠️ CONTEXT BLEEDING DETECTED: Response appears unrelated to prompt")
                    logger.warning(f"Prompt preview: {prompt[:100]}...")
                    logger.warning(f"Response preview: {response_text[:100]}...")
                    
                    # Try one more time with even more aggressive cache-busting
                    logger.info("Retrying with fresh context...")
                    payload["options"]["seed"] = random.randint(1, 1000000)
                    payload["options"]["temperature"] = 0.8  # Higher temperature for diversity
                    
                    retry_response = self.session.post(
                        f"{self.base_url}/api/generate",
                        json=payload,
                        timeout=30
                    )
                    
                    if retry_response.status_code == 200:
                        retry_data = retry_response.json()
                        response_text = retry_data.get("response", "")
                        logger.info("✅ Retry successful")
                
                return response_text
            else:
                logger.error(f"Generation failed: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    def _is_response_relevant(self, prompt: str, response: str) -> bool:
        """
        Check if response appears relevant to the prompt.
        Detects obvious context bleeding cases.
        """
        if not response or len(response) < 20:
            return True  # Too short to judge
        
        # Extract key nouns/topics from prompt (simple heuristic)
        prompt_lower = prompt.lower()
        response_lower = response.lower()
        
        # Check for completely unrelated response patterns
        suspicious_patterns = [
            # Logic puzzle responses when prompt is about history
            ("hittite" in prompt_lower or "bronze age" in prompt_lower or "ḫaḫḫu" in prompt_lower) and 
            ("red" in response_lower and "blue" in response_lower and "configuration" in response_lower),
            
            # Math/constraint responses when prompt is narrative
            (len(prompt) > 500 and "ATLES gave" in prompt) and 
            ("constraint" in response_lower or "satisf" in response_lower),
            
            # Generic: response talks about colors/numbers when prompt is about history/linguistics
            ("historical" in prompt_lower or "linguistic" in prompt_lower or "treaty" in prompt_lower) and
            (("red" in response_lower or "blue" in response_lower) and "configuration" in response_lower)
        ]
        
        if any(suspicious_patterns):
            return False
        
        return True  # Assume relevant if no obvious mismatch

    def chat(self, model: str, messages: list, **kwargs) -> Optional[str]:
        """Chat with an Ollama model using conversation format."""
        try:
            # CRITICAL FIX: Add cache-busting to chat endpoint as well
            import random
            
            # Prepare the request payload
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                # Cache-busting parameters
                "options": {
                    "seed": random.randint(1, 1000000),
                    "num_ctx": 4096,
                    "temperature": 0.7 + random.uniform(-0.05, 0.05),
                }
            }

            # Add any additional parameters (user params override defaults)
            if kwargs:
                if "options" in kwargs:
                    payload["options"].update(kwargs["options"])
                    kwargs.pop("options")
                payload.update(kwargs)

            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "")
            else:
                logger.error(f"Chat failed: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return None

    def is_available(self) -> bool:
        """Check if Ollama is running and available."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

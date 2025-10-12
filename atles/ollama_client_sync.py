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

    def close(self):
        """Close the HTTP session."""
        if self.session:
            self.session.close()

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
            # Prepare the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }

            # Add any additional parameters
            payload.update(kwargs)

            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                logger.error(f"Generation failed: {response.status_code}")
                logger.error(f"Error details: {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None

    def chat(self, model: str, messages: list, **kwargs) -> Optional[str]:
        """Chat with an Ollama model using conversation format."""
        try:
            # Prepare the request payload
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }

            # Add any additional parameters
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

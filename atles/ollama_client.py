"""
ATLES Ollama Client

Simple client to communicate with Ollama models.
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for communicating with Ollama models."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def list_models(self) -> list:
        """List available Ollama models."""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("models", [])
                else:
                    logger.error(f"Failed to list models: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    async def generate(self, model: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text using an Ollama model."""
        try:
            session = await self._get_session()
            
            # Prepare the request payload
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            # Add any additional parameters
            payload.update(kwargs)
            
            async with session.post(
                f"{self.base_url}/api/generate",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response", "")
                else:
                    logger.error(f"Generation failed: {response.status}")
                    error_text = await response.text()
                    logger.error(f"Error details: {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    async def chat(self, model: str, messages: list, **kwargs) -> Optional[str]:
        """Chat with an Ollama model using conversation format."""
        try:
            session = await self._get_session()
            
            # Prepare the request payload
            payload = {
                "model": model,
                "messages": messages,
                "stream": False
            }
            
            # Add any additional parameters
            payload.update(kwargs)
            
            async with session.post(
                f"{self.base_url}/api/chat",
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("message", {}).get("content", "")
                else:
                    logger.error(f"Chat failed: {response.status}")
                    error_text = await response.text()
                    logger.error(f"Error details: {error_text}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return None
    
    async def is_available(self) -> bool:
        """Check if Ollama is running and available."""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/api/tags") as response:
                return response.status == 200
        except Exception:
            return False

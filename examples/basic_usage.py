#!/usr/bin/env python3
"""
ATLES Basic Usage Example

This example demonstrates how to use ATLES programmatically
to interact with Hugging Face models.
"""

import asyncio
import logging
from pathlib import Path

# Add the parent directory to the path so we can import atles
import sys
sys.path.append(str(Path(__file__).parent.parent))

from atles.brain import ATLESBrain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main example function."""
    print("🧠 ATLES - AI Hub for Hugging Face Models")
    print("=" * 50)
    
    # Initialize the ATLES brain
    print("Initializing ATLES Brain...")
    brain = ATLESBrain()
    
    # Example 1: Download a model
    print("\n📥 Example 1: Downloading a model")
    print("-" * 30)
    
    model_id = "microsoft/DialoGPT-medium"
    print(f"Downloading {model_id}...")
    
    download_result = await brain.download_model(model_id)
    if download_result["success"]:
        print(f"✅ Model downloaded successfully!")
        print(f"   Path: {download_result['path']}")
    else:
        print(f"❌ Download failed: {download_result.get('error', 'Unknown error')}")
        return
    
    # Example 2: Start a conversation
    print("\n💬 Example 2: Starting a conversation")
    print("-" * 30)
    
    session_id = await brain.start_conversation(
        user_id="example_user",
        model_id=model_id
    )
    print(f"Session started: {session_id}")
    
    # Example 3: Chat with the model
    print("\n🤖 Example 3: Chatting with the model")
    print("-" * 30)
    
    messages = [
        "Hello! How are you today?",
        "Can you tell me a short joke?",
        "What's the weather like?",
        "Thank you for the conversation!"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\nMessage {i}: {message}")
        
        response = await brain.chat(message, session_id)
        
        if response["success"]:
            print(f"AI Response: {response['response']}")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")
    
    # Example 4: Get conversation history
    print("\n📚 Example 4: Conversation history")
    print("-" * 30)
    
    history = await brain.get_conversation_history(session_id)
    print(f"Total interactions: {len(history)}")
    
    for i, interaction in enumerate(history, 1):
        print(f"\nInteraction {i}:")
        print(f"  User: {interaction['user_message']}")
        print(f"  AI: {interaction['ai_response']}")
        print(f"  Model: {interaction['model_id']}")
    
    # Example 5: End conversation
    print("\n🔚 Example 5: Ending conversation")
    print("-" * 30)
    
    success = await brain.end_conversation(session_id)
    if success:
        print("✅ Conversation ended successfully")
    else:
        print("❌ Failed to end conversation")
    
    # Example 6: List available models
    print("\n📋 Example 6: Available models")
    print("-" * 30)
    
    models = await brain.list_available_models()
    if models:
        print("Available models:")
        for model in models:
            print(f"  • {model['model_id']} ({model.get('status', 'unknown')})")
    else:
        print("No models found")
    
    print("\n🎉 Example completed successfully!")
    print("\nTo try more features:")
    print("  • Use the CLI: python -m atles.cli interactive-chat microsoft/DialoGPT-medium")
    print("  • Generate images: python -m atles.cli generate-image stabilityai/stable-diffusion-2-1 'A beautiful sunset'")
    print("  • Process audio: python -m atles.cli process-audio openai/whisper-base audio.wav")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user.")
    except Exception as e:
        logger.error(f"Example failed: {e}")
        sys.exit(1)

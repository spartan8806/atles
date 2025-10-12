#!/usr/bin/env python3
"""
Test the Intelligent Model Router with various requests
"""

import sys
sys.path.append('.')

from atles.intelligent_model_router import IntelligentModelRouter

def test_router():
    """Test the model router with various request types"""
    
    print("🧠 Testing ATLES Intelligent Model Router")
    print("=" * 50)
    
    # Create router
    router = IntelligentModelRouter()
    
    # Test requests that should go to different models
    test_cases = [
        # Embedding tasks (should use EmbeddingGemma)
        "Find documents similar to this research paper",
        "Create embeddings for these text samples",
        "Cluster these documents by topic",
        "Analyze this document for key themes",
        "Search for information about machine learning",
        
        # Conversation tasks (should use Qwen)
        "Hello, how are you doing today?",
        "What do you think about artificial intelligence?",
        "Tell me about yourself",
        
        # Reasoning tasks (should use Qwen)
        "Why is the sky blue?",
        "Explain quantum computing to me",
        "What are the implications of climate change?",
        
        # Code generation (should prefer qwen2.5-coder)
        "Write a Python function to sort a list",
        "Create a class for managing user accounts",
        "Debug this JavaScript code",
        "Implement a binary search algorithm",
        
        # Text generation (should use Qwen)
        "Write a story about space exploration",
        "Generate a professional email template",
        "Create a blog post about AI ethics"
    ]
    
    # Available models for testing
    available_models = [
        'qwen2.5:7b', 
        'qwen2.5-coder:latest', 
        'llama3.2:3b', 
        'embeddinggemma-300m'
    ]
    
    print(f"Available models: {available_models}")
    print()
    
    # Test each request
    embedding_count = 0
    generative_count = 0
    
    for i, request in enumerate(test_cases, 1):
        print(f"Test {i:2d}: {request}")
        
        # Route the request
        decision = router.route_request(request, available_models)
        
        # Display results
        print(f"         -> Model: {decision.selected_model}")
        print(f"         -> Type: {decision.model_type.value}")
        print(f"         -> Task: {decision.task_type.value}")
        print(f"         -> Confidence: {decision.confidence:.1%}")
        print(f"         -> Reason: {decision.reasoning}")
        
        # Count model types
        if decision.model_type.value == 'embedding':
            embedding_count += 1
        else:
            generative_count += 1
        
        print()
    
    # Show statistics
    print("📊 ROUTING STATISTICS")
    print("=" * 30)
    stats = router.get_routing_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Average confidence: {stats['average_confidence']:.1%}")
    print(f"Embedding model usage: {embedding_count}")
    print(f"Generative model usage: {generative_count}")
    print()
    print("Model usage breakdown:")
    for model, count in stats['model_usage'].items():
        print(f"  {model}: {count} requests")
    print()
    print("Task distribution:")
    for task, count in stats['task_distribution'].items():
        print(f"  {task}: {count} requests")
    
    # Test specific functions
    print("\n🔍 TESTING SPECIFIC FUNCTIONS")
    print("=" * 35)
    
    # Test embedding model detection
    embedding_model = router.get_embedding_model(available_models)
    print(f"Best embedding model: {embedding_model}")
    
    # Test generative model detection
    generative_model = router.get_generative_model(available_models)
    print(f"Best generative model: {generative_model}")
    
    # Test quick embedding check
    embedding_requests = [
        "Find similar documents",
        "Hello there",
        "Create embeddings",
        "Write a story"
    ]
    
    print("\nEmbedding detection test:")
    for req in embedding_requests:
        should_embed = router.should_use_embedding_model(req)
        print(f"  '{req}' -> Use embedding: {should_embed}")

if __name__ == "__main__":
    test_router()

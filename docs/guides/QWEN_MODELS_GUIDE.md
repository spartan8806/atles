# Qwen Models Guide

## Overview

ATLES primarily uses **Qwen models** from Alibaba Cloud for its AI capabilities. These models are state-of-the-art language models that provide excellent performance for conversation, reasoning, and code generation tasks.

## 🤖 Qwen Models in ATLES

### **Primary Models**

#### 1. **Qwen2.5:7b** - Main Conversational Model
- **Size**: ~4.7 GB
- **Purpose**: Primary model for general conversations, reasoning, and question answering
- **Capabilities**:
  - Natural language understanding and generation
  - Complex reasoning and problem-solving
  - General knowledge and question answering
  - Mathematical calculations
  - Multi-turn conversations with context retention
- **Performance**: 95% task success rate
- **Resource Usage**: High (optimal GPU usage)
- **When to Use**: Default for all standard interactions, general queries, reasoning tasks

#### 2. **Qwen2.5-Coder:latest** - Specialized Coding Model  
- **Size**: ~4.7 GB
- **Purpose**: Specialized model for programming and technical tasks
- **Capabilities**:
  - Code generation in multiple languages
  - Code debugging and optimization
  - Technical documentation
  - Algorithm explanation
  - Software architecture analysis
- **Performance**: 98% confidence for coding tasks
- **Resource Usage**: High
- **When to Use**: Programming help, code review, debugging, technical analysis

#### 3. **Qwen2:7b** - Alternative Generative Model
- **Size**: ~4.4 GB
- **Purpose**: Previous generation Qwen model, backup option
- **Capabilities**:
  - General conversation
  - Text generation
  - Basic reasoning
- **When to Use**: Fallback when newer models unavailable

### **Embedding Model**

#### **EmbeddingGemma:300m**
- **Size**: ~300 MB (lightweight!)
- **Purpose**: Generate embeddings for semantic search and document analysis
- **Capabilities**:
  - Text embedding generation
  - Semantic similarity analysis
  - Document clustering
  - Search and retrieval
  - Content analysis
- **Performance**: 90% effectiveness for embedding tasks
- **Resource Usage**: Low (25-50% GPU)
- **When to Use**: Finding similar documents, semantic search, document analysis

### **Backup Models**

#### **Llama3.2:3b**
- **Size**: ~2.0 GB
- **Purpose**: Lightweight backup model for simple tasks
- **Capabilities**:
  - Basic conversation
  - Simple math
  - Lightweight queries
- **Resource Usage**: Low to medium
- **When to Use**: Only as backup when main models unavailable, or for very simple tasks

#### **Gemma3:4b**
- **Size**: ~3.3 GB  
- **Purpose**: Alternative lightweight model
- **Capabilities**: General conversation, basic reasoning
- **When to Use**: Alternative backup option

## 🧠 Intelligent Model Router

ATLES includes an **Intelligent Model Router** that automatically selects the best model for each task:

### Automatic Task Detection

```python
# Example routing decisions:
"Find similar documents" → EmbeddingGemma (95% confidence)
"What is quantum computing?" → Qwen2.5:7b (90% confidence)  
"Write a Python function" → Qwen2.5-Coder (98% confidence)
"Analyze this document" → EmbeddingGemma (90% confidence)
```

### Model Selection Strategy

1. **Pattern-based detection** - Analyzes request keywords and structure
2. **Performance-based selection** - Chooses model with best success rate
3. **Confidence scoring** - Provides transparency in routing decisions
4. **Fallback chains** - Ensures reliability if primary model unavailable

### Task Type Routing

| Task Type | Primary Model | Confidence |
|-----------|---------------|------------|
| Embedding generation | EmbeddingGemma:300m | 95% |
| Similarity analysis | EmbeddingGemma:300m | 95% |
| Document clustering | EmbeddingGemma:300m | 90% |
| Search/retrieval | EmbeddingGemma:300m | 90% |
| Conversation | Qwen2.5:7b | 90% |
| Reasoning | Qwen2.5:7b | 90% |
| Question answering | Qwen2.5:7b | 90% |
| Code generation | Qwen2.5-Coder | 98% |
| Debugging | Qwen2.5-Coder | 95% |
| Technical analysis | Qwen2.5-Coder | 95% |

## 🔧 Model Hierarchy

### Priority Order

```
1. Qwen2.5:7b (PRIMARY)
   ↓ Best for: General conversations, reasoning, questions
   
2. Qwen2.5-Coder:latest (SPECIALIST)
   ↓ Best for: Code, programming, technical tasks
   
3. Llama3.2:3b (BACKUP)
   ↓ Best for: Simple tasks, low resource situations
   
4. Gemma3:4b (ALTERNATIVE)
   ↓ Best for: Alternative backup option
```

### Fallback Chain

If primary model fails or unavailable:
```
Qwen2.5:7b → Qwen2.5-Coder:latest → Llama3.2:3b → Gemma3:4b
```

## 📦 Installation & Setup

### 1. Install Ollama

ATLES uses Ollama to manage models locally.

```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Pull Qwen Models

```bash
# Primary conversational model
ollama pull qwen2.5:7b

# Specialized coding model
ollama pull qwen2.5-coder:latest

# Embedding model
ollama pull embeddinggemma:300m

# Backup models (optional)
ollama pull llama3.2:3b
ollama pull gemma3:4b
```

### 3. Verify Installation

```bash
# List installed models
ollama list

# Should show:
# qwen2.5:7b              4.7 GB
# qwen2.5-coder:latest    4.7 GB
# embeddinggemma:300m     300 MB
# llama3.2:3b            2.0 GB
# gemma3:4b              3.3 GB
```

### 4. Start Ollama Server

```bash
# The server should auto-start, but if needed:
ollama serve
```

## 🎨 Custom ATLES Models

ATLES can create custom enhanced versions of Qwen models with:
- Direct model weight modifications
- Constitutional reasoning enhancements
- Truth-seeking capabilities
- Manipulation detection

### Create Custom Model

```bash
# Create Modelfile.atles
FROM qwen2.5:7b

# ATLES Enhanced Configuration
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM """You are ATLES (Autonomous Truth-seeking Learning Enhancement System), 
an advanced AI with enhanced constitutional reasoning, truth-seeking capabilities, 
and manipulation detection."""

# Build custom model
ollama create atles-qwen2.5:7b-enhanced -f Modelfile.atles
```

See [CUSTOM_MODEL_SETUP_INSTRUCTIONS.md](CUSTOM_MODEL_SETUP_INSTRUCTIONS.md) for detailed setup.

## 🚀 Model Performance

### Resource Usage

| Model | GPU Usage | CPU Usage | RAM Usage |
|-------|-----------|-----------|-----------|
| Qwen2.5:7b | 60-80% | 30-40% | ~6 GB |
| Qwen2.5-Coder | 60-80% | 30-40% | ~6 GB |
| EmbeddingGemma:300m | 25-50% | 15-25% | ~1 GB |
| Llama3.2:3b | 40-60% | 20-30% | ~3 GB |
| Gemma3:4b | 50-70% | 25-35% | ~4 GB |

### Speed Benchmarks

| Model | Tokens/Second | Response Time |
|-------|---------------|---------------|
| Qwen2.5:7b | 25-35 | Fast |
| Qwen2.5-Coder | 25-35 | Fast |
| EmbeddingGemma:300m | 50-100 | Very Fast |
| Llama3.2:3b | 40-50 | Very Fast |
| Gemma3:4b | 30-40 | Fast |

### Quality Ratings

| Model | Accuracy | Reasoning | Creativity | Code Quality |
|-------|----------|-----------|------------|--------------|
| Qwen2.5:7b | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Qwen2.5-Coder | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Llama3.2:3b | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Gemma3:4b | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

## 🛠️ Configuration

### Model Selection in Code

```python
from atles.intelligent_model_router import IntelligentModelRouter

router = IntelligentModelRouter()

# Automatic routing
decision = router.route_request("What is quantum computing?")
print(f"Using: {decision.selected_model}")  # qwen2.5:7b

decision = router.route_request("Write a Python function")
print(f"Using: {decision.selected_model}")  # qwen2.5-coder:latest
```

### Manual Model Selection

```python
# In Desktop App
selected_model = "qwen2.5:7b"  # Change in UI dropdown

# In configuration files
{
  "preferred_models": [
    "qwen2.5:7b",
    "qwen2.5-coder:latest",
    "llama3.2:3b"
  ]
}
```

## 📊 Model Capabilities Comparison

### Qwen2.5:7b vs Qwen2.5-Coder

| Feature | Qwen2.5:7b | Qwen2.5-Coder |
|---------|------------|---------------|
| **General Conversation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Code Generation** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Mathematical Reasoning** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Creative Writing** | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Technical Documentation** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Debugging** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Algorithm Design** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Natural Language** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔍 Troubleshooting

### Model Not Found (404 Error)

```bash
# Check if model is installed
ollama list

# If missing, pull it
ollama pull qwen2.5:7b

# Verify Ollama is running
curl http://localhost:11434
```

### Memory Issues

```
Error: model requires more system memory (4.3 GiB) than is available
```

**Solution**: Use lighter models or close other applications
```bash
# Use lighter model
ollama pull llama3.2:3b  # Only 2GB

# Or increase system memory/swap
```

### Slow Performance

- **Check GPU usage**: Qwen models perform best with GPU acceleration
- **Verify CUDA**: For NVIDIA GPUs, ensure CUDA is properly installed
- **Reduce concurrent models**: Only run one large model at a time
- **Use appropriate model**: Use Llama3.2:3b for simple tasks

### Model Selection Issues

If router selects wrong model:
1. Check task patterns in `intelligent_model_router.py`
2. Manually specify model in UI dropdown
3. Review router logs for confidence scores

## 📚 Related Documentation

- [CUSTOM_MODEL_SETUP_INSTRUCTIONS.md](CUSTOM_MODEL_SETUP_INSTRUCTIONS.md) - Create enhanced ATLES models
- [OLLAMA_INTEGRATION_GUIDE.md](OLLAMA_INTEGRATION_GUIDE.md) - Deep dive into Ollama integration
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Development with ATLES models
- [CORRECT_MODEL_HIERARCHY_SUMMARY.md](../updates/CORRECT_MODEL_HIERARCHY_SUMMARY.md) - Model priority details

## 🎯 Best Practices

1. **Use Qwen2.5:7b as default** for all general interactions
2. **Switch to Qwen2.5-Coder** when working with code
3. **Let the router decide** for optimal automatic selection
4. **Keep models updated** with `ollama pull model:tag`
5. **Monitor resource usage** to ensure optimal performance
6. **Create custom models** for specialized use cases
7. **Use EmbeddingGemma** for all semantic search tasks

## ❓ FAQ

**Q: Why Qwen instead of other models?**  
A: Qwen models offer the best balance of performance, speed, and capability for ATLES. They excel at reasoning, coding, and conversation.

**Q: Can I use other models?**  
A: Yes! ATLES supports any Ollama-compatible model. Just add it to the router configuration.

**Q: Which model is fastest?**  
A: EmbeddingGemma:300m is fastest for its tasks. For generation, Llama3.2:3b is fastest but Qwen2.5:7b offers better quality.

**Q: How much disk space do I need?**  
A: Minimum 10 GB for Qwen2.5:7b + Qwen2.5-Coder. Recommended 15 GB to include all models.

**Q: Do I need a GPU?**  
A: No, but highly recommended. Qwen models work on CPU but are much faster with GPU acceleration.

**Q: Can I run multiple models simultaneously?**  
A: Yes, but resource intensive. The router handles switching automatically for optimal performance.

---

**Last Updated**: November 2025  
**ATLES Version**: v6.0+

For questions or issues, see [OLLAMA_TROUBLESHOOTING.md](../atles_app/OLLAMA_TROUBLESHOOTING.md)


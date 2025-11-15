---
library_name: sentence-transformers
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- embeddings
- atles
- semantic-search
license: apache-2.0
pipeline_tag: sentence-similarity
---

# ATLES Embedding Model

**Advanced Thinking & Learning Execution System (ATLES) Embedding Model**

This is the embedding model powering ATLES - an advanced AI system for semantic search, document analysis, and intelligent reasoning.

## 🚀 Quick Start

```python
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("spartan8806/atles")

# Generate embeddings for queries and documents
query = "What is the ATLES system?"
documents = [
    "ATLES is an advanced AI system with episodic memory and reasoning capabilities.",
    "The system uses constitutional AI principles for safe and helpful interactions.",
    "ATLES supports multiple models including Qwen2.5 and EmbeddingGemma.",
]

# Encode queries and documents separately for optimal retrieval
query_embedding = model.encode_query(query)
document_embeddings = model.encode_document(documents)

# Compute similarities
from sentence_transformers.util import cos_sim
similarities = cos_sim(query_embedding, document_embeddings)
print(similarities)
```

## 📊 Model Details

- **Model Architecture**: Based on EmbeddingGemma-300M
- **Embedding Dimension**: 768
- **Max Sequence Length**: 2048 tokens
- **Supported Tasks**: 
  - Semantic search and retrieval
  - Document similarity
  - Text classification
  - Clustering
  - Code retrieval

## 🎯 Usage Examples

### Semantic Search

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("spartan8806/atles")

# Search query
query = "How does ATLES memory system work?"

# Document collection
docs = [
    "ATLES uses episodic semantic memory with JSON storage.",
    "Memory is organized by episodes and semantic embeddings.",
    "The system can recall past conversations and learnings."
]

# Generate embeddings
query_emb = model.encode_query(query)
doc_embs = model.encode_document(docs)

# Find most similar document
from sentence_transformers.util import cos_sim
scores = cos_sim(query_emb, doc_embs)
best_match_idx = scores.argmax()
print(f"Best match: {docs[best_match_idx]}")
```

### Text Classification

```python
model = SentenceTransformer("spartan8806/atles")

texts = [
    "This is excellent!",
    "Terrible product.",
    "Not bad, could be better."
]

embeddings = model.encode(texts, prompt_name="Classification")
# Use embeddings with your classifier
```

## 🔧 Installation

```bash
pip install sentence-transformers
```

## 📝 Model Card

This model is optimized for use with the ATLES system and provides state-of-the-art performance for embedding tasks at a compact 300M parameter size.

### Performance

- **Efficient**: 300M parameters, suitable for on-device deployment
- **Fast**: Optimized inference with Sentence-Transformers
- **Versatile**: Supports multiple task types via prompt customization

### Prompt Templates

The model supports various prompt templates for different use cases:

- **Retrieval**: `task: search result | query: {text}`
- **Document**: `title: {title} | text: {text}`
- **Classification**: `task: classification | query: {text}`
- **Clustering**: `task: clustering | query: {text}`
- **Similarity**: `task: sentence similarity | query: {text}`

## 🌐 ATLES System

This embedding model is part of the larger ATLES (Advanced Thinking & Learning Execution System) project. ATLES combines:

- **Episodic Memory**: Long-term conversation and learning storage
- **Semantic Search**: Powered by this embedding model
- **Constitutional AI**: Safe and principled AI interactions
- **Intelligent Routing**: Automatic model selection for optimal performance

## 📚 Citation

If you use this model, please cite:

```bibtex
@misc{atles2024,
  title={ATLES Embedding Model},
  author={Spartan8806},
  year={2024},
  howpublished={\url{https://huggingface.co/spartan8806/atles}}
}
```

## 📄 License

This model is released under the Apache 2.0 license.

---

**Repository**: [spartan8806/atles](https://huggingface.co/spartan8806/atles)  
**ATLES Project**: [GitHub Repository](https://github.com/spartan8806/atles)


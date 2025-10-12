# ATLES (Advanced Technical Learning & Enhancement System)

## 🧠 Overview

ATLES is a comprehensive AI knowledge management and model storage system designed for advanced technical learning and AI model organization. This repository serves as a centralized hub for AI models, curated programming datasets, and structured learning materials.

## 🏗️ System Architecture

### **📁 Core Components**

```
atles/
├── 📚 datasets/           # Curated learning datasets
│   ├── books/            # Programming book excerpts & examples
│   ├── challenges/       # Coding challenges & solutions  
│   ├── frameworks/       # Framework documentation & examples
│   └── github/           # Code snippets from repositories
├── 🤖 models/            # AI model storage & metadata
├── 🧠 memory/            # Persistent storage database
├── 🗂️ cache/            # Temporary files & caching
└── 📋 .gitignore         # Git configuration
```

## 🤖 AI Models

ATLES manages multiple state-of-the-art AI models:

### **Language Models**
- **Meta Llama 3.3-8B-Instruct** - Advanced instruction-following model
- **Google Gemma 3-270M** - Lightweight conversational model  
- **Microsoft Phi-4-mini-instruct** - Efficient instruction model
- **Microsoft Phi-3-mini** - Compact reasoning model
- **Microsoft Phi-2** - Educational fine-tuned model
- **TinyLlama 1.1B-Chat** - Ultra-lightweight chat model

### **Specialized Models**
- **Microsoft DialoGPT-medium** - Conversational AI model

### **Model Storage Features**
- **Metadata Tracking**: Each model includes `info.json` with download status and timestamps
- **Configuration Management**: Tokenizer configs, model parameters, and generation settings
- **Space Optimization**: Large model weights excluded from git (via `.gitignore`)
- **HuggingFace Integration**: Compatible with HuggingFace model format

## 📚 Knowledge Datasets

### **Programming Books** (`datasets/books/`)
Curated code examples and concepts from programming literature:
- **Design Patterns** (Gang of Four)
- **Clean Code** (Robert C. Martin)  
- **Effective Python**
- **Refactoring**

**Features:**
- Code examples with explanations
- Difficulty levels and concept tagging
- Relevance scoring system
- Multiple programming languages

### **Coding Challenges** (`datasets/challenges/`)
Structured programming problems and solutions:
- **Algorithm Problems**: Two Sum, Valid Parentheses, etc.
- **Data Structures**: Binary trees, arrays, hash maps
- **Difficulty Progression**: Easy to Hard classifications
- **Multiple Solutions**: Different approaches and optimizations

### **Framework Documentation** (`datasets/frameworks/`)
Real-world framework examples and patterns:
- **FastAPI**: CRUD operations, API design patterns
- **Web Development**: RESTful services, database integration
- **Best Practices**: Production-ready code examples

### **GitHub Code Samples** (`datasets/github/`)
Curated code snippets from open-source repositories:
- **Real-world Examples**: Production code patterns
- **Community Solutions**: Popular implementations
- **Code Quality**: Well-documented, tested examples

## 🗄️ Data Management

### **Memory System** (`memory/`)
- **SQLite Database**: Persistent storage for system state
- **Learning Progress**: Track user progress and preferences
- **Model Metadata**: Store model performance and usage statistics

### **Caching System** (`cache/`)
- **Temporary Storage**: Model loading optimization
- **Performance**: Reduce repeated computations
- **Memory Management**: Efficient resource utilization

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8+
- Git
- Sufficient disk space (~10GB for full model storage)

### **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/spartan8806/atles.git
   cd atles
   ```

2. **Install Dependencies** (if requirements.txt exists)
   ```bash
   pip install -r requirements.txt
   ```

3. **Model Setup**
   ```bash
   # Models need to be downloaded separately due to size
   # Use HuggingFace Hub or appropriate model sources
   ```

### **Usage**

This repository contains the **data layer** of the ATLES system:
- **Knowledge Base**: Access curated programming datasets
- **Model Storage**: Manage AI model metadata and configurations  
- **Learning Materials**: Browse structured educational content

> **Note**: This appears to be the **storage/data repository** for ATLES. The main application logic, brain modules, and user interfaces may be in a separate repository.

## 📊 Dataset Structure

### **Example: Programming Books Entry**
```json
{
  "id": "design_patterns_singleton",
  "book_title": "Design Patterns: Elements of Reusable Object-Oriented Software",
  "author": "Gang of Four",
  "chapter": "Creational Patterns",
  "language": "python",
  "code": "class Singleton: ...",
  "concepts": ["design-patterns", "singleton", "oop"],
  "difficulty": "intermediate",
  "relevance_score": 0.95
}
```

### **Example: Coding Challenge Entry**
```json
{
  "id": "two_sum",
  "title": "Two Sum",
  "difficulty": "easy",
  "category": "arrays",
  "problem_statement": "Find two numbers that add up to target...",
  "solution": "def two_sum(nums, target): ...",
  "time_complexity": "O(n)",
  "space_complexity": "O(n)"
}
```

## 🔧 Configuration

### **Git Configuration**
- **Large File Exclusion**: Model weights excluded from version control
- **Metadata Preservation**: Configuration files and metadata tracked
- **Repository Size**: Optimized for GitHub storage limits

### **Model Configuration**
- **HuggingFace Format**: Standard model structure
- **Tokenizer Settings**: Language-specific configurations
- **Generation Parameters**: Model-specific inference settings

## 📈 System Features

### **🎯 Educational Focus**
- **Structured Learning**: Progressive difficulty levels
- **Concept Mapping**: Tagged and categorized content
- **Real-world Examples**: Production-quality code samples

### **🤖 AI Model Management**
- **Multi-model Support**: Various model sizes and capabilities
- **Metadata Tracking**: Download status and performance metrics
- **Efficient Storage**: Optimized for large model files

### **📊 Data Organization**
- **Consistent Schema**: Standardized data formats
- **Search Optimization**: Tagged and scored content
- **Scalable Structure**: Easy to extend and modify

## 🔮 Future Enhancements

- **Model Integration**: Direct model loading and inference
- **Web Interface**: Browser-based access to datasets
- **API Endpoints**: RESTful access to knowledge base
- **Learning Analytics**: Progress tracking and recommendations
- **Collaborative Features**: Community contributions and sharing

## 📄 License

[Specify your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support information here]

---

**ATLES**: Empowering advanced technical learning through AI and structured knowledge management.
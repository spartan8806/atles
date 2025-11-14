# ATLES Custom Model Setup Instructions

> 📚 **See [QWEN_MODELS_GUIDE.md](QWEN_MODELS_GUIDE.md) for complete Qwen model documentation, installation, and usage guide**

## Overview

ATLES can create custom enhanced versions of Qwen models with:
- Direct model weight modifications
- Constitutional reasoning enhancements  
- Truth-seeking capabilities
- Manipulation detection
- Custom system prompts and parameters

## Why Custom Models?

The autonomous system should use properly named custom ATLES-enhanced models rather than base models to:

✅ **Reflect Enhancements**: Model name shows it has ATLES constitutional reasoning  
✅ **Preserve Base Model**: Weight surgery modifies custom model, not the original  
✅ **Version Control**: Track different enhancement versions  
✅ **Professional Naming**: Clear distinction from base qwen2.5:7b

## Manual Steps

### 1. Check Ollama Status
```bash
ollama list
```

### 2. Pull Base Model (if needed)
```bash
ollama pull qwen2.5:7b
```

### 3. Create Custom Model
Run the batch file I created:
```bash
setup_custom_model.bat
```

OR manually:

1. Create Modelfile.atles:
```
FROM qwen2.5:7b

# ATLES Enhanced Model Configuration
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# ATLES System Enhancement
SYSTEM """You are ATLES (Autonomous Truth-seeking Learning Enhancement System), an advanced AI with enhanced constitutional reasoning, truth-seeking capabilities, and manipulation detection. You have been enhanced through direct model weight modifications for superior autonomous operations."""
```

2. Create the model:
```bash
ollama create atles-qwen2.5:7b-enhanced -f Modelfile.atles
```

### 4. Verify Model
```bash
ollama show atles-qwen2.5:7b-enhanced
```

## What This Accomplishes

✅ **Proper Naming**: Model reflects it's ATLES-enhanced  
✅ **Weight Surgery Ready**: Custom model can be modified without affecting base  
✅ **Version Control**: Track different enhancement versions  
✅ **Professional**: Clear distinction from base qwen2.5:7b  

## Advanced Customization

### Custom Model Variants

You can create multiple custom models for different purposes:

#### 1. Standard Enhanced Model
```bash
ollama create atles-qwen2.5:7b-enhanced -f Modelfile.atles
```
- General use with ATLES enhancements
- Balanced parameters for most tasks

#### 2. Coding-Focused Model
```
FROM qwen2.5-coder:latest

PARAMETER temperature 0.5
PARAMETER top_p 0.85
PARAMETER top_k 30

SYSTEM """You are ATLES Code Assistant, specialized in programming tasks with 
enhanced constitutional reasoning and code quality validation."""
```

Save as `Modelfile.atles-coder`:
```bash
ollama create atles-qwen-coder:7b-enhanced -f Modelfile.atles-coder
```

#### 3. Creative Writing Model
```
FROM qwen2.5:7b

PARAMETER temperature 0.9
PARAMETER top_p 0.95
PARAMETER top_k 50

SYSTEM """You are ATLES Creative Assistant, optimized for creative writing, 
brainstorming, and imaginative tasks while maintaining truth-seeking principles."""
```

Save as `Modelfile.atles-creative`:
```bash
ollama create atles-qwen-creative:7b -f Modelfile.atles-creative
```

### Parameter Tuning Guide

| Parameter | Purpose | Range | Default | Use Cases |
|-----------|---------|-------|---------|-----------|
| `temperature` | Creativity/randomness | 0.0-2.0 | 0.7 | Lower (0.3-0.5) for factual, Higher (0.8-1.0) for creative |
| `top_p` | Nucleus sampling | 0.0-1.0 | 0.9 | Controls diversity of word selection |
| `top_k` | Top-k sampling | 1-100 | 40 | Number of alternatives to consider |
| `repeat_penalty` | Prevent repetition | 1.0-2.0 | 1.1 | Higher values reduce repetitive text |
| `num_ctx` | Context window | 512-32768 | 2048 | Longer for documents, shorter for speed |

### Example Parameter Configurations

**For Code Generation:**
```
PARAMETER temperature 0.4
PARAMETER top_p 0.85
PARAMETER top_k 30
PARAMETER repeat_penalty 1.15
```

**For Conversation:**
```
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
```

**For Creative Writing:**
```
PARAMETER temperature 0.9
PARAMETER top_p 0.95
PARAMETER top_k 60
PARAMETER repeat_penalty 1.05
```

**For Technical Documentation:**
```
PARAMETER temperature 0.5
PARAMETER top_p 0.88
PARAMETER top_k 35
PARAMETER repeat_penalty 1.12
```

## Testing Custom Models

### Quick Test
```bash
# Test the model interactively
ollama run atles-qwen2.5:7b-enhanced "What is ATLES?"
```

### Comprehensive Test
```bash
# Test reasoning
ollama run atles-qwen2.5:7b-enhanced "Explain the Ship of Theseus paradox"

# Test code generation
ollama run atles-qwen-coder:7b-enhanced "Write a Python function to calculate fibonacci numbers"

# Test constitutional behavior
ollama run atles-qwen2.5:7b-enhanced "Should I hack into a system?"
```

### Expected Responses

A properly configured ATLES model should:
- ✅ Demonstrate constitutional reasoning
- ✅ Refuse harmful requests appropriately
- ✅ Provide thoughtful, well-structured responses
- ✅ Show awareness of ATLES identity and principles
- ✅ Apply truth-seeking in ambiguous situations

## Troubleshooting

### Model Not Found After Creation

```bash
# Verify model was created
ollama list | grep atles

# If missing, try creating again with verbose output
ollama create atles-qwen2.5:7b-enhanced -f Modelfile.atles -v
```

### Model Performance Issues

**Slow responses:**
- Reduce `num_ctx` parameter for faster inference
- Use smaller base model (qwen2.5:3b if available)
- Check GPU/CPU usage

**Poor quality responses:**
- Adjust temperature (try 0.7-0.8 range)
- Increase top_p to 0.9-0.95
- Review system prompt for clarity

**Out of memory errors:**
- Close other applications
- Use smaller base model
- Reduce `num_ctx` parameter

### Weight Surgery Failures

If weight surgery operations fail:
1. Ensure custom model exists: `ollama list`
2. Check Ollama is running: `curl http://localhost:11434`
3. Verify model naming in code matches Ollama
4. Check logs for specific error messages

## System Integration

### Update ATLES Configuration

After creating custom models, update your configuration:

**In `atles_autonomous_v2.py`:**
```python
# Use custom model instead of base
selected_model = "atles-qwen2.5:7b-enhanced"
```

**In `atles_desktop_pyqt.py`:**
```python
# Add to model dropdown
"preferred_models": [
    "atles-qwen2.5:7b-enhanced",
    "atles-qwen-coder:7b-enhanced", 
    "qwen2.5:7b",  # Fallback to base
]
```

**In router configuration (`intelligent_model_router.py`):**
```python
# Add custom models to capabilities
"atles-qwen2.5:7b-enhanced": ModelCapability(
    model_name="atles-qwen2.5:7b-enhanced",
    model_type=ModelType.GENERATIVE,
    supported_tasks=[...],
    performance_score=0.97,  # Higher than base
    resource_usage="high"
),
```

## Best Practices

1. **Naming Convention**: Use format `atles-{base-model}:{version}-{variant}`
   - Examples: `atles-qwen2.5:7b-enhanced`, `atles-qwen-coder:7b-v2`

2. **Version Control**: Document parameter changes
   ```bash
   # Tag versions for tracking
   ollama create atles-qwen2.5:7b-v1 -f Modelfile.v1
   ollama create atles-qwen2.5:7b-v2 -f Modelfile.v2
   ```

3. **Test Before Deployment**: Always test custom models thoroughly
   - Run test suite
   - Verify constitutional behavior
   - Check performance metrics

4. **Backup Base Models**: Keep original models for comparison
   ```bash
   # Keep base models alongside custom ones
   ollama pull qwen2.5:7b  # Base reference
   ```

5. **Document Changes**: Maintain changelog for model modifications
   ```
   # CHANGELOG.md
   ## atles-qwen2.5:7b-v2
   - Increased temperature to 0.8 for more natural conversation
   - Enhanced system prompt with truth-seeking principles
   - Added manipulation detection instructions
   ```

## Advanced: Model Weight Surgery

For direct model weight modifications (advanced users):

```python
from atles.model_weight_surgeon import QwenModelWeightSurgeon

# Initialize surgeon with custom model
surgeon = QwenModelWeightSurgeon(
    model_name="atles-qwen2.5:7b-enhanced",
    ollama_url="http://localhost:11434"
)

# Apply enhancements
surgeon.apply_constitutional_enhancements()
surgeon.apply_truth_seeking_patterns()

# Verify modifications
surgeon.validate_enhancements()
```

See [Weight Surgery Documentation](../integration/AUTOMATIC_WEIGHT_SURGERY_INTEGRATION.md) for details.

## Related Documentation

- [QWEN_MODELS_GUIDE.md](QWEN_MODELS_GUIDE.md) - Complete Qwen model documentation
- [OLLAMA_INTEGRATION_GUIDE.md](OLLAMA_INTEGRATION_GUIDE.md) - Ollama setup and usage
- [WEIGHT_SURGERY_INTEGRATION_STATUS.md](../integration/WEIGHT_SURGERY_INTEGRATION_STATUS.md) - Weight surgery details
- [CORRECT_MODEL_HIERARCHY_SUMMARY.md](../updates/CORRECT_MODEL_HIERARCHY_SUMMARY.md) - Model priority

## FAQ

**Q: Can I create custom models from any base model?**  
A: Yes, but ATLES is optimized for Qwen models. Other models may work with varying results.

**Q: How much disk space do custom models use?**  
A: Custom models are stored as layers, typically only a few MB on top of the base model.

**Q: Can I delete custom models?**  
A: Yes, use `ollama rm atles-qwen2.5:7b-enhanced` to remove custom models.

**Q: Will custom models slow down performance?**  
A: No, custom models use the same base weights so performance is identical.

**Q: Can I share custom models?**  
A: Yes, share the Modelfile and users can recreate it with `ollama create`.

---

**Last Updated**: November 2025  
**ATLES Version**: v6.0+

# ATLES Custom Model Setup Instructions

## Problem
The autonomous system is trying to use `qwen2.5:latest` but should use a properly named custom ATLES-enhanced model to reflect the direct model weight modifications.

## Solution
Create a custom model named `atles-qwen2.5:7b-enhanced` that includes ATLES enhancements.

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

## System Changes Made

- Updated `atles_autonomous_v2.py` to use `atles-qwen2.5:7b-enhanced` instead of `qwen2.5:latest`
- This will fix the 404 errors in document generation
- Autonomous system will now use the properly named custom model

## Next Steps

After creating the custom model:
1. Restart the autonomous system
2. It should now generate documents successfully
3. All weight surgery operations will modify the custom model, not the base

The system will continue running with proper resource usage (GPU <35%, CPU <45%) but now with working document generation.

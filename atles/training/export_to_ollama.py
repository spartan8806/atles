#!/usr/bin/env python3
"""
Export Fine-Tuned Model to Ollama Format
Converts a fine-tuned Qwen2.5 model back to Ollama-compatible format.

This script merges the LoRA weights with the base model and creates
a Modelfile for Ollama.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def merge_lora_weights(
    base_model_path: str,
    lora_model_path: str,
    output_path: str
):
    """Merge LoRA weights with base model"""
    logger.info(f"Loading base model from: {base_model_path}")
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    logger.info(f"Loading LoRA weights from: {lora_model_path}")
    model = PeftModel.from_pretrained(base_model, lora_model_path)
    
    logger.info("Merging LoRA weights...")
    merged_model = model.merge_and_unload()
    
    logger.info(f"Saving merged model to: {output_path}")
    merged_model.save_pretrained(output_path, safe_serialization=True)
    
    # Save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    tokenizer.save_pretrained(output_path)
    
    logger.info("Model merged successfully!")
    return output_path


def create_ollama_modelfile(
    model_path: str,
    output_path: str,
    model_name: str = "atles-qwen2.5:7b-finetuned",
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    top_p: float = 0.9,
    top_k: int = 40
):
    """Create Ollama Modelfile for the fine-tuned model"""
    
    if system_prompt is None:
        system_prompt = """You are ATLES (Autonomous Truth-seeking Learning Enhancement System), an advanced AI with enhanced constitutional reasoning, truth-seeking capabilities, and manipulation detection. You have been fine-tuned for superior autonomous operations and explicit action responses."""
    
    modelfile_content = f"""FROM {model_path}

# ATLES Fine-Tuned Model Configuration
PARAMETER temperature {temperature}
PARAMETER top_p {top_p}
PARAMETER top_k {top_k}

# ATLES System Enhancement
SYSTEM \"\"\"{system_prompt}\"\"\"
"""
    
    modelfile_path = Path(output_path)
    modelfile_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(modelfile_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    logger.info(f"Created Modelfile at: {modelfile_path}")
    return modelfile_path


def export_to_ollama(
    finetuned_model_path: str,
    base_model_name: str = "Qwen/Qwen2.5-7B-Instruct",
    output_dir: str = "./ollama_export",
    model_name: str = "atles-qwen2.5:7b-finetuned",
    system_prompt: Optional[str] = None
):
    """Complete export process: merge LoRA and create Ollama Modelfile"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load base model and merge LoRA
    logger.info("Step 1: Merging LoRA weights with base model...")
    merged_model_path = output_dir / "merged_model"
    
    # Check if LoRA model exists
    finetuned_path = Path(finetuned_model_path)
    if not finetuned_path.exists():
        logger.error(f"Fine-tuned model path not found: {finetuned_model_path}")
        return None
    
    # Merge LoRA weights
    merge_lora_weights(
        base_model_path=base_model_name,
        lora_model_path=str(finetuned_path),
        output_path=str(merged_model_path)
    )
    
    # Step 2: Create Modelfile
    logger.info("Step 2: Creating Ollama Modelfile...")
    modelfile_path = output_dir / "Modelfile"
    create_ollama_modelfile(
        model_path=str(merged_model_path),
        output_path=str(modelfile_path),
        model_name=model_name,
        system_prompt=system_prompt
    )
    
    # Step 3: Create instructions file
    instructions_path = output_dir / "OLLAMA_EXPORT_INSTRUCTIONS.md"
    instructions = f"""# Ollama Export Instructions

## Model Export Complete!

Your fine-tuned model has been exported and is ready for Ollama.

## Files Created:
- `merged_model/` - Merged model weights (LoRA + base)
- `Modelfile` - Ollama Modelfile for creating the model

## Next Steps:

### Option 1: Use Ollama Import (Recommended)
If you have Ollama's import functionality:

```bash
ollama import {merged_model_path}
```

### Option 2: Manual Conversion
1. Convert the merged model to GGUF format using llama.cpp or similar tools
2. Create the model in Ollama:

```bash
ollama create {model_name} -f Modelfile
```

### Option 3: Use Ollama's Python API
You can use Ollama's Python API to load the model directly.

## Model Information:
- Base Model: {base_model_name}
- Fine-tuned Model: {finetuned_model_path}
- Export Name: {model_name}
- Export Location: {output_dir}

## Testing:
After importing to Ollama, test with:

```bash
ollama run {model_name} "What is the Principle of Explicit Action?"
```

## Notes:
- The merged model is in HuggingFace format
- You may need to convert to GGUF for optimal Ollama performance
- The Modelfile includes ATLES-specific system prompts and parameters
"""
    
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    logger.info(f"Export complete! See {instructions_path} for next steps")
    logger.info(f"Exported model to: {output_dir}")
    
    return output_dir


def main():
    parser = argparse.ArgumentParser(description="Export fine-tuned model to Ollama format")
    parser.add_argument("--finetuned-model", type=str, required=True,
                       help="Path to fine-tuned model (LoRA weights)")
    parser.add_argument("--base-model", type=str, default="Qwen/Qwen2.5-7B-Instruct",
                       help="Base model name or path")
    parser.add_argument("--output-dir", type=str, default="./ollama_export",
                       help="Output directory for exported model")
    parser.add_argument("--model-name", type=str, default="atles-qwen2.5:7b-finetuned",
                       help="Name for the Ollama model")
    parser.add_argument("--system-prompt", type=str,
                       help="Custom system prompt (optional)")
    
    args = parser.parse_args()
    
    export_to_ollama(
        finetuned_model_path=args.finetuned_model,
        base_model_name=args.base_model,
        output_dir=args.output_dir,
        model_name=args.model_name,
        system_prompt=args.system_prompt
    )


if __name__ == "__main__":
    main()


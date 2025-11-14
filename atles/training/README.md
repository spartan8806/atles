# ATLES Model Fine-Tuning

Fine-tuning tools for the ATLES Qwen2.5:7B model.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements_finetune.txt

# 2. Prepare training data
python prepare_training_data.py --output ./training_data/atles_training_data.jsonl

# 3. Fine-tune the model
python finetune_qwen.py --config finetune_config.json

# 4. Export to Ollama
python export_to_ollama.py --finetuned-model ./finetuned_models/atles_qwen2.5_7b
```

## Files

- **`finetune_qwen.py`** - Main fine-tuning script with LoRA support
- **`prepare_training_data.py`** - Data preparation utilities
- **`export_to_ollama.py`** - Export fine-tuned model to Ollama format
- **`finetune_config.json`** - Configuration file
- **`requirements_finetune.txt`** - Python dependencies
- **`FINETUNING_GUIDE.md`** - Complete documentation

## Features

- ✅ LoRA-based efficient fine-tuning
- ✅ Support for instruction-following datasets
- ✅ Automatic data preparation from conversations
- ✅ Export to Ollama format
- ✅ Configurable training parameters
- ✅ GPU memory optimization

## Requirements

- Python 3.8+
- CUDA-capable GPU (16GB+ VRAM recommended)
- ~30GB disk space

See `FINETUNING_GUIDE.md` for detailed instructions.


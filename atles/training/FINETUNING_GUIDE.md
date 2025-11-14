# ATLES Qwen2.5:7B Fine-Tuning Guide

Complete guide for fine-tuning the ATLES Qwen2.5:7B model to improve performance on specific tasks or domains.

## Overview

This fine-tuning system uses **LoRA (Low-Rank Adaptation)** for efficient training, allowing you to fine-tune the model without requiring massive computational resources. The fine-tuned model can then be exported back to Ollama format for use with your ATLES system.

## Prerequisites

1. **Python 3.8+** installed
2. **CUDA-capable GPU** (recommended, 16GB+ VRAM for 7B model)
3. **HuggingFace account** (for downloading base model)
4. **Sufficient disk space** (~30GB for model + training data)

## Installation

### 1. Install Dependencies

```bash
cd atles/training
pip install -r requirements_finetune.txt
```

### 2. Authenticate with HuggingFace (if needed)

```bash
huggingface-cli login
```

## Quick Start

### Step 1: Prepare Training Data

Create training data in JSONL format (one example per line):

```json
{"instruction": "What is the capital of France?", "input": "", "output": "The capital of France is Paris."}
{"instruction": "Search for Python tutorials.", "input": "", "output": "SEARCH[Python tutorials]"}
```

Or use the data preparation script:

```bash
python prepare_training_data.py \
    --sources path/to/conversations.json \
    --output ./training_data/atles_training_data.jsonl
```

### Step 2: Fine-Tune the Model

```bash
python finetune_qwen.py \
    --train-data ./training_data/atles_training_data.jsonl \
    --output-dir ./finetuned_models/atles_qwen2.5_7b \
    --epochs 3 \
    --batch-size 4 \
    --learning-rate 2e-4
```

Or use a config file:

```bash
python finetune_qwen.py --config finetune_config.json
```

### Step 3: Export to Ollama Format

```bash
python export_to_ollama.py \
    --finetuned-model ./finetuned_models/atles_qwen2.5_7b \
    --output-dir ./ollama_export \
    --model-name atles-qwen2.5:7b-finetuned
```

## Detailed Usage

### Training Data Format

Training data should be in JSONL format with the following structure:

```json
{
  "instruction": "The task or question",
  "input": "Optional additional context",
  "output": "The desired response"
}
```

**Example:**
```json
{"instruction": "What function searches for code?", "input": "", "output": "SEARCH_CODE[query='your query', language='python']"}
```

### Configuration Options

Edit `finetune_config.json` or pass command-line arguments:

- **`base_model`**: Base model to fine-tune (default: "Qwen/Qwen2.5-7B-Instruct")
- **`lora_r`**: LoRA rank (higher = more capacity, default: 16)
- **`lora_alpha`**: LoRA alpha (default: 32)
- **`num_epochs`**: Training epochs (default: 3)
- **`batch_size`**: Batch size per device (default: 4)
- **`learning_rate`**: Learning rate (default: 2e-4)
- **`max_seq_length`**: Maximum sequence length (default: 2048)

### Training Tips

1. **Start Small**: Begin with 1-2 epochs to test your setup
2. **Monitor Loss**: Watch training loss - it should decrease steadily
3. **Validation Split**: Use 10-20% of data for validation
4. **Learning Rate**: Lower learning rates (1e-4 to 5e-4) work well for LoRA
5. **Batch Size**: Adjust based on GPU memory (use gradient accumulation if needed)

### Memory Optimization

If you run out of GPU memory:

1. **Reduce batch size**: Set `batch_size` to 1 or 2
2. **Increase gradient accumulation**: Set `gradient_accumulation_steps` to 8 or 16
3. **Use gradient checkpointing**: Already enabled by default
4. **Reduce sequence length**: Lower `max_seq_length` to 1024 or 512

## Advanced Usage

### Custom LoRA Configuration

Edit the LoRA settings in `finetune_config.json`:

```json
{
  "lora_r": 32,
  "lora_alpha": 64,
  "lora_dropout": 0.1,
  "lora_target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]
}
```

### Multi-GPU Training

Use `accelerate` for multi-GPU training:

```bash
accelerate config  # Configure your setup
accelerate launch finetune_qwen.py --config finetune_config.json
```

### Using Existing Conversations

Convert ATLES conversation logs to training data:

```bash
python prepare_training_data.py \
    --sources \
        ../atles_memory/conversations.json \
        ../atles_app/atles_memory/core_memory.json \
    --output ./training_data/atles_training_data.jsonl
```

## Exporting to Ollama

After fine-tuning, export the model:

```bash
python export_to_ollama.py \
    --finetuned-model ./finetuned_models/atles_qwen2.5_7b \
    --base-model Qwen/Qwen2.5-7B-Instruct \
    --output-dir ./ollama_export \
    --model-name atles-qwen2.5:7b-finetuned \
    --system-prompt "Your custom system prompt here"
```

The export process:
1. Merges LoRA weights with base model
2. Creates Ollama Modelfile
3. Generates instructions for importing to Ollama

**Note**: You may need to convert the merged model to GGUF format for optimal Ollama performance. Use tools like `llama.cpp` for conversion.

## Troubleshooting

### Out of Memory Errors

- Reduce `batch_size` to 1
- Increase `gradient_accumulation_steps`
- Reduce `max_seq_length`
- Use `fp16: true` (already enabled)

### Model Not Improving

- Check training data quality
- Increase number of epochs
- Adjust learning rate (try 1e-4 or 5e-4)
- Increase LoRA rank (`lora_r`)

### Export Issues

- Ensure base model path is correct
- Check that LoRA weights exist
- Verify disk space for merged model

## Example Training Scenarios

### Scenario 1: Improve Function Calling

**Goal**: Make model better at providing explicit function calls

**Training Data Focus**:
- Examples of correct function call syntax
- Principle of Explicit Action examples
- Function call patterns

**Config**:
```json
{
  "num_epochs": 5,
  "learning_rate": 2e-4,
  "lora_r": 16
}
```

### Scenario 2: Domain-Specific Knowledge

**Goal**: Improve knowledge in specific domain (e.g., Python programming)

**Training Data Focus**:
- Domain-specific Q&A pairs
- Code examples and explanations
- Best practices

**Config**:
```json
{
  "num_epochs": 3,
  "learning_rate": 1e-4,
  "lora_r": 32
}
```

### Scenario 3: Conversational Style

**Goal**: Match specific conversational style or tone

**Training Data Focus**:
- Example conversations
- Style examples
- Tone and format

**Config**:
```json
{
  "num_epochs": 4,
  "learning_rate": 2e-4,
  "lora_r": 16
}
```

## Best Practices

1. **Quality over Quantity**: Better to have 1000 high-quality examples than 10000 poor ones
2. **Diverse Examples**: Include various types of tasks and scenarios
3. **Validation Set**: Always reserve some data for validation
4. **Iterative Training**: Start small, evaluate, then expand
5. **Save Checkpoints**: Use `save_steps` to save intermediate checkpoints
6. **Monitor Metrics**: Track loss, perplexity, and task-specific metrics

## Resources

- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Qwen2.5 Documentation](https://github.com/QwenLM/Qwen2.5)
- [HuggingFace PEFT](https://huggingface.co/docs/peft)
- [Ollama Documentation](https://ollama.ai/docs)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review training logs
3. Verify data format
4. Check GPU memory usage

## Next Steps

After fine-tuning:
1. Export model to Ollama format
2. Test the fine-tuned model
3. Compare with base model
4. Iterate based on results
5. Deploy to production ATLES system


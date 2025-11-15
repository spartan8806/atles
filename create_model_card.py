#!/usr/bin/env python3
"""
Create a proper model card (README.md) for Hugging Face model repository
"""

model_card_content = """---
license: apache-2.0
base_model: Qwen/Qwen2.5-7B-Instruct
tags:
- atles
- qwen
- fine-tuned
- conversational-ai
- autonomous-agent
- lora
datasets:
- custom
language:
- en
pipeline_tag: text-generation
---

# ATLES Large Model

## Model Description

ATLES (Advanced Thinking & Learning Execution System) Large is a fine-tuned version of Qwen2.5-7B-Instruct, optimized for autonomous AI agent tasks, conversational interactions, and complex reasoning.

## Training Details

### Base Model
- **Base Model**: Qwen/Qwen2.5-7B-Instruct
- **Architecture**: Transformer-based causal language model
- **Parameters**: 7B

### Fine-Tuning Method
- **Method**: LoRA (Low-Rank Adaptation)
- **LoRA Rank**: 16
- **LoRA Alpha**: 32
- **LoRA Dropout**: 0.08
- **Target Modules**: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj

### Training Configuration
- **Learning Rate**: 1.5e-5
- **Batch Size**: 1 (per device)
- **Gradient Accumulation Steps**: 16
- **Effective Batch Size**: 16
- **Training Epochs**: 2
- **Max Sequence Length**: 4096
- **Weight Decay**: 0.05
- **Warmup Steps**: 150
- **Precision**: FP16

### Training Data
- **Dataset**: Custom ATLES training data (v2)
- **Total Examples**: 6,487
- **Training Examples**: 5,838
- **Validation Examples**: 649
- **Sources**: 
  - ATLES memory snippets
  - Documentation guides
  - System architecture docs
  - Bug reports and fixes

## Usage

### Using Transformers

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "spartan8806/atles-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Example usage
prompt = "What is ATLES?"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

### Using Sentence Transformers (if applicable)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("spartan8806/atles-large")
embeddings = model.encode("Your text here")
```

## Model Capabilities

- **Conversational AI**: Natural, context-aware conversations
- **Autonomous Reasoning**: Complex multi-step problem solving
- **Code Generation**: Python, JavaScript, and other languages
- **Documentation Understanding**: Technical documentation comprehension
- **Memory Integration**: Episodic and semantic memory management
- **Task Planning**: Autonomous task decomposition and execution

## Limitations

- Model is fine-tuned primarily on English text
- May require additional fine-tuning for domain-specific tasks
- Large model size requires significant GPU memory
- Response quality depends on prompt quality and context

## Evaluation

Model performance can be evaluated using MTEB (Massive Text Embedding Benchmark) for embedding tasks, or standard language modeling metrics for generation tasks.

```bash
mteb run -m spartan8806/atles-large --tasks "*" --output_folder mteb_results
```

## Citation

If you use this model, please cite:

```bibtex
@software{atles2025,
  title={ATLES: Advanced Thinking & Learning Execution System},
  author={Spartan8806},
  year={2025},
  url={https://huggingface.co/spartan8806/atles-large}
}
```

## License

This model is licensed under Apache 2.0.

## Contact

- **Repository**: https://github.com/spartan8806/atles
- **Hugging Face**: https://huggingface.co/spartan8806/atles-large
- **Issues**: Please report issues on the GitHub repository

## Acknowledgments

- Built on top of Qwen2.5-7B-Instruct by Alibaba Cloud
- Fine-tuned using Hugging Face Transformers and PEFT
- Training infrastructure powered by ATLES autonomous system
"""

if __name__ == "__main__":
    output_file = "MODEL_CARD.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(model_card_content)
    print(f"✅ Model card created: {output_file}")
    print("📝 Review and customize the model card, then upload it to your Hugging Face repository.")


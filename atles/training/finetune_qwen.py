#!/usr/bin/env python3
"""
ATLES Qwen2.5:7B Fine-Tuning Script
Fine-tunes the Qwen2.5:7B model using LoRA (Low-Rank Adaptation) for efficient training.

This script allows you to fine-tune the model on custom datasets to improve
performance on specific tasks or domains.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import load_dataset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class FineTuneConfig:
    """Configuration for fine-tuning"""
    # Model settings
    base_model: str = "Qwen/Qwen2.5-7B-Instruct"
    output_dir: str = "./finetuned_models/atles_qwen2.5_7b"
    
    # LoRA settings (efficient fine-tuning)
    lora_r: int = 16  # LoRA rank
    lora_alpha: int = 32  # LoRA alpha
    lora_dropout: float = 0.05
    lora_target_modules: List[str] = None  # Will default to ["q_proj", "k_proj", "v_proj", "o_proj"]
    
    # Training settings
    num_epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-4
    warmup_steps: int = 100
    max_seq_length: int = 2048
    
    # Data settings
    train_data_path: str = "./training_data/atles_training_data.jsonl"
    validation_data_path: Optional[str] = None
    validation_split: float = 0.1
    
    # Other settings
    save_steps: int = 500
    eval_steps: int = 500
    logging_steps: int = 100
    save_total_limit: int = 3
    fp16: bool = True
    gradient_checkpointing: bool = True
    
    def __post_init__(self):
        if self.lora_target_modules is None:
            self.lora_target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


class ATLESTrainingDataset(Dataset):
    """Dataset for ATLES fine-tuning data"""
    
    def __init__(self, data_path: str, tokenizer, max_length: int = 2048):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data = self._load_data(data_path)
        
    def _load_data(self, data_path: str) -> List[Dict[str, str]]:
        """Load training data from JSONL file"""
        data = []
        path = Path(data_path)
        
        if not path.exists():
            logger.warning(f"Training data file not found: {data_path}")
            logger.info("Creating sample training data...")
            self._create_sample_data(data_path)
            path = Path(data_path)
        
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Skipping invalid JSON line: {e}")
        
        logger.info(f"Loaded {len(data)} training examples from {data_path}")
        return data
    
    def _create_sample_data(self, data_path: str):
        """Create sample training data if none exists"""
        Path(data_path).parent.mkdir(parents=True, exist_ok=True)
        
        sample_data = [
            {
                "instruction": "What is the capital of France?",
                "input": "",
                "output": "The capital of France is Paris."
            },
            {
                "instruction": "Explain the Principle of Explicit Action.",
                "input": "",
                "output": "The Principle of Explicit Action states that I must provide specific function calls when asked for actions, never substitute meta-commentary for executable commands, and use function calls as the primary way to demonstrate understanding."
            },
            {
                "instruction": "Search for information about Python web frameworks.",
                "input": "",
                "output": "SEARCH[Python web frameworks]"
            },
            {
                "instruction": "What function would you use to find code examples?",
                "input": "",
                "output": "SEARCH_CODE[query='code examples', language='python']"
            }
        ]
        
        with open(data_path, 'w', encoding='utf-8') as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"Created sample training data at {data_path}")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        
        # Format as instruction-following prompt
        if item.get("input"):
            prompt = f"### Instruction:\n{item['instruction']}\n\n### Input:\n{item['input']}\n\n### Response:\n"
        else:
            prompt = f"### Instruction:\n{item['instruction']}\n\n### Response:\n"
        
        response = item['output']
        
        # Tokenize
        full_text = prompt + response
        
        # Tokenize with special handling for instruction-following
        encoding = self.tokenizer(
            full_text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        # Create labels (mask prompt tokens with -100)
        prompt_encoding = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        prompt_length = prompt_encoding['input_ids'].shape[1]
        labels = encoding['input_ids'].clone()
        labels[:, :prompt_length] = -100  # Mask prompt tokens
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': labels.squeeze()
        }


def setup_model_and_tokenizer(config: FineTuneConfig):
    """Setup model and tokenizer for fine-tuning"""
    logger.info(f"Loading base model: {config.base_model}")
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(config.base_model, trust_remote_code=True)
    
    # Set pad token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Load model with device_map for automatic GPU memory handling
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        trust_remote_code=True,
        torch_dtype=torch.float16 if config.fp16 else torch.float32,
        device_map="auto",
        load_in_4bit=False,  # Keep False for now, set to True if memory issues
    )
    
    # Prepare model for LoRA training
    if config.gradient_checkpointing:
        model = prepare_model_for_kbit_training(model)
        model.gradient_checkpointing_enable()
    
    # Configure LoRA
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=config.lora_target_modules,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )
    
    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    return model, tokenizer


def train_model(config: FineTuneConfig):
    """Main training function"""
    logger.info("=" * 60)
    logger.info("ATLES Qwen2.5:7B Fine-Tuning")
    logger.info("=" * 60)
    
    # Setup model and tokenizer
    model, tokenizer = setup_model_and_tokenizer(config)
    
    # Load datasets
    train_dataset = ATLESTrainingDataset(
        config.train_data_path,
        tokenizer,
        max_length=config.max_seq_length
    )
    
    # Split validation if needed
    if config.validation_data_path:
        val_dataset = ATLESTrainingDataset(
            config.validation_data_path,
            tokenizer,
            max_length=config.max_seq_length
        )
    elif config.validation_split > 0:
        train_size = int((1 - config.validation_split) * len(train_dataset))
        val_size = len(train_dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(
            train_dataset, [train_size, val_size]
        )
    else:
        val_dataset = None
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_steps=config.warmup_steps,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_steps=config.eval_steps if val_dataset else None,
        eval_strategy="steps" if val_dataset else "no",  # Changed from evaluation_strategy
        save_total_limit=config.save_total_limit,
        fp16=config.fp16,
        gradient_checkpointing=config.gradient_checkpointing,
        report_to="none",  # Can change to "tensorboard" or "wandb"
        load_best_model_at_end=True if val_dataset else False,
        metric_for_best_model="loss" if val_dataset else None,
        ddp_find_unused_parameters=False,
        optim="paged_adamw_32bit",  # Use paged optimizer for large models
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
    )
    
    # Train
    logger.info("Starting training...")
    trainer.train()
    
    # Save final model
    logger.info(f"Saving final model to {config.output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(config.output_dir)
    
    # Save config
    config_path = Path(config.output_dir) / "finetune_config.json"
    with open(config_path, 'w') as f:
        json.dump(asdict(config), f, indent=2)
    
    logger.info("Fine-tuning complete!")
    logger.info(f"Model saved to: {config.output_dir}")
    logger.info("Next step: Use export_to_ollama.py to convert to Ollama format")


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Qwen2.5:7B model for ATLES")
    parser.add_argument("--config", type=str, help="Path to config JSON file")
    parser.add_argument("--train-data", type=str, help="Path to training data JSONL file")
    parser.add_argument("--output-dir", type=str, help="Output directory for fine-tuned model")
    parser.add_argument("--epochs", type=int, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, help="Batch size")
    parser.add_argument("--learning-rate", type=float, help="Learning rate")
    
    args = parser.parse_args()
    
    # Load config
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            config_dict = json.load(f)
        config = FineTuneConfig(**config_dict)
    else:
        config = FineTuneConfig()
    
    # Override with command line args
    if args.train_data:
        config.train_data_path = args.train_data
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.epochs:
        config.num_epochs = args.epochs
    if args.batch_size:
        config.batch_size = args.batch_size
    if args.learning_rate:
        config.learning_rate = args.learning_rate
    
    # Run training
    train_model(config)


if __name__ == "__main__":
    main()


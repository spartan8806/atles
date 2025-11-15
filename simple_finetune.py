"""
Minimal embedding fine-tuning script - no sentence-transformers dependencies
Uses basic transformers + datasets to fine-tune for embeddings
"""
import json
from pathlib import Path
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModel, TrainingArguments, Trainer
import torch
import torch.nn.functional as F

print("Loading base model: sentence-transformers/all-MiniLM-L6-v2")
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

print("Loading training data...")
# Load STS-B dataset
dataset = load_dataset("sentence-transformers/stsb", split="train[:5000]")  # Small subset

def tokenize_function(examples):
    # Tokenize pairs
    return tokenizer(
        examples['sentence1'],
        examples['sentence2'],
        padding='max_length',
        truncation=True,
        max_length=128
    )

print("Tokenizing dataset...")
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./finetuned_models/atles_mini_embedding",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    save_steps=500,
    save_total_limit=2,
    logging_steps=100,
    learning_rate=2e-5,
    warmup_steps=100,
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

print("Starting training...")
trainer.train()

print("Saving model...")
model.save_pretrained("./finetuned_models/atles_mini_embedding")
tokenizer.save_pretrained("./finetuned_models/atles_mini_embedding")

print("\nDone! Model saved to: ./finetuned_models/atles_mini_embedding")
print("You can now test it with MTEB")

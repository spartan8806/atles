#!/usr/bin/env python3
"""
Low-memory fine-tuning for Qwen3-Embedding-4B using 8-bit optimizer
"""

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from sentence_transformers import SentenceTransformer, losses, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from torch.utils.data import DataLoader
from datasets import load_dataset
import torch
import bitsandbytes as bnb

print("Loading model...")
model = SentenceTransformer("Qwen/Qwen3-Embedding-4B", device="cuda")

print("Loading data...")
stsb = load_dataset("sentence-transformers/stsb", split="train")
train_examples = [
    InputExample(texts=[d['sentence1'], d['sentence2']], label=d['score']/5.0)
    for d in stsb
]
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=4)

stsb_eval = load_dataset("sentence-transformers/stsb", split="validation")
eval_examples = [
    InputExample(texts=[d['sentence1'], d['sentence2']], label=d['score']/5.0)
    for d in stsb_eval
]
evaluator = EmbeddingSimilarityEvaluator.from_input_examples(eval_examples, name='sts-dev')

train_loss = losses.CosineSimilarityLoss(model)

print("Starting training with 8-bit Adam optimizer...")
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    evaluator=evaluator,
    epochs=3,
    warmup_steps=100,
    output_path="./models/atles_finetuned_embedding",
    optimizer_class=bnb.optim.Adam8bit,
    optimizer_params={'lr': 2e-5},
    use_amp=True
)

print("Training complete! Model saved to ./models/atles_finetuned_embedding")

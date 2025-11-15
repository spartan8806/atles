#!/usr/bin/env python3
"""
ATLES Embedding Model Fine-Tuning Script
Fine-tune Qwen3-Embedding-4B for optimal ATLES embedding performance

This script fine-tunes the embedding model using sentence pairs and 
contrastive learning to improve semantic similarity detection.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import torch
from torch.utils.data import DataLoader
from sentence_transformers import (
    SentenceTransformer, 
    InputExample, 
    losses,
    evaluation,
    util
)
from sentence_transformers.datasets import SentenceLabelDataset
from datasets import load_dataset
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EmbeddingFineTuneConfig:
    """Configuration for embedding model fine-tuning"""
    # Model settings
    base_model: str = "Qwen/Qwen3-Embedding-4B"
    output_dir: str = "./finetuned_models/atles_qwen3_embedding_4b"
    
    # Training settings
    num_epochs: int = 3
    batch_size: int = 16
    warmup_steps: int = 500
    learning_rate: float = 2e-5
    max_seq_length: int = 512
    
    # Data settings
    use_sts_benchmark: bool = True
    use_nli_data: bool = True
    use_custom_atles_data: bool = True
    custom_data_path: Optional[str] = "./training_data/atles_embedding_pairs.jsonl"
    
    # Evaluation
    eval_steps: int = 1000
    save_steps: int = 1000
    
    # Hardware
    fp16: bool = True
    device: str = "cuda"  # Force GPU usage


class ATLESEmbeddingFineTuner:
    """Fine-tune embedding models for ATLES tasks"""
    
    def __init__(self, config: EmbeddingFineTuneConfig):
        self.config = config
        self.model = None
        self.train_examples = []
        self.eval_examples = []
        
    def load_model(self):
        """Load the base embedding model"""
        logger.info(f"Loading model: {self.config.base_model}")
        logger.info(f"Target device: {self.config.device}")
        
        try:
            # Load model with explicit device setting
            self.model = SentenceTransformer(
                self.config.base_model,
                device=self.config.device
            )
            
            # Set max sequence length
            if hasattr(self.model, 'max_seq_length'):
                self.model.max_seq_length = self.config.max_seq_length
            
            logger.info(f"Model loaded successfully on {self.model.device}")
            logger.info(f"Max sequence length: {self.config.max_seq_length}")
            
            # Check GPU memory
            if self.config.device == "cuda" and torch.cuda.is_available():
                logger.info(f"GPU: {torch.cuda.get_device_name(0)}")
                logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def prepare_sts_benchmark_data(self):
        """Load and prepare STS Benchmark training data"""
        logger.info("Loading STS Benchmark dataset...")
        
        try:
            # Load STS-B dataset
            dataset = load_dataset("sentence-transformers/stsb")
            
            # Convert to InputExample format
            for split in ['train', 'validation']:
                data = dataset[split]
                for item in data:
                    score = float(item['score']) / 5.0  # Normalize to 0-1
                    example = InputExample(
                        texts=[item['sentence1'], item['sentence2']], 
                        label=score
                    )
                    if split == 'train':
                        self.train_examples.append(example)
                    else:
                        self.eval_examples.append(example)
            
            logger.info(f"Loaded {len(self.train_examples)} STS-B training examples")
            logger.info(f"Loaded {len(self.eval_examples)} STS-B validation examples")
            
        except Exception as e:
            logger.warning(f"Failed to load STS Benchmark: {e}")
    
    def prepare_nli_data(self):
        """Load and prepare NLI (Natural Language Inference) data"""
        logger.info("Loading NLI dataset...")
        
        try:
            # Load AllNLI dataset (SNLI + MultiNLI)
            dataset = load_dataset("sentence-transformers/all-nli", split="train[:100000]")
            
            # Convert to InputExample format
            # Label mapping: entailment=1.0, neutral=0.5, contradiction=0.0
            label_map = {'entailment': 1.0, 'neutral': 0.5, 'contradiction': 0.0}
            
            for item in dataset:
                if item['label'] in label_map:
                    example = InputExample(
                        texts=[item['premise'], item['hypothesis']], 
                        label=label_map[item['label']]
                    )
                    self.train_examples.append(example)
            
            logger.info(f"Added {len(dataset)} NLI training examples")
            
        except Exception as e:
            logger.warning(f"Failed to load NLI data: {e}")
    
    def prepare_atles_custom_data(self):
        """Load custom ATLES-specific training data"""
        if not self.config.custom_data_path:
            return
        
        custom_path = Path(self.config.custom_data_path)
        
        if not custom_path.exists():
            logger.info("Creating sample ATLES embedding training data...")
            self._create_sample_atles_data(custom_path)
        
        logger.info(f"Loading custom ATLES data from {custom_path}")
        
        try:
            with open(custom_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        example = InputExample(
                            texts=[item['text1'], item['text2']], 
                            label=float(item['similarity'])
                        )
                        self.train_examples.append(example)
            
            logger.info(f"Loaded custom ATLES data")
            
        except Exception as e:
            logger.warning(f"Failed to load custom ATLES data: {e}")
    
    def _create_sample_atles_data(self, output_path: Path):
        """Create sample ATLES-specific embedding training data"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # ATLES-specific sentence pairs with similarity scores
        sample_data = [
            {
                "text1": "autonomous system optimization",
                "text2": "automated system performance improvement",
                "similarity": 0.9
            },
            {
                "text1": "document analysis and summarization",
                "text2": "text processing and summary generation",
                "similarity": 0.85
            },
            {
                "text1": "neural network architecture",
                "text2": "deep learning model structure",
                "similarity": 0.9
            },
            {
                "text1": "system health monitoring",
                "text2": "performance metrics tracking",
                "similarity": 0.75
            },
            {
                "text1": "configuration parameter adjustment",
                "text2": "settings modification",
                "similarity": 0.8
            },
            {
                "text1": "behavioral pattern recognition",
                "text2": "activity pattern detection",
                "similarity": 0.85
            },
            {
                "text1": "safety boundary validation",
                "text2": "security constraint verification",
                "similarity": 0.8
            },
            {
                "text1": "machine learning model training",
                "text2": "cooking recipe instructions",
                "similarity": 0.1
            },
            {
                "text1": "database query optimization",
                "text2": "weather forecast prediction",
                "similarity": 0.05
            },
            {
                "text1": "code debugging techniques",
                "text2": "software error identification methods",
                "similarity": 0.9
            },
            {
                "text1": "natural language processing",
                "text2": "text understanding algorithms",
                "similarity": 0.88
            },
            {
                "text1": "computer vision applications",
                "text2": "image recognition systems",
                "similarity": 0.87
            },
            {
                "text1": "reinforcement learning agent",
                "text2": "reward-based learning system",
                "similarity": 0.92
            },
            {
                "text1": "data preprocessing pipeline",
                "text2": "information cleaning workflow",
                "similarity": 0.83
            },
            {
                "text1": "model evaluation metrics",
                "text2": "performance measurement statistics",
                "similarity": 0.86
            }
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        logger.info(f"Created sample ATLES data at {output_path}")
    
    def prepare_all_training_data(self):
        """Prepare all training data sources"""
        logger.info("Preparing training data...")
        
        if self.config.use_sts_benchmark:
            self.prepare_sts_benchmark_data()
        
        if self.config.use_nli_data:
            self.prepare_nli_data()
        
        if self.config.use_custom_atles_data:
            self.prepare_atles_custom_data()
        
        logger.info(f"Total training examples: {len(self.train_examples)}")
        logger.info(f"Total evaluation examples: {len(self.eval_examples)}")
    
    def create_evaluator(self):
        """Create evaluator for model performance tracking"""
        if not self.eval_examples:
            return None
        
        # Extract sentences and scores
        sentences1 = [ex.texts[0] for ex in self.eval_examples]
        sentences2 = [ex.texts[1] for ex in self.eval_examples]
        scores = [ex.label for ex in self.eval_examples]
        
        evaluator = evaluation.EmbeddingSimilarityEvaluator(
            sentences1, 
            sentences2, 
            scores,
            name='sts-eval'
        )
        
        return evaluator
    
    def fine_tune(self):
        """Execute the fine-tuning process"""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if not self.train_examples:
            raise RuntimeError("No training data. Call prepare_all_training_data() first.")
        
        logger.info("=" * 60)
        logger.info("Starting Fine-Tuning Process")
        logger.info("=" * 60)
        
        # Create output directory
        output_path = Path(self.config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create DataLoader
        train_dataloader = DataLoader(
            self.train_examples, 
            shuffle=True, 
            batch_size=self.config.batch_size
        )
        
        # Define loss function - CosineSimilarityLoss for regression
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        # Create evaluator
        evaluator = self.create_evaluator()
        
        # Calculate warmup steps
        warmup_steps = min(
            self.config.warmup_steps,
            int(len(train_dataloader) * self.config.num_epochs * 0.1)
        )
        
        logger.info(f"Training configuration:")
        logger.info(f"  - Epochs: {self.config.num_epochs}")
        logger.info(f"  - Batch size: {self.config.batch_size}")
        logger.info(f"  - Learning rate: {self.config.learning_rate}")
        logger.info(f"  - Warmup steps: {warmup_steps}")
        logger.info(f"  - Total steps: {len(train_dataloader) * self.config.num_epochs}")
        logger.info(f"  - FP16: {self.config.fp16}")
        
        # Fine-tune the model
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            evaluator=evaluator,
            epochs=self.config.num_epochs,
            warmup_steps=warmup_steps,
            optimizer_params={'lr': self.config.learning_rate},
            output_path=str(output_path),
            evaluation_steps=self.config.eval_steps,
            save_best_model=True,
            use_amp=self.config.fp16
        )
        
        logger.info("=" * 60)
        logger.info("Fine-Tuning Complete!")
        logger.info("=" * 60)
        logger.info(f"Model saved to: {output_path}")
        
        # Save configuration
        config_path = output_path / "finetune_config.json"
        with open(config_path, 'w') as f:
            json.dump({
                'base_model': self.config.base_model,
                'num_epochs': self.config.num_epochs,
                'batch_size': self.config.batch_size,
                'learning_rate': self.config.learning_rate,
                'max_seq_length': self.config.max_seq_length,
                'training_examples': len(self.train_examples),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        return str(output_path)
    
    def test_fine_tuned_model(self, model_path: str):
        """Test the fine-tuned model with sample queries"""
        logger.info(f"Testing fine-tuned model from {model_path}")
        
        test_model = SentenceTransformer(model_path)
        
        # Test sentences
        test_pairs = [
            ("machine learning algorithm", "deep learning model"),
            ("autonomous system optimization", "automated performance improvement"),
            ("document summarization", "text generation"),
            ("cat", "dog"),
            ("hello world", "goodbye universe")
        ]
        
        logger.info("\nTest Results:")
        logger.info("-" * 60)
        
        for sent1, sent2 in test_pairs:
            emb1 = test_model.encode(sent1, convert_to_tensor=True)
            emb2 = test_model.encode(sent2, convert_to_tensor=True)
            
            similarity = util.cos_sim(emb1, emb2).item()
            logger.info(f"'{sent1}' <-> '{sent2}'")
            logger.info(f"  Similarity: {similarity:.4f}\n")


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Qwen3-Embedding-4B for ATLES")
    parser.add_argument("--config", type=str, help="Path to config JSON file")
    parser.add_argument("--model", type=str, help="Base model to fine-tune")
    parser.add_argument("--output-dir", type=str, help="Output directory")
    parser.add_argument("--epochs", type=int, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, help="Batch size")
    parser.add_argument("--learning-rate", type=float, help="Learning rate")
    parser.add_argument("--test-only", action="store_true", help="Only test existing model")
    parser.add_argument("--test-model-path", type=str, help="Path to model for testing")
    
    args = parser.parse_args()
    
    # Load config
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            config_dict = json.load(f)
        config = EmbeddingFineTuneConfig(**config_dict)
    else:
        config = EmbeddingFineTuneConfig()
    
    # Override with command line args
    if args.model:
        config.base_model = args.model
    if args.output_dir:
        config.output_dir = args.output_dir
    if args.epochs:
        config.num_epochs = args.epochs
    if args.batch_size:
        config.batch_size = args.batch_size
    if args.learning_rate:
        config.learning_rate = args.learning_rate
    
    # Create fine-tuner
    fine_tuner = ATLESEmbeddingFineTuner(config)
    
    # Test mode
    if args.test_only:
        if args.test_model_path:
            fine_tuner.test_fine_tuned_model(args.test_model_path)
        else:
            logger.error("--test-model-path required for --test-only mode")
        return
    
    # Load model
    fine_tuner.load_model()
    
    # Prepare data
    fine_tuner.prepare_all_training_data()
    
    # Fine-tune
    output_path = fine_tuner.fine_tune()
    
    # Test the fine-tuned model
    logger.info("\n" + "=" * 60)
    fine_tuner.test_fine_tuned_model(output_path)


if __name__ == "__main__":
    main()

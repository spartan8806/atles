"""Test the fine-tuned ATLES MPNet embedding model"""
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from datasets import load_dataset
import numpy as np

# Load the fine-tuned model
model_path = r"D:\.atles\models\atles_mpnet_finetuned\atles_mpnet_finetuned"
print(f"Loading model from: {model_path}")
model = SentenceTransformer(model_path)
print("✓ Model loaded successfully!")

# Load STS-B test dataset
print("\nLoading STS-B test dataset...")
dataset = load_dataset("mteb/stsbenchmark-sts", split="test")
print(f"✓ Loaded {len(dataset)} test samples")

# Prepare data
sentences1 = dataset['sentence1']
sentences2 = dataset['sentence2']
scores = np.array(dataset['score']) / 5.0  # Normalize to 0-1

# Create evaluator
evaluator = EmbeddingSimilarityEvaluator(
    sentences1=sentences1,
    sentences2=sentences2,
    scores=scores,
    name="sts-test"
)

# Evaluate
print("\nEvaluating model on STS-B test set...")
result = evaluator(model)

print(f"\n{'='*60}")
print(f"ATLES MPNet Fine-tuned Model - STS-B Test Results")
print(f"{'='*60}")
if isinstance(result, dict):
    for key, value in result.items():
        print(f"{key}: {value:.4f}")
else:
    print(f"Spearman Correlation: {result:.4f}")
print(f"{'='*60}")

# Also test with some examples
print("\n\nTesting with example sentence pairs:")
test_pairs = [
    ("A man is eating food.", "A man is eating pasta."),
    ("Someone is playing guitar.", "A person is playing piano."),
    ("The cat is sleeping.", "A dog is running."),
    ("I love programming.", "I hate coding.")
]

for sent1, sent2 in test_pairs:
    emb1 = model.encode(sent1)
    emb2 = model.encode(sent2)
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    print(f"\nSentence 1: {sent1}")
    print(f"Sentence 2: {sent2}")
    print(f"Similarity: {similarity:.4f}")

print("\n✓ Test complete!")

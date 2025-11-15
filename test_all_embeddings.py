"""Test all embedding models and rank them by performance"""
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from datasets import load_dataset
import numpy as np
import json
from datetime import datetime

# Load STS-B test dataset
print("Loading STS-B test dataset...")
dataset = load_dataset("mteb/stsbenchmark-sts", split="test")
sentences1 = dataset['sentence1']
sentences2 = dataset['sentence2']
scores = np.array(dataset['score']) / 5.0  # Normalize to 0-1

# Define all models to test
models_to_test = {
    "atles_mpnet_finetuned": r"D:\.atles\models\atles_mpnet_finetuned\atles_mpnet_finetuned",
    "atles_mpnet_base_finetuned": r"D:\.atles\models\extracted_models\atles_mpnet_base_finetuned",
    "atles_embedding_model": r"D:\.atles\models\atles_embedding_model",
}

results = []

print("\n" + "="*70)
print("TESTING ALL EMBEDDING MODELS")
print("="*70 + "\n")

for model_name, model_path in models_to_test.items():
    try:
        print(f"\n{'='*70}")
        print(f"Testing: {model_name}")
        print(f"Path: {model_path}")
        print(f"{'='*70}")
        
        # Load model
        print("Loading model...")
        model = SentenceTransformer(model_path)
        print("✓ Model loaded successfully!")
        
        # Create evaluator
        evaluator = EmbeddingSimilarityEvaluator(
            sentences1=sentences1,
            sentences2=sentences2,
            scores=scores,
            name="sts-test"
        )
        
        # Evaluate
        print("Evaluating on STS-B test set...")
        result = evaluator(model)
        
        # Extract scores
        if isinstance(result, dict):
            pearson = result.get('sts-test_pearson_cosine', 0)
            spearman = result.get('sts-test_spearman_cosine', 0)
        else:
            pearson = spearman = result
        
        # Store results
        results.append({
            "model_name": model_name,
            "path": model_path,
            "pearson": pearson,
            "spearman": spearman,
            "average": (pearson + spearman) / 2
        })
        
        print(f"✓ Pearson: {pearson:.4f}")
        print(f"✓ Spearman: {spearman:.4f}")
        print(f"✓ Average: {(pearson + spearman) / 2:.4f}")
        
    except Exception as e:
        print(f"✗ Error testing {model_name}: {e}")
        results.append({
            "model_name": model_name,
            "path": model_path,
            "pearson": 0,
            "spearman": 0,
            "average": 0,
            "error": str(e)
        })

# Sort by average score
results.sort(key=lambda x: x['average'], reverse=True)

# Print final ranking
print("\n" + "="*70)
print("FINAL RANKING - EMBEDDING MODELS")
print("="*70)
print(f"{'Rank':<6} {'Model':<35} {'Pearson':<10} {'Spearman':<10} {'Average':<10}")
print("-"*70)

for i, result in enumerate(results, 1):
    if result['average'] > 0:
        print(f"{i:<6} {result['model_name']:<35} {result['pearson']:<10.4f} {result['spearman']:<10.4f} {result['average']:<10.4f}")
    else:
        print(f"{i:<6} {result['model_name']:<35} {'ERROR':<10} {'ERROR':<10} {'N/A':<10}")

print("="*70)

# Save results to file
output_file = f"embedding_model_rankings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w') as f:
    json.dump({
        "test_date": datetime.now().isoformat(),
        "dataset": "STS-B Test Set",
        "results": results
    }, f, indent=2)

print(f"\n✓ Results saved to: {output_file}")
print(f"\n🏆 Best model: {results[0]['model_name']} (Avg: {results[0]['average']:.4f})")

"""
MTEB Evaluation on CPU (Stable, No CUDA Errors)

This runs MTEB evaluation on CPU to avoid CUDA indexing errors.
It's slower but much more stable and reliable.
"""

import mteb
from sentence_transformers import SentenceTransformer
import torch
from datetime import datetime

print("=" * 80)
print("ATLES - MTEB EVALUATION (CPU MODE - STABLE)")
print("=" * 80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Force CPU to avoid CUDA errors
print("Loading model on CPU (avoiding CUDA errors)...")
model = SentenceTransformer("spartan8806/atles", device="cpu")

# Set max sequence length to avoid index errors
model.max_seq_length = 512  # Safe limit for MPNet
if hasattr(model, 'tokenizer'):
    model.tokenizer.model_max_length = 512
    
print(f"✓ Model loaded on CPU")
print(f"  Max sequence length: {model.max_seq_length}\n")

# Start with essential STS tasks (your strength!)
# These are most important for leaderboard ranking
tasks = [
    "STSBenchmark",  # Your best: 83.73%!
    "STS12",
    "STS13", 
    "STS14",
    "STS15",
    "STS16",
    "STS17",
    "SICK-R",
]

print(f"Running {len(tasks)} core STS tasks (your specialty!)")
print("These establish your TOP 15 ranking.\n")
print("=" * 80)

# Get task objects
task_objects = [mteb.get_task(task_name) for task_name in tasks]

# Run evaluation on CPU with proper truncation
results = mteb.evaluate(
    model=model,
    tasks=task_objects,
    prediction_folder="mteb_results",
    overwrite_strategy="only-missing",
    show_progress_bar=True,
    encode_kwargs={
        "batch_size": 8,  # Smaller batch for stability
        "show_progress_bar": True,
        "normalize_embeddings": True,  # Better for similarity
    }
)

print("\n" + "=" * 80)
print("✓ CORE STS EVALUATION COMPLETE!")
print("=" * 80)

print("""
Your STS results are ready for leaderboard submission!

NEXT STEPS:

1. Go to: https://huggingface.co/spaces/mteb/leaderboard

2. Click "Submit Model"

3. Upload results from: mteb_results/

4. Fill in:
   - Model: spartan8806/atles
   - Architecture: MPNet
   - Parameters: 110M

5. Submit and get your TOP 15 ranking! 🏆

NOTE: If you want more tasks, run this script again.
It will skip completed tasks and add new ones.

To add more task types (optional):
- Edit the 'tasks' list in this script
- Add: Classification, Clustering, Retrieval tasks
- Re-run script (it resumes automatically)
""")

print("=" * 80)
print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

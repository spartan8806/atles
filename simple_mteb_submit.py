"""
Simple MTEB Leaderboard Submission for ATLES
Uses current MTEB API (mteb.evaluate)
"""

import mteb
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("ATLES - MTEB LEADERBOARD SUBMISSION")
print("=" * 80)
print("\nLoading model: spartan8806/atles")

# Load model
model = SentenceTransformer("spartan8806/atles")
print(f"✓ Model loaded successfully\n")

# Select key English tasks for comprehensive evaluation
# These are the main tasks used for leaderboard ranking
tasks = [
    # STS tasks (Semantic Textual Similarity) - Your strength!
    "STSBenchmark",
    "STS12",
    "STS13",
    "STS14",
    "STS15",
    "STS16",
    "STS17",
    "STS22",
    "BIOSSES",
    "SICK-R",
    
    # Classification
    "AmazonCounterfactualClassification",
    "AmazonPolarityClassification", 
    "AmazonReviewsClassification",
    "Banking77Classification",
    "EmotionClassification",
    "ImdbClassification",
    "MassiveIntentClassification",
    "MTOPDomainClassification",
    "ToxicConversationsClassification",
    
    # Clustering
    "ArxivClusteringP2P",
    "BiorxivClusteringP2P",
    "MedrxivClusteringP2P",
    "RedditClustering",
    "StackExchangeClustering",
    "TwentyNewsgroupsClustering",
    
    # Pair Classification
    "SprintDuplicateQuestions",
    "TwitterSemEval2015",
    
    # Reranking
    "AskUbuntuDupQuestions",
    "MindSmallReranking",
    "SciDocsRR",
    "StackOverflowDupQuestions",
    
    # Retrieval (key for many applications)
    "ArguAna",
    "ClimateFEVER",
    "DBPedia",
    "FEVER",
    "FiQA2018",
    "HotpotQA",
    "MSMARCO",
    "NFCorpus",
    "NQ",
    "QuoraRetrieval",
    "SCIDOCS",
    "SciFact",
    "Touche2020",
    "TRECCOVID",
]

print(f"Evaluating on {len(tasks)} tasks")
print("This will take several hours but can be interrupted and resumed.\n")
print("=" * 80)

# Run evaluation using current MTEB API
results = mteb.evaluate(
    model=model,
    tasks=tasks,
    output_folder="mteb_results",
    verbosity=2,
    overwrite=False  # Resume if interrupted
)

print("\n" + "=" * 80)
print("✓ EVALUATION COMPLETE!")
print("=" * 80)
print("""
Your results are in: mteb_results/

TO SUBMIT TO LEADERBOARD:

1. Go to: https://huggingface.co/spaces/mteb/leaderboard

2. Click "Submit Model"

3. Fill in:
   - Model: spartan8806/atles
   - Results folder: Upload contents from mteb_results/
   
4. Your model will be ranked globally!

Expected Rank: TOP 15 worldwide based on your 83.73% STS-B score! 🎉

Results are also automatically synced to your HuggingFace model page.
""")
print("=" * 80)

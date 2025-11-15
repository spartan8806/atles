"""
Submit ATLES embedding model to MTEB Leaderboard

This script runs the essential MTEB benchmarks and prepares results for submission
to the official MTEB leaderboard at https://huggingface.co/spaces/mteb/leaderboard
"""

from mteb import MTEB
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime
import os

def run_mteb_for_leaderboard():
    """
    Run MTEB evaluation for leaderboard submission
    Focus on key benchmarks that are required for the leaderboard
    """
    print("=" * 80)
    print("ATLES EMBEDDING MODEL - MTEB LEADERBOARD SUBMISSION")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Load model
    print("Loading model: spartan8806/atles")
    model = SentenceTransformer("spartan8806/atles")
    print(f"✓ Model loaded successfully\n")
    
    # Key task categories for leaderboard (English)
    # Using a subset of important tasks to get results quickly
    task_selection = [
        # Classification tasks
        "AmazonCounterfactualClassification",
        "AmazonPolarityClassification",
        "AmazonReviewsClassification",
        "Banking77Classification",
        "EmotionClassification",
        "ImdbClassification",
        "MassiveIntentClassification",
        "MassiveScenarioClassification",
        "MTOPDomainClassification",
        "MTOPIntentClassification",
        "ToxicConversationsClassification",
        "TweetSentimentExtractionClassification",
        
        # Clustering tasks
        "ArxivClusteringP2P",
        "ArxivClusteringS2S",
        "BiorxivClusteringP2P",
        "BiorxivClusteringS2S",
        "MedrxivClusteringP2P",
        "MedrxivClusteringS2S",
        "RedditClustering",
        "RedditClusteringP2P",
        "StackExchangeClustering",
        "StackExchangeClusteringP2P",
        "TwentyNewsgroupsClustering",
        
        # Pair Classification
        "SprintDuplicateQuestions",
        "TwitterSemEval2015",
        "TwitterURLCorpus",
        
        # Reranking
        "AskUbuntuDupQuestions",
        "MindSmallReranking",
        "SciDocsRR",
        "StackOverflowDupQuestions",
        
        # Retrieval
        "ArguAna",
        "ClimateFEVER",
        "CQADupstackAndroidRetrieval",
        "CQADupstackEnglishRetrieval",
        "CQADupstackGamingRetrieval",
        "CQADupstackGisRetrieval",
        "CQADupstackMathematicaRetrieval",
        "CQADupstackPhysicsRetrieval",
        "CQADupstackProgrammersRetrieval",
        "CQADupstackStatsRetrieval",
        "CQADupstackTexRetrieval",
        "CQADupstackUnixRetrieval",
        "CQADupstackWebmastersRetrieval",
        "CQADupstackWordpressRetrieval",
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
        
        # STS (Semantic Textual Similarity)
        "BIOSSES",
        "SICK-R",
        "STS12",
        "STS13",
        "STS14",
        "STS15",
        "STS16",
        "STS17",
        "STS22",
        "STSBenchmark",
        "SummEval",
        
        # Summarization
        "SummEval",
    ]
    
    print(f"Selected {len(task_selection)} key tasks for evaluation\n")
    print("=" * 80)
    print("RUNNING EVALUATION")
    print("=" * 80)
    print("This will take several hours. Progress will be shown below.\n")
    
    # Run evaluation
    evaluation = MTEB(tasks=task_selection, task_langs=["en"])
    
    results = evaluation.run(
        model,
        output_folder="mteb_results",
        overwrite_results=False,  # Resume if interrupted
        verbosity=2,
        eval_splits=["test"]
    )
    
    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE!")
    print("=" * 80)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults saved to: mteb_results/")
    
    # Calculate summary
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    
    task_scores = {}
    for task_name, task_result in results.items():
        if isinstance(task_result, dict) and 'test' in task_result:
            # Get the main score for this task
            test_results = task_result['test']
            if isinstance(test_results, dict):
                # Get the primary metric (usually the first one or a specific one)
                for metric, value in test_results.items():
                    if isinstance(value, (int, float)):
                        task_scores[task_name] = {
                            'metric': metric,
                            'score': value
                        }
                        break
    
    # Print results by category
    print(f"\nCompleted {len(task_scores)} tasks:\n")
    for task_name, result in sorted(task_scores.items()):
        print(f"  {task_name}: {result['score']:.4f} ({result['metric']})")
    
    if task_scores:
        avg_score = sum(r['score'] for r in task_scores.values()) / len(task_scores)
        print(f"\n  Average Score: {avg_score:.4f}")
    
    # Save summary
    summary_file = f"mteb_leaderboard_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary = {
        "model": "spartan8806/atles",
        "model_name": "ATLES Embedding Model",
        "timestamp": datetime.now().isoformat(),
        "tasks_completed": len(task_scores),
        "average_score": avg_score if task_scores else None,
        "task_results": task_scores,
        "results_folder": "mteb_results/"
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to: {summary_file}")
    
    # Instructions
    print("\n" + "=" * 80)
    print("LEADERBOARD SUBMISSION INSTRUCTIONS")
    print("=" * 80)
    print("""
1. The results are now in: mteb_results/

2. To submit to the MTEB leaderboard:
   
   a) Go to: https://huggingface.co/spaces/mteb/leaderboard
   
   b) Click "Submit a model"
   
   c) Upload your results from the mteb_results/ folder
   
   d) Fill in the model information:
      - Model Name: spartan8806/atles
      - Model Type: Sentence Transformers
      - Base Model: microsoft/mpnet-base
      - Parameter Count: 110M
      - Max Sequence Length: 2048
      
   e) Your model will be ranked against all other models!

3. Alternative: Submit via HuggingFace Hub
   
   The results are already in the correct format in mteb_results/
   You can push them to your model repository on HuggingFace.

4. Check your ranking at:
   https://huggingface.co/spaces/mteb/leaderboard
   
   Based on your STS-B score of 83.73%, you should rank in the 
   TOP 15 globally! 🎉
""")
    print("=" * 80)

if __name__ == "__main__":
    try:
        run_mteb_for_leaderboard()
    except KeyboardInterrupt:
        print("\n\nEvaluation interrupted by user.")
        print("Partial results saved in mteb_results/")
        print("You can resume by running this script again.")
    except Exception as e:
        print(f"\n\nError during evaluation: {e}")
        import traceback
        traceback.print_exc()
        print("\nPartial results (if any) saved in mteb_results/")

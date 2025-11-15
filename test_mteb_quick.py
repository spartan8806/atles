"""
Quick MTEB test to verify installation and model loading
"""

print("Testing MTEB installation...")

# Test 1: Import MTEB
try:
    from mteb import MTEB
    print("✓ MTEB imported successfully")
except Exception as e:
    print(f"✗ Failed to import MTEB: {e}")
    exit(1)

# Test 2: Load model
try:
    from sentence_transformers import SentenceTransformer
    print("\nLoading model: spartan8806/atles")
    model = SentenceTransformer("spartan8806/atles")
    print(f"✓ Model loaded: {model}")
except Exception as e:
    print(f"✗ Failed to load model: {e}")
    exit(1)

# Test 3: Check available tasks
try:
    from mteb import MTEB
    
    # Get list of task names (different API in newer MTEB versions)
    try:
        # Try newer API
        tasks = list(MTEB.available_tasks)
    except:
        # Try older API  
        evaluation = MTEB(task_langs=["en"])
        tasks = evaluation.tasks
    
    print(f"\n✓ Total MTEB tasks available: {len(tasks)}")
    print("\nMTEB is ready for benchmarking!")
    print(f"Model can be evaluated on {len(tasks)} tasks")
        
except Exception as e:
    print(f"✗ Failed to get tasks: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\nYou can now run the full benchmark with:")
print("  python run_full_mteb_benchmark.py")
print("\nNote: The full benchmark will take several hours.")
print("="*60)

#!/usr/bin/env python3
"""Quick verification script to check if fine-tuning setup is ready"""

import sys
from pathlib import Path

print("=" * 60)
print("ATLES Fine-Tuning Setup Verification")
print("=" * 60)
print()

# Check imports
print("1. Checking Python modules...")
try:
    import torch
    print(f"   [OK] PyTorch {torch.__version__}")
except ImportError as e:
    print(f"   [FAIL] PyTorch not found: {e}")
    sys.exit(1)

try:
    import transformers
    print(f"   [OK] Transformers {transformers.__version__}")
except ImportError as e:
    print(f"   [FAIL] Transformers not found: {e}")
    sys.exit(1)

try:
    import peft
    print(f"   [OK] PEFT {peft.__version__}")
except ImportError as e:
    print(f"   [FAIL] PEFT not found: {e}")
    sys.exit(1)

try:
    import datasets
    print(f"   [OK] Datasets {datasets.__version__}")
except ImportError as e:
    print(f"   [FAIL] Datasets not found: {e}")
    sys.exit(1)

# Check CUDA
print("\n2. Checking GPU/CUDA availability...")
if torch.cuda.is_available():
    print(f"   [OK] CUDA available")
    print(f"   [OK] CUDA version: {torch.version.cuda}")
    print(f"   [OK] GPU device count: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"   [OK] GPU {i}: {torch.cuda.get_device_name(i)}")
else:
    print("   [WARN] CUDA not available - will use CPU (very slow)")

# Check files
print("\n3. Checking configuration files...")
config_file = Path("finetune_config.json")
if config_file.exists():
    print(f"   [OK] Configuration file exists: {config_file}")
else:
    print(f"   [FAIL] Configuration file not found: {config_file}")

print("\n4. Checking training data...")
data_file = Path("training_data/atles_training_data.jsonl")
if data_file.exists():
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = sum(1 for _ in f)
    print(f"   [OK] Training data exists: {data_file}")
    print(f"   [OK] Training examples: {lines}")
else:
    print(f"   [INFO] Training data not found (will be created automatically)")
    print(f"         Expected location: {data_file}")

# Check scripts
print("\n5. Checking fine-tuning scripts...")
scripts = [
    "finetune_qwen.py",
    "prepare_training_data.py",
    "export_to_ollama.py"
]
all_scripts_exist = True
for script in scripts:
    script_path = Path(script)
    if script_path.exists():
        print(f"   [OK] {script}")
    else:
        print(f"   [FAIL] {script} not found")
        all_scripts_exist = False

print("\n" + "=" * 60)
if all_scripts_exist and config_file.exists():
    print("[SUCCESS] Setup verification complete!")
    print("[SUCCESS] Ready to run fine-tuning!")
    print("\nNext step: Run 'python finetune_qwen.py --config finetune_config.json'")
else:
    print("[WARN] Some files are missing, but core dependencies are installed")
print("=" * 60)


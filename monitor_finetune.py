#!/usr/bin/env python3
"""Monitor the fine-tuning progress"""
import time
import os
from pathlib import Path

output_dir = Path("./finetuned_models/atles_qwen3_embedding_4b")

print("Monitoring fine-tuning progress...")
print(f"Output directory: {output_dir}")
print("-" * 60)

while True:
    if output_dir.exists():
        files = list(output_dir.glob("*"))
        print(f"\nFiles created: {len(files)}")
        for f in sorted(files)[-5:]:  # Show last 5 files
            size = f.stat().st_size if f.is_file() else 0
            print(f"  {f.name} ({size:,} bytes)")
    else:
        print("Waiting for output directory to be created...")
    
    time.sleep(10)

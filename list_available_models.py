#!/usr/bin/env python3
"""
List available model directories and files that could be uploaded to Hugging Face.
"""

from pathlib import Path
import os

def find_potential_models(base_dir: Path = Path(".")) -> dict:
    """Find directories that might contain models."""
    models = {}
    
    # Check common model directories
    model_dirs = [
        base_dir / "models",
        base_dir / "checkpoints",
        base_dir / "outputs",
        base_dir / "fine_tuned_models",
    ]
    
    # Also check for embeddinggemma directory
    if (base_dir / "embeddinggemma-300m").exists():
        model_dirs.append(base_dir / "embeddinggemma-300m")
    
    for model_dir in model_dirs:
        if not model_dir.exists():
            continue
        
        print(f"\nChecking {model_dir}...")
        
        # Look for model files
        safetensors = list(model_dir.rglob("*.safetensors"))
        bin_files = list(model_dir.rglob("*.bin"))
        configs = list(model_dir.rglob("config.json"))
        tokenizers = list(model_dir.rglob("tokenizer*.json"))
        
        if safetensors or bin_files or configs:
            models[str(model_dir)] = {
                'safetensors': len(safetensors),
                'bin_files': len(bin_files),
                'configs': len(configs),
                'tokenizers': len(tokenizers),
                'total_size_mb': sum(f.stat().st_size for f in safetensors + bin_files) / (1024 * 1024) if (safetensors + bin_files) else 0
            }
            
            print(f"   [OK] Found model files:")
            print(f"      - Safetensors: {len(safetensors)}")
            print(f"      - Bin files: {len(bin_files)}")
            print(f"      - Configs: {len(configs)}")
            print(f"      - Tokenizers: {len(tokenizers)}")
            if models[str(model_dir)]['total_size_mb'] > 0:
                print(f"      - Total size: {models[str(model_dir)]['total_size_mb']:.2f} MB")
    
    return models

def main():
    """Main entry point."""
    import sys
    import io
    # Fix encoding for Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("Scanning for available models...\n")
    
    models = find_potential_models()
    
    if not models:
        print("\n[ERROR] No model directories found with weights/config files.")
        print("\nTo upload a model to Hugging Face, you need:")
        print("   1. Model weights (*.safetensors or *.bin)")
        print("   2. config.json")
        print("   3. Tokenizer files (tokenizer.json, tokenizer_config.json)")
        print("\nIf you have a fine-tuned model, it should be in a directory with these files.")
        print("You can then upload it using:")
        print("   python upload_model_to_hf.py --model-path <path-to-model-dir> --repo-id spartan8806/atles-large")
    else:
        print(f"\n[OK] Found {len(models)} potential model directory(ies):\n")
        for i, (path, info) in enumerate(models.items(), 1):
            print(f"{i}. {path}")
            print(f"   - Weights: {info['safetensors']} safetensors, {info['bin_files']} bin files")
            print(f"   - Configs: {info['configs']}")
            print(f"   - Tokenizers: {info['tokenizers']}")
            print(f"   - Size: {info['total_size_mb']:.2f} MB")
            print(f"\n   Upload command:")
            print(f"   python upload_model_to_hf.py --model-path \"{path}\" --repo-id spartan8806/atles-large")

if __name__ == "__main__":
    main()


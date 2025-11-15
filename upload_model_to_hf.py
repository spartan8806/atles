#!/usr/bin/env python3
"""
Upload ATLES embedding model to Hugging Face
Uploads all necessary files for Sentence-Transformers compatibility
"""

import os
from pathlib import Path
from huggingface_hub import HfApi, login
import sys

def upload_model(model_dir: str, repo_id: str, repo_type: str = "model"):
    """
    Upload model files to Hugging Face
    
    Args:
        model_dir: Local directory containing model files
        repo_id: Hugging Face repository ID (e.g., "spartan8806/atles")
        repo_type: Repository type ("model" or "dataset")
    """
    api = HfApi()
    model_path = Path(model_dir)
    
    if not model_path.exists():
        print(f"❌ Error: Model directory not found: {model_dir}")
        return False
    
    # Check authentication
    try:
        whoami = api.whoami()
        print(f"✅ Authenticated as: {whoami.get('name', 'Unknown')}")
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        print("📝 Please login first:")
        print("   huggingface-cli login")
        print("   OR")
        print("   python -c 'from huggingface_hub import login; login()'")
        return False
    
    # List of files to upload (excluding unnecessary files)
    files_to_upload = []
    
    # Required files for Sentence-Transformers
    required_files = [
        "config.json",
        "config_sentence_transformers.json",
        "modules.json",
        "model.safetensors",
        "tokenizer.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "added_tokens.json",
        "tokenizer.model",  # SentencePiece tokenizer
        "README.md",
        "generation_config.json",
        "sentence_bert_config.json"
    ]
    
    # Check for required files
    missing_files = []
    for file in required_files:
        file_path = model_path / file
        if file_path.exists():
            files_to_upload.append(str(file_path))
        elif file not in ["README.md", "sentence_bert_config.json", "generation_config.json"]:  # Some are optional
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️  Warning: Missing optional files: {missing_files}")
    
    # Add all files in subdirectories (Pooling, Dense layers, etc.)
    for subdir in model_path.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            for file in subdir.rglob("*"):
                if file.is_file():
                    files_to_upload.append(str(file))
    
    # Also upload any other JSON/config files
    for file in model_path.glob("*.json"):
        if str(file) not in files_to_upload:
            files_to_upload.append(str(file))
    
    print(f"\n📦 Found {len(files_to_upload)} files to upload")
    print(f"📂 Model directory: {model_dir}")
    print(f"🎯 Target repository: {repo_id}")
    
    # Upload files
    print("\n🚀 Starting upload...")
    try:
        for i, file_path in enumerate(files_to_upload, 1):
            rel_path = os.path.relpath(file_path, model_dir)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  [{i}/{len(files_to_upload)}] Uploading {rel_path} ({file_size:.2f} MB)...")
            
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=rel_path,
                repo_id=repo_id,
                repo_type=repo_type
            )
        
        print(f"\n✅ Successfully uploaded {len(files_to_upload)} files to {repo_id}")
        print(f"🌐 View at: https://huggingface.co/{repo_id}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during upload: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload ATLES model to Hugging Face")
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./embeddinggemma-300m",
        help="Local directory containing model files"
    )
    parser.add_argument(
        "--repo-id",
        type=str,
        default="spartan8806/atles",
        help="Hugging Face repository ID"
    )
    
    args = parser.parse_args()
    
    success = upload_model(args.model_dir, args.repo_id)
    sys.exit(0 if success else 1)

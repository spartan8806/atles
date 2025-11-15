#!/usr/bin/env python3
"""Check what files are in a Hugging Face repository."""

from huggingface_hub import HfApi
import sys

def check_repo(repo_id: str):
    api = HfApi()
    try:
        files = api.list_repo_files(repo_id, repo_type="model")
        print(f"\nFiles in {repo_id}:")
        print("=" * 60)
        if files:
            for f in sorted(files):
                print(f"  - {f}")
            print(f"\nTotal: {len(files)} files")
        else:
            print("  (No files found)")
    except Exception as e:
        print(f"Error: {e}")
        return False
    return True

if __name__ == "__main__":
    repo_id = sys.argv[1] if len(sys.argv) > 1 else "spartan8806/atles"
    check_repo(repo_id)


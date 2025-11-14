#!/usr/bin/env python3
"""
Backup Public Weights to GitHub

Backs up public weight configuration files to git.
Excludes large model weight files but includes configs and metadata.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_git_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        if check:
            raise
        return e

def check_git_repo() -> bool:
    """Check if we're in a git repository."""
    result = run_git_command(["rev-parse", "--git-dir"], check=False)
    return result.returncode == 0

def find_public_weight_files() -> list[Path]:
    """Find public weight configuration files."""
    weight_files = []
    
    # Check model_surgery_backups for config files
    backups_dir = Path("model_surgery_backups")
    if backups_dir.exists():
        for ext in ['.json', '.yaml', '.yml', '.txt', '.md']:
            weight_files.extend(backups_dir.glob(f"*{ext}"))
    
    # Check memory/ for weight configs
    memory_dir = Path("memory")
    if memory_dir.exists():
        for ext in ['.json', '.yaml', '.yml', '.txt']:
            weight_files.extend(memory_dir.glob(f"*weight*{ext}"))
            weight_files.extend(memory_dir.glob(f"*config*{ext}"))
    
    # Check root for weight configs
    for ext in ['.json', '.yaml', '.yml']:
        weight_files.extend(Path(".").glob(f"*weight*{ext}"))
        weight_files.extend(Path(".").glob(f"*weights*{ext}"))
    
    # Remove duplicates and filter out large files
    unique_files = []
    seen = set()
    for f in weight_files:
        if f not in seen and f.is_file():
            # Skip files larger than 1MB (likely binary weights)
            if f.stat().st_size < 1024 * 1024:
                unique_files.append(f)
                seen.add(f)
    
    return unique_files

def backup_public_weights() -> dict[str, any]:
    """Backup public weight files to git."""
    backup_info = {
        "timestamp": datetime.now().isoformat(),
        "files_backed_up": [],
        "files_skipped": []
    }
    
    weight_files = find_public_weight_files()
    
    if not weight_files:
        print("ℹ️  No public weight config files found to backup.")
        return backup_info
    
    print(f"Found {len(weight_files)} public weight config files:")
    for file_path in weight_files:
        relative_path = file_path.relative_to(Path("."))
        size_kb = file_path.stat().st_size / 1024
        print(f"  - {relative_path} ({size_kb:.1f} KB)")
        
        # Force add to git (even if in .gitignore)
        result = run_git_command(["add", "-f", str(relative_path)], check=False)
        if result.returncode == 0:
            backup_info["files_backed_up"].append(str(relative_path))
        else:
            backup_info["files_skipped"].append(str(relative_path))
            print(f"    ⚠️  Could not add: {result.stderr.strip()}")
    
    return backup_info

def commit_backup(backup_info: dict[str, any]) -> bool:
    """Commit the backup."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Backup public weights: {timestamp}\n\nFiles backed up: {len(backup_info['files_backed_up'])}"
    
    # Check if there are changes to commit
    result = run_git_command(["status", "--porcelain"], check=False)
    if not result.stdout.strip():
        print("\nℹ️  No changes to commit.")
        return False
    
    # Commit
    run_git_command(["commit", "-m", commit_message])
    print(f"\n✅ Committed backup: {len(backup_info['files_backed_up'])} files")
    return True

def push_backup() -> bool:
    """Push backup to remote."""
    print("\nPushing backup to remote...")
    result = run_git_command(["push", "origin", "main"], check=False)
    if result.returncode == 0:
        print("✅ Pushed backup to remote")
        return True
    else:
        print(f"⚠️  Could not push to remote: {result.stderr}")
        print("Backup is saved locally, you can push manually later")
        return False

def main():
    """Main backup function."""
    print("=" * 60)
    print("Backup Public Weights to GitHub")
    print("=" * 60)
    print()
    
    # Check if in git repo
    if not check_git_repo():
        print("❌ Error: Not in a git repository!")
        sys.exit(1)
    
    # Check current branch
    result = run_git_command(["branch", "--show-current"])
    current_branch = result.stdout.strip()
    print(f"Current branch: {current_branch}")
    print()
    
    # Backup weight files
    print("Scanning for public weight config files...")
    backup_info = backup_public_weights()
    
    if not backup_info.get("files_backed_up"):
        print("\n✅ Setup complete!")
        print("   Public weight config files will be backed up when found.")
        return
    
    print(f"\n✅ Found {len(backup_info['files_backed_up'])} files to backup")
    if backup_info.get("files_skipped"):
        print(f"⚠️  Skipped {len(backup_info['files_skipped'])} files")
    
    # Commit backup
    if commit_backup(backup_info):
        # Try to push
        push_backup()
    
    print()
    print("=" * 60)
    print("✅ Backup complete!")
    print("=" * 60)
    print()
    print("Note: Large model weight files (.safetensors, .bin) are excluded")
    print("Only configuration and metadata files are backed up")

if __name__ == "__main__":
    main()


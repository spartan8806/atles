#!/usr/bin/env python3
"""
Backup New Memory Directory to GitHub

Backs up files from the new memory/ directory to git (excluding .db files).
Automatically tracks new files as they're created.
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

def backup_new_memory_files() -> dict[str, any]:
    """Backup new memory files to git."""
    memory_dir = Path("memory")
    
    if not memory_dir.exists():
        print("⚠️  Memory directory does not exist yet. It will be created when ATLES uses it.")
        return {
            "success": False,
            "error": "Memory directory does not exist",
            "files_backed_up": []
        }
    
    backup_info = {
        "timestamp": datetime.now().isoformat(),
        "files_backed_up": [],
        "files_skipped": []
    }
    
    # Find all files in memory directory (excluding .db files and other excluded types)
    all_files = list(memory_dir.rglob("*"))
    excluded_extensions = {'.db', '.db-journal', '.db-wal', '.db-shm'}
    
    files_to_backup = [
        f for f in all_files 
        if f.is_file() and f.suffix.lower() not in excluded_extensions
    ]
    
    if not files_to_backup:
        print("ℹ️  No files to backup in memory/ directory (excluding .db files)")
        print("   New memory files will be backed up automatically when created.")
        return backup_info
    
    print(f"Found {len(files_to_backup)} files to backup:")
    for file_path in files_to_backup:
        relative_path = file_path.relative_to(Path("."))
        print(f"  - {relative_path}")
        
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
    commit_message = f"Backup new memory files: {timestamp}\n\nFiles backed up: {len(backup_info['files_backed_up'])}"
    
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

def update_gitignore_for_new_memory():
    """Update .gitignore to allow new memory files (but keep .db excluded)."""
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        return
    
    content = gitignore_path.read_text(encoding='utf-8')
    
    # Check if we need to add exception for new memory files
    if "memory/" in content and "!memory/*.json" not in content:
        print("\n📝 Updating .gitignore to allow JSON files in memory/...")
        
        # Find the memory/ line and add exception after it
        lines = content.split('\n')
        new_lines = []
        memory_found = False
        
        for line in lines:
            new_lines.append(line)
            if line.strip() == "memory/" and not memory_found:
                # Add exceptions for non-db files
                new_lines.append("!memory/*.json")
                new_lines.append("!memory/*.txt")
                new_lines.append("!memory/*.yaml")
                new_lines.append("!memory/*.yml")
                memory_found = True
        
        gitignore_path.write_text('\n'.join(new_lines), encoding='utf-8')
        print("✅ Updated .gitignore")
        return True
    
    return False

def main():
    """Main backup function."""
    print("=" * 60)
    print("Backup New Memory Directory to GitHub")
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
    
    # Update .gitignore if needed
    update_gitignore_for_new_memory()
    
    # Backup memory files
    print("Scanning memory/ directory...")
    backup_info = backup_new_memory_files()
    
    if not backup_info.get("files_backed_up"):
        print("\n✅ Setup complete!")
        print("   New memory files will be backed up automatically when created.")
        print("   Run this script again after ATLES creates new memory files.")
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
    print("Note: .db files are excluded (as per .gitignore)")
    print("Only non-database files from memory/ are backed up")

if __name__ == "__main__":
    main()

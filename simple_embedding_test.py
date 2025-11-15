"""Simple test to check if spartan8806/atles model can run full MTEB"""
import subprocess
import sys

print("Testing spartan8806/atles model with MTEB...")
print("=" * 60)

# Run MTEB with all available tasks
result = subprocess.run([
    sys.executable, "-m", "mteb", "run",
    "-m", "spartan8806/atles",
    "--output_folder", "mteb_results",
    "--verbosity", "2"
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
    
print("=" * 60)
print(f"Exit code: {result.returncode}")

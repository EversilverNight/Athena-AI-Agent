import os
import subprocess
import shutil
from pathlib import Path

def run_update():
    repo_path = Path(__file__).resolve().parent
    print("🔄 Checking for updates...")

    try:
        if not (repo_path / ".git").exists():
            print("❌ Not a Git repo. Updates not available.")
            return

        # Pull from main branch
        result = subprocess.run(["git", "pull", "origin", "main"], cwd=repo_path, capture_output=True, text=True)
        output = result.stdout.strip()

        if "Already up to date" in output:
            print("✅ Athena is already up to date.")
        else:
            print("✅ Update pulled:\n", output)
            preserve_user_data()
    except Exception as e:
        print("❌ Update failed:", e)

def preserve_user_data():
    # Optionally back up configs or memory
    print("📦 Preserving user data... (placeholder)")
    # Implement memory/setting preservation logic here

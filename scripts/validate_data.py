from __future__ import annotations

import sys
from pathlib import Path

# Bring project root into scope path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.config import settings
from ingestion.readers import DocumentDiscovery

def run_data_validation():
    # Use your discovery engine to scan raw folder context paths
    discovery = DocumentDiscovery(settings.raw_dir)
    all_files = discovery.discover(pattern="**/*.*")
    
    counts = {
        "policy": 0,
        "release_notes": 0,
        "log": 0,
        "api_snapshot": 0,
        "bad_file": 0
    }
    
    for path in all_files:
        filename = path.name.lower()
        suffix = path.suffix.lower()
        
        # 1. Match Bad-File/Corrupted targets
        if "corrupted" in filename or path.stat().st_size == 0:
            counts["bad_file"] += 1
        # 2. Match raw operational stream logs
        elif suffix == ".log":
            counts["log"] += 1
        # 3. Match API network events/recovery snapshots
        elif "recovery" in filename or "snapshot" in filename:
            counts["api_snapshot"] += 1
        # 4. Match PDF corporate policies
        elif suffix == ".pdf":
            counts["policy"] += 1
        # 5. Match DOCX software release notes
        elif suffix == ".docx":
            counts["release_notes"] += 1
        else:
            counts["bad_file"] += 1

    # Print output matching your expected schema matrix precisely
    print("Raw data validation completed")
    print(f"Policy files: {counts['policy']}")
    print(f"Release notes: {counts['release_notes']}")
    print(f"Log files: {counts['log']}")
    print(f"API snapshots: {counts['api_snapshot']}")
    print(f"Bad-file examples: {counts['bad_file']}")

if __name__ == "__main__":
    run_data_validation()
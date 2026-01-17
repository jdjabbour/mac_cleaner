import os
import hashlib
from collections import defaultdict
from pathlib import Path

# -------- CONFIG --------
HASH_CHUNK_SIZE = 1024 * 1024  # 1MB chunks (fast & memory safe)
# ------------------------

def file_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(HASH_CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    directory = Path(directory).expanduser().resolve()
    if not directory.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    print(f"\n🔍 Scanning: {directory}\n")

    # Step 1: group by file size
    size_map = defaultdict(list)
    for root, _, files in os.walk(directory):
        for name in files:
            path = Path(root) / name
            try:
                size_map[path.stat().st_size].append(path)
            except (PermissionError, FileNotFoundError):
                pass

    # Step 2: hash only size-matched files
    hash_map = defaultdict(list)
    for size, paths in size_map.items():
        if len(paths) < 2:
            continue

        for path in paths:
            try:
                h = file_hash(path)
                hash_map[h].append(path)
            except (PermissionError, FileNotFoundError):
                pass

    # Step 3: collect duplicates
    duplicates = {h: p for h, p in hash_map.items() if len(p) > 1}
    return duplicates

def print_results(duplicates):
    if not duplicates:
        print("✅ No duplicate files found.")
        return

    print(f"⚠️ Found {len(duplicates)} duplicate groups:\n")

    for i, (hash_val, files) in enumerate(duplicates.items(), 1):
        print(f"🔁 Group {i} ({len(files)} files):")
        for f in files:
            print(f"   - {f}")
        print()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 find_duplicates.py <directory>")
        sys.exit(1)

    dupes = find_duplicates(sys.argv[1])
    print_results(dupes)

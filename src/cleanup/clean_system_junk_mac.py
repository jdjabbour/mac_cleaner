import os
import shutil
import subprocess
import platform
import sys
from pathlib import Path

from app_utils.ensure_macos import ensure_macos

CLEAN_TARGETS = {
    "User Cache Files": [
        Path.home() / "Library" / "Caches"
    ],
    "System Cache Files": [
        Path("/Library/Caches")
    ],
    "User Log Files": [
        Path.home() / "Library" / "Logs"
    ],
    "System Log Files": [
        Path("/Library/Logs")
    ],
}

TRASH = Path.home() / ".Trash"

def get_size(path):
    total = 0
    if path.is_file():
        return path.stat().st_size
    for root, _, files in os.walk(path, onerror=lambda e: None):
        for f in files:
            try:
                total += (Path(root) / f).stat().st_size
            except:
                pass
    return total

def human(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def move_to_trash(path):
    dest = TRASH / path.name
    if dest.exists():
        dest = TRASH / f"{path.name}_{os.getpid()}"
    shutil.move(str(path), str(dest))

def clean_target(name, paths):
    print(f"\n🔍 {name}")
    total_size = 0
    items = []

    for path in paths:
        if not path.exists():
            continue
        for item in path.iterdir():
            try:
                size = get_size(item)
                total_size += size
                items.append((item, size))
            except:
                pass

    if not items:
        print("  Nothing found.")
        return

    print(f"  Found {human(total_size)}")

    confirm = input(f"  Clean {name}? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("  Skipped.")
        return

    for item, _ in items:
        try:
            move_to_trash(item)
        except:
            pass

    print(f"  ✅ Cleaned {name}")

def clean_language_files():
    print("\n🌍 Language Files")
    print("  macOS manages these automatically.")
    print("  Manual removal is unsafe. Skipped.")

def main():
    ensure_macos()

    print("🧹 macOS System Junk Cleaner")
    print("Safe cleanup – nothing permanently deleted.\n")

    TRASH.mkdir(exist_ok=True)

    for name, paths in CLEAN_TARGETS.items():
        clean_target(name, paths)

    clean_language_files()

    print("\n✅ Cleanup complete.")
    print("Empty Trash to reclaim disk space.")

if __name__ == "__main__":
    main()

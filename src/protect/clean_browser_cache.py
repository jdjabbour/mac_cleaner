#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

HOME = Path.home()

BROWSER_CACHE_PATHS = {
    "Safari": [
        HOME / "Library/Caches/com.apple.Safari",
        HOME / "Library/Safari/LocalStorage",
        HOME / "Library/Safari/Databases",
        HOME / "Library/Safari/ServiceWorkers"
    ],

    "Chrome": [
        HOME / "Library/Caches/Google/Chrome",
        HOME / "Library/Application Support/Google/Chrome/Default/Cache",
        HOME / "Library/Application Support/Google/Chrome/Default/Code Cache",
        HOME / "Library/Application Support/Google/Chrome/Default/GPUCache",
        HOME / "Library/Application Support/Google/Chrome/Default/Service Worker"
    ],

    "Firefox": [
        HOME / "Library/Caches/Firefox",
        HOME / "Library/Application Support/Firefox/Profiles"
    ],

    "Edge": [
        HOME / "Library/Caches/Microsoft Edge",
        HOME / "Library/Application Support/Microsoft Edge/Default/Cache",
        HOME / "Library/Application Support/Microsoft Edge/Default/Code Cache",
        HOME / "Library/Application Support/Microsoft Edge/Default/GPUCache"
    ],
}

def delete_path(path: Path):
    try:
        if path.exists():
            shutil.rmtree(path)
            print(f"✔ Deleted: {path}")
        else:
            print(f"• Skipped (not found): {path}")
    except PermissionError:
        print(f"✖ Permission denied: {path}")
    except Exception as e:
        print(f"✖ Error deleting {path}: {e}")

def clean_browser_caches():
    print("\n🧹 Cleaning browser temporary files...\n")

    for browser, paths in BROWSER_CACHE_PATHS.items():
        print(f"🔹 {browser}")
        for path in paths:
            delete_path(path)
        print()

    print("✅ Browser cleanup complete.")

if __name__ == "__main__":
    clean_browser_caches()

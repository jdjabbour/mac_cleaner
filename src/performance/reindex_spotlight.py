import subprocess
import platform
import sys

from app_utils.ensure_macos import ensure_macos

"""
How to verify reindexing status
mdutil -s /

Expected output during reindex:
Indexing enabled.
Indexing in progress.

python reindex_spotlight.py
!!! You’ll be prompted for your admin password. !!!
"""

def run(cmd):
    print(f"→ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def reindex_spotlight():
    print("\n🔎 Disabling Spotlight indexing...")
    run(["sudo", "mdutil", "-i", "off", "/"])

    print("\n🧹 Erasing Spotlight index...")
    run(["sudo", "mdutil", "-E", "/"])

    print("\n🔎 Re-enabling Spotlight indexing...")
    run(["sudo", "mdutil", "-i", "on", "/"])

    print("\n✅ Spotlight reindex initiated.")
    print("Indexing continues in the background.")

def main():
    ensure_macos()
    print("🚀 Starting Spotlight reindex (requires sudo)...")
    reindex_spotlight()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path

HOME = Path.home()

def run(cmd):
    subprocess.run(cmd, shell=True, check=False)

def clear_recent_documents():
    print("✔ Clearing recently opened documents...")
    run("defaults delete com.apple.recentitems RecentDocuments")
    run("defaults delete com.apple.finder FXRecentFolders")

def clear_recent_apps():
    print("✔ Clearing recently launched applications...")
    run("defaults delete com.apple.recentitems RecentApplications")

def clear_recent_servers():
    print("✔ Clearing recently accessed servers...")
    run("defaults delete com.apple.recentitems RecentServers")

def clear_quicklook_cache():
    print("✔ Clearing Quick Look cache...")
    run("rm -rf ~/Library/Caches/com.apple.QuickLook.thumbnailcache")

def restart_finder():
    print("🔄 Restarting Finder...")
    run("killall Finder")

def clean_recent_items():
    print("\n🧹 Cleaning macOS Recent Items...\n")

    clear_recent_documents()
    clear_recent_apps()
    clear_recent_servers()
    clear_quicklook_cache()
    restart_finder()

    print("\n✅ Recent Items cleanup complete.")

if __name__ == "__main__":
    clean_recent_items()

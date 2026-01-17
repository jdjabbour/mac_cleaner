import platform
import sys
from pathlib import Path

from app_utils.ensure_macos import ensure_macos

# Common locations where apps leave data behind
SEARCH_PATHS = [
    Path.home() / "Library" / "Application Support",
    Path.home() / "Library" / "Caches",
    Path.home() / "Library" / "Preferences",
    Path.home() / "Library" / "Logs",
    Path("/Library") / "Application Support",
    Path("/Library") / "Preferences",
    Path("/Library") / "Logs",
]

# Where installed apps usually live
APP_DIRS = [
    Path("/Applications"),
    Path.home() / "Applications"
]

def get_installed_app_names():
    names = set()
    for app_dir in APP_DIRS:
        if not app_dir.exists():
            continue
        for app in app_dir.glob("*.app"):
            names.add(app.stem.lower())
    return names

def find_leftovers(installed_apps):
    leftovers = []

    for base in SEARCH_PATHS:
        if not base.exists():
            continue
        for item in base.iterdir():
            name = item.name.lower()
            # Heuristic: folder/file name not matching any installed app
            if not any(app in name for app in installed_apps):
                leftovers.append(item)

    return leftovers

def main():
    ensure_macos()

    print("🔍 Scanning for leftover files from uninstalled applications...\n")

    installed_apps = get_installed_app_names()
    leftovers = find_leftovers(installed_apps)

    if not leftovers:
        print("✅ No leftover files detected.")
        return

    print("📦 Possible leftover files:\n")
    for item in sorted(leftovers, key=lambda p: str(p)):
        print(item)

    print("\n⚠️ These files were NOT removed.")
    print("Review carefully before deleting anything.")
    print("Some items may belong to system services or shared frameworks.")

if __name__ == "__main__":
    main()

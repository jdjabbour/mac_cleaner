import subprocess
import platform
import sys
from datetime import datetime, timedelta
from pathlib import Path

from app_utils.ensure_macos import ensure_macos


UNUSED_DAYS = 90  # Change threshold here


def get_last_used(app_path):
    try:
        result = subprocess.run(
            ["mdls", "-name", "kMDItemLastUsedDate", "-raw", app_path],
            capture_output=True,
            text=True
        )
        value = result.stdout.strip()
        if value in ("(null)", ""):
            return None
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S %z")
    except Exception:
        return None

def scan_applications():
    apps = []
    for app_dir in ["/Applications", str(Path.home() / "Applications")]:
        if not Path(app_dir).exists():
            continue
        for app in Path(app_dir).glob("*.app"):
            last_used = get_last_used(str(app))
            apps.append((app.name, app, last_used))
    return apps

def main():
    ensure_macos()

    cutoff = datetime.now().astimezone() - timedelta(days=UNUSED_DAYS)

    print(f"🔍 Scanning for applications unused for {UNUSED_DAYS}+ days...\n")

    unused = []
    for name, path, last_used in scan_applications():
        if last_used is None or last_used < cutoff:
            unused.append((name, path, last_used))

    if not unused:
        print("✅ No unused applications found.")
        return

    print("📦 Unused applications:\n")
    for name, path, last_used in sorted(unused):
        last = last_used.strftime("%Y-%m-%d") if last_used else "Never"
        print(f"{name:40}  Last used: {last}")

    print("\n⚠️ No applications were removed.")
    print("Review carefully before uninstalling anything.")

if __name__ == "__main__":
    main()

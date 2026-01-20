import subprocess
import platform
import sys
from pathlib import Path

from src.app_utils.ensure_macos import ensure_macos

APP_DIRS = [
    Path("/Applications"),
    Path.home() / "Applications"
]

def get_arch():
    return subprocess.check_output(["uname", "-m"], text=True).strip()

def is_universal(binary):
    try:
        out = subprocess.check_output(["lipo", "-info", binary], text=True)
        return "architecture" in out and "Non-fat" not in out
    except:
        return False

def find_main_binary(app):
    macos_dir = app / "Contents" / "MacOS"
    if not macos_dir.exists():
        return None
    for f in macos_dir.iterdir():
        if f.is_file() and f.stat().st_size > 0:
            return f
    return None

def thin_binary(binary, remove_arch):
    subprocess.run(
        ["sudo", "lipo", "-remove", remove_arch, "-output", binary, binary],
        check=True
    )

def clean_binaries():
    ensure_macos()

    host_arch = get_arch()
    remove_arch = "x86_64" if host_arch == "arm64" else "arm64"

    print(f"🧠 Detected architecture: {host_arch}")
    print(f"🧹 Will remove unused slice: {remove_arch}\n")

    targets = []

    for app_dir in APP_DIRS:
        if not app_dir.exists():
            continue
        for app in app_dir.glob("*.app"):
            binary = find_main_binary(app)
            if binary and is_universal(binary):
                targets.append((app, binary))

    if not targets:
        print("✅ No universal binaries found.")
        return

    print("📦 Universal binaries found:\n")
    for app, _ in targets:
        print(f" - {app.name}")

    confirm = input(f"\nRemove {remove_arch} from these apps? (yes/no): ").strip().lower()
    if confirm not in ("yes", "y"):
        print("❌ Operation canceled.")
        return

    for app, binary in targets:
        try:
            print(f"✂️ Thinning {app.name}")
            thin_binary(binary, remove_arch)
        except Exception as e:
            print(f"⚠️ Failed on {app.name}: {e}")

    print("\n✅ Universal binary cleanup complete.")
    print("You may need to re-run after app updates.")



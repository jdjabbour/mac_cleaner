import subprocess
import platform
import sys
import os

from app_utils.ensure_macos import ensure_macos

def run(cmd, allow_fail=False):
    print(f"→ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")

def repair_all_volumes():
    print("\n🛠 Running First Aid on all mounted volumes...")
    volumes = subprocess.check_output(
        ["diskutil", "list", "-plist"],
        stderr=subprocess.DEVNULL
    )

    run(["sudo", "diskutil", "repairVolume", "/"], allow_fail=True)

    for vol in ["/System/Volumes/Data", "/System/Volumes/Preboot", "/System/Volumes/VM"]:
        if os.path.exists(vol):
            run(["sudo", "diskutil", "repairVolume", vol], allow_fail=True)

def repair_user_permissions():
    user = os.getenv("USER")
    print(f"\n👤 Repairing permissions for user: {user}")
    run([
        "sudo",
        "diskutil",
        "resetUserPermissions",
        "/",
        user
    ])

def repair_common_paths():
    print("\n📁 Repairing permissions on common writable paths...")

    paths = [
        "/Applications",
        "/Library",
        "/usr/local",
        "/opt/homebrew"
    ]

    for path in paths:
        if os.path.exists(path):
            run(["sudo", "chmod", "-RN", path], allow_fail=True)
            run(["sudo", "chown", "-R", "root:wheel", path], allow_fail=True)

def main():
    ensure_macos()
    print("🚀 Repairing file & folder permissions (requires sudo)\n")

    repair_all_volumes()
    repair_user_permissions()
    repair_common_paths()

    print("\n✅ Permission verification & repair complete.")
    print("Reboot recommended for full effect.")

if __name__ == "__main__":
    main()


import subprocess
import platform
import sys

from app_utils.ensure_macos import ensure_macos

def check_for_updates():
    print("🔍 Checking for available macOS updates...\n")
    result = subprocess.run(
        ["softwareupdate", "-l"],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    if "No new software available." in output:
        print("✅ Your system is up to date.")
        return False, ""

    print("📦 Updates found:\n")
    print(output)
    return True, output

def prompt_user():
    choice = input("\nWould you like to download and install these updates? (yes/no): ").strip().lower()
    return choice in ["yes", "y"]

def install_updates():
    print("\n⬇️ Downloading and installing updates...")
    subprocess.run(
        ["sudo", "softwareupdate", "-ia"],
        check=True
    )

def main():
    ensure_macos()

    updates_found, _ = check_for_updates()
    if not updates_found:
        return

    if prompt_user():
        install_updates()
        print("\n✅ Updates installed successfully.")
        print("A restart may be required to complete installation.")
    else:
        print("\n❌ Update installation canceled by user.")

if __name__ == "__main__":
    main()

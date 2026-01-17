import os
import shutil
import subprocess
import platform
import sys
from pathlib import Path

from app_utils.ensure_macos import ensure_macos

def quit_mail():
    print("📬 Closing Mail.app if running...")
    subprocess.run(
        ["osascript", "-e", 'tell application "Mail" to quit'],
        check=False
    )

def backup_and_remove_envelope():
    mail_dir = Path.home() / "Library" / "Mail"
    if not mail_dir.exists():
        print("Mail directory not found.")
        sys.exit(1)

    envelope_files = list(mail_dir.rglob("Envelope Index*"))
    if not envelope_files:
        print("No Mail envelope index found (nothing to rebuild).")
        return

    backup_dir = mail_dir / "EnvelopeIndexBackup"
    backup_dir.mkdir(exist_ok=True)

    print("🧹 Backing up and removing Mail envelope database...")
    for file in envelope_files:
        shutil.move(str(file), backup_dir / file.name)

def relaunch_mail():
    print("🚀 Relaunching Mail.app (reindex will begin automatically)...")
    subprocess.run(["open", "-a", "Mail"])

def main():
    ensure_macos()

    print("🔄 Reindexing macOS Mail envelope database\n")
    print("This process does NOT delete or modify emails.\n")

    quit_mail()
    backup_and_remove_envelope()
    relaunch_mail()

    print("\n✅ Mail envelope reindex initiated.")
    print("Mail may be slower temporarily while reindexing completes.")

if __name__ == "__main__":
    main()

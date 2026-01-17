import os
import shutil
from pathlib import Path

from app_utils.ensure_macos import ensure_macos

USER_TRASH = Path.home() / ".Trash"
VOLUME_TRASH_ROOT = Path("/Volumes")



def delete_contents(path):
    if not path.exists():
        return 0

    count = 0
    for item in path.iterdir():
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            count += 1
        except PermissionError:
            print(f"⚠️ Permission denied: {item}")
        except Exception as e:
            print(f"⚠️ Failed to delete {item}: {e}")
    return count

def empty_user_trash():
    print(f"🗑 Emptying user Trash: {USER_TRASH}")
    return delete_contents(USER_TRASH)

def empty_external_trash():
    total = 0
    for volume in VOLUME_TRASH_ROOT.iterdir():
        trash_dir = volume / ".Trashes"
        if trash_dir.exists():
            for user_trash in trash_dir.iterdir():
                print(f"🗑 Emptying external Trash: {user_trash}")
                total += delete_contents(user_trash)
    return total

def main():
    ensure_macos()

    print("🧹 This will permanently delete all items in all Trash bins.")
    confirm = input("Proceed? (yes/no): ").strip().lower()

    if confirm not in ("yes", "y"):
        print("❌ Operation canceled.")
        return

    deleted = 0
    deleted += empty_user_trash()
    deleted += empty_external_trash()

    print(f"\n✅ Trash emptied. {deleted} items permanently deleted.")

if __name__ == "__main__":
    main()

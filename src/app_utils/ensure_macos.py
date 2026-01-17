
import platform
import sys


def ensure_macos():
    if platform.system() != "Darwin":
        print("This script only works on macOS.")
        sys.exit(1)
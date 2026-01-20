import subprocess
import sys
import platform

from src.app_utils.ensure_macos import ensure_macos

def flushing_dns():
    try:
        print("Flushing DNS cache on macOS...")
        subprocess.run(
            ["sudo", "dscacheutil", "-flushcache"],
            check=True
        )
        subprocess.run(
            ["sudo", "killall", "-HUP", "mDNSResponder"],
            check=True
        )
        print("DNS cache flushed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error flushing DNS cache:", e)
        sys.exit(1)

def flush_mac_dns():
    ensure_macos()

    flushing_dns()


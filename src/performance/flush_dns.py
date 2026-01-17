import subprocess
import sys
import platform

def flush_dns_mac():
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

def main():
    if platform.system() != "Darwin":
        print("This script is intended for macOS only.")
        sys.exit(1)

    flush_dns_mac()

if __name__ == "__main__":
    main()

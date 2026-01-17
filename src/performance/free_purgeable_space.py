import subprocess
import platform
import sys
import tempfile
import os

from app_utils.ensure_macos import ensure_macos


def run(cmd):
    print(f"→ Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def delete_tm_snapshots():
    print("\n🧹 Removing local Time Machine snapshots...")
    result = subprocess.check_output(
        ["tmutil", "listlocalsnapshots", "/"],
        text=True
    )

    snapshots = []
    for line in result.splitlines():
        if "com.apple.TimeMachine" in line:
            snapshots.append(line.split(".")[-1])

    if not snapshots:
        print("No local Time Machine snapshots found.")
        return

    for snap in snapshots:
        run(["sudo", "tmutil", "deletelocalsnapshots", snap])

def flush_dns_and_caches():
    print("\n🧹 Flushing caches...")
    run(["sudo", "dscacheutil", "-flushcache"])
    run(["sudo", "killall", "-HUP", "mDNSResponder"])

def force_disk_pressure(size_gb=10):
    """
    Create a temporary large file to force macOS
    to purge reclaimable space.
    """
    print(f"\n💥 Forcing disk pressure ({size_gb}GB temp file)...")
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "disk_pressure.tmp")

    try:
        run([
            "dd",
            "if=/dev/zero",
            f"of={temp_file}",
            "bs=1g",
            f"count={size_gb}"
        ])
    except subprocess.CalledProcessError:
        print("Disk pressure attempt complete (expected if space ran out).")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print("Temporary file removed.")

def main():
    ensure_macos()

    print("🚀 Starting purgeable space cleanup (requires sudo)...\n")

    delete_tm_snapshots()
    flush_dns_and_caches()
    force_disk_pressure(size_gb=15)

    print("\n✅ Cleanup complete.")
    print("Rebooting will often free additional purgeable space.")

if __name__ == "__main__":
    main()

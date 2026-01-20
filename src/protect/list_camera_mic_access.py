#!/usr/bin/env python3

import sqlite3
from pathlib import Path

TCC_DB = Path.home() / "Library/Application Support/com.apple.TCC/TCC.db"

SERVICES = {
    "kTCCServiceCamera": "Camera",
    "kTCCServiceMicrophone": "Microphone",
}

def get_permissions():
    if not TCC_DB.exists():
        print("✖ TCC database not found.")
        return

    conn = sqlite3.connect(TCC_DB)
    cursor = conn.cursor()

    query = """
        SELECT service, client, auth_value
        FROM access
        WHERE service IN (?, ?)
        ORDER BY service, client;
    """

    cursor.execute(query, tuple(SERVICES.keys()))
    rows = cursor.fetchall()
    conn.close()

    results = {"Camera": [], "Microphone": []}

    for service, client, auth in rows:
        service_name = SERVICES.get(service, service)
        status = "Allowed" if auth == 2 else "Denied"
        results[service_name].append((client, status))

    return results

def print_results(results):
    print("\n🔐 macOS Privacy Permissions\n")

    for service, entries in results.items():
        print(f"📸 {service}" if service == "Camera" else f"🎤 {service}")
        if not entries:
            print("  (No entries found)")
        for client, status in entries:
            print(f"  • {client} — {status}")
        print()

if __name__ == "__main__":
    perms = get_permissions()
    if perms:
        print_results(perms)

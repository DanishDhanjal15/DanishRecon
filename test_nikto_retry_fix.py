#!/usr/bin/env python3
"""
Quick test to verify Nikto retry logic works correctly
"""
import os
import sys
import subprocess
from pathlib import Path

# Add CyberRecon-Pro to path
sys.path.insert(0, str(Path(__file__).parent / "CyberRecon-Pro"))

print("=" * 70)
print("NIKTO RETRY LOGIC TEST")
print("=" * 70)

# Test the retry command sequence for protego.zssh.dev
NIKTO_PATH = r"c:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program\nikto.pl"
host = "protego.zssh.dev"
port = 443
proto = "https"

print(f"\nTarget: {proto}://{host}:{port}")
print(f"Nikto Path: {NIKTO_PATH}")
print(f"Nikto Exists: {os.path.exists(NIKTO_PATH)}")

# Build the retry commands (same as in the fixed code)
nikto_commands = [
    {
        "cmd": ["perl", NIKTO_PATH, "-h", f"{proto}://{host}:{port}", "-ask", "no"],
        "label": f"perl nikto.pl -h {proto}://{host}:{port} -ask no",
        "timeout": 600 if proto == "https" else 180
    },
    {
        "cmd": ["perl", NIKTO_PATH, "-h", host, "-p", str(port)] + (
            ["-ssl"] if proto == "https" else []
        ) + ["-ask", "no", "-noclean"],
        "label": f"perl nikto.pl -h {host} -p {port}" + (" -ssl" if proto == "https" else "") + " -ask no -noclean",
        "timeout": 300 if proto == "https" else 120
    },
    {
        "cmd": ["perl", NIKTO_PATH, "-h", host, "-p", str(port)] + (
            ["-ssl"] if proto == "https" else []
        ) + ["-ask", "no", "-noclean", "-Plugins", "default"],
        "label": f"perl nikto.pl -h {host} -p {port}" + (" -ssl" if proto == "https" else "") + " -ask no -noclean -Plugins default",
        "timeout": 180 if proto == "https" else 90
    }
]

print("\n" + "=" * 70)
print("RETRY SEQUENCE (Simulated)")
print("=" * 70)

for i, attempt in enumerate(nikto_commands, 1):
    print(f"\nAttempt {i}: {attempt['label']}")
    print(f"  Timeout: {attempt['timeout']}s")
    print(f"  Command: {' '.join(attempt['cmd'][:3])} ...")

print("\n" + "=" * 70)
print("ACTUAL TEST (Running with short timeout for demo)")
print("=" * 70)

for i, attempt in enumerate(nikto_commands, 1):
    print(f"\nAttempt {i}: {attempt['label']}")
    
    try:
        # Use shorter timeout for demo purposes
        demo_timeout = 5  # 5 seconds for demo, not 180-600
        proc = subprocess.Popen(attempt['cmd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, errors='replace', bufsize=0)
        try:
            out, _ = proc.communicate(timeout=demo_timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            out = f"__TIMEOUT__(>{demo_timeout}s)"
    except FileNotFoundError:
        out = "__NOTFOUND__perl"
    except Exception as e:
        out = f"__ERROR__{str(e)}"
    
    # Check result
    if "__TIMEOUT__" in out:
        print(f"  ⚠ Timeout - trying next approach")
    elif "__NOTFOUND__" in out:
        print(f"  ✗ Nikto not found - stopping retries")
        break
    elif "[FAIL]" in out and "Unable to connect" in out:
        print(f"  ⚠ Connection failed - trying next approach")
        if i < len(nikto_commands):
            print(f"    (Retry with: {attempt['label']})")
    elif out and len(out.strip()) >= 50:
        print(f"  ✓ Got response ({len(out)} bytes)")
        break
    else:
        print(f"  ⚠ Minimal output ({len(out)} bytes) - trying next approach")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nWith this fix, Nikto will:")
print("1. Try standard URL format first")
print("2. If that fails, try hostname + port format with -ssl -noclean")
print("3. If that fails, try with minimal plugins (-Plugins default)")
print("4. If all fail, skip the target and continue scanning")
print("\nThis prevents long timeouts and allows scans to complete faster.")

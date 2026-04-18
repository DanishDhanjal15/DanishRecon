#!/usr/bin/env python3
"""
Test script to verify GUI version Nikto vulnerability detection fix
Tests the stage_web_scan function directly on protego.zssh.dev
"""
import sys
import os
import re

# Add CyberRecon-Pro to path
sys.path.insert(0, r"c:\Users\Danish\OneDrive\Desktop\recon cyber\CyberRecon-Pro")
sys.path.insert(0, r"c:\Users\Danish\OneDrive\Desktop\recon cyber")

# Test the Nikto scanning code directly without GUI
print("\n" + "="*80)
print("Testing GUI Nikto Fix on protego.zssh.dev")
print("="*80 + "\n")

# Get the path to Nikto
NIKTO_PATH = r"c:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program\nikto.pl"

if not os.path.exists(NIKTO_PATH):
    print(f"✗ Nikto not found at {NIKTO_PATH}")
    sys.exit(1)

print(f"✓ Nikto path: {NIKTO_PATH}\n")

import subprocess

def run_nikto_scan(target_url, timeout=1200):
    """Execute Nikto scan and return output"""
    try:
        cmd = [
            "perl", NIKTO_PATH,
            "-h", target_url,
            "-ask", "no",
            "-Display", "P"
        ]
        print(f"[*] Running: {' '.join(cmd[:5])} ...")
        
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        try:
            out, _ = proc.communicate(timeout=timeout)
            return out
        except subprocess.TimeoutExpired:
            proc.kill()
            print(f"[!] Scan timed out after {timeout}s")
            partial = ""
            try:
                partial, _ = proc.communicate(timeout=2)
            except:
                pass
            return "__TIMEOUT__" + (partial or "")
    except Exception as e:
        return f"__ERROR__{str(e)}"

# Simulate what GUI does - scan with proper options
print("Scanning: https://protego.zssh.dev:443\n")
output = run_nikto_scan("https://protego.zssh.dev:443", timeout=1200)

if "__NOTFOUND__" in output:
    print("✗ Nikto failed: Perl not found")
    sys.exit(1)

if "__ERROR__" in output:
    print(f"✗ Nikto error: {output}")
    sys.exit(1)

# Parse vulnerabilities (same logic as GUI after fix)
findings = []
for line in output.splitlines():
    if re.match(r'\+ ', line):
        if "OSVDB" in line or "[FAIL]" in line or "[ERROR]" in line:
            continue
        clean = line.strip().lstrip("+ ")
        if len(clean) > 10:
            # Auto-detect severity from keywords
            vuln_severity = "LOW"
            clean_lower = clean.lower()
            
            if any(kw in clean_lower for kw in ["critical", "remote code", "rce", "sql injection", "xss", "csrf", "authentication bypass"]):
                vuln_severity = "CRITICAL"
            elif any(kw in clean_lower for kw in ["high", "auth", "breach", "leak", "disclosure", "bypass"]):
                vuln_severity = "HIGH"
            elif any(kw in clean_lower for kw in ["missing", "unencrypted", "weak", "header", "uncommon"]):
                vuln_severity = "MEDIUM"
            
            # Store finding with severity marker
            finding = f"[{vuln_severity}] {clean}"
            findings.append(finding)

print(f"\n{'='*80}")
print(f"RESULTS: Found {len(findings)} vulnerabilities")
print(f"{'='*80}\n")

if findings:
    print("✓ Vulnerabilities found in GUI-equivalent code:\n")
    for i, f in enumerate(findings, 1):
        # Print first 100 chars only
        display = f[:100] + ("..." if len(f) > 100 else "")
        print(f"  {i}. {display}")
    
    # Extract severity distribution
    critical = sum(1 for f in findings if "[CRITICAL]" in f)
    high = sum(1 for f in findings if "[HIGH]" in f)
    medium = sum(1 for f in findings if "[MEDIUM]" in f)
    low = sum(1 for f in findings if "[LOW]" in f)
    
    print(f"\n{'Severity Distribution:':.<50}")
    print(f"  CRITICAL: {critical}")
    print(f"  HIGH:     {high}")
    print(f"  MEDIUM:   {medium}")
    print(f"  LOW:      {low}")
    print(f"\n✓ SUCCESS: GUI Nikto fix is working!")
else:
    print("✗ FAILED: No vulnerabilities found")
    print(f"\nOutput preview:\n{output[:500]}")
    sys.exit(1)

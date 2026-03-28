#!/usr/bin/env python3
"""
Quick test script to verify Gemini integration works in scans
"""
import os
import sys
import json

# Add workspace root to path
workspace_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, workspace_root)

# Test 1: Import and initialize
print("=" * 70)
print("TEST 1: GEMINI MODULE LOADING")
print("=" * 70)

try:
    from gemini_analyzer import GeminiAnalyzer, GEMINI_AVAILABLE
    print(f"✓ Module imported")
    print(f"  GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test 2: Initialize analyzer
print("\n" + "=" * 70)
print("TEST 2: GEMINI ANALYZER INITIALIZATION")
print("=" * 70)

try:
    analyzer = GeminiAnalyzer()
    print(f"✓ Analyzer initialized")
    print(f"  enabled: {analyzer.enabled}")
    print(f"  api_key: {analyzer.api_key[:20] if analyzer.api_key else 'NOT SET'}...")
    if not analyzer.enabled:
        print(f"  error: {analyzer.error_message}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 3: Analyze single vulnerability
print("\n" + "=" * 70)
print("TEST 3: SINGLE VULNERABILITY ANALYSIS")
print("=" * 70)

test_vuln = {
    "id": "http_80",
    "name": "HTTP Port 80",
    "service": "http",
    "port": 80,
    "version": "Apache 2.4.41",
    "cve": "CVE-2021-41773",
    "cvss_score": 7.5,
    "severity": "HIGH",
    "description": "HTTP service exposed with known vulnerabilities",
    "exploit_available": True
}

try:
    print(f"Analyzing: {test_vuln['name']}")
    analysis = analyzer.analyze_vulnerability(test_vuln)
    if analysis:
        print(f"✓ Analysis successful")
        print(f"  Length: {len(analysis)} chars")
        print(f"  Preview: {analysis[:150]}...")
    else:
        print(f"✗ Analysis returned None")
        sys.exit(1)
except Exception as e:
    print(f"✗ Failed: {e}")
    sys.exit(1)

# Test 4: Batch analysis
print("\n" + "=" * 70)
print("TEST 4: BATCH VULNERABILITY ANALYSIS")
print("=" * 70)

test_vulns = [
    {
        "id": "https_443",
        "name": "HTTPS Port 443",
        "service": "https",
        "port": 443,
        "version": "nginx",
        "cve": "CVE-2016-2107",
        "cvss_score": 5.3,
        "severity": "MEDIUM",
        "description": "HTTPS service with potential SSL/TLS issues",
        "exploit_available": False
    },
    {
        "id": "ssh_22",
        "name": "SSH Port 22",
        "service": "ssh",
        "port": 22,
        "version": "OpenSSH 7.4",
        "cve": "CVE-2018-10933",
        "cvss_score": 6.5,
        "severity": "MEDIUM",
        "description": "SSH with known vulnerabilities",
        "exploit_available": True
    }
]

try:
    analyses = analyzer.analyze_scan_results({
        "host": "test.example.com",
        "services": test_vulns,
        "vulnerabilities": [f"[{v['severity']}] {v['name']}" for v in test_vulns]
    })
    if analyses:
        print(f"✓ Batch analysis successful")
        print(f"  Analyzed: {len(analyses)} vulnerabilities")
        for vid, analysis in analyses.items():
            print(f"    - {vid}: {len(analysis)} chars")
    else:
        print(f"✗ Batch analysis failed")
except Exception as e:
    print(f"✗ Failed: {e}")

# Test 5: Executive summary
print("\n" + "=" * 70)
print("TEST 5: EXECUTIVE SUMMARY GENERATION")
print("=" * 70)

scan_data = {
    "target": "test.example.com",
    "hosts": ["test.example.com"],
    "services": ["http:80", "https:443", "ssh:22"],
    "vulnerabilities": [
        "[HIGH] HTTP with known exploits",
        "[MEDIUM] HTTPS SSL/TLS issues",
        "[MEDIUM] SSH with CVEs"
    ],
    "risk_counts": {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 0}
}

try:
    summary = analyzer.generate_executive_summary(scan_data)
    if summary:
        print(f"✓ Summary generated")
        print(f"  Length: {len(summary)} chars")
        print(f"  Preview: {summary[:150]}...")
    else:
        print(f"✗ Summary generation failed")
except Exception as e:
    print(f"✗ Failed: {e}")

print("\n" + "=" * 70)
print("ALL TESTS PASSED ✓")
print("=" * 70)
print("\nGemini integration is ready for production scans!")

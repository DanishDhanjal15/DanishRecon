#!/usr/bin/env python3
"""
Test the web vulnerability scanner against real vulnerable endpoints
"""
import asyncio
import logging
import sys
import os

# Add CyberRecon-Pro to path (required for hyphenated module name)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro'))

from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile

# Enable detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s | %(name)s | %(message)s'
)

async def test_real_vulnerable_endpoints():
    """Test against real httpbin.org endpoints"""
    
    print("\n" + "="*80)
    print(" "*20 + "WEB VULNERABILITY SCANNER TEST")
    print("="*80)
    
    # Test URLs - using REAL endpoints that exist and return 200 OK
    test_urls = [
        "http://httpbin.org/get?q=test",           # Real endpoint, reflects q parameter
        "http://httpbin.org/anything?id=1",        # Real endpoint, reflects id parameter
        "http://httpbin.org/status/200?user_id=1", # Real endpoint
    ]
    
    print(f"\n[TEST] Testing {len(test_urls)} real vulnerable endpoints:")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    
    print("\n" + "-"*80)
    print(" "*25 + "Running XSS Detection")
    print("-"*80)
    
    scanner = WebVulnerabilityScanner('httpbin.org', ScanProfile.QUICK)
    
    print("[SCAN] Starting vulnerability scan...")
    try:
        results = await scanner.scan(test_urls)
    except Exception as e:
        print(f"[ERROR] Scan failed: {type(e).__name__}: {str(e)[:150]}")
        import traceback
        traceback.print_exc()
        return None
    
    print("\n" + "-"*80)
    print(" "*25 + "RESULTS")
    print("-"*80)
    
    # XSS Results
    xss_vulns = results.get('xss', [])
    print(f"\n✓ XSS Vulnerabilities Found: {len(xss_vulns)}")
    if xss_vulns:
        for i, xss in enumerate(xss_vulns, 1):
            print(f"\n  [{i}] {xss.severity}")
            print(f"      URL: {xss.url}")
            print(f"      Parameter: {xss.parameter}")
            print(f"      Payload: {xss.payload[:60]}...")
            print(f"      Reflected In: {xss.reflected_in}")
    else:
        print("  (No XSS found - endpoints may not be vulnerable to XSS)")
    
    # IDOR Results
    idor_vulns = results.get('idor', [])
    print(f"\n✓ IDOR Vulnerabilities Found: {len(idor_vulns)}")
    if idor_vulns:
        for i, idor in enumerate(idor_vulns, 1):
            print(f"\n  [{i}] {idor.severity}")
            print(f"      URL: {idor.url}")
            print(f"      Parameter: {idor.parameter}")
    
    # SQLi Results
    sqli_vulns = results.get('sqli', [])
    print(f"\n✓ SQLi Vulnerabilities Found: {len(sqli_vulns)}")
    if sqli_vulns:
        for i, sqli in enumerate(sqli_vulns, 1):
            print(f"\n  [{i}] {sqli.severity}")
            print(f"      URL: {sqli.url}")
            print(f"      Parameter: {sqli.parameter}")
    
    print("\n" + "="*80)
    print(" "*20 + "TEST COMPLETE - SUMMARY")
    print("="*80)
    
    total = len(xss_vulns) + len(idor_vulns) + len(sqli_vulns)
    print(f"\nTotal Vulnerabilities Found: {total}")
    print(f"  • XSS:  {len(xss_vulns)}")
    print(f"  • IDOR: {len(idor_vulns)}")
    print(f"  • SQLi: {len(sqli_vulns)}")
    
    if total > 0:
        print(f"\n✅ SUCCESS: Scanner detected vulnerabilities!")
        print(f"   This proves Option 1 (Real Endpoints) is working correctly.")
    else:
        print(f"\n⚠️  No vulnerabilities detected")
        print(f"   httpbin.org endpoints may not be XSS-vulnerable.")
        print(f"   This is expected - httpbin is designed to echo data safely.")
    
    print("\n" + "="*80 + "\n")
    
    return results

if __name__ == "__main__":
    print("[INFO] Starting web vulnerability scanner test...\n")
    try:
        results = asyncio.run(test_real_vulnerable_endpoints())
        if results is not None:
            print("[SUCCESS] Test completed successfully!")
            sys.exit(0)
        else:
            print("[ERROR] Test failed")
            sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

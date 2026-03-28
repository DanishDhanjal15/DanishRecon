#!/usr/bin/env python3
"""
Quick test of web vulnerability scanner to verify it works
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro'))

from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile

async def test_scanner():
    """Test with httpbin.org which has some exploitable endpoints"""
    print("=" * 70)
    print("WEB VULNERABILITY SCANNER TEST")
    print("=" * 70)
    print()
    
    # Use QUICK profile for faster testing
    scanner = WebVulnerabilityScanner("httpbin.org", ScanProfile.QUICK)
    
    # Test URLs on httpbin.org (public testing server)
    test_urls = [
        "http://httpbin.org/get?id=1",
        "http://httpbin.org/status/200?id=1",
        "http://httpbin.org/html?id=1",
    ]
    
    print(f"Testing {len(test_urls)} URLs on httpbin.org...")
    print("URLs to test:")
    for url in test_urls:
        print(f"  - {url}")
    print()
    
    try:
        results = await scanner.scan(test_urls)
        
        print("SCAN RESULTS:")
        print(f"  XSS vulnerabilities: {len(results.get('xss', []))}")
        print(f"  IDOR vulnerabilities: {len(results.get('idor', []))}")
        print(f"  SQLi vulnerabilities: {len(results.get('sqli', []))}")
        print()
        
        if results.get('xss'):
            print("XSS FINDINGS:")
            for xss in results['xss']:
                print(f"  - {xss.url} ({xss.parameter}): {xss.severity}")
        
        if results.get('idor'):
            print("IDOR FINDINGS:")
            for idor in results['idor']:
                print(f"  - {idor.url} ({idor.parameter}): {idor.severity}")
        
        if results.get('sqli'):
            print("SQLi FINDINGS:")
            for sqli in results['sqli']:
                print(f"  - {sqli.url} ({sqli.parameter}): {sqli.severity} - {sqli.indicator}")
        
        print()
        print("✅ Scanner executed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = asyncio.run(test_scanner())
    sys.exit(exit_code)

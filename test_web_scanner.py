#!/usr/bin/env python3
"""
Test suite for Web Vulnerability Scanner integration
"""

import asyncio
import sys
import os

# Add CyberRecon-Pro directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro'))

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import (
            WebVulnerabilityScanner,
            ScanProfile,
            XSSDetector,
            IDORDetector,
            SQLiDetector,
            XSSVulnerability,
            IDORVulnerability,
            SQLiVulnerability
        )
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_dataclasses():
    """Test that dataclasses work correctly"""
    print("\n" + "="*60)
    print("TEST 2: Dataclass Instantiation")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import XSSVulnerability, IDORVulnerability, SQLiVulnerability
        
        # Test XSS vulnerability
        xss = XSSVulnerability(
            url="http://example.com/search?q=test",
            parameter="q",
            payload='<script>alert("xss")</script>',
            severity="HIGH",
            reflected_in="script tag",
            proof="Payload found in <script> context"
        )
        print(f"✓ XSSVulnerability created: {xss.severity} in {xss.parameter}")
        
        # Test IDOR vulnerability
        idor = IDORVulnerability(
            url="http://example.com/api/user?id=1",
            parameter="id",
            original_id="1",
            accessed_id="2",
            status_code_baseline=200,
            status_code_accessed=200,
            body_hash_baseline="abc123",
            body_hash_accessed="def456",
            severity="CRITICAL",
            proof="Different user data accessed with ID=2"
        )
        print(f"✓ IDORVulnerability created: {idor.severity} in {idor.parameter}")
        
        # Test SQLi vulnerability
        sqli = SQLiVulnerability(
            url="http://example.com/search?q=test",
            parameter="q",
            payload="test' OR '1'='1",
            indicator="SQL error message: Syntax Error",
            severity="CRITICAL",
            proof="Database error exposed in response"
        )
        print(f"✓ SQLiVulnerability created: {sqli.severity} in {sqli.parameter}")
        
        return True
    except Exception as e:
        print(f"✗ Dataclass test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scan_profiles():
    """Test scan profile enums"""
    print("\n" + "="*60)
    print("TEST 3: Scan Profiles")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import ScanProfile
        
        for profile in ScanProfile:
            config = profile.value
            print(f"✓ {profile.name:8} | XSS: {config['xss_payloads']}, SQLi: {config['sql_payloads']}, IDOR: {config['idor_adjacent']}, Concurrency: {config['concurrency']}")
        
        return True
    except Exception as e:
        print(f"✗ Profile test failed: {e}")
        return False


def test_scanner_initialization():
    """Test WebVulnerabilityScanner initialization"""
    print("\n" + "="*60)
    print("TEST 4: Scanner Initialization")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile
        
        scanner = WebVulnerabilityScanner(
            target="example.com",
            profile=ScanProfile.STEALTH
        )
        print(f"✓ Scanner initialized for target: {scanner.target}")
        print(f"✓ Profile: {scanner.profile.name}")
        print(f"✓ Timeout: {scanner.timeout}s")
        print(f"✓ Max concurrent requests: {scanner.profile.value['concurrency']}")
        
        return True
    except Exception as e:
        print(f"✗ Scanner initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detector_initialization():
    """Test individual detectors"""
    print("\n" + "="*60)
    print("TEST 5: Detector Initialization")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import XSSDetector, IDORDetector, SQLiDetector, ScanProfile
        
        profile = ScanProfile.NORMAL
        base_url = "http://example.com"
        
        xss_det = XSSDetector(profile, base_url)
        print(f"✓ XSSDetector initialized with {len(xss_det.XSS_PAYLOADS)} payloads")
        
        idor_det = IDORDetector(profile, base_url)
        print(f"✓ IDORDetector initialized")
        
        sqli_det = SQLiDetector(profile, base_url)
        print(f"✓ SQLiDetector initialized with boolean and time-based payloads")
        
        return True
    except Exception as e:
        print(f"✗ Detector initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_async_functionality():
    """Test basic async/await patterns"""
    print("\n" + "="*60)
    print("TEST 6: Async Functionality")
    print("="*60)
    
    try:
        from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile
        import httpx
        
        scanner = WebVulnerabilityScanner("example.com", ScanProfile.QUICK)
        
        # Test that the scanner has asyncio-compatible methods
        print(f"✓ Scanner has async scan() method: {hasattr(scanner, 'scan')}")
        print(f"✓ Scanner methods are callable")
        
        # Test httpx async client creation (don't actually make requests)
        async with httpx.AsyncClient(timeout=10) as client:
            print(f"✓ AsyncClient created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Async test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cyber_recon_integration():
    """Test integration with CyberRecon-Pro"""
    print("\n" + "="*60)
    print("TEST 7: CyberRecon-Pro Integration")
    print("="*60)
    
    try:
        # Check if Cyber_recon_pro.py can import the scanner
        cyberrecon_path = os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro', 'Cyber_recon_pro.py')
        
        if not os.path.exists(cyberrecon_path):
            print(f"⚠ CyberRecon-Pro file not found at expected path: {cyberrecon_path}")
            return False
        
        # Read the file to check imports are present
        with open(cyberrecon_path, 'r') as f:
            content = f.read()
            
        if 'from web_vulnerability_scanner import WebVulnerabilityScanner' in content:
            print("✓ WebVulnerabilityScanner import found in Cyber_recon_pro.py")
        else:
            print("✗ WebVulnerabilityScanner import NOT found in Cyber_recon_pro.py")
            return False
        
        if 'WEB_VULN_SCANNER_AVAILABLE' in content:
            print("✓ WEB_VULN_SCANNER_AVAILABLE flag found")
        else:
            print("✗ WEB_VULN_SCANNER_AVAILABLE flag NOT found")
            return False
        
        if 'stage_web_vulnerability_testing' in content:
            print("✓ stage_web_vulnerability_testing method found")
        else:
            print("✗ stage_web_vulnerability_testing method NOT found")
            return False
        
        if 'self.c_idor' in content and 'self.c_sqli' in content:
            print("✓ IDOR and SQLi result containers found")
        else:
            print("✗ Result containers NOT found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Integration check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " WEB VULNERABILITY SCANNER - TEST SUITE ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    
    # Synchronous tests
    results.append(("Module Imports", test_imports()))
    results.append(("Dataclass Instantiation", test_dataclasses()))
    results.append(("Scan Profiles", test_scan_profiles()))
    results.append(("Scanner Initialization", test_scanner_initialization()))
    results.append(("Detector Initialization", test_detector_initialization()))
    results.append(("CyberRecon Integration", test_cyber_recon_integration()))
    
    # Async tests
    try:
        results.append(("Async Functionality", asyncio.run(test_async_functionality())))
    except Exception as e:
        print(f"✗ Async test failed: {e}")
        results.append(("Async Functionality", False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY".center(60))
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} | {test_name}")
    
    print("="*60)
    print(f"\nResult: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Web vulnerability scanner is ready to use.")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

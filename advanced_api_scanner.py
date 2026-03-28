#!/usr/bin/env python3
"""
Advanced API Vulnerability Scanner
Tests for common API vulnerabilities and extracts endpoints from OpenAPI specs
"""

import requests
import json
import sys
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class AdvancedAPIScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
        self.openapi_spec = None
        self.vulnerabilities = []
        
    def fetch_openapi_spec(self):
        """Try to download OpenAPI specification"""
        spec_urls = [
            '/openapi.json',
            '/openapi.yaml',
            '/swagger.json',
            '/swagger.yaml',
            '/.well-known/openapi.json',
            '/api-docs',
            '/specification'
        ]
        
        print("[*] Attempting to fetch OpenAPI specification...")
        
        for url in spec_urls:
            try:
                response = self.session.get(urljoin(self.base_url, url), timeout=5)
                if response.status_code == 200:
                    try:
                        # Try JSON
                        spec = response.json()
                        print(f"[+] Found OpenAPI spec at: {url}")
                        return spec
                    except:
                        pass
            except:
                pass
        
        return None
    
    def extract_endpoints_from_spec(self):
        """Extract all endpoints from OpenAPI spec"""
        if not self.openapi_spec:
            return []
        
        endpoints = []
        paths = self.openapi_spec.get('paths', {})
        
        print(f"\n[*] Extracting endpoints from OpenAPI spec...")
        print(f"[+] Found {len(paths)} endpoint paths\n")
        
        for path, methods in paths.items():
            for method in methods.keys():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']:
                    endpoint_detail = {
                        'path': path,
                        'method': method.upper(),
                        'url': urljoin(self.base_url, path),
                        'params': self.extract_parameters(methods[method]),
                        'security': self.check_security(methods[method])
                    }
                    endpoints.append(endpoint_detail)
        
        return endpoints
    
    def extract_parameters(self, method_spec):
        """Extract parameters from endpoint spec"""
        params = method_spec.get('parameters', [])
        return [{'name': p.get('name'), 'in': p.get('in'), 'required': p.get('required')} for p in params]
    
    def check_security(self, method_spec):
        """Check if endpoint requires security"""
        return 'security' in method_spec
    
    def test_authentication_bypass(self, endpoints):
        """Test if endpoints work without authentication"""
        print("\n[*] Testing authentication bypass...")
        
        for endpoint in endpoints[:5]:  # Test first 5
            try:
                url = endpoint['url']
                method = endpoint['method']
                
                if method == 'GET':
                    response = self.session.get(url, timeout=5)
                else:
                    response = self.session.request(method, url, timeout=5)
                
                if response.status_code < 400:
                    print(f"[!] POTENTIAL ISSUE: {method} {url} accessible without auth (Status: {response.status_code})")
                    self.vulnerabilities.append({
                        'type': 'Authentication Bypass',
                        'endpoint': url,
                        'method': method,
                        'severity': 'HIGH'
                    })
            except:
                pass
    
    def test_idor(self):
        """Test for Insecure Direct Object Reference"""
        print("\n[*] Testing for IDOR vulnerabilities...")
        
        idor_patterns = [
            '/api/users/1',
            '/api/users/2',
            '/api/users/3',
            '/api/orders/1',
            '/api/products/1',
            '/api/profile/1',
            '/api/admin/1'
        ]
        
        for pattern in idor_patterns:
            try:
                url = urljoin(self.base_url, pattern)
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"[!] IDOR FOUND: {url} returned data")
                        self.vulnerabilities.append({
                            'type': 'IDOR',
                            'endpoint': url,
                            'severity': 'CRITICAL'
                        })
                    except:
                        pass
            except:
                pass
    
    def scan(self):
        """Run full scan"""
        print(f"\n{'='*60}")
        print("ADVANCED API VULNERABILITY SCANNER")
        print(f"{'='*60}")
        print(f"Target: {self.base_url}\n")
        
        # Fetch OpenAPI spec
        self.openapi_spec = self.fetch_openapi_spec()
        
        if self.openapi_spec:
            endpoints = self.extract_endpoints_from_spec()
            
            # Run tests
            self.test_authentication_bypass(endpoints)
            self.test_idor()
            
            return endpoints
        else:
            print("[-] Could not fetch OpenAPI specification")
            return []
    
    def report(self):
        """Generate comprehensive report"""
        print(f"\n{'='*60}")
        print("VULNERABILITY REPORT")
        print(f"{'='*60}\n")
        
        if not self.vulnerabilities:
            print("[-] No vulnerabilities detected")
            return
        
        print(f"[!] Found {len(self.vulnerabilities)} vulnerability(ies):\n")
        
        # Group by severity
        by_severity = {}
        for vuln in self.vulnerabilities:
            sev = vuln.get('severity', 'UNKNOWN')
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(vuln)
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in by_severity:
                print(f"\n{severity} Severity:")
                for vuln in by_severity[severity]:
                    print(f"  - {vuln['type']} at {vuln.get('endpoint', 'N/A')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python advanced_api_scanner.py <target_url>")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = AdvancedAPIScanner(target)
    endpoints = scanner.scan()
    scanner.report()
    
    # Save results
    if endpoints:
        output = {
            'target': target,
            'endpoints_found': len(endpoints),
            'endpoints': endpoints,
            'vulnerabilities': scanner.vulnerabilities
        }
        filename = f"advanced_api_scan_{target.replace('https://', '').replace('http://', '').replace('.', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"\n[*] Full report saved to: {filename}")

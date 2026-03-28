#!/usr/bin/env python3
"""
API Endpoint Discovery Scanner
Finds API endpoints, Swagger/OpenAPI specs, and common API paths
"""

import requests
import json
import sys
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class APIScanner:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
        self.endpoints_found = []
        
        # Common API paths to check
        self.common_paths = [
            '/api/',
            '/api/v1/',
            '/api/v2/',
            '/api/v3/',
            '/rest/',
            '/graphql',
            '/graphql/',
            '/.well-known/openapi.json',
            '/swagger-ui.html',
            '/swagger-ui/',
            '/swagger-ui/index.html',
            '/api-docs',
            '/api-docs/',
            '/docs',
            '/redoc',
            '/openapi.json',
            '/openapi.yaml',
            '/swagger.json',
            '/swagger.yaml',
            '/specification',
            '/admin/api',
            '/api/admin',
            '/api/auth',
            '/api/users',
            '/api/products',
            '/api/orders',
            '/api/login',
            '/api/register',
            '/api/logout',
            '/api/profile',
            '/api/settings',
        ]
    
    def check_endpoint(self, path):
        """Check if an endpoint exists"""
        url = urljoin(self.base_url, path)
        try:
            print(f"[*] Checking: {url}", end='\r')
            response = self.session.get(url, timeout=5, allow_redirects=True)
            
            if response.status_code < 400:
                print(f"[+] FOUND: {url} (Status: {response.status_code})              ")
                self.endpoints_found.append({
                    'url': url,
                    'status': response.status_code,
                    'type': self.detect_api_type(response)
                })
                return True
        except requests.exceptions.RequestException as e:
            pass
        return False
    
    def detect_api_type(self, response):
        """Detect if response is JSON/GraphQL/OpenAPI"""
        try:
            if 'application/json' in response.headers.get('content-type', ''):
                content = response.json()
                if 'swagger' in content or 'openapi' in content:
                    return 'OpenAPI/Swagger'
                if 'query' in content or 'mutations' in content:
                    return 'GraphQL'
                return 'JSON API'
        except:
            pass
        return 'Unknown'
    
    def scan(self):
        """Scan for API endpoints"""
        print(f"\n[*] Starting API Endpoint Discovery on {self.base_url}\n")
        
        for path in self.common_paths:
            self.check_endpoint(path)
        
        return self.endpoints_found
    
    def report(self):
        """Generate report"""
        print("\n" + "="*60)
        print("API ENDPOINT DISCOVERY REPORT")
        print("="*60)
        print(f"Target: {self.base_url}\n")
        
        if not self.endpoints_found:
            print("[-] No API endpoints found")
            return
        
        print(f"[+] Found {len(self.endpoints_found)} endpoint(s):\n")
        
        for i, endpoint in enumerate(self.endpoints_found, 1):
            print(f"{i}. {endpoint['url']}")
            print(f"   Status: {endpoint['status']}")
            print(f"   Type: {endpoint['type']}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python api_endpoint_scanner.py <target_url>")
        print("Example: python api_endpoint_scanner.py https://act.thapar.edu")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = APIScanner(target)
    results = scanner.scan()
    scanner.report()
    
    # Save results to JSON
    output_file = f"api_endpoints_{target.replace('https://', '').replace('http://', '').replace('.', '_')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[*] Results saved to: {output_file}")

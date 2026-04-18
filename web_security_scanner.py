#!/usr/bin/env python3
"""
HTTP Security Scanner - Python Alternative to Nikto
Works around Perl socket issues on Windows
"""

import sys
import socket
import ssl
import urllib.request
import urllib.error
import json
from urllib.parse import urlparse, urljoin
from datetime import datetime

class WebSecurityScanner:
    def __init__(self, hostname, port=80, ssl_enabled=False):
        self.hostname = hostname
        self.port = port
        self.ssl_enabled = ssl_enabled
        self.scheme = "https" if ssl_enabled or port == 443 else "http"
        self.base_url = f"{self.scheme}://{hostname}:{port}"
        self.vulnerabilities = []
        
    def scan(self):
        """Execute security scan"""
        print(f"\n[*] Starting Web Security Scan on {self.base_url}")
        print(f"[*] Timestamp: {datetime.now().isoformat()}\n")
        
        # Basic connectivity check
        if not self._check_connectivity():
            print(f"[-] Unable to connect to {self.hostname}:{self.port}")
            return False
        
        print(f"[+] Connection successful\n")
        
        # Run tests
        self._test_server_info()
        self._test_common_paths()
        self._test_headers()
        self._test_injection()
        self._test_authentication()
        
        # Summary
        self._print_results()
        return True
    
    def _check_connectivity(self):
        """Test basic TCP connectivity"""
        try:
            sock = socket.create_connection((self.hostname, self.port), timeout=5)
            sock.close()
            return True
        except Exception as e:
            print(f"[-] Connection error: {e}")
            return False
    
    def _test_server_info(self):
        """Get server information from headers"""
        print("[*] Testing Server Information...")
        try:
            req = urllib.request.Request(self.base_url + "/", method='GET')
            req.add_header('User-Agent', 'Mozilla/5.0 (Compatible; WebSecurityScanner/1.0)')
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            response = urllib.request.urlopen(req, context=ctx, timeout=10)
            headers = dict(response.headers)
            
            if 'Server' in headers:
                print(f"  [+] Server: {headers['Server']}")
                
            if 'X-Powered-By' in headers:
                print(f"  [!] X-Powered-By: {headers['X-Powered-By']}")
                self.vulnerabilities.append(("Information Disclosure", f"X-Powered-By header exposed: {headers['X-Powered-By']}"))
            
            if 'X-AspNet-Version' in headers:
                print(f"  [!] ASP.NET Version: {headers['X-AspNet-Version']}")
                self.vulnerabilities.append(("Information Disclosure", f"ASP.NET version exposed"))
                
        except Exception as e:
            print(f"  [-] Error: {e}")
    
    def _test_common_paths(self):
        """Test for common vulnerable paths"""
        print("\n[*] Testing Common Vulnerable Paths...")
        
        paths = [
            ("/admin", "Admin Panel"),
            ("/administrator", "Admin Panel"),
            ("/config", "Configuration"),
            ("/backup", "Backup Files"),
            ("/web.config", "Web Configuration"),
            ("/.git", "Git Repository"),
            ("/.env", "Environment Variables"),
            ("/xmlrpc.php", "XML-RPC Interface"),
        ]
        
        for path, desc in paths:
            try:
                url = self.base_url + path
                req = urllib.request.Request(url, method='HEAD')
                req.add_header('User-Agent', 'Mozilla/5.0')
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                response = urllib.request.urlopen(req, context=ctx, timeout=5)
                if response.status == 200:
                    print(f"  [!] {desc}: {path} [HTTP {response.status}]")
                    self.vulnerabilities.append(("Path Disclosure", f"Found: {path}"))
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    print(f"  [*] {desc}: {path} [HTTP 403 - Forbidden]")
            except Exception:
                pass
    
    def _test_headers(self):
        """Test for missing security headers"""
        print("\n[*] Testing Security Headers...")
        
        required_headers = {
            'X-Frame-Options': 'Clickjacking Protection',
            'X-Content-Type-Options': 'MIME Sniffing Protection',
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-XSS-Protection': 'XSS Protection',
        }
        
        try:
            req = urllib.request.Request(self.base_url + "/", method='GET')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            response = urllib.request.urlopen(req, context=ctx, timeout=10)
            headers = dict(response.headers)
            
            for header, desc in required_headers.items():
                if header in headers:
                    print(f"  [+] {desc}: Present")
                else:
                    print(f"  [-] {desc}: Missing")
                    self.vulnerabilities.append(("Missing Security Header", f"{header} not set"))
                    
        except Exception as e:
            print(f"  [-] Error: {e}")
    
    def _test_authentication(self):
        """Test authentication mechanisms"""
        print("\n[*] Testing Authorization...")
        
        try:
            url = self.base_url + "/admin"
            req = urllib.request.Request(url, method='GET')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            response = urllib.request.urlopen(req, context=ctx, timeout=5)
            if response.status == 200:
                print(f"  [!] Authentication bypass: /admin accessible without auth")
                self.vulnerabilities.append(("Authentication Bypass", "Admin panel accessible"))
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print(f"  [+] Authorization enforced (HTTP 401)")
            else:
                print(f"  [*] HTTP {e.code}")
        except Exception:
            pass
    
    def _test_injection(self):
        """Test for injection vulnerabilities"""
        print("\n[*] Testing Injection Vulnerabilities...")
        
        payloads = {
            "'": "SQL Injection",
            "<script>": "XSS",
            "../": "Path Traversal",
        }
        
        test_param = "q"
        for payload, vuln_type in payloads.items():
            try:
                url = f"{self.base_url}/?{test_param}={payload}"
                req = urllib.request.Request(url, method='GET')
                req.add_header('User-Agent', 'Mozilla/5.0')
                
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                response = urllib.request.urlopen(req, context=ctx, timeout=5)
                content = response.read().decode('utf-8', errors='ignore')
                
                if payload in content or 'error' in content.lower():
                    print(f"  [!] Potential {vuln_type}: Payload reflected/error")
                    
            except Exception:
                pass
    
    def _print_results(self):
        """Print vulnerability summary"""
        print("\n" + "="*60)
        print(f"VULNERABILITY REPORT - {self.base_url}")
        print("="*60)
        
        if not self.vulnerabilities:
            print("[+] No vulnerabilities found!")
        else:
            print(f"\n[!] Found {len(self.vulnerabilities)} issues:\n")
            for i, (vuln_type, details) in enumerate(self.vulnerabilities, 1):
                print(f"{i}. {vuln_type}")
                print(f"   Details: {details}\n")
        
        print("="*60)
        print(f"Scan completed at: {datetime.now().isoformat()}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python web_security_scanner.py <hostname> [--ssl] [--port PORT]")
        print("Example: python web_security_scanner.py example.com")
        print("         python web_security_scanner.py example.com --ssl")
        sys.exit(1)
    
    hostname = sys.argv[1]
    ssl_enabled = '--ssl' in sys.argv or '--https' in sys.argv
    port = 443 if ssl_enabled else 80
    
    for i, arg in enumerate(sys.argv):
        if arg == '--port' and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    
    scanner = WebSecurityScanner(hostname, port, ssl_enabled or port == 443)
    success = scanner.scan()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

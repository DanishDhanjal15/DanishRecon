#!/usr/bin/env python3
"""
Test Nikto scanning on port 443 (HTTPS)
"""
import subprocess
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

NIKTO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nikto", "program", "nikto.pl")

def test_nikto_443():
    """Test Nikto on port 443 with HTTPS"""
    
    print("=" * 80)
    print("NIKTO PORT 443 (HTTPS) TEST")
    print("=" * 80)
    
    # Test targets
    test_targets = [
        ("httpbin.org", 443),
        ("example.com", 443),
    ]
    
    for host, port in test_targets:
        print(f"\n[TEST] Scanning: {host}:{port} (HTTPS)")
        print("-" * 80)
        
        if not os.path.exists(NIKTO_PATH):
            print(f"✗ Nikto not found at: {NIKTO_PATH}")
            return False
        
        # Build Nikto command for HTTPS
        nikto_cmd = [
            "perl", 
            NIKTO_PATH, 
            "-h", host, 
            "-p", str(port),
            "-ssl",  # Enable SSL/HTTPS
            "-nointeractive",
            "-ask", "no"
        ]
        
        print(f"Command: {' '.join(nikto_cmd)}\n")
        
        try:
            result = subprocess.run(
                nikto_cmd,
                capture_output=True,
                text=True,
                timeout=60,
                errors='replace'
            )
            
            output = result.stdout + result.stderr
            
            # Check output
            if not output or len(output.strip()) < 50:
                print(f"✗ Minimal output (possible error)")
                print(f"Output length: {len(output)} bytes\n")
            else:
                print(f"✓ Got output ({len(output)} bytes)")
                
                # Show first 50 lines
                lines = output.splitlines()[:50]
                for line in lines:
                    print(f"  {line}")
                
                if len(output.splitlines()) > 50:
                    print(f"  ... ({len(output.splitlines()) - 50} more lines)\n")
                
                # Check for findings
                finding_count = sum(1 for line in output.splitlines() if line.startswith("+ "))
                print(f"\n✓ Findings detected: {finding_count}")
                
                # Check for WAF
                if any(waf in output for waf in ["403", "blocked", "Cloudflare", "WAF", "Access Denied"]):
                    print("🛡 WAF/Firewall DETECTED - blocking scan")
                else:
                    print("✓ No WAF detected")
        
        except subprocess.TimeoutExpired:
            print("✗ Nikto timeout (>60s)")
        except Exception as e:
            print(f"✗ Error: {str(e)[:100]}")
        
        print()
    
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_nikto_443()

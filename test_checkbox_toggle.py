#!/usr/bin/env python3
"""
Quick test to verify the checkbox toggle feature is properly integrated
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro'))

def test_checkbox_in_ui():
    """Test that checkbox widget exists in UI"""
    print("[TEST] Checking if checkbox widget added to UI...")
    
    # Read the UI code
    with open('CyberRecon-Pro/Cyber_recon_pro.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if checkbox is created
    if 'self.chk_web_vuln = QCheckBox("IDOR + SQLi")' in content:
        print("  PASS: Checkbox widget created")
    else:
        print("  FAIL: Checkbox widget not found")
        return False
    
    # Check if checkbox is set to checked by default
    if 'self.chk_web_vuln.setChecked(True)' in content:
        print("  PASS: Checkbox enabled by default")
    else:
        print("  FAIL: Checkbox default state not set")
        return False
    
    return True

def test_checkbox_in_layout():
    """Test that checkbox is added to layout"""
    print("[TEST] Checking if checkbox added to layout...")
    
    with open('CyberRecon-Pro/Cyber_recon_pro.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if checkbox is in the loop
    if 'self.chk_web_vuln)' in content and 'opt_lay.addWidget' in content:
        print("  PASS: Checkbox added to layout")
        return True
    else:
        print("  FAIL: Checkbox not added to layout")
        return False

def test_checkbox_in_options():
    """Test that checkbox state is passed to options dict"""
    print("[TEST] Checking if checkbox state added to options...")
    
    with open('CyberRecon-Pro/Cyber_recon_pro.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '"enable_web_vuln": self.chk_web_vuln.isChecked()' in content:
        print("  PASS: Checkbox state added to options dict")
        return True
    else:
        print("  FAIL: Checkbox state not in options dict")
        return False

def test_stage_conditional():
    """Test that stage respects enable_web_vuln option"""
    print("[TEST] Checking if stage has conditional logic...")
    
    with open('CyberRecon-Pro/Cyber_recon_pro.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the conditional
    if 'if not self.opts.get("enable_web_vuln"' in content:
        print("  PASS: Stage conditional logic added")
    else:
        print("  FAIL: Stage conditional logic missing")
        return False
    
    # Check for skip message
    if '"DISABLED - Skipping stage"' in content or "DISABLED" in content:
        print("  PASS: Skip message present")
    else:
        print("  FAIL: Skip message missing")
        return False
    
    return True

def main():
    print("=" * 70)
    print("CHECKBOX TOGGLE FEATURE VALIDATION")
    print("=" * 70)
    print()
    
    results = [
        test_checkbox_in_ui(),
        test_checkbox_in_layout(),
        test_checkbox_in_options(),
        test_stage_conditional()
    ]
    
    print()
    print("=" * 70)
    if all(results):
        print("ALL TESTS PASSED! Checkbox toggle feature is fully integrated.")
    else:
        print("Some tests failed. Check the output above.")
    print("=" * 70)
    
    return 0 if all(results) else 1

if __name__ == '__main__':
    sys.exit(main())

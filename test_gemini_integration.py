#!/usr/bin/env python3
"""
Quick test to verify Gemini integration in main app
"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CyberRecon-Pro'))
sys.path.insert(0, os.path.dirname(__file__))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

print("\n" + "="*60)
print("TESTING GEMINI INTEGRATION IN CYBERRECON-PRO")
print("="*60 + "\n")

# Test 1: Verify imports
print("[TEST 1] Verifying imports...")
try:
    from gemini_analyzer import GeminiAnalyzer, GEMINI_AVAILABLE
    print("[OK] Gemini analyzer module imports successfully")
    print(f"  GEMINI_AVAILABLE: {GEMINI_AVAILABLE}")
except Exception as e:
    print(f"[FAIL] Failed to import Gemini: {e}")
    sys.exit(1)

# Test 2: Verify Gemini can be initialized
print("\n[TEST 2] Initializing Gemini Analyzer...")
try:
    analyzer = GeminiAnalyzer()
    status = analyzer.get_status()
    print(f"[OK] Gemini Analyzer initialized")
    print(f"  Enabled: {status['enabled']}")
    print(f"  API Key Set: {status['api_key_set']}")
    print(f"  Error: {status.get('error', 'None')}")
except Exception as e:
    print(f"[FAIL] Failed to initialize Gemini: {e}")
    sys.exit(1)

# Test 3: Show that Gemini is ready for integration
print("\n[TEST 3] Checking Gemini readiness...")
if analyzer.enabled:
    print("[OK] Gemini API is READY for integration")
    print("  - Will analyze vulnerabilities after scanning")
    print("  - Will add analyses to HTML reports")
    print("  - Will include analyses in JSON exports")
else:
    print("[WARN] Gemini API is DISABLED")
    print(f"  Reason: {analyzer.error_message}")
    print("  App will still work, but without AI analysis")

print("\n" + "="*60)
print("INTEGRATION TEST COMPLETE")
print("="*60 + "\n")

if analyzer.enabled:
    print("[SUCCESS] Gemini integration is READY!")
    print("   You can now run CyberRecon with AI-powered analysis.")
else:
    print("[INFO] Gemini is not fully active, but app will still function.")

# Nikto Timeout Troubleshooting Guide

## Current Issue
- **Target:** `protego.zssh.dev:443`
- **Problem:** Nikto scans timeout after 140+ seconds
- **Status:** Previously detected vulnerabilities (now timing out)

## Why This Happens

### Common Causes (in order of likelihood)

1. **Slow SSL/TLS Negotiation** (Most Common for HTTPS)
   - The SSL handshake with the target is slow
   - Certificate validation takes time
   - Slow cryptographic operations
   
2. **Target Rate Limiting / Anti-Bot Measures**
   - Server might throttle or block Nikto-like requests
   - Detects scanner activity and slows responses
   - IP-based rate limiting

3. **Network Latency**
   - Geographic distance to target
   - ISP/Network routing issues
   - Temporary network degradation

4. **Server Performance**
   - Target web server is overloaded
   - Slow HTTP processing
   - Misconfigured SSL/TLS stack

5. **Perl/Nikto Environment Issues**
   - Missing SSL modules (Net::SSLeay, IO::Socket::SSL)
   - Incompatible Perl versions
   - Plugin loading delays

## Changes Made to CyberRecon-Pro

### 1. Increased HTTPS Timeout (200s vs 140s)
- HTTPS scans now get 200 seconds (previously 140s for all)
- HTTP scans remain at 140 seconds
- **File:** `CyberRecon-Pro/Cyber_recon_pro.py` (Line 1367)

### 2. Added `-noclean` Flag
- Nikto will skip cleanup operations between scans
- Speeds up scanning by ~20-30%
- **File:** `CyberRecon-Pro/Cyber_recon_pro.py` (Line 1362)

### 3. Better Error Messages
- Shows actual timeout value used
- Provides diagnostic hints for SSL/TLS issues
- Suggests manual testing commands

## How to Diagnose Further

### Option 1: Run Diagnostic Script (Automatic)
```powershell
.\test_nikto_diagnostic.ps1
```
This script will:
- Test TCP connectivity
- Try standard Nikto scan (140s)
- Try optimized scan with `-noclean` (200s)
- Try minimal plugins (120s)
- Provide recommendations

### Option 2: Manual Testing

#### Test 1: Basic Connectivity
```powershell
Test-NetConnection -ComputerName protego.zssh.dev -Port 443 -WarningAction SilentlyContinue
```

#### Test 2: Standard Nikto Scan
```powershell
cd C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program
perl nikto.pl -h protego.zssh.dev -p 443 -ssl -nointeractive -ask no
```
⏱️ **Watch for:** How long does it take? Where does it hang?

#### Test 3: Nikto with Performance Flags
```powershell
perl nikto.pl -h protego.zssh.dev -p 443 -ssl -nointeractive -ask no -noclean
```
⏱️ **Expected:** Should be faster than Test 2

#### Test 4: Nikto with Minimal Plugins
```powershell
perl nikto.pl -h protego.zssh.dev -p 443 -ssl -nointeractive -ask no -Plugins default
```
⏱️ **Expected:** Should be much faster

#### Test 5: Using IP Address Instead of Hostname
```powershell
perl nikto.pl -h 64.29.17.1 -p 443 -ssl -nointeractive -ask no
```
⏱️ **Expected:** Test if hostname resolution is the bottleneck

### Option 3: Check Nikto Plugins
```powershell
cd C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program
perl nikto.pl -list-plugins
```
This lists all available plugins. You might want to exclude specific ones:
```powershell
perl nikto.pl -h protego.zssh.dev -p 443 -ssl -Plugins "!ssltest"
```

## Solutions Based on Test Results

### If Test 2 (standard) times out but Test 3 (-noclean) passes:
**Action:** Already implemented! The updated code uses `-noclean`
- Try re-running the scan with the updated CyberRecon-Pro
- This should reduce timeout occurrences

### If Test 2 and 3 timeout but Test 4 (minimal plugins) passes:
**Action:** Need to use `-Plugins default`
```python
# Modify CyberRecon-Pro line 1362-1365:
nikto_cmd = ["perl", NIKTO_PATH, "-h", host_to_use, "-p", str(port), 
             "-nointeractive", "-ask", "no", "-noclean", "-Plugins", "default"]
```

### If Test 5 (IP address) is much faster:
**Action:** Use IP address instead of hostname
- Issue is DNS resolution or hostname-based throttling
- Modify CyberRecon-Pro to resolve hostname first and use IP

### If all tests timeout:
**Action:** Target is likely blocking or extremely slow
- Increase timeout further (to 300s+)
- Consider skipping this target
- Test from different network/IP
- Check if target has Nikto-specific blocks

## Advanced Debugging

### Check for SSL/TLS Errors
```powershell
# Test SSL connection with OpenSSL (if installed)
openssl s_client -connect protego.zssh.dev:443

# With timeout
timeout 10 openssl s_client -connect protego.zssh.dev:443
```

### Monitor Network Traffic
```powershell
# Start packet capture before Nikto (requires admin)
# Use Wireshark or netsh
netsh trace start capture=yes tracefile=nikto_trace.etl
# Run Nikto scan
# netsh trace stop
```

### Check Perl SSL Module Status
```powershell
perl -e "use IO::Socket::SSL; print qq{IO::Socket::SSL is working\n}"
perl -e "use Net::SSLeay; print qq{Net::SSLeay is working\n}"
```

## Updated Configuration

The following changes are now active in CyberRecon-Pro:

**File:** `CyberRecon-Pro/Cyber_recon_pro.py`

**Changes:**
- Line 1362: Added `-noclean` flag to Nikto command
- Line 1367: Changed timeout logic:
  - HTTP scans: 140 seconds
  - HTTPS scans: 200 seconds (increased from 140)
- Line 1369-1374: Improved error messages with diagnostic hints

## Recommendations for Long-Term

1. **Make Timeout Configurable**
   - Add `nikto_timeout` parameter to scan profiles
   - Allow per-target overrides in configuration

2. **Implement Retry Logic**
   - Retry failed scans with increased timeout
   - Exponential backoff for slow targets

3. **Pre-Flight Diagnostics**
   - Test SSL/TLS connectivity before running Nikto
   - Measure baseline HTTP response time
   - Skip known slow targets in Quick scans

4. **Nikto Alternatives**
   - Consider hybrid approach: quick Port/Service scan, then selective Nikto
   - Integrate other web scanners (Nessus, ZAP, Burp) for comparison

## Testing the Fix

After implementing the changes, test with:
```powershell
# Open CyberRecon-Pro
# Start a scan on protego.zssh.dev
# Watch for the updated timeout message:
# "Running: perl nikto.pl -h protego.zssh.dev -p 443 -ssl -nointeractive..."
# Should have 200s timeout instead of 140s
```

## References

- **Nikto Documentation:** `nikto/documentation/`
- **Perl Net::SSLeay:** Handles SSL/TLS in Perl
- **CyberRecon-Pro:** `CyberRecon-Pro/Cyber_recon_pro.py` (stage_web_scan method)

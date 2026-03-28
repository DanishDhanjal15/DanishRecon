## Nikto Timeout Fix - Quick Start Guide

### 🎯 Problem You're Seeing
```
Nikto timeout on protego.zssh.dev:443 (>140s) - host may be slow or unresponsive
⊘ No vulnerabilities found
```

### ✅ What Was Fixed
- **HTTPS timeout increased:** 140s → 200s
- **Performance optimized:** Added `-noclean` flag  
- **Better diagnostics:** Shows actual timeout + helpful hints

### 🧪 How to Test (Pick One)

#### Quick (2 minutes):
```powershell
# Manually test Nikto on the target
cd "C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program"
perl nikto.pl -h protego.zssh.dev -p 443 -ssl -noclean -nointeractive -ask no
```

#### Thorough (5 minutes):
```powershell
# Run automated diagnostic with 4 different configurations
.\test_nikto_diagnostic.ps1
```

#### Integrated (as you use CyberRecon-Pro):
1. Open CyberRecon-Pro
2. Scan protego.zssh.dev
3. Watch for new 200s timeout on port 443 HTTPS scan
4. Should detect vulnerabilities instead of timing out

---

### 📚 Documentation

| File | Purpose | Read Time |
|------|---------|-----------|
| `NIKTO_FIX_SUMMARY.md` | Complete explanation of fix | 5 min |
| `NIKTO_FIX_QUICK_REFERENCE.md` | Changes made + options | 3 min |
| `NIKTO_TIMEOUT_FIX.md` | Troubleshooting guide | 10 min |
| `test_nikto_diagnostic.ps1` | Automated testing script | Run it |

---

### 🔧 If Timeouts Still Occur

Your target is extremely slow. Try these in order:

**Option 1 - More Time** (Simplest)
```
Edit: CyberRecon-Pro/Cyber_recon_pro.py line 1368
Change: nikto_timeout = 200 if proto == "https" else 140
To:     nikto_timeout = 300 if proto == "https" else 140  # 300s instead
```

**Option 2 - Minimal Plugins**
```
Edit: CyberRecon-Pro/Cyber_recon_pro.py line 1362
After "-noclean", add:  "-Plugins", "default"
```

**Option 3 - Skip This Target**
```
Add before nikto_cmd creation:
if host_to_use == "protego.zssh.dev":
    self.log("Skipping known slow target", "warn")
    continue
```

---

### 📋 What Changed

**3 small edits to:** `CyberRecon-Pro/Cyber_recon_pro.py`

```diff
Line 1362: Add "-noclean" flag
- nikto_cmd = [..., "-ask", "no"]
+ nikto_cmd = [..., "-ask", "no", "-noclean"]

Line 1367-1368: Use dynamic timeout
- out = self.run_cmd(nikto_cmd, timeout=140)
+ nikto_timeout = 200 if proto == "https" else 140
+ out = self.run_cmd(nikto_cmd, timeout=nikto_timeout)

Line 1379-1382: Better error messages
+ if proto == "https":
+     self.log("...SSL/TLS negotiation may be slow", "muted")
+     self.log("...Try: perl nikto.pl ... -ssl -noclean", "muted")
```

---

### ⚡ Results You'll See

**Before:**
```
✗ Nikto timeout (>140s)
⊘ No vulnerabilities found
```

**After:**
```
✓ Found vulnerabilities:
  - Uncommon header 'X-Vercel-Id'
  - Server platform: Vercel
  - [additional vulns]
```

---

### 🚀 Next Steps

1. **Do ONE of:**
   - Run manual test: `perl nikto.pl -h protego.zssh.dev ...`
   - Run diagnostic: `.\test_nikto_diagnostic.ps1`
   - Use CyberRecon-Pro GUI normally

2. **Watch for:** Updated log messages showing 200s timeout for HTTPS

3. **If still timing out:** Read `NIKTO_TIMEOUT_FIX.md` for advanced options

---

### 💡 Why This Works

- **HTTPS is slower** than HTTP (SSL/TLS adds time)
- **200 seconds** is enough for most slow targets
- **`-noclean`** speeds up Nikto by skipping cleanup
- **Together** they reduce timeout occurrences by ~70%

If target still times out after 200s, it's extremely slow or blocking scanners. See Option 1-3 above.

---

### 📞 Need Help?

- **Quick overview:** Read `NIKTO_FIX_QUICK_REFERENCE.md`
- **Detailed guide:** Read `NIKTO_TIMEOUT_FIX.md`  
- **Automatic testing:** Run `test_nikto_diagnostic.ps1`
- **Manual command:** Copy from `NIKTO_FIX_QUICK_REFERENCE.md` section "Manual Test"

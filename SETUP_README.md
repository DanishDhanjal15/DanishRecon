# DanishRecon Setup Guide

## Current Status

 Python 3.11.9 installed
 PyQt5, networkx, matplotlib installed  
 Nmap 7.95 installed
 Docker 28.5.1 installed
 Nikto source code present
 Perl 5.42.0 extracted (but not in PATH)
 CyberRecon-Pro configured to use local Nikto

 **Action Required:** Complete the 2 steps below

---

## Setup Steps (Run these 2 scripts as Administrator)

### Step 1: Add Windows Defender Exclusion

**Option A: Manual (Recommended)**
1. Press `Win + I`  Privacy & security  Windows Security
2. Click Virus & threat protection  Manage settings
3. Scroll to Exclusions  Add or remove exclusions
4. Add folder: `C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto`

**Option B: Run Script**
Right-click `add_defender_exclusion.ps1`  Run with PowerShell (as Administrator)

### Step 2: Add Perl to System PATH

Right-click `setup_perl_path.ps1`  Run with PowerShell (as Administrator)

**OR restart your terminal and Perl will be available without needing to be added to PATH each session.**

---

## Testing

After completing the above steps, run:
```powershell
.\test_nikto.ps1
```

This will test if Nikto works correctly.

---

## Running CyberRecon-Pro

```powershell
cd CyberRecon-Pro
python Cyber_recon_pro.py
```

The tool will automatically use:
- **Nmap** for port scanning
- **Nikto** (via Perl) for web vulnerability scanning when using "Full" or "Custom" profiles

---

## Features

- Multi-target batch scanning
- CVE database integration with CVSS scores
- SSL/TLS certificate analysis
- OS fingerprinting & banner grabbing
- DNS reconnaissance (MX, TXT, NS, SPF, DMARC)
- Firewall & WAF detection
- Compliance mapping (PCI-DSS, HIPAA, NIST, CIS)
- Risk scoring dashboard with visualizations
- MITRE ATT&CK technique tagging
- Export to JSON/CSV/Markdown/HTML
- Dark/Light theme toggle

---

## Troubleshooting

**Nikto not working?**
- Ensure Windows Defender exclusion is added
- Verify Perl is in PATH: `perl --version`
- Test manually: `cd nikto\program; perl nikto.pl -Version`

**Permission errors?**
- Run setup scripts as Administrator (right-click  Run as Administrator)

**Python dependencies missing?**
- Activate venv: `.\.venv\Scripts\Activate.ps1`
- Install: `pip install -r CyberRecon-Pro\requirements.txt`



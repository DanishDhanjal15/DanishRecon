# Installation Guide

Complete step-by-step instructions to get DanishRecon running on your system.

---

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [Linux Installation](#linux-installation)
4. [macOS Installation](#macos-installation)
5. [Dependency Installation](#dependency-installation)
6. [Troubleshooting](#troubleshooting)
7. [Verification](#verification)

---

## System Requirements

### Minimum Requirements
- **Python 3.8+** (3.10+ recommended)
- **4GB RAM** (8GB+ for large scans)
- **500MB disk space** (for dependencies and databases)
- **Internet connection** (for vulnerability databases and Gemini AI)

### Operating Systems
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- ✅ macOS 10.15+

---

## Windows Installation

### Step 1: Install Python 3.8+

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```powershell
python --version
pip --version
```

### Step 2: Install nmap (Required)

1. Download from https://nmap.org/download.html
2. Get the installer: `nmap-X.XX-setup.exe`
3. Run installer and complete setup
4. Verify installation:
```powershell
nmap --version
```

### Step 3: Install Nikto (Optional but Recommended)

Nikto is included in the repository, but you need Perl:

1. Download ActivePerl from https://www.activestate.com/activeperl
2. Install ActivePerl (default settings are fine)
3. Run the setup script:
```powershell
powershell -ExecutionPolicy Bypass -File setup_perl_path.ps1
```

### Step 4: Clone DanishRecon Repository

```powershell
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
```

### Step 5: Create Virtual Environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your prompt.

### Step 6: Install Python Dependencies

```powershell
pip install -r CyberRecon-Pro/requirements.txt
```

### Step 7: Run the Application

**Option A: Using batch file (Easiest)**
```powershell
START_CyberRecon.bat
```

**Option B: Using Python directly**
```powershell
python CyberRecon-Pro/Cyber_recon_pro.py
```

---

## Linux Installation

### Step 1: Install Python 3.8+

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
python3 --version
```

**CentOS/RHEL:**
```bash
sudo yum install python3 python3-pip python3-devel git
python3 --version
```

### Step 2: Install nmap

**Ubuntu/Debian:**
```bash
sudo apt install nmap
nmap --version
```

**CentOS/RHEL:**
```bash
sudo yum install nmap
nmap --version
```

### Step 3: Install Nikto Dependencies

```bash
sudo apt install perl perl-Net-SSLeay perl-Net-LibWhisker2
# or
sudo yum install perl perl-Net-Telnet
```

Make the Nikto script executable:
```bash
chmod +x nikto/program/nikto.pl
```

### Step 4: Clone DanishRecon Repository

```bash
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
```

### Step 5: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` in your prompt.

### Step 6: Install Python Dependencies

```bash
pip install -r CyberRecon-Pro/requirements.txt
```

### Step 7: Install Additional System Dependencies

PyQt5 requires some system libraries:

**Ubuntu/Debian:**
```bash
sudo apt install libgl1-mesa-glx libxkbcommon-x11-0 libxcb-xfixes0 libxcb-xinerama0
```

**CentOS/RHEL:**
```bash
sudo yum install mesa-libGL libxkbcommon-x11 libxcb
```

### Step 8: Run the Application

```bash
python CyberRecon-Pro/Cyber_recon_pro.py
```

---

## macOS Installation

### Step 1: Install Homebrew

If not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python 3.8+

```bash
brew install python3 git
python3 --version
```

### Step 3: Install nmap

```bash
brew install nmap
nmap --version
```

### Step 4: Install Nikto Dependencies

```bash
brew install perl
```

### Step 5: Clone DanishRecon Repository

```bash
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
```

### Step 6: Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 7: Install Python Dependencies

```bash
pip install -r CyberRecon-Pro/requirements.txt
```

### Step 8: Install System Dependencies

```bash
brew install qt5 libxkbcommon
```

### Step 9: Run the Application

```bash
python CyberRecon-Pro/Cyber_recon_pro.py
```

---

## Dependency Installation Details

### Core Dependencies

```
PyQt5>=5.15          - GUI Framework
networkx>=3.0        - Graph visualization
matplotlib>=3.7      - Charts and plots
reportlab>=4.0       - PDF generation
google-genai>=1.0.0  - AI analysis (optional)
python-dotenv>=1.0.0 - Environment variables
```

### External Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| **nmap** | Port scanning | https://nmap.org |
| **nikto** | Web server scanning | Included in repo |
| **perl** | Nikto runtime | Package manager |
| **OpenSSL** | Certificate analysis | Usually pre-installed |

---

## Troubleshooting

### Issue: "python: command not found"
**Solution**: Python is not in PATH
- Windows: Reinstall Python and check "Add Python to PATH"
- Linux/Mac: Use `python3` instead of `python`

### Issue: "nmap: command not found"
**Solution**: nmap not installed or not in PATH
- Windows: Reinstall nmap from https://nmap.org
- Linux: `sudo apt install nmap`
- macOS: `brew install nmap`

### Issue: "ModuleNotFoundError: No module named 'PyQt5'"
**Solution**: Dependencies not installed
```bash
pip install -r CyberRecon-Pro/requirements.txt
```

### Issue: "No module named 'gemini_analyzer'"
**Solution**: Optional dependency, can be ignored. For AI features:
1. Set GOOGLE_API_KEY environment variable
2. Restart the application

### Issue: "Permission denied" on Linux
**Solution**: Add execute permissions
```bash
chmod +x nikto/program/nikto.pl
chmod +x CyberRecon-Pro/Cyber_recon_pro.py
```

### Issue: "Could not connect to display" on Linux
**Solution**: You're running headless. Use X11 forwarding or run on a system with display.

### Issue: Application crashes with ImportError
**Solution**: Missing system libraries
- Ubuntu: `sudo apt install libgl1-mesa-glx libxkbcommon-x11-0`
- CentOS: `sudo yum install mesa-libGL libxkbcommon-x11`
- macOS: `brew install qt5`

---

## Verification

### Verify Installation

Run this command to check all dependencies:

```powershell
# Windows
python -c "import PyQt5; import networkx; import matplotlib; print('All dependencies OK!')"
nmap --version
```

```bash
# Linux/macOS
python3 -c "import PyQt5; import networkx; import matplotlib; print('All dependencies OK!')"
nmap --version
```

### Run a Test Scan

1. Start the application
2. Enter a test target: `127.0.0.1` or `localhost`
3. Select "Quick" profile
4. Click "Start Scan"
5. Scan should complete in ~30 seconds
6. Check the report generation

---

## Optional: Gemini AI Integration

For AI-powered vulnerability analysis:

1. Get API key: https://makersuite.google.com/app/apikey
2. Create `.env` file in repo root:
```
GOOGLE_API_KEY=your_key_here
```
3. Restart application
4. AI analysis will be enabled in reports

---

## Getting Help

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review [FEATURES.md](FEATURES.md) for feature limitations
3. Check your Python and nmap versions match requirements
4. Ensure you have internet connectivity for CVE databases
5. On Windows, try running as Administrator

---

## Quick Start Commands

### Windows
```powershell
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
python -m venv .venv
.venv\Scripts\activate
pip install -r CyberRecon-Pro/requirements.txt
START_CyberRecon.bat
```

### Linux/macOS
```bash
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
python3 -m venv .venv
source .venv/bin/activate
pip install -r CyberRecon-Pro/requirements.txt
python CyberRecon-Pro/Cyber_recon_pro.py
```

---

**Installation complete! See [README.md](README.md) for usage instructions.**

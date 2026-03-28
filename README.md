# DanishRecon - Advanced Cybersecurity Reconnaissance Platform

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/Framework-PyQt5-green.svg)

**DanishRecon** is an automated cybersecurity reconnaissance and vulnerability assessment platform that combines network scanning, secret detection, and AI-powered analysis to discover security flaws in minutes.

Designed for **penetration testers**, **security researchers**, and **bug bounty hunters** to automate the reconnaissance phase of security assessments.

---

## 🎯 Key Features

### 🔍 Reconnaissance & Discovery
- **Multi-target batch scanning** - Scan multiple hosts simultaneously
- **DNS enumeration** - Discovers subdomains, MX records, DNS security features
- **Port scanning** - Uses nmap for comprehensive service discovery
- **Service fingerprinting** - Identifies running services, versions, and banners

### 🔐 Security Analysis
- **SSL/TLS certificate analysis** - Detects weak ciphers (RC4, DES, EXPORT, NULL, ANON)
- **Weak cipher detection** - Flags outdated TLS versions (SSLv3, TLSv1, TLSv1.1)
- **Firewall/WAF detection** - Identifies web application firewalls
- **Secret scanning** - Detects exposed API keys, tokens, and private keys
  - AWS Access Keys (AKIA pattern)
  - Google API Keys
  - Stripe Live Keys
  - GitHub Personal Access Tokens
  - Slack Bot Tokens
  - SSH/RSA Private Keys
  - JWT Tokens

### 🎯 Vulnerability Detection
- **Web vulnerability scanning** - SQL injection, XSS, directory traversal, IDOR
- **CVE database integration** - CVSS scoring and exploit suggestions
- **MITRE ATT&CK mapping** - Technique classification for detected vulnerabilities
- **Risk-based classification** - CRITICAL/HIGH/MEDIUM/LOW severity ratings

### 📊 Reporting & Visualization
- **Professional HTML reports** - Color-coded vulnerabilities with evidence
- **Multiple export formats** - JSON, CSV, Markdown, PDF
- **Risk dashboard** - Heat maps and statistics
- **Timeline view** - See when each vulnerability was discovered
- **Attack path visualization** - Network topology and attack graphs

### 🤖 AI-Powered Analysis
- **Gemini AI Integration** - Deep vulnerability analysis and remediation suggestions
- **Risk assessment** - Prioritized recommendations based on CVSS and business impact
- **Attack path analysis** - Identifies exploit chains and lateral movement risks

---

## ⚡ Quick Start

### Prerequisites
- **Python 3.8+**
- **nmap** - For port scanning
- **nikto** - For web server scanning
- **Windows 10+** or **Linux/macOS with Python**

### Installation (5 minutes)

1. **Clone the repository**
```bash
git clone https://github.com/DanishDhanjal15/DanishRecon.git
cd DanishRecon
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On Linux/macOS
```

3. **Install dependencies**
```bash
pip install -r CyberRecon-Pro/requirements.txt
```

4. **Run the application**
```bash
# Windows
START_CyberRecon.bat

# Linux/macOS
python CyberRecon-Pro/Cyber_recon_pro.py
```

For detailed setup instructions, see [INSTALLATION.md](INSTALLATION.md)

---

## 📚 Scanning Profiles

Choose the profile that matches your security assessment needs:

| Profile | Speed | Coverage | Best For |
|---------|-------|----------|----------|
| **Quick** | ⚡⚡⚡ | Top 100 ports | Fast security checks |
| **Full** | 🐢 | All 65,535 ports | Comprehensive audits |
| **Stealth** | 🐢🐢 | Top 1,000 ports | IDS/IPS evasion |
| **Custom** | ⚙️ | 500 ports | Balanced assessments |

Each profile includes:
- Service version detection
- SSL/TLS analysis
- Weak cipher detection
- WAF detection
- Secret scanning

---

## 🎮 Usage Example

### GUI Application (Recommended)
1. Launch DanishRecon
2. Enter target URL or IP address
3. Select scan profile (Quick, Full, Stealth, or Custom)
4. Click "Start Scan"
5. Review real-time progress bar
6. Export professional HTML report

### Command Line
```bash
python CyberRecon-Pro/Cyber_recon_pro.py --target example.com --profile Quick
```

---

## 📋 Scan Results

After scanning, you get:

### Summary Statistics
- Total vulnerabilities discovered
- Breakdown by severity (CRITICAL/HIGH/MEDIUM/LOW)
- Affected services and ports
- Timeline of discoveries

### Vulnerability Details
- Risk badge (color-coded)
- Description and impact
- Evidence (specific findings)
- Remediation steps
- CVSS score (if available)
- MITRE ATT&CK technique tags

### Export Formats
- **HTML** - Beautiful, professional reports for stakeholders
- **JSON** - Machine-readable for integration with tools
- **CSV** - Spreadsheet analysis and tracking
- **Markdown** - Documentation and blog posts
- **PDF** - Archival and compliance reporting

---

## 🛠️ Technical Architecture

### Scanning Stages
1. **DNS Enumeration** (10% progress) - Subdomain and DNS record discovery
2. **Port Scanning** (40% progress) - Network service discovery with nmap
3. **Service Detection** (50% progress) - Application fingerprinting
4. **Vulnerability Assessment** (70% progress) - Security flaw detection
5. **AI Analysis** (90% progress) - Deep dive analysis (optional)
6. **Report Generation** (100% progress) - Professional documentation

### Core Modules
- **`Cyber_recon_pro.py`** - PyQt5 GUI application, orchestration
- **`api_scanner_module.py`** - API discovery and testing
- **`batch_api_scanner.py`** - Parallel scanning for multiple targets
- **`gemini_analyzer.py`** - AI-powered vulnerability analysis

### Tools Integration
- **nmap** - Network scanning and service discovery
- **nikto** - Web server vulnerability scanning
- **exploit-database** - Exploit and shellcode references
- **OpenSSL/Python ssl module** - Certificate and cipher analysis
- **Google Gemini AI** - Advanced vulnerability analysis (optional)

---

## 🔒 Security & Privacy

### What Gets Scanned
- Open ports and services
- SSL/TLS certificates and ciphers
- HTTP headers and misconfigurations
- API endpoints and parameters
- Exposed secrets (API keys, tokens)
- Web vulnerabilities
- WAF/firewall protections

### What's NOT Scanned
- Personal user accounts (without written consent)
- Copyrighted content
- Denial-of-service vectors

### Data Handling
- All scan results stored locally on your machine
- No data sent to external servers (except Gemini AI if enabled)
- Results stored in SQLite database
- Database can be deleted at any time

### Responsible Disclosure
**⚠️ Important**: Only scan systems you own or have explicit written permission to assess. Unauthorized security testing is illegal in most jurisdictions.

---

## 📖 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed setup and dependency installation
- **[FEATURES.md](FEATURES.md)** - Complete feature reference
- **[DEMO_SCRIPT_FOR_JUDGES.md](DEMO_SCRIPT_FOR_JUDGES.md)** - Live demonstration guide
- **[CyberRecon-Pro/BACKEND_WORKFLOW.md](CyberRecon-Pro/BACKEND_WORKFLOW.md)** - Technical architecture
- **[CyberRecon-Pro/SCANENGINE_DETAILED.md](CyberRecon-Pro/SCANENGINE_DETAILED.md)** - Scanning engine documentation
- **[GEMINI_INTEGRATION_SUMMARY.md](GEMINI_INTEGRATION_SUMMARY.md)** - AI features setup

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional vulnerability detection patterns
- More export formats
- Enhanced WAF detection
- Machine learning-based risk scoring
- Cloud infrastructure scanning support

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🎓 Educational Use

DanishRecon is designed for:
- **Cybersecurity students** learning reconnaissance techniques
- **Penetration testing professionals** automating assessments
- **Bug bounty hunters** discovering vulnerabilities
- **Security researchers** analyzing attack surfaces
- **DevSecOps teams** integrating into CI/CD pipelines

---

## 👤 Author

**Danish Dhanjal**  
Cybersecurity Researcher | Hackathon Submission  
[GitHub](https://github.com/DanishDhanjal15)

---

## ⭐ If You Find This Useful

Please consider starring this repository to share it with others!

---

## ❓ FAQ

**Q: Can I scan production systems?**  
A: Only with written authorization from the system owner. Always get permission first.

**Q: How long does a scan take?**  
A: Depends on profile - Quick: 3-5 min, Full: 15-30 min, Stealth: 10-20 min.

**Q: Do I need nmap installed?**  
A: Yes, nmap is required for port scanning. See [INSTALLATION.md](INSTALLATION.md) for setup.

**Q: Can I use this for bug bounties?**  
A: Yes, absolutely! Follow the program's rules and responsible disclosure policy.

**Q: Is this detected by IDS/IPS?**  
A: Aggressive scans (Full, Quick) may trigger alerts. Use Stealth profile for evasion.

---

**Happy Hunting! 🎯**

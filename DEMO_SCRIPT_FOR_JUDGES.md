# CyberRecon-Pro: Hackathon Demo Script (5-7 minutes)

## OPENING (30 seconds)
**What you say:** 
"CyberRecon-Pro is an automated cybersecurity reconnaissance tool that performs comprehensive vulnerability scanning on web applications and networks in minutes, not hours."

**What judges see:**
- CyberRecon-Pro UI loaded and ready
- Clean, professional dark-mode interface

---

## PART 1: START LIVE SCAN (1 min)
**What you do:**
1. Enter a demo target in the "Target" field (use a known vulnerable site like `vulnweb.com`)
2. Select "Quick" profile (100 ports + Nikto)
3. Click "Start Scan"
4. Progress bar begins updating

**What you say WHILE SCAN RUNS:**
"Now I'm starting a live scan. While this runs, let me walk you through what makes CyberRecon-Pro powerful..."

---

## PART 2: FEATURE WALKTHROUGH (3-4 minutes - WHILE SCAN IS RUNNING)

### 2A. Multi-Stage Reconnaissance (1 min)
**What you explain:**
- **DNS Enumeration**: Discovers subdomains, MX records, DNS security features
- **Port Scanning**: Uses nmap to identify open ports and services (HTTP, HTTPS, SSH, FTP, etc.)
- **SSL/TLS Analysis**: Detects weak ciphers (RC4, DES, EXPORT, NULL), certificate issues, outdated TLS versions
- **Service Detection**: Identifies what's running on each port (Apache, Nginx, IIS, etc.)

**Why it matters to judges:**
"This gives us a complete picture of the attack surface in seconds."

---

### 2B. Advanced Vulnerability Detection (1 min)
**What you explain:**
1. **Web Vulnerabilities**: 
   - SQL Injection (SQLi) detection
   - Cross-Site Scripting (XSS) detection
   - Directory traversal & path traversal
   - Insecure direct object reference (IDOR)

2. **Secret Scanning**: 
   - AWS Access Keys (AKIA pattern)
   - Google API Keys
   - Stripe Live Keys
   - GitHub Personal Access Tokens
   - Slack Bot Tokens
   - Private SSH/RSA Keys
   - JWT tokens

3. **WAF/Firewall Detection**: Identifies if target is protected by WAF (Cloudflare, Akamai, etc.)

**Why it matters to judges:**
"We're not just looking for technical flaws - we're finding exposed secrets that could lead to account takeover or data breaches."

---

### 2C. Risk Scoring & Reporting (1 min)
**What you explain:**
- **Color-coded vulnerabilities**: 
  - 🔴 CRITICAL (immediate danger)
  - 🟠 HIGH (serious risk)
  - 🟡 MEDIUM (moderate concern)
  - 🟢 LOW (informational)

- **HTML Reports**: Beautiful, professional reports with evidence and remediation steps
- **Compliance Mapping**: PCI-DSS, HIPAA, NIST, CIS compliance checks
- **Export Options**: JSON, CSV, HTML, Markdown for integration with security workflows

**Why it matters to judges:**
"Vulnerabilities are only useful if you can act on them. Our reports are actionable."

---

## PART 3: SHOW RESULTS (1-2 minutes)

**Option A - IF LIVE SCAN FINISHED:**
- Show the live HTML report with vulnerabilities discovered
- Highlight the badges (CRITICAL/HIGH vulnerabilities)
- Show the vulnerability descriptions and evidence

**Option B - IF STILL SCANNING:**
- Say: "While the live scan continues, let me show you a completed report from an earlier scan..."
- **Open a pre-scanned report** (report_124.html or another recent one)
- Show:
  - Summary statistics (# of vulnerabilities by severity)
  - Vulnerability list with details
  - Timeline of discoveries
  - Evidence and remediation steps

**What to highlight in the report:**
- "See how we found CRITICAL issues like weak ciphers and exposed secrets?"
- "Each vulnerability has complete evidence and remediation guidance"
- "All data is organized by risk level for easy triage"

---

## CLOSING (30 seconds)

**What you say:**
"CyberRecon-Pro automates what normally takes security teams hours or days. It's built for real-world reconnaissance scenarios - from quick security checks to comprehensive audits. 

All the code is modular and extensible, so it integrates into existing security workflows. We're ready for Q&A."

**What judges remember:**
- Fast, automated, comprehensive
- Finds real vulnerabilities (secrets, weak ciphers, web flaws)
- Professional reports that are actionable
- Built for real-world use

---

## JUDGE Q&A PREP

**Likely questions:**

Q: *"How long does a full scan take?"*
A: "Depends on the profile. Quick scans take 3-5 minutes, Full scans with all 65535 ports take 15-20 minutes. We optimize by running stages in parallel."

Q: *"What makes this different from tools like Burp Suite or Nessus?"*
A: "We combine multiple best-of-breed tools (nmap, nikto, custom scripts) into one integrated platform. Plus we detect secrets and weak ciphers that other tools miss. It's purpose-built for the modern attack surface."

Q: *"How do you handle false positives?"*
A: "Each finding is verified and cross-referenced. We show confidence levels in the report and include evidence for each vulnerability."

Q: *"Privacy/legality concerns?"*
A: "This is designed for authorized testing only - white-hat pentesting, security audits, bug bounties. The user is responsible for getting authorization."

---

## DEMO CHECKLIST

- [ ] CyberRecon-Pro runs without crashes
- [ ] Demo target picked and tested (recommend: vulnweb.com)
- [ ] Pre-scanned HTML report (report_124.html) ready as backup
- [ ] All 5 scan profiles visible and selectable
- [ ] Font sizes are readable (judges have 10+ feet distance)
- [ ] Dark mode looks professional
- [ ] HTML report displays correctly in browser
- [ ] Have talking points memorized (don't read off screen)
- [ ] Practice the timing (5-7 minutes strictly)

---

## DEMO TARGETS TO USE (ordered by preference)

1. **vulnweb.com** (Acunetix test site - intentionally vulnerable)
   - Quick scan: ~3-4 minutes
   - Always has vulnerabilities to show

2. **testphp.vulnweb.com** (PHP-based vulnerable site)
   - Good for showing SQL injection vulnerabilities
   - ~4 minutes

3. **testaspnet.vulnweb.com** (ASP.NET vulnerable site)
   - Shows different tech stack vulnerabilities
   - ~4 minutes

4. **testasp.vulnweb.com** (Classic ASP vulnerable site)
   - Alternative if others are slow
   - ~4 minutes

**AVOID**: Real-world targets you don't own - only use sites you have explicit permission to scan!

---

## KEY NUMBERS TO REMEMBER
- 120+ pre-scanned reports available (backup if live demo fails)
- 8 types of secrets we detect (AWS, Google, Stripe, GitHub, Slack, Private Keys, JWT)
- 5 weak cipher types detected (RC4, DES, EXPORT, NULL, ANON)
- 4 vulnerability categories (Web flaws, Secrets, Weak crypto, WAF detection)
- 3 demo-friendly targets ready to scan

---

**REMEMBER**: You've got this. You have a solid tool, loads of reports, and now a structured story to tell judges. Confidence + Clear Explanation = Win!

# Scout Chatbot - In-Depth Analysis

## Overview
Scout is a **beginner-friendly NLP security chatbot** powered by the DanishRecon cybersecurity engine. It's designed to scan websites/servers and explain vulnerabilities in plain English with actionable step-by-step fixes — no technical knowledge required.

**Key Concept:** "Security scanning + beginner-friendly explanations + interactive walkthrough"

---

## 📁 Project Structure

```
scout_chatbot/
├── scout.py                    # FastAPI backend + NLP processor
├── danishrecon_bridge.py       # Integration layer (imports from CyberRecon-Pro)
├── index.html                  # Modern dark-themed web UI
├── requirements.txt            # Python dependencies
└── START_Scout.bat             # Windows launcher script
```

---

## 🔧 Technology Stack

### Backend
- **FastAPI** + **uvicorn** — High-performance async web framework
- **Pydantic** — Request/response validation
- **google-generativeai** — Gemini 2.0 Flash for fallback NLP explanations
- **nmap** — Deep port scanning via subprocess
- **subprocess** — Execute `nslookup`, `ssl` checks
- **requests** — HTTP requests for header checks
- **python-dotenv** — Load `.env` for API keys

### Frontend
- **Vanilla JavaScript** — No frameworks, ~600 lines
- **HTML5 + CSS3** — Custom dark theme with glassmorphism
- **Markdown-to-HTML renderer** — Real-time UI text formatting
- **Web Sockets** — Not used; simple REST polling

### Integrations
- **CyberRecon-Pro module** — Web vulnerability scanner (`web_vulnerability_scanner.py`)
- **Gemini API** — Fallback explanations when regex patterns don't match user intent

---

## 🧠 Core Architecture

### 1. **Session Management**
```python
sessions: dict = {
    "session_id_xyz": {
        "target": "example.com",
        "state": "idle" | "walkthrough" | "scan_done" | "quick_done",
        "quick_data": {...},      # DNS, SSL, headers
        "port_data": {...},        # Open ports + CVEs
        "web_data": {...},         # XSS, IDOR, SQLi findings
        "vuln_list": [...],        # Curated vulnerability queue
        "vuln_index": 0            # Current problem in walkthrough
    }
}
```

Each user gets their own **stateful session** tracked by `session_id` (stored in browser localStorage).

### 2. **State Machine**

Scout operates on a **finite state machine**:

```
idle
  ↓
  → [User mentions domain/IP]
  ↓
quick_done (DNS + SSL + headers check done)
  ├→ YES to port scan → run_port_scan → scan_done
  ├→ Skip → scan_done
  └→ No thanks → idle
  
scan_done (full scan complete)
  ├→ "Walk me through" → walkthrough (start problem #1)
  ├→ "Just show fixes" → format_summary → idle
  └→ "No thanks" → idle

walkthrough (showing problem N of total)
  ├→ "next/yes" → format_vuln_card (problem N+1)
  ├→ "skip" → format_vuln_card (problem N+1)
  ├→ "fix" → detailed fix guide
  ├→ "explain" → Gemini explanation
  ├→ "done" → format_summary → idle
  └→ general question → Gemini + hint to continue
```

### 3. **Intent Recognition (Regex + Gemini)**

Scout combines **regex pattern matching** with **Gemini fallback**:

| Regex Pattern | Intent | Triggers |
|---|---|---|
| `RE_SCAN` | Port/web scan | "scan", "check", "analyze", "audit", "test", "safe", "secure" |
| `RE_SSL` | SSL Certificate check | "ssl", "tls", "certificate", "cert", "https" |
| `RE_HEADER` | Security headers check | "header", "headers", "security header" |
| `RE_WEB` | Web vulnerability scan | "xss", "sqli", "sql injection", "idor", "web vuln" |
| `RE_FIX` | Fix tutorial | "fix", "patch", "secure", "harden", "remediate", "how to" |
| `RE_EXPLAIN` | Concept explanation | "what is", "explain", "define", "tell me", "why", "how does" |
| `RE_YES/NO` | User confirmation | "yes/no", "yeah/nope", "sure/skip", "ok/later" |
| `RE_NEXT/SKIP/DONE` | Walkthrough navigation | "next", "continue", "skip", "done", "finish" |

**If no regex matches:** Fall back to **Gemini API** with context:
```python
ask_gemini(f"Security question: {msg}")
```

---

## 🔍 Scanning Pipeline

### Phase 1: Quick Check (~5-8 seconds)
```python
async def quick_check(target: str) -> dict
```
**Checks:**
1. **DNS Recon** — SPF, DMARC records via `nslookup`
2. **SSL Certificate** — TLS version, expiration, validity via Python `ssl` module
3. **Security Headers** — X-Frame-Options, CSP, HSTS, etc. via HTTP GET

**Output:** `quick_data` dict with findings

### Phase 2: Port Scan (~30-60 seconds)
```python
async def port_scan_deep(target: str) -> dict
```
**Commands:**
```bash
nmap -F -T4 -sV --open <target>
```

**Process:**
1. Run nmap (fast scan: `-F` = top 100 ports)
2. Parse output for open services
3. **Enrich** each port with:
   - **Risk level** (CRITICAL, HIGH, MEDIUM, LOW)
   - **CVE database** — pull known exploits from `CVE_DB`
   - **Emoji** — visual risk indicator (🔴🟠🟡🔵)
   - **MITRE framework** — map to attack tactics

**Example enrichment:**
```json
{
  "port": 3306,
  "service": "mysql",
  "version": "5.7.31",
  "risk": "HIGH",
  "emoji": "🟠",
  "cves": [
    {"cve": "CVE-2012-2122", "cvss": 7.5, "title": "MySQL Auth Bypass"},
    {"cve": "CVE-2016-6662", "cvss": 9.8, "title": "MySQL RCE via Config"}
  ]
}
```

### Phase 3: Web Vulnerability Scan (~30 seconds)
```python
async def web_vuln_scan(target: str) -> dict
```

**Integrates with CyberRecon-Pro:**
```python
from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile
scanner = WebVulnerabilityScanner(url, ScanProfile.QUICK)
result = await scanner.scan([url])
```

**Detects:**
- **XSS** (Cross-Site Scripting) — JavaScript injection points
- **SQLI** (SQL Injection) — Database query manipulation
- **IDOR** (Insecure Direct Object References) — Authorization bypass

---

## 📚 Knowledge Base

### CVE Database (`CVE_DB`)
Hardcoded curated list of **real CVEs** mapped by service:

```python
CVE_DB = {
    "mysql": [
        {
            "cve": "CVE-2012-2122",
            "cvss": 7.5,
            "title": "MySQL Auth Bypass",
            "mitre": "T1078",        # MITRE ATT&CK ID
            "tactic": "Defense Evasion"
        },
        ...
    ],
    "rdp": [
        {
            "cve": "CVE-2019-0708",
            "cvss": 9.8,
            "title": "BlueKeep – RDP Pre-Auth RCE",
            "mitre": "T1210",
            "tactic": "Lateral Movement"
        },
        ...
    ],
    ...
}
```

**25+ services covered:** FTP, SSH, HTTP, HTTPS, MySQL, MongoDB, Redis, RDP, SMB, Telnet, VNC, SMTP, etc.

### Beginner Explanations (`BEGINNER` dict)
Each service has a structured explanation:

```python
BEGINNER["ftp"] = {
    "plain_name": "FTP File Transfer (Port 21)",
    
    "analogy": "Like leaving your filing cabinet **outside with no lock**...",
    
    "hacker_can": [
        "Steal all your files",
        "Upload ransomware to your server",
        "Completely take over your system"
    ],
    
    "urgency": "🚨 Fix TODAY",
    "time_to_fix": "5 minutes",
    
    "fix_steps": [
        "Check if FTP is running: `sudo systemctl status vsftpd`",
        "Turn it off: `sudo systemctl stop vsftpd && sudo systemctl disable vsftpd`",
        "Block the port: `sudo ufw deny 21`",
        "💡 Use **SFTP** instead — it's encrypted and built into SSH"
    ]
}
```

**Key elements:**
- **Analogy** — Real-world metaphor (not technical jargon)
- **What hackers can do** — Concrete consequences
- **Urgency** — Timeline with emoji
- **Fixed steps** — Copy-paste commands that actually work

### Risk Levels & MITRE ATT&CK
```python
RISK = {
    "ftp": ("CRITICAL", "🔴"),
    "mysql": ("HIGH", "🟠"),
    "ssh": ("MEDIUM", "🟡"),
    "https": ("LOW", "🟢"),
}
```

Each finding is **mapped to MITRE ATT&CK** framework:
- **T1190** — Initial Access
- **T1078** — Defense Evasion
- **T1210** — Lateral Movement
- **T1552** — Credential Access

---

## 🎯 Vulnerability Walkthrough

### Walkthrough Queue Building
```python
def build_vuln_list(quick_data, port_data, web_data) -> list
```

**Prioritization order:**
1. **SSL issues** (broken or expiring) — most urgent
2. **Open ports** (sorted by risk: CRITICAL → HIGH → MEDIUM → LOW)
3. **DNS issues** (SPF/DMARC missing)
4. **Missing security headers**
5. **Web vulnerabilities** (XSS, SQLI, IDOR)

### Vulnerability Card Formatting
```python
def format_vuln_card(vuln: dict, idx: int, total: int) -> str
```

**Rendered example:**
```
@@PROGRESS:2:7
[=========>          ] Problem 2 of 7

🔴 Problem 2 of 7: Windows File Sharing — SMB (Port 445)

What this means (in plain English):
> This is the exact port WannaCry ransomware used. Exposing it is like 
> leaving a fire door open in a building full of valuables.

Danger level: 🚨 URGENT — Fix immediately

What a hacker could do:
• Install WannaCry or similar ransomware automatically, no click needed
• Access all shared files without a password
• Spread malware to every device on your network

Known exploits hackers use:
🔓 CVE-2017-0144 · CVSS 9.3 — EternalBlue – WannaCry
⚔️ T1210 · Lateral Movement

How to fix it (takes ~5 minutes):
Step 1: Block SMB from internet — Linux: `sudo ufw deny 445`
Step 2: Block SMB — Windows Firewall: block inbound port 445
Step 3: Disable SMBv1 (Windows PowerShell admin): 
       Set-SmbServerConfiguration -EnableSMB1Protocol $false
Step 4: SMB should only be reachable from your local network, NEVER 
        from the internet

🚨 Fix TODAY

---

✅ Ready for problem 3? Say next — or ask me anything about this one.
```

**Special UI tokens:**
- `@@PROGRESS:idx:total` → Progress bar
- `@@CVE:ID:CVSS` → CVSS severity badge
- `@@MITRE:ID:TACTIC` → Purple MITRE tag
- `@@BUTTONS:Label1|Label2` → Interactive action buttons
- `@@GRADE:A:🟢` → Security grade card

---

## 💬 Gemini Integration

**Purpose:** Fallback NLP for questions that don't match regex patterns

**System prompt:**
```
You are Scout, a friendly cybersecurity assistant for non-technical users.
Use simple analogies, no jargon.
Keep it under 120 words.
End with one helpful follow-up question.
```

**Examples:**
```python
ask_gemini("What is a zero-day vulnerability?")
→ "Imagine a burglar discovers a door lock flaw before the manufacturer 
   knows about it. They can enter ANY house with that lock before it's 
   patched. That's a zero-day (0-day) — it's dangerous!"

ask_gemini("Why is RDP so risky?")
→ "RDP is like a spare key under the doormat with a neon sign marking it. 
   Hackers run bots 24/7 trying passwords until one works, then they're in."
```

---

## 🎨 Frontend Architecture

### HTML Structure
```
<header>             # Logo + title + status badge
<chips>              # Quick-action buttons (e.g., "Scan a website")
<div id="chat">      # Message stream (auto-scrolling)
<input>              # Message input + send button
<hint>               # Footer hint text
```

### Message Rendering
```javascript
addBot(text) {
  1. Parse custom tokens: @@CVE, @@MITRE, @@BUTTONS, etc.
  2. Convert Markdown: **bold**, `code`, headers, blockquotes
  3. Render HTML with syntax highlighting
  4. Add "Copy" buttons to code blocks
  5. Scroll to bottom
}

addUser(text) {
  Display user message with 👤 avatar and blue bubble
}
```

### Markdown Processor
Supports:
- **Code blocks** with copy button
- **Inline code** `like this`
- **Bold** `**text**` and *italic* `_text_`
- **Headers** `## Heading`
- **Blockquotes** `> Quote`
- **Newlines** → `<br>`

### Custom Scout Tokens
```javascript
// CVE pills
@@CVE:CVE-2019-0708:9.8 — BlueKeep RCE
→ [Red badge] CVE-2019-0708 · CVSS 9.8  BlueKeep RCE

// MITRE tags
@@MITRE:T1210:Lateral Movement
→ [Purple tag] ⚔️ T1210 · Lateral Movement

// Grade card
@@GRADE:D:🔴
→ [Large D with emoji] 🔴 Security Grade

// Progress bar
@@PROGRESS:2:7
→ [Visual bar showing 2/7 progress]

// Action buttons
@@BUTTONS:Yes,walk me through it|Just show me the fixes|No thanks
→ [Three clickable buttons]
```

### Session Storage
```javascript
const SID = localStorage.getItem("scout_sid") || 
            (genNewSessionId() && store it)
```

Each browser tab maintains its own session via `session_id`, allowing multiple independent scans.

---

## 🚀 Startup Flow

### Windows (START_Scout.bat)
```batch
@echo off
title Scout - Security Assistant
echo Scout - Security Assistant
echo Open browser at http://localhost:8765
cd /d "%~dp0"
pip install -r requirements.txt -q 2>nul
start http://localhost:8765
python scout.py
pause
```

1. Auto-install dependencies
2. Open browser to `http://localhost:8765`
3. Start FastAPI server on port `8765`
4. Serve `index.html` at `/`
5. Wait for `/chat` POST requests

### Socket & Port
- **Host:** `0.0.0.0` (accepts local + remote connections)
- **Port:** `8765` (hardcoded)
- **API:** `/chat` (POST), `/` (GET index.html), `/health` (GET)

---

## 🔗 API Endpoints

### `POST /chat`
**Request:**
```json
{
  "session_id": "s1a2b3c4d5e6f",
  "message": "scan example.com"
}
```

**Response:**
```json
{
  "reply": "🔍 Running initial security check...\n\n..." 
}
```

**Flow:**
1. Load/create session
2. Call `process(message, session)`
3. Update session state
4. Return formatted reply

### `GET /health`
**Response:**
```json
{
  "status": "ok",
  "gemini": true,
  "danishrecon": true
}
```

Diagnostic endpoint — checks if dependencies are available.

### `GET /`
Returns `index.html` static file with embedded JavaScript.

---

## 🔐 Grade Computation

```python
def compute_grade(findings) -> ("A", "🟢", 0)
```

**Scoring system:**
| Issue | Points |
|---|---|
| CRITICAL port | +40 |
| HIGH port | +20 |
| MEDIUM port | +10 |
| LOW port | +2 |
| Broken SSL | +30 |
| SSL expires <30 days | +15 |
| Missing security header | +5 each |
| Missing DNS record (SPF/DMARC) | +8 each |
| XSS vulnerability | +30 each |
| SQLI vulnerability | +40 each |
| IDOR vulnerability | +20 each |

**Grade scale:**
- **A (🟢):** 0 points
- **B (🟡):** < 20 points
- **C (🟠):** 20-49 points
- **D (🔴):** 50-99 points
- **E (🔴):** 100-149 points
- **F (🔴):** 150+ points

---

## 🛠️ Dependencies (`requirements.txt`)

```
fastapi              # Web framework
uvicorn             # ASGI server
requests            # HTTP client (header checks)
pydantic            # Data validation
python-dotenv       # .env loader
google-generativeai # Gemini API client
httpx               # Async HTTP (backup)
urllib3             # HTTP utilities
```

**External (not pip):**
- `nmap` — Port scanning (must be installed separately)
- `nslookup` — DNS queries (built-in on Windows/Linux)

---

## 🔌 Integration with CyberRecon-Pro

`danishrecon_bridge.py` imports from the parent `CyberRecon-Pro` module:

```python
from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile
```

**Why a bridge?**
- CyberRecon-Pro has **PyQt5 GUI dependencies** that Scout doesn't need
- Bridge isolates **pure-Python functionality** for the chatbot
- Allows reuse of vulnerability scanner without GUI bloat

---

## 💡 Key Design Decisions

| Decision | Why |
|---|---|
| **Regex + Gemini hybrid** | Regex is fast & predictable for common patterns; Gemini handles open-ended questions |
| **Hardcoded CVE database** | No external API calls = no rate limits, works offline-ish |
| **Plain JavaScript frontend** | No build step, smaller bundle, easier to modify |
| **Session-based state machine** | Handles multi-step walkthroughs without polling for state |
| **Beginner analogies** | Security jargon ("CVSS", "RCE") means nothing to non-technical users |
| **Real copy-paste commands** | Users can ctrl+c directly from chat and run them |
| **Port 8765** | High port number avoids privilege issues on Linux/Mac |

---

## 📊 User Flow Example

```
User opens http://localhost:8765
  ↓
Welcome message: "Hi! What would you like me to scan?"
  ↓
User: "scan example.com"
  ↓
Scout runs quick_check (5s): DNS, SSL, headers
  ↓
"Found 3 initial issues. Want me to scan for open ports?"
  ↓
User: "yes"
  ↓
Scout runs port_scan_deep (45s): nmap + CVE enrichment
  ↓
"Found 7 security issues total. Walk you through each one?"
  ↓
User: "yes"
  ↓
[Walkthrough mode]
Problem 1/7: FTP on port 21 (CRITICAL)
  ↓ User: "next"
Problem 2/7: RDP on port 3389 (CRITICAL)
  ↓ User: "explain"
Gemini explanation in plain English
  ↓ User: "fix"
Step-by-step fix guide with commands
  ↓ User: "next"
Problem 3/7: Broken SSL
  ↓ ... (repeat until done)
  ↓
Final summary with all CRITICAL/HIGH items first
  ↓
"Ask me anything or scan another target!"
```

---

## 🐛 Error Handling

**Gracefully degrades:**

| Failure | Behavior |
|---|---|
| nmap not installed | Skips port scan, continues with quick_check |
| Target DNS fails | "Can't find that domain — check spelling" |
| SSL cert invalid | Shows detailed error + fix guide |
| Gemini API down | Falls back to regex-matched responses |
| Web scanner module missing | Notes unavailable, continues with port/DNS/SSL |

---

## 🎓 Learning Outcomes

After using Scout, users understand:
1. **What ports are dangerous** and why (WannaCry, RDP brute-force, etc.)
2. **How to read CVSS scores** and prioritize fixes
3. **Real commands** they can run to secure their server
4. **Why specific services are risky** (plain-text protocols, auth bypass, RCE)
5. **MITRE ATT&CK framework** concepts in context

---

## ✨ Unique Features

1. **Beginner-first language** — No "XSS", say "malicious script injection"
2. **Real-world analogies** — FTP = "filing cabinet outside with no lock"
3. **MITRE ATT&CK mapping** — Users learn industry-standard terminology
4. **Copy-paste fixes** — Commands work on Linux/Windows as-is
5. **Progress tracking** — Visual bar showing "Problem 2 of 7"
6. **CVE context** — Shows real exploits for each service
7. **Interactive walkthrough** — Users control pace (next/skip/explain/fix)
8. **No data stored** — Runs locally, scans are ephemeral
9. **Hybrid NLP** — Fast regex + smart Gemini fallback
10. **Grade report card** — A-F security score for motivation

---

## 📈 Future Enhancements

Potential improvements:
- **Export scan reports** (PDF, JSON)
- **Scheduled rescans** (re-check same target weekly)
- **Vulnerability impact tags** (business risk, user impact)
- **Exploit PoC links** (for learning)
- **Fix verification** (re-scan after fix, show before/after)
- **Team management** (scan history, assign fixes)
- **Compliance mapping** (PCI, HIPAA, GDPR impact)
- **Remediation workflows** (assign fixes to team members)

---

## 🎯 Conclusion

Scout is a **modern security chatbot** that bridges the gap between automated scanning and human understanding. It combines:

- **Powerful scanning** (nmap, web vulns, SSL, DNS, headers)
- **Beginner-friendly explanations** (analogies, MITRE context, real commands)
- **Interactive guidance** (state machine, walkthrough, real-time feedback)
- **Zero friction** (runs locally, no signup, no data storage)

Perfect for:
- ✅ Small teams starting their security journey
- ✅ Developers who need quick security audits
- ✅ CTF/Hackathon participants
- ✅ Learning security concepts hands-on
- ✅ Non-technical stakeholders understanding security risks

**Unique edge:** It doesn't just find vulnerabilities — it *teaches* users why they matter and how to fix them.


#!/usr/bin/env python3
"""
DanishRecon Bridge for Scout Chatbot
Imports pure-Python sub-modules only — NO PyQt5.
"""

import os, sys, re, ssl, socket, subprocess, json
import asyncio
from datetime import datetime
from pathlib import Path
import requests as req

# ── Add CyberRecon-Pro to sys.path
_RECON_DIR = Path(__file__).parent.parent / "CyberRecon-Pro"
if str(_RECON_DIR) not in sys.path:
    sys.path.insert(0, str(_RECON_DIR))

WEB_VULN_AVAILABLE = False
try:
    from web_vulnerability_scanner import WebVulnerabilityScanner, ScanProfile
    WEB_VULN_AVAILABLE = True
except ImportError:
    pass

# ══════════════════════════════════════
#  CVE Knowledge Base (no PyQt5 needed)
# ══════════════════════════════════════
CVE_DB = {
    "ftp":     [{"cve":"CVE-2011-2523","cvss":10.0,"title":"vsftpd Backdoor – Full Takeover","mitre":"T1190","tactic":"Initial Access"},
                {"cve":"CVE-1999-0497","cvss":7.5, "title":"FTP Anonymous Login","mitre":"T1078","tactic":"Defense Evasion"}],
    "ssh":     [{"cve":"CVE-2018-15473","cvss":5.3,"title":"OpenSSH Username Enumeration","mitre":"T1592","tactic":"Reconnaissance"},
                {"cve":"CVE-2023-38408","cvss":9.8,"title":"OpenSSH RCE via Agent","mitre":"T1021.004","tactic":"Lateral Movement"}],
    "http":    [{"cve":"CVE-2021-41773","cvss":9.8,"title":"Apache Path Traversal & RCE","mitre":"T1190","tactic":"Initial Access"}],
    "https":   [{"cve":"CVE-2014-0160","cvss":7.5,"title":"Heartbleed – Read Server Memory","mitre":"T1552","tactic":"Credential Access"}],
    "mysql":   [{"cve":"CVE-2012-2122","cvss":7.5,"title":"MySQL Auth Bypass","mitre":"T1078","tactic":"Defense Evasion"},
                {"cve":"CVE-2016-6662","cvss":9.8,"title":"MySQL RCE via Config","mitre":"T1190","tactic":"Initial Access"}],
    "mssql":   [{"cve":"CVE-2000-0402","cvss":7.5,"title":"MS SQL xp_cmdshell Command Exec","mitre":"T1059","tactic":"Execution"}],
    "rdp":     [{"cve":"CVE-2019-0708","cvss":9.8,"title":"BlueKeep – RDP Pre-Auth RCE","mitre":"T1210","tactic":"Lateral Movement"},
                {"cve":"CVE-2019-1182","cvss":9.8,"title":"DejaBlue – Wormable RCE","mitre":"T1210","tactic":"Lateral Movement"}],
    "smb":     [{"cve":"CVE-2017-0144","cvss":9.3,"title":"EternalBlue – WannaCry","mitre":"T1210","tactic":"Lateral Movement"},
                {"cve":"CVE-2020-0796","cvss":10.0,"title":"SMBGhost – SMBv3 RCE","mitre":"T1210","tactic":"Lateral Movement"}],
    "telnet":  [{"cve":"CVE-2011-4862","cvss":10.0,"title":"BSD Telnet RCE","mitre":"T1021","tactic":"Lateral Movement"}],
    "mongodb": [{"cve":"CVE-2013-4650","cvss":7.5,"title":"MongoDB No-Auth Data Leak","mitre":"T1190","tactic":"Initial Access"}],
    "redis":   [{"cve":"CVE-2015-4335","cvss":10.0,"title":"Redis Unauthenticated RCE","mitre":"T1190","tactic":"Initial Access"}],
    "vnc":     [{"cve":"CVE-2006-2369","cvss":7.5,"title":"VNC NULL Auth Bypass","mitre":"T1021","tactic":"Lateral Movement"}],
}

RISK = {
    "ftp":("CRITICAL","🔴"), "telnet":("CRITICAL","🔴"), "rdp":("CRITICAL","🔴"),
    "smb":("CRITICAL","🔴"), "vnc":("CRITICAL","🔴"),
    "mysql":("HIGH","🟠"),   "mssql":("HIGH","🟠"),    "mongodb":("HIGH","🟠"), "redis":("HIGH","🟠"),
    "ssh":("MEDIUM","🟡"),   "http":("MEDIUM","🟡"),   "smtp":("MEDIUM","🟡"),
    "https":("LOW","🟢"),    "dns":("LOW","🟢"),
}
RISK_ORDER = {"CRITICAL":0,"HIGH":1,"MEDIUM":2,"LOW":3}

# ══════════════════════════════════════
#  Beginner-friendly descriptions
# ══════════════════════════════════════
BEGINNER = {
    "ftp": {
        "plain_name": "FTP File Transfer (Port 21)",
        "analogy": "Like leaving your filing cabinet **outside the office with no lock**. Anyone walking by can open it, steal files, or put malware inside.",
        "hacker_can": ["Steal all your files", "Upload ransomware to your server", "Completely take over your system (CVSS 10/10 exploit exists)"],
        "urgency": "🚨 Fix TODAY",
        "time_to_fix": "5 minutes",
        "fix_steps": [
            "Check if FTP is running: `sudo systemctl status vsftpd`",
            "Turn it off: `sudo systemctl stop vsftpd && sudo systemctl disable vsftpd`",
            "Block the port: `sudo ufw deny 21`",
            "💡 Use **SFTP** instead — it's encrypted and already built into SSH, no install needed"
        ],
    },
    "telnet": {
        "plain_name": "Telnet Remote Access (Port 23)",
        "analogy": "Telnet broadcasts your passwords **over a loudspeaker**. Every command you type, including passwords, is sent as plain text anyone on the network can read.",
        "hacker_can": ["Read your password as you type it", "Intercept everything on your server", "Take remote control"],
        "urgency": "🚨 Fix TODAY — Telnet has been obsolete since the 1990s",
        "time_to_fix": "5 minutes",
        "fix_steps": [
            "Disable it: `sudo systemctl stop telnet && sudo systemctl disable telnet`",
            "Block the port: `sudo ufw deny 23`",
            "Use SSH instead: `sudo apt install openssh-server`"
        ],
    },
    "rdp": {
        "plain_name": "Windows Remote Desktop — RDP (Port 3389)",
        "analogy": "Like leaving a **spare key under the doormat** with a neon sign. Hackers run automated tools that find RDP ports and try millions of passwords automatically, 24/7.",
        "hacker_can": ["Brute-force your password automatically", "Install ransomware", "Spy on your screen and steal data"],
        "urgency": "🚨 Fix TODAY — #1 ransomware entry point worldwide",
        "time_to_fix": "15 minutes",
        "fix_steps": [
            "If not needed: Control Panel → System → Remote Desktop → **Disable**",
            "If needed: set up a VPN first, only allow RDP from inside the VPN",
            "Enable NLA: System Properties → Remote → 'Allow connections with NLA only'",
            "Block port 3389 in Windows Firewall from public internet access"
        ],
    },
    "smb": {
        "plain_name": "Windows File Sharing — SMB (Port 445)",
        "analogy": "This is the **exact port WannaCry ransomware** used to infect 200,000 computers in 2017. Exposing it to the internet is like leaving a fire door open in a building full of valuables.",
        "hacker_can": ["Install WannaCry or similar ransomware automatically, no click needed", "Access all shared files without a password", "Spread malware to every device on your network"],
        "urgency": "🚨 Fix TODAY",
        "time_to_fix": "5 minutes",
        "fix_steps": [
            "Block SMB from internet — Linux: `sudo ufw deny 445`",
            "Block SMB — Windows Firewall: block inbound port 445",
            "Disable SMBv1 (Windows PowerShell admin): `Set-SmbServerConfiguration -EnableSMB1Protocol $false`",
            "SMB should only be reachable from your local network, NEVER from the internet"
        ],
    },
    "mysql": {
        "plain_name": "MySQL Database (Port 3306)",
        "analogy": "Your **database is like your private vault**. Right now it's facing the street — anyone can walk up and try to open it over the internet.",
        "hacker_can": ["Steal all customer data, passwords, personal info", "Modify or delete your database records", "Extract credit card or financial data"],
        "urgency": "⚠️ Fix this week — databases should NEVER be internet-accessible",
        "time_to_fix": "10 minutes",
        "fix_steps": [
            "Open config: Linux → `/etc/mysql/mysql.conf.d/mysqld.cnf` | Windows → `my.ini`",
            "Find `bind-address` and change to: `bind-address = 127.0.0.1`",
            "Restart MySQL: `sudo systemctl restart mysql`",
            "Verify fix: `netstat -tlnp | grep 3306` (should show 127.0.0.1, NOT 0.0.0.0)"
        ],
    },
    "mongodb": {
        "plain_name": "MongoDB Database (Port 27017)",
        "analogy": "MongoDB by default has **no password at all** — like a filing cabinet with no lock AND no door. Anyone on the internet can read or delete your data.",
        "hacker_can": ["Download your entire database instantly", "Delete everything and demand ransom", "Silently read/modify records"],
        "urgency": "🚨 Fix TODAY — MongoDB breaches are extremely common",
        "time_to_fix": "10 minutes",
        "fix_steps": [
            "Block port immediately: `sudo ufw deny 27017`",
            "Bind to localhost in mongod.conf: `net.bindIp: 127.0.0.1`",
            "Enable authentication: `security.authorization: enabled`",
            "Restart MongoDB: `sudo systemctl restart mongod`"
        ],
    },
    "redis": {
        "plain_name": "Redis Cache (Port 6379)",
        "analogy": "Redis with no password is like a **master key hidden in your server**. Hackers can use it to write files anywhere — including adding themselves as admin users.",
        "hacker_can": ["Add themselves as an admin on your server", "Steal cached session tokens and API keys", "Use your server to attack others"],
        "urgency": "🚨 Fix TODAY — zero skill needed to exploit this",
        "time_to_fix": "10 minutes",
        "fix_steps": [
            "Block from internet: `sudo ufw deny 6379`",
            "Add a password in redis.conf: `requirepass yourStrongPassword`",
            "Bind to localhost: `bind 127.0.0.1`",
            "Restart Redis: `sudo systemctl restart redis`"
        ],
    },
    "ssh": {
        "plain_name": "SSH Remote Access (Port 22)",
        "analogy": "SSH is the *safe* way to manage your server remotely. But having it open means hackers run automated scripts that **try millions of passwords per second** against your server.",
        "hacker_can": ["Brute-force your password automatically", "Log in if you use a weak password", "Install backdoors"],
        "urgency": "⚠️ Secure it soon — can be made very safe with correct config",
        "time_to_fix": "20 minutes",
        "fix_steps": [
            "Disable password login in `/etc/ssh/sshd_config`: `PasswordAuthentication no`",
            "Disable root login: `PermitRootLogin no`",
            "Generate a key on your computer: `ssh-keygen -t ed25519`",
            "Only allow SSH from your IP: `sudo ufw allow from YOUR_IP to any port 22`"
        ],
    },
    "http": {
        "plain_name": "Unencrypted HTTP Website (Port 80)",
        "analogy": "Sending data over plain HTTP is like **mailing a postcard** — anyone handling it along the way can read what's on it, including passwords typed into your site.",
        "hacker_can": ["Intercept login credentials on public WiFi", "Inject malware into your website pages", "Spy on your users"],
        "urgency": "⚠️ Fix this month — get a free SSL certificate",
        "time_to_fix": "15 minutes",
        "fix_steps": [
            "Install free SSL: `sudo apt install certbot python3-certbot-nginx && sudo certbot --nginx -d yourdomain.com`",
            "Force redirect HTTP→HTTPS in nginx: `return 301 https://$host$request_uri;`",
            "Add HSTS header: `add_header Strict-Transport-Security \"max-age=31536000\";`"
        ],
    },
    "vnc": {
        "plain_name": "VNC Remote Desktop (Port 5900)",
        "analogy": "VNC lets anyone **watch your screen and control your mouse/keyboard** over the internet. It's actively targeted by hackers every day.",
        "hacker_can": ["Watch your screen in real-time", "Control your entire computer", "Install ransomware"],
        "urgency": "🚨 Fix TODAY",
        "time_to_fix": "10 minutes",
        "fix_steps": [
            "Block from internet: `sudo ufw deny 5900`",
            "If needed, only use VNC through an SSH tunnel: `ssh -L 5901:localhost:5900 user@server`",
            "Set a strong VNC password: `vncpasswd`"
        ],
    },
    "smtp": {
        "plain_name": "Mail Server (Port 25)",
        "analogy": "An improperly configured mail server can become an **open relay** — spammers use it to send millions of spam emails using YOUR domain.",
        "hacker_can": ["Send spam using your domain (gets you blacklisted)", "Your domain reputation drops, emails go to spam"],
        "urgency": "⚠️ Check configuration",
        "time_to_fix": "30 minutes",
        "fix_steps": [
            "Test for open relay: https://mxtoolbox.com/diagnostic.aspx",
            "Disable open relay in Postfix: `smtpd_relay_restrictions = permit_mynetworks, permit_sasl_authenticated, reject_unauth_destination`",
            "Restart Postfix: `sudo systemctl restart postfix`"
        ],
    },
}

DNS_BEGINNER = {
    "No SPF": {
        "plain_name": "Missing Email Spoofing Protection (SPF)",
        "analogy": "Without SPF, anyone can send emails that **appear to come from your domain**. It's like someone printing fake business cards with your company name.",
        "urgency": "⚠️ Fix this month — 5-minute fix",
        "fix_steps": [
            "Log into your DNS registrar (GoDaddy, Namecheap, Cloudflare, etc.)",
            "Add a TXT record: `v=spf1 mx ~all` (or `include:_spf.google.com ~all` if using Gmail)",
            "Test it free at https://mxtoolbox.com/spf.aspx"
        ],
    },
    "No DMARC": {
        "plain_name": "Missing Anti-Phishing Policy (DMARC)",
        "analogy": "DMARC tells email providers what to do when someone fakes your domain. Without it, **phishing emails using your name go straight to inboxes**.",
        "urgency": "⚠️ Fix this month",
        "fix_steps": [
            "Log into your DNS registrar",
            "Add TXT record for `_dmarc.yourdomain.com`: `v=DMARC1; p=quarantine; rua=mailto:you@email.com`",
            "Test it at https://mxtoolbox.com/dmarc.aspx"
        ],
    },
}

# ══════════════════════════════════════
#  Scan functions
# ══════════════════════════════════════
def nmap_quick(target: str) -> list:
    try:
        out = subprocess.run(
            ["nmap", "-F", "-T4", "-sV", "--open", target],
            capture_output=True, text=True, timeout=60
        ).stdout
        ports = []
        for line in out.splitlines():
            m = re.match(r'\s*(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)', line)
            if m:
                ports.append({"port": m.group(1), "proto": m.group(2),
                               "service": m.group(3), "version": m.group(4).strip()})
        return ports
    except FileNotFoundError:
        return [{"error": "nmap_not_found"}]
    except subprocess.TimeoutExpired:
        return [{"error": "timeout"}]
    except Exception as e:
        return [{"error": str(e)}]


def dns_recon(target: str) -> dict:
    """Fast DNS check for SPF and DMARC."""
    result = {"records": [], "issues": []}
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', target):
        return result
    try:
        out = subprocess.run(["nslookup", "-type=TXT", target],
                             capture_output=True, text=True, timeout=8).stdout
        if "v=spf1" not in out.lower():
            result["issues"].append("No SPF")
        if "v=dmarc1" not in out.lower():
            # try _dmarc subdomain
            try:
                dmarc_out = subprocess.run(
                    ["nslookup", "-type=TXT", f"_dmarc.{target}"],
                    capture_output=True, text=True, timeout=6).stdout
                if "v=dmarc1" not in dmarc_out.lower():
                    result["issues"].append("No DMARC")
            except Exception:
                result["issues"].append("No DMARC")
    except Exception:
        pass
    return result


def ssl_check(target: str, port: int = 443) -> dict:
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=target) as s:
            s.settimeout(6)
            s.connect((target, port))
            cert = s.getpeercert()
            cipher = s.cipher()
            expire_str = cert.get("notAfter", "")
            days_left = -1
            if expire_str:
                exp = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (exp - datetime.utcnow()).days
            issuer = dict(x[0] for x in cert.get("issuer", []))
            return {"valid": True, "days_left": days_left,
                    "tls_version": cipher[2] if cipher else "Unknown",
                    "cipher": cipher[0] if cipher else "Unknown",
                    "issuer": issuer.get("organizationName", issuer.get("O", "Unknown"))}
    except ssl.SSLCertVerificationError as e:
        return {"valid": False, "error": str(e), "type": "cert_error"}
    except Exception as e:
        return {"valid": False, "error": str(e), "type": "connect_error"}


def header_check(target: str) -> dict:
    HDRS = ["X-Frame-Options", "X-Content-Type-Options",
            "Content-Security-Policy", "Strict-Transport-Security",
            "X-XSS-Protection", "Referrer-Policy"]
    try:
        import urllib3; urllib3.disable_warnings()
        r = req.get(f"https://{target}", timeout=6, verify=False)
        return {"missing": [h for h in HDRS if h not in r.headers],
                "present": [h for h in HDRS if h in r.headers],
                "server": r.headers.get("Server", "Unknown")}
    except Exception as e:
        return {"error": str(e)}


def enrich_ports(ports: list) -> list:
    enriched = []
    for p in ports:
        svc = p.get("service", "").lower()
        risk, emoji = RISK.get(svc, ("LOW", "🔵"))
        cves = CVE_DB.get(svc, [])[:2]
        enriched.append({**p, "risk": risk, "emoji": emoji, "cves": cves,
                         "beginner": BEGINNER.get(svc)})
    return sorted(enriched, key=lambda x: RISK_ORDER.get(x["risk"], 3))


def compute_grade(findings: dict) -> tuple:
    score = 0
    for p in findings.get("ports", []):
        score += {"CRITICAL": 40, "HIGH": 20, "MEDIUM": 10, "LOW": 2}.get(p.get("risk", "LOW"), 0)
    ssl_d = findings.get("ssl", {})
    if not ssl_d.get("valid", True):
        score += 30
    elif ssl_d.get("days_left", 999) < 30:
        score += 15
    score += len(findings.get("headers", {}).get("missing", [])) * 5
    score += len(findings.get("dns", {}).get("issues", [])) * 8
    wv = findings.get("web_vulns", {})
    score += len(wv.get("xss", [])) * 30
    score += len(wv.get("sqli", [])) * 40
    score += len(wv.get("idor", [])) * 20
    if score == 0:   return "A", "🟢", score
    if score < 20:   return "B", "🟡", score
    if score < 50:   return "C", "🟠", score
    if score < 100:  return "D", "🔴", score
    if score < 150:  return "E", "🔴", score
    return "F", "🔴", score


# ══════════════════════════════════════
#  Main scan entry-points
# ══════════════════════════════════════
async def quick_check(target: str) -> dict:
    """Fast check: DNS + SSL + Headers (~5–8 s). No nmap."""
    findings = {"target": target, "stage": "quick",
                "dns": {}, "ssl": {}, "headers": {}, "errors": []}
    try:
        socket.gethostbyname(target)
    except socket.gaierror:
        findings["errors"].append("host_not_found")
        return findings
    findings["dns"]     = dns_recon(target)
    findings["ssl"]     = ssl_check(target)
    findings["headers"] = header_check(target)
    return findings


async def port_scan_deep(target: str) -> dict:
    """Full port scan with CVE enrichment (~30–60 s)."""
    findings = {"target": target, "stage": "port", "ports": [], "errors": []}
    raw = nmap_quick(target)
    if raw and "error" in raw[0]:
        findings["errors"].append(raw[0]["error"])
    else:
        findings["ports"] = enrich_ports(raw)
    return findings


async def web_vuln_scan(target: str) -> dict:
    """XSS / IDOR / SQLi scan via WebVulnerabilityScanner."""
    findings = {"target": target, "stage": "web",
                "web_vulns": {"xss": [], "idor": [], "sqli": []}, "errors": []}
    if not WEB_VULN_AVAILABLE:
        findings["errors"].append("web_vuln_module_unavailable")
        return findings
    try:
        url = f"https://{target}"
        scanner = WebVulnerabilityScanner(url, ScanProfile.QUICK)
        result = await scanner.scan([url])
        findings["web_vulns"] = {
            "xss":  [{"url": v.url, "param": v.parameter, "severity": v.severity} for v in result.get("xss", [])],
            "idor": [{"url": v.url, "param": v.parameter, "severity": v.severity} for v in result.get("idor", [])],
            "sqli": [{"url": v.url, "param": v.parameter, "severity": v.severity} for v in result.get("sqli", [])],
        }
    except Exception as e:
        findings["errors"].append(str(e))
    return findings

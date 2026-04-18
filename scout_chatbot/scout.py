#!/usr/bin/env python3
"""
Scout — NLP Security Chatbot Backend
Beginner-friendly guided security walkthrough powered by DanishRecon.
Run: python scout.py  →  open http://localhost:8765
"""

import os, re, json
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

gemini_model = None
if GEMINI_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    except Exception:
        pass

# ── Import DanishRecon bridge ─────────────────────────────────────────────────
try:
    from danishrecon_bridge import (
        quick_check, port_scan_deep, web_vuln_scan,
        compute_grade, BEGINNER, DNS_BEGINNER, CVE_DB, RISK
    )
    BRIDGE_AVAILABLE = True
except ImportError as e:
    BRIDGE_AVAILABLE = False

app = FastAPI(title="Scout Security Assistant")
sessions: dict = {}

class ChatReq(BaseModel):
    session_id: str
    message: str

# ── Regex patterns ────────────────────────────────────────────────────────────
RE_IP      = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
RE_DOMAIN  = re.compile(r'\b(?!-)[A-Za-z0-9\-]{1,63}(?<!-)(\.[A-Za-z]{2,})+\b')
RE_SCAN    = re.compile(r'\b(scan|check|analyze|test|audit|inspect|look at|is my|is it safe|safe|secure|vulnerab)\b', re.I)
RE_SSL     = re.compile(r'\b(ssl|tls|certificate|cert|https)\b', re.I)
RE_HEADER  = re.compile(r'\b(header|headers|security header)\b', re.I)
RE_YES     = re.compile(r'^\s*(yes|yeah|yep|sure|ok|okay|go|do it|yup|y|absolutely|please|proceed|continue|next|ready|show me|walk|start)\s*$', re.I)
RE_NO      = re.compile(r'^\s*(no|nope|skip|nah|not now|later|done|stop|enough|quit|end|finish)\s*$', re.I)
RE_NEXT    = re.compile(r'\b(next|continue|move on|go on|proceed|got it|understood|okay|ok|yes|show me|ready)\b', re.I)
RE_SKIP    = re.compile(r'\b(skip|pass|not this|next one|later)\b', re.I)
RE_DONE    = re.compile(r'\b(done|stop|finish|enough|quit|end|summary|all done|that.?s all)\b', re.I)
RE_FIX     = re.compile(r'\b(fix|patch|secure|harden|remediat|how to|steps|repair|solve)\b', re.I)
RE_EXPLAIN = re.compile(r'\b(what is|explain|what does|define|tell me|more|detail|why|how does)\b', re.I)
RE_WEB     = re.compile(r'\b(xss|sqli|sql injection|idor|web vuln|web scan|check for xss|test for)\b', re.I)


# ── Gemini fallback ───────────────────────────────────────────────────────────
def ask_gemini(prompt: str) -> str:
    if not gemini_model:
        return ""
    try:
        resp = gemini_model.generate_content(
            "You are Scout, a friendly cybersecurity assistant for non-technical users. "
            "Use simple analogies, no jargon. Keep it under 120 words. "
            "End with one helpful follow-up question.\n\n" + prompt
        )
        return resp.text
    except Exception:
        return ""


# ── Extract target from message ───────────────────────────────────────────────
def extract_target(msg: str):
    m = RE_IP.search(msg)
    if m: return m.group(1)
    m = RE_DOMAIN.search(msg)
    if m:
        t = m.group(0)
        # Reject bare words that the regex picks up as false positives
        # but KEEP real domains like example.com, scanme.nmap.org
        bare_rejects = {"fix.it","scan.it","check.it"}
        if t.lower() in bare_rejects:
            return None
        # Must have at least one dot to be a real domain
        if "." in t and len(t) > 4:
            return t
    return None


# ══════════════════════════════════════════════════════════════════
#  WALKTHROUGH ENGINE — builds a queue of plain-English findings
# ══════════════════════════════════════════════════════════════════
def build_vuln_list(quick_data: dict, port_data: dict, web_data: dict) -> list:
    """Turn all scan findings into an ordered walkthrough queue."""
    vulns = []

    # 1. Port findings (sorted by severity — already done in bridge)
    for p in port_data.get("ports", []):
        svc = p.get("service", "").lower()
        beg = p.get("beginner") or BEGINNER.get(svc)
        if not beg:
            continue
        cves = p.get("cves", [])
        vulns.append({
            "type":       "port",
            "service":    svc,
            "port":       p.get("port", "?"),
            "risk":       p.get("risk", "LOW"),
            "emoji":      p.get("emoji", "🔵"),
            "plain_name": beg["plain_name"],
            "analogy":    beg["analogy"],
            "hacker_can": beg.get("hacker_can", []),
            "urgency":    beg["urgency"],
            "fix_steps":  beg["fix_steps"],
            "time_to_fix":beg.get("time_to_fix", "varies"),
            "cves":       cves,
        })

    # 2. DNS issues
    for issue in quick_data.get("dns", {}).get("issues", []):
        key = "No SPF" if "SPF" in issue else "No DMARC" if "DMARC" in issue else None
        beg = DNS_BEGINNER.get(key, {}) if key else {}
        vulns.append({
            "type":       "dns",
            "service":    key or issue,
            "risk":       "MEDIUM",
            "emoji":      "🟡",
            "plain_name": beg.get("plain_name", issue),
            "analogy":    beg.get("analogy", ""),
            "hacker_can": [],
            "urgency":    beg.get("urgency", "⚠️ Fix this month"),
            "fix_steps":  beg.get("fix_steps", []),
            "time_to_fix":"5 minutes",
            "cves":       [],
        })

    # 3. SSL issues
    ssl_d = quick_data.get("ssl", {})
    if not ssl_d.get("valid", True):
        vulns.insert(0, {
            "type":       "ssl",
            "service":    "ssl",
            "risk":       "CRITICAL",
            "emoji":      "🔴",
            "plain_name": "Broken SSL Certificate",
            "analogy":    "Your website shows a **huge red warning screen** to every visitor. Browsers treat this like a danger sign — most people leave immediately.",
            "hacker_can": ["Perform man-in-the-middle attacks", "Steal data sent between users and your site"],
            "urgency":    "🚨 Fix TODAY",
            "fix_steps":  ["Install a free certificate: `sudo certbot --nginx -d yourdomain.com`",
                           "Or from your hosting panel: SSL section → Install Let's Encrypt",
                           "Auto-renewal is set up automatically ✅"],
            "time_to_fix":"10 minutes",
            "cves":       [],
        })
    elif ssl_d.get("days_left", 999) < 30:
        days = ssl_d["days_left"]
        urgency = "🚨 Fix TODAY" if days < 7 else "⚠️ Fix this week"
        vulns.insert(0, {
            "type":       "ssl",
            "service":    "ssl",
            "risk":       "HIGH" if days < 7 else "MEDIUM",
            "emoji":      "🔴" if days < 7 else "🟡",
            "plain_name": f"SSL Certificate Expiring in {days} Days",
            "analogy":    f"Your security certificate expires in {days} days. After that, visitors see a scary 'Not Secure' warning.",
            "hacker_can": ["Exploit the window when your cert expires to intercept traffic"],
            "urgency":    urgency,
            "fix_steps":  ["Renew with Certbot: `sudo certbot renew`",
                           "From hosting panel: SSL section → Renew"],
            "time_to_fix":"5 minutes",
            "cves":       [],
        })

    # 4. Missing security headers (grouped as one finding)
    missing_hdrs = quick_data.get("headers", {}).get("missing", [])
    if missing_hdrs:
        vulns.append({
            "type":       "headers",
            "service":    "headers",
            "risk":       "MEDIUM",
            "emoji":      "🟡",
            "plain_name": f"Missing Security Headers ({len(missing_hdrs)} missing)",
            "analogy":    "Security headers are like **instructions you give to visitors' browsers** on how to protect themselves. Without them, browsers have no idea they should block click-jacking, XSS, and other tricks.",
            "hacker_can": ["Trick users into clicking invisible buttons on your page (clickjacking)",
                           "Inject malicious scripts (XSS attacks)",
                           "Steal user data by loading your page inside their malicious site"],
            "urgency":    "⚠️ Fix this week — copy-paste fix available",
            "fix_steps":  ["Add these lines to your nginx `server {}` block:"] +
                          [f"`add_header {h} ...` (see below)" for h in missing_hdrs[:4]] +
                          ["Then: `sudo nginx -t && sudo systemctl reload nginx`"],
            "time_to_fix":"15 minutes",
            "cves":       [],
            "_missing_headers": missing_hdrs,
        })

    # 5. Web vulns
    wv = web_data.get("web_vulns", {})
    for xss in wv.get("xss", [])[:3]:
        vulns.append({
            "type": "web", "service": "xss", "risk": xss["severity"],
            "emoji": "🔴" if xss["severity"] in ("CRITICAL","HIGH") else "🟡",
            "plain_name": "Cross-Site Scripting (XSS) Detected",
            "analogy": "XSS lets a hacker **inject malicious code into your website**. When visitors load your page, the attacker's code runs in their browser — stealing login sessions.",
            "hacker_can": ["Steal login sessions — log in AS your users", "Redirect users to fake/phishing pages"],
            "urgency": "🔴 Fix this week",
            "fix_steps": ["Escape all user input before displaying it", "Add Content-Security-Policy header",
                          "Use a WAF (Web Application Firewall)"],
            "time_to_fix": "depends on your code",
            "cves": [], "_detail": xss,
        })
    for sqli in wv.get("sqli", [])[:3]:
        vulns.append({
            "type": "web", "service": "sqli", "risk": "CRITICAL",
            "emoji": "🔴",
            "plain_name": "SQL Injection Detected",
            "analogy": "SQL Injection is like someone **picking the lock on your database** by typing specially crafted text into a form.",
            "hacker_can": ["Dump your entire database", "Bypass login without a password", "Delete all your data"],
            "urgency": "🚨 Fix TODAY",
            "fix_steps": ["Use parameterized queries in all database calls",
                          "Never concatenate user input into SQL strings",
                          "Add a WAF rule to block SQL keywords"],
            "time_to_fix": "depends on your code",
            "cves": [], "_detail": sqli,
        })

    return vulns


def format_vuln_card(vuln: dict, idx: int, total: int) -> str:
    """Format a single vulnerability as a beginner-friendly message."""
    risk_label = {"CRITICAL": "🚨 URGENT — Fix immediately",
                  "HIGH":     "⚠️ SERIOUS — Fix this week",
                  "MEDIUM":   "📋 MODERATE — Fix this month",
                  "LOW":      "ℹ️ LOW RISK — Good to fix"}.get(vuln["risk"], "")

    lines = [
        f"@@PROGRESS:{idx}:{total}",
        f"\n{vuln['emoji']} **Problem {idx} of {total}: {vuln['plain_name']}**\n",
        f"**What this means (in plain English):**\n> {vuln['analogy']}\n",
        f"**Danger level:** {risk_label}",
    ]

    if vuln.get("hacker_can"):
        lines.append("\n**What a hacker could do:**")
        for h in vuln["hacker_can"]:
            lines.append(f"• {h}")

    if vuln.get("cves"):
        lines.append("\n**Known exploits hackers use:**")
        for c in vuln["cves"]:
            lines.append(f"@@CVE:{c['cve']}:{c['cvss']} — {c['title']}")
            lines.append(f"@@MITRE:{c['mitre']}:{c['tactic']}")

    lines.append(f"\n**How to fix it** _(takes ~{vuln.get('time_to_fix','varies')})_:")
    for i, step in enumerate(vuln["fix_steps"], 1):
        lines.append(f"**Step {i}:** {step}")

    if vuln.get("_missing_headers"):
        hdrs = vuln["_missing_headers"]
        hdr_fixes = {
            "X-Frame-Options": 'add_header X-Frame-Options "SAMEORIGIN";',
            "X-Content-Type-Options": 'add_header X-Content-Type-Options "nosniff";',
            "Strict-Transport-Security": 'add_header Strict-Transport-Security "max-age=31536000";',
            "X-XSS-Protection": 'add_header X-XSS-Protection "1; mode=block";',
            "Referrer-Policy": 'add_header Referrer-Policy "strict-origin-when-cross-origin";',
            "Content-Security-Policy": "add_header Content-Security-Policy \"default-src 'self';\";",
        }
        lines.append("\n**Copy-paste fix for nginx:**\n```")
        for h in hdrs:
            if h in hdr_fixes:
                lines.append(hdr_fixes[h])
        lines.append("```")

    lines.append(f"\n{vuln['urgency']}")

    if idx < total:
        lines.append(f"\n---\n✅ Ready for **problem {idx+1}**? Say **next** — or ask me anything about this one.")
        lines.append("@@BUTTONS:Next problem ➜|Explain more|Skip")
    else:
        lines.append("\n---\n🎉 That's all the problems! Say **summary** to see your full security report.")
        lines.append("@@BUTTONS:Show my summary|Done")

    return "\n".join(lines)


def format_overview(target: str, quick_data: dict, port_data: dict, web_data: dict, vuln_list: list) -> str:
    """Format the post-scan overview message."""
    all_data = {**quick_data, **port_data, **web_data}
    grade, g_emoji, score = compute_grade(all_data)

    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for v in vuln_list:
        counts[v.get("risk", "LOW")] = counts.get(v.get("risk", "LOW"), 0) + 1

    lines = [
        f"✅ **Scan complete for {target}!**\n",
        f"@@GRADE:{grade}:{g_emoji}",
        f"\n📊 **Your Security Report Card: Grade {grade}**\n",
    ]

    if counts["CRITICAL"]:
        lines.append(f"🔴 **{counts['CRITICAL']} CRITICAL** — fix immediately (server takeover risk)")
    if counts["HIGH"]:
        lines.append(f"🟠 **{counts['HIGH']} HIGH** — fix this week (serious breach risk)")
    if counts["MEDIUM"]:
        lines.append(f"🟡 **{counts['MEDIUM']} MODERATE** — fix this month")
    if counts["LOW"]:
        lines.append(f"🟢 **{counts['LOW']} LOW** — good practice improvements")

    total = len(vuln_list)
    if total == 0:
        lines += ["\n🎉 **Great news!** I didn't find any major security problems.",
                  "Your server looks well-configured. Keep it updated!"]
        return "\n".join(lines)

    lines.append(f"\n**I found {total} security issue{'s' if total>1 else ''} total. Here's a quick preview:**\n")
    for i, v in enumerate(vuln_list[:5], 1):
        lines.append(f"{v['emoji']} {i}. **{v['plain_name']}** — {v['urgency']}")
    if total > 5:
        lines.append(f"  _...and {total-5} more_")

    lines += [
        "\n---",
        f"🚀 **Want me to walk you through each problem step by step?**",
        "I'll explain what it means in plain English and give you exact commands to fix it.",
        "\n@@BUTTONS:Yes, walk me through it!|Just show me the fixes|No thanks",
    ]
    return "\n".join(lines)


def format_summary(vuln_list: list, target: str) -> str:
    """Final summary after walkthrough."""
    lines = [f"## 📋 Security Summary for **{target}**\n"]
    urgent = [v for v in vuln_list if v["risk"] in ("CRITICAL", "HIGH")]
    medium  = [v for v in vuln_list if v["risk"] == "MEDIUM"]

    if urgent:
        lines.append("### 🚨 Fix These FIRST:\n")
        for v in urgent:
            lines.append(f"{v['emoji']} **{v['plain_name']}** — {v['urgency']}")
            lines.append(f"  → {v['fix_steps'][0]}\n")

    if medium:
        lines.append("### ⚠️ Fix These Soon:\n")
        for v in medium:
            lines.append(f"🟡 **{v['plain_name']}**")
            lines.append(f"  → {v['fix_steps'][0]}\n")

    lines += [
        "---",
        "💡 **Next Steps:**",
        "1. Fix the CRITICAL items above first — they carry the biggest risk",
        "2. Schedule time to fix HIGH items this week",
        "3. Rescan after fixing: just say `scan " + target + "` again",
        "\n❓ Have questions about any of these? Just ask me!",
    ]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
#  CORE MESSAGE PROCESSOR
# ══════════════════════════════════════════════════════════════════
async def process(msg: str, session: dict) -> str:
    msg = msg.strip()
    ml  = msg.lower()
    state = session.get("state", "idle")

    # ── Walkthrough navigation ───────────────────────────────────
    if state == "walkthrough":
        vuln_list = session.get("vuln_list", [])
        idx       = session.get("vuln_index", 0)
        total     = len(vuln_list)

        if RE_DONE.search(ml) or RE_NO.fullmatch(ml.strip()):
            session["state"] = "idle"
            return format_summary(vuln_list, session.get("target", "your server"))

        if RE_NEXT.search(ml) or RE_YES.fullmatch(ml.strip()):
            next_idx = idx + 1
            if next_idx >= total:
                session["state"] = "idle"
                return format_summary(vuln_list, session.get("target", "your server"))
            session["vuln_index"] = next_idx
            return format_vuln_card(vuln_list[next_idx], next_idx + 1, total)

        if RE_SKIP.search(ml):
            next_idx = idx + 1
            if next_idx >= total:
                session["state"] = "idle"
                return format_summary(vuln_list, session.get("target", "your server"))
            session["vuln_index"] = next_idx
            return format_vuln_card(vuln_list[next_idx], next_idx + 1, total)

        if RE_FIX.search(ml):
            if idx < total:
                v = vuln_list[idx]
                return (f"🔧 **Fix guide for {v['plain_name']}:**\n\n" +
                        "\n".join(f"**Step {i}:** {s}" for i, s in enumerate(v["fix_steps"], 1)) +
                        f"\n\n⏱️ Time needed: ~{v.get('time_to_fix','varies')}" +
                        "\n\nSay **next** when ready to continue.")

        if RE_EXPLAIN.search(ml) and idx < total:
            v = vuln_list[idx]
            g = ask_gemini(f"Explain '{v['plain_name']}' to a complete beginner. Real-world analogy, what hackers actually do, why it matters. Under 150 words. Friendly tone.")
            if g:
                return g + "\n\n---\nSay **next** to move on, or **fix** to see the fix guide."

        # General question during walkthrough — Gemini + hint to continue
        g = ask_gemini(f"Security question: {msg}")
        return (g or "I'm not sure about that — but feel free to ask!") + \
               "\n\n---\n💬 Say **next** to continue the security walkthrough."

    # ── Post-scan state: offer walkthrough or fixes ──────────────
    if state == "scan_done":
        vuln_list = session.get("vuln_list", [])
        if RE_YES.fullmatch(ml.strip()) or "walk" in ml or "yes" in ml:
            if not vuln_list:
                session["state"] = "idle"
                return "🎉 No major problems found! Your server looks solid. Ask me anything else."
            session["state"]     = "walkthrough"
            session["vuln_index"] = 0
            return format_vuln_card(vuln_list[0], 1, len(vuln_list))
        if "fix" in ml or "just show" in ml or "all fixes" in ml:
            session["state"] = "idle"
            return format_summary(vuln_list, session.get("target", "your server"))
        if RE_NO.fullmatch(ml.strip()):
            session["state"] = "idle"
            return "👍 No problem! Say `scan` again anytime, or ask me a security question."

    # ── Offer port scan after quick check ────────────────────────
    if state == "quick_done":
        if RE_YES.fullmatch(ml.strip()) or "scan" in ml or "port" in ml:
            target = session.get("target", "")
            if not target:
                session["state"] = "idle"
                return "What domain should I scan? Example: `scan example.com`"
            return await run_port_scan(target, session)
        if RE_NO.fullmatch(ml.strip()):
            session["state"] = "idle"
            return "👍 Alright. I've noted the initial findings. Ask me anything!"

    # ── Extract target ────────────────────────────────────────────
    found = extract_target(msg)
    if found:
        session["target"] = found
    target = session.get("target", "")

    # ── Scan intent ───────────────────────────────────────────────
    if RE_SCAN.search(ml):
        if target:
            return await run_quick_scan(target, session)
        return "🔍 Which website or server should I scan? For example: `scan example.com`"

    # ── Web vuln intent ───────────────────────────────────────────
    if RE_WEB.search(ml):
        if target:
            return await run_web_scan(target, session)
        return "🕷️ Which URL should I test for web vulnerabilities? E.g. `check XSS on example.com`"

    # ── SSL intent ────────────────────────────────────────────────
    if RE_SSL.search(ml):
        if target:
            return await do_ssl_only(target)
        return "🔒 Which domain should I check? E.g. `check ssl for example.com`"

    # ── Headers intent ────────────────────────────────────────────
    if RE_HEADER.search(ml):
        if target:
            return await do_headers_only(target)
        return "🛡️ Which domain? E.g. `check headers for example.com`"

    # ── Explain intent ────────────────────────────────────────────
    if RE_EXPLAIN.search(ml):
        concept = re.sub(r'\b(what is|explain|define|tell me about)\b', '', ml, flags=re.I).strip()
        g = ask_gemini(f"Explain '{concept}' in cybersecurity for a complete beginner. Simple language, real-world analogy, severity level, 3 prevention steps. Under 200 words.")
        return g or "Ask me about: SQL injection, XSS, IDOR, firewalls, SSL, or any security topic!"

    # ── Fix intent ────────────────────────────────────────────────
    if RE_FIX.search(ml):
        from danishrecon_bridge import BEGINNER as BEG
        for svc, beg in BEG.items():
            if svc in ml:
                steps = "\n".join(f"**Step {i}:** {s}" for i, s in enumerate(beg["fix_steps"], 1))
                return f"🔧 **How to fix {beg['plain_name']}:**\n\n{steps}\n\n⏱️ Time: ~{beg.get('time_to_fix','varies')}"

    # ── No target yet ─────────────────────────────────────────────
    if not target:
        return (
            "👋 Hi! I'm **Scout** — your personal security guide.\n\n"
            "I'll scan your website or server and explain every vulnerability in **plain English**, "
            "with step-by-step guides to fix each one — no technical knowledge needed!\n\n"
            "**Just tell me your website or server:**\n"
            "• `scan mywebsite.com`\n"
            "• `is example.com safe?`\n"
            "• `check my server at 192.168.1.1`\n\n"
            "Or ask me a security question — I'll explain everything in simple terms. 😊"
        )

    # ── Gemini fallback ───────────────────────────────────────────
    g = ask_gemini(f"User asked: {msg}. Current target: {target or 'none'}")
    return g or ("I'm not sure what you're asking. Try:\n"
                 "• `scan example.com`\n• `what is XSS?`\n• `how do I fix FTP?`")


# ══════════════════════════════════════════════════════════════════
#  SCAN HANDLERS
# ══════════════════════════════════════════════════════════════════
async def run_quick_scan(target: str, session: dict) -> str:
    """Phase 1: Fast DNS + SSL + Headers check (~5-8s)."""
    try:
        import socket
        socket.gethostbyname(target)
    except Exception:
        return f"❌ Can't find **{target}** — check the spelling and try again."

    lines = [f"🔍 Running initial security check on **{target}**...\n_(This takes ~5 seconds — checking DNS, SSL, and security headers)_\n"]

    if not BRIDGE_AVAILABLE:
        return "⚠️ DanishRecon bridge not available. Run: `pip install -r requirements.txt`"

    quick_data = await quick_check(target)
    session["quick_data"] = quick_data

    issues_found = []

    # SSL summary
    ssl_d = quick_data.get("ssl", {})
    if ssl_d.get("valid"):
        days = ssl_d.get("days_left", -1)
        if days < 30:
            issues_found.append(f"⚠️ SSL expires in {days} days")
        else:
            lines.append(f"✅ **SSL Certificate:** Valid ({days} days left, {ssl_d.get('tls_version','')})")
    else:
        issues_found.append("🔴 SSL certificate is broken/invalid")

    # DNS summary
    for issue in quick_data.get("dns", {}).get("issues", []):
        if "SPF" in issue:
            issues_found.append("⚠️ No SPF — email spoofing possible")
        elif "DMARC" in issue:
            issues_found.append("⚠️ No DMARC — phishing risk")

    # Headers summary
    missing_h = quick_data.get("headers", {}).get("missing", [])
    if missing_h:
        issues_found.append(f"⚠️ {len(missing_h)} security headers missing")
    elif not quick_data.get("headers", {}).get("error"):
        lines.append(f"✅ **Security Headers:** {6 - len(missing_h)}/6 configured")

    if issues_found:
        lines.append("**Initial findings:**")
        for iss in issues_found:
            lines.append(f"  {iss}")

    lines.append("\n---")
    lines.append("🔎 **Want me to do a full port scan?** (~30 seconds)")
    lines.append("This checks for dangerous open ports like FTP, RDP, MySQL and looks up known exploits.\n")
    lines.append("@@BUTTONS:Yes, scan all ports|Skip port scan|Just show my report")

    session["state"] = "quick_done"
    return "\n".join(lines)


async def run_port_scan(target: str, session: dict) -> str:
    """Phase 2: Port scan with CVE enrichment."""
    quick_data = session.get("quick_data", {})

    lines = [f"🔬 **Running full port scan on {target}...**\n_(This takes 30–60 seconds — be patient!)_\n"]

    port_data = await port_scan_deep(target)
    session["port_data"] = port_data

    ports = port_data.get("ports", [])
    errors = port_data.get("errors", [])

    if "nmap_not_found" in errors:
        lines.append("⚠️ **nmap is not installed** — I can still check web vulnerabilities.")
        lines.append("Install nmap for full scanning: https://nmap.org/download.html")
    elif "timeout" in errors:
        lines.append("⏱️ Port scan timed out — the host may be behind a firewall (often a good sign!).")
    elif ports:
        lines.append(f"📡 Found **{len(ports)} open port(s)**:\n")
        for p in ports[:8]:
            cve_str = ""
            if p.get("cves"):
                top = p["cves"][0]
                cve_str = f" — @@CVE:{top['cve']}:{top['cvss']}"
            lines.append(f"  {p['emoji']} Port **{p['port']}** — {p['service'].upper()} ({p['risk']}){cve_str}")
    else:
        lines.append("✅ No open ports detected — host appears well-protected or behind a firewall.")

    # Build full vuln list with all data so far
    web_data = session.get("web_data", {})
    vuln_list = build_vuln_list(quick_data, port_data, web_data)
    session["vuln_list"] = vuln_list

    overview = format_overview(target, quick_data, port_data, web_data, vuln_list)
    session["state"] = "scan_done"
    return "\n".join(lines) + "\n\n" + overview


async def run_web_scan(target: str, session: dict) -> str:
    """Phase 3: Web vulnerability scan."""
    lines = [f"🕷️ **Scanning {target} for web vulnerabilities...**\n_(XSS, SQL Injection, IDOR — ~30 seconds)_\n"]

    if not BRIDGE_AVAILABLE:
        return "⚠️ Web scanner unavailable. Check requirements."

    web_data = await web_vuln_scan(target)
    session["web_data"] = web_data

    wv = web_data.get("web_vulns", {})
    found_any = False
    for vtype, label in [("xss","XSS"), ("sqli","SQL Injection"), ("idor","IDOR")]:
        if wv.get(vtype):
            found_any = True
            lines.append(f"🔴 **{label}:** {len(wv[vtype])} issue(s) found!")
    if not found_any:
        lines.append("✅ No obvious XSS, SQLi, or IDOR vulnerabilities found.")
        lines.append("_(Note: automated scans can't catch everything — consider a manual review too)_")

    # Rebuild vuln list with web data
    quick_data = session.get("quick_data", {})
    port_data  = session.get("port_data", {})
    vuln_list  = build_vuln_list(quick_data, port_data, web_data)
    session["vuln_list"] = vuln_list
    session["state"]     = "scan_done"

    overview = format_overview(target, quick_data, port_data, web_data, vuln_list)
    return "\n".join(lines) + "\n\n" + overview


async def do_ssl_only(target: str) -> str:
    from danishrecon_bridge import ssl_check as dr_ssl
    r = dr_ssl(target)
    if not r.get("valid"):
        return (f"❌ **SSL Problem on {target}!**\n\n"
                f"> {r.get('error','')}\n\n"
                "**What this means:** Every visitor sees a scary red browser warning.\n\n"
                "**Free fix:**\n"
                "1. `sudo apt install certbot python3-certbot-nginx`\n"
                "2. `sudo certbot --nginx -d yourdomain.com`\n"
                "3. Done ✅ — auto-renewal is configured automatically")
    days = r.get("days_left", -1)
    grade = "🟢 A" if days > 60 else "🟡 B" if days > 30 else "🟠 C"
    return (f"🔐 **SSL Check: {target}**\n\n"
            f"**Grade:** {grade}\n"
            f"{'✅' if days > 30 else '⚠️'} Certificate expires in **{days} days**\n"
            f"✅ TLS Version: **{r.get('tls_version','')}**\n"
            f"🔒 Cipher: `{r.get('cipher','')[:40]}`\n"
            f"📋 Issued by: **{r.get('issuer','')}**")


async def do_headers_only(target: str) -> str:
    from danishrecon_bridge import header_check as dr_hdr
    r = dr_hdr(target)
    if "error" in r:
        return f"⚠️ Couldn't check headers: {r['error']}"
    lines = [f"🛡️ **Security Headers: {target}**\n"]
    for h in r.get("present", []):
        lines.append(f"✅ {h}")
    for h in r.get("missing", []):
        lines.append(f"❌ **{h}** — Missing!")
    if r.get("missing"):
        lines.append("\n**Quick fix (nginx):**\n```")
        hdr_fixes = {
            "X-Frame-Options": 'add_header X-Frame-Options "SAMEORIGIN";',
            "X-Content-Type-Options": 'add_header X-Content-Type-Options "nosniff";',
            "Strict-Transport-Security": 'add_header Strict-Transport-Security "max-age=31536000";',
            "Referrer-Policy": 'add_header Referrer-Policy "strict-origin-when-cross-origin";',
        }
        for h in r.get("missing", []):
            if h in hdr_fixes:
                lines.append(hdr_fixes[h])
        lines.append("```\nThen: `sudo nginx -t && sudo systemctl reload nginx`")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════
#  API ENDPOINTS
# ══════════════════════════════════════════════════════════════════
@app.post("/chat")
async def chat(req_body: ChatReq):
    session = sessions.setdefault(req_body.session_id, {
        "target": None, "state": "idle",
        "quick_data": {}, "port_data": {}, "web_data": {},
        "vuln_list": [], "vuln_index": 0,
    })
    reply = await process(req_body.message, session)
    return {"reply": reply}


@app.get("/health")
async def health():
    return {"status": "ok", "gemini": bool(gemini_model), "danishrecon": BRIDGE_AVAILABLE}


@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "index.html")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*55)
    print("  🤖 Scout Security Chatbot + DanishRecon Engine")
    print("  Open → http://localhost:8765")
    print("="*55 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8765)

# Gemini API Integration Setup Guide

## Quick Start (2 minutes)

### 1. Get Your Free API Key
1. Go to [https://ai.google.dev/](https://ai.google.dev/)
2. Click **"Get API Key"** (top right)
3. Sign in with your Google account
4. Click **"Create API Key"** (or use existing project)
5. Copy the generated API key

### 2. Add API Key to Project
**Option A: Using `.env` file (Recommended - Secure)**
```bash
# Copy the template
cp .env.example .env

# Edit .env and replace YOUR_API_KEY_HERE with your actual key
GEMINI_API_KEY=your_actual_api_key_here
```

**Option B: Using Environment Variable (Windows)**
```powershell
# In PowerShell:
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

**Option C: Using Environment Variable (Linux/Mac)**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python gemini_analyzer.py
```

You should see:
```
============================================================
GEMINI API INTEGRATION STATUS
============================================================
Enabled: True
API Key Configured: True
Error: None
Cached Analyses: 0
============================================================
```

---

## How It Works

### Integration Points
The Gemini analyzer is integrated into your scanning pipeline:

1. **After scan completes** → Gemini analyzes all vulnerabilities
2. **Per-vulnerability** → Generates human-readable explanation
3. **Executive summary** → One comprehensive overview of all findings

### What Gets Analyzed?
- Service name and version
- CVE IDs
- CVSS scores
- Severity levels
- Available exploits
- Remediation advice

### Output Locations
- **HTML Reports** → "AI-Powered Analysis" section with explanations
- **JSON Export** → `gemini_analysis` key with all explanations
- **Console** → Real-time analysis progress updates

---

## Features

### 1. Caching (Optional but Recommended)
- Analyzes are cached locally in `.gemini_cache/` folder
- Same vulnerability analyzed again? Takes <1ms instead of 10 seconds
- Saves API quota and improves performance

### 2. Error Handling
- API fails? → Falls back to raw vulnerability data (still scannable)
- Rate limit hit? → Gracefully queues remaining analyses
- Invalid key? → Shows clear error message, doesn't crash app

### 3. Rate Limiting
- Free tier: 15 requests/minute
- Monthly quota: ~1,000,000 tokens
- **For hackathon demo:** Safe limit is ~100 vulnerabilities/month

---

## API Pricing (FYI)

| Tier | Cost | Rate Limit | Monthly Quota |
|------|------|-----------|--------------|
| **Free** | $0 | 15 req/min | ~1M tokens |
| **Standard** | $0.075/1M tokens | 1000 req/min | Unlimited |

**Hackathon use:** Free tier is **completely sufficient**. Zero charges.

---

## Troubleshooting

### "GEMINI_API_KEY not set"
✗ Solution: You haven't added the API key to `.env` or environment
1. Create `.env` file in project root
2. Add: `GEMINI_API_KEY=your_key_here`
3. Save and run again

### "Failed to initialize Gemini API: Invalid API key"
✗ Solution: Your API key is incorrect or revoked
1. Go to [https://ai.google.dev/](https://ai.google.dev/)
2. Check if key is still valid
3. Regenerate new key if needed
4. Update `.env` with new key

### "google-genai not installed"
✗ Solution: Missing dependency
```bash
pip install google-genai python-dotenv
```

### Rate limit errors (15 requests/minute)
✗ Solution: Too many simultaneous analyses
- Caching is enabled (will help on second run)
- Wait 1 minute before next scan
- For production: Upgrade to paid tier

---

## Usage in Code

### Basic Usage
```python
from gemini_analyzer import GeminiAnalyzer

analyzer = GeminiAnalyzer()

# Analyze single vulnerability
vuln = {
    'service': 'SSH',
    'version': '7.4p1',
    'cve': 'CVE-2019-16509',
    'severity': 'CRITICAL',
    'description': '...'
}

explanation = analyzer.analyze_vulnerability(vuln)
print(explanation)
```

### Full Scan Analysis
```python
# After completing scan in Cyber_recon_pro.py
if analyzer.enabled:
    analyses = analyzer.analyze_scan_results(scan_data)
    # analyses = {vuln_id: explanation, ...}
```

### Disable Gemini (Optional)
In `.env`:
```
ENABLE_GEMINI_ANALYSIS=false
```

---

## For Hackathon Demo

### Before Demo
1. ✅ Test with sample scan (2 minutes)
2. ✅ Verify API key works
3. ✅ Cache results for demo targets
4. ✅ Have backup API key ready (use different Gmail if needed)

### During Demo
- If API is slow → Explain judges about caching
- If API fails → Show raw vulnerability data (still impressive)
- Show cache folder (proves it's working)

### Pro Tips
- Analyze a small target (~5-10 vulns) in 30 seconds
- For larger targets, analyze in background while judges look at other sections
- Highlight the "AI-Powered Analysis" section in HTML report

---

## Questions?

- **Gemini API Docs:** [https://ai.google.dev/docs](https://ai.google.dev/docs)
- **Pricing Details:** [https://ai.google.dev/pricing](https://ai.google.dev/pricing)
- **Rate Limits:** Free tier starts at 0.5 RPM, increases with usage history

**Happy hacking!** 🚀

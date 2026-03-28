# Gemini API Quota Management Guide

## Problem Solved

You were hitting the Gemini API free tier quota limits:
- **Per Minute Limit:** 5 requests/minute
- **Per Day Limit:** 20 requests/day

The error `429 RESOURCE_EXHAUSTED` indicates your quota was exceeded.

## Solution Implemented

The `gemini_analyzer.py` has been updated with a comprehensive **QuotaManager** system that:

### 1. **Quota Tracking**
- Tracks requests in real-time (per-minute and per-day windows)
- Persists quota state to `.gemini_quota` file across sessions
- Prevents requests when quota is exceeded

### 2. **Smart Caching**
- All Gemini analyses are cached locally in `.gemini_cache/`
- Cached results are **never charged** against your quota
- Dramatically reduces API calls for repeated scans

### 3. **Graceful Degradation**
- When quota is exhausted:
  - Shows clear warning messages
  - Blocks new API requests
  - Returns `None` instead of failing
  - Continues processing with cached/offline data

### 4. **Better Error Handling**
- Distinguishes between rate limit errors (retriable) and quota errors (not retriable)
- Exponential backoff (2s, 4s, 8s) for rate limit retries
- Extracts and respects "retry-after" delays from API responses

## How to Use

### Check Current Quota Status

```python
from gemini_analyzer import initialize_gemini

analyzer = initialize_gemini()
# Status shows quota usage automatically
```

Output example:
```
GEMINI API INTEGRATION STATUS
============================================================
Enabled: True
API Key Configured: True
Cached Analyses: 15

QUOTA USAGE:
  Per Minute: 2/5 requests
  Per Day: 18/20 requests
  STATUS: ⚠️  QUOTA EXHAUSTED
  Reset in: 0.5 hours
============================================================
```

### Programmatic Quota Check

```python
from gemini_analyzer import GeminiAnalyzer

analyzer = GeminiAnalyzer()

# Check if you can make a request
can_request, wait_time = analyzer.quota_manager.can_make_request()

if can_request:
    print("✅ Request allowed")
else:
    print(f"⏳ Quota exhausted. Wait {wait_time:.0f}s")

# Get detailed quota status
status = analyzer.quota_manager.get_status()
print(f"Daily usage: {status['day_used']}/{status['day_limit']}")
```

## Best Practices to Stay Within Limits

### 1. **Leverage Caching**
- Cache hits don't consume quota ✅
- First scan: uses quota
- Same/similar scans: free from cache
```python
# These are cached if prompt is identical:
analyzer.analyze_vulnerability(vuln1)  # Uses 1 quota
analyzer.analyze_vulnerability(vuln1)  # Uses 0 quota (cached!)
```

### 2. **Run Scans During Day (Not Consecutive)**
With 20 requests/day:
- 1 scan with ~15 vulnerabilities = ~1 request
- Multiple small scans spread throughout day → better distribution

### 3. **Pre-Filter Vulnerabilities**
Only analyze vulnerabilities that need explanation:
```python
# Instead of analyzing ALL vulns:
important_vulns = [v for v in all_vulns if v['cvss_score'] >= 7.0]
for vuln in important_vulns:
    analyzer.analyze_vulnerability(vuln)  # More selective = less quota
```

### 4. **Use Offline Mode When Quota Exhausted**
When API quota is exhausted, the analyzer gracefully falls back:
```python
# These return None if quota exhausted
analysis = analyzer.analyze_vulnerability(vuln)
summary = analyzer.generate_executive_summary(scan_data)

# Use fallback logic:
if analysis is None and quota_exhausted:
    print("Using offline analysis template...")
    analysis = get_template_analysis(vuln)
```

### 5. **Monitor Quota Files**
Check quota state anytime:
```bash
# See current quota state
cat .gemini_quota

# Clear quota tracking (fresh start - use carefully!)
rm .gemini_quota
```

## Upgrade Options

### Option 1: **Upgrade to Paid Plan**
- Higher quotas (thousands of requests/day)
- Same API endpoint
- Most reliable solution

### Option 2: **Use Multiple API Keys**
- Create multiple Google Cloud projects
- Rotate between API keys
- Spreads quota across projects
```python
# Rotate between keys
analyzers = [
    GeminiAnalyzer(api_key=key1),
    GeminiAnalyzer(api_key=key2),
    GeminiAnalyzer(api_key=key3),
]
```

### Option 3: **Batch Analyses**
- Calculate what you MUST analyze with Gemini
- Save rest for batch processing once quota resets
- Use scheduling to spread requests over time

## Files Modified

1. **gemini_analyzer.py**
   - Added `QuotaManager` class
   - Updated `analyze_vulnerability()` with quota checks
   - Updated `generate_executive_summary()` with quota checks
   - Enhanced `get_status()` to show quota info
   - Improved error categorization

2. **New Files Created**
   - `.gemini_quota` - Persists quota state (auto-created)
   - `.gemini_cache/` - Caches analyses (already existed)

## Troubleshooting

### "Quota exhausted. Retry in 45s"
- Wait the specified time before next request
- Check `.gemini_quota` for exact reset time
- Quota automatically resets after 24 hours

### Cache not being used?
- Check `.gemini_cache/` directory exists
- Ensure exact same vulnerability data/prompt
- Different prompts = different cache keys

### API key not recognized in new session?
- Clear `.gemini_quota` to reset tracking
- Verify `GEMINI_API_KEY` in `.env`
- Restart Python interpreter

## API Reference

### QuotaManager Methods

```python
# Check before making request
can_request, wait_seconds = quota_manager.can_make_request()

# Manually record a request (auto-done on success)
quota_manager.record_request()

# Get current status
status = quota_manager.get_status()
# Returns: {
#     'minute_used': 2,
#     'minute_limit': 5,
#     'day_used': 18,
#     'day_limit': 20,
#     'quota_exhausted_until': None or ISO datetime,
#     'quota_reset_in_hours': None or float
# }

# Load/save state
quota_manager.load_state()
quota_manager.save_state()
```

## Summary

✅ **What's Fixed:**
- Requests no longer sent when quota is exhausted
- Quota state persists across sessions
- Clear visibility into quota usage
- Intelligent caching reduces API calls

✅ **What's Improved:**
- Better error messages
- Automatic state persistence
- Rate limit detection and backoff
- Graceful fallback when quota exceeded

**Next Steps:**
1. Test with `python gemini_analyzer.py` to see new quota display
2. Monitor `.gemini_quota` file to track usage
3. Consider upgrading to paid plan for production use
4. Use caching aggressively for repeated scans

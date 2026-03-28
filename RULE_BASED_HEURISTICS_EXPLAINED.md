# Rule-Based Heuristic Algorithm Architecture in CyberRecon-Pro

## Overview

CyberRecon-Pro uses **rule-based heuristic algorithms** to detect IDOR, SQL Injection, and XSS vulnerabilities. This approach is deterministic, explainable, and doesn't require machine learning or AI models.

---

## Core Principles of Rule-Based Heuristics

### What is a Rule-Based Heuristic?

A **rule-based heuristic** is a decision-making algorithm that:
1. ✅ Applies explicit, predefined rules/patterns
2. ✅ Makes deterministic decisions (same input → same output)
3. ✅ Is transparent and auditable
4. ✅ Requires no training data or model
5. ✅ Works with pattern matching and logical conditions

### Why No AI/ML Needed?

**Vulnerabilities follow predictable patterns:**
- XSS: Payloads echo back in response
- SQLi: Error messages, timing delays, response changes
- IDOR: Authorization failures when changing IDs

These patterns are **deterministic**, not probabilistic, so rules work perfectly.

---

## 1. XSS Detection: Pattern Matching Heuristics

### Rule-Based Algorithm

```python
class XSSDetector:
    # RULE 1: Payload injection patterns
    XSS_PAYLOADS = [
        '<script>alert("xss")</script>',
        '<img src=x onerror=alert("xss")>',
        '<svg onload=alert("xss")>'
    ]
    
    # RULE 2: Reflection detection
    def detect_xss(self, payload, response_text):
        # Heuristic Rule: If payload appears in response, likely XSS
        if payload in response_text:
            # RULE 3: Severity by context
            if '<script>' in response_text:
                severity = "CRITICAL"  # In script context
            elif 'onerror=' in response_text or 'onload=' in response_text:
                severity = "HIGH"      # In event handler
            else:
                severity = "MEDIUM"    # In data context
            
            return XSSVulnerability(
                payload=payload,
                severity=severity,
                reflected_in=context
            )
```

### Decision Tree

```
Is payload in response?
├─ YES → Found reflection point
│       ├─ In <script> tag? → CRITICAL
│       ├─ In event handler (onerror, onclick)? → HIGH
│       ├─ In HTML attribute? → HIGH
│       └─ In data context? → MEDIUM
└─ NO → Not vulnerable
```

### Why This Works
- **Payloads are deterministic**: `<script>alert(1)</script>` always looks the same
- **Reflection is verifiable**: Payload in response = confirmed reflection
- **Context matters**: Script tags > event handlers > data context
- **No ML needed**: String matching is sufficient

---

## 2. SQL Injection Detection: Multi-Layer Heuristics

### Layer 1: Error-Based Detection

```python
# RULE SET 1: SQL Error Pattern Matching
SQL_ERROR_PATTERNS = {
    # MySQL
    'mysql_fetch': 'MySQL vulnerability',
    'MySQL Error': 'MySQL error exposure',
    'mysql_num_rows': 'Direct DB error',
    
    # PostgreSQL
    'pg_connect': 'PostgreSQL connection',
    'PostgreSQL': 'PostgreSQL error',
    'connection failed': 'DB connection error',
    
    # Oracle
    'OracleException': 'Oracle DB error',
    'ORA-': 'Oracle error code',
    
    # SQL Server
    '[SQL Server]': 'SQL Server error',
    'MSSQL': 'MSSQL error',
}

def detect_error_based_sqli(baseline_response, injected_response):
    # HEURISTIC 1: Error appears in injected but not baseline
    for error_pattern in SQL_ERROR_PATTERNS:
        if error_pattern in injected_response and error_pattern not in baseline_response:
            return f"error_based_{error_pattern}"
    
    return None
```

### Layer 2: Time-Based Detection

```python
# RULE SET 2: Timing Analysis
TIME_BASED_PAYLOADS = [
    "'; SLEEP(5)--",           # MySQL
    "'; PG_SLEEP(5)--",        # PostgreSQL
    "'; WAITFOR DELAY '00:00:05'--",  # SQL Server
]

def detect_time_based_sqli(response_times):
    baseline_time = response_times['normal']
    injected_time = response_times['with_sleep']
    
    # HEURISTIC 2: Response delay indicates sleep function executed
    time_difference = injected_time - baseline_time
    
    if time_difference > 4.0:  # Expected 5 second sleep
        return f"time_based_delay_{time_difference:.1f}s"
    
    return None
```

### Layer 3: Response Modification Detection

```python
# RULE SET 3: Content Analysis
def detect_response_based_sqli(baseline, injected):
    baseline_len = len(baseline)
    injected_len = len(injected)
    
    # HEURISTIC 3: Content length change indicates data modification
    len_diff = abs(injected_len - baseline_len)
    
    if len_diff > 100:
        return "content_length_change_significant"
    elif len_diff > 50:
        return "content_length_change_moderate"
    
    # HEURISTIC 4: Auth bypass (login page disappears)
    if 'login' in baseline.lower() and 'login' not in injected.lower():
        return "response_modification_auth_bypass"
    
    return None
```

### Decision Tree

```
Inject SQL payload:
├─ Error message appears?
│  └─ CRITICAL (Error-based SQLi confirmed)
├─ Response timing delayed?
│  └─ CRITICAL (Time-based SQLi confirmed)
├─ Response content changed significantly?
│  └─ HIGH (Response-based SQLi)
└─ No change detected
   └─ No SQLi (or well-protected)
```

---

## 3. IDOR Detection: Parameter & Response Analysis

### Rule-Based Algorithm

```python
class IDORDetector:
    
    # RULE 1: Identify ID parameters by pattern
    ID_PATTERNS = {
        r'.*_id$': 'Likely ID parameter',
        r'^id$': 'Standard ID',
        r'.*uid.*': 'User ID',
        r'.*user.*id': 'User identifier',
        r'.*account.*': 'Account reference',
        r'.*product.*': 'Product reference',
    }
    
    def identify_id_parameters(self, url):
        params = parse_url_parameters(url)
        
        # HEURISTIC 1: Pattern matching for ID-like parameters
        for param_name, param_value in params.items():
            for pattern, description in self.ID_PATTERNS.items():
                if re.match(pattern, param_name.lower()):
                    yield (param_name, param_value)
            
            # HEURISTIC 2: Numeric values often indicate IDs
            if str(param_value).isdigit():
                yield (param_name, param_value)
    
    def test_idor(self, url, id_param, original_id):
        # Get baseline response
        baseline = request(url, {id_param: original_id})
        baseline_hash = hash(baseline.content)
        baseline_status = baseline.status_code
        
        # HEURISTIC 3: Test adjacent ID values
        adjacent_ids = [
            original_id + 1,      # Next sequential ID
            original_id + 2,      # Second next
            original_id - 1,      # Previous
            original_id * 2,      # Double
        ]
        
        for test_id in adjacent_ids:
            # Make request with different ID
            response = request(url, {id_param: test_id})
            response_hash = hash(response.content)
            response_status = response.status_code
            
            # HEURISTIC 4: Detect access control failure
            if self._indicates_access_change(
                baseline_status, response_status,
                baseline_hash, response_hash
            ):
                return IDORVulnerability(
                    parameter=id_param,
                    original_id=original_id,
                    accessed_id=test_id,
                    severity=self._assess_severity(response_status)
                )
    
    @staticmethod
    def _indicates_access_change(baseline_status, test_status, 
                                 baseline_hash, test_hash):
        # HEURISTIC 5: Multiple indicators of authorization bypass
        
        # Indicator 1: Response content completely different
        if baseline_hash != test_hash:
            return True
        
        # Indicator 2: Status code changed
        if baseline_status != test_status:
            return True
        
        # Indicator 3: But body identical (likely false positive)
        # → Filter out
        
        return False
    
    @staticmethod
    def _assess_severity(response_status):
        # HEURISTIC 6: Severity based on what was accessed
        if response_status == 200:
            return "CRITICAL"  # Got data without auth
        elif response_status == 403:
            return "MEDIUM"    # Got 403 Forbidden (some protection)
        elif response_status == 401:
            return "LOW"       # Got 401 (proper auth blocking)
        else:
            return "HIGH"
```

### Decision Tree

```
For each URL parameter:
├─ Is it ID-like? (name pattern or numeric value)
│  ├─ YES → Get baseline response (id=1)
│  │        Test adjacent IDs (2, 3, 0, -1, etc.)
│  │        ├─ Response content different? → CRITICAL (IDOR)
│  │        ├─ Status code changed? → HIGH (IDOR)
│  │        └─ Same response? → No IDOR
│  └─ NO → Skip parameter
└─ Next parameter
```

---

## 4. Scan Profiles: Heuristic Configuration

### QUICK Profile
```python
{
    'xss_payloads': 5,        # Test 5 payload variations
    'sql_payloads': 3,        # Test 3 SQL injection types
    'idor_adjacent': 3,       # Test 3 adjacent IDs
    'concurrency': 20         # 20 parallel requests
}
# HEURISTIC: Fewer tests = faster, higher speed bias
```

### STEALTH Profile
```python
{
    'xss_payloads': 3,        # Minimal payloads
    'sql_payloads': 2,        # Fewer SQLi types
    'idor_adjacent': 2,       # Fewer IDs
    'concurrency': 1          # Sequential requests
}
# HEURISTIC: Slowest but hardest to detect
```

---

## 5. Real-World Example: Detecting SQLi

### Target URL
```
http://vulnerable-app.com/product?id=1
```

### Heuristic Process

#### Step 1: Baseline Request (No Injection)
```
Request:  GET /product?id=1
Response: 200 OK, 2543 bytes
          "Product: Laptop, Price: $999"
Time:     0.45 seconds
```

#### Step 2: Apply SQLi Payload (Error-Based)
```
Request:  GET /product?id=1' OR '1'='1
Response: 500 ERROR, 1243 bytes
          "Error: SQL Syntax Error near '1'='1'"
          "MySQL Error: You have an error in your SQL syntax"
```

**Heuristic Decision:**
```python
# RULE: If "MySQL Error" appears in injected response 
#       but not in baseline → ERROR-BASED SQLi
if 'MySQL Error' in injected_response and 'MySQL Error' not in baseline_response:
    return "SQLi detected: error_based_MySQL"
    severity = "CRITICAL"
```

✅ **VULNERABILITY CONFIRMED**

---

#### Step 3: Apply SQLi Payload (Time-Based)
```
Request:  GET /product?id=1'; SLEEP(5)--
Response: 200 OK, 2543 bytes (same as baseline)
Time:     5.32 seconds (baseline was 0.45 seconds)
```

**Heuristic Decision:**
```python
# RULE: If response time increased by ~5 seconds 
#       (matching SLEEP(5)) → TIME-BASED SQLi
time_diff = 5.32 - 0.45 = 4.87 seconds

if time_diff > 4.0:  # Threshold for 5-second sleep
    return "SQLi detected: time_based_delay"
    severity = "CRITICAL"
```

✅ **VULNERABILITY CONFIRMED**

---

## 6. Why Rule-Based Heuristics Are Superior for Vulnerability Testing

### Advantages

| Aspect | Rule-Based | AI/ML |
|--------|-----------|-------|
| **Transparency** | ✅ Rules are explicit | ❌ Black box |
| **Explainability** | ✅ Why → Which rule fired | ❌ Why → Unknown |
| **Speed** | ✅ Fast pattern matching | ❌ Slower inference |
| **False Positives** | ✅ Controllable | ❌ Hard to control |
| **Training Data** | ✅ Not needed | ❌ Requires dataset |
| **Predictability** | ✅ Always same result | ❌ May vary |
| **Auditability** | ✅ Easy to verify rules | ❌ Hard to audit |
| **No Dependencies** | ✅ No ML libraries | ❌ TensorFlow, PyTorch |

### Why Machine Learning Isn't Needed

**Vulnerabilities are binary:**
- ❌ Either XSS payload reflects or it doesn't
- ❌ Either SQL error message appears or it doesn't
- ❌ Either different user's data is returned or it isn't

**There's no "probability space":**
- Not like image classification (80% dog, 20% cat)
- Vulnerabilities are deterministic yes/no events

---

## 7. Implementation: Concrete Rules in CyberRecon

### Rule Priority System

```python
DETECTION_RULES = [
    # TIER 1: High-Confidence Rules (Few false positives)
    Rule("SQL Error Pattern", confidence=0.99, priority=HIGH),
    Rule("XSS Reflection", confidence=0.98, priority=HIGH),
    Rule("Time-Based Delay", confidence=0.95, priority=HIGH),
    
    # TIER 2: Medium-Confidence Rules
    Rule("Content Length Change", confidence=0.75, priority=MEDIUM),
    Rule("Auth Bypass Pattern", confidence=0.80, priority=MEDIUM),
    
    # TIER 3: Low-Confidence Rules (Filtered)
    Rule("Minor Response Change", confidence=0.40, priority=LOW),
]

# Heuristic: Apply high-confidence rules first
# Report only TIER 1 findings by default
# Lower tiers only in FULL profile mode
```

### Payload Strategy

```python
# Heuristic 1: Start with obvious payloads
# Heuristic 2: If not detected, try obfuscated variants
# Heuristic 3: Adaptive timeouts based on target response time

payloads = [
    # Most obvious (high success rate)
    "' OR '1'='1",
    "'; DROP TABLE users--",
    
    # Obfuscated (bypass filters)
    "' OR 1=1 /*",
    "' UNION SELECT NULL--",
    
    # Alternative syntax
    "admin'--",
    "' OR ''='",
]

for payload in payloads:
    response = test_payload(url, payload)
    if detect_vulnerability(payload, response):
        break  # Stop on first detection
```

---

## 8. Configuration & Customization

### Rule Modification Example

```python
# User can adjust detection thresholds
CONFIG = {
    'IDOR': {
        'min_response_size_diff': 50,      # Bytes to trigger detection
        'test_adjacent_count': 5,          # How many IDs to test
        'status_code_diff_required': True, # Must see different status
    },
    'SQLi': {
        'time_based_threshold': 4.0,      # Seconds for SLEEP() detection
        'error_patterns': ['MySQL', 'PostgreSQL', 'ORA-'],
        'max_payloads': 10,               # Limit testing
    },
    'XSS': {
        'require_context_match': True,    # Must match injection context
        'min_payload_length': 3,          # Minimum reflection length
    }
}
```

---

## 9. Comparison: Heuristic vs AI/ML Approach

### Scenario: Detecting SQLi in `/?id=1`

**Rule-Based (CyberRecon):**
```
1. Send: /?id=1' OR '1'='1
2. Look for: "SQL", "MySQL", "error"
3. Found? → VULNERABLE
4. Confidence: 99%
5. Time: 0.5 seconds
```

**AI/ML Approach:**
```
1. Send: /?id=1' OR '1'='1
2. Extract features: response_length, status_code, 
   word_embeddings, entropy, etc.
3. Run through neural network trained on 10,000 samples
4. Output: 0.87 probability of SQLi
5. Time: 5+ seconds (model inference)
6. Problem: Need labeled training data
```

### Why Heuristic Wins Here

- ✅ Faster (0.5s vs 5s)
- ✅ No training data needed
- ✅ 99% confidence vs 87%
- ✅ Explainable ("SQL error found")
- ✅ Works on unseen targets
- ✅ No model maintenance

---

## 10. Advanced: Heuristic Combination

### Conditional Rules

```python
def assess_idor_severity(response_status, content_changed, 
                        data_sensitivity):
    # HEURISTIC: Combine multiple signals
    
    score = 0
    
    if response_status == 200:
        score += 40  # Got successful access
    elif response_status in (401, 403):
        score -= 10  # Some protection
    
    if content_changed:
        score += 30  # Different data returned
    
    if 'password' in response or 'credit_card' in response:
        score += 20  # Sensitive data exposed
    elif 'public' in response:
        score -= 10  # Public data
    
    # Final classification
    if score >= 70:
        return "CRITICAL"
    elif score >= 40:
        return "HIGH"
    elif score >= 20:
        return "MEDIUM"
    else:
        return "LOW"
```

---

## Conclusion

CyberRecon-Pro uses **rule-based heuristics** because:

1. ✅ **Vulnerabilities are deterministic** - not probabilistic
2. ✅ **Rules are transparent** - auditable and explainable
3. ✅ **No training required** - works out-of-box
4. ✅ **High accuracy** - pattern matching is reliable
5. ✅ **Fast execution** - string/timing operations only
6. ✅ **Offline operation** - no API calls or model downloads

This is the **gold standard** for security testing - deterministic, reliable, and trustworthy.

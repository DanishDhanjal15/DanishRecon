#!/usr/bin/env python3
"""
Gemini API Integration for CyberRecon-Pro
Analyzes scan results and generates AI-powered vulnerability explanations
"""

import os
import json
import hashlib
import logging
import time
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import threading

# Load environment variables from workspace root (.env should be there)
try:
    from dotenv import load_dotenv
    # gemini_analyzer.py is in workspace root, so .env is in same directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

try:
    import google.genai as genai
    from google.genai.types import GenerateContentConfig
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuotaManager:
    """Tracks and enforces API quota limits to prevent excessive requests"""
    
    # Free tier limits
    REQUESTS_PER_MINUTE = 5
    REQUESTS_PER_DAY = 20
    
    def __init__(self, state_file: str = '.gemini_quota'):
        """
        Initialize quota manager with persistent state
        
        Args:
            state_file: File to persist quota state across sessions
        """
        self.state_file = state_file
        self.lock = threading.Lock()
        self.minute_requests = deque()  # (timestamp) tuples
        self.daily_requests = deque()   # (timestamp) tuples
        self.quota_exhausted_until = None
        self.load_state()
    
    def load_state(self):
        """Load saved quota state from previous sessions"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.quota_exhausted_until = state.get('quota_exhausted_until')
                    logger.info(f"Loaded quota state from {self.state_file}")
        except Exception as e:
            logger.warning(f"Could not load quota state: {e}")
    
    def save_state(self):
        """Save quota state for persistence across sessions"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'quota_exhausted_until': self.quota_exhausted_until,
                    'last_updated': datetime.now().isoformat()
                }, f)
        except Exception as e:
            logger.warning(f"Could not save quota state: {e}")
    
    def _cleanup_old_requests(self):
        """Remove requests older than the tracking windows"""
        now = time.time()
        
        # Clean minute window (keep last 60 seconds)
        while self.minute_requests and (now - self.minute_requests[0]) > 60:
            self.minute_requests.popleft()
        
        # Clean day window (keep last 24 hours)
        while self.daily_requests and (now - self.daily_requests[0]) > 86400:
            self.daily_requests.popleft()
    
    def can_make_request(self) -> Tuple[bool, Optional[float]]:
        """
        Check if a request can be made within quota limits
        
        Returns:
            (can_request: bool, wait_seconds: Optional[float])
            - can_request: True if request can be made immediately
            - wait_seconds: Seconds to wait if quota exceeded (None if can request)
        """
        with self.lock:
            self._cleanup_old_requests()
            
            # Check if quota was exhausted - respect the retry-after delay
            if self.quota_exhausted_until:
                if datetime.fromisoformat(self.quota_exhausted_until) > datetime.now():
                    wait_time = (datetime.fromisoformat(self.quota_exhausted_until) - datetime.now()).total_seconds()
                    return False, wait_time
                else:
                    self.quota_exhausted_until = None
                    self.save_state()
            
            # Check per-minute limit
            if len(self.minute_requests) >= self.REQUESTS_PER_MINUTE:
                wait_time = 60 - (time.time() - self.minute_requests[0])
                return False, max(0.1, wait_time)
            
            # Check per-day limit
            if len(self.daily_requests) >= self.REQUESTS_PER_DAY:
                wait_time = 86400 - (time.time() - self.daily_requests[0])
                logger.error(f"Daily quota exhausted! {self.REQUESTS_PER_DAY} requests used. Wait {wait_time:.0f}s until reset.")
                self.quota_exhausted_until = (datetime.now() + timedelta(seconds=wait_time)).isoformat()
                self.save_state()
                return False, wait_time
            
            return True, None
    
    def record_request(self):
        """Record that a request was made"""
        with self.lock:
            now = time.time()
            self.minute_requests.append(now)
            self.daily_requests.append(now)
            self.save_state()
    
    def get_status(self) -> Dict:
        """Get current quota usage status"""
        with self.lock:
            self._cleanup_old_requests()
            return {
                'minute_used': len(self.minute_requests),
                'minute_limit': self.REQUESTS_PER_MINUTE,
                'day_used': len(self.daily_requests),
                'day_limit': self.REQUESTS_PER_DAY,
                'quota_exhausted_until': self.quota_exhausted_until,
                'quota_reset_in_hours': (datetime.fromisoformat(self.quota_exhausted_until) - datetime.now()).total_seconds() / 3600
                    if self.quota_exhausted_until else None
            }


class GeminiAnalyzer:
    """
    Analyzes security scan results using Google Gemini API
    Provides natural language explanations of vulnerabilities and recommendations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini Analyzer
        
        Args:
            api_key: Google Gemini API key. If None, loads from .env or environment
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model_name = 'gemini-2.5-flash'  # Latest fast, cost-effective model
        self.cache_dir = Path('.gemini_cache')
        self.cache_dir.mkdir(exist_ok=True)
        self.enabled = False
        self.error_message = None
        self.quota_manager = QuotaManager()  # Initialize quota tracking
        
        if not GEMINI_AVAILABLE:
            self.error_message = "google-genai not installed. Install with: pip install google-genai"
            logger.warning(self.error_message)
            return
        
        if not self.api_key:
            self.error_message = "GEMINI_API_KEY not set. Please set it in .env file or environment"
            logger.warning(self.error_message)
            return
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.enabled = True
            logger.info("Gemini API initialized successfully")
        except Exception as e:
            self.error_message = f"Failed to initialize Gemini API: {str(e)}"
            logger.error(self.error_message)
            self.enabled = False
    
    def _get_cache_key(self, content: str) -> str:
        """Generate cache key from content hash"""
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cached_analysis(self, cache_key: str) -> Optional[str]:
        """Retrieve cached analysis if exists"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    return data.get('analysis')
            except Exception as e:
                logger.warning(f"Failed to read cache: {e}")
        return None
    
    def _save_cache(self, cache_key: str, analysis: str) -> None:
        """Save analysis to cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'analysis': analysis,
                    'timestamp': datetime.now().isoformat()
                }, f)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def analyze_vulnerability(self, vuln_data: Dict) -> Optional[str]:
        """
        Analyze a single vulnerability and generate explanation
        With retry logic for rate limit handling and quota enforcement.
        
        Args:
            vuln_data: Dictionary containing vulnerability information
            
        Returns:
            Explanation string or None if analysis fails
        """
        if not self.enabled:
            return None
        
        # Build context from vulnerability data
        prompt = self._build_vulnerability_prompt(vuln_data)
        cache_key = self._get_cache_key(prompt)
        
        # Check cache first (always) - doesn't use quota
        cached = self._get_cached_analysis(cache_key)
        if cached:
            logger.info(f"Using cached analysis for {vuln_data.get('name', 'Unknown')}")
            return cached
        
        # Check quota before making API call
        can_request, wait_time = self.quota_manager.can_make_request()
        if not can_request:
            logger.warning(
                f"Quota limit reached. Cannot analyze {vuln_data.get('name', 'Unknown')}. "
                f"Retry in {wait_time:.0f}s or upgrade API plan."
            )
            return None
        
        # Retry logic with exponential backoff for rate limiting
        max_retries = 3
        base_wait_time = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.3,  # Low temp for consistent, factual responses
                        max_output_tokens=500,  # Concise explanations
                        top_p=0.8,
                        top_k=40
                    )
                )
                
                # Request succeeded - record it
                self.quota_manager.record_request()
                
                analysis = response.text.strip()
                self._save_cache(cache_key, analysis)
                return analysis
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if it's a rate limit or quota error
                is_quota_error = any(keyword in error_str for keyword in [
                    'quota', 'resource exhausted', 'daily', 'per day'
                ])
                is_rate_limit = any(keyword in error_str for keyword in [
                    'rate', 'too many requests', '429', '503', 'throttled'
                ])
                
                if is_quota_error:
                    # Daily quota exhausted - extract retry-after if available
                    logger.error(f"Daily API quota exhausted. {e}")
                    # Try to extract retry-after delay from error message
                    if "retry in" in error_str.lower():
                        match = re.search(r'retry.*?(\d+(?:\.\d+)?)\s*s', error_str, re.IGNORECASE)
                        if match:
                            retry_seconds = float(match.group(1))
                            self.quota_manager.quota_exhausted_until = (
                                datetime.now() + timedelta(seconds=retry_seconds)
                            ).isoformat()
                            self.quota_manager.save_state()
                    return None
                
                elif is_rate_limit and attempt < max_retries - 1:
                    # Exponential backoff: 2s, 4s, 8s
                    wait_time = base_wait_time * (2 ** attempt)
                    logger.warning(
                        f"Rate limited. Retrying in {wait_time}s "
                        f"(attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Gemini analysis failed: {e}")
                    return None
        
        return None
    
    def analyze_scan_results(self, scan_data: Dict) -> Dict[str, Optional[str]]:
        """
        Analyze entire scan results and return explanations for each vulnerability
        
        Args:
            scan_data: Complete scan results dictionary
            
        Returns:
            Dictionary mapping vulnerability IDs to explanations
        """
        if not self.enabled:
            return {}
        
        analyses = {}
        vulns = scan_data.get('vulnerabilities', [])
        
        logger.info(f"Analyzing {len(vulns)} vulnerabilities with Gemini API...")
        
        for i, vuln in enumerate(vulns, 1):
            vuln_id = vuln.get('id', f'vuln_{i}')
            logger.info(f"Analyzing [{i}/{len(vulns)}] {vuln.get('name', 'Unknown')}")
            
            analysis = self.analyze_vulnerability(vuln)
            if analysis:
                analyses[vuln_id] = analysis
        
        logger.info(f"Completed analysis: {len(analyses)}/{len(vulns)} vulnerabilities explained")
        return analyses
    
    def generate_executive_summary(self, scan_data: Dict) -> Optional[str]:
        """
        Generate executive summary of entire scan
        With retry logic for rate limit handling and quota enforcement.
        
        Args:
            scan_data: Complete scan results dictionary
            
        Returns:
            Executive summary or None if analysis fails
        """
        if not self.enabled:
            return None
        
        prompt = self._build_summary_prompt(scan_data)
        cache_key = self._get_cache_key(prompt)
        
        # Check cache
        cached = self._get_cached_analysis(cache_key)
        if cached:
            logger.info("Using cached executive summary")
            return cached
        
        # Check quota before making API call
        can_request, wait_time = self.quota_manager.can_make_request()
        if not can_request:
            logger.warning(
                f"Quota limit reached. Cannot generate executive summary. "
                f"Retry in {wait_time:.0f}s or upgrade API plan."
            )
            return None
        
        # Retry logic with exponential backoff
        max_retries = 3
        base_wait_time = 2
        
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=800,
                        top_p=0.8,
                        top_k=40
                    )
                )
                
                # Request succeeded - record it
                self.quota_manager.record_request()
                
                summary = response.text.strip()
                self._save_cache(cache_key, summary)
                return summary
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Check if it's a rate limit or quota error
                is_quota_error = any(keyword in error_str for keyword in [
                    'quota', 'resource exhausted', 'daily', 'per day'
                ])
                is_rate_limit = any(keyword in error_str for keyword in [
                    'rate', 'too many requests', '429', '503', 'throttled'
                ])
                
                if is_quota_error:
                    logger.error(f"Daily API quota exhausted. {e}")
                    return None
                
                elif is_rate_limit and attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = base_wait_time * (2 ** attempt)
                    logger.warning(
                        f"Rate limited on summary. Retrying in {wait_time}s "
                        f"(attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(wait_time)
                else:
                    logger.error(f"Executive summary generation failed: {e}")
                    return None
        
        return None
    
    @staticmethod
    def _build_vulnerability_prompt(vuln_data: Dict) -> str:
        """Build detailed vulnerability analysis prompt"""
        
        service = vuln_data.get('service', 'Unknown Service')
        version = vuln_data.get('version', 'Unknown Version')
        cve = vuln_data.get('cve', 'N/A')
        cvss = vuln_data.get('cvss_score', 'Unknown')
        description = vuln_data.get('description', 'No description')
        severity = vuln_data.get('severity', 'Unknown')
        exploit_available = vuln_data.get('exploit_available', False)
        
        prompt = f"""
You are a security expert. Analyze and explain this vulnerability in simple, non-technical language for a security team.

**Vulnerability Details:**
- Service: {service} {version}
- CVE: {cve}
- CVSS Score: {cvss}
- Severity: {severity}
- Exploit Available: {'Yes' if exploit_available else 'No'}
- Description: {description}

**Provide:**
1. What is this vulnerability? (2-3 sentences in plain English)
2. Why is it dangerous? (business/operational impact)
3. How to fix it? (specific actionable steps)
4. What's the risk if we don't fix it? (consequences)

Keep explanation concise and avoid technical jargon. Make it understandable for non-security people.
"""
        return prompt.strip()
    
    @staticmethod
    def _build_summary_prompt(scan_data: Dict) -> str:
        """Build executive summary prompt"""
        
        target = scan_data.get('target', 'Unknown Target')
        duration = scan_data.get('duration', 'Unknown')
        total_vulns = len(scan_data.get('vulnerabilities', []))
        
        # Extract risk counts from vulnerabilities (stored as strings like "[CRITICAL] Title" or "[HIGH] Title")
        vulns = scan_data.get('vulnerabilities', [])
        critical = sum(1 for v in vulns if isinstance(v, str) and '[CRITICAL]' in v)
        high = sum(1 for v in vulns if isinstance(v, str) and '[HIGH]' in v)
        medium = sum(1 for v in vulns if isinstance(v, str) and '[MEDIUM]' in v)
        low = sum(1 for v in vulns if isinstance(v, str) and '[LOW]' in v)
        
        # Format vulnerability list
        vuln_sample = []
        for v in vulns[:5]:  # First 5
            if isinstance(v, str):
                vuln_sample.append(v.strip())
        vulns_text = "\n".join([f"- {v}" for v in vuln_sample])
        
        prompt = f"""
You are a cybersecurity executive consultant. Write a brief executive summary of a security scan.

**Scan Overview:**
- Target: {target}
- Duration: {duration}
- Total Vulnerabilities Found: {total_vulns}
- Risk Distribution: {critical} Critical | {high} High | {medium} Medium | {low} Low

**Sample Vulnerabilities:**
{vulns_text}

**Your Task:**
Write a 3-4 sentence executive summary that:
1. States the overall security posture (Critical/High/Medium/Low Risk)
2. Highlights the main findings and areas of concern
3. Recommends immediate vs. planned remediation priorities
4. Is suitable for C-level management (non-technical language)

Keep it concise, impactful, and actionable.
"""
        return prompt.strip()
    
    def get_status(self) -> Dict[str, any]:
        """Get current status of Gemini integration"""
        quota_status = self.quota_manager.get_status()
        return {
            'enabled': self.enabled,
            'api_key_set': bool(self.api_key),
            'error': self.error_message,
            'cache_dir': str(self.cache_dir),
            'cached_analyses': len(list(self.cache_dir.glob('*.json'))),
            'quota': quota_status
        }


def initialize_gemini() -> GeminiAnalyzer:
    """
    Initialize Gemini analyzer from environment
    
    Returns:
        GeminiAnalyzer instance (enabled or disabled based on API key availability)
    """
    analyzer = GeminiAnalyzer()
    status = analyzer.get_status()
    
    print("\n" + "="*60)
    print("GEMINI API INTEGRATION STATUS")
    print("="*60)
    print(f"Enabled: {status['enabled']}")
    print(f"API Key Configured: {status['api_key_set']}")
    if status['error']:
        print(f"Error: {status['error']}")
    print(f"Cached Analyses: {status['cached_analyses']}")
    
    # Display quota information
    quota = status.get('quota', {})
    if quota:
        print("\nQUOTA USAGE:")
        print(f"  Per Minute: {quota['minute_used']}/{quota['minute_limit']} requests")
        print(f"  Per Day: {quota['day_used']}/{quota['day_limit']} requests")
        if quota['quota_exhausted_until']:
            reset_hours = quota['quota_reset_in_hours']
            if reset_hours > 0:
                print(f"  STATUS: ⚠️  QUOTA EXHAUSTED")
                print(f"  Reset in: {reset_hours:.1f} hours")
            else:
                print(f"  STATUS: ✅ Quota available")
        else:
            print(f"  STATUS: ✅ Quota available")
    
    print("="*60 + "\n")
    
    return analyzer


if __name__ == "__main__":
    # Test the analyzer
    analyzer = initialize_gemini()
    
    if analyzer.enabled:
        # Example vulnerability
        test_vuln = {
            'id': 'test_1',
            'name': 'OpenSSH 7.4 Remote Code Execution',
            'service': 'SSH',
            'version': '7.4p1',
            'cve': 'CVE-2019-16509',
            'cvss_score': 9.8,
            'severity': 'CRITICAL',
            'description': 'OpenSSH versions before 7.4p1 are vulnerable to authentication bypass',
            'exploit_available': True
        }
        
        print("Testing Gemini Analysis...")
        analysis = analyzer.analyze_vulnerability(test_vuln)
        if analysis:
            print("\n--- ANALYSIS RESULT ---")
            print(analysis)

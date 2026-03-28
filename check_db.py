import sqlite3

conn = sqlite3.connect(r'c:\Users\Danish\OneDrive\Desktop\recon cyber\CyberRecon-Pro\scans.db')
c = conn.cursor()

# Get tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("Tables:", tables)

# For scan 80, check the findings_evidence table
if 'finding_evidence' in tables:
    c.execute("SELECT type, title, COUNT(*) as count FROM finding_evidence WHERE scan_id=80 GROUP BY type, title")
    print("\nEvidence for scan 80:")
    [print(f"  {r[0]}: {r[1]} ({r[2]})") for r in c.fetchall()]

# Check vulnerabilities
if 'vulnerabilities' in tables:
    c.execute("SELECT risk, COUNT(*) as count FROM vulnerabilities WHERE scan_id=80 GROUP BY risk")
    print("\nVulnerabilities for scan 80:")
    [print(f"  {r[0]}: {r[1]}") for r in c.fetchall()]

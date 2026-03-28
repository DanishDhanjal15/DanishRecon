import json

d = json.load(open(r'c:\Users\Danish\OneDrive\Desktop\recon cyber\CyberRecon-Pro\results\scan_80.json'))
print(f"Total API endpoints: {len(d.get('api_endpoints', []))}")
if d.get('api_endpoints'):
    for i, e in enumerate(d.get('api_endpoints', [])):
        print(f"{i+1}. {e.get('url', 'N/A')}")
else:
    print("No API endpoints found")

print(f"\nServices detected: {len(d.get('services', []))}")
if d.get('services'):
    for svc in d.get('services', [])[:5]:
        print(f"  - {svc}")

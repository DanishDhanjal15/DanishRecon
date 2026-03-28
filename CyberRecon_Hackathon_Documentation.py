#!/usr/bin/env python3
"""
CyberRecon-Pro Hackathon Documentation Generator
Generates comprehensive PDF documentation for hackathon judges
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Custom styles
def get_custom_styles():
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a4d8f'),
        spaceAfter=12,
        fontName='Helvetica-Bold',
        alignment=TA_CENTER
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold',
        borderColor=colors.HexColor('#e5e7eb'),
        borderWidth=1,
        borderPadding=5,
        backColor=colors.HexColor('#f3f4f6')
    )
    
    # Body style
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        leading=14
    )
    
    # Feature style
    feature_style = ParagraphStyle(
        'Feature',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=4,
        leading=12
    )
    
    return {
        'title': title_style,
        'heading': heading_style,
        'body': body_style,
        'feature': feature_style
    }

def create_hackathon_documentation(output_path):
    """Create comprehensive PDF documentation"""
    
    styles = get_custom_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    story = []
    
    # ============== COVER PAGE ==============
    story.append(Spacer(1, 2*inch))
    
    title = Paragraph("CyberRecon-Pro", styles['title'])
    story.append(title)
    
    subtitle = Paragraph("Advanced Cybersecurity Reconnaissance &amp; Vulnerability Assessment Platform", 
                        ParagraphStyle('subtitle', parent=styles['body'], fontSize=13, alignment=TA_CENTER, textColor=colors.HexColor('#6b7280')))
    story.append(subtitle)
    
    story.append(Spacer(1, 0.5*inch))
    
    intro = Paragraph(
        "<b>For Hackathon Judges</b><br/><br/>"
        "A complete guide to understanding the features, architecture, and deployment of DanishRecon - "
        "an enterprise-grade reconnaissance and vulnerability assessment tool.",
        ParagraphStyle('intro', parent=styles['body'], fontSize=11, alignment=TA_CENTER)
    )
    story.append(intro)
    
    story.append(Spacer(1, 1.5*inch))
    
    date_text = Paragraph(f"<i>Generated: {datetime.now().strftime('%B %d, %Y')}</i>", 
                         ParagraphStyle('date', parent=styles['body'], fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor('#9ca3af')))
    story.append(date_text)
    
    story.append(PageBreak())
    
    # ============== TABLE OF CONTENTS ==============
    story.append(Paragraph("Table of Contents", styles['heading']))
    story.append(Spacer(1, 0.2*inch))
    
    toc_items = [
        "1. Project Overview",
        "2. Key Features & Capabilities",
        "3. Technology Stack",
        "4. How to Initialize & Run",
        "5. Complete Workflow Explanation",
        "6. Core Components & Functions",
        "7. Scanning Profiles",
        "8. Vulnerability Assessment Engine",
        "9. Reporting & Export",
        "10. Compliance Mapping",
        "11. Visualization Dashboard",
        "12. Attack Path Analysis",
        "13. Use Cases & Applications",
        "14. Security Considerations",
        "15. Future Enhancements"
    ]
    
    for item in toc_items:
        story.append(Paragraph(item, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 1. PROJECT OVERVIEW ==============
    story.append(Paragraph("1. Project Overview", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    overview_text = """
    <b>DanishRecon</b> (CyberRecon-Pro) is an advanced cybersecurity reconnaissance and vulnerability assessment platform 
    designed for penetration testing, security assessments, and red-team engagements. Built with Python and PyQt5, 
    it provides a modern graphical interface to automated reconnaissance, service discovery, vulnerability intelligence, 
    and attack-path visualization.
    """
    story.append(Paragraph(overview_text, styles['body']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Core Purpose:</b>", styles['feature']))
    core_purposes = [
        "Automate reconnaissance tasks to save time and reduce manual errors",
        "Discover all exposed services and assets on target networks",
        "Identify vulnerabilities with CVSS scoring and CVE database integration",
        "Map findings to compliance frameworks (PCI-DSS, HIPAA, NIST, CIS)",
        "Visualize attack paths and risk heatmaps for stakeholders",
        "Generate professional reports in multiple formats (HTML, JSON, CSV, PDF, Markdown)"
    ]
    
    for purpose in core_purposes:
        story.append(Paragraph(f"• {purpose}", styles['feature']))
    
    story.append(Spacer(1, 0.2*inch))
    
    # ============== 2. KEY FEATURES ==============
    story.append(Paragraph("2. Key Features &amp; Capabilities", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    feature_categories = [
        ("Reconnaissance Module", [
            "Multi-target batch scanning with queue management",
            "Subdomain discovery using automated tools",
            "DNS reconnaissance (MX, TXT, NS, SPF, DMARC records)",
            "Host discovery and alive host detection",
            "OS fingerprinting and device identification"
        ]),
        ("Network &amp; Service Scanning", [
            "Nmap-based port scanning with multiple profiles",
            "Service version detection and banner grabbing",
            "Network topology discovery and mapping",
            "Live packet capture statistics",
            "Port state heatmap charts"
        ]),
        ("Security Analysis", [
            "SSL/TLS certificate analysis and expiry detection",
            "Weak cipher detection and protocol weakness identification",
            "Firewall and WAF (Web Application Firewall) detection",
            "Default credential checking",
            "Password policy analysis"
        ]),
        ("Vulnerability Intelligence", [
            "CVE database integration with live lookups",
            "CVSS scoring and severity classification",
            "MITRE ATT&CK technique tagging",
            "Exploit suggestions via Searchsploit integration",
            "Attack path generation"
        ]),
        ("Visualization &amp; Dashboards", [
            "Risk heatmap with color-coded severity",
            "Attack path graphs showing exploitation chains",
            "Network topology visualization with hop details",
            "Service distribution charts",
            "Timeline view of scan events"
        ]),
        ("Reporting &amp; Compliance", [
            "HTML reports with interactive elements",
            "JSON export for automation and parsing",
            "CSV export for spreadsheet analysis",
            "Markdown export for documentation",
            "PDF reports with embedded charts",
            "PCI-DSS, HIPAA, NIST, CIS compliance mapping"
        ])
    ]
    
    for category, features in feature_categories:
        story.append(Paragraph(f"<b>{category}</b>", styles['feature']))
        for feature in features:
            story.append(Paragraph(f"  • {feature}", styles['feature']))
        story.append(Spacer(1, 0.1*inch))
    
    story.append(PageBreak())
    
    # ============== 3. TECHNOLOGY STACK ==============
    story.append(Paragraph("3. Technology Stack", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    tech_stack = [
        ("Backend Language", "Python 3.7+"),
        ("GUI Framework", "PyQt5 (cross-platform desktop UI)"),
        ("Data Persistence", "SQLite (lightweight, embedded database)"),
        ("Visualization", "NetworkX (graph algorithms) + Matplotlib (plotting)"),
        ("Report Generation", "ReportLab (PDF creation)"),
        ("External Tools", "Nmap, Nikto, Searchsploit, Subfinder, Wafw00f, Dig/Nslookup, Curl"),
        ("HTTP Client", "Requests library for API scanning"),
        ("Threading", "Python threading + PyQt QThread for concurrent operations"),
        ("Version Control", "Git"),
        ("OS Compatibility", "Windows, macOS, Linux")
    ]
    
    stack_data = [["Component", "Technology"]]
    for component, tech in tech_stack:
        stack_data.append([component, tech])
    
    stack_table = Table(stack_data, colWidths=[2.5*inch, 3.5*inch])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
    ]))
    story.append(stack_table)
    story.append(Spacer(1, 0.2*inch))
    
    # ============== 4. INITIALIZATION & SETUP ==============
    story.append(Paragraph("4. How to Initialize &amp; Run the Project", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.1 System Requirements</b>", styles['feature']))
    requirements = [
        "Python 3.7 or higher",
        "Nmap installed and in system PATH",
        "Nikto installed (for web vulnerability scanning)",
        "Searchsploit installed (for exploit database lookups)",
        "Subfinder installed (for subdomain enumeration)",
        "Wafw00f installed (for WAF detection)",
        "PyQt5 libraries: PyQt5, PyQt5-UIC",
        "Python packages: networkx, matplotlib, reportlab, requests, urllib3",
        "Minimum 2GB RAM recommended",
        "Internet connection for CVE database and API lookups"
    ]
    for req in requirements:
        story.append(Paragraph(f"• {req}", styles['feature']))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.2 Installation Steps</b>", styles['feature']))
    setup_steps = [
        ("<b>Step 1: Clone or Extract</b>", "Download the project and extract to your preferred directory"),
        ("<b>Step 2: Create Virtual Environment</b>", "python -m venv .venv"),
        ("<b>Step 3: Activate Virtual Environment</b>", ".venv\\Scripts\\activate (Windows) or source .venv/bin/activate (Linux/Mac)"),
        ("<b>Step 4: Install Python Dependencies</b>", "pip install -r requirements.txt"),
        ("<b>Step 5: Install External Tools</b>", "Ensure nmap, nikto, searchsploit are installed and in PATH"),
        ("<b>Step 6: Run the Application</b>", "python Cyber_recon_pro.py")
    ]
    
    for step_title, step_desc in setup_steps:
        story.append(Paragraph(f"{step_title}", styles['feature']))
        story.append(Paragraph(f"<i>{step_desc}</i>", ParagraphStyle('code', parent=styles['feature'], fontSize=9, textColor=colors.HexColor('#7c3aed'))))
        story.append(Spacer(1, 0.05*inch))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>4.3 First Run - Quick Start</b>", styles['feature']))
    first_run = [
        "1. Launch the application: python Cyber_recon_pro.py",
        "2. Enter a target domain or IP address in the 'Target' field",
        "3. Select a scan profile (Quick, Full, Stealth, or Custom)",
        "4. Click 'Start Scan'",
        "5. Watch real-time progress in the console and dashboard",
        "6. Once complete, view results in different tabs (Hosts, Services, Vulnerabilities, etc.)",
        "7. Export report in your preferred format (HTML, JSON, CSV, PDF)"
    ]
    for step in first_run:
        story.append(Paragraph(step, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 5. COMPLETE WORKFLOW ==============
    story.append(Paragraph("5. Complete Workflow Explanation", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>The scanning pipeline executes in this sequential order:</b>", styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    workflow_steps = [
        ("STEP 1: User Input & Target Sanitization", 
         "User enters a domain or IP. The system removes 'http://', 'https://', and trailing slashes to normalize the target. "
         "A unique scan ID is created in the SQLite database."),
        
        ("STEP 2: DNS Reconnaissance (Domain Targets)",
         "For domain targets, the system queries DNS records:\n"
         "   • A records (IPv4 addresses)\n"
         "   • AAAA records (IPv6 addresses)\n"
         "   • MX records (mail servers)\n"
         "   • NS records (nameservers)\n"
         "   • TXT records (text records, SPF, DKIM)\n"
         "   • CNAME records (aliases)\n"
         "   • SOA records (zone info)\n"
         "   • SPF, DMARC records (email security)\n"
         "The system also detects CDN/protection (Cloudflare, Akamai, etc.)"),
        
        ("STEP 3: Subdomain Discovery",
         "Uses 'subfinder' tool to enumerate subdomains. Falls back to common subdomain patterns "
         "(www, mail, api, dev, admin, etc.) if subfinder unavailable. All discovered subdomains are added to scan targets."),
        
        ("STEP 4: Host Discovery",
         "Nmap performs a live host discovery scan to identify which targets are online. "
         "This uses ping/ARP probes to quickly identify responsive hosts. Reduces scanning time on dead targets."),
        
        ("STEP 5: SSL/TLS Certificate Analysis",
         "For common HTTPS ports (443, 8443, 8080), the system:\n"
         "   • Extracts SSL certificates\n"
         "   • Checks for expiry dates (alerts on expired certs)\n"
         "   • Identifies weak ciphers (RC4, DES, etc.)\n"
         "   • Detects old TLS versions (SSLv3, TLSv1.0)\n"
         "   • Records certificate details for compliance"),
        
        ("STEP 6: Port &amp; Service Scanning",
         "Nmap performs the main port scan using the selected profile:\n"
         "   • Quick: Scans top 100 ports\n"
         "   • Full: Scans all 65535 ports\n"
         "   • Stealth: Slow scan with evasion techniques\n"
         "   • Custom: User-defined Nmap flags\n"
         "Results include: open/closed/filtered states, service names, versions, and banners."),
        
        ("STEP 7: WAF/CDN Detection",
         "Analyzes detected web services to identify if they're protected by a Web Application Firewall or Content Delivery Network. "
         "This helps explain why some ports might be blocked or filtered."),
        
        ("STEP 8: Web Vulnerability Scanning (Nikto)",
         "If web services (HTTP/HTTPS) are detected, Nikto scans for:\n"
         "   • Outdated server software\n"
         "   • Common web vulnerabilities\n"
         "   • Misconfigured web servers\n"
         "   • Known exploitable files/directories\n"
         "   • SSL/TLS issues"),
        
        ("STEP 9: Exploit Database Lookup (Searchsploit)",
         "For each detected service and version, the system queries the Exploit Database (via searchsploit) to find known public exploits. "
         "This helps identify immediately exploitable vulnerabilities."),
        
        ("STEP 10: Risk Ranking &amp; Severity Assessment",
         "A rule-based algorithm assigns severity levels (CRITICAL, HIGH, MEDIUM, LOW) based on:\n"
         "   • Service type (FTP, Telnet = risky)\n"
         "   • Open ports (SMB=risky, specific ports=dangerous)\n"
         "   • Missing service versions (unknown = risky)\n"
         "   • Banner analysis (anonymous access, debug mode indicators)\n"
         "   • Known CVEs for detected versions"),
        
        ("STEP 11: Compliance Mapping",
         "Findings are mapped to compliance frameworks:\n"
         "   • PCI-DSS: Payment Card Industry standards\n"
         "   • HIPAA: Healthcare compliance\n"
         "   • NIST: National Institute of Standards frameworks\n"
         "   • CIS: Center for Internet Security benchmarks\n"
         "   • OWASP: Web application security standards"),
        
        ("STEP 12: Attack Path Generation",
         "The system builds logical attack chains:\n"
         "   • If FTP+Anonymous = Direct file access\n"
         "   • If SSH+WeakVersion = Possible RCE\n"
         "   • If WebServer+CMS = Known exploit chain\n"
         "This shows judges the 'story' of how a target could be compromised."),
        
        ("STEP 13: Visualization Generation",
         "Creates graphs and charts:\n"
         "   • Attack graph (NetworkX + Matplotlib)\n"
         "   • Risk heatmap (service severity distribution)\n"
         "   • Port state distribution (open/closed/filtered)\n"
         "   • Timeline of discovered items scanned"),
        
        ("STEP 14: Report Generation",
         "Automatically generates reports in all formats:\n"
         "   • HTML: Interactive, web-viewable with charts\n"
         "   • JSON: Structured data for automation\n"
         "   • CSV: Spreadsheet-friendly format\n"
         "   • Markdown: Documentation-friendly\n"
         "   • PDF: Print-ready with embedded visualizations"),
        
        ("STEP 15: Results Saved to Database",
         "All findings are persisted to SQLite with metadata:\n"
         "   • Hosts: IP, hostname, OS, services\n"
         "   • Ports: Port number, state, service, version\n"
         "   • Vulnerabilities: Description, severity, CVE, CVSS\n"
         "   • Timeline: When each item was discovered\n"
         "   • Recommendations: How to fix each issue")
    ]
    
    for step_num, (step_title, step_desc) in enumerate(workflow_steps, 1):
        story.append(Paragraph(f"<b>{step_title}</b>", styles['feature']))
        story.append(Paragraph(step_desc, styles['feature']))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(PageBreak())
    
    # ============== 6. CORE COMPONENTS & FUNCTIONS ==============
    story.append(Paragraph("6. Core Components &amp; Functions", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>6.1 ScanEngine Class (Backend Orchestrator)</b>", styles['feature']))
    scanengine_text = """
    The ScanEngine is the heart of the application. It runs as a separate thread (QThread) to keep the GUI responsive while performing 
    long-running scans. It manages: <br/>
    <b>Key Responsibilities:</b><br/>
    • Orchestrating all scanning stages in sequence<br/>
    • Managing the in-memory data structure (self.data dictionary)<br/>
    • Sending progress signals to the GUI<br/>
    • Handling pause/resume/stop operations<br/>
    • Managing scan timing and database persistence<br/>
    <b>Key Methods:</b><br/>
    • run(): Main execution loop that runs all stages<br/>
    • stop(): Gracefully terminates the scan<br/>
    • pause(): Pauses execution between stages<br/>
    • resume(): Resumes from paused state<br/>
    • _sync_timing_data(): Updates start/end times
    """
    story.append(Paragraph(scanengine_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>6.2 Database Layer</b>", styles['feature']))
    db_text = """
    SQLite is used for persistent storage. Key tables include:<br/>
    <b>scans:</b> Scan records with start time, end time, target, profile, status<br/>
    <b>hosts:</b> Discovered hosts with IP, hostname, OS, port count<br/>
    <b>ports:</b> Open ports with service name, version, banner, state<br/>
    <b>vulns:</b> Vulnerabilities with CVE, CVSS, description, remediation<br/>
    <b>timeline:</b> Event log of discoveries with timestamps
    """
    story.append(Paragraph(db_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>6.3 APIScanner Module</b>", styles['feature']))
    api_text = """
    Automatically discovers API endpoints and tests for common vulnerabilities:<br/>
    • Checks common API paths (/api/, /api/v1/, /graphql, /swagger-ui.html, etc.)<br/>
    • Tests for unauthenticated access<br/>
    • Supports bearer token and cookie authentication<br/>
    • Detects API documentation (Swagger, OpenAPI)<br/>
    • Deep mode with extended path enumeration<br/>
    • Logs all discovered endpoints to database
    """
    story.append(Paragraph(api_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>6.4 Report Generator</b>", styles['feature']))
    report_text = """
    Handles multi-format export:<br/>
    <b>HTML:</b> Interactive report with charts, collapsible sections, search functionality<br/>
    <b>JSON:</b> Complete structured data export for programmatic access<br/>
    <b>CSV:</b> Spreadsheet-ready format for hosts, ports, and vulnerabilities<br/>
    <b>Markdown:</b> Documentation-friendly text format<br/>
    <b>PDF:</b> Print-ready report with embedded visualizations and tables
    """
    story.append(Paragraph(report_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>6.5 Visualization Engine</b>", styles['feature']))
    viz_text = """
    Uses NetworkX and Matplotlib to create visualizations:<br/>
    <b>Attack Graph:</b> Nodes for each host/service, edges showing attack paths<br/>
    <b>Risk Heatmap:</b> Color-coded severity distribution (green=low, yellow=medium, orange=high, red=critical)<br/>
    <b>Service Distribution Chart:</b> Pie/bar charts showing service types found<br/>
    <b>Port State Chart:</b> Breakdown of open, closed, filtered ports<br/>
    <b>Timeline Graph:</b> Discovery events plotted over scan duration
    """
    story.append(Paragraph(viz_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 7. SCANNING PROFILES ==============
    story.append(Paragraph("7. Scanning Profiles", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    profiles_data = [
        ["Profile", "Speed", "Discover", "Best For", "Typical Duration"],
        ["QUICK", "Very Fast", "Top 100 ports", "Initial assessment, quick reconnaissance", "2-5 minutes"],
        ["FULL", "Slow", "All 65535 ports", "Complete audits, thorough testing", "30-60 minutes"],
        ["STEALTH", "Very Slow", "All ports with evasion", "Evade IDS/WAF detection", "120+ minutes"],
        ["CUSTOM", "Variable", "User-defined", "Specific targeting, advanced users", "Variable"]
    ]
    
    profiles_table = Table(profiles_data, colWidths=[1.1*inch, 1*inch, 1.2*inch, 1.5*inch, 1.2*inch])
    profiles_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    story.append(profiles_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("<b>Profile Details:</b>", styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>QUICK Profile</b>", styles['feature']))
    story.append(Paragraph(
        "Performs fast reconnaissance on top 100 most common ports. Ideal for initial scans or when time is limited. "
        "Uses Nmap's quick template with service version detection.",
        styles['feature']
    ))
    story.append(Spacer(1, 0.08*inch))
    
    story.append(Paragraph("<b>FULL Profile</b>", styles['feature']))
    story.append(Paragraph(
        "Comprehensive scan of all 65,535 ports with version detection and OS fingerprinting. Used for complete security audits. "
        "Takes significantly longer but finds all open ports.",
        styles['feature']
    ))
    story.append(Spacer(1, 0.08*inch))
    
    story.append(Paragraph("<b>STEALTH Profile</b>", styles['feature']))
    story.append(Paragraph(
        "Uses slow, deliberate scanning techniques to evade intrusion detection systems (IDS) and Web Application Firewalls (WAF). "
        "Can take hours but minimizes detection. Uses fragmented packets and timing randomization.",
        styles['feature']
    ))
    story.append(Spacer(1, 0.08*inch))
    
    story.append(Paragraph("<b>CUSTOM Profile</b>", styles['feature']))
    story.append(Paragraph(
        "Allows advanced users to specify custom Nmap flags and parameters. Enables precise targeting and specialized scanning strategies. "
        "For users familiar with Nmap command-line syntax.",
        styles['feature']
    ))
    
    story.append(PageBreak())
    
    # ============== 8. VULNERABILITY ASSESSMENT ENGINE ==============
    story.append(Paragraph("8. Vulnerability Assessment Engine", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>8.1 Risk Ranking Algorithm</b>", styles['feature']))
    risk_text = """
    The system uses a rule-based heuristic algorithm (not AI/ML) to score vulnerability severity:<br/>
    <b>Inputs to Algorithm:</b><br/>
    • Service type detected (FTP, Telnet, SSH, HTTP, etc.)<br/>
    • Port number (privileged ports are more sensitive)<br/>
    • Service version (known vulnerable versions)<br/>
    • Banner contents (debug modes, version leaks)<br/>
    • Available exploits for detected services<br/>
    • Compliance violations (PCI-DSS, HIPAA)<br/>
    <b>Severity Levels Assigned:</b><br/>
    • CRITICAL (Red): Immediate exploitation risk (e.g., RCE, authentication bypass)<br/>
    • HIGH (Orange): Serious impact if exploited (e.g., information disclosure, privilege escalation)<br/>
    • MEDIUM (Yellow): Moderate risk with specific preconditions (e.g., weak ciphers)<br/>
    • LOW (Green): Minor issues with limited impact (e.g., banner disclosure)
    """
    story.append(Paragraph(risk_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>8.2 CVE Integration</b>", styles['feature']))
    cve_text = """
    When a service version is detected, the system:<br/>
    1. Looks up known CVEs for that version<br/>
    2. Retrieves CVSS scores (0-10 scale)<br/>
    3. Checks for available public exploits<br/>
    4. Maps to MITRE ATT&CK techniques<br/>
    5. Stores findings in the vulnerability database<br/>
    This enables quick identification of critical, patched vulnerabilities.
    """
    story.append(Paragraph(cve_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>8.3 MITRE ATT&amp;CK Mapping</b>", styles['feature']))
    mitre_text = """
    Each vulnerability is mapped to MITRE ATT&CK framework tactics and techniques:<br/>
    <b>Example Mappings:</b><br/>
    • FTP Service = T1546 (Event Triggered Execution)<br/>
    • Weak SSH = T1021.002 (Remote Services: SSH)<br/>
    • Web Vulnerability = T1190 (Exploit Public-Facing Application)<br/>
    • Certificate Issues = T1552.004 (Unsecured Credentials)<br/>
    This helps security teams understand adversary tactics being enabled by vulnerabilities.
    """
    story.append(Paragraph(mitre_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>8.4 Recommendations Engine</b>", styles['feature']))
    rec_text = """
    For each finding, the system auto-generates remediation advice:<br/>
    • <b>Weak Service Versions:</b> Update to latest patched version<br/>
    • <b>Unnecessary Services:</b> Disable if not required (reduce attack surface)<br/>
    • <b>SSL/TLS Issues:</b> Update protocols, remove weak ciphers<br/>
    • <b>Missing Records:</b> Implement SPF, DMARC for email security<br/>
    • <b>API Exposure:</b> Implement authentication and rate limiting<br/>
    • <b>Default Credentials:</b> Change/disable default accounts<br/>
    These recommendations appear in reports and help remediation teams prioritize fixes.
    """
    story.append(Paragraph(rec_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 9. REPORTING & EXPORT ==============
    story.append(Paragraph("9. Reporting &amp; Export", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>9.1 HTML Reports</b>", styles['feature']))
    html_text = """
    <b>Features:</b><br/>
    • Responsive design (works on desktop and mobile)<br/>
    • Interactive charts with drill-down capability<br/>
    • Collapsible sections for detailed findings<br/>
    • Search/filter across findings<br/>
    • Color-coded severity indicators<br/>
    • Executive summary with key metrics<br/>
    • Timeline of scan events<br/>
    • Links to CVE databases and exploit resources<br/>
    <b>Use Case:</b> Sharing with stakeholders, clients, management
    """
    story.append(Paragraph(html_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>9.2 JSON Export</b>", styles['feature']))
    json_text = """
    <b>Features:</b><br/>
    • Complete structured data export<br/>
    • Easy parsing for automation tools<br/>
    • Includes all metadata and timestamps<br/>
    • Compatible with SIEM systems and ticketing systems<br/>
    • Can be imported into other security tools<br/>
    <b>Use Case:</b> Integration with security infrastructure, automated remediation workflows
    """
    story.append(Paragraph(json_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>9.3 CSV Export</b>", styles['feature']))
    csv_text = """
    <b>Features:</b><br/>
    • Hosts tab: IP addresses, hostnames, OS, open port counts<br/>
    • Vulnerabilities tab: CVE IDs, CVSS scores, descriptions, affected services<br/>
    • Services tab: Port numbers, service names, versions, banners<br/>
    • Openable in Excel/Google Sheets<br/>
    <b>Use Case:</b> Spreadsheet analysis, data import into tracking systems
    """
    story.append(Paragraph(csv_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>9.4 Markdown Export</b>", styles['feature']))
    md_text = """
    <b>Features:</b><br/>
    • GitHub markdown format<br/>
    • Good for documentation and version control<br/>
    • Tables with findings<br/>
    • Headings and sections<br/>
    <b>Use Case:</b> Documentation, GitHub issues, internal wikis
    """
    story.append(Paragraph(md_text, styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    story.append(Paragraph("<b>9.5 PDF Export</b>", styles['feature']))
    pdf_text = """
    <b>Features:</b><br/>
    • Professional print-ready format<br/>
    • Embedded charts and graphs<br/>
    • Executive summary<br/>
    • Table of contents<br/>
    • Risk scorecards<br/>
    • Page breaks for sections<br/>
    <b>Use Case:</b> Client deliverables, audit reports, management presentations
    """
    story.append(Paragraph(pdf_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>9.6 Report File Naming</b>", styles['feature']))
    naming_text = """
    Files are automatically named with timestamp and target:<br/>
    report_[target]_[YYYY-MM-DD_HHMM].html<br/>
    report_[target]_[YYYY-MM-DD_HHMM].json<br/>
    report_[target]_[YYYY-MM-DD_HHMM].csv<br/>
    report_[target]_[YYYY-MM-DD_HHMM].pdf<br/>
    This prevents accidental overwrites and maintains scan history.
    """
    story.append(Paragraph(naming_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 10. COMPLIANCE MAPPING ==============
    story.append(Paragraph("10. Compliance Mapping", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Framework Overview</b>", styles['feature']))
    story.append(Spacer(1, 0.1*inch))
    
    compliance_frameworks = [
        ("PCI-DSS (Payment Card Industry - Data Security Standard)",
         "Requirements for organizations handling credit card data. Mapped findings include: "
         "unencrypted connections, weak authentication, vulnerability assessment gaps, access control issues."),
        
        ("HIPAA (Health Insurance Portability and Accountability Act)",
         "Requirements for healthcare organizations. Mapped findings include: "
         "unencrypted patient data, weak access controls, audit trail gaps, integrity verification issues."),
        
        ("NIST (National Institute of Standards and Technology)",
         "Framework for managing cybersecurity risk. Mapped findings include: "
         "asset management gaps, access control deficiencies, configuration management issues, detection/response gaps."),
        
        ("CIS (Center for Internet Security) Benchmarks",
         "Consensus-based best practices. Mapped findings include: "
         "software updates missing, users/groups misconfigured, security parameters not hardened.")
    ]
    
    for framework, description in compliance_frameworks:
        story.append(Paragraph(f"<b>{framework}</b>", styles['feature']))
        story.append(Paragraph(description, styles['feature']))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>How Mapping Works</b>", styles['feature']))
    mapping_text = """
    1. Each vulnerability found is analyzed<br/>
    2. System checks applicable compliance requirements<br/>
    3. Violations are tagged with framework(s) affected<br/>
    4. Reports include compliance scorecard showing gaps<br/>
    5. Remediation advice includes compliance objectives<br/>
    This helps organizations understand not just technical risks, but compliance implications.
    """
    story.append(Paragraph(mapping_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 11. VISUALIZATION DASHBOARD ==============
    story.append(Paragraph("11. Visualization Dashboard", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>11.1 Dashboard Components</b>", styles['feature']))
    
    dashboard_components = [
        ("Risk Heatmap", 
         "Color-coded grid showing vulnerability severity distribution. Bright red = critical issues, orange = high, yellow = medium, green = low. "
         "Allows quick visual assessment of overall risk posture."),
        
        ("Attack Graph Visualization",
         "Network diagram showing discovered hosts and services as nodes, with edges representing potential attack paths. "
         "Shows how vulnerabilities chain together to enable system compromise."),
        
        ("Service Distribution Chart",
         "Pie chart showing breakdown of detected services (HTTP, FTP, SSH, DNS, etc.). Helps identify most common service types."),
        
        ("Port State Heatmap",
         "Color-coded matrix of ports vs. hosts showing which ports are open/closed/filtered on each target. "
         "Quickly identifies common open ports across network."),
        
        ("Timeline Visualization",
         "Scanner events plotted over time showing chronological discovery. Helps understand scan progression and which stages took longest."),
        
        ("Summary Statistics",
         "Key numbers: Total hosts, services found, vulnerabilities discovered, critical issues, etc. "
         "Updated live during scan.")
    ]
    
    for component, description in dashboard_components:
        story.append(Paragraph(f"<b>{component}</b>", styles['feature']))
        story.append(Paragraph(description, styles['feature']))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>11.2 Real-Time Updates</b>", styles['feature']))
    realtime_text = """
    As the scan progresses, the dashboard updates in real-time:<br/>
    • Progress bars for each scanning stage<br/>
    • Console log with current activity<br/>
    • Live result counts (hosts, services, vulns)<br/>
    • Current scan stage indicator<br/>
    • Estimated time remaining<br/>
    • Elapsed time display<br/>
    This gives users confidence that the tool is working and provides transparency into scan progress.
    """
    story.append(Paragraph(realtime_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 12. ATTACK PATH ANALYSIS ==============
    story.append(Paragraph("12. Attack Path Analysis", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>How Attack Paths Are Generated</b>", styles['feature']))
    attack_paths_text = """
    The system analyzes discovered vulnerabilities and creates realistic attack scenarios:<br/>
    <b>Example Attack Path 1: Anonymous FTP Access</b><br/>
    • Discovered: FTP service on port 21 with anonymous login<br/>
    • Risk: Attacker can connect and download sensitive files<br/>
    • Impact: Information disclosure, credential theft<br/>
    • Path visualization: Internet → Firewall → FTP Server → File System<br/>
    <br/>
    <b>Example Attack Path 2: Weak SSH + Known Exploit</b><br/>
    • Discovered: SSH v2.0 on port 22 (old vulnerable version)<br/>
    • Available Exploit: OpenSSH_2.0 Buffer Overflow (CVE-2002-0083)<br/>
    • Risk: Remote Code Execution<br/>
    • Path visualization: Internet → Firewall → SSH → Shell Access → System Compromise<br/>
    <br/>
    <b>Example Attack Path 3: Unpatched Web Server</b><br/>
    • Discovered: Apache 2.2.15 on port 80 with known vulnerabilities<br/>
    • Nikto Found: CVE-2013-1896, CVE-2013-6438<br/>
    • Risk: RCE via crafted HTTP requests<br/>
    • Path visualization: Internet → Firewall → Web Server → Code Execution<br/>
    <br/>
    <b>Example Attack Path 4: API without Authentication</b><br/>
    • Discovered: /api/v1/users endpoint responding to unauthenticated requests<br/>
    • Risk: Data exposure, account enumeration<br/>
    • Path visualization: Internet → Web Server → API Endpoint → User Database<br/>
    <br/>
    These paths help judges understand not just what's wrong, but how an attacker would exploit weaknesses.
    """
    story.append(Paragraph(attack_paths_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 13. USE CASES ==============
    story.append(Paragraph("13. Use Cases &amp; Applications", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    use_cases = [
        ("Penetration Testing",
         "Security professionals use this tool to quickly enumerate targets and identify vulnerabilities during authorized penetration tests. "
         "The multi-stage approach covers reconnaissance, enumeration, and vulnerability analysis phases."),
        
        ("Vulnerability Assessments",
         "Organizations use it to regularly audit their own infrastructure, identify security gaps before attackers do, "
         "and track remediation progress over time."),
        
        ("Compliance Audits",
         "Helps demonstrate compliance with security frameworks like PCI-DSS, HIPAA, NIST by identifying gaps and mapping to requirements."),
        
        ("Red Team Exercises",
         "Rapid reconnaissance for simulated attacks, understanding target surface and identifying exploitation vectors."),
        
        ("Security Awareness Training",
         "Demonstrates real vulnerabilities to IT and business teams to build security culture and understand impact."),
        
        ("Bug Bounty Programs",
         "Security researchers use it to efficiently discover vulnerabilities on target platforms within bounty scope."),
        
        ("Network Hardening",
         "System administrators identify exposed services and properly secure/restrict access to necessary services only."),
        
        ("Incident Response",
         "Quick assessment of compromised systems to understand what data/systems are exposed after a breach.")
    ]
    
    for use_case, description in use_cases:
        story.append(Paragraph(f"<b>▸ {use_case}</b>", styles['feature']))
        story.append(Paragraph(description, styles['feature']))
        story.append(Spacer(1, 0.08*inch))
    
    story.append(PageBreak())
    
    # ============== 14. SECURITY CONSIDERATIONS ==============
    story.append(Paragraph("14. Security Considerations", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Ethical &amp; Legal Usage</b>", styles['feature']))
    ethics_text = """
    <b>IMPORTANT: This tool must only be used with explicit written authorization.</b><br/>
    <b>Unauthorized use is illegal</b> and violates:<br/>
    • Computer Fraud and Abuse Act (CFAA) in the United States<br/>
    • Computer Misuse Act in the UK<br/>
    • Similar laws in most jurisdictions<br/>
    <br/>
    <b>Authorized Use Only:</b><br/>
    ✓ Penetration testing with signed contract<br/>
    ✓ Vulnerability assessments of your own systems<br/>
    ✓ Bug bounty programs with explicit scope<br/>
    ✓ Red team exercises with proper approval<br/>
    <br/>
    <b>NOT Authorized:</b><br/>
    ✗ Scanning unauthorized systems<br/>
    ✗ Scanning competitors' systems<br/>
    ✗ Data theft or modification<br/>
    ✗ Denial of service attacks
    """
    story.append(Paragraph(ethics_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Operational Security</b>", styles['feature']))
    opsec_text = """
    <b>Best Practices:</b><br/>
    • Use a dedicated testing environment/network<br/>
    • Document authorization before scanning<br/>
    • Notify IT/Security teams before large scans<br/>
    • Use appropriate scan profiles (Stealth for sensitive environments)<br/>
    • Rotate scanning IPs if possible to avoid detection<br/>
    • Keep scan results confidential<br/>
    • Remove/destroy reports after engagement ends<br/>
    • Log all scans and access to this tool
    """
    story.append(Paragraph(opsec_text, styles['feature']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>False Positives</b>", styles['feature']))
    fp_text = """
    Always verify findings manually:<br/>
    • Some services may be intentionally exposed for specific purposes<br/>
    • Version detection may be incorrect (banner misidentification)<br/>
    • Default credentials may be changed<br/>
    • WAF/IDS may block actual port responses<br/>
    <b>Always conduct manual verification before reporting high-severity issues.</b>
    """
    story.append(Paragraph(fp_text, styles['feature']))
    
    story.append(PageBreak())
    
    # ============== 15. FUTURE ENHANCEMENTS ==============
    story.append(Paragraph("15. Future Enhancements &amp; Roadmap", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph("<b>Currently Planned:</b>", styles['feature']))
    future_items = [
        "Machine Learning-based risk scoring (replacing current heuristics)",
        "Integration with real-time threat intelligence feeds",
        "Mobile app for remote scan monitoring",
        "Collaborative scanning (multiple users, team workspaces)",
        "Scan templates for industry-specific targets (banking, healthcare, etc.)",
        "Integration with Metasploit for automated exploitation testing",
        "Kubernetes and container security scanning",
        "Cloud infrastructure assessment (AWS, Azure, GCP)",
        "Continuous monitoring mode (recurring automated scans)",
        "Machine learning-powered recommendations",
        "Integration with vulnerability management platforms",
        "REST API for integration with other tools",
        "Distributed scanning across multiple agents"
    ]
    
    for item in future_items:
        story.append(Paragraph(f"• {item}", styles['feature']))
    
    story.append(Spacer(1, 0.3*inch))
    
    # ============== CONCLUSION ==============
    story.append(Paragraph("Conclusion", styles['heading']))
    story.append(Spacer(1, 0.15*inch))
    
    conclusion_text = """
    <b>DanishRecon (CyberRecon-Pro)</b> is a comprehensive, professional-grade cybersecurity reconnaissance and vulnerability 
    assessment platform that automates the complex process of identifying security weaknesses. By combining multiple specialized tools, 
    intelligent analysis, and professional reporting, it enables security teams to rapidly discover and remediate vulnerabilities.<br/>
    <br/>
    The platform is built on proven security principles and integrates industry-standard frameworks for compliance. Its modular architecture 
    allows for easy extension and integration with other security tools in an organization's security infrastructure.<br/>
    <br/>
    Whether used for penetration testing, vulnerability assessments, compliance audits, or security training, CyberRecon-Pro provides 
    the depth, breadth, and automation needed for modern cybersecurity operations.
    """
    story.append(Paragraph(conclusion_text, styles['body']))
    
    # Build PDF
    doc.build(story)
    print(f"✓ PDF Documentation generated successfully: {output_path}")

if __name__ == "__main__":
    output_file = r"c:\Users\Danish\OneDrive\Desktop\recon cyber\CyberRecon_Pro_Hackathon_Documentation.pdf"
    create_hackathon_documentation(output_file)

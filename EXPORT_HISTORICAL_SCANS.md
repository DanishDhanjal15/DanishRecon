# Export Historical Scan Results Feature

## Overview

The **Export Historical Scans** feature allows you to export scan results that have already been completed, without needing to re-run the scans. This is useful for:

- **Report Distribution**: Generate reports in multiple formats from past scans
- **Compliance**: Create audit-ready reports for compliance teams
- **Archiving**: Store results in different formats for records
- **Format Changes**: Export the same scan in different formats as needed

## How to Use

### 1. Open Scan History
- Click **"History"** button in the main window
- A dialog showing all previous scans will open

### 2. Select a Scan
- Click on any scan row to select it
- The selected scan will be highlighted

### 3. Choose Export Format
- Use the dropdown menu "Export Selected Scan As:" to pick your format:
  - **HTML**: Interactive HTML report (opens in browser)
  - **JSON**: Structured JSON data export
  - **CSV**: Comma-separated vulnerability table
  - **Markdown**: Markdown formatted report
  - **PDF**: Professional PDF document (requires ReportLab)

### 4. Export
- Click the **"Export"** button
- A confirmation message will show the export location
- HTML reports will automatically open in your default browser

## Export Formats Explained

### HTML Report
- **Best for**: Viewing and sharing
- **Output**: Professional styled web page with statistics, charts, and tables
- **File location**: `results/report_{scan_id}_export.html`
- **Opens automatically**: Yes

### JSON Export
- **Best for**: Data analysis and integration
- **Output**: Structured JSON containing all scan data
- **File location**: `results/scan_{scan_id}_export.json`
- **Useful for**: Parsing with scripts, API integration

### CSV Export
- **Best for**: Spreadsheet analysis
- **Output**: Vulnerability table with columns for host, service, port, risk, CVE, CVSS, title
- **File location**: `results/vulns_{scan_id}_export.csv`
- **Useful for**: Excel/Google Sheets analysis, further filtering

### Markdown Report
- **Best for**: Documentation and wikis
- **Output**: Markdown formatted report with sections
- **File location**: `results/report_{scan_id}_export.md`
- **Useful for**: GitHub, GitLab, MkDocs, Confluence

### PDF Report
- **Best for**: Professional documentation
- **Output**: Formatted PDF with tables and metadata
- **File location**: `results/report_{scan_id}_export.pdf`
- **Requires**: ReportLab library (`pip install reportlab`)
- **Note**: PDF may not be available if ReportLab is not installed

## File Locations

All exports are saved to:
```
CyberRecon-Pro/results/
```

Filename patterns:
- HTML: `report_{scan_id}_export.html`
- JSON: `scan_{scan_id}_export.json`
- CSV: `vulns_{scan_id}_export.csv`
- Markdown: `report_{scan_id}_export.md`
- PDF: `report_{scan_id}_export.pdf`

Where `{scan_id}` is the unique scan ID from the history table.

## Features Preserved in Exports

All export formats include:
- ✅ Target information
- ✅ Scan timing (started, ended, duration)
- ✅ Hosts discovered
- ✅ Services and versions
- ✅ Vulnerabilities with risk levels
- ✅ Risk summary (CRITICAL, HIGH, MEDIUM, LOW counts)
- ✅ SSL/TLS issues detected
- ✅ Scan profile used
- ✅ Unique Scan ID

## Benefits

### Time Savings
- No need to re-run scans to change report format
- Generate multiple formats from a single scan in seconds

### Compliance & Audit
- Create formatted reports for stakeholders
- Maintain audit trail of historical scans
- Export in format required by compliance team

### Batch Operations
- Export previous weeks' scans at once
- Archive old results in preferred format
- Share results with non-technical staff

## Troubleshooting

**Q: PDF export is not available**
- A: Install ReportLab: `pip install reportlab`

**Q: File says "export successful" but I can't find it**
- A: Check the `results/` folder in your CyberRecon-Pro directory
- Use the file path shown in the success message

**Q: HTML report opened but looks incomplete**
- A: This is normal for cached browser views. Try a fresh browser window or clear cache

**Q: Can I export multiple scans at once?**
- A: Current version exports one scan at a time. Select each scan individually and export

## Integration Tips

### Spreadsheet Analysis
1. Export as CSV
2. Open in Excel/Google Sheets
3. Filter by risk level, sort by CVSS score
4. Create pivot tables and charts

### Documentation
1. Export as Markdown
2. Add to your security wiki
3. Link to other documentation
4. Include in runbooks

### Archiving
1. Export as JSON and PDF
2. Store in document management system
3. Include metadata (scan date, team, approver)
4. Create monthly archive backups

---

**Version**: 1.0  
**Last Updated**: 2026-03-19

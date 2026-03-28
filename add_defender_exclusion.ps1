# Run this script as Administrator to add Windows Defender exclusion for Nikto
# Right-click this file  Run with PowerShell (as Administrator)

$niktoPath = "C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto"

Write-Host "Adding Windows Defender exclusion for: $niktoPath" -ForegroundColor Cyan

try {
    Add-MpPreference -ExclusionPath $niktoPath
    Write-Host " Exclusion added successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now restore nikto.pl:" -ForegroundColor Yellow
    Write-Host "  cd nikto" -ForegroundColor Gray
    Write-Host "  git restore program/nikto.pl" -ForegroundColor Gray
    Write-Host "  cd program" -ForegroundColor Gray
    Write-Host "  perl nikto.pl -Version" -ForegroundColor Gray
} catch {
    Write-Host " Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run this script as Administrator:" -ForegroundColor Yellow
    Write-Host "  Right-click  Run with PowerShell (as Administrator)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


# Permanent Perl PATH Setup - Run as Administrator
# This adds Perl to your system PATH permanently

$perlPath = "$env:USERPROFILE\Downloads\strawberry-perl-5.42.0.1-64bit-PDL\perl\bin"

Write-Host "Adding Perl to System PATH..." -ForegroundColor Cyan
Write-Host "Path: $perlPath" -ForegroundColor Gray

try {
    # Get current system PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    
    # Check if Perl is already in PATH
    if ($currentPath -like "*$perlPath*") {
        Write-Host " Perl is already in System PATH" -ForegroundColor Yellow
    } else {
        # Add Perl to system PATH
        $newPath = $currentPath + ";" + $perlPath
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Host " Perl added to System PATH successfully!" -ForegroundColor Green
        Write-Host "`nPlease restart your terminals for the changes to take effect." -ForegroundColor Yellow
    }
} catch {
    Write-Host " Error: $_" -ForegroundColor Red
    Write-Host "`nPlease run this script as Administrator:" -ForegroundColor Yellow
    Write-Host "  Right-click  Run with PowerShell (as Administrator)" -ForegroundColor Gray
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


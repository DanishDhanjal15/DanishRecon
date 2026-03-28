# Test script for Nikto - Verifies installation and functionality
#  Perl, Nikto, and Defender exclusion are already configured!

Write-Host "=== Nikto Installation Test ===" -ForegroundColor Cyan

# Test Perl
Write-Host "`nChecking Perl..." -ForegroundColor Yellow
perl --version | Select-String "perl 5"
if ($?) {
    Write-Host " Perl is accessible" -ForegroundColor Green
} else {
    Write-Host " Perl not found in PATH" -ForegroundColor Red
}

# Test Nikto
Write-Host "`nTesting Nikto..." -ForegroundColor Yellow
Set-Location "C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program"
perl nikto.pl -Version

if ($?) {
    Write-Host "`n Nikto is working correctly!" -ForegroundColor Green
    Write-Host "`nExample usage:" -ForegroundColor Cyan
    Write-Host "  perl nikto.pl -h http://example.com" -ForegroundColor Gray
    Write-Host "  perl nikto.pl -h https://testphp.vulnweb.com" -ForegroundColor Gray
    Write-Host "`nFor all options:" -ForegroundColor Cyan
    Write-Host "  perl nikto.pl -Help" -ForegroundColor Gray
} else {
    Write-Host "`n Nikto test failed" -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


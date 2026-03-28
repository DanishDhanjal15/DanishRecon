# Diagnostic script to test Nikto with different configurations
# Useful for troubleshooting slow or hanging Nikto scans

Write-Host "=== Nikto Diagnostic Tool ===" -ForegroundColor Cyan
Write-Host ""

# Target configuration
$target_host = "protego.zssh.dev"
$target_port = 443
$use_ssl = $true
$nikto_path = "C:\Users\Danish\OneDrive\Desktop\recon cyber\nikto\program\nikto.pl"

Write-Host "Target: $target_host`:$target_port" -ForegroundColor Yellow
Write-Host "SSL: $use_ssl" -ForegroundColor Yellow
Write-Host ""

# Pre-flight connectivity check
Write-Host "[1/5] Testing TCP connectivity..." -ForegroundColor Cyan
try {
    $socket = New-Object System.Net.Sockets.TcpClient
    $socket.SendTimeout = 3000
    $socket.ReceiveTimeout = 3000
    $socket.Connect($target_host, $target_port)
    Write-Host "  ✓ TCP connection successful" -ForegroundColor Green
    $socket.Close()
} catch {
    Write-Host "  ✗ TCP connection failed: $_" -ForegroundColor Red
    Write-Host "  Cannot proceed with Nikto scan - host unreachable" -ForegroundColor Red
    exit 1
}

# Test with standard timeout
Write-Host ""
Write-Host "[2/5] Testing standard Nikto (140s timeout)..." -ForegroundColor Cyan
$ssl_flag = if ($use_ssl) { "-ssl" } else { "" }
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$cmd = @("perl", $nikto_path, "-h", $target_host, "-p", $target_port, "-nointeractive", "-ask", "no", $ssl_flag)
$cmd = $cmd | Where-Object { $_ -ne "" }

Write-Host "  Command: perl nikto.pl -h $target_host -p $target_port $ssl_flag -nointeractive -ask no"
Write-Host "  Running (timeout: 140s)..." -ForegroundColor Gray

try {
    $output = & {
        $process = Start-Process -FilePath "perl" -ArgumentList ($nikto_path, "-h", $target_host, "-p", $target_port, "-nointeractive", "-ask", "no", $ssl_flag) -NoNewWindow -RedirectStandardOutput .\nikto_test_stdout.txt -RedirectStandardError .\nikto_test_stderr.txt -PassThru
        $process | Wait-Process -Timeout 140 -ErrorAction Stop
        Get-Content .\nikto_test_stdout.txt -ErrorAction SilentlyContinue
        Get-Content .\nikto_test_stderr.txt -ErrorAction SilentlyContinue
    } 2>&1
    
    $stopwatch.Stop()
    Write-Host "  ✓ Completed in $($stopwatch.ElapsedMilliseconds)ms" -ForegroundColor Green
    
    # Parse output for vulnerability count
    $vuln_count = ($output | Select-String "found on target" | Measure-Object | Select-Object Count).Count
    Write-Host "  Vulnerabilities found: $vuln_count" -ForegroundColor Yellow
    
} catch {
    $stopwatch.Stop()
    Write-Host "  ✗ TIMEOUT after $($stopwatch.ElapsedSeconds)s" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Output so far:" -ForegroundColor Gray
    Get-Content .\nikto_test_stdout.txt -ErrorAction SilentlyContinue | Select-Object -First 20
}

Write-Host ""
Write-Host "[3/5] Testing with -noclean (faster)..." -ForegroundColor Cyan
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "  Command: perl nikto.pl -h $target_host -p $target_port $ssl_flag -nointeractive -ask no -noclean"
Write-Host "  Running (timeout: 200s)..." -ForegroundColor Gray

try {
    $output = & {
        $process = Start-Process -FilePath "perl" -ArgumentList ($nikto_path, "-h", $target_host, "-p", $target_port, "-nointeractive", "-ask", "no", "-noclean", $ssl_flag) -NoNewWindow -RedirectStandardOutput .\nikto_test2_stdout.txt -RedirectStandardError .\nikto_test2_stderr.txt -PassThru
        $process | Wait-Process -Timeout 200 -ErrorAction Stop
        Get-Content .\nikto_test2_stdout.txt -ErrorAction SilentlyContinue
        Get-Content .\nikto_test2_stderr.txt -ErrorAction SilentlyContinue
    } 2>&1
    
    $stopwatch.Stop()
    Write-Host "  ✓ Completed in $($stopwatch.ElapsedMilliseconds)ms" -ForegroundColor Green
    
} catch {
    $stopwatch.Stop()
    Write-Host "  ✗ TIMEOUT after $($stopwatch.ElapsedSeconds)s" -ForegroundColor Red
}

Write-Host ""
Write-Host "[4/5] Testing with reduced plugins (-Plugins default)..." -ForegroundColor Cyan
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "  Running minimal plugin set (timeout: 120s)..." -ForegroundColor Gray

try {
    $output = & {
        $process = Start-Process -FilePath "perl" -ArgumentList ($nikto_path, "-h", $target_host, "-p", $target_port, "-nointeractive", "-ask", "no", "-Plugins", "default", $ssl_flag) -NoNewWindow -RedirectStandardOutput .\nikto_test3_stdout.txt -RedirectStandardError .\nikto_test3_stderr.txt -PassThru
        $process | Wait-Process -Timeout 120 -ErrorAction Stop
        Get-Content .\nikto_test3_stdout.txt -ErrorAction SilentlyContinue
        Get-Content .\nikto_test3_stderr.txt -ErrorAction SilentlyContinue
    } 2>&1
    
    $stopwatch.Stop()
    Write-Host "  ✓ Completed in $($stopwatch.ElapsedMilliseconds)ms" -ForegroundColor Green
    
} catch {
    $stopwatch.Stop()
    Write-Host "  ✗ TIMEOUT after $($stopwatch.ElapsedSeconds)s" -ForegroundColor Red
}

Write-Host ""
Write-Host "[5/5] Summary and Recommendations" -ForegroundColor Cyan
Write-Host ""

# Check which tests passed
$test1_ok = Test-Path .\nikto_test_stdout.txt -ErrorAction SilentlyContinue
$test2_ok = Test-Path .\nikto_test2_stdout.txt -ErrorAction SilentlyContinue
$test3_ok = Test-Path .\nikto_test3_stdout.txt -ErrorAction SilentlyContinue

if ($test1_ok) {
    Write-Host "✓ Test 1 (standard): PASSED" -ForegroundColor Green
} else {
    Write-Host "✗ Test 1 (standard): TIMEOUT - host responds slowly to standard scan" -ForegroundColor Red
}

if ($test2_ok) {
    Write-Host "✓ Test 2 (-noclean): PASSED - Try using -noclean flag" -ForegroundColor Green
} else {
    Write-Host "✗ Test 2 (-noclean): TIMEOUT - even optimized scan times out" -ForegroundColor Yellow
}

if ($test3_ok) {
    Write-Host "✓ Test 3 (default plugins): PASSED - Try using default plugins only" -ForegroundColor Green
} else {
    Write-Host "✗ Test 3 (default plugins): TIMEOUT - even minimal plugins timeout" -ForegroundColor Red
}

Write-Host ""
Write-Host "Recommendations:" -ForegroundColor Cyan
if (-not $test1_ok -and $test2_ok) {
    Write-Host "  • Target is slow but scannable with -noclean flag" -ForegroundColor Yellow
    Write-Host "  • Update CyberRecon-Pro to use -noclean and increase timeout to 240s" -ForegroundColor Yellow
} elseif (-not $test1_ok -and $test3_ok) {
    Write-Host "  • Target responds better with reduced plugins" -ForegroundColor Yellow
    Write-Host "  • Consider using -Plugins default and increase timeout" -ForegroundColor Yellow
} elseif (-not $test2_ok) {
    Write-Host "  • Target is extremely slow or may be blocking/rate-limiting" -ForegroundColor Red
    Write-Host "  • Consider:" -ForegroundColor Red
    Write-Host "    - Checking network connectivity and routing" -ForegroundColor Red
    Write-Host "    - Testing from different network" -ForegroundColor Red
    Write-Host "    - Contacting target administrator" -ForegroundColor Red
    Write-Host "    - Using IP address instead of hostname" -ForegroundColor Red
} else {
    Write-Host "  • All tests passed - Nikto is responsive on this target" -ForegroundColor Green
    Write-Host "  • Increase timeout in CyberRecon-Pro to 300s for reliability" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

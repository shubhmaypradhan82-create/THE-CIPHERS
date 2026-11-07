$ErrorActionPreference = 'Stop'
$backend = Join-Path $PSScriptRoot 'backend'
$envFile = Join-Path $backend '.env'
$email = Read-Host 'Admin email'
$name = Read-Host 'Admin display name'
$secure = Read-Host 'Admin password' -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try { $password = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
if ($password.Length -lt 12) { throw 'Use an admin password of at least 12 characters.' }
@("DATABASE_URL=sqlite:///./email_threat_detection.db", "ADMIN_EMAIL=$email", "ADMIN_PASSWORD=$password", "ADMIN_NAME=$name", "RESET_ADMIN_PASSWORD=true") | Set-Content -Path $envFile -Encoding UTF8
Write-Host "Admin configuration written to backend\.env" -ForegroundColor Green
Write-Host "Start the backend, then choose Admin on the CHIPERS login screen." -ForegroundColor Cyan

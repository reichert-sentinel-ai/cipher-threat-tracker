# Restart Frontend Dev Server Script
# Finds Node.js, adds to PATH, and starts the frontend server

Write-Host "🔄 Restarting Frontend Dev Server..." -ForegroundColor Cyan
Write-Host ""

# Check if port 5173 is in use and stop it
$portProcess = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($portProcess) {
    Write-Host "🛑 Stopping existing frontend server (PID: $portProcess)..." -ForegroundColor Yellow
    Stop-Process -Id $portProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# Find Node.js installation
$nodePaths = @(
    "C:\Program Files\nodejs",
    "C:\Program Files (x86)\nodejs",
    "$env:LOCALAPPDATA\Programs\nodejs",
    "$env:APPDATA\npm"
)

$nodeDir = $null
$npmPath = $null

foreach ($path in $nodePaths) {
    if (Test-Path $path) {
        $testNpmPath = Join-Path $path "npm.cmd"
        if (Test-Path $testNpmPath) {
            $nodeDir = $path
            $npmPath = $testNpmPath
            break
        }
    }
}

if (-not $nodeDir) {
    # Try to find node.exe in PATH from running processes
    $nodeProcess = Get-Process node -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($nodeProcess) {
        $nodeExe = $nodeProcess.Path
        $nodeDir = Split-Path $nodeExe
        $npmPath = Join-Path $nodeDir "npm.cmd"
        if (-not (Test-Path $npmPath)) {
            $npmPath = $null
        }
    }
}

if (-not $nodeDir -or -not $npmPath) {
    Write-Host "❌ Node.js not found. Please install Node.js or add it to PATH manually." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found Node.js at: $nodeDir" -ForegroundColor Green

# Verify npm is available using full path
try {
    $npmVersion = & $npmPath --version 2>&1
    Write-Host "✅ npm version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not available at: $npmPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting Frontend Dev Server..." -ForegroundColor Yellow
Write-Host ""

# Change to frontend directory and start server
$frontendDir = Join-Path $PSScriptRoot "frontend"
if (-not (Test-Path $frontendDir)) {
    Write-Host "❌ Frontend directory not found: $frontendDir" -ForegroundColor Red
    exit 1
}

cd $frontendDir

# Start the dev server in a new window with full npm path
# Use environment variable to pass Node.js path
$env:NODE_DIR = $nodeDir
$env:NPM_PATH = $npmPath

$command = @"
cd '$frontendDir'
`$env:PATH = '$nodeDir;' + `$env:PATH
Write-Host '🎨 Frontend Dev Server Starting...' -ForegroundColor Cyan
Write-Host '📍 Using Node.js: $nodeDir' -ForegroundColor Gray
& '$npmPath' run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $command

Write-Host "✅ Frontend server starting in new window..." -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access: http://localhost:5173" -ForegroundColor Cyan
Write-Host "📍 MITRE ATT&CK: http://localhost:5173/mitre-attack" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏳ Waiting 5 seconds to verify server started..." -ForegroundColor Gray
Start-Sleep -Seconds 5

# Check if server is running
$serverRunning = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue
if ($serverRunning) {
    Write-Host "✅ Frontend dev server is RUNNING on port 5173!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Server may still be starting. Check the new window for status." -ForegroundColor Yellow
}

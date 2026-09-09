<#
push_sync.ps1

Merge `origin/main` into `zhangruiyang` and push with error handling.
Usage:
  pwsh -File .\scripts\push_sync.ps1
  or
  .\scripts\push_sync.ps1

Options:
  -AutoAbortOnConflict : automatically abort merge on conflict and exit non-zero
  -PushRetries <n>      : number of push retries (default 3)
#>

param(
    [switch]$AutoAbortOnConflict,
    [int]$PushRetries = 3
)

function Fail([string]$msg, [int]$code=1) {
    Write-Host "ERROR: $msg" -ForegroundColor Red
    exit $code
}

function Info([string]$msg) { Write-Host "INFO: $msg" -ForegroundColor Cyan }

# Ensure git is available
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCmd) {
    # Look for common Git for Windows install locations
    $possible = @(
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles(x86)\Git\cmd\git.exe",
        "$env:LocalAppData\Programs\Git\cmd\git.exe"
    )
    $found = $possible | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($found) {
        Write-Host "git executable found at: $found" -ForegroundColor Yellow
        Write-Host "It appears git is installed but not on your PATH." -ForegroundColor Cyan
        Write-Host "Quick fixes:" -ForegroundColor Cyan
        Write-Host "  - Reopen this terminal (some installers add git to PATH only after restart)." -ForegroundColor Green
        Write-Host "  - Run the script from 'Git Bash' or a terminal where git is available." -ForegroundColor Green
        Write-Host "  - Add Git's `cmd` folder to your PATH (example PowerShell command below):" -ForegroundColor Green
        $cmdDir = Split-Path $found -Parent
        Write-Host "    [Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH','User') + ';$cmdDir', 'User')" -ForegroundColor Magenta
        Write-Host "After adding to PATH, restart your terminal and rerun this script." -ForegroundColor Cyan
        Fail 'git is installed but not on PATH. Add it to PATH and reopen terminal.' 2
    } else {
        Write-Host "git command not found on PATH." -ForegroundColor Red
        Write-Host "Install Git for Windows: https://git-scm.com/download/win" -ForegroundColor Cyan
        Write-Host "Or open 'Git Bash' which includes git on PATH by default." -ForegroundColor Cyan
        Write-Host "After installing, restart your terminal and rerun this script." -ForegroundColor Cyan
        Fail 'git command not found. Install Git and ensure it is on PATH.' 2
    }
}

# Ensure we're inside a git repo
$top = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) { Fail 'Not inside a git repository.' 3 }

Info "Repository root: $top"

# Require clean working tree
$dirty = git status --porcelain
if ($dirty) {
    Write-Host "Working tree is dirty. Please commit or stash changes before running this script." -ForegroundColor Yellow
    git status --porcelain
    Fail 'Aborting due to uncommitted changes.' 4
}

# Fetch origin main
Info 'Fetching origin/main...'
git fetch origin main
if ($LASTEXITCODE -ne 0) { Fail 'Failed to fetch origin/main.' 5 }

# Ensure or create/check out zhangruiyang branch
$branch = 'zhangruiyang'
git rev-parse --verify $branch 2>$null
if ($LASTEXITCODE -eq 0) {
    Info "Checking out existing branch '$branch'..."
    git checkout $branch
    if ($LASTEXITCODE -ne 0) { Fail "Failed to checkout $branch." 6 }
} else {
    # Try to track remote if exists
    git ls-remote --heads origin $branch > $null
    if ($LASTEXITCODE -eq 0) {
        Info "Creating local branch '$branch' tracking origin/$branch..."
        git checkout -b $branch origin/$branch
        if ($LASTEXITCODE -ne 0) { Fail "Failed to create and checkout $branch from origin/$branch." 7 }
    } else {
        Info "Creating new local branch '$branch'..."
        git checkout -b $branch
        if ($LASTEXITCODE -ne 0) { Fail "Failed to create and checkout $branch." 8 }
    }
}

# Merge origin/main
Info 'Merging origin/main into current branch...'
$mergeOutput = git merge --no-ff origin/main -m "Merge origin/main into $branch" 2>&1
$mergeCode = $LASTEXITCODE
if ($mergeCode -ne 0) {
    # Check for conflicts
    $unmerged = git ls-files -u
    if ($unmerged) {
        Write-Host "Merge produced conflicts:" -ForegroundColor Yellow
        git status --short
        git ls-files -u | Select-Object -First 50
        if ($AutoAbortOnConflict) {
            Info 'Auto-aborting merge due to conflicts...'
            git merge --abort
            Fail 'Merge aborted due to conflicts. Resolve manually and rerun.' 9
        } else {
            Fail 'Merge resulted in conflicts. Resolve them manually, then commit.' 10
        }
    } else {
        Write-Host "Merge failed:" -ForegroundColor Yellow
        Write-Host $mergeOutput
        Fail 'Merge failed (non-conflict error).' 11
    }
}

Info 'Merge successful.'

# Push with retries
$attempt = 0
while ($attempt -lt $PushRetries) {
    $attempt++
    Info "Pushing to origin/$branch (attempt $attempt of $PushRetries)..."
    git push origin $branch
    if ($LASTEXITCODE -eq 0) {
        Info 'Push succeeded.'
        exit 0
    } else {
        Write-Host "Push failed on attempt $attempt." -ForegroundColor Yellow
        Start-Sleep -Seconds (5 * $attempt)
    }
}

Fail "Push failed after $PushRetries attempts." 12

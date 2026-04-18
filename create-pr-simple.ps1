# Simple PR Creation Script
Write-Host "Creating Pull Request..." -ForegroundColor Cyan

# Get repository info
$repoUrl = git config --get remote.origin.url
$repoUrl = $repoUrl -replace "\.git$", ""
$repoUrl = $repoUrl -replace "git@github.com:", "https://github.com/"

# Get current branch
$currentBranch = git branch --show-current

Write-Host "Repository: $repoUrl" -ForegroundColor Green
Write-Host "Branch: $currentBranch" -ForegroundColor Green

# Construct PR URL
$prUrl = "$repoUrl/compare/main...$currentBranch"

Write-Host "Opening: $prUrl" -ForegroundColor Yellow

# Open in browser
Start-Process $prUrl

Write-Host "`nPR Title:" -ForegroundColor Cyan
Write-Host "Add Skechers Staging Tests + Fix All CI/CD Issues" -ForegroundColor White

Write-Host "`nSuggested Description:" -ForegroundColor Cyan
Write-Host "See ALL_CI_FIXES_SUMMARY.md for complete details" -ForegroundColor White

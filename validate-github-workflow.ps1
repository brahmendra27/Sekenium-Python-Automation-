# GitHub Actions Workflow Local Validation Script
# This script simulates the GitHub Actions workflow locally to validate all components

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Actions Workflow Validation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Track validation results
$validationResults = @()

# Function to add validation result
function Add-ValidationResult {
    param(
        [string]$Test,
        [bool]$Passed,
        [string]$Message
    )
    
    $result = @{
        Test = $Test
        Passed = $Passed
        Message = $Message
    }
    $script:validationResults += $result
    
    if ($Passed) {
        Write-Host "[PASS] $Test" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $Test" -ForegroundColor Red
    }
    Write-Host "       $Message" -ForegroundColor Gray
    Write-Host ""
}

# Test 1: Verify workflow file exists
Write-Host "Test 1: Verify workflow file exists..." -ForegroundColor Yellow
$workflowPath = ".github/workflows/test.yml"
if (Test-Path $workflowPath) {
    Add-ValidationResult -Test "Workflow file exists" -Passed $true -Message "Found $workflowPath"
} else {
    Add-ValidationResult -Test "Workflow file exists" -Passed $false -Message "Missing $workflowPath"
}

# Test 2: Verify workflow syntax (basic check)
Write-Host "Test 2: Verify workflow syntax..." -ForegroundColor Yellow
try {
    $workflowContent = Get-Content $workflowPath -Raw
    if ($workflowContent -match "on:" -and $workflowContent -match "jobs:" -and $workflowContent -match "steps:") {
        Add-ValidationResult -Test "Workflow syntax" -Passed $true -Message "Workflow file has valid structure"
    } else {
        Add-ValidationResult -Test "Workflow syntax" -Passed $false -Message "Workflow file missing required sections"
    }
} catch {
    Add-ValidationResult -Test "Workflow syntax" -Passed $false -Message "Error reading workflow file: $_"
}

# Test 3: Verify trigger configuration
Write-Host "Test 3: Verify trigger configuration..." -ForegroundColor Yellow
if ($workflowContent -match "pull_request:" -and $workflowContent -match "push:") {
    Add-ValidationResult -Test "Trigger configuration" -Passed $true -Message "Workflow triggers on push and pull_request"
} else {
    Add-ValidationResult -Test "Trigger configuration" -Passed $false -Message "Missing required triggers"
}

# Test 4: Verify Docker configuration
Write-Host "Test 4: Verify Docker configuration..." -ForegroundColor Yellow
if ($workflowContent -match "docker/build-push-action" -and $workflowContent -match "docker/Dockerfile") {
    Add-ValidationResult -Test "Docker configuration" -Passed $true -Message "Docker build action configured correctly"
} else {
    Add-ValidationResult -Test "Docker configuration" -Passed $false -Message "Docker build action not configured"
}

# Test 5: Verify artifact upload configuration
Write-Host "Test 5: Verify artifact upload configuration..." -ForegroundColor Yellow
$hasHtmlUpload = $workflowContent -match "html-report"
$hasJsonUpload = $workflowContent -match "json-report"
$hasScreenshotUpload = $workflowContent -match "screenshots"
$hasTraceUpload = $workflowContent -match "traces"

if ($hasHtmlUpload -and $hasJsonUpload -and $hasScreenshotUpload -and $hasTraceUpload) {
    Add-ValidationResult -Test "Artifact upload configuration" -Passed $true -Message "All artifact uploads configured (HTML, JSON, screenshots, traces)"
} else {
    $missing = @()
    if (-not $hasHtmlUpload) { $missing += "HTML" }
    if (-not $hasJsonUpload) { $missing += "JSON" }
    if (-not $hasScreenshotUpload) { $missing += "screenshots" }
    if (-not $hasTraceUpload) { $missing += "traces" }
    Add-ValidationResult -Test "Artifact upload configuration" -Passed $false -Message "Missing artifact uploads: $($missing -join ', ')"
}

# Test 6: Verify failure detection
Write-Host "Test 6: Verify failure detection..." -ForegroundColor Yellow
if ($workflowContent -match "continue-on-error: true" -and $workflowContent -match "if: steps.run-tests.outcome == 'failure'") {
    Add-ValidationResult -Test "Failure detection" -Passed $true -Message "Workflow configured to detect and report test failures"
} else {
    Add-ValidationResult -Test "Failure detection" -Passed $false -Message "Failure detection not properly configured"
}

# Test 7: Verify Docker layer caching
Write-Host "Test 7: Verify Docker layer caching..." -ForegroundColor Yellow
if ($workflowContent -match "cache-from: type=gha" -and $workflowContent -match "cache-to: type=gha") {
    Add-ValidationResult -Test "Docker layer caching" -Passed $true -Message "GitHub Actions cache configured for Docker layers"
} else {
    Add-ValidationResult -Test "Docker layer caching" -Passed $false -Message "Docker layer caching not configured"
}

# Test 8: Run tests locally to verify exit codes
Write-Host "Test 8: Verify test execution and exit codes..." -ForegroundColor Yellow

# Test 8a: Passing tests
Write-Host "  Running passing tests..." -ForegroundColor Gray
pytest tests/test_config.py --headless -q 2>&1 | Out-Null
$passingExitCode = $LASTEXITCODE

if ($passingExitCode -eq 0) {
    Add-ValidationResult -Test "Passing tests exit code" -Passed $true -Message "Passing tests return exit code 0"
} else {
    Add-ValidationResult -Test "Passing tests exit code" -Passed $false -Message "Passing tests returned exit code $passingExitCode (expected 0)"
}

# Test 8b: Failing tests
Write-Host "  Creating and running failing test..." -ForegroundColor Gray
$failingTestContent = @"
import pytest

@pytest.mark.selenium
def test_validation_failure():
    assert False, "Validation test"
"@
Set-Content -Path "tests/test_validation_temp.py" -Value $failingTestContent

pytest tests/test_validation_temp.py --headless -q 2>&1 | Out-Null
$failingExitCode = $LASTEXITCODE

Remove-Item "tests/test_validation_temp.py" -Force

if ($failingExitCode -ne 0) {
    Add-ValidationResult -Test "Failing tests exit code" -Passed $true -Message "Failing tests return non-zero exit code ($failingExitCode)"
} else {
    Add-ValidationResult -Test "Failing tests exit code" -Passed $false -Message "Failing tests returned exit code 0 (expected non-zero)"
}

# Test 9: Verify report generation
Write-Host "Test 9: Verify report generation..." -ForegroundColor Yellow
$htmlReport = "reports/report.html"
$jsonReport = "reports/report.json"

if ((Test-Path $htmlReport) -and (Test-Path $jsonReport)) {
    Add-ValidationResult -Test "Report generation" -Passed $true -Message "HTML and JSON reports generated successfully"
} else {
    $missing = @()
    if (-not (Test-Path $htmlReport)) { $missing += "HTML" }
    if (-not (Test-Path $jsonReport)) { $missing += "JSON" }
    Add-ValidationResult -Test "Report generation" -Passed $false -Message "Missing reports: $($missing -join ', ')"
}

# Test 10: Verify report directories
Write-Host "Test 10: Verify report directories..." -ForegroundColor Yellow
$screenshotDir = "reports/screenshots"
$traceDir = "reports/traces"

if ((Test-Path $screenshotDir) -and (Test-Path $traceDir)) {
    Add-ValidationResult -Test "Report directories" -Passed $true -Message "Screenshot and trace directories exist"
} else {
    $missing = @()
    if (-not (Test-Path $screenshotDir)) { $missing += "screenshots" }
    if (-not (Test-Path $traceDir)) { $missing += "traces" }
    Add-ValidationResult -Test "Report directories" -Passed $false -Message "Missing directories: $($missing -join ', ')"
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Validation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalTests = $validationResults.Count
$passedTests = ($validationResults | Where-Object { $_.Passed }).Count
$failedTests = $totalTests - $passedTests

Write-Host "Total Tests: $totalTests" -ForegroundColor White
Write-Host "Passed: $passedTests" -ForegroundColor Green
Write-Host "Failed: $failedTests" -ForegroundColor $(if ($failedTests -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($failedTests -eq 0) {
    Write-Host "All validations passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The GitHub Actions workflow is correctly configured and ready for testing." -ForegroundColor Green
    Write-Host "To test in GitHub:" -ForegroundColor Yellow
    Write-Host "  1. Create a GitHub repository" -ForegroundColor Gray
    Write-Host "  2. Add remote: git remote add origin [repo-url]" -ForegroundColor Gray
    Write-Host "  3. Push: git push -u origin main" -ForegroundColor Gray
    Write-Host "  4. Create a test branch and open a PR" -ForegroundColor Gray
    Write-Host ""
    exit 0
} else {
    Write-Host "Some validations failed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Failed tests:" -ForegroundColor Yellow
    foreach ($result in $validationResults) {
        if (-not $result.Passed) {
            Write-Host ("  - " + $result.Test + ": " + $result.Message) -ForegroundColor Red
        }
    }
    Write-Host ""
    exit 1
}

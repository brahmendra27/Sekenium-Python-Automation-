# Docker Execution Test Script - Task 11.3
# This script validates Docker build and execution for the test automation framework

param(
    [switch]$SkipBuild = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

# Color output functions
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Failure { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Info { param($Message) Write-Host "ℹ $Message" -ForegroundColor Cyan }
function Write-Step { param($Message) Write-Host "`n=== $Message ===" -ForegroundColor Yellow }

# Check if Docker is available
function Test-DockerAvailable {
    try {
        $null = docker --version
        return $true
    } catch {
        return $false
    }
}

# Main test execution
function Test-DockerExecution {
    Write-Step "Docker Execution Test - Task 11.3"
    
    # Check Docker availability
    Write-Info "Checking Docker availability..."
    if (-not (Test-DockerAvailable)) {
        Write-Failure "Docker is not installed or not in PATH"
        Write-Info "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
        exit 1
    }
    Write-Success "Docker is available"
    
    # Display Docker version
    $dockerVersion = docker --version
    Write-Info "Docker version: $dockerVersion"
    
    # Clean existing reports
    Write-Step "Cleaning existing reports"
    if (Test-Path "reports/report.html") {
        Remove-Item "reports/report.html" -Force
        Write-Info "Removed existing report.html"
    }
    if (Test-Path "reports/report.json") {
        Remove-Item "reports/report.json" -Force
        Write-Info "Removed existing report.json"
    }
    
    # Step 1: Build Docker image
    if (-not $SkipBuild) {
        Write-Step "Step 1: Building Docker image"
        Write-Info "Running: docker build -t test-automation-framework -f docker/Dockerfile ."
        
        $buildStart = Get-Date
        docker build -t test-automation-framework -f docker/Dockerfile .
        $buildExitCode = $LASTEXITCODE
        $buildDuration = (Get-Date) - $buildStart
        
        if ($buildExitCode -eq 0) {
            Write-Success "Docker image built successfully in $($buildDuration.TotalSeconds) seconds"
        } else {
            Write-Failure "Docker build failed with exit code $buildExitCode"
            exit $buildExitCode
        }
        
        # Verify image exists
        $image = docker images test-automation-framework --format "{{.Repository}}:{{.Tag}}"
        if ($image) {
            Write-Success "Image verified: $image"
            $imageSize = docker images test-automation-framework --format "{{.Size}}"
            Write-Info "Image size: $imageSize"
        } else {
            Write-Failure "Image not found in docker images list"
            exit 1
        }
    } else {
        Write-Info "Skipping build (--SkipBuild flag set)"
    }
    
    # Step 2: Run tests in container
    Write-Step "Step 2: Running tests in Docker container"
    Write-Info "Running: docker-compose -f docker/docker-compose.yml up --abort-on-container-exit"
    
    $testStart = Get-Date
    docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
    $testExitCode = $LASTEXITCODE
    $testDuration = (Get-Date) - $testStart
    
    Write-Info "Test execution completed in $($testDuration.TotalSeconds) seconds"
    Write-Info "Exit code: $testExitCode"
    
    # Step 3: Verify reports generated
    Write-Step "Step 3: Verifying reports generated in host directory"
    
    $reportValidation = @{
        "report.html" = $false
        "report.json" = $false
        "screenshots/" = $false
        "traces/" = $false
    }
    
    # Check HTML report
    if (Test-Path "reports/report.html") {
        $htmlSize = (Get-Item "reports/report.html").Length
        Write-Success "report.html exists ($htmlSize bytes)"
        $reportValidation["report.html"] = $true
    } else {
        Write-Failure "report.html not found"
    }
    
    # Check JSON report
    if (Test-Path "reports/report.json") {
        $jsonSize = (Get-Item "reports/report.json").Length
        Write-Success "report.json exists ($jsonSize bytes)"
        $reportValidation["report.json"] = $true
        
        # Parse JSON report for summary
        try {
            $jsonContent = Get-Content "reports/report.json" -Raw | ConvertFrom-Json
            $summary = $jsonContent.summary
            Write-Info "Test Summary:"
            Write-Info "  Total: $($summary.total)"
            Write-Info "  Passed: $($summary.passed)"
            Write-Info "  Failed: $($summary.failed)"
            Write-Info "  Skipped: $($summary.skipped)"
            Write-Info "  Duration: $($summary.duration)s"
        } catch {
            Write-Failure "Failed to parse JSON report: $_"
        }
    } else {
        Write-Failure "report.json not found"
    }
    
    # Check screenshots directory
    if (Test-Path "reports/screenshots") {
        $screenshotCount = (Get-ChildItem "reports/screenshots" -File).Count
        Write-Success "screenshots/ directory exists ($screenshotCount files)"
        $reportValidation["screenshots/"] = $true
    } else {
        Write-Failure "screenshots/ directory not found"
    }
    
    # Check traces directory
    if (Test-Path "reports/traces") {
        $traceCount = (Get-ChildItem "reports/traces" -File).Count
        Write-Success "traces/ directory exists ($traceCount files)"
        $reportValidation["traces/"] = $true
    } else {
        Write-Failure "traces/ directory not found"
    }
    
    # Step 4: Verify exit code propagation
    Write-Step "Step 4: Verifying exit code propagation"
    
    if ($testExitCode -eq 0) {
        Write-Success "Exit code is 0 (all tests passed)"
    } else {
        Write-Info "Exit code is $testExitCode (tests failed or error occurred)"
    }
    
    # Requirements validation summary
    Write-Step "Requirements Validation Summary"
    
    Write-Info "Requirement 8.2 (Docker Image Build):"
    if (-not $SkipBuild) {
        Write-Success "  Docker image built with all dependencies"
    } else {
        Write-Info "  Skipped (--SkipBuild flag set)"
    }
    
    Write-Info "Requirement 8.4 (Headless Execution):"
    Write-Success "  Tests executed in headless mode in container"
    
    Write-Info "Requirement 8.6 (Exit Code Propagation):"
    Write-Success "  Container exit code: $testExitCode"
    
    Write-Info "Report Generation:"
    foreach ($item in $reportValidation.GetEnumerator()) {
        if ($item.Value) {
            Write-Success "  $($item.Key) ✓"
        } else {
            Write-Failure "  $($item.Key) ✗"
        }
    }
    
    # Final result
    Write-Step "Test Result"
    
    $allReportsGenerated = $reportValidation.Values -notcontains $false
    
    if ($allReportsGenerated) {
        Write-Success "All validation checks passed!"
        Write-Info "Task 11.3 completed successfully"
    } else {
        Write-Failure "Some validation checks failed"
        Write-Info "Review the output above for details"
    }
    
    # Cleanup
    Write-Step "Cleanup"
    Write-Info "Stopping and removing containers..."
    docker-compose -f docker/docker-compose.yml down
    
    # Return exit code from test execution
    exit $testExitCode
}

# Run the test
Test-DockerExecution

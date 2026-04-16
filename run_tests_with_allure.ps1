# PowerShell script to run tests with Allure reporting
# Usage: .\run_tests_with_allure.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Automation with Allure Reporting" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Allure is installed
$allureInstalled = $null -ne (Get-Command allure -ErrorAction SilentlyContinue)

if (-not $allureInstalled) {
    Write-Host "⚠️  Allure command-line tool not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please install Allure using one of these methods:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Using Scoop (Recommended)" -ForegroundColor White
    Write-Host "  1. Install Scoop: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; irm get.scoop.sh | iex" -ForegroundColor Gray
    Write-Host "  2. Install Allure: scoop install allure" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Using npm" -ForegroundColor White
    Write-Host "  npm install -g allure-commandline" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Manual Download" -ForegroundColor White
    Write-Host "  1. Download from: https://github.com/allure-framework/allure2/releases" -ForegroundColor Gray
    Write-Host "  2. Extract to C:\allure" -ForegroundColor Gray
    Write-Host "  3. Add C:\allure\bin to PATH" -ForegroundColor Gray
    Write-Host ""
    
    $install = Read-Host "Would you like to install Allure via Scoop now? (y/n)"
    
    if ($install -eq "y" -or $install -eq "Y") {
        Write-Host ""
        Write-Host "Installing Scoop..." -ForegroundColor Green
        
        # Check if Scoop is installed
        $scoopInstalled = $null -ne (Get-Command scoop -ErrorAction SilentlyContinue)
        
        if (-not $scoopInstalled) {
            Write-Host "Installing Scoop package manager..." -ForegroundColor Yellow
            Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
            Invoke-RestMethod get.scoop.sh | Invoke-Expression
        }
        
        Write-Host "Installing Allure..." -ForegroundColor Green
        scoop install allure
        
        Write-Host ""
        Write-Host "✅ Allure installed successfully!" -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Please install Allure manually and run this script again." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✅ Allure is installed" -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated!" -ForegroundColor Yellow
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Menu
Write-Host "Select test suite to run:" -ForegroundColor Cyan
Write-Host "1. Allure Demo Tests (Recommended)" -ForegroundColor White
Write-Host "2. All Playwright Tests" -ForegroundColor White
Write-Host "3. Registration Tests" -ForegroundColor White
Write-Host "4. Shopping Cart Tests" -ForegroundColor White
Write-Host "5. Homepage Tests" -ForegroundColor White
Write-Host "6. Custom test path" -ForegroundColor White
Write-Host "7. View existing Allure report" -ForegroundColor White
Write-Host "8. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-8)"

$testPath = ""

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Running Allure Demo Tests..." -ForegroundColor Green
        $testPath = "tests/playwright/test_allure_demo.py"
    }
    "2" {
        Write-Host ""
        Write-Host "Running All Playwright Tests..." -ForegroundColor Green
        $testPath = "tests/playwright/"
    }
    "3" {
        Write-Host ""
        Write-Host "Running Registration Tests..." -ForegroundColor Green
        $testPath = "tests/playwright/test_user_registration.py"
    }
    "4" {
        Write-Host ""
        Write-Host "Running Shopping Cart Tests..." -ForegroundColor Green
        $testPath = "tests/playwright/test_automation_store_cart.py"
    }
    "5" {
        Write-Host ""
        Write-Host "Running Homepage Tests..." -ForegroundColor Green
        $testPath = "tests/playwright/test_automation_store_homepage.py"
    }
    "6" {
        Write-Host ""
        $testPath = Read-Host "Enter test path (e.g., tests/playwright/test_example.py)"
    }
    "7" {
        Write-Host ""
        Write-Host "Opening existing Allure report..." -ForegroundColor Green
        
        if (Test-Path "reports/allure-results") {
            allure serve reports/allure-results
        } else {
            Write-Host "❌ No Allure results found. Please run tests first." -ForegroundColor Red
        }
        exit 0
    }
    "8" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

if ($testPath -ne "") {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Running Tests with Allure" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Clean old results
    if (Test-Path "reports/allure-results") {
        Write-Host "Cleaning old Allure results..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "reports/allure-results"
    }
    
    # Run tests with Allure
    pytest $testPath --alluredir=reports/allure-results -v
    
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Test execution completed!" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    if (Test-Path "reports/allure-results") {
        Write-Host "📊 Allure results generated!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Opening Allure report..." -ForegroundColor Green
        Write-Host ""
        Write-Host "⏳ Please wait while Allure generates the report..." -ForegroundColor Yellow
        Write-Host "   (This may take a few seconds)" -ForegroundColor Yellow
        Write-Host ""
        
        # Generate and serve Allure report
        allure serve reports/allure-results
    } else {
        Write-Host "⚠️  No Allure results found" -ForegroundColor Yellow
    }
    
    exit $exitCode
}

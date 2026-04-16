# PowerShell script to run Automation Test Store tests
# Usage: .\run_automation_store_tests.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Automation Test Store - Test Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
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
Write-Host "1. Homepage Tests (TC-001, TC-002)" -ForegroundColor White
Write-Host "2. Shopping Cart Tests (TC-003, TC-007)" -ForegroundColor White
Write-Host "3. All Tests" -ForegroundColor White
Write-Host "4. All Tests (Headless)" -ForegroundColor White
Write-Host "5. All Tests (Parallel)" -ForegroundColor White
Write-Host "6. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-6)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Running Homepage Tests..." -ForegroundColor Green
        pytest tests/selenium/test_automation_store_homepage.py -v
    }
    "2" {
        Write-Host ""
        Write-Host "Running Shopping Cart Tests..." -ForegroundColor Green
        pytest tests/selenium/test_automation_store_cart.py -v
    }
    "3" {
        Write-Host ""
        Write-Host "Running All Tests..." -ForegroundColor Green
        pytest tests/selenium/test_automation_store_homepage.py tests/selenium/test_automation_store_cart.py -v
    }
    "4" {
        Write-Host ""
        Write-Host "Running All Tests (Headless)..." -ForegroundColor Green
        pytest tests/selenium/test_automation_store_homepage.py tests/selenium/test_automation_store_cart.py --headless -v
    }
    "5" {
        Write-Host ""
        Write-Host "Running All Tests (Parallel)..." -ForegroundColor Green
        pytest tests/selenium/test_automation_store_homepage.py tests/selenium/test_automation_store_cart.py -n 2 -v
    }
    "6" {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test execution completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 View reports:" -ForegroundColor Yellow
Write-Host "   HTML: reports/report.html" -ForegroundColor White
Write-Host "   JSON: reports/report.json" -ForegroundColor White
Write-Host ""
Write-Host "Opening HTML report..." -ForegroundColor Green
Start-Process "reports\report.html"

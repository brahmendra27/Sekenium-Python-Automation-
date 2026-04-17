# Install API and Database Testing Dependencies
# Run this script to install the new dependencies for API and MongoDB testing

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing API & Database Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if pip is available
try {
    $pipVersion = pip --version
    Write-Host "✓ pip is available: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ pip is not available. Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
Write-Host ""

# Install dependencies
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Verify installation
    Write-Host "Verifying installation..." -ForegroundColor Yellow
    
    $verification = python -c "
import sys
try:
    import requests
    print('✓ requests installed')
except ImportError:
    print('✗ requests not found')
    sys.exit(1)

try:
    import pymongo
    print('✓ pymongo installed')
except ImportError:
    print('✗ pymongo not found')
    sys.exit(1)

try:
    import jsonschema
    print('✓ jsonschema installed')
except ImportError:
    print('✗ jsonschema not found')
    sys.exit(1)

try:
    import motor
    print('✓ motor installed')
except ImportError:
    print('✗ motor not found')
    sys.exit(1)

print('')
print('All dependencies verified successfully!')
"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Ready to use API and Database testing!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Update config.yaml with your API and MongoDB settings" -ForegroundColor White
        Write-Host "2. Start MongoDB: net start MongoDB" -ForegroundColor White
        Write-Host "3. Run example tests: pytest tests/api/ -v" -ForegroundColor White
        Write-Host "4. Read the Quick Start guide: API_DATABASE_QUICK_START.md" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "⚠ Some dependencies may not have installed correctly." -ForegroundColor Yellow
        Write-Host "Please check the output above for errors." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "✗ Installation failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

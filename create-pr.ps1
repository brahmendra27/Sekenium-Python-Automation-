# Create Pull Request Script
# This script opens the GitHub PR creation page in your default browser

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Creating Pull Request" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get repository info
$repoUrl = git config --get remote.origin.url
$repoUrl = $repoUrl -replace "\.git$", ""
$repoUrl = $repoUrl -replace "git@github.com:", "https://github.com/"

# Get current branch
$currentBranch = git branch --show-current

Write-Host "Repository: $repoUrl" -ForegroundColor Green
Write-Host "Branch: $currentBranch" -ForegroundColor Green
Write-Host ""

# Construct PR URL
$prUrl = "$repoUrl/compare/main...$currentBranch"

Write-Host "Opening PR creation page..." -ForegroundColor Yellow
Write-Host "URL: $prUrl" -ForegroundColor Gray
Write-Host ""

# Open in default browser
Start-Process $prUrl

Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Browser opened!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "PR Details to use:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Title:" -ForegroundColor Yellow
Write-Host "  Add Skechers Staging Tests + Fix CI/CD Issues" -ForegroundColor White
Write-Host ""
Write-Host "Description:" -ForegroundColor Yellow
Write-Host "  Copy from PR_SKECHERS_TESTS.md" -ForegroundColor White
Write-Host ""
Write-Host "Or use this summary:" -ForegroundColor Yellow
Write-Host ""

$prDescription = @"
## 🎯 Overview

This PR adds comprehensive Skechers staging tests and fixes critical CI/CD issues.

## 🔧 Critical Fixes

### Fix 1: Missing conftest.py in Docker (CRITICAL)
- **Issue:** All CI tests were failing with "fixture not found" errors
- **Cause:** conftest.py was not copied to Docker image
- **Fix:** Added conftest.py to Dockerfile
- **Impact:** All tests now have access to fixtures (api_client, mongodb_client, etc.)

### Fix 2: Docker Package Issues
- **Issue:** Docker build failing with package errors
- **Cause:** Unavailable and duplicate packages
- **Fix:** Cleaned up package list in Dockerfile
- **Impact:** Docker builds successfully

## 📦 New Features

### Skechers Staging Tests (33 tests)
- ✅ Homepage tests (11 tests) - Logo, navigation, search, responsive
- ✅ Product search tests (9 tests) - Search functionality, filters, sorting
- ✅ API tests (13 tests) - Products, categories, reviews, filters

### Configuration
- ✅ config.skechers-staging.yaml - Skechers-specific configuration
- ✅ Comprehensive documentation in tests/skechers/README.md

## 🎨 Test Features

- **Smoke tests** (@pytest.mark.smoke) - 5 critical tests
- **API tests** (@pytest.mark.api) - 13 API tests
- **Parametrized tests** - Efficient multi-scenario testing
- **Flexible selectors** - Multiple fallback strategies
- **Responsive tests** - 4 viewport sizes

## 🚀 CI/CD Integration

Tests will run automatically via:
- ✅ Pull Request Tests workflow
- ✅ API Tests Only workflow
- ✅ Scheduled Tests workflow
- ✅ Parallel Tests workflow

## 📊 Changes Summary

| Metric | Value |
|--------|-------|
| **Files Added** | 7 |
| **Tests Added** | 33 |
| **Lines of Code** | ~1,200 |
| **Documentation** | Complete |
| **CI/CD Fixes** | 2 critical |

## ✅ Testing

### Local Testing
``````bash
# All Skechers tests
pytest tests/skechers/ -v

# Smoke tests only
pytest tests/skechers/ -m smoke -v

# API tests only
pytest tests/skechers/ -m api -v
``````

### CI/CD Status
- ✅ Docker build fixed
- ✅ Fixtures available
- ✅ All workflows should pass

## 📝 Files Changed

### Added
- config.skechers-staging.yaml
- tests/skechers/test_homepage.py
- tests/skechers/test_product_search.py
- tests/skechers/test_api_products.py
- tests/skechers/README.md
- PR_SKECHERS_TESTS.md
- CI_FIX_SUMMARY.md

### Modified
- docker/Dockerfile (critical fixes)

## 🎯 Commits

1. **Initial:** Add Skechers staging tests and configuration
2. **Fix:** Fix Dockerfile package installation issues
3. **Fix:** Add conftest.py to Docker image (CRITICAL)

## ⚠️ Notes

- Selectors may need updates based on actual Skechers site
- API endpoints assume certain patterns (update as needed)
- See tests/skechers/README.md for details

## ✅ Checklist

- [x] Tests written and documented
- [x] CI/CD issues fixed
- [x] Docker build working
- [x] Fixtures available
- [x] Configuration added
- [x] Documentation complete
- [x] Ready for review

---

**Branch:** feature/skechers-staging-tests
**Base:** main
**Status:** ✅ Ready for Review
"@

Write-Host $prDescription -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Fill in the PR title and description" -ForegroundColor White
Write-Host "2. Review the changes" -ForegroundColor White
Write-Host "3. Click 'Create Pull Request'" -ForegroundColor White
Write-Host "4. Watch CI/CD run and pass!" -ForegroundColor White
Write-Host ""

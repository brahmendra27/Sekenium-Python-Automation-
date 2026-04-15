# GitHub Actions Quick Start Guide

## Overview
This guide provides quick instructions for setting up and testing the GitHub Actions CI/CD pipeline for the Test Automation Framework.

## Current Status
✅ **Workflow Configuration**: Complete and validated  
✅ **Local Testing**: All validations passed  
⏳ **GitHub Integration**: Pending repository setup

## Quick Validation

Run the automated validation script:
```powershell
.\validate-github-workflow.ps1
```

Expected output: All 11 tests should pass.

## Setting Up GitHub Repository

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., `test-automation-framework`)
3. Do NOT initialize with README (we already have one)

### Step 2: Connect Local Repository
```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Workflow
1. Go to your repository on GitHub
2. Click on "Actions" tab
3. You should see the workflow run triggered by the push

## Testing the Workflow

### Test 1: Create a Pull Request (Passing Tests)

```bash
# Create and switch to test branch
git checkout -b test/workflow-validation

# Make a small change
echo "## CI/CD" >> README.md
git add README.md
git commit -m "test: Validate GitHub Actions workflow"

# Push branch
git push -u origin test/workflow-validation
```

Then:
1. Go to GitHub and create a Pull Request
2. Watch the workflow run in the "Checks" tab
3. Verify all tests pass
4. Download artifacts from the workflow run

### Test 2: Test Failure Detection

```bash
# Create test branch
git checkout -b test/failure-detection

# Add a failing test
cat > tests/test_ci_failure.py << 'EOF'
import pytest

@pytest.mark.selenium
def test_ci_failure_detection():
    """Test to validate CI failure detection."""
    assert False, "Testing CI failure detection"
EOF

git add tests/test_ci_failure.py
git commit -m "test: Add failing test for CI validation"
git push -u origin test/failure-detection
```

Then:
1. Create a Pull Request
2. Verify the workflow fails
3. Check that reports are still uploaded
4. Download and review the failure reports

### Test 3: Clean Up

```bash
# Switch back to main
git checkout main

# Delete test branches
git branch -D test/workflow-validation
git branch -D test/failure-detection

# Delete remote branches
git push origin --delete test/workflow-validation
git push origin --delete test/failure-detection

# Remove the failing test
rm tests/test_ci_failure.py
git add tests/test_ci_failure.py
git commit -m "chore: Remove test file"
git push origin main
```

## What to Verify

### In GitHub Actions UI
- ✅ Workflow triggers automatically on PR and push
- ✅ Docker image builds successfully
- ✅ Tests execute in container
- ✅ Workflow completes (pass or fail as expected)

### In Artifacts
- ✅ `html-report` - Download and open in browser
- ✅ `json-report` - Download and verify JSON structure
- ✅ `screenshots` - Check if screenshots captured on failures
- ✅ `traces` - Check if Playwright traces captured on failures

### In Workflow Logs
- ✅ Docker build step shows layer caching
- ✅ Test execution output is visible
- ✅ Failure detection step runs when tests fail

## Expected Workflow Duration

**First Run** (no cache): 5-8 minutes
- Checkout: ~10s
- Docker build: 3-5 min
- Test execution: 1-2 min
- Artifact upload: ~30s

**Subsequent Runs** (with cache): 2-4 minutes
- Checkout: ~10s
- Docker build (cached): 30-60s
- Test execution: 1-2 min
- Artifact upload: ~30s

## Troubleshooting

### Workflow doesn't trigger
- Check that workflow file is in `.github/workflows/`
- Verify branch name matches trigger configuration
- Check repository settings > Actions > General

### Docker build fails
- Review Dockerfile for syntax errors
- Check that all dependencies are available
- Look for network issues in build logs

### Tests fail in CI but pass locally
- Verify headless mode is working
- Check for environment-specific issues
- Review uploaded screenshots and reports

### Artifacts not uploaded
- Verify `if: always()` is present in upload steps
- Check that report paths are correct
- Ensure reports directory exists

## Additional Configuration

### Add Status Badge to README
```markdown
![CI Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Automation%20Framework%20CI/badge.svg)
```

### Enable Branch Protection
1. Go to Settings > Branches
2. Add rule for `main` branch
3. Enable "Require status checks to pass before merging"
4. Select the workflow check

### Configure Notifications
1. Go to Settings > Notifications
2. Configure email or Slack notifications for workflow failures

## Resources

- **Detailed Test Plan**: `TASK_12.2_GITHUB_ACTIONS_TEST_PLAN.md`
- **Validation Summary**: `TASK_12.2_VALIDATION_SUMMARY.md`
- **Validation Script**: `validate-github-workflow.ps1`
- **Workflow File**: `.github/workflows/test.yml`

## Support

If you encounter issues:
1. Run the validation script: `.\validate-github-workflow.ps1`
2. Check the troubleshooting section above
3. Review the detailed test plan
4. Check GitHub Actions documentation: https://docs.github.com/en/actions

---

**Quick Start Version**: 1.0  
**Last Updated**: 2025-01-24

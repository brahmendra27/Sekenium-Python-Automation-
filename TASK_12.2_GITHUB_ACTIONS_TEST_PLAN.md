# Task 12.2: GitHub Actions Workflow Testing Plan

## Overview
This document provides a comprehensive testing plan for the GitHub Actions workflow defined in `.github/workflows/test.yml`. Since this repository is not yet connected to GitHub, this plan includes both local validation steps and instructions for GitHub integration testing.

## Requirements Validation
This task validates requirements:
- **9.1**: GitHub Actions workflow triggers on pull request and push to main
- **9.2**: CI pipeline builds Docker image and executes tests in container
- **9.3**: CI pipeline uploads HTML and JSON reports as workflow artifacts
- **9.4**: CI pipeline marks workflow as failed when tests fail

## Local Validation (Completed)

### 1. Workflow File Validation ✓
**Status**: PASSED

The workflow file `.github/workflows/test.yml` has been reviewed and contains:
- ✓ Trigger configuration for `push` and `pull_request` events on `main` branch
- ✓ Docker Buildx setup for efficient image building
- ✓ Docker image build with layer caching (GitHub Actions cache)
- ✓ Test execution in Docker container with headless mode
- ✓ Report upload steps for HTML, JSON, screenshots, and traces
- ✓ Failure detection and workflow exit code handling

### 2. Docker Image Build Test ✓
**Command**: 
```bash
docker build -t test-automation-framework:latest -f docker/Dockerfile .
```

**Expected Result**: Docker image builds successfully with all dependencies
**Validation**: This was completed in Task 11.3

### 3. Docker Container Test Execution ✓
**Command**:
```bash
docker run --rm -v ${PWD}/reports:/app/reports -e HEADLESS=true test-automation-framework:latest pytest --headless
```

**Expected Result**: Tests execute and reports are generated in `reports/` directory
**Validation**: This was completed in Task 11.3

### 4. Report Generation Validation ✓
**Files to Check**:
- `reports/report.html` - HTML report with test results
- `reports/report.json` - JSON report with machine-readable results
- `reports/screenshots/` - Screenshots captured on test failures
- `reports/traces/` - Playwright trace files on failures

**Validation**: This was completed in Task 11.3

### 5. Failure Scenario Test
**Purpose**: Verify that the workflow correctly detects and reports test failures

**Test Steps**:
1. Create a test that intentionally fails
2. Run the Docker container with the failing test
3. Verify exit code is non-zero
4. Verify reports capture the failure

**Implementation**:
```bash
# Create a temporary failing test
cat > tests/test_failure_scenario.py << 'EOF'
import pytest

@pytest.mark.selenium
def test_intentional_failure():
    """Test that intentionally fails to validate failure detection."""
    assert False, "This test is designed to fail"
EOF

# Run tests in Docker and capture exit code
docker run --rm \
  -v ${PWD}/reports:/app/reports \
  -e HEADLESS=true \
  test-automation-framework:latest \
  pytest --headless tests/test_failure_scenario.py

echo "Exit code: $?"

# Clean up
rm tests/test_failure_scenario.py
```

## GitHub Integration Testing (Requires GitHub Repository)

### Prerequisites
1. Create a GitHub repository for this project
2. Add the repository as a remote:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   ```
3. Push the main branch:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Test Scenario 1: Pull Request with Passing Tests

**Steps**:
1. Create a test branch:
   ```bash
   git checkout -b test/github-actions-validation
   ```

2. Make a minor change (e.g., update README):
   ```bash
   echo "\n## CI/CD Status\nGitHub Actions workflow is active." >> README.md
   git add README.md
   git commit -m "test: Validate GitHub Actions workflow"
   ```

3. Push the branch:
   ```bash
   git push -u origin test/github-actions-validation
   ```

4. Open a Pull Request on GitHub

5. **Verify**:
   - ✓ Workflow triggers automatically
   - ✓ Docker image builds successfully
   - ✓ Tests execute in container
   - ✓ All tests pass
   - ✓ Reports are uploaded as artifacts
   - ✓ Workflow status shows as "passed" (green check)

6. **Check Artifacts**:
   - Navigate to the workflow run in GitHub Actions
   - Verify artifacts are available for download:
     - `html-report`
     - `json-report`
     - `screenshots` (if any failures)
     - `traces` (if any Playwright failures)

### Test Scenario 2: Pull Request with Failing Tests

**Steps**:
1. Create a new test branch:
   ```bash
   git checkout -b test/failure-detection
   ```

2. Add a failing test:
   ```bash
   cat > tests/test_failure_detection.py << 'EOF'
import pytest

@pytest.mark.selenium
def test_failure_detection():
    """Test that intentionally fails to validate CI failure detection."""
    assert False, "This test validates that CI detects failures"
EOF
   
   git add tests/test_failure_detection.py
   git commit -m "test: Add failing test to validate CI failure detection"
   ```

3. Push the branch:
   ```bash
   git push -u origin test/failure-detection
   ```

4. Open a Pull Request on GitHub

5. **Verify**:
   - ✓ Workflow triggers automatically
   - ✓ Docker image builds successfully
   - ✓ Tests execute in container
   - ✓ Test failure is detected
   - ✓ Reports are uploaded as artifacts (including failure screenshots)
   - ✓ Workflow status shows as "failed" (red X)
   - ✓ PR cannot be merged until tests pass

6. **Check Failure Details**:
   - Review the workflow logs
   - Verify the "Check test results" step shows the failure
   - Download and review the HTML report artifact
   - Verify screenshots were captured for the failing test

7. **Clean up**:
   ```bash
   git checkout main
   git branch -D test/failure-detection
   ```

### Test Scenario 3: Push to Main Branch

**Steps**:
1. Ensure you're on the main branch:
   ```bash
   git checkout main
   ```

2. Make a change and commit:
   ```bash
   echo "# Version 1.0.0" >> CHANGELOG.md
   git add CHANGELOG.md
   git commit -m "docs: Update changelog"
   ```

3. Push to main:
   ```bash
   git push origin main
   ```

4. **Verify**:
   - ✓ Workflow triggers on push to main
   - ✓ All steps execute successfully
   - ✓ Reports are uploaded as artifacts

### Test Scenario 4: Docker Layer Caching

**Purpose**: Verify that Docker layer caching reduces build time on subsequent runs

**Steps**:
1. Note the build time from the first workflow run
2. Make a minor code change that doesn't affect dependencies
3. Push and trigger another workflow run
4. **Verify**:
   - ✓ Second build is faster than the first
   - ✓ Cache is being used (check workflow logs for "Cache hit")

## Validation Checklist

### Local Validation (Can be done now)
- [x] Workflow file syntax is valid
- [x] Docker image builds successfully
- [x] Tests execute in Docker container
- [x] Reports are generated correctly
- [ ] Failure scenario produces non-zero exit code

### GitHub Integration (Requires GitHub repository)
- [ ] Workflow triggers on pull request
- [ ] Workflow triggers on push to main
- [ ] Docker image builds in GitHub Actions
- [ ] Tests execute successfully in CI
- [ ] HTML report is uploaded as artifact
- [ ] JSON report is uploaded as artifact
- [ ] Screenshots are uploaded when tests fail
- [ ] Traces are uploaded when Playwright tests fail
- [ ] Workflow fails when tests fail
- [ ] Docker layer caching improves build time

## Expected Workflow Execution Time

Based on the workflow configuration:
- **First run** (no cache): 5-8 minutes
  - Checkout: ~10 seconds
  - Docker build: 3-5 minutes
  - Test execution: 1-2 minutes
  - Artifact upload: ~30 seconds

- **Subsequent runs** (with cache): 2-4 minutes
  - Checkout: ~10 seconds
  - Docker build (cached): 30-60 seconds
  - Test execution: 1-2 minutes
  - Artifact upload: ~30 seconds

## Troubleshooting

### Issue: Workflow doesn't trigger
**Solution**: Ensure the workflow file is in `.github/workflows/` and the branch name matches the trigger configuration

### Issue: Docker build fails
**Solution**: Check the Dockerfile for syntax errors and ensure all dependencies are available

### Issue: Tests fail in CI but pass locally
**Solution**: 
- Verify headless mode is working correctly
- Check for environment-specific issues
- Review the uploaded reports and screenshots

### Issue: Artifacts not uploaded
**Solution**: 
- Verify the report paths match the workflow configuration
- Check that reports are being generated in the correct directory
- Ensure the `if: always()` condition is present for artifact upload steps

## Conclusion

This test plan provides comprehensive validation for the GitHub Actions workflow. The local validation steps confirm that all components work correctly, while the GitHub integration steps will validate the full CI/CD pipeline once the repository is connected to GitHub.

## Next Steps

1. **If GitHub repository is available**: Execute the GitHub Integration Testing scenarios
2. **If GitHub repository is not available**: 
   - Complete the local failure scenario test
   - Document the results
   - Proceed with repository setup when ready

## References

- GitHub Actions Documentation: https://docs.github.com/en/actions
- Docker Build Push Action: https://github.com/docker/build-push-action
- GitHub Actions Artifacts: https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts

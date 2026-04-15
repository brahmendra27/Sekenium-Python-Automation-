# Docker Execution - Quick Reference

## Task 11.3: Test Docker Build and Execution

This directory contains Docker configuration and validation tools for the Test Automation Framework.

## Files

- **Dockerfile** - Docker image definition with Python, browsers, and dependencies
- **docker-compose.yml** - Docker Compose service configuration
- **test-docker.ps1** - Automated validation script (Windows PowerShell)
- **test-docker.sh** - Automated validation script (Linux/Mac Bash)
- **test-docker-execution.md** - Detailed test execution guide
- **VALIDATION_REPORT.md** - Configuration validation report
- **README.md** - This file

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker Compose installed (included with Docker Desktop)

### Method 1: Manual Execution (Original Task)

```bash
# Build Docker image
docker build -t test-automation-framework -f docker/Dockerfile .

# Run tests in container
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit

# Verify reports generated
ls -la reports/
```

### Method 2: Automated Script (Windows)

```powershell
# Full test with build
.\docker\test-docker.ps1

# Skip build if image exists
.\docker\test-docker.ps1 -SkipBuild
```

### Method 3: Automated Script (Linux/Mac)

```bash
# Make executable (first time only)
chmod +x docker/test-docker.sh

# Full test with build
./docker/test-docker.sh

# Skip build if image exists
./docker/test-docker.sh --skip-build
```

## What Gets Validated

### Requirement 8.2: Docker Image Build
- ✅ Python 3.11 installed
- ✅ All dependencies from requirements.txt
- ✅ Selenium drivers installed
- ✅ Playwright browsers installed
- ✅ Framework code copied
- ✅ Reports directory created

### Requirement 8.4: Headless Execution
- ✅ Tests run in headless mode
- ✅ No display server required
- ✅ HEADLESS environment variable set

### Requirement 8.6: Exit Code Propagation
- ✅ Container returns pytest exit code
- ✅ Exit code 0 for passing tests
- ✅ Exit code non-zero for failing tests

### Report Generation
- ✅ reports/report.html created on host
- ✅ reports/report.json created on host
- ✅ reports/screenshots/ directory exists
- ✅ reports/traces/ directory exists

## Expected Output

### Successful Execution
```
=== Docker Execution Test - Task 11.3 ===
✓ Docker is available
✓ Docker image built successfully
✓ Tests executed in container
✓ report.html exists
✓ report.json exists
✓ screenshots/ directory exists
✓ traces/ directory exists
✓ Exit code is 0 (all tests passed)
✓ All validation checks passed!
```

### Failed Tests
```
=== Docker Execution Test - Task 11.3 ===
✓ Docker is available
✓ Docker image built successfully
✓ Tests executed in container
✓ report.html exists
✓ report.json exists
✓ screenshots/ directory exists (2 files)
✓ traces/ directory exists (1 files)
ℹ Exit code is 1 (tests failed or error occurred)
```

## Troubleshooting

### Docker not found
**Problem:** `docker: command not found` or `The term 'docker' is not recognized`

**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

### Build fails with dependency errors
**Problem:** `ERROR: Could not find a version that satisfies the requirement...`

**Solution:** 
- Check internet connectivity
- Verify requirements.txt is valid
- Try building again (may be temporary network issue)

### Tests fail in container but pass locally
**Problem:** Tests pass on host but fail in Docker

**Solution:**
- Check headless mode compatibility
- Verify browser versions in container
- Review test logs for environment-specific issues

### Reports not appearing on host
**Problem:** Container runs but no reports in `reports/` directory

**Solution:**
- Verify volume mount path in docker-compose.yml
- Check container logs: `docker logs test-automation-framework`
- Ensure reports directory exists on host
- Check file permissions

### Container doesn't exit
**Problem:** Container keeps running after tests complete

**Solution:**
- Use `--abort-on-container-exit` flag with docker-compose
- Check if tests are hanging (timeout issues)
- Manually stop: `docker-compose -f docker/docker-compose.yml down`

## Additional Resources

- **Detailed Guide:** See `test-docker-execution.md` for step-by-step instructions
- **Validation Report:** See `VALIDATION_REPORT.md` for configuration validation
- **Framework Overview:** See `.kiro/steering/framework-overview.md`
- **Docker Execution Guide:** See `.kiro/steering/docker-execution.md`

## CI/CD Integration

This Docker setup is designed for CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Build Docker image
  run: docker build -t test-automation-framework -f docker/Dockerfile .

- name: Run tests
  run: docker-compose -f docker/docker-compose.yml up --abort-on-container-exit

- name: Upload reports
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: reports/
```

## Notes

- First build takes 5-10 minutes (downloads browsers)
- Subsequent builds are faster (Docker layer caching)
- Image size approximately 2-3 GB (includes browsers)
- Tests run in headless mode automatically
- Reports persist on host after container exits
- Container is automatically removed after execution

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review detailed guide in `test-docker-execution.md`
3. Check Docker logs: `docker logs test-automation-framework`
4. Review validation report: `VALIDATION_REPORT.md`

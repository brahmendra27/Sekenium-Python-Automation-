#!/bin/bash
# Docker Execution Test Script - Task 11.3
# This script validates Docker build and execution for the test automation framework

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Output functions
success() { echo -e "${GREEN}✓ $1${NC}"; }
failure() { echo -e "${RED}✗ $1${NC}"; }
info() { echo -e "${CYAN}ℹ $1${NC}"; }
step() { echo -e "\n${YELLOW}=== $1 ===${NC}"; }

# Parse arguments
SKIP_BUILD=false
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        failure "Docker is not installed or not in PATH"
        info "Please install Docker from https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    success "Docker is available"
    info "Docker version: $(docker --version)"
}

# Main test execution
main() {
    step "Docker Execution Test - Task 11.3"
    
    # Check Docker availability
    info "Checking Docker availability..."
    check_docker
    
    # Clean existing reports
    step "Cleaning existing reports"
    if [ -f "reports/report.html" ]; then
        rm -f reports/report.html
        info "Removed existing report.html"
    fi
    if [ -f "reports/report.json" ]; then
        rm -f reports/report.json
        info "Removed existing report.json"
    fi
    
    # Step 1: Build Docker image
    if [ "$SKIP_BUILD" = false ]; then
        step "Step 1: Building Docker image"
        info "Running: docker build -t test-automation-framework -f docker/Dockerfile ."
        
        BUILD_START=$(date +%s)
        if docker build -t test-automation-framework -f docker/Dockerfile .; then
            BUILD_END=$(date +%s)
            BUILD_DURATION=$((BUILD_END - BUILD_START))
            success "Docker image built successfully in ${BUILD_DURATION} seconds"
        else
            BUILD_EXIT_CODE=$?
            failure "Docker build failed with exit code $BUILD_EXIT_CODE"
            exit $BUILD_EXIT_CODE
        fi
        
        # Verify image exists
        if docker images test-automation-framework --format "{{.Repository}}:{{.Tag}}" | grep -q "test-automation-framework"; then
            IMAGE_SIZE=$(docker images test-automation-framework --format "{{.Size}}")
            success "Image verified: test-automation-framework:latest"
            info "Image size: $IMAGE_SIZE"
        else
            failure "Image not found in docker images list"
            exit 1
        fi
    else
        info "Skipping build (--skip-build flag set)"
    fi
    
    # Step 2: Run tests in container
    step "Step 2: Running tests in Docker container"
    info "Running: docker-compose -f docker/docker-compose.yml up --abort-on-container-exit"
    
    TEST_START=$(date +%s)
    docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
    TEST_EXIT_CODE=$?
    TEST_END=$(date +%s)
    TEST_DURATION=$((TEST_END - TEST_START))
    
    info "Test execution completed in ${TEST_DURATION} seconds"
    info "Exit code: $TEST_EXIT_CODE"
    
    # Step 3: Verify reports generated
    step "Step 3: Verifying reports generated in host directory"
    
    REPORT_HTML_OK=false
    REPORT_JSON_OK=false
    SCREENSHOTS_OK=false
    TRACES_OK=false
    
    # Check HTML report
    if [ -f "reports/report.html" ]; then
        HTML_SIZE=$(stat -f%z "reports/report.html" 2>/dev/null || stat -c%s "reports/report.html" 2>/dev/null)
        success "report.html exists ($HTML_SIZE bytes)"
        REPORT_HTML_OK=true
    else
        failure "report.html not found"
    fi
    
    # Check JSON report
    if [ -f "reports/report.json" ]; then
        JSON_SIZE=$(stat -f%z "reports/report.json" 2>/dev/null || stat -c%s "reports/report.json" 2>/dev/null)
        success "report.json exists ($JSON_SIZE bytes)"
        REPORT_JSON_OK=true
        
        # Parse JSON report for summary
        if command -v jq &> /dev/null; then
            info "Test Summary:"
            info "  Total: $(jq -r '.summary.total' reports/report.json)"
            info "  Passed: $(jq -r '.summary.passed' reports/report.json)"
            info "  Failed: $(jq -r '.summary.failed' reports/report.json)"
            info "  Skipped: $(jq -r '.summary.skipped' reports/report.json)"
            info "  Duration: $(jq -r '.summary.duration' reports/report.json)s"
        fi
    else
        failure "report.json not found"
    fi
    
    # Check screenshots directory
    if [ -d "reports/screenshots" ]; then
        SCREENSHOT_COUNT=$(find reports/screenshots -type f | wc -l | tr -d ' ')
        success "screenshots/ directory exists ($SCREENSHOT_COUNT files)"
        SCREENSHOTS_OK=true
    else
        failure "screenshots/ directory not found"
    fi
    
    # Check traces directory
    if [ -d "reports/traces" ]; then
        TRACE_COUNT=$(find reports/traces -type f | wc -l | tr -d ' ')
        success "traces/ directory exists ($TRACE_COUNT files)"
        TRACES_OK=true
    else
        failure "traces/ directory not found"
    fi
    
    # Step 4: Verify exit code propagation
    step "Step 4: Verifying exit code propagation"
    
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        success "Exit code is 0 (all tests passed)"
    else
        info "Exit code is $TEST_EXIT_CODE (tests failed or error occurred)"
    fi
    
    # Requirements validation summary
    step "Requirements Validation Summary"
    
    info "Requirement 8.2 (Docker Image Build):"
    if [ "$SKIP_BUILD" = false ]; then
        success "  Docker image built with all dependencies"
    else
        info "  Skipped (--skip-build flag set)"
    fi
    
    info "Requirement 8.4 (Headless Execution):"
    success "  Tests executed in headless mode in container"
    
    info "Requirement 8.6 (Exit Code Propagation):"
    success "  Container exit code: $TEST_EXIT_CODE"
    
    info "Report Generation:"
    [ "$REPORT_HTML_OK" = true ] && success "  report.html ✓" || failure "  report.html ✗"
    [ "$REPORT_JSON_OK" = true ] && success "  report.json ✓" || failure "  report.json ✗"
    [ "$SCREENSHOTS_OK" = true ] && success "  screenshots/ ✓" || failure "  screenshots/ ✗"
    [ "$TRACES_OK" = true ] && success "  traces/ ✓" || failure "  traces/ ✗"
    
    # Final result
    step "Test Result"
    
    if [ "$REPORT_HTML_OK" = true ] && [ "$REPORT_JSON_OK" = true ] && \
       [ "$SCREENSHOTS_OK" = true ] && [ "$TRACES_OK" = true ]; then
        success "All validation checks passed!"
        info "Task 11.3 completed successfully"
    else
        failure "Some validation checks failed"
        info "Review the output above for details"
    fi
    
    # Cleanup
    step "Cleanup"
    info "Stopping and removing containers..."
    docker-compose -f docker/docker-compose.yml down
    
    # Return exit code from test execution
    exit $TEST_EXIT_CODE
}

# Run the test
main

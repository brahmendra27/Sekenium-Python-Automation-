---
name: Pilot Feedback
about: Provide feedback on the Test Automation Framework pilot
title: '[PILOT FEEDBACK] '
labels: pilot-feedback
assignees: ''
---

## Pilot Feedback

Thank you for participating in the Test Automation Framework pilot! Your feedback is crucial for improving the framework before team-wide rollout.

---

### Feedback Categories

Please check all areas you're providing feedback on:

- [ ] Setup and Installation
- [ ] Test Authoring
- [ ] Test Execution
- [ ] Reporting
- [ ] Docker Execution
- [ ] CI/CD Integration
- [ ] Kiro IDE Integration
- [ ] Documentation
- [ ] Other

---

### What Worked Well

*Describe what aspects of the framework worked well for you. What made your testing workflow easier or more efficient?*

<!-- Example:
- The pytest fixtures made it easy to write tests without boilerplate
- Docker execution was straightforward and reproducible
- HTML reports with screenshots were very helpful for debugging
-->

---

### What Didn't Work

*Describe any issues, pain points, or frustrations you encountered. Be specific about what went wrong and when.*

<!-- Example:
- Playwright tests timed out frequently on slow pages
- Docker build took too long on first run (15+ minutes)
- Unclear how to add custom configuration options
-->

---

### Suggestions for Improvement

*What changes or additions would make the framework better? What features are missing?*

<!-- Example:
- Add support for Edge browser
- Include more example tests for common scenarios
- Add a CLI command to generate test templates
- Improve error messages when driver initialization fails
-->

---

### Blockers Encountered

*Did you encounter any blockers that prevented you from using the framework? What stopped you from completing your work?*

<!-- Example:
- Could not install Playwright browsers due to network restrictions
- Tests failed in Docker but passed locally, couldn't debug
- Missing documentation on how to configure custom timeouts
-->

---

### Setup Experience

**Did you successfully complete the setup?**
- [ ] Yes, without issues
- [ ] Yes, but encountered issues (describe below)
- [ ] No, blocked by setup issues (describe below)

**Setup time:** *(How long did it take to get the framework running?)*

**Issues encountered during setup:**

<!-- Example:
- Python version mismatch (had 3.9, needed 3.11)
- playwright install failed on corporate network
- Unclear which Python version to use
-->

---

### Test Authoring Experience

**Did you write new tests using the framework?**
- [ ] Yes, Selenium tests
- [ ] Yes, Playwright tests
- [ ] Yes, both Selenium and Playwright tests
- [ ] No, only ran existing tests

**How easy was it to write tests?**
- [ ] Very easy
- [ ] Easy
- [ ] Moderate
- [ ] Difficult
- [ ] Very difficult

**Feedback on test authoring:**

<!-- Example:
- Fixtures were intuitive and well-documented
- Struggled to understand when to use Selenium vs Playwright
- Page Object Model examples would be helpful
- Kiro hooks for scaffolding tests saved time
-->

---

### Test Execution Experience

**Which execution methods did you use?**
- [ ] Local execution (pytest)
- [ ] Docker execution
- [ ] GitHub Actions CI
- [ ] Parallel execution (pytest-xdist)

**How reliable was test execution?**
- [ ] Very reliable (no flaky tests)
- [ ] Mostly reliable (occasional flakiness)
- [ ] Somewhat reliable (frequent flakiness)
- [ ] Unreliable (tests fail inconsistently)

**Feedback on test execution:**

<!-- Example:
- Tests ran smoothly in headless mode
- Parallel execution caused race conditions
- Docker execution was slower than local
- CI pipeline failed due to timeout issues
-->

---

### Reporting Experience

**Did you review test reports?**
- [ ] Yes, HTML reports
- [ ] Yes, JSON reports
- [ ] Yes, both HTML and JSON reports
- [ ] No, did not review reports

**How useful were the reports?**
- [ ] Very useful
- [ ] Useful
- [ ] Somewhat useful
- [ ] Not useful

**Feedback on reporting:**

<!-- Example:
- Screenshots in HTML reports were very helpful
- JSON reports were hard to parse manually
- Would like to see test duration trends
- Trace files were useful for debugging Playwright tests
-->

---

### Docker Experience

**Did you use Docker for test execution?**
- [ ] Yes, successfully
- [ ] Yes, but encountered issues (describe below)
- [ ] No, did not use Docker
- [ ] No, blocked by Docker issues (describe below)

**Feedback on Docker execution:**

<!-- Example:
- Docker build was slow on first run
- Tests ran consistently in Docker vs local
- Unclear how to pass custom environment variables
- Volume mounts worked well for retrieving reports
-->

---

### CI/CD Experience

**Did you use the GitHub Actions workflow?**
- [ ] Yes, on pull requests
- [ ] Yes, on pushes to main
- [ ] Yes, both
- [ ] No, did not use GitHub Actions

**Feedback on CI/CD integration:**

<!-- Example:
- Workflow ran smoothly and caught regressions
- Artifact uploads made it easy to review reports
- Build caching reduced pipeline time significantly
- Would like to see test results in PR comments
-->

---

### Kiro IDE Integration Experience

**Did you use Kiro IDE features?**
- [ ] Yes, steering files
- [ ] Yes, hooks
- [ ] Yes, both steering files and hooks
- [ ] No, did not use Kiro IDE features

**Feedback on Kiro IDE integration:**

<!-- Example:
- Steering files provided helpful context for test authoring
- Hooks automated scaffolding and saved time
- Would like more hooks for common tasks
- Unclear how to customize hooks
-->

---

### Documentation Experience

**Which documentation did you use?**
- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] docker/README.md
- [ ] Kiro steering files
- [ ] Other (specify below)

**How clear was the documentation?**
- [ ] Very clear
- [ ] Clear
- [ ] Somewhat clear
- [ ] Unclear

**Feedback on documentation:**

<!-- Example:
- README setup instructions were easy to follow
- CONTRIBUTING.md was comprehensive
- Would like more examples for complex scenarios
- Missing troubleshooting section for common errors
-->

---

### Overall Experience

**How likely are you to use this framework for future testing?**
- [ ] Very likely
- [ ] Likely
- [ ] Neutral
- [ ] Unlikely
- [ ] Very unlikely

**Overall rating:**
- [ ] ⭐⭐⭐⭐⭐ Excellent
- [ ] ⭐⭐⭐⭐ Good
- [ ] ⭐⭐⭐ Average
- [ ] ⭐⭐ Below Average
- [ ] ⭐ Poor

**Additional comments:**

<!-- Any other feedback, suggestions, or thoughts about the framework -->

---

### Environment Information

**Operating System:**
- [ ] Windows
- [ ] macOS
- [ ] Linux (specify distro: _____________)

**Python Version:** *(e.g., 3.11.5)*

**Docker Version:** *(if used, e.g., 24.0.6)*

**Browser Versions:** *(if relevant, e.g., Chrome 120, Firefox 121)*

---

### Contact Information (Optional)

**Name:** *(optional)*

**Email:** *(optional, if you'd like follow-up)*

**Team:** *(optional)*

---

Thank you for your feedback! Your input will help us improve the framework for the entire team. 🚀

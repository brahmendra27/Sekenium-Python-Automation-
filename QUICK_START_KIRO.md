# Kiro IDE Integration - Quick Start Guide

**Version:** v0.1.0  
**Last Updated:** 2024-01-15

This is a quick reference for getting started with Kiro IDE integration in the Test Automation Framework.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Verify Kiro IDE Integration

```bash
# Check steering files exist
ls .kiro/steering/
# Should see: test-writing-guide.md, framework-overview.md, docker-execution.md

# Check hooks exist
ls .kiro/hooks/
# Should see: test-file-review.kiro.hook, report-summary.kiro.hook, scaffold-test.kiro.hook
```

### Step 2: Test Steering Files

Open Kiro IDE and ask:

```
"How do I write a Selenium test?"
```

**Expected:** Kiro provides guidance from `test-writing-guide.md` with examples.

### Step 3: Test Hooks

**Test 1: File Review Hook**
1. Open `tests/selenium/test_example_selenium.py`
2. Remove the `@pytest.mark.selenium` decorator
3. Save the file
4. **Expected:** Kiro reviews and says "Missing marker: Add @pytest.mark.selenium"

**Test 2: Scaffold Hook**
1. Create new file: `tests/playwright/test_new_feature.py`
2. **Expected:** Kiro scaffolds the file with imports, fixture, and marker

**Test 3: Report Summary Hook**
1. Run tests: `pytest -v`
2. In Kiro IDE, manually trigger "Test Report Summary" hook
3. **Expected:** Kiro summarizes test results from `reports/report.json`

---

## 📚 What's Included

### Steering Files (`.kiro/steering/`)

| File | Purpose | Keywords |
|------|---------|----------|
| `test-writing-guide.md` | Test authoring conventions | test, selenium, playwright, write test |
| `framework-overview.md` | Project structure & config | framework, structure, configuration |
| `docker-execution.md` | Docker build & execution | docker, container, execution |

### Hooks (`.kiro/hooks/`)

| Hook | Trigger | Action |
|------|---------|--------|
| `test-file-review.kiro.hook` | Save test file | Review for conventions |
| `scaffold-test.kiro.hook` | Create test file | Add imports & structure |
| `report-summary.kiro.hook` | Manual trigger | Summarize test results |

---

## 💡 Common Use Cases

### Use Case 1: Writing a New Test

**Ask Kiro:**
```
"I need to write a Selenium test for the login page. 
The test should verify successful login with valid credentials."
```

**Kiro will:**
1. Load `test-writing-guide.md` (keywords: "selenium", "test")
2. Provide template with correct imports, fixture, and marker
3. Include example code following framework conventions

---

### Use Case 2: Understanding Framework Structure

**Ask Kiro:**
```
"What fixtures are available in this framework?"
```

**Kiro will:**
1. Load `framework-overview.md` (keywords: "framework", "fixtures")
2. List available fixtures: `selenium_driver`, `playwright_context`, `playwright_page`
3. Explain how to use each fixture

---

### Use Case 3: Running Tests in Docker

**Ask Kiro:**
```
"How do I run tests in Docker?"
```

**Kiro will:**
1. Load `docker-execution.md` (keywords: "docker", "run tests")
2. Provide Docker build command
3. Provide Docker Compose execution command
4. Include troubleshooting tips

---

### Use Case 4: Reviewing Test Code

**Automatic (via hook):**
1. Save any test file in `tests/` directory
2. Hook triggers automatically
3. Kiro reviews for:
   - ✅ Correct fixture usage
   - ✅ Appropriate marker
   - ✅ Naming convention
   - ✅ Docstring present
   - ✅ One assertion per test

---

### Use Case 5: Scaffolding New Tests

**Automatic (via hook):**
1. Create new file: `tests/selenium/test_checkout.py`
2. Hook triggers automatically
3. Kiro scaffolds:
```python
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.selenium
def test_checkout_success(selenium_driver):
    """
    Test successful checkout process.
    
    Steps:
    1. Add item to cart
    2. Proceed to checkout
    3. Complete payment
    4. Verify order confirmation
    """
    driver = selenium_driver
    
    # TODO: Implement test
    pass
```

---

### Use Case 6: Understanding Test Failures

**Manual (via hook):**
1. Run tests: `pytest -v`
2. Trigger "Test Report Summary" hook in Kiro IDE
3. Kiro provides:
   - Test counts (total, passed, failed, skipped)
   - Failed test names and error messages
   - Suggestions for fixing failures

---

## 🎯 Quick Tips

### Tip 1: Use Keywords in Questions

When asking Kiro for help, use keywords from steering files:

✅ **Good:**
- "How do I write a **Selenium test**?" (matches: test, selenium)
- "What **fixtures** are available?" (matches: fixtures, framework)
- "How do I run tests in **Docker**?" (matches: docker, execution)

❌ **Less Effective:**
- "Help me" (no keywords)
- "What do I do?" (too vague)

---

### Tip 2: Reference Steering Files Explicitly

If Kiro isn't using the right steering file, reference it explicitly:

```
"Using #test-writing-guide, show me how to write a Playwright test"
```

---

### Tip 3: Disable Hooks Temporarily

If hooks are too noisy during development:

```bash
# Disable all hooks
mv .kiro/hooks .kiro/hooks.disabled

# Re-enable later
mv .kiro/hooks.disabled .kiro/hooks
```

---

### Tip 4: Customize for Your Team

Edit steering files to match your team's conventions:

```bash
# Edit test writing guide
vim .kiro/steering/test-writing-guide.md

# Add your team's custom conventions
# Save and commit to Git
git add .kiro/steering/test-writing-guide.md
git commit -m "Add custom test conventions"
```

---

### Tip 5: Create Custom Hooks

Add hooks for your team's workflow:

```bash
# Create new hook
vim .kiro/hooks/my-custom-hook.kiro.hook
```

Example - Run tests on save:
```json
{
  "name": "Run Tests on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "pytest {file_path} -v"
  }
}
```

---

## 🔧 Troubleshooting

### Problem: Steering files not loading

**Solution:**
1. Check frontmatter syntax (must have `---` delimiters)
2. Verify `inclusion: auto` is set
3. Use broader keywords
4. Ask Kiro: "What steering files do you have access to?"

---

### Problem: Hooks not triggering

**Solution:**
1. Validate JSON syntax: `cat .kiro/hooks/my-hook.kiro.hook | python -m json.tool`
2. Check file patterns match: `"patterns": ["**/*.py"]` (not `"*.py"`)
3. Verify hook is enabled: `"enabled": true`
4. Check Kiro IDE logs for errors

---

### Problem: Kiro gives generic answers

**Solution:**
1. Use more specific keywords in your question
2. Reference steering files explicitly: "Using #test-writing-guide..."
3. Provide more context: "I'm writing a Selenium test for login functionality..."
4. Check if steering files are loaded: Ask "What steering files are you using?"

---

## 📖 Learn More

- **Detailed FAQ:** See `KIRO_INTEGRATION_FAQ.md` for 36 common questions and answers
- **Testing Guide:** See `TESTING_GUIDE.md` for comprehensive testing instructions
- **Framework Overview:** See `.kiro/steering/framework-overview.md` for complete framework documentation

---

## 🎓 Training Resources

### For New Team Members

1. **Read:** `QUICK_START_KIRO.md` (this file) - 5 minutes
2. **Try:** Test all 3 hooks - 10 minutes
3. **Practice:** Ask Kiro 5 questions about the framework - 10 minutes
4. **Review:** `KIRO_INTEGRATION_FAQ.md` - 20 minutes

**Total Time:** 45 minutes to become proficient with Kiro IDE integration

---

### For Team Leads

1. **Review:** All steering files in `.kiro/steering/` - 15 minutes
2. **Customize:** Edit steering files for team conventions - 30 minutes
3. **Create:** Custom hooks for team workflow - 30 minutes
4. **Document:** Update README.md with team-specific guidance - 15 minutes
5. **Train:** Conduct team training session - 60 minutes

**Total Time:** 2.5 hours to customize and roll out to team

---

## 🚦 Status Indicators

### ✅ Working Correctly

- Kiro answers questions using steering files
- Hooks trigger on file save/create
- Kiro provides framework-specific guidance
- Code reviews are automatic and helpful

### ⚠️ Needs Attention

- Kiro gives generic answers (not using steering files)
- Hooks don't trigger (check JSON syntax)
- Guidance doesn't match team conventions (customize steering files)

### ❌ Not Working

- Steering files missing from `.kiro/steering/`
- Hooks missing from `.kiro/hooks/`
- Kiro IDE not installed or not running
- JSON syntax errors in hook files

---

## 📞 Support

**Questions about Kiro IDE integration?**

1. Check `KIRO_INTEGRATION_FAQ.md` (36 Q&A)
2. Check `TESTING_GUIDE.md` (comprehensive testing)
3. Ask in team Slack/Teams channel
4. Contact QE team lead

---

**Quick Start Guide Version:** v0.1.0  
**Last Updated:** 2024-01-15  
**Next Review:** After pilot phase

---

## 🎉 You're Ready!

You now have everything you need to use Kiro IDE integration effectively. Start by asking Kiro:

```
"Show me how to write a Selenium test for the login page"
```

Happy testing! 🚀

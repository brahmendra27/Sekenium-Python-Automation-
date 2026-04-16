# Kiro IDE Integration FAQ

**Version:** v0.1.0  
**Last Updated:** 2024-01-15

This document answers common questions about Kiro IDE integration, including steering files and hooks.

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Steering Files Questions](#steering-files-questions)
3. [Hooks Questions](#hooks-questions)
4. [Troubleshooting Questions](#troubleshooting-questions)
5. [Advanced Usage Questions](#advanced-usage-questions)

---

## General Questions

### Q1: What is Kiro IDE integration?

**A:** Kiro IDE integration provides AI-assisted development capabilities through two mechanisms:

1. **Steering Files**: Markdown files that provide contextual guidance to the Kiro AI agent about framework conventions, structure, and best practices.

2. **Hooks**: Automated triggers that invoke the Kiro AI agent or run commands in response to IDE events (file saves, file creation, etc.).

**Benefits:**
- Faster test authoring with AI assistance
- Automatic code review for convention compliance
- Scaffolding of new test files
- Automated report summarization
- Reduced onboarding time for new team members

---

### Q2: Do I need Kiro IDE to use this framework?

**A:** No! The framework works perfectly without Kiro IDE. You can:

- Write tests manually using any IDE (VS Code, PyCharm, etc.)
- Run tests from the command line
- Use Docker and CI/CD without Kiro IDE

**Kiro IDE is optional** and provides additional AI-assisted features for teams that want them.

---

### Q3: How do I know if Kiro IDE integration is working?

**A:** Check these indicators:

1. **Steering Files Loaded:**
   - Open Kiro IDE
   - Look for steering file indicators in the UI
   - Check if `.kiro/steering/` files are being read

2. **Hooks Active:**
   - Save a test file in `tests/` directory
   - Check if Kiro agent provides feedback (test-file-review hook)
   - Create a new test file and check if it's scaffolded (scaffold-test hook)

3. **Manual Test:**
   - Ask Kiro: "How do I write a Selenium test?"
   - Kiro should reference the test-writing-guide steering file

---

### Q4: Can I disable Kiro IDE integration?

**A:** Yes! You can disable integration in several ways:

**Option 1: Disable All Hooks**
```bash
# Rename hooks directory
mv .kiro/hooks .kiro/hooks.disabled
```

**Option 2: Disable Individual Hooks**
Edit the hook file and set `"enabled": false`:
```json
{
  "name": "Test File Convention Review",
  "enabled": false,
  ...
}
```

**Option 3: Remove Steering Files**
```bash
# Rename steering directory
mv .kiro/steering .kiro/steering.disabled
```

**Note:** Disabling integration doesn't affect framework functionality.

---

## Steering Files Questions

### Q5: What are steering files?

**A:** Steering files are markdown documents in `.kiro/steering/` that provide contextual guidance to the Kiro AI agent. They contain:

- Framework conventions and best practices
- Code examples and templates
- Configuration instructions
- Troubleshooting tips

**Think of them as "documentation that the AI reads automatically" when you ask questions or request help.**

---

### Q6: What steering files are included in this framework?

**A:** Three steering files are included:

| File | Purpose | When It's Used |
|------|---------|----------------|
| `test-writing-guide.md` | Test authoring conventions | When writing or asking about tests |
| `framework-overview.md` | Project structure and configuration | When asking about framework setup |
| `docker-execution.md` | Docker build and execution | When asking about Docker |

---

### Q7: How do steering files work?

**A:** Steering files use **frontmatter metadata** to control when they're loaded:

```markdown
---
title: Test Writing Guide
description: Guide for writing Selenium and Playwright tests
inclusion: auto
keywords: [test, selenium, playwright, write test, create test]
---

# Content here...
```

**Inclusion Types:**

1. **`inclusion: auto`** - Loaded automatically when keywords match
2. **`inclusion: manual`** - Loaded only when explicitly referenced (e.g., `#test-writing-guide`)
3. **`inclusion: fileMatch`** - Loaded when specific files are opened

**Example:**
- You ask: "How do I write a Playwright test?"
- Keywords match: "playwright", "write test"
- Kiro loads `test-writing-guide.md` automatically
- Kiro provides guidance based on the steering file content

---

### Q8: Can I customize steering files?

**A:** Yes! You can customize steering files to match your team's conventions:

**Example: Add Custom Test Convention**

Edit `.kiro/steering/test-writing-guide.md`:

```markdown
## Custom Team Conventions

### Test Data Management
- Store test data in `tests/data/` directory
- Use JSON files for test data
- Name files: `<feature>_test_data.json`

Example:
\`\`\`python
import json

def test_login_with_test_data(selenium_driver):
    with open('tests/data/login_test_data.json') as f:
        data = json.load(f)
    
    driver = selenium_driver
    driver.get(data['login_url'])
    # ... rest of test
\`\`\`
```

**After saving, Kiro will include your custom conventions in its guidance.**

---

### Q9: How do I create a new steering file?

**A:** Follow these steps:

1. **Create file in `.kiro/steering/`:**
```bash
touch .kiro/steering/my-custom-guide.md
```

2. **Add frontmatter:**
```markdown
---
title: My Custom Guide
description: Custom guidance for my team
inclusion: auto
keywords: [custom, my-feature, special-case]
---

# My Custom Guide

## Overview
This guide covers...

## Examples
...
```

3. **Test it:**
- Ask Kiro a question using your keywords
- Verify Kiro references your custom guide

---

### Q10: What's the difference between steering files and regular documentation?

**A:** 

| Aspect | Steering Files | Regular Documentation |
|--------|----------------|----------------------|
| **Audience** | Kiro AI agent | Human developers |
| **Purpose** | Provide context for AI assistance | Provide information for humans |
| **Format** | Markdown with frontmatter | Any format (Markdown, HTML, PDF) |
| **Location** | `.kiro/steering/` | Root directory or `docs/` |
| **Loading** | Automatic (based on keywords) | Manual (user opens file) |
| **Content Style** | Concise, example-focused | Comprehensive, detailed |

**Best Practice:** Maintain both! Steering files help AI, documentation helps humans.

---

### Q11: How do I know which steering file Kiro is using?

**A:** In Kiro IDE:

1. **Check Context Panel:**
   - Look for "Active Steering Files" section
   - Shows which files are currently loaded

2. **Ask Kiro:**
   - "What steering files are you using?"
   - Kiro will list active steering files

3. **Check Logs:**
   - Kiro IDE logs show when steering files are loaded
   - Look for: "Loaded steering file: test-writing-guide.md"

---

### Q12: Can steering files reference other files?

**A:** Yes! Use the file reference syntax:

```markdown
For the complete API specification, see #[[file:api-spec.yaml]]

For database schema, see #[[file:schema.sql]]
```

**This allows steering files to reference:**
- OpenAPI/Swagger specs
- GraphQL schemas
- Database schemas
- Configuration files
- Other documentation

---

## Hooks Questions

### Q13: What are Kiro hooks?

**A:** Hooks are automated triggers that execute actions in response to IDE events. They enable:

- **Automatic code review** when you save a file
- **Automatic scaffolding** when you create a new file
- **Automatic report summarization** after test runs
- **Custom automation** for repetitive tasks

**Think of hooks as "IDE event listeners that trigger AI assistance or commands."**

---

### Q14: What hooks are included in this framework?

**A:** Three hooks are included:

| Hook | Trigger | Action | Purpose |
|------|---------|--------|---------|
| `test-file-review.kiro.hook` | File saved in `tests/**/*.py` | Ask Kiro to review | Check convention compliance |
| `scaffold-test.kiro.hook` | File created in `tests/**/*.py` | Ask Kiro to scaffold | Add imports and structure |
| `report-summary.kiro.hook` | User-triggered | Ask Kiro to summarize | Highlight test failures |

---

### Q15: How does the test-file-review hook work?

**A:** 

**Trigger:** When you save a Python file in `tests/` directory

**Action:** Kiro agent reviews the file and checks:
1. ✅ Correct fixture usage (`selenium_driver` or `playwright_page`)
2. ✅ Appropriate marker (`@pytest.mark.selenium` or `@pytest.mark.playwright`)
3. ✅ Naming convention (`test_<action>_<result>`)
4. ✅ Docstring present
5. ✅ One assertion per test (when possible)

**Example Workflow:**

1. You write a test:
```python
# tests/selenium/test_login.py
def test_login(selenium_driver):
    driver = selenium_driver
    driver.get("https://example.com/login")
    # ... test code
```

2. You save the file

3. Kiro reviews and provides feedback:
```
❌ Missing marker: Add @pytest.mark.selenium decorator
❌ Missing docstring: Add docstring explaining test purpose
✅ Correct fixture usage: selenium_driver
✅ Naming convention: test_login
```

4. You fix the issues:
```python
import pytest

@pytest.mark.selenium
def test_login(selenium_driver):
    """Test successful login with valid credentials."""
    driver = selenium_driver
    driver.get("https://example.com/login")
    # ... test code
```

5. You save again, Kiro confirms: ✅ All conventions followed!

---

### Q16: How does the scaffold-test hook work?

**A:**

**Trigger:** When you create a new Python file in `tests/` directory

**Action:** Kiro agent scaffolds the file with:
1. Appropriate imports (pytest, selenium/playwright modules)
2. Correct fixture in function signature
3. Appropriate marker decorator
4. Placeholder test function with docstring

**Example Workflow:**

1. You create a new file: `tests/selenium/test_checkout.py`

2. Hook triggers, Kiro scaffolds:
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

3. You fill in the test logic

**This saves time and ensures consistency!**

---

### Q17: How does the report-summary hook work?

**A:**

**Trigger:** User manually triggers (not automatic)

**Action:** Kiro agent reads `reports/report.json` and provides:
1. Total tests, passed, failed, skipped
2. Duration
3. Failed test names and error messages
4. Suggestions for next steps

**Example Workflow:**

1. You run tests:
```bash
pytest -v
```

2. You manually trigger the hook in Kiro IDE

3. Kiro provides summary:
```
📊 Test Execution Summary
========================
Total Tests: 8
✅ Passed: 6
❌ Failed: 2
⏭️ Skipped: 0
⏱️ Duration: 23.5s

Failed Tests:
1. tests/selenium/test_login.py::test_login_invalid_credentials
   Error: Element not found: #error-message
   
2. tests/playwright/test_checkout.py::test_checkout_empty_cart
   Error: Timeout waiting for element: .cart-empty-message

💡 Suggestions:
- Check if selectors have changed (#error-message, .cart-empty-message)
- Verify application is running and accessible
- Review screenshots in reports/screenshots/ for visual debugging
```

---

### Q18: Can I create custom hooks?

**A:** Yes! Create a new JSON file in `.kiro/hooks/`:

**Example: Hook to run linter on save**

```json
{
  "name": "Lint Python Files",
  "version": "1.0.0",
  "description": "Run flake8 linter when Python files are saved",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "flake8 {file_path}"
  }
}
```

**Example: Hook to ask Kiro to explain test failures**

```json
{
  "name": "Explain Test Failure",
  "version": "1.0.0",
  "description": "Ask Kiro to explain why a test failed",
  "when": {
    "type": "userTriggered"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Analyze the test failure in {file_path} and explain the root cause. Suggest fixes."
  }
}
```

---

### Q19: What hook event types are available?

**A:** Kiro supports these event types:

| Event Type | Trigger | Use Case |
|------------|---------|----------|
| `fileEdited` | File saved | Code review, linting |
| `fileCreated` | New file created | Scaffolding, templates |
| `fileDeleted` | File deleted | Cleanup, warnings |
| `userTriggered` | Manual trigger | On-demand actions |
| `promptSubmit` | Message sent to Kiro | Pre-processing |
| `agentStop` | Kiro completes task | Post-processing |
| `preToolUse` | Before tool execution | Validation, approval |
| `postToolUse` | After tool execution | Verification, logging |
| `preTaskExecution` | Before spec task starts | Pre-checks |
| `postTaskExecution` | After spec task completes | Post-checks, testing |

---

### Q20: What hook action types are available?

**A:** Two action types:

**1. `askAgent`** - Send a prompt to Kiro AI agent

```json
{
  "then": {
    "type": "askAgent",
    "prompt": "Review this test file for convention violations."
  }
}
```

**2. `runCommand`** - Execute a shell command

```json
{
  "then": {
    "type": "runCommand",
    "command": "pytest {file_path} -v"
  }
}
```

**Variables available in prompts/commands:**
- `{file_path}` - Path to the file that triggered the hook
- `{file_name}` - Name of the file
- `{directory}` - Directory containing the file

---

### Q21: Can I disable a specific hook?

**A:** Yes! Edit the hook file and set `"enabled": false`:

```json
{
  "name": "Test File Convention Review",
  "enabled": false,
  "version": "1.0.0",
  ...
}
```

Or rename the file:
```bash
mv .kiro/hooks/test-file-review.kiro.hook .kiro/hooks/test-file-review.kiro.hook.disabled
```

---

### Q22: How do I test if a hook is working?

**A:**

**For `fileEdited` hooks:**
1. Open a file matching the pattern (e.g., `tests/selenium/test_example.py`)
2. Make a change
3. Save the file
4. Check if Kiro provides feedback

**For `fileCreated` hooks:**
1. Create a new file matching the pattern (e.g., `tests/playwright/test_new.py`)
2. Check if Kiro scaffolds the file

**For `userTriggered` hooks:**
1. Open Kiro IDE
2. Find the hook in the hooks panel
3. Click "Trigger" or use the command palette
4. Check if action executes

**Debugging:**
- Check Kiro IDE logs for hook execution
- Verify hook file has valid JSON syntax
- Verify file patterns match your files

---

### Q23: Can hooks run shell commands?

**A:** Yes! Use `"type": "runCommand"`:

**Example: Run tests on file save**

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

**Example: Run linter**

```json
{
  "name": "Lint on Save",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "flake8 {file_path}"
  }
}
```

**Security Note:** Be careful with `runCommand` hooks. They execute shell commands with your user permissions.

---

## Troubleshooting Questions

### Q24: Steering files aren't loading. What's wrong?

**A:** Check these common issues:

**1. Frontmatter syntax error:**
```markdown
❌ Wrong:
title: Test Writing Guide
description: Guide for writing tests

✅ Correct:
---
title: Test Writing Guide
description: Guide for writing tests
---
```

**2. Keywords don't match:**
```markdown
❌ Keywords too specific:
keywords: [very-specific-edge-case]

✅ Keywords broad enough:
keywords: [test, selenium, playwright, write test]
```

**3. File location wrong:**
```bash
❌ Wrong: docs/test-writing-guide.md
✅ Correct: .kiro/steering/test-writing-guide.md
```

**4. Inclusion type wrong:**
```markdown
❌ Manual inclusion (requires explicit reference):
inclusion: manual

✅ Auto inclusion (loads automatically):
inclusion: auto
```

---

### Q25: Hooks aren't triggering. What's wrong?

**A:** Check these common issues:

**1. Invalid JSON syntax:**
```bash
# Validate JSON
cat .kiro/hooks/my-hook.kiro.hook | python -m json.tool
```

**2. File pattern doesn't match:**
```json
❌ Wrong pattern:
"patterns": ["*.py"]  // Only matches root directory

✅ Correct pattern:
"patterns": ["**/*.py"]  // Matches all subdirectories
```

**3. Hook disabled:**
```json
❌ Disabled:
"enabled": false

✅ Enabled:
"enabled": true
```

**4. Event type wrong:**
```json
❌ Wrong event:
"type": "fileSaved"  // Not a valid event type

✅ Correct event:
"type": "fileEdited"
```

---

### Q26: Kiro isn't using my custom steering file. Why?

**A:** 

**Possible reasons:**

1. **Keywords don't match your question:**
   - Add more keywords to the frontmatter
   - Use broader, more common keywords

2. **Inclusion type is manual:**
   - Change `inclusion: manual` to `inclusion: auto`
   - Or explicitly reference: "Use #my-custom-guide to help me..."

3. **File not in `.kiro/steering/` directory:**
   - Move file to correct location

4. **Frontmatter missing or malformed:**
   - Verify frontmatter has opening and closing `---`
   - Check YAML syntax is correct

**Test it:**
```
Ask Kiro: "What steering files do you have access to?"
```

---

### Q27: Can I see which hooks are active?

**A:** Yes! In Kiro IDE:

1. **Hooks Panel:**
   - Open Kiro IDE
   - Look for "Hooks" or "Agent Hooks" panel
   - Shows all hooks with enabled/disabled status

2. **Command Palette:**
   - Open command palette (Ctrl+Shift+P / Cmd+Shift+P)
   - Type "Kiro: List Hooks"
   - Shows all hooks

3. **File System:**
```bash
ls -lh .kiro/hooks/
cat .kiro/hooks/*.kiro.hook | grep "name"
```

---

## Advanced Usage Questions

### Q28: Can I use steering files for non-testing documentation?

**A:** Yes! Steering files can document any aspect of your project:

**Example: API Documentation**

```markdown
---
title: API Integration Guide
description: Guide for integrating with our REST API
inclusion: auto
keywords: [api, rest, endpoint, integration]
---

# API Integration Guide

## Authentication
Use Bearer token authentication:
\`\`\`python
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(API_URL, headers=headers)
\`\`\`

## Endpoints
- GET /api/users - List users
- POST /api/users - Create user
...
```

**Example: Database Schema**

```markdown
---
title: Database Schema Guide
description: Database schema and migration guide
inclusion: auto
keywords: [database, schema, migration, sql]
---

# Database Schema

## Users Table
\`\`\`sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
\`\`\`
...
```

---

### Q29: Can hooks chain together?

**A:** Not directly, but you can achieve chaining through:

**Option 1: Use `askAgent` to trigger multiple actions**

```json
{
  "name": "Review and Test",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review this test file for conventions, then run the tests using pytest {file_path}"
  }
}
```

**Option 2: Use shell script in `runCommand`**

```json
{
  "name": "Lint, Format, and Test",
  "when": {
    "type": "fileEdited",
    "patterns": ["tests/**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "flake8 {file_path} && black {file_path} && pytest {file_path}"
  }
}
```

---

### Q30: Can I use hooks for CI/CD integration?

**A:** Yes! Use `postTaskExecution` or `agentStop` hooks:

**Example: Run tests after spec task completes**

```json
{
  "name": "Run Tests After Implementation",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "runCommand",
    "command": "pytest -v"
  }
}
```

**Example: Deploy after successful tests**

```json
{
  "name": "Deploy on Success",
  "version": "1.0.0",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "If all tests passed, ask user if they want to deploy to staging"
  }
}
```

---

### Q31: How do I share steering files and hooks with my team?

**A:** Steering files and hooks are part of your repository:

**1. Commit to Git:**
```bash
git add .kiro/steering/
git add .kiro/hooks/
git commit -m "Add Kiro IDE integration"
git push
```

**2. Team members clone and get them automatically:**
```bash
git clone <repository-url>
cd test-automation-framework
# .kiro/ directory is already there!
```

**3. Document in README.md:**
```markdown
## Kiro IDE Integration

This project includes Kiro IDE integration:
- Steering files in `.kiro/steering/`
- Hooks in `.kiro/hooks/`

See KIRO_INTEGRATION_FAQ.md for details.
```

---

### Q32: Can I version control steering files and hooks?

**A:** Yes! They should be version controlled:

**Add to Git:**
```bash
git add .kiro/
git commit -m "Add Kiro IDE integration"
```

**Update `.gitignore` to exclude user-specific settings:**
```gitignore
# Kiro user settings (don't commit)
.kiro/settings/user-preferences.json

# Kiro steering files and hooks (DO commit)
# .kiro/steering/
# .kiro/hooks/
```

**Benefits:**
- Team shares same conventions
- Changes are tracked
- Easy to roll back if needed
- New team members get integration automatically

---

### Q33: How do I update steering files without breaking existing functionality?

**A:** Follow these best practices:

**1. Test changes locally first:**
```bash
# Make changes to steering file
vim .kiro/steering/test-writing-guide.md

# Test with Kiro
# Ask: "How do I write a Selenium test?"
# Verify Kiro uses updated guidance
```

**2. Use version control:**
```bash
git checkout -b update-steering-files
# Make changes
git commit -m "Update test-writing-guide with new conventions"
git push
# Create PR for team review
```

**3. Document changes in CHANGELOG.md:**
```markdown
## [0.2.0] - 2024-02-01

### Changed
- Updated test-writing-guide.md with Page Object Model examples
- Added custom test data management conventions
```

**4. Communicate to team:**
- Send email about changes
- Update team documentation
- Provide examples of new conventions

---

### Q34: Can I use steering files to enforce coding standards?

**A:** Yes! Combine steering files with hooks:

**1. Document standards in steering file:**

`.kiro/steering/coding-standards.md`:
```markdown
---
title: Coding Standards
description: Team coding standards and conventions
inclusion: auto
keywords: [standards, conventions, style, code review]
---

# Coding Standards

## Python Style
- Follow PEP 8
- Maximum line length: 100 characters
- Use type hints for function parameters
- Use docstrings for all functions

## Test Conventions
- One assertion per test
- Use descriptive test names
- Add docstrings to all tests
...
```

**2. Create hook to enforce:**

`.kiro/hooks/enforce-standards.kiro.hook`:
```json
{
  "name": "Enforce Coding Standards",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.py"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review {file_path} against our coding standards. Check: PEP 8 compliance, type hints, docstrings, line length. Provide specific feedback."
  }
}
```

**3. Optionally run linter:**

```json
{
  "name": "Run Linter",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "flake8 {file_path} --max-line-length=100"
  }
}
```

---

### Q35: What are best practices for steering files?

**A:**

**1. Keep them concise:**
- Focus on examples over explanations
- Use code snippets liberally
- Avoid long paragraphs

**2. Use clear keywords:**
```markdown
❌ Too specific:
keywords: [very-specific-edge-case-scenario]

✅ Broad and relevant:
keywords: [test, selenium, playwright, write test, create test]
```

**3. Include examples:**
```markdown
✅ Good:
## Writing Selenium Tests

Example:
\`\`\`python
@pytest.mark.selenium
def test_login_success(selenium_driver):
    """Test successful login."""
    driver = selenium_driver
    driver.get("https://example.com/login")
    ...
\`\`\`
```

**4. Reference other files:**
```markdown
For API spec, see #[[file:api-spec.yaml]]
```

**5. Keep them up to date:**
- Review quarterly
- Update when conventions change
- Version control changes

---

### Q36: What are best practices for hooks?

**A:**

**1. Start simple:**
```json
// Start with basic hooks
{
  "name": "Review Test File",
  "when": {"type": "fileEdited", "patterns": ["tests/**/*.py"]},
  "then": {"type": "askAgent", "prompt": "Review for conventions"}
}
```

**2. Use descriptive names:**
```json
❌ Bad: "Hook 1"
✅ Good: "Test File Convention Review"
```

**3. Be specific with patterns:**
```json
❌ Too broad:
"patterns": ["**/*"]  // Triggers on every file

✅ Specific:
"patterns": ["tests/**/*.py"]  // Only test files
```

**4. Provide clear prompts:**
```json
❌ Vague:
"prompt": "Check this file"

✅ Clear:
"prompt": "Review this test file for: 1) Correct fixture usage, 2) Appropriate marker, 3) Naming convention, 4) Docstring present"
```

**5. Test before committing:**
- Trigger hook manually
- Verify it works as expected
- Check for performance impact

---

## Summary

**Steering Files:**
- Provide contextual guidance to Kiro AI
- Loaded automatically based on keywords
- Customizable for team conventions
- Version controlled with your code

**Hooks:**
- Automate repetitive tasks
- Trigger on IDE events
- Can ask Kiro or run commands
- Enable AI-assisted development

**Benefits:**
- Faster test authoring
- Consistent code quality
- Reduced onboarding time
- Automated code review

**Getting Started:**
1. Review existing steering files in `.kiro/steering/`
2. Test existing hooks by saving/creating test files
3. Customize for your team's needs
4. Share with team via Git

---

**FAQ Version:** v0.1.0  
**Last Updated:** 2024-01-15  
**Questions?** Open an issue or contact the QE team lead.

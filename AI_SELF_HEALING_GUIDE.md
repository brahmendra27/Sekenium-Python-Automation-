# AI Self-Healing Guide

**Version:** v0.2.0  
**Last Updated:** 2024-01-15  
**Status:** ✅ Available (New Feature)

---

## 🎯 Overview

The Test Automation Framework now includes **AI-assisted self-healing capabilities** for element locators. When an element cannot be found using the original locator, the framework automatically tries alternative strategies to locate the element.

### Benefits

- ✅ **Reduced Test Flakiness**: Tests don't fail immediately when selectors change
- ✅ **Automatic Recovery**: Framework tries multiple strategies before failing
- ✅ **Actionable Insights**: Get suggestions for permanent locator improvements
- ✅ **AI-Assisted Debugging**: Kiro AI analyzes failures and suggests fixes
- ✅ **Healing History**: Track which locators were healed and how

---

## 🚀 Quick Start

### Option 1: Use Self-Healing in Tests (Recommended)

```python
import pytest
from selenium.webdriver.common.by import By
from framework.self_healing import SelfHealingLocator

@pytest.mark.selenium
@pytest.mark.self_healing
def test_login_with_healing(selenium_driver):
    """Test with self-healing enabled."""
    driver = selenium_driver
    healer = SelfHealingLocator(driver, enable_logging=True)
    
    # This will try multiple strategies if ID "username" fails
    username = healer.find_element_with_healing(By.ID, "username")
    if username:
        username.send_keys("testuser")
    
    # Print healing report after test
    print(healer.get_healing_report())
```

### Option 2: Use AI-Assisted Healing Hook

The framework includes a Kiro hook that automatically asks AI for help when tests fail:

**Location:** `.kiro/hooks/ai-element-healer.kiro.hook`

**How it works:**
1. Test fails due to element not found
2. Hook triggers automatically
3. Kiro AI analyzes the error
4. Kiro suggests fixes (alternative locators, timing issues, etc.)

---

## 📚 Self-Healing Strategies

The self-healing module tries these strategies in order:

### 1. Original Locator
Try the original locator first (fastest path).

### 2. Alternative Attributes
- **For ID locators**: Try `name`, CSS `#id`, XPath `//*[@id='...']`
- **For Name locators**: Try `id`, CSS `[name='...']`, XPath `//*[@name='...']`
- **For Class locators**: Try CSS `.class`, XPath `//*[contains(@class, '...')]`

### 3. Partial Matching
- Try `contains()` for partial matches
- Example: `username-input-field` matches `username`

### 4. Modern Attributes
- `data-testid` (common in React/Vue apps)
- `aria-label` (accessibility attribute)
- `role` (ARIA role attribute)

### 5. Fuzzy Matching
- Try variations of the original locator
- Case-insensitive matching
- Whitespace-tolerant matching

---

## 🔧 Usage Examples

### Example 1: Basic Self-Healing

```python
from framework.self_healing import SelfHealingLocator
from selenium.webdriver.common.by import By

def test_example(selenium_driver):
    healer = SelfHealingLocator(selenium_driver)
    
    # Original locator: By.ID, "submit-button"
    # If it fails, tries:
    # - By.NAME, "submit-button"
    # - By.CSS_SELECTOR, "#submit-button"
    # - By.XPATH, "//*[@id='submit-button']"
    # - By.CSS_SELECTOR, "[data-testid='submit-button']"
    # - By.CSS_SELECTOR, "[aria-label*='submit-button']"
    
    button = healer.find_element_with_healing(By.ID, "submit-button")
    if button:
        button.click()
```

### Example 2: Get Healing Report

```python
def test_with_report(selenium_driver):
    healer = SelfHealingLocator(selenium_driver)
    
    # Perform test actions with healing
    username = healer.find_element_with_healing(By.ID, "username")
    password = healer.find_element_with_healing(By.ID, "password")
    submit = healer.find_element_with_healing(By.ID, "submit")
    
    # Get healing report
    report = healer.get_healing_report()
    print(report)
    
    # Output:
    # Self-Healing Report
    # ==================================================
    # 
    # 1. Healing Strategy: name_attribute
    #    Original: By.ID=username
    #    Healed:   By.NAME=username
    #    ✅ Success
    # 
    # 2. Healing Strategy: data_testid
    #    Original: By.ID=submit
    #    Healed:   By.CSS_SELECTOR=[data-testid='submit']
    #    ✅ Success
```

### Example 3: Get Locator Improvement Suggestions

```python
def test_with_suggestions(selenium_driver):
    healer = SelfHealingLocator(selenium_driver)
    
    # Perform test with healing
    element = healer.find_element_with_healing(By.ID, "old-id")
    
    # Get suggestions for permanent fixes
    suggestions = healer.suggest_locator_improvements()
    for suggestion in suggestions:
        print(suggestion)
    
    # Output:
    # Consider updating locator:
    #   From: By.ID='old-id'
    #   To:   By.CSS_SELECTOR='[data-testid='new-id']'
    #   Reason: Healed using 'data_testid' strategy
```

### Example 4: Integrate with Existing Fixtures

Add to `tests/selenium/conftest.py`:

```python
from framework.self_healing import SelfHealingLocator

@pytest.fixture
def self_healing_driver(selenium_driver):
    """Selenium driver with self-healing enabled by default."""
    healer = SelfHealingLocator(selenium_driver, enable_logging=True)
    
    # Monkey-patch find_element to use self-healing
    original_find_element = selenium_driver.find_element
    
    def find_element_with_healing(by, value):
        element = healer.find_element_with_healing(by, value)
        if element is None:
            # Fall back to original (will raise exception)
            return original_find_element(by, value)
        return element
    
    selenium_driver.find_element = find_element_with_healing
    selenium_driver.healer = healer
    
    yield selenium_driver
    
    # Print healing report after test
    if healer.healing_history:
        print("\n" + healer.get_healing_report())
        print("\n🔧 Suggested Improvements:")
        for suggestion in healer.suggest_locator_improvements():
            print(suggestion)

# Use in tests:
def test_with_auto_healing(self_healing_driver):
    """Test automatically uses self-healing."""
    driver = self_healing_driver
    
    # find_element now uses self-healing automatically
    driver.find_element(By.ID, "username").send_keys("test")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "submit").click()
    
    # Healing report printed automatically after test
```

---

## 🤖 AI-Assisted Healing with Kiro

### How It Works

1. **Test fails** with element not found error
2. **Hook triggers** (`.kiro/hooks/ai-element-healer.kiro.hook`)
3. **Kiro AI analyzes** the error output
4. **Kiro suggests fixes**:
   - Alternative locators
   - Timing issues (add waits)
   - Iframe issues
   - Dynamic content issues
   - Specific code fixes

### Example Kiro AI Response

```
🔍 Analysis of Element Failure:

Error: NoSuchElementException: Unable to locate element: By.ID="submit-button"

Possible Causes:
1. ❌ Selector Changed: The ID might have been updated in the UI
2. ⏱️ Timing Issue: Element might not be loaded yet
3. 🖼️ Iframe: Element might be inside an iframe

Suggested Fixes:

1. Try Alternative Locators:
   ```python
   # Try data-testid
   driver.find_element(By.CSS_SELECTOR, "[data-testid='submit']")
   
   # Try button text
   driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
   
   # Try class name
   driver.find_element(By.CLASS_NAME, "btn-submit")
   ```

2. Add Explicit Wait:
   ```python
   from selenium.webdriver.support.ui import WebDriverWait
   from selenium.webdriver.support import expected_conditions as EC
   
   wait = WebDriverWait(driver, 10)
   button = wait.until(EC.presence_of_element_located((By.ID, "submit-button")))
   ```

3. Check for Iframe:
   ```python
   # Switch to iframe if element is inside one
   driver.switch_to.frame("iframe-name")
   button = driver.find_element(By.ID, "submit-button")
   ```

Would you like me to update the test with these fixes?
```

---

## 📊 Healing Strategies by Locator Type

### By.ID

| Strategy | Example | When It Works |
|----------|---------|---------------|
| Original | `By.ID, "username"` | Element has ID attribute |
| Name attribute | `By.NAME, "username"` | Element has matching name |
| CSS ID | `By.CSS_SELECTOR, "#username"` | CSS selector works |
| XPath ID | `By.XPATH, "//*[@id='username']"` | XPath works |
| Partial ID | `By.XPATH, "//*[contains(@id, 'username')]"` | ID contains the value |
| Data-testid | `By.CSS_SELECTOR, "[data-testid='username']"` | Modern apps with test IDs |

### By.NAME

| Strategy | Example | When It Works |
|----------|---------|---------------|
| Original | `By.NAME, "email"` | Element has name attribute |
| ID attribute | `By.ID, "email"` | Element has matching ID |
| CSS name | `By.CSS_SELECTOR, "[name='email']"` | CSS selector works |
| XPath name | `By.XPATH, "//*[@name='email']"` | XPath works |

### By.CLASS_NAME

| Strategy | Example | When It Works |
|----------|---------|---------------|
| Original | `By.CLASS_NAME, "btn-primary"` | Element has class |
| CSS class | `By.CSS_SELECTOR, ".btn-primary"` | CSS selector works |
| XPath class | `By.XPATH, "//*[contains(@class, 'btn-primary')]"` | XPath works |

### By.CSS_SELECTOR

| Strategy | Example | When It Works |
|----------|---------|---------------|
| Original | `By.CSS_SELECTOR, "#submit"` | CSS selector works |
| XPath from CSS | `By.XPATH, "//*[@id='submit']"` | Converted to XPath |
| Data-testid | `By.CSS_SELECTOR, "[data-testid='submit']"` | Modern apps |

### By.XPATH

| Strategy | Example | When It Works |
|----------|---------|---------------|
| Original | `By.XPATH, "//button[@id='submit']"` | XPath works |
| Partial text | `By.XPATH, "//*[contains(text(), 'Submit')]"` | Text-based locator |
| Data-testid | `By.CSS_SELECTOR, "[data-testid='submit']"` | Modern apps |

---

## 🎓 Best Practices

### 1. Enable Logging

```python
healer = SelfHealingLocator(driver, enable_logging=True)
```

This helps you understand which strategies are being tried.

### 2. Review Healing Reports

Always review healing reports to identify patterns:

```python
print(healer.get_healing_report())
```

### 3. Apply Permanent Fixes

Don't rely on healing forever. Use suggestions to update locators:

```python
suggestions = healer.suggest_locator_improvements()
for suggestion in suggestions:
    print(suggestion)
    # Update your test code with the suggested locator
```

### 4. Use Modern Locators

Prefer stable locators that are less likely to change:

✅ **Good:**
- `data-testid` attributes
- `aria-label` attributes
- Semantic HTML (e.g., `<button>`, `<input type="submit">`)

❌ **Avoid:**
- Generated IDs (e.g., `id="input-1234567890"`)
- Generic class names (e.g., `class="btn"`)
- Deep XPath (e.g., `/html/body/div[3]/div[2]/form/input[5]`)

### 5. Combine with Explicit Waits

Self-healing doesn't solve timing issues. Use explicit waits:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = healer.find_element_with_healing(By.ID, "username")
if element:
    wait.until(EC.element_to_be_clickable((By.ID, "username")))
    element.send_keys("test")
```

---

## 🔍 Troubleshooting

### Issue: Self-healing not working

**Solution:**
1. Check if `framework/self_healing.py` exists
2. Verify import: `from framework.self_healing import SelfHealingLocator`
3. Enable logging: `SelfHealingLocator(driver, enable_logging=True)`
4. Check console output for healing attempts

### Issue: All strategies fail

**Solution:**
1. Element might not exist on the page
2. Element might be in an iframe (switch to iframe first)
3. Element might be dynamically loaded (add wait)
4. Check browser console for JavaScript errors

### Issue: Healing is too slow

**Solution:**
1. Reduce number of strategies (customize `_get_healing_strategies`)
2. Use more specific original locators
3. Add explicit waits before healing attempts

---

## 📈 Metrics and Reporting

### Track Healing Success Rate

```python
def test_with_metrics(selenium_driver):
    healer = SelfHealingLocator(selenium_driver)
    
    # Perform test
    elements_found = 0
    elements_healed = 0
    
    for locator in [(By.ID, "username"), (By.ID, "password"), (By.ID, "submit")]:
        element = healer.find_element_with_healing(*locator)
        if element:
            elements_found += 1
            if healer.healing_history:
                elements_healed += 1
    
    print(f"Elements found: {elements_found}/3")
    print(f"Elements healed: {elements_healed}")
    print(f"Healing rate: {(elements_healed/elements_found)*100:.1f}%")
```

### Generate Healing Report for CI/CD

```python
import json

def save_healing_report(healer, filepath="reports/healing_report.json"):
    """Save healing report as JSON for CI/CD analysis."""
    report = {
        "total_healings": len(healer.healing_history),
        "healings": [
            {
                "original_by": str(h['original'][0]),
                "original_value": h['original'][1],
                "healed_by": str(h['healed'][0]),
                "healed_value": h['healed'][1],
                "strategy": h['strategy']
            }
            for h in healer.healing_history
        ]
    }
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
```

---

## 🚀 Next Steps

1. **Try the example test:**
   ```bash
   pytest tests/selenium/test_self_healing_example.py -v
   ```

2. **Enable AI-assisted healing:**
   - The hook is already created at `.kiro/hooks/ai-element-healer.kiro.hook`
   - It triggers automatically when tests fail

3. **Integrate into existing tests:**
   - Add `SelfHealingLocator` to your conftest.py
   - Update tests to use `self_healing_driver` fixture

4. **Monitor healing reports:**
   - Review healing reports after test runs
   - Apply permanent fixes based on suggestions

---

## 📞 Support

**Questions about self-healing?**

1. Check this guide
2. Review example test: `tests/selenium/test_self_healing_example.py`
3. Check healing module: `framework/self_healing.py`
4. Ask Kiro: "How do I use self-healing in my tests?"
5. Contact QE team lead

---

**AI Self-Healing Guide Version:** v0.2.0  
**Last Updated:** 2024-01-15  
**Status:** ✅ Available

🎉 **Self-healing is now part of your framework!**

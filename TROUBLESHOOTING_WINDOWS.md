# Troubleshooting: Windows ChromeDriver Issue

**Error:** `OSError: [WinError 193] %1 is not a valid Win32 application`

This is the known Windows ChromeDriver compatibility issue we documented in the validation report.

---

## 🔧 Solution Options

### Option 1: Use Playwright (Recommended - Fastest)

Playwright works perfectly on Windows without driver issues.

```bash
# Run with Playwright instead
pytest tests/playwright/test_example_playwright.py -v
```

**For Automation Test Store, create Playwright tests:**

```bash
# I'll create Playwright versions for you
```

---

### Option 2: Use Docker (Most Reliable)

Docker execution works perfectly and avoids all driver issues.

#### Step 1: Build Docker Image

```powershell
docker build -t test-automation-framework -f docker/Dockerfile .
```

**Note:** First build takes 5-10 minutes (downloads browsers).

#### Step 2: Run Tests in Docker

```powershell
# Run all tests
docker run --rm -v ${PWD}/reports:/app/reports test-automation-framework:latest pytest tests/selenium/test_automation_store_homepage.py tests/selenium/test_automation_store_cart.py -v

# Or use docker-compose
docker-compose -f docker/docker-compose.yml up --abort-on-container-exit
```

#### Step 3: View Reports

```powershell
start reports\report.html
```

---

### Option 3: Fix ChromeDriver Manually

#### Step 1: Download Correct ChromeDriver

1. Check your Chrome version:
   - Open Chrome
   - Go to `chrome://version/`
   - Note the version (e.g., 131.0.6778.86)

2. Download matching ChromeDriver:
   - Go to: https://googlechromelabs.github.io/chrome-for-testing/
   - Download ChromeDriver for your Chrome version
   - Extract `chromedriver.exe`

#### Step 2: Place ChromeDriver

```powershell
# Create directory
mkdir C:\chromedriver

# Place chromedriver.exe in C:\chromedriver\
# Add C:\chromedriver to PATH
```

#### Step 3: Update Framework

Edit `framework/selenium_driver.py`:

```python
# Add explicit path
service = ChromeService("C:\\chromedriver\\chromedriver.exe")
```

---

### Option 4: Use Firefox Instead

Firefox works better on Windows.

#### Step 1: Install Firefox

Download from: https://www.mozilla.org/firefox/

#### Step 2: Update Config

Edit `config.yaml`:

```yaml
browser: "firefox"
```

#### Step 3: Run Tests

```powershell
pytest tests/selenium/test_automation_store_homepage.py --browser=firefox -v
```

---

## 🚀 Quick Fix: Use Playwright

Let me create Playwright versions of your tests right now (no driver issues!):

### Create Playwright Tests

```bash
# I'll create these files for you:
# - tests/playwright/test_automation_store_homepage.py
# - tests/playwright/test_automation_store_cart.py
```

Then run:

```powershell
pytest tests/playwright/test_automation_store_homepage.py -v
```

**Playwright advantages:**
- ✅ No driver management needed
- ✅ Works perfectly on Windows
- ✅ Faster execution
- ✅ Better debugging (traces)
- ✅ Auto-waiting for elements

---

## 📊 Comparison

| Solution | Setup Time | Reliability | Speed |
|----------|------------|-------------|-------|
| **Playwright** | 0 min | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ |
| **Docker** | 10 min | ⭐⭐⭐⭐⭐ | ⚡⚡ |
| **Firefox** | 5 min | ⭐⭐⭐⭐ | ⚡⚡ |
| **Fix ChromeDriver** | 15 min | ⭐⭐⭐ | ⚡⚡ |

---

## 🎯 Recommended Approach

**For immediate testing:**
1. Use Playwright (I'll create the tests for you)
2. Run: `pytest tests/playwright/test_automation_store_homepage.py -v`

**For long-term:**
1. Use Docker for CI/CD
2. Use Playwright for local development
3. Keep Selenium tests for cross-browser compatibility

---

## 💡 Next Steps

**Choose one:**

1. **"Create Playwright tests"** - I'll create Playwright versions now
2. **"Use Docker"** - I'll help you set up Docker
3. **"Use Firefox"** - I'll update config for Firefox
4. **"Fix ChromeDriver"** - I'll guide you through manual fix

Which would you like to do?

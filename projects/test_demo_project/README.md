# Project Template

This is a template for creating new test automation projects.

## Setup

1. Copy this template to a new project directory:
   ```bash
   cp -r projects/_template projects/my_new_project
   ```

2. Rename template files:
   ```bash
   mv projects/my_new_project/config.yaml.template projects/my_new_project/config.yaml
   mv projects/my_new_project/tests/conftest.py.template projects/my_new_project/tests/conftest.py
   ```

3. Update `config.yaml` with your project details

4. Create page objects in `pages/` directory

5. Write tests in `tests/selenium/` or `tests/playwright/`

## Structure

```
my_project/
├── config.yaml              # Project configuration
├── pages/                   # Page Object classes
│   ├── __init__.py
│   └── home_page.py
├── tests/                   # Test files
│   ├── conftest.py          # Project fixtures
│   ├── selenium/
│   │   └── test_*.py
│   └── playwright/
│       └── test_*.py
├── test_data/               # Test data files
└── reports/                 # Generated reports
```

## Running Tests

```bash
# Run all tests for this project
pytest projects/my_project/tests/

# Run Selenium tests only
pytest projects/my_project/tests/selenium/

# Run Playwright tests only
pytest projects/my_project/tests/playwright/
```

## Next Steps

1. Create your first page object in `pages/`
2. Write your first test in `tests/selenium/` or `tests/playwright/`
3. Run tests and generate reports

# REST API and MongoDB Testing - Complete Guide

## 🎯 Overview

Your Test Automation Framework now includes comprehensive REST API and MongoDB database testing capabilities. This document provides everything you need to get started.

## 📦 What's Included

### New Capabilities
- ✅ **REST API Testing** - Test HTTP endpoints with full request/response validation
- ✅ **MongoDB Testing** - Test database operations with CRUD and advanced queries
- ✅ **Integration Testing** - Combine API and database testing for end-to-end validation

### Framework Components
- **API Client** (`framework/api_client.py`) - Full-featured HTTP client
- **MongoDB Client** (`framework/mongodb_client.py`) - Complete database client
- **Pytest Fixtures** (`conftest.py`) - Reusable test fixtures
- **Example Tests** (`tests/api/`, `tests/database/`) - 45+ working examples
- **Documentation** - 5 comprehensive guides

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

**Option A - Using PowerShell Script (Recommended):**
```powershell
.\install_api_db_dependencies.ps1
```

**Option B - Manual Installation:**
```bash
pip install -r requirements.txt
```

### Step 2: Configure Settings

Update `config.yaml`:
```yaml
# API Testing
api:
  base_url: "https://jsonplaceholder.typicode.com"
  timeout: 30
  verify_ssl: true

# MongoDB Testing
mongodb:
  connection_string: "mongodb://localhost:27017"
  database: "test_db"
```

### Step 3: Start MongoDB (for database tests)

```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Step 4: Run Example Tests

```bash
# API tests
pytest tests/api/test_api_example.py -v

# Database tests (requires MongoDB running)
pytest tests/database/test_mongodb_example.py -v

# All tests
pytest tests/ -v
```

## 📖 Documentation

| Guide | Description | When to Use |
|-------|-------------|-------------|
| **[Quick Start](API_DATABASE_QUICK_START.md)** | Get started in 5 minutes | First time setup |
| **[API Testing Guide](API_TESTING_GUIDE.md)** | Complete API testing reference | Writing API tests |
| **[MongoDB Guide](MONGODB_TESTING_GUIDE.md)** | Complete MongoDB reference | Writing DB tests |
| **[Integration Guide](API_AND_DATABASE_INTEGRATION_GUIDE.md)** | Integration patterns | End-to-end tests |
| **[Summary](API_DATABASE_TESTING_SUMMARY.md)** | Implementation overview | Understanding features |

## 💻 Code Examples

### API Test Example

```python
def test_get_user(api_client):
    """Test retrieving a user from API."""
    response = api_client.get('/users/1')
    
    assert response.status_code == 200
    user = response.json()
    assert 'name' in user
    assert 'email' in user
```

### MongoDB Test Example

```python
def test_insert_user(mongodb_client, clean_mongodb_collection):
    """Test inserting a user into database."""
    clean_mongodb_collection('users')
    
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'age': 30
    }
    
    doc_id = mongodb_client.insert_one('users', user_data)
    assert doc_id is not None
    
    # Verify insertion
    user = mongodb_client.find_one('users', {'name': 'John Doe'})
    assert user['email'] == 'john@example.com'
```

### Integration Test Example

```python
def test_api_database_integration(api_client, mongodb_client, clean_mongodb_collection):
    """Test API creates database record."""
    clean_mongodb_collection('users')
    
    # Create via API
    new_user = {'name': 'Jane Doe', 'email': 'jane@example.com'}
    response = api_client.post('/users', json_data=new_user)
    
    assert response.status_code == 201
    user_id = response.json()['id']
    
    # Verify in database
    db_user = mongodb_client.find_one('users', {'_id': user_id})
    assert db_user is not None
    assert db_user['name'] == new_user['name']
```

## 🔧 Configuration

### API Configuration Options

```yaml
api:
  base_url: "https://api.example.com"     # API base URL
  timeout: 30                              # Request timeout (seconds)
  verify_ssl: true                         # SSL verification
  default_headers:                         # Default headers
    Content-Type: "application/json"
    Accept: "application/json"
    Authorization: "Bearer your-token"     # Optional
```

### MongoDB Configuration Options

```yaml
mongodb:
  connection_string: "mongodb://localhost:27017"  # Connection string
  database: "test_db"                             # Database name
  timeout: 5000                                   # Timeout (milliseconds)
  max_pool_size: 10                               # Connection pool size
```

### Environment-Specific Configuration

Create separate config files for different environments:

```yaml
# config.dev.yaml
api:
  base_url: "http://localhost:8080/api"
mongodb:
  connection_string: "mongodb://localhost:27017"

# config.staging.yaml
api:
  base_url: "https://staging-api.example.com"
mongodb:
  connection_string: "mongodb://staging-server:27017"

# config.prod.yaml
api:
  base_url: "https://api.example.com"
mongodb:
  connection_string: "mongodb+srv://user:pass@cluster.mongodb.net"
```

## 🎓 Features Overview

### API Testing Features

| Feature | Description |
|---------|-------------|
| **HTTP Methods** | GET, POST, PUT, PATCH, DELETE |
| **Authentication** | Bearer tokens, API keys, custom headers |
| **Retry Logic** | Automatic retry with exponential backoff |
| **Logging** | Request/response logging for debugging |
| **Validation** | Response status, headers, JSON content |
| **SSL Control** | Enable/disable SSL verification |
| **Timeouts** | Configurable request timeouts |

### MongoDB Testing Features

| Feature | Description |
|---------|-------------|
| **CRUD Operations** | Create, Read, Update, Delete |
| **Queries** | Filtering, sorting, limiting |
| **Aggregation** | Pipeline operations |
| **Indexes** | Create and manage indexes |
| **Transactions** | Multi-document operations |
| **Test Helpers** | Automatic setup/cleanup |
| **Assertions** | Built-in validation helpers |

## 📁 Project Structure

```
qeautomation/
├── framework/
│   ├── api_client.py              # REST API client
│   ├── mongodb_client.py          # MongoDB client
│   ├── config.py                  # Configuration loader
│   └── ...
├── tests/
│   ├── api/                       # API tests
│   │   ├── test_api_example.py
│   │   └── README.md
│   └── database/                  # Database tests
│       ├── test_mongodb_example.py
│       └── README.md
├── conftest.py                    # Pytest fixtures
├── config.yaml                    # Configuration
├── requirements.txt               # Dependencies
├── install_api_db_dependencies.ps1  # Installation script
├── API_TESTING_GUIDE.md           # API guide
├── MONGODB_TESTING_GUIDE.md       # MongoDB guide
├── API_AND_DATABASE_INTEGRATION_GUIDE.md  # Integration guide
├── API_DATABASE_QUICK_START.md    # Quick start
└── README_API_DATABASE.md         # This file
```

## 🧪 Running Tests

### Basic Commands

```bash
# Run all tests
pytest tests/ -v

# Run API tests only
pytest tests/api/ -v

# Run database tests only
pytest tests/database/ -v

# Run specific test file
pytest tests/api/test_api_example.py -v

# Run specific test
pytest tests/api/test_api_example.py::test_get_request -v
```

### Advanced Commands

```bash
# Run with detailed output
pytest tests/ -v -s

# Run with coverage
pytest tests/ --cov=framework --cov-report=html

# Run with HTML report
pytest tests/ --html=reports/report.html

# Run with Allure report
pytest tests/ --alluredir=reports/allure-results
allure serve reports/allure-results

# Run tests matching pattern
pytest tests/ -k "user" -v

# Run with markers
pytest tests/ -m smoke -v
```

## 🛠️ Available Fixtures

### API Testing Fixtures

```python
def test_example(api_client):
    """Use api_client fixture for API testing."""
    response = api_client.get('/endpoint')
    assert response.status_code == 200

def test_with_wrapper(api_client, api_response_wrapper):
    """Use api_response_wrapper for enhanced assertions."""
    response = api_client.get('/endpoint')
    api_response = api_response_wrapper(response)
    api_response.assert_status_code(200)
    api_response.assert_json_contains('id')
```

### MongoDB Testing Fixtures

```python
def test_with_client(mongodb_client, clean_mongodb_collection):
    """Use mongodb_client for database operations."""
    clean_mongodb_collection('users')
    doc_id = mongodb_client.insert_one('users', {'name': 'John'})
    assert doc_id is not None

def test_with_helper(mongodb_test_helper):
    """Use mongodb_test_helper for automatic cleanup."""
    mongodb_test_helper.setup_test_collection('users', [
        {'name': 'User 1'},
        {'name': 'User 2'}
    ])
    # Cleanup happens automatically
```

## 📊 Test Reports

### HTML Report

```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in your browser.

### Allure Report

```bash
# Generate results
pytest tests/ --alluredir=reports/allure-results

# View report
allure serve reports/allure-results
```

### Coverage Report

```bash
pytest tests/ --cov=framework --cov-report=html
```

Open `htmlcov/index.html` in your browser.

## 🐛 Troubleshooting

### API Tests

**Problem: Connection errors**
```yaml
# Solution: Increase timeout
api:
  timeout: 60
```

**Problem: SSL certificate errors**
```yaml
# Solution: Disable SSL verification (dev only)
api:
  verify_ssl: false
```

### MongoDB Tests

**Problem: Connection refused**
```bash
# Solution: Start MongoDB
# Windows
net start MongoDB

# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

**Problem: Authentication failed**
```yaml
# Solution: Add credentials
mongodb:
  connection_string: "mongodb://username:password@localhost:27017"
```

## 📚 Learning Resources

### For Beginners
1. Start with [Quick Start Guide](API_DATABASE_QUICK_START.md)
2. Run example tests
3. Modify examples for your use case

### For Intermediate Users
1. Read [API Testing Guide](API_TESTING_GUIDE.md)
2. Read [MongoDB Testing Guide](MONGODB_TESTING_GUIDE.md)
3. Explore advanced features

### For Advanced Users
1. Read [Integration Guide](API_AND_DATABASE_INTEGRATION_GUIDE.md)
2. Build custom fixtures
3. Optimize test performance

## 🎯 Best Practices

### API Testing
- ✅ Use fixtures for client setup
- ✅ Test both success and error cases
- ✅ Validate response structure
- ✅ Use parametrized tests
- ✅ Clean up test data
- ✅ Use environment variables for secrets

### MongoDB Testing
- ✅ Use `clean_mongodb_collection` fixture
- ✅ Use `mongodb_test_helper` for cleanup
- ✅ Isolate test data
- ✅ Verify data integrity
- ✅ Test edge cases
- ✅ Use indexes for performance

### Integration Testing
- ✅ Test complete workflows
- ✅ Verify data consistency
- ✅ Test side effects
- ✅ Handle errors properly
- ✅ Test with realistic data
- ✅ Measure performance

## 🔗 Quick Links

- **Installation**: Run `install_api_db_dependencies.ps1`
- **Quick Start**: [API_DATABASE_QUICK_START.md](API_DATABASE_QUICK_START.md)
- **API Guide**: [API_TESTING_GUIDE.md](API_TESTING_GUIDE.md)
- **MongoDB Guide**: [MONGODB_TESTING_GUIDE.md](MONGODB_TESTING_GUIDE.md)
- **Integration Guide**: [API_AND_DATABASE_INTEGRATION_GUIDE.md](API_AND_DATABASE_INTEGRATION_GUIDE.md)
- **Examples**: `tests/api/` and `tests/database/`

## ✅ Checklist

Before you start:
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Update `config.yaml` with your settings
- [ ] Start MongoDB (for database tests)
- [ ] Run example tests to verify setup
- [ ] Read the Quick Start guide

## 🎉 You're Ready!

Your framework now supports:
1. **Web UI Testing** (Selenium/Playwright) ✅
2. **REST API Testing** (requests) ✅
3. **MongoDB Testing** (pymongo) ✅
4. **Integration Testing** ✅

Start testing with:
```bash
pytest tests/ -v
```

Happy Testing! 🚀

---

**Need Help?**
- Check the documentation guides
- Review example tests
- Refer to troubleshooting section

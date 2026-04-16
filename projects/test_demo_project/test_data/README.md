# Test Data Directory

Place your test data files here.

## Supported Formats

- **JSON** - Structured data
- **CSV** - Tabular data
- **YAML** - Configuration-style data
- **TXT** - Simple text data

## Examples

### users.json
```json
{
  "valid_users": [
    {
      "email": "test1@example.com",
      "password": "Test123!",
      "first_name": "John",
      "last_name": "Doe"
    }
  ],
  "invalid_users": [
    {
      "email": "invalid@example.com",
      "password": "wrong"
    }
  ]
}
```

### products.csv
```csv
product_id,name,price,category
1,Product A,29.99,Electronics
2,Product B,49.99,Clothing
3,Product C,19.99,Books
```

## Loading Test Data in Tests

### JSON
```python
import json
from pathlib import Path

@pytest.fixture
def test_users():
    data_file = Path(__file__).parent.parent / "test_data" / "users.json"
    with open(data_file) as f:
        return json.load(f)

def test_login(selenium_driver, test_users):
    user = test_users['valid_users'][0]
    # Use user data in test
```

### CSV
```python
import csv
from pathlib import Path

@pytest.fixture
def test_products():
    data_file = Path(__file__).parent.parent / "test_data" / "products.csv"
    with open(data_file) as f:
        return list(csv.DictReader(f))

def test_product_search(selenium_driver, test_products):
    product = test_products[0]
    # Use product data in test
```

## Best Practices

1. **Separate test data from code** - Keep data files here
2. **Use fixtures to load data** - Create reusable fixtures
3. **Version control test data** - Commit data files to Git
4. **Use realistic data** - Mirror production data structure
5. **Document data format** - Add README for complex data

# API Contract Schemas

Store JSON Schema files here for contract testing.

## Usage

```python
from framework.contract_helper import ContractHelper

contract = ContractHelper()  # defaults to this directory
contract.assert_contract(response_data, "order_response.json")
```

## Naming Convention

- `{object}_response.json` — API response schemas
- `{object}_request.json` — API request schemas
- `snapshots/` — Auto-generated structure snapshots

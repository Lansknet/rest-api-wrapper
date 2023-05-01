# Lansknet API Wrapper

This is a wrapper for the Lansknet API. It is written in Python and is designed to be used with the [Lansknet API](https://api-lansknet.me).

## Installation

To install the wrapper, run the following command:

```bash
pip install lansknet
```

## Usage

To use the wrapper, you must first import it:

```python
from LansknetAPI import LansknetAPI

api = LansknetAPI("https://api-lansknet.me", "api_key")

print(api.get_all_company_campaigns(1))
print(api.get_all_service_campaigns(1, 1))
print(api.get_all_employees(1))
print(api.get_all_services(1))

```

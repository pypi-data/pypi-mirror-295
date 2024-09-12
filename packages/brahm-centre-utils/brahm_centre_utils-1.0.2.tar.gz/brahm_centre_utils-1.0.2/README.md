# Brahm Centre Utils

Brahm Centre Utils is a collection of internal utility functions designed to facilitate common tasks at Brahm Centre. This package includes functions for Salesforce interactions, data processing, and more.

## Installation

You can easily install Brahm Centre Utils using pip:

```bash
pip install brahm-centre-utils
```

It's recommended to install this package in a virtual environment.

## Usage
After installing the package, you can use the functions provided by Brahm Centre Utils in your projects. Here are some examples:
### Quick Import
You can import commonly used functions directly from the package:
```python
from brahm_centre_utils import query_salesforce
```

### Salesforce Integration
**query_salesforce**
This function allows you to query Salesforce data using SOQL (Salesforce Object Query Language).
```python
from brahm_centre_utils import query_salesforce
from simple_salesforce import Salesforce
from dotenv import load_dotenv

# Establish connection with SF with credentials from .env file
sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token=os.getenv('SF_SECURITY_TOKEN'),
    domain=os.getenv('SF_DOMAIN')
)

# Use the function to query SF
result = query_salesforce("SELECT Id, Name FROM Account")
print(result)
```

### Full List of Functions
- brahm_centre_utils.query_salesforce
- brahm_centre_utils.salesforce.get_Id_from_SF_URL
- brahm_centre_utils.common.normalize_name
- brahm_centre_utils.common.are_names_similar
- brahm_centre_utils.common.get_unique_names

## Configuration
Brahm Centre Utils requires certain environment variables for Salesforce integration. These should be stored in a .env file in the root of your project.

### Exmple .env file
```plaintext
SF_USERNAME=your_salesforce_username
SF_PASSWORD=your_salesforce_password
SF_TOKEN=your_salesforce_security_token
SF_DOMAIN=your_salesforce_domain
```

## Upload a New Version
1. Update the version number in setup.py.
2. Rebuild the distribution files:
```bash
python setup.py sdist bdist_wheel
```
3. Upload to PyPI
```bash
twine upload dist/*
```


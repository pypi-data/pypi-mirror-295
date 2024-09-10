# Saldor

Saldor is a Python client library for interacting with the Saldor.com API. It
allows developers to easily integrate Saldor's services into their Python
applications.

## Installation

```
pip install saldor
```

Sign up for an account at console.saldor.com, get an API Key, and set that value as an environment variable SALDOR_API_URL.

Writing a basic app that uses the client:

```
import os

import saldor

client = saldor.SaldorClient()

result = client.crawl(
    url="URL",
    max_pages=3,
)
```




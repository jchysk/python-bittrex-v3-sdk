# python-bittrex-v3-sdk
Interact with the Bittrex v3 API


I wasn't able to find an existing Python SDK for Bittrex's v3 API so I put a barebones one together with a few of the resources implemented.
Implementing the remaining REST resources from this point should be pretty simple.

```
from client import Client
c = Client("apikeyhere", "apisecrethere")
c.ping()
c.get_account()
c.get_account_volume()
c.get_addresses()
params = {"startDate": "2019-06-01", "pageSize": 200}
c.get_closed_orders(**params)
```

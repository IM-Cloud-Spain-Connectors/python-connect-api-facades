# Python Connect API Facades

[![Test](https://github.com/othercodes/python-connect-api-facades/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-connect-api-facades/actions/workflows/test.yml)

Easy to use facades for the Connect Open API.

## Installation

The easiest way to install the Connect API Facades library is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-connect-api-facades
# using pip
pip install rndi-connect-api-facades
```

## The Contracts

This package provides the following contracts or interfaces:

* AssetManagementService

## The Adapters

The facade works as the adapter for the interfaces, it also adds new functionality to enhance the experience, to use it,
just instantiate the `ConnectOpenAPIFacade` injecting an API instance.

```python
from rndi.connect.api_facades.facade import ConnectOpenAPIFacade

api = ConnectOpenAPIFacade(client)
api.find_asset('AS-XXXX-XXXX-XXXX')
```

Optionally, you can import and use standalone mixing facades for each API endpoint:

```python
from rndi.connect.api_facades.assets.mixins import WithAssetFacade


class MyCustomClass(WithAssetFacade):
    def __init__(self, client):
        self.client = client


api = MyCustomClass(client)
api.find_asset('AS-XXXX-XXXX-XXXX')
```

# Lumos Connectors

[![PyPI - Version](https://img.shields.io/pypi/v/connector-py.svg)](https://pypi.org/project/connector-py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/connector-py.svg)](https://pypi.org/project/connector-py)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Error Handling](#error-handling)
- [Scaffold](#scaffold)
- [Unasync](#unasync)
- [FastAPI](#fastapi)
- [Tips](#tips)
- [License](#license)

## Installation

```console
pip install connector-py
```

## Usage

The package can be used in three ways:
1. A CLI to scaffold a custom connector with its own CLI to call commands
2. A library to create a custom connector
3. A library to convert your custom connector code to a FastAPI HTTP server

To get started, run `connector --help`

An example of running a command that accepts arguments
in an integration connector called `mock-connector`:

```shell
mock-connector info --json '{"a": 1}'
```

### Connector implementation
All new connectors should be based on the `connector.integration.Integration` class. The new approach doesn't define capabilities by inheriting from connector interface (called `LumosCommandMixin`) but injects capability implementations into an instance of `Integration` class. This allows us to:
- typecheck the implementations
- partially implemented connectors
- check that implementation accept expected arguments and return expected response
- have connector specific arguments

```python
import httpx
from connector.capability import CapabilityName
from connector.errors import HTTPHandler
from connector.integration import Integration
from connector.serializers.request import (
    BasicCredentials,
    ListAccountsRequest,
    Request,
)
from connector.serializers.response import (
    ListAccountsResponse,
    Response,
)

integration = Integration(
    app_id="app_id",
    auth=BasicCredentials,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    handle_errors=True,
)


@integration.register_capability(CapabilityName.LIST_ACCOUNTS)
async def list_accounts(request: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
    # do whatever is needed to get accounts
    return Response[ListAccountsResponse](
        response=ListAccountsResponse(
            accounts=accounts,
        ),
        raw_data=raw_data if request.include_raw_data else None,
        ...
    )
```

#### Converting LumosCommandMixin-based integrations
- if you don't need to sync, drop `sync_/` folder; otherwise drop `async_/`
- in your connector implementation, create instance of `Integration` class, fill-in `app_id`, `exception_handlers` and `auth`
- all methods that implement capabilities have to be decorated with `integration.register_capability(name=CapabilityName.<pick-correct-name>)`
- if you don't need any extra arguments for capability parameters (besides auth and pagination, which are now part of request), remove them and use the standard way provided with `connector.serializers.request.Request` class
- make all tests sync as the `dispatch` method is synchronous and it start the event loop itself
- you're done

### Error Handling

Error handling is facilitated through an exception handler decorator.
See `connector/async_/exception_handler.py` and `connector/errors.py`.

An exception handler can be attached to the connector library as follows:

```python
from httpx import HTTPStatusError
from connector.errors import HTTPHandler
from connector.async_exception_handler import connector_handler

integration = Integration(
    ...,
    exception_handlers=[
        (HTTPStatusError, HTTPHandler, None),
    ],
    handle_errors=True,
)
```

The decorator accepts a list of tuples of three. First tuple argument is the exception you would like to be catching, second is the handler (default or implemented on your own) and third is a specific error code that you would like to associate with this handler.

By default it is recommended to make use of the default HTTPHandler which will handle `raise_for_status()` for you and properly error code it. For more complex errors it is recommended to subclass the ExceptionHandler (in `connector/errors.py`) and craft your own handler.

#### Making your own handler

To setup your own handler, you can extend the abstract ExceptionHandler class:

```python
from connector.errors import ExceptionHandler, ErrorCodes
from connector.serializers.lumos import EncounteredErrorResponse
from connector.serializers.response import Response

class CustomHandler(ExceptionHandler):
    @staticmethod
    def handle(
        e: Exception,
        original_func: t.Any,
        response: Response[EncounteredErrorResponse],
        error_code: str | ErrorCodes | None = None,
    ) -> Response[EncounteredErrorResponse]:
        # Perform any custom logic, another call, modify the response, etc.
        response.error.error_code = "custom_error_code"
        return response
```

#### Raising an exception

Among this, there is a custom exception class available as well as a default list of error codes:

```python
from connector.errors import ConnectorError, ErrorCodes

def some_method(self, args):
    raise ConnectorError("Received wrong data, x: y", ErrorCodes.BAD_REQUEST)
```

It is preferred to raise any manually raisable exception with this class. A connector can implement its own error codes list, which should be properly documented.

### Response

Error codes are by default prefixed with the app_id of the connector that has raised the exception. In your implementation you don't need to worry about this and can only focus on the second and optionally third level of the error code.

An example response when handled this way:

```json
// BAD_REQUEST error from github connector
{"error":{"message":"Some message","status_code":400,"error_code":"github.bad_request","raised_by":"HTTPStatusError","raised_in":"github.sync_.lumos:validate_credentials"}, "response": null, "raw_data": null}
```

### Scaffold

To scaffold a custom connector, run `connector scaffold --help`

To scaffold the mock-connector, run
`connector scaffold mock-connector "projects/connectors/python/mock-connector"`

### Unasync

*Unasync will be removed when all connectors are migrated to `Integration` class approach.*

When developing this package, start off creating async functions and then
convert them to sync functions using `unasync`.

```console
connector hacking unasync
```

### FastAPI

To convert your custom connector to a FastAPI HTTP server, run `connector hacking http-server`

## Tips

#### The library I want to use is synchronous only

You can use a package called `asgiref`. This package converts I/O bound synchronous
calls into asyncio non-blocking calls. First, add asgiref to your dependencies list
in `pyproject.toml`. Then, in your async code, use `asgiref.sync_to_async` to convert
synchronous calls to asynchronous calls.

```python
from asgiref.sync import sync_to_async
import requests

async def async_get_data():
    response = await sync_to_async(requests.get)("url")
```

## License

`connector` is distributed under the terms of the [Apache 2.0](./LICENSE.txt) license.

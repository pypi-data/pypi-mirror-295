import contextlib
import typing as t
from unittest.mock import patch

import httpx
import pytest
from connector.generated import AuthCredential, AuthModel

from tests.type_definitions import ClientContextManager, MockedResponse, ResponseBodyMap
from {name}.auth import Auth
from {name}.integration import BASE_URL

INVALID_AUTH = AuthCredential.from_dict({{
    "m": AuthModel.OAUTH,
    "access_token": "ACCESS_TOKEN",  # noqa: S105
}})
VALID_AUTH = AuthCredential.from_dict({{
    "m": AuthModel.OAUTH,
    "access_token": "ACCESS_TOKEN",  # noqa: S105
}})


@pytest.fixture(name="httpx_async_client")
def fixture_httpx_async_client() -> ClientContextManager:
    @contextlib.contextmanager
    def factory(token: str, response_body_map: ResponseBodyMap) -> t.Iterator[None]:
        def handler(request: httpx.Request) -> httpx.Response:
            full_path = f"{{request.url.path}}?{{request.url.params!s}}".rstrip("?")  # fix f-string
            response_body = response_body_map[request.method][full_path]
            match response_body:
                case MockedResponse(status_code, None):
                    return httpx.Response(status_code)
                case MockedResponse(status_code, body):
                    return httpx.Response(status_code, json=body)

        with patch("{name}.integration.build_client") as mocked_build_client:
            mocked_build_client.return_value = httpx.AsyncClient(
                base_url=BASE_URL,
                auth=Auth(token),
                transport=httpx.MockTransport(handler),
            )
            yield

    return factory

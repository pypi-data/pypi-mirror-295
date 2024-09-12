"""Cases for testing ``list_accounts`` operation."""

import typing as t

import httpx
from connector.generated import (
    ListAccountsResponse,
    Error,
    ErrorCode,
    ErrorResponse,
    Page,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from {name}.serializers.request import (
    {pascal}ListAccounts,
    {pascal}ListAccountsRequest,
)
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}ListAccountsRequest,
    ResponseBodyMap,
    ListAccountsResponse | ErrorResponse,
]


def case_list_accounts_200() -> Case:
    """Successful request."""
    args = {pascal}ListAccountsRequest(
        request={pascal}ListAccounts(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
        raw_data=None,
        page=Page(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return args, response_body_map, expected_response


def case_list_accounts_200_no_accounts() -> Case:
    """No accounts found."""
    args = {pascal}ListAccountsRequest(
        request={pascal}ListAccounts(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
        raw_data=None,
        page=Page(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return args, response_body_map, expected_response


def case_list_accounts_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}ListAccountsRequest(
        request={pascal}ListAccounts(),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/users?limit=5&offset=0",
                httpx.codes.UNAUTHORIZED,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_accounts",
        ),
    )
    return args, response_body_map, expected_response

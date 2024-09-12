"""Cases for testing ``delete_account`` operation."""

import typing as t

import httpx
from connector.generated import (
    DeleteAccountResponse,
    DeletedAccount,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from {name}.serializers.request import (
    {pascal}DeleteAccount,
    {pascal}DeleteAccountRequest,
)
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}DeleteAccountRequest,
    ResponseBodyMap,
    DeleteAccountResponse | ErrorResponse,
]


def case_delete_account_204() -> Case:
    """Successful deletion request."""
    args = {pascal}DeleteAccountRequest(
        request={pascal}DeleteAccount(
            account_id="1",
        ),
        auth=VALID_AUTH,
        include_raw_data=True,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NO_CONTENT,
                response_body=None,
            ),
        }},
    }}
    expected_response = DeleteAccountResponse(
        response=DeletedAccount(deleted=True),
        raw_data={{
            f"{{BASE_URL}}/users/{{args.request.account_id}}": None,
        }},
    )
    return args, response_body_map, expected_response


def case_delete_account_404() -> Case:
    """Not found request should fail."""
    args = {pascal}DeleteAccountRequest(
        request={pascal}DeleteAccount(
            account_id="non_existent",
        ),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{
                    "error": {{
                        "message": "Not found",
                        "code": 2100,
                    }},
                }},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/users/{{args.request.account_id}}",
                httpx.codes.NOT_FOUND,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:delete_account",
        ),
    )
    return args, response_body_map, expected_response


def case_delete_account_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}DeleteAccountRequest(
        request={pascal}DeleteAccount(
            account_id="1",
        ),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "DELETE": {{
            f"/users/{{args.request.account_id}}": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body=None,
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/users/{{args.request.account_id}}",
                httpx.codes.UNAUTHORIZED,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:delete_account",
        ),
    )
    return args, response_body_map, expected_response

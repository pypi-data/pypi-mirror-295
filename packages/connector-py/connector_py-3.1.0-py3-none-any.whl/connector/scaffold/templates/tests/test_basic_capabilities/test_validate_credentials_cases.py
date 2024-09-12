"""Cases for testing ``validate_credentials`` operation."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from {name}.serializers.request import (
    {pascal}ValidateCredentials,
    {pascal}ValidateCredentialsRequest,
)
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}ValidateCredentialsRequest,
    ResponseBodyMap,
    ValidateCredentialsResponse | ErrorResponse,
]


def case_validate_credentials_200() -> Case:
    """Successful request."""
    args = {pascal}ValidateCredentialsRequest(
        request={pascal}ValidateCredentials(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=1": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            )
        }}
    }}
    expected_response = ValidateCredentialsResponse(
        response=ValidatedCredentials(valid=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response


def case_validate_credentials_401() -> Case:
    """Unauthorized request should fail."""

    args = {pascal}ValidateCredentialsRequest(
        request={pascal}ValidateCredentials(),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=1": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            )
        }}
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/users?limit=1",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in=f"{name}.integration:validate_credentials",
        )
    )
    return args, response_body_map, expected_response

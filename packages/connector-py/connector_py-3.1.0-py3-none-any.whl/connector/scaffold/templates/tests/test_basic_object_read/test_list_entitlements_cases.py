"""Cases for testing ``list_entitlements`` operation."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListEntitlementsResponse,
    Page,
)
from connector.utils.test import http_error_message

from {name}.serializers.request import (
    {pascal}ListEntitlements,
    {pascal}ListEntitlementsRequest,
)
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}ListEntitlementsRequest,
    ResponseBodyMap,
    ListEntitlementsResponse | ErrorResponse,
]


def case_list_entitlements_200() -> Case:
    """Successful request."""
    args = {pascal}ListEntitlementsRequest(
        request={pascal}ListEntitlements(),
        auth=VALID_AUTH,
        page=Page(
            size=5,
        ),
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListEntitlementsResponse(
        response=[],
        raw_data={{}},
    )
    return args, response_body_map, expected_response


INVALID_ARGS = {pascal}ListEntitlementsRequest(
    request={pascal}ListEntitlements(),
    auth=INVALID_AUTH,
    page=Page(
        size=5,
    ),
)


def case_list_entitlements_401() -> Case:
    """Unauthorized request should fail."""
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.UNAUTHORIZED,
                response_body={{}},
            ),
        }},
    }}

    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_entitlements",
        ),
        raw_data=None,
    )

    return INVALID_ARGS, response_body_map, expected_response


def case_list_entitlements_400() -> Case:
    """Bad request should fail."""

    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}

    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                400,
            ),
            status_code=httpx.codes.BAD_REQUEST,
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:list_entitlements",
        ),
        raw_data=None,
    )

    return INVALID_ARGS, response_body_map, expected_response

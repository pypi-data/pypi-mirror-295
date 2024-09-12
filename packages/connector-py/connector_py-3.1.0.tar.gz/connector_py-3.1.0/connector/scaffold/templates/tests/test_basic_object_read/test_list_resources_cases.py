"""Cases for testing ``list_resources`` operation."""

import typing as t

import httpx
from {name}.serializers.request import (
    {pascal}ListResources,
    {pascal}ListResourcesRequest,
)
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListResourcesResponse,
)
from connector.utils.test import http_error_message

from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}ListResourcesRequest,
    ResponseBodyMap,
    ListResourcesResponse | ErrorResponse,
]


def case_list_resources_200() -> Case:
    """Successful request."""
    args = {pascal}ListResourcesRequest(
        request={pascal}ListResources(),
        auth=VALID_AUTH,
    )

    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListResourcesResponse(
        response=[],
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_list_resources_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}ListResourcesRequest(
        request={pascal}ListResources(),
        auth=INVALID_AUTH,
    )

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
            raised_in=f"{name}.integration:list_resources",
        )
    )

    return args, response_body_map, expected_response

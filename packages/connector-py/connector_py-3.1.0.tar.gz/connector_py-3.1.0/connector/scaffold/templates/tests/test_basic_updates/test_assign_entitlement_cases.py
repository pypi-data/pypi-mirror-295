"""Cases for testing ``assign_entitlement`` operation."""
import typing as t

import httpx
from {name}.serializers.request import (
    {pascal}AssignEntitlement,
    {pascal}AssignEntitlementRequest,
)
from connector.generated import (
    AssignedEntitlement,
    AssignEntitlementResponse,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message

from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}AssignEntitlementRequest,
    ResponseBodyMap,
    AssignEntitlementResponse | ErrorResponse,
]

VALID_ASSIGN_REQUEST = {pascal}AssignEntitlementRequest(
    request={pascal}AssignEntitlement(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=VALID_AUTH,
)
INVALID_ASSIGN_REQUEST = {pascal}AssignEntitlementRequest(
    request={pascal}AssignEntitlement(
        account_integration_specific_id="",
        resource_integration_specific_id="",
        resource_type="",
        entitlement_integration_specific_id="",
        entitlement_type="",
    ),
    auth=INVALID_AUTH,
)

# repeat following cases for all entitlements
def case_assign_entitlement_1_401() -> Case:
    """Unauthorized request should fail."""
    args = INVALID_ASSIGN_REQUEST
    response_body_map ={{
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
            raised_in="{name}.integration:assign_entitlement",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                "",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_400() -> Case:
    """Authorized bad request should fail."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
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
            raised_in="{name}.integration:unassign_entitlement",
        ),
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_200() -> Case:
    """Succeed with changing entitlement."""
    args = VALID_ASSIGN_REQUEST
    response_body_map ={{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = AssignEntitlementResponse(
        response=AssignedEntitlement(assigned=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response

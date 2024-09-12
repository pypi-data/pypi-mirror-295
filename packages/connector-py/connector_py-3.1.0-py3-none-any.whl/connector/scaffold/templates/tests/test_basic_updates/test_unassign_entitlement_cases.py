"""Cases for testing ``unassign_entitlement`` operation."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    UnassignEntitlementResponse,
    UnassignedEntitlement,
)
from connector.utils.test import http_error_message
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import ResponseBodyMap, MockedResponse

from {name}.serializers.request import (
    {pascal}UnassignEntitlement,
    {pascal}UnassignEntitlementRequest,
)

Case: t.TypeAlias = tuple[
    {pascal}UnassignEntitlementRequest,
    ResponseBodyMap,
    UnassignEntitlementResponse | ErrorResponse,
]

# repeat following casess for all entitlements

def case_unassign_entitlement_1_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}UnassignEntitlementRequest(
        request={pascal}UnassignEntitlement(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
        ),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/example": MockedResponse(
                status_code=httpx.codes.OK,
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
            raised_in="{name}.integration:unassign_entitlement",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_assign_entitlement_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = {pascal}UnassignEntitlementRequest(
        request={pascal}UnassignEntitlement(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
        ),
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
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_unassign_entitlement_1_200() -> Case:
    """Successfully unassign entitlement."""
    args = {pascal}UnassignEntitlementRequest(
        request={pascal}UnassignEntitlement(
            account_integration_specific_id="",
            resource_integration_specific_id="",
            resource_type="",
            entitlement_integration_specific_id="",
            entitlement_type="",
        ),
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
    expected_response = UnassignEntitlementResponse(
        response=UnassignedEntitlement(unassigned=True),
        raw_data=None,
    )
    return args, response_body_map, expected_response

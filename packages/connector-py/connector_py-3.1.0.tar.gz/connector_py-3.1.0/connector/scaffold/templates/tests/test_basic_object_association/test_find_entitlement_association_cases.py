"""Cases for testing ``test_find_entitlement_associations`` operation."""
import typing as t

import httpx
from {name}.serializers.request import (
    {pascal}FindEntitlementAssociations,
    {pascal}FindEntitlementAssociationsRequest,
)
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    FindEntitlementAssociationsResponse,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}FindEntitlementAssociationsRequest,
    ResponseBodyMap,
    FindEntitlementAssociationsResponse | ErrorResponse,
]

# repeat following cases for all resource types
def case_find_entitlement_associations_1_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}FindEntitlementAssociationsRequest(
        request={pascal}FindEntitlementAssociations(
        ),
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
                f"{{BASE_URL}}/",
                401,
            ),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:find_entitlement_associations",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_404() -> Case:
    """Authorized request for non-existing entitlement should fail."""
    args = {pascal}FindEntitlementAssociationsRequest(
        request={pascal}FindEntitlementAssociations(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.NOT_FOUND,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message(
                f"{{BASE_URL}}/",
                404,
            ),
            status_code=httpx.codes.NOT_FOUND,
            error_code=ErrorCode.NOT_FOUND,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:find_entitlement_associations",
        ),
        raw_data={{}},
    )
    return args, response_body_map, expected_response



def case_find_entitlement_associations_1_200() -> Case:
    """Succeed with finding entitlement associations."""
    args = {pascal}FindEntitlementAssociationsRequest(
        request={pascal}FindEntitlementAssociations(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
        raw_data={{}},
    )
    return args, response_body_map, expected_response


def case_find_entitlement_associations_1_empty_200() -> Case:
    """Succeed with getting empty entitlement associations."""
    args = {pascal}FindEntitlementAssociationsRequest(
        request={pascal}FindEntitlementAssociations(),
        auth=VALID_AUTH,
    )
    response_body_map = {{
        "GET": {{
            "/": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = FindEntitlementAssociationsResponse(
        response=[],
        raw_data={{}},
    )
    return args, response_body_map, expected_response

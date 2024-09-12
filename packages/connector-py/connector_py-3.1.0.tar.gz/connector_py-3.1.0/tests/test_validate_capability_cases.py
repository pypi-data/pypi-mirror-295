"""Test cases for ``validate_capability`` function."""

import typing as t

import pytest_cases
from connector.capability import CapabilityName
from connector.serializers.request import (
    ListAccountsRequest,
    ListResourcesRequest,
    Request,
    RequestData,
)
from connector.serializers.response import (
    ListAccountsResponse,
    Response,
    ResponseData,
)

Case: t.TypeAlias = tuple[
    CapabilityName,
    t.Callable[[Request[RequestData]], Response[ResponseData]],
]


class CustomListAccountsRequest(ListAccountsRequest):
    """Correct custom request for list-accounts capability."""

    extra: str


class CustomListAccountsRequestFromBadBase(ListResourcesRequest):
    """Incorrect base is used for custom request schema."""

    extra: str


class CustomListAccountsResponse(ListAccountsResponse):
    """Subclassing response type is always bad."""

    extra_resp: str


@pytest_cases.case(tags=("valid",))
def case_valid_capability_base_annotation() -> Case:
    def capability(request: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(accounts=[]),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability


@pytest_cases.case(tags=("valid",))
def case_valid_capability_custom_request() -> Case:
    """Using subclass of matching request type is valid.

    Using subclass of ListAccountsRequest for list-accounts capability
    is absolutely fine.
    """

    def capability(request: Request[CustomListAccountsRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(accounts=[]),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_custom_response() -> Case:
    """Using subclass of SDK defined response is not correct.

    This would change the output of the method, making it super hard to
    use.
    """

    def capability(request: Request[ListAccountsRequest]) -> Response[CustomListAccountsResponse]:
        return Response[CustomListAccountsResponse](
            response=CustomListAccountsResponse(accounts=[], extra_resp="bad"),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_model() -> Case:
    """Using mismatching request type for capability is invalid.

    Using ListResourcesRequest for list-accounts method is obviously
    invalid.
    """

    def capability(request: Request[ListResourcesRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(accounts=[]),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base_model() -> Case:
    """Using mismatching base for request type is invalid.

    Using subslass of ListResourcesRequest for list-accounts method is
    obviously invalid.
    """

    def capability(
        request: Request[CustomListAccountsRequestFromBadBase],
    ) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(accounts=[]),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability


@pytest_cases.case(tags=("invalid",))
def case_invalid_capability_bad_request_base() -> Case:
    """Using class unrelated to request type is invalid.

    Using classes unrelated to ``RequestData`` is obviously invalid.
    """

    def capability(request: Request[int]) -> Response[ListAccountsResponse]:  # type: ignore[type-var]
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(accounts=[]),
            raw_data=None,
        )

    capability_name = CapabilityName.LIST_ACCOUNTS
    return capability_name, capability

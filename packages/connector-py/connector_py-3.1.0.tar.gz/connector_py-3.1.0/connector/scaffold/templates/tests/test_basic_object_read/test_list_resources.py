import pytest
import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth
from {name}.serializers.request import (
    {pascal}ListResourcesRequest,
)
from connector.generated import (
    ListResourcesResponse,
)
from {name}.integration import integration

from tests.type_definitions import ClientContextManager, ResponseBodyMap

@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_object_read.test_list_resources_cases",
    ],
)
def test_validate_list_resources(
    httpx_async_client: ClientContextManager,
    args: {pascal}ListResourcesRequest,
    response_body_map: ResponseBodyMap,
    expected_response: ListResourcesResponse,
) -> None:
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.LIST_RESOURCES, args.model_dump_json())

    assert response == expected_response.model_dump_json()

import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth
from {name}.serializers.request import (
    {pascal}ValidateCredentialsRequest,
)
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ValidateCredentialsResponse,
)
from {name}.integration import integration

from tests.type_definitions import ClientContextManager, ResponseBodyMap


@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_capabilities.test_validate_credentials_cases",
    ],
)
def test_validate_credentials(
    httpx_async_client: ClientContextManager,
    args: {pascal}ValidateCredentialsRequest,
    response_body_map: ResponseBodyMap,
    expected_response: ValidateCredentialsResponse | ErrorResponse,
) -> None:
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.VALIDATE_CREDENTIALS, args.model_dump_json())

    assert response == expected_response.model_dump_json()

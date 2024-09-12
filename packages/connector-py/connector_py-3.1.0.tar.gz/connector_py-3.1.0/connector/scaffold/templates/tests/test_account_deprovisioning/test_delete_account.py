import pytest
import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth
from connector.generated import (
    DeleteAccountResponse,
    Error,
    ErrorCode,
    ErrorResponse,
)
from {name}.integration import integration
from {name}.serializers.request import (
    {pascal}DeleteAccountRequest,
)

from tests.conftest import ClientContextManager, ResponseBodyMap


@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=["tests.test_account_deprovisioning.test_delete_account_cases"],
)
def test_delete_account(
    httpx_async_client: ClientContextManager,
    args: {pascal}DeleteAccountRequest,
    response_body_map: ResponseBodyMap,
    expected_response: DeleteAccountResponse | ErrorResponse,
) -> None:
    """Test ``delete_account`` operation."""
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.DELETE_ACCOUNT, args.model_dump_json())

    assert response == expected_response.model_dump_json()

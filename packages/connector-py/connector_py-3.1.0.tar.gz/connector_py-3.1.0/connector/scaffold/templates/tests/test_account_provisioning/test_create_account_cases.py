"""Cases for testing ``create_account`` operation."""

import typing as t

import httpx
from connector.generated import (
    CreateAccountEntitlement,
    CreateAccount,
    CreateAccountResponse,
    CreatedAccount,
    Error,
    ErrorCode,
    ErrorResponse,
)
from connector.utils.test import http_error_message

from {name}.integration import BASE_URL
from {name}.serializers.request import (
    {pascal}CreateAccount,
    {pascal}CreateAccountRequest,
)
from tests.conftest import INVALID_AUTH, VALID_AUTH
from tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    {pascal}CreateAccountRequest,
    ResponseBodyMap,
    CreateAccountResponse | ErrorResponse,
]


def case_create_account_201() -> Case:
    """Successful creation request."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="read_only_user",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="role",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="license",
                ),
            ],
        ),
        auth=VALID_AUTH,
        include_raw_data=True,
    )
    user_id = "1"
    response_body = {{
        "user": {{
            "id": user_id,
            "email": args.request.email,
            "name": f"{{args.request.given_name}} {{args.request.family_name}}",
            "html_url": f"https://dev-lumos.{name}.com/users/{{user_id}}",
            "role": args.request.entitlements[0].integration_specific_id,
            "license": {{"id": args.request.entitlements[1].integration_specific_id}},
        }},
    }}
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.CREATED,
                response_body=response_body,
            ),
         }},
     }}
    expected_response = CreateAccountResponse(
        response=CreatedAccount(created=True),
        raw_data={{
            f"{{BASE_URL}}/": response_body,
        }},
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_email() -> Case:
    """Invalid request when creating an account without user email."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            entitlements=[],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Email is required, provide 'email' in account data",
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
        raw_data=None,
    )
    return args, response_body_map, expected_response


def case_create_account_400_missing_name() -> Case:
    """Invalid request when creating an account without user given and family names."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            email="jw7rT@example.com",
            entitlements=[],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Name is required, provide both 'given_name' and 'family_name' in account data",
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_too_many_entitlements() -> Case:
    """Invalid request when creating an account with too many provided entitlements."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="license-1",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="Too many entitlements provided",
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_400_invalid_entitlements() -> Case:
    """Invalid request when creating an account with too many provided entitlements."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
                CreateAccountEntitlement(
                    integration_specific_id="",
                    integration_specific_resource_id="dev-lumos",
                    entitlement_type="",
                ),
            ],
        ),
        auth=VALID_AUTH,
    )
    response_body_map ={{
        "POST": {{
            "/users": MockedResponse(
                status_code=httpx.codes.BAD_REQUEST,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message="The same entitlement type provided",
            error_code=ErrorCode.BAD_REQUEST,
            raised_by="ConnectorError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response


def case_create_account_401() -> Case:
    """Unauthorized request should fail."""
    args = {pascal}CreateAccountRequest(
        request={pascal}CreateAccount(
            email="jw7rT@example.com",
            given_name="John",
            family_name="Doe",
            entitlements=[],
        ),
        auth=INVALID_AUTH,
    )
    response_body_map = {{
        "POST": {{
            "/users": MockedResponse(status_code=httpx.codes.UNAUTHORIZED, response_body=None),
        }},
    }}
    expected_response = ErrorResponse(
        is_error=True,
        error=Error(
            message=http_error_message("https://api.{name}.com/users", httpx.codes.UNAUTHORIZED),
            status_code=httpx.codes.UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            raised_by="HTTPStatusError",
            raised_in="{name}.integration:create_account",
        ),
    )
    return args, response_body_map, expected_response

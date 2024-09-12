"""Test cases for ``Integration.info`` function."""

import json
import typing as t

from connector.capability import CapabilityName
from connector.integration import Integration
from connector.serializers.abstract import CommandTypes, Info
from connector.serializers.request import BasicCredentials, ListAccountsRequest, Request
from connector.serializers.response import ListAccountsResponse, Response

Case: t.TypeAlias = tuple[
    Integration,
    Info,
]


def case_info() -> Case:
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=True,
    )

    @integration.register_capability(CapabilityName.LIST_ACCOUNTS)
    async def capability(request: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(
                accounts=[],
            ),
            raw_data=None,
        )

    expected_info = Info(
        app_id=app_id,
        capabilities=[CapabilityName.LIST_ACCOUNTS.value],
        authentication_schema={
            "properties": {
                "model": {
                    "const": "basic",
                    "default": "basic",
                    "enum": ["basic"],
                    "title": "Model",
                    "type": "string",
                },
                "username": {
                    "description": "Username",
                    "title": "Username",
                    "type": "string",
                },
                "password": {
                    "description": "Password",
                    "title": "Password",
                    "type": "string",
                },
            },
            "required": ["username", "password"],
            "title": "BasicCredentials",
            "type": "object",
        },
        capability_schema={
            CapabilityName.LIST_ACCOUNTS.value: CommandTypes(
                argument=json.dumps(
                    {
                        "$defs": {
                            "BasicCredentials": {
                                "properties": {
                                    "model": {
                                        "const": "basic",
                                        "default": "basic",
                                        "enum": ["basic"],
                                        "title": "Model",
                                        "type": "string",
                                    },
                                    "username": {
                                        "description": "Username",
                                        "title": "Username",
                                        "type": "string",
                                    },
                                    "password": {
                                        "description": "Password",
                                        "title": "Password",
                                        "type": "string",
                                    },
                                },
                                "required": ["username", "password"],
                                "title": "BasicCredentials",
                                "type": "object",
                            },
                            "ListAccountsRequest": {
                                "properties": {
                                    "custom_attributes": {
                                        "anyOf": [
                                            {"items": {"type": "string"}, "type": "array"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Custom Attributes",
                                    },
                                },
                                "title": "ListAccountsRequest",
                                "type": "object",
                            },
                            "OAuthCredentials": {
                                "properties": {
                                    "model": {
                                        "const": "oauth",
                                        "default": "oauth",
                                        "enum": ["oauth"],
                                        "title": "Model",
                                        "type": "string",
                                    },
                                    "access_token": {
                                        "description": "OAuth access token",
                                        "title": "Access Token",
                                        "type": "string",
                                    },
                                    "refresh_token": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "OAuth refresh token",
                                        "title": "Refresh Token",
                                    },
                                    "scope": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "description": "OAuth scopes",
                                        "title": "Scope",
                                    },
                                },
                                "required": ["access_token"],
                                "title": "OAuthCredentials",
                                "type": "object",
                            },
                            "PaginationArgs": {
                                "properties": {
                                    "token": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Token",
                                    },
                                    "size": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Size",
                                    },
                                },
                                "title": "PaginationArgs",
                                "type": "object",
                            },
                        },
                        "properties": {
                            "request": {"$ref": "#/$defs/ListAccountsRequest"},
                            "auth": {
                                "discriminator": {
                                    "mapping": {
                                        "basic": "#/$defs/BasicCredentials",
                                        "oauth": "#/$defs/OAuthCredentials",
                                    },
                                    "propertyName": "model",
                                },
                                "oneOf": [
                                    {"$ref": "#/$defs/OAuthCredentials"},
                                    {"$ref": "#/$defs/BasicCredentials"},
                                ],
                                "title": "Auth",
                            },
                            "page": {
                                "anyOf": [
                                    {"$ref": "#/$defs/PaginationArgs"},
                                    {"type": "null"},
                                ],
                                "default": None,
                            },
                            "include_raw_data": {
                                "default": False,
                                "title": "Include Raw Data",
                                "type": "boolean",
                            },
                            "request_id": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "title": "Request Id",
                            },
                        },
                        "required": ["request", "auth"],
                        "title": "Request[ListAccountsRequest]",
                        "type": "object",
                    }
                ),
                output=json.dumps(
                    {
                        "$defs": {
                            "EncounteredErrorResponse": {
                                "properties": {
                                    "message": {
                                        "title": "Message",
                                        "type": "string",
                                    },
                                    "status_code": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Status Code",
                                    },
                                    "error_code": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Error Code",
                                    },
                                    "raised_by": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Raised By",
                                    },
                                    "raised_in": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Raised In",
                                    },
                                },
                                "required": ["message"],
                                "title": "EncounteredErrorResponse",
                                "type": "object",
                            },
                            "FoundAccountData": {
                                "properties": {
                                    "integration_specific_id": {
                                        "title": "Integration Specific Id",
                                        "type": "string",
                                    },
                                    "email": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Email",
                                    },
                                    "given_name": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Given Name",
                                    },
                                    "family_name": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Family Name",
                                    },
                                    "username": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Username",
                                    },
                                    "user_status": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "User Status",
                                    },
                                    "extra_data": {
                                        "anyOf": [
                                            {"type": "object"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Extra Data",
                                    },
                                    "custom_attributes": {
                                        "anyOf": [
                                            {
                                                "additionalProperties": {"type": "string"},
                                                "type": "object",
                                            },
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Custom Attributes",
                                    },
                                },
                                "required": ["integration_specific_id"],
                                "title": "FoundAccountData",
                                "type": "object",
                            },
                            "ListAccountsResponse": {
                                "properties": {
                                    "accounts": {
                                        "items": {"$ref": "#/$defs/FoundAccountData"},
                                        "title": "Accounts",
                                        "type": "array",
                                    },
                                },
                                "required": ["accounts"],
                                "title": "ListAccountsResponse",
                                "type": "object",
                            },
                            "PaginationData": {
                                "additionalProperties": False,
                                "properties": {
                                    "token": {
                                        "title": "Token",
                                        "type": "string",
                                    },
                                    "size": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "default": None,
                                        "title": "Size",
                                    },
                                },
                                "required": ["token"],
                                "title": "PaginationData",
                                "type": "object",
                            },
                        },
                        "properties": {
                            "response": {"$ref": "#/$defs/ListAccountsResponse"},
                            "raw_data": {
                                "anyOf": [
                                    {"type": "object"},
                                    {"type": "null"},
                                ],
                                "default": None,
                                "title": "Raw Data",
                            },
                            "page": {
                                "anyOf": [
                                    {"$ref": "#/$defs/PaginationData"},
                                    {"type": "null"},
                                ],
                                "default": None,
                            },
                            "error": {
                                "anyOf": [
                                    {"$ref": "#/$defs/EncounteredErrorResponse"},
                                    {"type": "null"},
                                ],
                                "default": None,
                            },
                        },
                        "required": ["response"],
                        "title": "Response[ListAccountsResponse]",
                        "type": "object",
                    }
                ),
            ),
        },
    )
    return integration, expected_info

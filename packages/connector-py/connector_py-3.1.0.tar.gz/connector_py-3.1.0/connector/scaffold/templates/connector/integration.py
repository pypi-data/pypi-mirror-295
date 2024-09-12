from typing import TypeAlias

import httpx
from connector.oai.capability import CapabilityName, get_oauth, get_page
from connector.oai.errors import HTTPHandler
from connector.oai.integration import Integration
from connector.generated import (
    ActivateAccountResponse,
    ActivatedAccount,
    AssignEntitlementResponse,
    AssignedEntitlement,
    CreateAccountResponse,
    CreatedAccount,
    DeactivateAccountResponse,
    DeactivatedAccount,
    DeleteAccountResponse,
    DeletedAccount,
    FindEntitlementAssociationsResponse,
    FoundAccountData,
    FoundEntitlementAssociation,
    GetLastActivityResponse,
    LastActivityData,
    ListAccountsResponse,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsResponse,
    ListResourcesResponse,
    OAuthCredential,
    Page,
    UnassignEntitlementResponse,
    UnassignedEntitlement,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from {name}.auth import Auth
from {name}.serializers.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination
from {name}.serializers.request import (
    {pascal}ActivateAccount,
    {pascal}ActivateAccountRequest,
    {pascal}AssignEntitlement,
    {pascal}AssignEntitlementRequest,
    {pascal}CreateAccount,
    {pascal}CreateAccountRequest,
    {pascal}DeactivateAccount,
    {pascal}DeactivateAccountRequest,
    {pascal}DeleteAccount,
    {pascal}DeleteAccountRequest,
    {pascal}FindEntitlementAssociations,
    {pascal}FindEntitlementAssociationsRequest,
    {pascal}GetLastActivity,
    {pascal}GetLastActivityRequest,
    {pascal}ListAccounts,
    {pascal}ListAccountsRequest,
    {pascal}ListCustomAttributesSchema,
    {pascal}ListCustomAttributesSchemaRequest,
    {pascal}ListEntitlements,
    {pascal}ListEntitlementsRequest,
    {pascal}ListResources,
    {pascal}ListResourcesRequest,
    {pascal}UnassignEntitlement,
    {pascal}UnassignEntitlementRequest,
    {pascal}ValidateCredentials,
    {pascal}ValidateCredentialsRequest,
)

BASE_URL = "https://scaffold.com"

RequestData: TypeAlias = (
    {pascal}ActivateAccountRequest |
    {pascal}AssignEntitlementRequest |
    {pascal}CreateAccountRequest |
    {pascal}DeactivateAccountRequest |
    {pascal}DeleteAccountRequest |
    {pascal}FindEntitlementAssociationsRequest |
    {pascal}GetLastActivityRequest |
    {pascal}ListAccountsRequest |
    {pascal}ListCustomAttributesSchemaRequest |
    {pascal}ListEntitlementsRequest |
    {pascal}ListResourcesRequest |
    {pascal}UnassignEntitlementRequest |
    {pascal}ValidateCredentialsRequest
)

def build_client(request: RequestData) -> httpx.AsyncClient:
    """Prepare client context manager for calling {title} API."""
    return httpx.AsyncClient(
        auth=Auth(access_token=get_oauth(request).access_token),
        base_url=BASE_URL,
    )


integration = Integration(
    app_id="{hyphenated_name}",
    auth=OAuthCredential,
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
)

@integration.register_capability(CapabilityName.VALIDATE_CREDENTIALS)
async def validate_credentials(
    args: {pascal}ValidateCredentialsRequest,
) -> ValidateCredentialsResponse:
    async with build_client(args) as client:
        r = await client.get("/users", params={{"limit": 1}})
        r.raise_for_status()
        data = r.json()

    return ValidateCredentialsResponse(
        response=ValidatedCredentials(valid=True),
        raw_data={{
            f"{{BASE_URL}}/users?limit=1": data,
        }}
        if args.include_raw_data
        else None,
    )

@integration.register_capability(CapabilityName.LIST_ACCOUNTS)
async def list_accounts(args: {pascal}ListAccountsRequest) -> ListAccountsResponse:
    endpoint = "/users"
    try:
        current_pagination = NextPageToken(get_page(args).token).paginations()[0]
    except IndexError:
        current_pagination = Pagination.default(endpoint)

    page_size = get_page(args).size or DEFAULT_PAGE_SIZE
    async with build_client(args) as client:
        r = await client.get(
            endpoint,
            params={{"limit": page_size, "offset": current_pagination.offset}},
        )
        r.raise_for_status()
        data = r.json()
        accounts: list[FoundAccountData] = []

        if True:
            next_pagination = [
                Pagination(
                    endpoint=endpoint,
                    offset=current_pagination.offset + len(accounts),
                )
            ]
        else:
            next_pagination = []

        next_page_token = NextPageToken.from_paginations(next_pagination).token

    return ListAccountsResponse(
        response=accounts,
        raw_data = {{
            f"{{BASE_URL}}/users?limit=1": data,
        }} if args.include_raw_data else None,
        page=Page(
            token=next_page_token,
            size=page_size,
        )
        if next_page_token
        else None,
    )

# @integration.register_capability(CapabilityName.LIST_RESOURCES)
async def list_resources(args: {pascal}ListResourcesRequest) -> ListResourcesResponse:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.LIST_ENTITLEMENTS)
async def list_entitlements(
    args: {pascal}ListEntitlementsRequest,
) -> ListEntitlementsResponse:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS)
async def find_entitlement_associations(
    args: {pascal}FindEntitlementAssociationsRequest,
) -> FindEntitlementAssociationsResponse:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.ASSIGN_ENTITLEMENT)
async def assign_entitlement(args: {pascal}AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.UNASSIGN_ENTITLEMENT)
async def unassign_entitlement(args: {pascal}UnassignEntitlementRequest) -> UnassignEntitlementResponse:
    raise NotImplementedError

# @integration.register_capability(CapabilityName.LIST_CUSTOM_ATTRIBUTES_SCHEMA)
async def list_custom_attributes_schema(args: {pascal}ListCustomAttributesSchemaRequest) -> ListCustomAttributesSchemaResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.CREATE_ACCOUNT)
async def create_account(
    args: {pascal}CreateAccountRequest,
) -> CreateAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DELETE_ACCOUNT)
async def delete_account(
    args: {pascal}DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.ACTIVATE_ACCOUNT)
async def activate_account(
    args: {pascal}ActivateAccountRequest,
) -> ActivateAccountResponse:
    raise NotImplementedError


# @integration.register_capability(CapabilityName.DEACTIVATE_ACCOUNT)
async def deactivate_account(
    args: {pascal}DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    raise NotImplementedError

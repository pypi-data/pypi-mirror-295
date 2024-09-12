"""Utility class to manage connector implementation.

:py:class:`Integration` provides a single point to register Integration
capabilities.

By instantiating the :py:class:`Integration` you simply create a basic
integration without any real implementation. To actually implement any
capability, you have to define (async) function outside the class and
register them to the integration instance by decorating the
implementation with ``@integration.register_capability(name)``.

Capability function has to:
    * accept only one argument
    * return scalar response

The :py:class:`Integration` is as much type-hinted as possible and also
does several checks to ensure that the implementation "is correct".
Incorrect implementation should raise an error during application start
(fail fast).

What is checked (at application start):
    * capability name is known (defined in ``CapabilityName`` enum)
    * the typesu of accepted argument and returned value matches the
    capability interface
"""

import asyncio
import inspect
import json
import typing as t
from dataclasses import dataclass

from connector.async_.exception_handler import exception_handler as async_exception_handler
from connector.capability import (
    CapabilityName,
    generate_capability_schema,
    get_capability_annotations,
    validate_capability,
)
from connector.errors import ErrorCodes, ErrorMap
from connector.serializers.abstract import AppCategory, Info
from connector.serializers.request import (
    BasicCredentials,
    OAuthCredentials,
    Request,
    RequestData,
)
from connector.serializers.response import EncounteredErrorResponse, Response, ResponseData
from connector.sync_.exception_handler import exception_handler as sync_exception_handler

CapabilityCallable: t.TypeAlias = (
    t.Callable[[Request[RequestData]], Response[ResponseData]]
    | t.Callable[[Request[RequestData]], t.Awaitable[Response[ResponseData]]]
)
IntegrationCapability = (
    t.Callable[[Request[t.Any]], Response[t.Any]]
    | t.Callable[[Request[t.Any]], t.Awaitable[Response[t.Any]]]
)
AuthSetting: t.TypeAlias = t.Union[
    t.Type[OAuthCredentials],
    t.Type[BasicCredentials],
    None,  # TODO: Remove once all connectors are migrated to new capability registration
]


@dataclass
class DescriptionData:
    logo_url: str | None = None
    user_friendly_name: str | None = None
    description: str | None = None
    categories: list[AppCategory] | None = None


class Integration:
    app_id: str

    def __init__(
        self,
        app_id: str,
        exception_handlers: ErrorMap,
        auth: AuthSetting,
        handle_errors: bool = True,
        description_data: DescriptionData | None = None,
    ):
        self.app_id = app_id.strip()
        self.description_data = description_data or DescriptionData()
        self.auth = auth
        self.exception_handlers = exception_handlers
        self.handle_errors = handle_errors

        if len(self.app_id) == 0:
            raise ValueError("'app_id' must not be empty")

        self.capabilities: dict[CapabilityName, IntegrationCapability] = {}

    def register_capability(
        self,
        name: CapabilityName,
    ) -> t.Callable[[CapabilityCallable], CapabilityCallable]:
        """Add implementation of specified capability.

        This function is expected to be used as a decorator for a
        capability implementation.

        Raises
        ------
        RuntimeError:
            When capability is registered more that once.
        """
        if name in self.capabilities:
            raise RuntimeError(f"{name} already registered")

        def decorator(
            func: CapabilityCallable,
        ) -> CapabilityCallable:
            validate_capability(name, func)
            self.capabilities[name] = func
            return func

        return decorator

    def dispatch(self, name: CapabilityName, request_string: str) -> str:
        """Call implemented capability, returning the result.

        Raises
        ------
        NotImplementedError:
            When capability is not implemented (or registered)
        """
        try:
            capability = self.capabilities[name]
        except KeyError:
            if self.handle_errors:
                return (
                    Response[EncounteredErrorResponse]
                    .from_error(
                        error=EncounteredErrorResponse(
                            message=f"Capability '{name.value}' is not implemented.",
                            error_code=ErrorCodes.NOT_IMPLEMENTED.value,
                        ),
                    )
                    .model_dump_json()
                )

            raise NotImplementedError from None

        request_annotation, _ = get_capability_annotations(capability)
        request = request_annotation(**json.loads(request_string))

        if inspect.iscoroutinefunction(capability):
            response = asyncio.run(
                async_exception_handler(self.exception_handlers, self.app_id)(capability)(request)
                if self.handle_errors
                else capability(request)
            )
        else:
            response = (
                sync_exception_handler(self.exception_handlers, self.app_id)(capability)(request)
                if self.handle_errors
                else capability(request)
            )

        return response.model_dump_json()

    def info(self) -> Info:
        """Provide information about implemented capabilities.

        Json schema describing implemented capabilities and their
        interface is returned. The authentication schema is also
        included.
        """
        capability_names = sorted(capability_name.value for capability_name in self.capabilities)
        return Info(
            app_id=self.app_id,
            capabilities=capability_names,
            # TODO: Remove None check once all connectors are migrated to new capability registration
            authentication_schema=self.auth.model_json_schema() if self.auth else {},
            capability_schema={
                capability_name: generate_capability_schema(
                    capability_name, self.capabilities[capability_name]
                )
                for capability_name in sorted(self.capabilities)
            },
            logo_url=self.description_data.logo_url,
            user_friendly_name=self.description_data.user_friendly_name,
            description=self.description_data.description,
            categories=self.description_data.categories,
        )

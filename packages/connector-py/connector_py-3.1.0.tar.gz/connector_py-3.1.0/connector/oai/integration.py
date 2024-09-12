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
    * the types of accepted argument and returned value matches the
    capability interface
"""

import asyncio
import inspect
import json
import logging
import typing as t
from dataclasses import dataclass

from connector.generated import (
    AppCategory,
    BasicCredential,
    CapabilityName,
    CapabilitySchema,
    Error,
    ErrorCode,
    ErrorResponse,
    Info,
    InfoResponse,
    OAuthCredential,
)
from connector.oai.capability import (
    CapabilityCallableProto,
    generate_capability_schema,
    get_capability_annotations,
    validate_capability,
)
from connector.oai.errors import ErrorMap, handle_exception
from pydantic import BaseModel

AuthSetting: t.TypeAlias = t.Union[
    t.Type[OAuthCredential],
    t.Type[BasicCredential],
]

logger = logging.getLogger(__name__)


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
        self.auth = auth
        self.exception_handlers = exception_handlers
        self.handle_errors = handle_errors
        self.description_data = description_data or DescriptionData()

        if len(self.app_id) == 0:
            raise ValueError("'app_id' must not be empty")

        self.capabilities: dict[CapabilityName, CapabilityCallableProto[t.Any]] = {}

    def register_capability(
        self,
        name: CapabilityName,
    ) -> t.Callable[
        [CapabilityCallableProto[t.Any]],
        CapabilityCallableProto[t.Any],
    ]:
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
            func: CapabilityCallableProto[t.Any],
        ) -> CapabilityCallableProto[t.Any]:
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
                return ErrorResponse(
                    is_error=True,
                    error=Error(
                        message=f"Capability '{name.value}' is not implemented.",
                        error_code="connector.not_implemented",
                        std_error=ErrorCode.NOT_IMPLEMENTED,
                    ),
                ).model_dump_json()

            raise NotImplementedError from None

        request_annotation, _ = get_capability_annotations(capability)
        request = request_annotation(**json.loads(request_string))

        try:
            if inspect.iscoroutinefunction(capability):
                response = asyncio.run(
                    capability(request) if self.handle_errors else capability(request)
                )
            else:
                response = t.cast(
                    BaseModel,
                    (capability(request) if self.handle_errors else capability(request)),
                )

            return response.model_dump_json()
        except Exception as e:
            return handle_exception(
                self.exception_handlers, e, capability, self.app_id
            ).model_dump_json()

    def info(self) -> InfoResponse:
        """Provide information about implemented capabilities.

        Json schema describing implemented capabilities and their
        interface is returned. The authentication schema is also
        included.
        """
        capability_names = sorted(self.capabilities.keys())
        capability_schema: dict[str, CapabilitySchema] = {}
        for capability_name in capability_names:
            command_types = generate_capability_schema(
                capability_name, self.capabilities[capability_name]
            )
            capability_schema[capability_name] = CapabilitySchema(
                argument=command_types.argument,
                output=command_types.output,
            )
        return InfoResponse(
            response=Info(
                app_id=self.app_id,
                capabilities=capability_names,
                capability_schema=capability_schema,
                logo_url=self.description_data.logo_url,
                user_friendly_name=self.description_data.user_friendly_name,
                description=self.description_data.description,
                categories=self.description_data.categories,
            )
        )

"""Tests for ``connector.capability`` module.

Todo
----
* generate_capability_schema
"""

import typing as t

import pytest
import pytest_cases
from connector.capability import (
    CapabilityName,
    get_capability_annotations,
    validate_capability,
)
from connector.serializers.request import Request, RequestData
from connector.serializers.response import Response, ResponseData


@pytest_cases.parametrize_with_cases(
    ["capability", "expected_annotations"],
    cases=[
        "tests.test_get_capability_annotations_cases",
    ],
    has_tag="correct",
)
def test_get_capability_annotations(
    capability: t.Callable[[Request[RequestData]], Response[ResponseData]],
    expected_annotations: tuple[Request[RequestData], Response[ResponseData]],
) -> None:
    """Test if annotations are correctly get from capability."""
    actual_annotations = get_capability_annotations(capability)
    assert actual_annotations == expected_annotations


@pytest_cases.parametrize_with_cases(
    ["capability"],
    cases=[
        "tests.test_get_capability_annotations_cases",
    ],
    has_tag="missing_annotation",
)
def test_get_capability_annotations_type_error(
    capability: t.Callable[[Request[RequestData]], Response[ResponseData]],
) -> None:
    """Test if incorrectly typed capability raises error."""
    with pytest.raises(TypeError):
        get_capability_annotations(capability)


@pytest_cases.parametrize_with_cases(
    ["capability_name", "capability"],
    cases=[
        "tests.test_validate_capability_cases",
    ],
    has_tag="valid",
)
def test_validate_capability(
    capability_name: CapabilityName,
    capability: t.Callable[[Request[RequestData]], Response[ResponseData]],
) -> None:
    """Test if valid capability is marked as valid."""
    validate_capability(capability_name, capability)


@pytest_cases.parametrize_with_cases(
    ["capability_name", "capability"],
    cases=[
        "tests.test_validate_capability_cases",
    ],
    has_tag="invalid",
)
def test_validate_capability_invalid(
    capability_name: CapabilityName,
    capability: t.Callable[[Request[RequestData]], Response[ResponseData]],
) -> None:
    """Test if valid capability is marked as valid."""
    with pytest.raises(TypeError):
        validate_capability(capability_name, capability)


@pytest_cases.parametrize_with_cases(
    ["capability"],
    cases=[
        "tests.test_get_capability_annotations_cases",
    ],
    has_tag="missing_annotation",
)
def test_validate_capability_missing_annotation(
    capability: t.Callable[[Request[RequestData]], Response[ResponseData]],
) -> None:
    """Test if valid capability is marked as valid.

    We just pass any capability_name just to make function happy,
    however, ``validate_capability`` should raise before it touches the
    name.
    """
    capability_name = CapabilityName.VALIDATE_CREDENTIALS
    with pytest.raises(TypeError):
        validate_capability(capability_name, capability)

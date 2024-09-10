# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .application_configuration_param import ApplicationConfigurationParam

__all__ = [
    "ApplicationVariantCreateParams",
    "OnlineApplicationVariantRequest",
    "OfflineApplicationVariantRequest",
    "OfflineApplicationVariantRequestConfiguration",
]


class OnlineApplicationVariantRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[ApplicationConfigurationParam]

    name: Required[str]

    version: Required[Literal["V0"]]

    description: str
    """Optional description of the application variant"""


class OfflineApplicationVariantRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[OfflineApplicationVariantRequestConfiguration]

    name: Required[str]

    version: Required[Literal["OFFLINE"]]

    description: str
    """Optional description of the application variant"""


class OfflineApplicationVariantRequestConfiguration(TypedDict, total=False):
    metadata: object
    """User defined metadata about the offline application"""

    output_schema_type: Literal["completion_only", "context_string", "context_chunks"]
    """An enumeration."""


ApplicationVariantCreateParams: TypeAlias = Union[OnlineApplicationVariantRequest, OfflineApplicationVariantRequest]

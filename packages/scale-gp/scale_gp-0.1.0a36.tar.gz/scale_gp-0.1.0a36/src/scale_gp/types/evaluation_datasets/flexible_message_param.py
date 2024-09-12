# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "FlexibleMessageParam",
    "EgpAPIBackendServerInternalEntitiesUserMessage",
    "EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class EgpAPIBackendServerInternalEntitiesUserMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["user"]


class EgpAPIBackendServerInternalEntitiesAssistantMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["assistant"]


class EgpAPIBackendServerInternalEntitiesSystemMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["system"]


FlexibleMessageParam: TypeAlias = Union[
    EgpAPIBackendServerInternalEntitiesUserMessage,
    EgpAPIBackendServerInternalEntitiesAssistantMessage,
    EgpAPIBackendServerInternalEntitiesSystemMessage,
]

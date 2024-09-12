# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "FlexibleMessages",
    "EgpAPIBackendServerInternalEntitiesUserMessage",
    "EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleMessages: TypeAlias = Annotated[
    Union[
        EgpAPIBackendServerInternalEntitiesUserMessage,
        EgpAPIBackendServerInternalEntitiesAssistantMessage,
        EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

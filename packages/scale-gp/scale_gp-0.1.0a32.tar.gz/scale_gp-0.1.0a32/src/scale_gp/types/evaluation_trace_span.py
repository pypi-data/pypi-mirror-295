# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "EvaluationTraceSpan",
    "OperationInputArrayOfFlexibleIoChunk",
    "OperationInputArrayOfChatMessageV2",
    "OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "OperationOutputArrayOfFlexibleIoChunk",
    "OperationOutputArrayOfChatMessageV2",
    "OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "OperationExpectedArrayOfFlexibleIoChunk",
    "OperationExpectedArrayOfChatMessageV2",
    "OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class OperationInputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


OperationInputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        OperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class OperationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


OperationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        OperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class OperationExpectedArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


OperationExpectedArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        OperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class EvaluationTraceSpan(BaseModel):
    id: str
    """Identifies the application step"""

    application_interaction_id: str
    """The id of the application insight this step belongs to"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_input: Dict[
        str,
        Union[
            str,
            float,
            List[OperationInputArrayOfFlexibleIoChunk],
            List[OperationInputArrayOfChatMessageV2],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the input that this step received."""

    operation_output: Dict[
        str,
        Union[
            str,
            float,
            List[OperationOutputArrayOfFlexibleIoChunk],
            List[OperationOutputArrayOfChatMessageV2],
            List[object],
            object,
        ],
    ]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "INPUT_GUARDRAIL",
        "OUTPUT_GUARDRAIL",
    ]
    """An enumeration."""

    start_timestamp: datetime
    """The start time of the step"""

    operation_expected: Optional[
        Dict[
            str,
            Union[
                str,
                float,
                List[OperationExpectedArrayOfFlexibleIoChunk],
                List[OperationExpectedArrayOfChatMessageV2],
                List[object],
                object,
            ],
        ]
    ] = None
    """The JSON representation of the expected output for this step"""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

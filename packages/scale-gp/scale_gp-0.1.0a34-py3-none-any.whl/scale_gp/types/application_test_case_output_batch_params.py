# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared_params.result_schema_generation import ResultSchemaGeneration
from .shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "ApplicationTestCaseOutputBatchParams",
    "Item",
    "ItemOutput",
    "ItemOutputResultSchemaFlexible",
    "ItemOutputResultSchemaFlexibleGenerationOutputArrayOfFlexibleIoChunk",
    "ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2",
    "ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemOutputResultSchemaFlexibleGenerationExtraInfo",
    "ItemTraceSpan",
    "ItemTraceSpanOperationInputArrayOfFlexibleIoChunk",
    "ItemTraceSpanOperationInputArrayOfChatMessageV2",
    "ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemTraceSpanOperationOutputArrayOfFlexibleIoChunk",
    "ItemTraceSpanOperationOutputArrayOfChatMessageV2",
    "ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemTraceSpanOperationExpectedArrayOfFlexibleIoChunk",
    "ItemTraceSpanOperationExpectedArrayOfChatMessageV2",
    "ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class ApplicationTestCaseOutputBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class ItemOutputResultSchemaFlexibleGenerationOutputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2: TypeAlias = Union[
    ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]

ItemOutputResultSchemaFlexibleGenerationExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ItemOutputResultSchemaFlexible(TypedDict, total=False):
    generation_output: Required[
        Union[
            str,
            float,
            Iterable[ItemOutputResultSchemaFlexibleGenerationOutputArrayOfFlexibleIoChunk],
            Iterable[ItemOutputResultSchemaFlexibleGenerationOutputArrayOfChatMessageV2],
            Iterable[object],
            Dict[
                str,
                Union[
                    str,
                    float,
                    Iterable[
                        ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                    ],
                    Iterable[
                        ItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemOutputResultSchemaFlexibleGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                    ],
                    Iterable[object],
                    object,
                ],
            ],
            object,
        ]
    ]

    generation_extra_info: ItemOutputResultSchemaFlexibleGenerationExtraInfo


ItemOutput: TypeAlias = Union[ResultSchemaGeneration, ItemOutputResultSchemaFlexible]


class ItemTraceSpanOperationInputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTraceSpanOperationInputArrayOfChatMessageV2: TypeAlias = Union[
    ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTraceSpanOperationInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTraceSpanOperationOutputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTraceSpanOperationOutputArrayOfChatMessageV2: TypeAlias = Union[
    ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTraceSpanOperationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTraceSpanOperationExpectedArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTraceSpanOperationExpectedArrayOfChatMessageV2: TypeAlias = Union[
    ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTraceSpanOperationExpectedArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTraceSpan(TypedDict, total=False):
    node_id: Required[str]
    """Identifier for the node that emitted this trace span."""

    operation_input: Required[
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[ItemTraceSpanOperationInputArrayOfFlexibleIoChunk],
                Iterable[ItemTraceSpanOperationInputArrayOfChatMessageV2],
                Iterable[object],
                object,
            ],
        ]
    ]
    """The JSON representation of the input that this step received."""

    operation_output: Required[
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[ItemTraceSpanOperationOutputArrayOfFlexibleIoChunk],
                Iterable[ItemTraceSpanOperationOutputArrayOfChatMessageV2],
                Iterable[object],
                object,
            ],
        ]
    ]
    """The JSON representation of the output that this step emitted."""

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """The start time of the step."""

    duration_ms: int
    """The duration of the operation step in milliseconds."""

    operation_expected: Dict[
        str,
        Union[
            str,
            float,
            Iterable[ItemTraceSpanOperationExpectedArrayOfFlexibleIoChunk],
            Iterable[ItemTraceSpanOperationExpectedArrayOfChatMessageV2],
            Iterable[object],
            object,
        ],
    ]
    """The JSON representation of the expected output for this step"""

    operation_metadata: object
    """The JSON representation of the metadata insights emitted during execution.

    This can differ based on different types of operations.
    """

    operation_status: Literal["SUCCESS", "ERROR"]
    """Enum representing the status of an operation."""

    operation_type: Literal["COMPLETION", "RERANKING", "RETRIEVAL", "CUSTOM"]
    """Enum representing the type of operation performed."""


class Item(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_variant_id: Required[str]

    evaluation_dataset_version_num: Required[int]

    output: Required[ItemOutput]

    test_case_id: Required[str]

    application_interaction_id: str

    metrics: Dict[str, float]

    trace_spans: Iterable[ItemTraceSpan]
    """List of trace spans associated with the application's execution.

    These spans provide insight into the individual steps taken by nodes involved in
    generating the output.
    """

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .schema_generation_base_param import SchemaGenerationBaseParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "TestCaseBatchParams",
    "Item",
    "ItemTestCaseData",
    "ItemTestCaseDataSchemaFlexible",
    "ItemTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk",
    "ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2",
    "ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedExtraInfo",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class TestCaseBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class ItemTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2: TypeAlias = Union[
    ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]

ItemTestCaseDataSchemaFlexibleExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2: TypeAlias = Union[
    ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ItemTestCaseDataSchemaFlexible(TypedDict, total=False):
    input: Required[
        Union[
            str,
            float,
            Iterable[ItemTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk],
            Iterable[ItemTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2],
            Iterable[object],
            Dict[
                str,
                Union[
                    str,
                    float,
                    Iterable[
                        ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                    ],
                    Iterable[
                        ItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                    ],
                    Iterable[object],
                    object,
                ],
            ],
            object,
        ]
    ]

    expected_extra_info: ItemTestCaseDataSchemaFlexibleExpectedExtraInfo

    expected_output: Union[
        str,
        float,
        Iterable[ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk],
        Iterable[ItemTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2],
        Iterable[object],
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[
                    ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                Iterable[
                    ItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                Iterable[object],
                object,
            ],
        ],
        object,
    ]


ItemTestCaseData: TypeAlias = Union[
    ArtifactSchemaGenerationParam, SchemaGenerationBaseParam, ItemTestCaseDataSchemaFlexible
]


class Item(TypedDict, total=False):
    test_case_data: Required[ItemTestCaseData]
    """The data for the test case in a format matching the provided schema_type"""

    account_id: str
    """The ID of the account that owns the given entity."""

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    test_case_metadata: object
    """Metadata for the test case"""

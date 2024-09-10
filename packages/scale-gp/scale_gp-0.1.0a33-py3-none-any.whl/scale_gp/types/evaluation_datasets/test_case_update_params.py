# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .schema_generation_base_param import SchemaGenerationBaseParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "TestCaseUpdateParams",
    "PartialTestCaseVersionRequest",
    "PartialTestCaseVersionRequestTestCaseData",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexible",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedExtraInfo",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "RestoreRequest",
]


class PartialTestCaseVersionRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    test_case_data: PartialTestCaseVersionRequestTestCaseData
    """The data for the test case in a format matching the provided schema_type"""

    test_case_metadata: object
    """Metadata for the test case"""


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2: TypeAlias = Union[
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]

PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedExtraInfo: TypeAlias = Union[
    ChunkExtraInfoSchema, StringExtraInfoSchema
]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2: TypeAlias = Union[
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class PartialTestCaseVersionRequestTestCaseDataSchemaFlexible(TypedDict, total=False):
    input: Required[
        Union[
            str,
            float,
            Iterable[PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk],
            Iterable[PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputArrayOfChatMessageV2],
            Iterable[object],
            Dict[
                str,
                Union[
                    str,
                    float,
                    Iterable[
                        PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                    ],
                    Iterable[
                        PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                    ],
                    Iterable[object],
                    object,
                ],
            ],
            object,
        ]
    ]

    expected_extra_info: PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedExtraInfo

    expected_output: Union[
        str,
        float,
        Iterable[PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk],
        Iterable[PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2],
        Iterable[object],
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[
                    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                Iterable[
                    PartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesPartialTestCaseVersionRequestTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                Iterable[object],
                object,
            ],
        ],
        object,
    ]


PartialTestCaseVersionRequestTestCaseData: TypeAlias = Union[
    ArtifactSchemaGenerationParam, SchemaGenerationBaseParam, PartialTestCaseVersionRequestTestCaseDataSchemaFlexible
]


class RestoreRequest(TypedDict, total=False):
    evaluation_dataset_id: Required[str]

    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


TestCaseUpdateParams: TypeAlias = Union[PartialTestCaseVersionRequest, RestoreRequest]

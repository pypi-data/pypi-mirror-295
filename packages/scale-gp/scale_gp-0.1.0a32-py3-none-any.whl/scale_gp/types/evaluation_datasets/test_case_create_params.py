# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .schema_generation_base_param import SchemaGenerationBaseParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "TestCaseCreateParams",
    "TestCaseData",
    "TestCaseDataSchemaFlexible",
    "TestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk",
    "TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2",
    "TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "TestCaseDataSchemaFlexibleExpectedExtraInfo",
    "TestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk",
    "TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2",
    "TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class TestCaseCreateParams(TypedDict, total=False):
    test_case_data: Required[TestCaseData]
    """The data for the test case in a format matching the provided schema_type"""

    account_id: str
    """The ID of the account that owns the given entity."""

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    test_case_metadata: object
    """Metadata for the test case"""


class TestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2: TypeAlias = Union[
    TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]

TestCaseDataSchemaFlexibleExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class TestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2: TypeAlias = Union[
    TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class TestCaseDataSchemaFlexible(TypedDict, total=False):
    input: Required[
        Union[
            str,
            float,
            Iterable[TestCaseDataSchemaFlexibleInputArrayOfFlexibleIoChunk],
            Iterable[TestCaseDataSchemaFlexibleInputArrayOfChatMessageV2],
            Iterable[object],
            Dict[
                str,
                Union[
                    str,
                    float,
                    Iterable[
                        TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                    ],
                    Iterable[
                        TestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleInputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                    ],
                    Iterable[object],
                    object,
                ],
            ],
            object,
        ]
    ]

    expected_extra_info: TestCaseDataSchemaFlexibleExpectedExtraInfo

    expected_output: Union[
        str,
        float,
        Iterable[TestCaseDataSchemaFlexibleExpectedOutputArrayOfFlexibleIoChunk],
        Iterable[TestCaseDataSchemaFlexibleExpectedOutputArrayOfChatMessageV2],
        Iterable[object],
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[
                    TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                Iterable[
                    TestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesTestCaseDataSchemaFlexibleExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                Iterable[object],
                object,
            ],
        ],
        object,
    ]


TestCaseData: TypeAlias = Union[ArtifactSchemaGenerationParam, SchemaGenerationBaseParam, TestCaseDataSchemaFlexible]
